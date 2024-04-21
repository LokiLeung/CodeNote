![82e144e7c4b41afc669a5032c2de5e0](./Android9超过2G升级包无法升级问题排查.assets/82e144e7c4b41afc669a5032c2de5e0.jpg)

### 问题描述

Android9系统，当升级包大小超过2G的时候，升级失败。

### 原因分析

### update_engine报错

```
04-27 11:09:50.511 2293 2293 E update_engine:[0427/110950.511596:ERROR:payload_metadata.cc(74)] Bad payload format -- invalid delta magic.
04-27 11:09:50.511 2293 2293 E update_engine:[0427/110950.511679:ERROR:download_action.cc(337)] Error ErrorCode::kDownloadInvalidMetadataMagicString (21) in DeltaPerformet's Write method when processing the received payload -- Terminating processing
```

通过日志可以看出update_engine报错错误码kDownloadInvalidMetadataMagicString（21），通过查阅update_engine源码得知，在update_engine中是因为解析出来的payload.bin前面的元数据不是'CrAU'（Android源码定义的就是CrAU）导致；

### 升级包偏移量

通过参考资料得知：

- .zip文件的文件格式中，会在生成一定的头部信息，然后内部的文件会按一定规则顺序排列在后面；
- 压缩包内容中，头部有30个字节是固定的，然后后面就到文件名（可变长度）、拓展区（可变长度），这些加起来就是头部内容的长度。

> 参考： [Android A/B System OTA分析（六）如何获取 payload 的 offset 和 size_packageoffset size_洛奇看世界的博客-CSDN博客](https://blog.csdn.net/guyongqiangx/article/details/122498561)

metadata数据中的偏移量与升级包实际的偏移量对不上，这个偏移量其实指的是压缩包内文件数据(payload.bin)在文件（升级包）中的偏移量。系统打包的时候会将这个偏移量解析出来写在metadata中，而update_engine会根据metadata文件中定义的这个偏移量提取payload.bin，并判断payload.bin的前4个字节是不是'CrAU'，如果提取出来的payload.bin的前4个字节与'CrAU'不匹配，则证明偏移量错误，导致提取的payload.bin文件不正确； 

既然得知这原理，后面主要是看针对一个问题：

**一个问题：为什么metadata中的偏移量和实际压缩包的偏移量对应不上？ --> metadata的偏移量是如何生成的？**

### metadata的偏移量是如何生成？

从打包的python脚本ota_from_target_files.py入手，具体的排查过程不赘述。

最终排查到这个偏移量的计算有两处：其中一处是用于解析偏移量，一处是用来做重新计算校验的（因为解析之后经过了一些签名之类的处理，所以重新校验）。这里能校验过，是因为解析和校验用的接口和公式是一致的。

```
    payload_offset = payload_info.header_offset + len(payload_info.FileHeader()) // 计算
    offset = info.header_ofet + len(info.FileHeader()) // 生成
```

通过在python脚本添加打印得知， 升级包无论大于或小于2G：

- payload_info.header_offset、 info.header_ofet均不变，len(payload_info.FileHeader())、len(info.FileHeader())均改变了；
- payload_info.header_offset和info.header_ofet是文件在压缩包本身的偏移量（例如如果文件在压缩包排在第2个，它本身的偏移量就要加上第一个文件占用的部分）；
-  len(payload_info.FileHeader())、len(info.FileHeader())是压缩包内此文件的头部。这两部分偏移量加起来， 才是这文件在压缩包中要提取的数据；

制作一个超过2G的升级包，并通过imhex工具查看升级包、zipinfo命令查看压缩包信息，均发现**payload.bin在压缩包的偏移量为47，但是通过python打印出来的是67。**

因此继续查阅python代码，最终发现fileHeader的extra拓展区部分在大于2G的时候，额外计算多了一部分信息。下面代码会对升级包进行判断，若文件大小或者压缩包大小大于ZIP64_LIMIT大小，则认为是zip64；若属于zip64，会在extra拓展区部分额外增加了一部分数据。通过打印复现，把这部分数据减掉，刚好是实际压缩包的47。

```
if zip64 is None:
    zip64 = file_size > ZIP64_LIMIT or compress_size > ZIP64_LIMIT # 这里的ZIP64_LIMIT是2G
    if zip64:
        fmt = '<HHQQ'
        extra = extra + struct.pack(fmt,
                                    1, struct.calcsize(fmt)-4, file_size, compress_size)
```

这里便是metadata中偏移量的计算，那么在打包时，payload.bin又是如何打进zip的呢？

### payload.bin的实际偏移量由来？

从打包的python脚本ota_from_target_files.py入手，具体的排查过程不赘述。最终排查到common.py的ZipWrite方法。

通过注释的意思和代码，可以得知，Android为了能够编译出2G以上的包，将zipFile的ZIP64_LIMIT改为了4G，这个ZIP64_LIMIT就上面用来判断是否为zip64的一个条件。

zip_file.write在python中同样用到了FileHeader()方法，但是写入的时候因为小于4G，不认为是zip64，所以extra另外的那一部分数据没有写入，但是在解析的时候却认为是zip64，导致写入和解析所获取的长度不一致。update_engine根据metadata的偏移量解析出来的payload.bin自然就不正确了。

**总结：脚本在写入升级包是，认为文件<4G，使用zip32格式写入，解析升级包时认为文件>2G，按照zip64格式解析计算偏移量，最终导致metadata中的偏移量偏大。**

```
def ZipWrite(zip_file, filename, arcname=None, perms=0o644,
             compress_type=None):
  import datetime

  # http://b/18015246
  # Python 2.7's zipfile implementation wrongly thinks that zip64 is required
  # for files larger than 2GiB. We can work around this by adjusting their
  # limit. Note that `zipfile.writestr()` will not work for strings larger than
  # 2GiB. The Python interpreter sometimes rejects strings that large (though
  # it isn't clear to me exactly what circumstances cause this).
  # `zipfile.write()` must be used directly to work around this.
  #
  # This mess can be avoided if we port to python3.
  saved_zip64_limit = zipfile.ZIP64_LIMIT
  zipfile.ZIP64_LIMIT = (1 << 32) - 1

  if compress_type is None:
    compress_type = zip_file.compression
  if arcname is None:
    arcname = filename

  saved_stat = os.stat(filename)

  try:
    # `zipfile.write()` doesn't allow us to pass ZipInfo, so just modify the
    # file to be zipped and reset it when we're done.
    os.chmod(filename, perms)

    # Use a fixed timestamp so the output is repeatable.
    epoch = datetime.datetime.fromtimestamp(0)
    timestamp = (datetime.datetime(2009, 1, 1) - epoch).total_seconds()
    os.utime(filename, (timestamp, timestamp))

    zip_file.write(filename, arcname=arcname, compress_type=compress_type)
  finally:
    os.chmod(filename, saved_stat.st_mode)
    os.utime(filename, (saved_stat.st_atime, saved_stat.st_mtime))
    zipfile.ZIP64_LIMIT = saved_zip64_limit
```

## 解决方法

### 方法1：

既然知道是因为python的FileHeader()会在文件头部的拓展区部分额外增加了导致的，那可以直接根据zip压缩包的结构，将公式改为

```
offset = info.header_offset + info.filename.__len__() + info.extra.__len__() + 30
# 可以参考上面提供的链接文章， 30这里是头部的固定长度， 但是尽量推荐下面官方的解决办法
```

### 方法2（推荐解决方法）：

根据AOSP官方代码库的修改记录，移植相关方法。

>  Commit:25ab998 Fix a bug in computing streaming property of payload.bin When computing the data offset of an entry in zip file, we used length of extra field from central directory. That is correct most of the time but wrong if the extra field in central directory has different length than the one in local file directory. Since python's zipfile doesn't provide an API to access local file header, we need to parse local file header ourselves and extract length of extra field. An incorrect offset will cause magic mismatch error from update_engine, as update_engine expects to find uncompressed payload at the recorded offset. Test: th, partner verification Bug: 191443484 Change-Id: Id670cd79b0bd65adffaaa5224ae4f8065d66b358、 zhangkelvin@google.com(author) eventCommitted on2021-07-28 11:40 PM

因为本地代码和2021-07的代码还是存在较大差异。仅移植需要用到的部分。

ota_from_target_files.py方法增加以下改动（megre部分）

```
# ************** merge start *************
# https://cs.android.com/android/_/android/platform/build/+/928c2341a6abc3b1ddb7ddd7652e78b67c7ef7a9
def GetZipEntryOffset(zfp, entry_info):
  """Get offset to a beginning of a particular zip entry
  Args:
    fp: zipfile.ZipFile
    entry_info: zipfile.ZipInfo

  Returns:
    (offset, size) tuple
  """
  # Don't use len(entry_info.extra). Because that returns size of extra
  # fields in central directory. We need to look at local file directory,
  # as these two might have different sizes.

  # We cannot work with zipfile.ZipFile instances, we need a |fp| for the underlying file.
  zfp = zfp.fp
  zfp.seek(entry_info.header_offset)
  data = zfp.read(zipfile.sizeFileHeader)
  fheader = struct.unpack(zipfile.structFileHeader, data)
  # Last two fields of local file header are filename length and
  # extra length
  filename_len = fheader[-2]
  extra_len = fheader[-1]
  offset = entry_info.header_offset
  offset += zipfile.sizeFileHeader
  offset += filename_len + extra_len
  size = entry_info.file_size
  return (offset, size)
# ************** merge end *************
def ComputeEntryOffsetSize(name):
    """Computes the zip entry offset and size."""
    info = zip_file.getinfo(name)
    # offset = info.header_offset + len(info.FileHeader())
    # ************** merge start *************
    # merge 928c234 Allow zip64 support when opening zip files start
    # https://cs.android.com/android/_/android/platform/build/+/928c2341a6abc3b1ddb7ddd7652e78b67c7ef7a9
    (offset, size) = GetZipEntryOffset(zip_file, info)
    # offset = info.header_offset + info.filename.__len__() + info.extra.__len__() + 30
    # size = info.file_size
    # ************** merge end *************
    return '%s:%d:%d' % (os.path.basename(name), offset, size)
	payload_info = input_zip.getinfo('payload.bin')
    
    # ************** merge start *************
    # ---- by Y4944 2023/07/21
    # https://cs.android.com/android/_/android/platform/build/+/928c2341a6abc3b1ddb7ddd7652e78b67c7ef7a9
    # payload_offset = payload_info.header_offset + len(payload_info.FileHeader())
    (payload_offset, payload_size) = GetZipEntryOffset(input_zip, payload_info)
    # payload_offset = payload_info.header_offset + payload_info.filename.__len__() + payload_info.extra.__len__() + 30
    # payload_size = payload_info.file_size
    # ************** merge end *************

    with input_zip.open('payload.bin', 'r') as payload_fp:
      header_bin = payload_fp.read(24)

    # network byte order (big-endian)
    header = struct.unpack("!IQQL", header_bin)

    # 'CrAU'
    magic = header[0]
    assert magic == 0x43724155, "Invalid magic: {:x}".format(magic)

    manifest_size = header[2]
    metadata_signature_size = header[3]
    metadata_total = 24 + manifest_size + metadata_signature_size
    assert metadata_total < payload_size

    return (payload_offset, metadata_total)
```
# Android常用签名方式及签名转换技巧



## 基本知识

1. 常用的Android签名有.keystore，.jks，.pk8，.x509.pem
2. .keystore: Java KeyStore 文件，安全证书（授权证书或公钥证书）以及相应的私钥的存储库；
3. .jks: Java KeyStore 文件，Java KeyStore有多种实现方式， jks是其中一半， 在Java8中， jks也是默认的keystore方式；
4. .pk8: 通常包含私钥的 DER 格式文件，用于 Android 系统的代码签名；
5. .x509.pem: 包含公钥或证书的 PEM 格式文件，通常用于验证和加密；
6. platform.pk8和platform.x509.pem在android/build/target/product/security文件夹下可以找到；
7. 其他更多一些关于Android签名的基础知识，可以查看官网介绍https://source.android.com/devices/tech/ota/sign_builds.html



## 签名使用方法

### 使用platform.pk8和platform.x509.pem + 命令签名

准备好以下要素：

1. java环境；
2. signapk.jar；
3. platform.x509.pem；
4.  platform.pk8；

> signapk源码在/build/tools/signapk/下， 可以服务器单编此模块后，在/out/host/linux-x86/framework文件夹下找到；
>
> platform.pk8和platform.x509.pem在android/build/target/product/security文件夹下可以找到；

```shell
java -jar signapk.jar platform.x509.pem platform.pk8 apk-unsigned.apk apk-signed.apk
```



### 使用.keystore或.jks + gradle签名

> 使用.keystore和.jks，需要提供.keystore和.jks的相关信息，以便在gradle中引入

```groovy
// 引入签名 , 标注好相关信息
signingConfigs {
    debug {
        storeFile file('SignDemo.jks')
        storePassword '123456'
        keyAlias 'SignDemo'
        keyPassword '123456'
    }
    release {
        storeFile file('SignDemo.jks')
        storePassword '123456'
        keyAlias 'SignDemo'
        keyPassword '123456'
    }
}

buildTypes {
    debug{
        // 添加以下代码，以便编译debug版本时，自动签名
        signingConfig signingConfigs.debug
    }
    release {
        // 添加以下代码，以便编译release版本时，自动签名
        signingConfig signingConfigs.release
    }
}
```



### 使用.keystore或.jks + jarsigner命令签名

```shell
jarsigner -verbose -keystore platform.keystore demo.apk alias1（这里要补充一下别名）
输入密钥库的密码短语: (这里输入password)
```



### 使用.keystore或.jks + Android Studio签名

1. 点击Build -> Generate Signed Bundle / APK -> 弹窗选择APK -> Next -> 选择.keystore或.jks签名文件 -> 输入store密码、key密码、key别名；
2. 点击确认后自动编译并生成签名后的APK。

![image-20240413210746013](./Android%E5%B8%B8%E7%94%A8%E7%AD%BE%E5%90%8D%E5%BC%80%E5%8F%91%E5%92%8C%E7%AD%BE%E5%90%8D%E8%BD%AC%E6%8D%A2%E6%8A%80%E5%B7%A7.assets/image-20240413210746013.png)

![image-20240413210756456](./Android%E5%B8%B8%E7%94%A8%E7%AD%BE%E5%90%8D%E5%BC%80%E5%8F%91%E5%92%8C%E7%AD%BE%E5%90%8D%E8%BD%AC%E6%8D%A2%E6%8A%80%E5%B7%A7.assets/image-20240413210756456.png)



### 使用Android.mk或者Android.bp进行签名

1. 使用Android.mk进行签名

```makefile
# 添加以下代码， 编译时使用platform签名
LOCAL_CERTIFICATE := platform
```



2. 使用Android.bp进行签名

```bp
# 添加以下代码， 编译时使用platform签名
certificate: "platform",
```





## 签名转换

### platform.pk8和platform.x509.pem 生成 .keystore、.jks

利用网上开源项目：https://github.com/getfatday/keytool-importkeypair， 使用 keytool-importantkeypair工具， 将platform.pk8和platform.x509.pem 转成platform.keystore；使用命令在linux环境生成platform.keystore即可；

> 这里的别名、密码等等，需要记下来，在引入签名文件时需要用到

```bash
:<<!
使用platform.pk8、platform.x509.pem生成.keystore
windows 上换行注意 只用LF，不能使用CR

命令详解:
./keytool-importkeypair -k system.keystore -p 123456 -pk8 platform.pk8 -cert platform.x509.pem -alias test
-k 表示要生成的 keystore 文件的名字，这里为 system.keystore
-p 表示要生成的 keystore 的密码，这里为 123456
-pk8 表示要导入的 platform.pk8 文件
-cert 表示要导入的platform.x509.pem
-alias 表示给生成的 keystore 取一个别名，这是命名为 test

!

# read -p "Please input password >>>: " password
# read -p "Please keystore name >>>: " keystore_name
# read -p "Please alias name >>>: " alias_name

#./keytool-importkeypair -k ./$keystore_name -p $password -pk8 platform.pk8 -cert platform.x509.pem -alias $alias_name


# name: platform.keystore or platform.jks
# password: android
# alias: android
./keytool-importkeypair -k platform.keystore -p android -pk8 platform.pk8 -cert platform.x509.pem -alias android
```



### .jks 、.keystore 转 platform.pk8和platform.x509.pem

1. 提供platform.keystore文件；
2. 使用以下脚本，转换签名

```bash
./convertKeyStoreToPk8AndPem.sh <your_keystore_file>
# 之后根据提示输入、目标密钥库口令、新口令、密钥库口令:
```



3. 脚本代码如下：

```bash
#!/bin/bash

# 检查命令是否存在
command -v keytool >/dev/null 2>&1 || { echo >&2 "keytool 工具未找到，请确保 JDK 已安装"; exit 1; }
command -v openssl >/dev/null 2>&1 || { echo >&2 "openssl 工具未找到，请确保已安装 OpenSSL"; exit 1; }

# 检查参数
if [ $# -ne 1 ]; then
  echo "用法: $0 <your_keystore_file>"
  exit 1
fi

# 检查 keystore 文件是否存在
if [ ! -f "$1" ]; then
  echo "指定的 keystore 文件不存在: $1"
  exit 1
fi

# 1. 将 keystore 文件转换为 PKCS12 格式
echo "正在将 keystore 文件转换为 PKCS12 格式..."
keytool -importkeystore -srckeystore "$1" -destkeystore tmp.p12 -srcstoretype JKS -deststoretype PKCS12 || { echo "转换失败"; exit 1; }
echo "转换完成"

# 2. 将 PKCS12 文件转换为 PEM 格式
echo "正在将 PKCS12 文件转换为 PEM 格式..."
openssl pkcs12 -in tmp.p12 -nodes -out tmp.rsa.pem || { echo "转换失败"; exit 1; }
echo "转换完成"

# 3. 提取证书和私钥
echo "正在提取证书和私钥..."
awk '/BEGIN PRIVATE KEY/,/END PRIVATE KEY/' tmp.rsa.pem > private.rsa.pem
awk '/BEGIN CERTIFICATE/,/END CERTIFICATE/' tmp.rsa.pem > cert.x509.pem
echo "提取完成"

# 4. 生成 PKCS8 格式的私钥
echo "正在生成 PKCS8 格式的私钥..."
openssl pkcs8 -topk8 -outform DER -in private.rsa.pem -inform PEM -out private.pk8 -nocrypt || { echo "转换失败"; exit 1; }
echo "转换完成"

# 清理临时文件
echo "清理临时文件..."
rm tmp.p12 tmp.rsa.pem private.rsa.pem
echo "清理完成"

echo "生成的 cert.x509.pem 和 private.pk8 文件即为转换后的结果"
```



### platform.pk8和platform.x509.pem 生成 .jks

1. 提供platform.pk8、platform.x509.pem 、signapk.jar， 并放在同一个目录下

2. 生成platform.pem文件 --> 生成platform.p12文件 --> 生成platform.jks文件


```bash
# 生成platform.pem文件
openssl pkcs8 -inform DER -nocrypt -in platform.pk8 -out platform.pem
# 生成platform.p12文件，需要设置别名和密码
openssl pkcs12 -export -in platform.x509.pem -out platform.p12 -inkey platform.pem -password pass:android -name key
# 生成platform.jks文件， -srcstorepass 设置jks文件的密码
keytool -importkeystore -deststorepass android -destkeystore ./platform.jks -srckeystore ./platform.p12 -srcstoretype PKCS12 -srcstorepass android
# 别名、密码、jks文件密码需要记下来，用于在Android Studio进行签名
```

> 也可以用上述keytool-importkeypair生成jks



## 参考

1. https://www.ibm.com/docs/en/was-liberty/nd?topic=configuration-keystore
2. https://developer.android.com/privacy-and-security/keystore?hl=zh-cn
3. https://source.android.com/docs/core/ota/sign_builds?hl=zh-cn#release-keys
4. https://en.wikipedia.org/wiki/Java_KeyStore
5. https://github.com/getfatday/keytool-importkeypair


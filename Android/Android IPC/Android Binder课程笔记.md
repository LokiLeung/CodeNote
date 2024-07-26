# Android Binder 课程笔记

> 此文章为课程学习笔记
>
> 结合[手撕Android 大厂面试必问Framework 底层通信：Binder IPC机制+Handler 消息机制 + Livedata 时间机制_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1tA4y1f7cf/?spm_id_from=333.337.search-card.all.click&vd_source=acb61e4b6fa95ff36b3893f0e348be69)课程食用



通信本质





## 面试题

### Q1 为什么Android要采用Binder做进程通信

（见Android IPC概述， 主要回答Linux常见的IPC机制和优缺点，最终针对什么情况才需要设计和实现Binder）

新技术的出现，一般都是因为旧技术无法满足现有需求才被发明出来的。Android系统是基于Linux系统上实现的。Linux系统常见的IPC机制有管道、共享内存、Socket等等。

管道是在系统内核空间建立一个管道，发送进程将数据写入管道，接收进程从管道读取数据，适用于1：1的关系，数据安全，但是每次通信需要复制2次，效率低；

共享内存是不同进程或多个进程共用一块内存，控制复杂，不需要重新拷贝，但是数据不安全；

Socket为C/S架构，通过端口转发机制实现，一般用于网络通信，拷贝效率较低；

基于这种情况，各种IPC机制均有不匹配的地方，因此设计Binder机制结合上面的优点进行通信。

### Q2 用户空间和内核空间区别

Linux系统将系统内存分为两个不同的区域，内核空间和用户空间。内核空间是Kernel运行并提供服务的区域；用户空间是内存中用户进程的运行部分。

进程是程序执行的实例。当一个程序要运行时，它被从存储器复制到用户空间，以便CPU（中央处理器）可以高速访问它。内核的作用之一是管理此空间内的各个用户进程，并防止它们相互干扰。

内核是构成计算机操作系统中心核心的程序。它不是一个进程，而是一个进程的控制器，它完全控制系统上发生的一切。这包括管理用户空间内的各个用户进程，并防止它们相互干扰。

用户进程只能通过使用系统调用来访问内核空间。系统调用是类 Unix 操作系统中由内核执行的服务的活动进程发出的请求，例如输入/输出 （I/O） 或进程创建。

### Q3 简单说说物理地址和虚拟地址



### Q4 Binder如何做到一次拷贝

### Q5 简单讲讲mmap原理

### Q6 内存中的一页是什么，你怎么理解的

### Q7 Binder传输数据的大小限制是多少

### Q8 Binder并发支持多少线程

### Q9 Android APP有多少Binder线程，是固定的么

### Q10 bindservice启动Service与Binder服务实体的流程

### Q11 Java层Binder实体与与BinderProxy是如何实例化及使用的，与Native层的关系是怎样的

### Q12 Binder如何找到目标进程





为什么Android不采用Linux已有的进程通信，而是另辟蹊径弄一个binder(或者你认为binder是独有的吗)

Binder机制发生在哪个进程(或者 binder机制是发生在system_server进程，还是service_manager进程)。

Binder-次拷贝原理是什么(或者binder通信的效率为什么如此高效)

Binder传输数据的大小限制 传输Bitmap过大，就会崩溃的原因，Activity之间传输BitMap

为什么会有内核空间，和用户空间，设置内核空间的意义是什么

你了解mmap函数吗，说说他的机制是什么

什么是物理内存，什么是虚拟内存

Android APP进程天生支持Binder通信的原理是什么

Android APP有多少Binder线程，是因定的么

Binder线程的睡眠与唤醒(请求线程睡在哪个等待队列上，唤醒目标端哪个队列上的线程)

Binder协议中BC与BR的区别

Binder在传输数据的时候是如何层层封装的-不同层次使用的数据结构(命令的封装)

Binder驱动传递数据的释放(释放时机)

一个简单的Binder通信C/S模型
ServiceManager addService的限制(并非服务都能使用ServiceManager的addService)

bindService启动Service与Binder服务实体的流程

Java层Binder实体与与BinderProxy是如何实例化及使用的，与Native层的关系是怎样的

Parcel readStrongBinder与writeStrongBinder的原理





## 参考

1. [Kernel Space Definition (linfo.org)](https://www.linfo.org/kernel_space.html)
2. [[User Space Definition (linfo.org)](https://www.linfo.org/user_space.html)](https://www.linfo.org/user_space.html)
3. [Process definition by The Linux Information Project (LINFO)](https://www.linfo.org/process.html)
# Android Binder 课程笔记

> 此文章为课程学习笔记
>
> 结合[手撕Android 大厂面试必问Framework 底层通信：Binder IPC机制+Handler 消息机制 + Livedata 时间机制_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1tA4y1f7cf/?spm_id_from=333.337.search-card.all.click&vd_source=acb61e4b6fa95ff36b3893f0e348be69)课程食用



### Q1：为什么Android Binder不采用Linux IPC机制？

> 侧重点：Linux IPC机制种类、原理和特性， Binder机制的优势。
>
> 新技术的产生，基本都是源于需求；

1. Linux IPC机制包括管道、共享内存、Socket、文件传输等；

2. 管道的基本原理

   > [进程间的通信方式——pipe（管道）-CSDN博客](https://blog.csdn.net/skyroben/article/details/71513385)

3. 共享内存

   > [【操作系统/进程间通信】共享内存-原理和实现_内存共享和保护机制-CSDN博客](https://blog.csdn.net/icecreamTong/article/details/130656475)

4. Socket原理

   > [Socket（套接字）通信原理 - codedot - 博客园 (cnblogs.com)](https://www.cnblogs.com/myitnews/p/13790067.html)

5. 
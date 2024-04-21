![进程CPU占用率过高排查流程笔记](./进程CPU占用率过高排查流程笔记.assets/进程CPU占用率过高排查流程笔记-1713678100919-1.jpg)

## 问题描述

top命令查看当前进程CPU过高

进程名：android.hardware.automotive.vehicle@2.0-service

版本：Android11

```bash
Tasks: 372 total,   4 running, 368 sleeping,   0 stopped,   0 zombie
  Mem:  8047016K total,  6529068K used,  1517948K free,   135968K buffers
 Swap:  4194300K total,         0 used,  4194300K free,  1814164K cached
800%cpu 297%user  40%nice 307%sys 136%idle   8%iow   9%irq   4%sirq   0%host
   PID USER         PR  NI VIRT  RES  SHR S[%CPU] %MEM     TIME+ ARGS                                                                                                                                                                                                         
  1175 system       18  -2  17G 306M 173M S  100   3.8  19:42.93 system_server
 19281 vehicle_net+ 20   0  12G  10M 6.4M S 49.1   0.1   5:46.15 android.hardware.automotive.vehicle@2.0-service
   276 logd         30  10  12G 174M 2.7M S 35.4   2.2   7:19.32 logd
```



## 排查流程
### 查看进程CPU占用率

```bash
console:/ # top -p 19281
Tasks: 1 total,   0 running,   1 sleeping,   0 stopped,   0 zombie
  Mem:  8047016K total,  7306672K used,   740344K free,   147348K buffers
 Swap:  4194300K total,         0 used,  4194300K free,  1821408K cached
800%cpu 290%user  57%nice 302%sys 124%idle  13%iow   9%irq   4%sirq   0%host
   PID USER         PR  NI VIRT  RES  SHR S[%CPU] %MEM     TIME+ ARGS                                            
 19281 vehicle_net+ 20   0  12G  10M 6.4M S 49.3   0.1  14:27.25 android.hardware.automotive.vehicle@2.0-service
```

从top命令查看得知，CPU是8核的处理器， vehicle进程占用约50%， 按百分比计算约占用6%左右。

### 查看线程CPU占用率

```bash
console:/ # top -H -p 19281 
Threads: 18 total,   0 running,  18 sleeping,   0 stopped,   0 zombie
  Mem:  8047016K total,  7264500K used,   782516K free,   147696K buffers
 Swap:  4194300K total,         0 used,  4194300K free,  1821928K cached
800%cpu 370%user  89%nice 322%sys   7%idle   0%iow   7%irq   4%sirq   0%host
  TID USER         PR  NI VIRT  RES  SHR S[%CPU] %MEM     TIME+ THREAD          PROCESS                                                                                                                                                                                       
19303 vehicle_net+ 20   0  12G  10M 6.4M S 22.2   0.1   3:46.03 HwBinder:19281_ android.hardware.automotive.vehicle@2.0-service
19307 vehicle_net+ 20   0  12G  10M 6.4M S 18.5   0.1   3:48.29 HwBinder:19281_ android.hardware.automotive.vehicle@2.0-service
20072 vehicle_net+ 20   0  12G  10M 6.4M S  7.4   0.1   3:47.50 HwBinder:19281_ android.hardware.automotive.vehicle@2.0-service
20058 vehicle_net+ 20   0  12G  10M 6.4M S  7.4   0.1   3:46.76 HwBinder:19281_ android.hardware.automotive.vehicle@2.0-service
19311 vehicle_net+ 20   0  12G  10M 6.4M S  0.0   0.1   0:00.02 Binder:19281_3  android.hardware.automotive.vehicle@2.0-service
19304 vehicle_net+ 20   0  12G  10M 6.4M S  0.0   0.1   0:00.49 vehicle@2.0-ser android.hardware.automotive.vehicle@2.0-service
19310 vehicle_net+ 20   0  12G  10M 6.4M S  0.0   0.1   0:00.00 Binder:19281_1  android.hardware.automotive.vehicle@2.0-service
19298 vehicle_net+ 20   0  12G  10M 6.4M S  0.0   0.1   0:00.00 vehicle@2.0-ser android.hardware.automotive.vehicle@2.0-service
19291 vehicle_net+ 20   0  12G  10M 6.4M S  0.0   0.1   0:00.10 vehicle@2.0-ser android.hardware.automotive.vehicle@2.0-service
19301 vehicle_net+ 20   0  12G  10M 6.4M S  0.0   0.1   0:00.01 vehicle@2.0-ser android.hardware.automotive.vehicle@2.0-service
19299 vehicle_net+ 20   0  12G  10M 6.4M S  0.0   0.1   0:00.07 vehicle@2.0-ser android.hardware.automotive.vehicle@2.0-service
19294 vehicle_net+ 20   0  12G  10M 6.4M S  0.0   0.1   0:00.00 vehicle@2.0-ser android.hardware.automotive.vehicle@2.0-service
19295 vehicle_net+ 20   0  12G  10M 6.4M S  0.0   0.1   0:05.85 vehicle@2.0-ser android.hardware.automotive.vehicle@2.0-service
19296 vehicle_net+ 20   0  12G  10M 6.4M S  0.0   0.1   0:00.00 vehicle@2.0-ser android.hardware.automotive.vehicle@2.0-service
19297 vehicle_net+ 20   0  12G  10M 6.4M S  0.0   0.1   0:00.00 vehicle@2.0-ser android.hardware.automotive.vehicle@2.0-service
19290 vehicle_net+ 20   0  12G  10M 6.4M S  0.0   0.1   0:00.00 vehicle@2.0-ser android.hardware.automotive.vehicle@2.0-service
19289 vehicle_net+ 20   0  12G  10M 6.4M S  0.0   0.1   0:00.00 vehicle@2.0-ser android.hardware.automotive.vehicle@2.0-service
19281 vehicle_net+ 20   0  12G  10M 6.4M S  0.0   0.1   0:00.62 Binder:19281_2  android.hardware.automotive.vehicle@2.0-service
```

可以看到其中占用较高的是线程19303、19307、20072、20058， 该4个线程线程名均有HwBinder，是HwBinder相关的线程。Android进程中，Binder相关的线程，基本上可以认定跟跨进程通信有关。binder和vndbinder使用的是AIDL接口， hwbinder使用的是HIDL接口。 这里能基本确定是有其他进程频繁调用Vehicle服务的接口引起的。



### 查找Binder客户端

既然清楚是因为有其他进程频繁调用引起，那么下一步就是需要找出该调用的客户端了。在对外提供的接口上，加上binder pid和uid的打印。以此来查找对应的进程。

```C++
    int pid = IPCThreadState::self()->getCallingPid();
    int uid = IPCThreadState::self()->getCallingUid();
    ALOGI("%s  Prop: 0x%x, PID: %d, UID: %d ", __func__, requestedPropValue.prop, pid, uid);
```

修改、替换后打印logcat日志，得知调用的PID为19915， UID为0，多次调用中基本没有停顿。

```bash
04-01 14:42:51.169 19281 19307 I DefaultVehicleHal_v2_0: get  Prop: 0x294034c2, PID: 19915, UID: 0 
04-01 14:42:51.169 19281 19307 I DefaultVehicleHal_v2_0: get  Prop: 0x11400409, PID: 19915, UID: 0 
```

根据PID，查找对应的服务（这里用xxx替代）

```bash
130|console:/ # ps -A | grep 19915
root          19915      1 12493068 27708 futex_wait_queue_me 0 S xxx_service
```





## 验证流程

1. 删除调用的服务，先把调用的进程改名备份

```bash
adb root
adb remount
adb shell "mv /system/bin/xxx_service /system/bin/xxx_service1"
```

2. kill掉调用进程

```bash
130|console:/ # ps -A | grep xxx_service
root          19915      1 12493068 27708 futex_wait_queue_me 0 S xxx_service
130|console:/ # kill 19915
```

3. 查看进程CPU占用

```bash
console:/ # top -p 19281

Tasks: 1 total,   0 running,   1 sleeping,   0 stopped,   0 zombie
  Mem:  8047016K total,  7683740K used,   363276K free,   150140K buffers
 Swap:  4194300K total,         0 used,  4194300K free,  1829356K cached
800%cpu 182%user  64%nice 257%sys 264%idle  21%iow   7%irq   4%sirq   0%host
   PID USER         PR  NI VIRT  RES  SHR S[%CPU] %MEM     TIME+ ARGS           
 19281 vehicle_net+ 20   0  12G  10M 6.4M S  0.0   0.1  23:23.91 android.hardwa+
Tasks: 1 total,   0 running,   1 sleeping,   0 stopped,   0 zombie
  Mem:  8047016K total,  7682600K used,   364416K free,   150140K buffers
 Swap:  4194300K total,         0 used,  4194300K free,  1829356K cached
800%cpu 182%user  64%nice 257%sys 264%idle  21%iow   7%irq   4%sirq   0%host
   PID USER         PR  NI VIRT  RES  SHR S[%CPU] %MEM     TIME+ ARGS                                                                                                                                                                                                         
 19281 vehicle_net+ 20   0  12G  10M 6.4M S  0.0   0.1  23:23.91 android.hardware.automotive.vehicle@2.0-service
```

4. 至此可看到Vehicle进程CPU占用恢复正常， 通知xxx_service排查。
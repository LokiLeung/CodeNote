#  【Android性能优化】Android CPU占用率检测原理和优化方向

![4372e373033cb1c7039140acbc228d3](./【Android性能优化】CPU占用率检测原理和优化方向.assets/4372e373033cb1c7039140acbc228d3.jpg)

### CPU相关知识

1. **CPU占用的基本计算公式**
   (1 - 空闲态运行时间/总运行时间) * 100%

2. **Hz、Tick、Jiffies：**
   Hz：Linux核心每隔固定周期会发出timer interrupt (**IRQ** 0)，HZ是用来定义每一秒有几次timer interrupts。举例来说，HZ为1000，代表每秒有1000次timer interrupts。
   通过`getconf CLK_TC`命令，可以查看当前系统的Hz。以某某项目为例，Hz为100。

```bash
130|console:/ # getconf CLK_TCK
100
```

Tick：Tick = 1/Hz，即多久发出一次timer interrupt。
以上述情况为例，则为10ms发生一次。

Jiffies：Jiffies是Linux的核心变数。用于记录系统启动后发生timer interrupt的次数，timer interrupt每发生一次，jiffies增加一次。Jiffies可以认为是Linux下CPU的单位时间；

3. **user、nice、system、idle、iowait、irq、softirq**

> kernel/Documentation/filesystems/proc.txt

```bash
1.8 Miscellaneous kernel statistics in /proc/stat
-------------------------------------------------

Various pieces   of  information about  kernel activity  are  available in the
/proc/stat file.  All  of  the numbers reported  in  this file are  aggregates
since the system first booted.  For a quick look, simply cat the file:

  > cat /proc/stat
  cpu  2255 34 2290 22625563 6290 127 456 0 0 0
  cpu0 1132 34 1441 11311718 3675 127 438 0 0 0
  cpu1 1123 0 849 11313845 2614 0 18 0 0 0
  intr 114930548 113199788 3 0 5 263 0 4 [... lots more numbers ...]
  ctxt 1990473
  btime 1062191376
  processes 2915
  procs_running 1
  procs_blocked 0
  softirq 183433 0 21755 12 39 1137 231 21459 2263

The very first  "cpu" line aggregates the  numbers in all  of the other "cpuN" lines.  These numbers identify the amount of time the CPU has spent performing different kinds of work.  Time units are in USER_HZ (typically hundredths of a second).  The meanings of the columns are as follows, from left to right:

- user: normal processes executing in user mode
- nice: niced processes executing in user mode
- system: processes executing in kernel mode
- idle: twiddling thumbs
- iowait: In a word, iowait stands for waiting for I/O to complete. But there
  are several problems:
  1. Cpu will not wait for I/O to complete, iowait is the time that a task is  waiting for I/O to complete. When cpu goes into idle state for outstanding task io, another task will be scheduled on this CPU.
  2. In a multi-core CPU, the task waiting for I/O to complete is not running on any CPU, so the iowait of each CPU is difficult to calculate.
  3. The value of iowait field in /proc/stat will decrease in certain
     conditions.
  So, the iowait is not reliable by reading from /proc/stat.
- irq: servicing interrupts
- softirq: servicing softirqs
- steal: involuntary wait
- guest: running a normal guest
- guest_nice: running a niced guest

```

1. 第一行数字是其他所有CPUN行中的数字总和；
2. 这些数字表示CPU执行不同工作花费的时间，时间单位为USER_HZ，一般为10ms，从左到右，各列的含义如下

| 标题       | 含义                                                         |
| ---------- | ------------------------------------------------------------ |
| user       | 在用户模式下执行的正常进程                                   |
| nice       | niced进程在用户模式下执行                                    |
| system     | 在内核模式下执行的进程                                       |
| idle       | 空闲                                                         |
| iowait     | 总而言之，iowait代表等待I/O完成。但是<br/>存在以下几个问题：<br/>1.Cpu不会等待I/O完成，iowait是任务等待I/O完成的时间。当cpu为未完成的任务io进入空闲状态时，将在该cpu上调度另一个任务。<br/>2.在多核CPU中，等待I/O完成的任务不在任何CPU上运行，因此每个CPU的iowait很难计算。<br/>3./proc/stat中iowait字段的值将在一定程度上减少<br/>条件<br/>因此，从/proc/stat读取iowait是不可靠的。 |
| irq        | 服务中断                                                     |
| softirq    | 服务软中断                                                   |
| steal      | 非自愿等待时间，另一个解释是其它系统所花的时间               |
| guest      | 执行时间为客户操作系统下的虚拟CPU控制                        |
| guest_nice | 低优先级程序所占用的用户态的cpu时间                          |

3. **Cpu花费时间总和cpuTime = user + nice + system + idle + iowait + irq + softirq + steal + guest + guest_nice；**

### 计算整机CPU占用率

根据上面的公式，我们可以采取两个时间点计算CPU总时间差值和CPU空闲时间IDLE的差值，以此得出CPU使用率；

> **采样两个足够短的时间间隔的cpu数据，分别记作t1、t2，其中t1、t2的结构均为：
> (user、nice、system、idle、iowait、irq、softirq、stealstolen、guest、guest_nice)的10元组;（当然这里依据Linux内核的不同有些数据可能没有，就不必计入）**
>
> **计算t1、t2总的cpu时间片totalCPUTime
> a)   把第一次的所有cpu10元组数据求和，得到totalCPUTime1;
> b)   把第二次的所有cpu10元组数据求和，得到totalCPUTime2;**
>
> **计算空闲时间idle
> cpu空闲时间对应第四列的数据
> a）获得第一次的idle数据，记为idle1
> b）获得第二次的idle数据，记为idle2**
>
> **计算cpu使用率
> totalCPUrate = 1 - ((totalCPUTime2-idle2)-(totalCPUTime1-idle1))／（totalCPUTime2-totalCPUTime1）x100%**

### 计算某个进程CPU占用率

> kernel/msm-5.4/Documentation/filesystems/proc.txt

```bash
The stat filecontains details information about the process itself.  Its fields are explained in Table 1-4.

Table 1-4: Contents of the stat files (as of 2.6.30-rc7)
..............................................................................
 Field          Content
  pid           process id
  tcomm         filename of the executable
  state         state (R is running, S is sleeping, D is sleeping in an
                uninterruptible wait, Z is zombie, T is traced or stopped)
 ...
  cmaj_flt      number of major faults with child's
  utime         user mode jiffies  utime指进程在用户态的运行时间
  stime         kernel mode jiffies  ;stime指进程在内核态的运行时间
  cutime        user mode jiffies with child's   utime指所有子进程在用户态的运行时间总和
  cstime        kernel mode jiffies with child's   cstime指所有子进程在核心态的运行时间总和
  priority      priority level
  nice          nice level
  num_threads   number of threads
  it_real_value	(obsolete, always 0)
  start_time    time the process started after system boot
  vsize         virtual memory size
  rss           resident set memory size
  rsslim        current limit in bytes on the rss
  start_code    address above which program text can run
...
```

这里只关注 utime、 stime、 cutime、 cstime，它们的总和就是该进程的CPU时间。取两个时间点进行采样并取差值，就可以得到这段时间内的该进程所占用的CPU时间片。

```bash
scheduledTime = utime + stime + cutime + sctime;
```

```java
if (lastCpuTime && lastScheduledTime)
    cpuUsage = (scheduledTime - lastScheduledTime) * 100. / (cpuTime - lastCpuTime);
lastScheduledTime = scheduledTime;
lastCpuTime = cpuTime;
```

### 优化的基本思路和方向

1. 确定CPU占用高的进程，使用top命令查看；
2. 确定该进程CPU占用高的线程，`top -p <PID>`查看线程状态和线程CPU；
3. 结合logcat命令和trace工具，确定该线程处于什么工作逻辑中以及相关方法耗时，（实在找不到就打断点，加日志，控制变量法）；
   1. 频繁报错 ---> 解决报错；
   2. 过度绘制 ---> 重新布局绘制；
   3. 解码/编码 ---> 排查具体算法逻辑；
   4. 频繁调用 ---> 确定各个调用者，并协调修改；
   5. ...
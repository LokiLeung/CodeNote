# 【Android系统启动】Android Init 语言官网教程及中文翻译

![微信图片_20240421041032](./【Android系统启动】 Android Init 语言官网教程及中文翻译.assets/微信图片_20240421041032.jpg)

> 文章根据system/core/init/README.md对Android Init语言进行翻译；
>
> 下面给出Init语言中文翻译和原文，翻译为机翻和个人翻译综合完成，如有错误欢迎提出纠正。



---

# Android Init 语言官网中文翻译

## Android Init Language（Android Init语言）

Android Init语言由五大类语句组成：动作（Actions）、命令（Commands）、服务（Services）、选项（Options）和导入（Imports）。

+ 所有这些语句都以行为导向的（一行就是一个语句），由以空白分隔的标记组成； C语言风格的反斜线转义符可用于在标记符号中插入空格；双引号也可用于防止空白将文本分割成多个标记；当反斜杠是一行中的最后一个字符时，可用于折行；
+ 以#开始的行是注释（允许#前面是空白）；
+ 系统属性可以使用`${property.name}`语法展开。这也适用于需要import的情况，如 `import /init.recovery.${ro.hardware}.rc`；
+ Action和Service隐式声明一个新的section（章节）。所有Command或者Option属于这个这个最近声明的section。第一个section之前声明的Commad和Option将会被忽略；
+ Service具有唯一的名称。 如果定义的第二个Service与现有Service名称相同，则该Service将被忽略并记录错误信息。



## Init .rc Files（Init.rc 文件）

init 语言用于扩展名为 .rc 文件的纯文本文件中。 在系统的多个位置通常有多个这样的文件，如下所述。

`/system/etc/init/hw/init.rc` 是主要的 .rc 文件，由 init 可执行文件（init进程）在开始执行时加载。 它负责系统的初始设置。

加载主文件 `/system/etc/init/hw/init.rc`后，init 会立即加载 `/{system,system_ext,vendor,odm,product}/etc/init/`目录下的所有文件。 在
[Imports](#imports)章节有更详细的解释。

以前，没有第一阶段挂载机制的旧版设备可以在 mount_all 过程中导入启动脚本，但这种做法已被弃用，Android Q（Android 10） 之后启动的设备也不允许这样做。

上面这些目录的作用是：

1. `/system/etc/init/`用于核心系统项目，如 SurfaceFlinger、MediaService 和 logd；
  2. `/vendor/etc/init/` 用于 SoC 供应商项目，如核心 SoC 功能所需的操作或守护进程；
  3. `/odm/etc/init/` 用于设备制造商项目，如运动传感器或其他外设功能所需的操作或守护进程；

二进制文件位于system、vendor 或 odm 分区的所有Service，都应将其Service 入口放入相应的 init .rc 文件，该文件位于其所在分区的 /etc/init/ 目录中。 有一个名为 LOCAL\_INIT\_RC 的构建系统宏可为开发人员处理此事。 每个 init .rc 文件还应包含与其服务相关的任何操作。

例如，位于 system/core/logcat 目录中的 userdebug logcatd.rc 和 Android.mk 文件。 在构建过程中，Android.mk 文件中的 LOCAL\_INIT\_RC 宏将 logcatd.rc 置于 /system/etc/init/ 中。 在 mount\_all 命令期间，Init 会加载 logcatd.rc，并允许运行服务和在适当时排队执行操作。(PS：现在logcatd不使用Android.mk了，但是可以通过logcatd中的Android.bp，查看对应的写法)

与以前使用的单个 init .rc 文件相比，这种根据守护进程分割 init .rc 文件的做法更为可取。 这种方法可确保 init 读取的唯一服务条目和 init 执行的唯一操作都与文件系统中实际存在二进制文件的服务相对应，而单一的 init .rc 文件则不是这种情况。 当多个服务被添加到系统中时，这将有助于解决合并冲突问题，因为每个服务都将被添加到一个单独的文件中。



## Versioned RC files within APEXs（APEX文件中版本控制的RC文件）

> PS：Android Pony EXpress (APEX) 是 Android 10 中引入的一种容器格式，用于较低级别系统模块的安装流程中。此格式可帮助更新不适用于标准 Android 应用模型的系统组件。一些示例组件包括原生服务和原生库、硬件抽象层 (HAL))、运行时 (ART) 以及类库。
>
> “APEX”这一术语也可以指 APEX 文件。
>
> [APEX 文件格式  |  Android 开源项目  |  Android Open Source Project](https://source.android.google.cn/docs/core/ota/apex?hl=zh-cn)

随着 Android Q 上主线的到来，各个主线模块都在其边界（这里可以认为是作用域）内携带了自己的 init.rc 文件。Init 会根据命名模式 `/apex/*/etc/*rc`处理这些文件。

由于 APEX 模块必须在多个 Android 版本上运行，因此它们可能需要不同的参数作为其定义的服务的一部分。为此，从 Android T （Android13）开始，在 init 文件名中加入 SDK 版本信息。 后缀从 `.rc` 改为 `.#rc`，其中 # 是该 RC 文件被接受的第一个 SDK（可以认为是minSdkVersion）。
RC 文件的第一个 SDK。SDK=31 的启动文件可命名为 `init.31rc`。使用这种方案，APEX 可以包含多个初始文件。举个适当的例子。

对于一个在 /apex/sample-module/apex/etc/ 中包含以下文件的 APEX 模块来说，

      1. init.rc
      2. init.32rc
      3. init.35rc

选择规则会选择不超过当前运行系统 SDK 的最高`.#rc`值。未经修饰的 `.rc` 被解释为 sdk=0。

当该 APEX 安装在 SDK <=31 的设备上时，系统将处理 init.rc。 安装在运行 SDK 32、33 或 34 的设备上时，将使用 init.32rc。 当安装在运行 SDK >= 35 的设备上时，系统将选择 init.35rc

此版本命名方案仅用于 APEX 模块中的 init 文件；不适用于存储在 /system/etc/init、/vendor/etc/init 或其他目录中的 init 文件。

此命名方案在 Android S（Android 12） 之后可用。



## Actions（动作）

Action 是一系列的Commad。 Action 有一个Trigger（触发器），用于决定何时执行该 Action。 当发生与 Action 的Trigger相匹配的事件时，该 Action 会被添加到待执行队列的尾部（除非它已经在队列中）。

队列中的每个 Action 都会被按顺序出队（FIFO），该 Action 中的每个Commad也会按顺序执行。 Init 会在执行任务的 "间隙 "处理其他任务（设备创建/销毁、属性设置、进程重启）。

Action 的格式如下：

    on <trigger> [&& <trigger>]*
       <command>
       <command>
       <command>

Action 会被添加到队列中，并根据包含这些 Action 的文件的解析顺序（参见导入部分）执行，然后在单个文件中按顺序执行。

例如，如果一个文件包含

```
on boot
   setprop a 1
   setprop b 2

on boot && property:true=true
   setprop c 1
   setprop d 2

on boot
   setprop e 1
   setprop f 2
```

那么当发生 `boot` 触发时，假定属性 `true` 等于 `true`，那么执行命令的顺序将是：

    setprop a 1
    setprop b 2
    setprop c 1
    setprop d 2
    setprop e 1
    setprop f 2

如果属性 `true` 在触发`boot`时不是`true`，那么执行命令的顺序将是：

    setprop a 1
    setprop b 2
    setprop e 1
    setprop f 2

如果属性 `true` 在触发`boot`后变为`true`，则不会执行任何命令。条件 `boot && property:true=true` 将被评估为 false，因为 `boot` 触发是一个过去的事件。

请注意，当 `ro.property_service.async_persist_writes` 为 `true` 时，持久 persistent setprops（设置持久系统属性） 和 non-persistent setprops（设置非持久系统属性）之间没有确定的熟悉怒。例如

    on boot
        setprop a 1
        setprop persist.b 2

当 `ro.property_service.async_persist_writes` 为 `true` 时，这两个属性的触发器可按任何顺序执行。



## Services（服务）

服务是 init 启动并（可选）在退出时重启的程序。 服务的形式包括

```
service <name> <pathname> [ <argument> ]*
   <option>
   <option>
   ...
```



## Options（选项）

Option是Service的修改器。 它们会影响 init 运行服务的方式和时间。

`capabilities [ <capability>\* ]`

> 在执行此服务时设置能力。'capability' 应该是一个 Linux 能力，不包含 "CAP_" 前缀，例如 "NET_ADMIN" 或 "SETPCAP"。请参阅 http://man7.org/linux/man-pages/man7/capabilities.7.html 获取 Linux 能力的列表。
>
> 如果没有提供能力，则行为取决于服务运行的用户：
>
> - 如果是 root 用户，则服务将以所有能力运行（注意：服务实际上是否可以使用它们由 selinux 控制）；
> - 否则，所有能力都将被删除。

`class <name> [ <name>\* ]`

> 指定服务的类名。具有相同类名的所有服务可以一起启动或停止。如果未通过 class 选项指定，服务将属于 "default" 类。除了（必需的）第一个类名之外的其他类名用于分组服务。
> `animation` 类应包含启动动画和关闭动画所需的所有服务。由于这些服务可能在引导过程的非常早期启动，并且可能在关闭的最后阶段运行，因此不能保证对 /data 分区的访问。这些服务可以检查 /data 下的文件，但不应保持文件打开，并且应在 /data 不可用时正常工作。

`console [<console>]`

> 该服务需要一个控制台。可选的第二个参数选择特定的控制台，而不是默认的。默认的 "/dev/console" 可以通过设置 "androidboot.console" 内核参数来更改。在所有情况下，应省略前导的 "/dev/"，因此 "/dev/tty0" 应该指定为 "console tty0"。
>
> 此选项将标准输入、标准输出和标准错误连接到控制台。它与 stdio_to_kmsg 选项互斥，后者仅将标准输出和标准错误连接到 kmsg。

`critical [window=<fatal crash window mins>] [target=<fatal reboot target>]`

> 这是一个设备关键的服务。如果在_fatal crash window mins_分钟内退出超过四次，或在启动完成之前退出，则设备将重新启动到_fatal reboot target_。 _fatal crash window mins_ 的默认值为4，_fatal reboot target_ 的默认值为'bootloader'。对于测试，可以通过将属性`init.svc_debug.no_fatal.<service-name>`设置为指定关键服务的`true`来跳过致命重新启动。

`disabled`

> 该服务不会自动与其类一起启动。必须通过名称或接口名称显式启动它。

`enter_namespace <type> <path>`

> 进入位于路径 _path_ 的类型为 _type_ 的命名空间。只支持将 _type_ 设置为 "net" 的网络命名空间。请注意，每种 _type_ 的命名空间只能进入一个。

`file <path> <type>`

> 打开文件路径并将其文件描述符传递给启动的进程。_type_ 必须是 "r"、"w" 或 "rw"。对于本机可执行文件，请参阅 libcutils 的 android\_get\_control\_file()。

`gentle_kill`

> 停止时，此服务将收到 SIGTERM 而不是 SIGKILL。在 200 毫秒的超时后，它将收到 SIGKILL。

`group <groupname> [ <groupname>\* ]`

> 在执行此服务之前切换到 'groupname'。除了（必需的）第一个之外的其他 groupname 用于设置进程的附加组（通过 setgroups()）。目前默认为 root。（??? 可能应该默认为 nobody）

`interface <interface name> <instance name>`

> 将此服务与其提供的一组 AIDL 或 HIDL 服务相关联。接口名称必须是完全限定的名称，而不是值名称。例如，这用于允许 servicemanager 或 hwservicemanager 懒惰地启动服务。当服务多个接口时，应该多次使用此标签。HIDL 接口的示例条目是 `interface vendor.foo.bar@1.0::IBaz default`。对于 AIDL 接口，请使用 `interface aidl <instance name>`。AIDL 接口的实例名称是注册到 servicemanager 的名称，可以使用 `adb shell dumpsys -l` 列出这些名称。

`ioprio <class> <priority>`

> 通过 SYS_ioprio_set 系统调用为此服务设置 IO 优先级和 IO 优先级类别。 _class_ 必须是 "rt"、"be" 或 "idle" 中的一个。 _priority_ 必须是范围在 0 到 7 之间的整数。

`keycodes <keycode> [ <keycode>\* ]`

> 设置触发此服务的按键代码。如果同时按下与传递的按键代码相对应的所有按键，则服务将启动。这通常用于启动 bugreport 服务。

> 此选项可以接受属性而不是按键代码列表。在这种情况下，只提供一个选项：典型属性扩展格式中的属性名称。该属性必须包含逗号分隔的按键代码值列表，或文本“none”以指示此服务不响应按键代码。

> 例如，`keycodes ${some.property.name:-none}` 其中 some.property.name 展开为 "123,124,125"。由于按键代码在 init 中处理得非常早，因此只能使用 PRODUCT_DEFAULT_PROPERTY_OVERRIDES 属性。

`memcg.limit_in_bytes <value>` and `memcg.limit_percent <value>`

> 将子进程的memory.limit_in_bytes设置为`limit_in_bytes`字节和`limit_percent`的最小值，`limit_percent`被解释为设备物理内存大小的百分比（仅在memcg已挂载时）。值必须等于或大于0。

`memcg.limit_property <value>`

> 将子进程的memory.limit_in_bytes设置为指定属性的值（仅在memcg已挂载时）。此属性将覆盖通过 `memcg.limit_in_bytes` 和 `memcg.limit_percent` 指定的值。

`memcg.soft_limit_in_bytes <value>`

> 将子进程的memory.soft_limit_in_bytes设置为指定的值（仅在memcg已挂载时），该值必须大于或等于0。

`memcg.swappiness <value>`

> 将子进程的memory.swappiness设置为指定的值（仅在memcg已挂载时），该值必须大于或等于0。

`namespace <pid|mnt>`

> 在fork服务时，进入一个新的PID或挂载命名空间。

`oneshot`

> 当服务退出时不要重新启动服务。

`onrestart`

> 当服务重新启动时执行一个命令（见下文）。

`oom_score_adjust <value>`

> 将子进程的 /proc/self/oom_score_adj 设置为指定的值，必须在 -1000 到 1000 的范围内。

`override`

> 指示此服务定义旨在覆盖先前针对具有相同名称的服务的定义。通常用于/odm上的服务来覆盖在/vendor上定义的服务。init解析的具有此关键字的最后一个服务定义将用于此服务。要注意init.rc文件解析的顺序，因为出于向后兼容性的原因，它具有一些特殊性。此文件的“imports”部分详细介绍了顺序。

`priority <priority>`

> 服务进程的调度优先级。该值必须在 -20 到 19 的范围内。默认优先级为 0。优先级通过 setpriority() 设置。

`reboot_on_failure <target>`

> 如果此进程无法启动，或者进程以除 CLD_EXITED 之外的退出代码或除 '0' 之外的状态终止，则使用指定的 _target_ 重新启动系统。_target_ 采用与 sys.powerctl 参数相同的格式。这特别用于与 `exec_start` 内置一起用于在引导过程中进行必要检查。

`restart_period <seconds>`

> 如果一个非单次执行的服务退出，它将在其前次启动时间加上该周期后重新启动。默认值为 5 秒。这可用于与下面的 `timeout_period` 命令一起实现周期性服务。例如，可以将其设置为 3600 表示服务应该每小时运行一次，或者设置为 86400 表示服务应该每天运行一次。此周期可以设置为比 5 秒更短的值，例如 0，但如果重启是由于崩溃引起的，则将强制执行最小的 5 秒延迟。这是为了限制持续崩溃的服务的速率。换句话说，只有当服务有意义地并成功地退出（即通过调用 exit(0)）时，才会尊重小于 5 秒的 `<seconds>`。

`rlimit <resource> <cur> <max>`

> 这将给服务应用指定的资源限制。资源限制会被子进程继承，因此这实际上将给由此服务启动的进程树应用指定的资源限制。其解析方式类似于下面指定的 setrlimit 命令。

`seclabel <seclabel>`

> 在执行此服务之前切换到 'seclabel'。主要用于从根文件系统运行的服务，例如 ueventd、adbd。位于系统分区上的服务可以使用基于其文件安全上下文的策略定义的转换。如果未指定并且策略中没有定义转换，则默认为 init 上下文。

`setenv <name> <value>`

> 在启动的进程中将环境变量 _name_ 设置为 _value_。

`shutdown <shutdown_behavior>`

> 设置服务进程的关机行为。当没有指定此选项时，服务将在关机过程中使用 SIGTERM 和 SIGKILL 被终止。具有 "critical" 关机行为的服务在关机期间不会被终止，直到关机超时。当关机超时时，即使标记为 "shutdown critical" 的服务也会被终止。如果在关机开始时标记为 "shutdown critical" 的服务未运行，则会启动该服务。

`sigstop`

> 在调用 exec 之前立即向服务发送 SIGSTOP 信号。这是为了调试而设计的。有关如何使用此功能的详细信息，请参阅下面的调试部分。

`socket <name> <type> <perm> [ <user> [ <group> [ <seclabel> ] ] ]`

> 创建一个名为 /dev/socket/_name_ 的 UNIX 域套接字，并将其文件描述符传递给启动的进程。当服务启动时，套接字会同步创建。_type_ 必须是 "dgram"、"stream" 或 "seqpacket"。_type_ 可以以 "+passcred" 结尾，以启用套接字上的 SO_PASSCRED 选项，或以 "+listen" 结尾，以同步地将其设置为监听套接字。用户和组默认为 0。'seclabel' 是套接字的 SELinux 安全上下文。默认为服务的安全上下文，如通过 seclabel 或根据服务可执行文件的安全上下文计算的。对于本机可执行文件，请参阅 libcutils android\_get\_control\_socket()。

`stdio_to_kmsg`

> 将 stdout 和 stderr 重定向到 /dev/kmsg_debug。这对于在早期引导期间不使用原生 Android 日志记录并且希望捕获其日志消息的服务非常有用。仅在启用了 /dev/kmsg_debug 时才启用此选项，而 /dev/kmsg_debug 仅在用户调试版和工程版中启用。这与控制台选项是互斥的，后者还将 stdin 连接到指定的控制台。

`task_profiles <profile> [ <profile>\* ]`

> 设置任务配置文件。在 Android U 之前，配置文件会应用于服务的主线程。对于 Android U 及更高版本，配置文件会应用于整个服务进程。这是为了取代将进程移入 cgroup 的 writepid 选项而设计的。

`timeout_period <seconds>`

> 提供一个超时时间，超过该时间后服务将被终止。这里会尊重 oneshot 关键字，因此 oneshot 服务不会自动重新启动，但所有其他服务都会。这对于创建一个与上面描述的 restart_period 选项结合的周期性服务特别有用。

`updatable`

> 标记该服务可以在启动序列的后续阶段被APEXes通过 'override' 选项覆盖。当具有可更新选项的服务在所有APEXes激活之前启动时，执行将被延迟直到激活完成。未标记为可更新的服务不能被APEXes覆盖。

`user <username>`

> 在执行此服务之前切换到 'username'。目前默认为 root。（??? 可能应该默认为 nobody）从Android M开始，即使进程需要Linux权限，也应使用此选项。以前，要获取Linux权限，进程需要以root身份运行，请求权限，然后切换到所需的uid。现在有一种新的机制，通过fs\_config允许设备制造商向文件系统上的特定二进制文件添加Linux权限，这些文件应该使用。该机制在<http://source.android.com/devices/tech/config/filesystem.html>中进行了描述。使用这种新机制时，进程可以使用用户选项选择所需的uid，而无需以root身份运行。从Android O开始，进程还可以直接在其 .rc 文件中请求权限。请参阅上面的 "capabilities" 选项。

`writepid <file> [ <file>\* ]`

> 在fork时将子进程的pid写入给定的文件。主要用于cgroup/cpuset的使用。如果未指定/dev/cpuset/下的任何文件，但是系统属性 'ro.cpuset.default' 被设置为非空的cpuset名称（例如 '/foreground'），则pid将被写入到文件/dev/cpuset/_cpuset\_name_/tasks。此选项用于将进程移动到cgroup已过时，请改用task_profiles选项。



## Triggers（触发器）

Trigger是一个字符串，可用于匹配某些类型的事件，并导致action发生。

Trigger又分为事件触发器event triggers和属性触发器property triggers。

事件触发器event triggers是由 "trigger "命令或 init 可执行文件中的 QueueEventTrigger() 函数触发的字符串。 其形式为简单字符串，如 "boot "或 "late-init"。

属性触发器property triggers是在指定系统属性的值变为给定新值或指定系统属性的值变为任何新值时触发的字符串。 其形式分别为 "property:<name>=<value>"和 "property:<name>=\*"。 在 init 的初始启动阶段，属性触发器也会进行相应的评估和触发。

一个 Action 可以有多个属性触发器，但只能有一个事件触发器。

例如：
`on boot && property:a=b` 定义了一个仅在`boot`事件触发器发生且属性 a 等于 b 时执行的 Action。在触发 Trigger "启动 "`boot`事件后，当属性 a 变为值 b 时，将不会执行该操作。

`on property:a=b && property:c=d` 定义了一个在三个时间点执行的 Action：

1. 初始启动时，如果属性 a=b 和属性 c=d。
2. 当属性 a 变为值 b，而属性 c 已等于 d 时。
3. 当属性 c 转换为值 d 时，而属性 a 已等于 b。

## Trigger Sequence（触发器时序）

Init进程使用以下系列的触发器在early-boot阶段。这些内置的trigger定义在init.cpp中。

1. `early-init`：该时序（顺序）的的第一个，在配置了 cgroups 之后、但在 ueventd 的冷启动完成之前触发。
2. `init`：在冷启动完成后触发。
3. `charger`：当 `ro.bootmode == "charger"` 时触发。
4. `late-init`：当 `ro.bootmode != "charger"` 或通过 healthd 触发从充电模式启动时触发。

其余触发器在 `init.rc` 中配置，并非内置。这些触发的默认顺序在 `init.rc` 中的 "on late-init "事件下指定。`init.rc` 中的内部 Action
内部的操作已被省略。

1. `early-fs`：启动 vold。
2. `fs`：Vold 启动。挂载未标记为第一阶段或latemounted的分区。
3. `post-fs`：配置任何依赖于early mounts的内容。
 4. `late-fs`：挂载标记为latemounted的分区。
5. `post-fs-data`：挂载并配置 `/data`；设置加密。如果在第一阶段启动时无法挂载，则在此处重新格式化 `/metadata`。
6. `zygote-start`：启动zygote。
7. `early-boot`：在 zygote 启动之后。
8. `boot`：`early-boot` 动作完成后。

## Commands（命令）

`bootchart [start|stop]`

> 启动/停止bootchart记录。这些在默认的 init.rc 文件中存在，但只有当文件 /data/bootchart/enabled 存在时，bootchart记录才会生效；否则启动/停止bootchart将不起作用。

`chmod <octal-mode> <path>`

> 更改文件访问权限。

`chown <owner> <group> <path>`

> 更改文件所有者和所属组。

`class_start <serviceclass>`

> 如果指定类别的所有服务尚未运行，则启动它们。有关启动服务的更多信息，请参阅启动条目。

`class_stop <serviceclass>`

> 如果指定类别的所有服务当前正在运行，则停止并禁用它们。

`class_reset <serviceclass>`

> 如果指定类别的所有服务当前正在运行，则停止它们，但不禁用它们。稍后可以使用 `class_start` 重新启动它们。

`class_restart [--only-enabled] <serviceclass>`

> 重新启动指定类别的所有服务。如果指定了 `--only-enabled`，则跳过已禁用的服务。

`copy <src> <dst>`

> 复制文件。与写入类似，但适用于二进制/大量数据。
>
> 关于源文件，不允许从符号链接文件和世界可写或组可写文件复制。
>
> 关于目标文件，如果目标文件不存在，默认创建的模式为 0600。
>
> 如果目标文件是普通常规文件并且已存在，则会将其截断。

`copy_per_line <src> <dst>`

> 逐行复制文件。类似于复制，但适用于目标是无法处理多行数据的 sysfs 节点。

`domainname <name>`

> 设置域名。

`enable <servicename>`

> 将一个已禁用的服务转换为启用状态，就好像服务没有指定禁用一样。
> 如果该服务应该正在运行，现在将启动它。
> 通常在引导加载程序设置一个变量指示需要启动特定服务时使用。例如：

    on property:ro.boot.myfancyhardware=1
        enable my_fancy_service_for_my_fancy_hardware

`exec [ <seclabel> [ <user> [ <group>\* ] ] ] -- <command> [ <argument>\* ]`

> Fork并执行带有给定参数的命令。命令在 "--" 之后启动，以便可以提供可选的安全上下文、用户和附加组。在此命令完成之前，不会运行其他命令。 _seclabel_ 可以是 -，表示默认值。在参数中展开属性。
> Init 暂停执行命令，直到fork的进程退出。

`exec_background [ <seclabel> [ <user> [ <group>\* ] ] ] -- <command> [ <argument>\* ]`

> 使用给定的参数fork并执行命令。这与 `exec` 命令类似处理。不同之处在于对于 `exec_background`，init 不会在进程退出之前停止执行命令。

`exec_start <service>`

> 启动给定的服务，并暂停处理其他 init 命令，直到它返回。该命令的功能类似于 `exec` 命令，但是使用现有的服务定义来替换 exec 参数向量。

`export <name> <value>`

> 在全局环境中设置环境变量 _name_ 的值为 _value_（此命令执行后启动的所有进程都将继承该环境变量）。

`hostname <name>`

> 设置主机名称

`ifup <interface>`

> 将网络接口 *interface* 上线。

`insmod [-f] <path> [<options>]`

> 使用指定的选项在 _path_ 处安装模块。
> -f: 即使运行内核的版本与编译模块的内核版本不匹配，也强制安装模块。

`interface_start <name>` \
`interface_restart <name>` \
`interface_stop <name>`

> 查找提供接口 _name_ 的服务，如果存在，则分别对其运行 `start`、`restart` 或 `stop` 命令。 _name_ 可以是一个完全合格的 HIDL 名称，格式为 `<interface>/<instance>`，或者是一个 AIDL 名称，格式为 `aidl/<interface>`，例如 `android.hardware.secure_element@1.1::ISecureElement/eSE1` 或 `aidl/aidl_lazy_test_1`。

> 请注意，这些命令仅作用于由 `interface` 服务选项指定的接口，而不是在运行时注册的接口。

> 这些命令的示例用法： \
> `interface_start android.hardware.secure_element@1.1::ISecureElement/eSE1` 将启动提供 `android.hardware.secure_element@1.1` 和 `eSI1` 实例的 HIDL 服务。 \
> `interface_start aidl/aidl_lazy_test_1` 将启动提供 `aidl_lazy_test_1` 接口的 AIDL 服务。

`load_exports <path>`

> 打开路径为 _path_ 的文件，并导出在其中声明的全局环境变量。每一行必须符合 `export <name> <value>` 的格式，如上所述。

`load_system_props`

> （此操作已被弃用，无效。）

`load_persist_props`

> 当/data被解密后，加载持久属性。这已包含在默认的init.rc中。

`loglevel <level>`

> 将init的日志级别设置为整数级别，范围从7（全部记录）到0（仅致命错误记录）。这些数字值对应于内核日志级别，但此命令不影响内核日志级别。要更改内核日志级别，请使用`write`命令写入`/proc/sys/kernel/printk`。在_level_中展开属性。

`mark_post_data`

> 用于标记/data挂载后的点。

`mkdir <path> [<mode>] [<owner>] [<group>] [encryption=<action>] [key=<key>]`

> 在 _path_ 处创建一个目录，可选地设置指定的模式、所有者和组。如果未提供这些参数，则目录将以权限755创建，并由root用户和root组拥有。如果提供了这些参数，则目录的模式、所有者和组将在目录已存在时更新。
> 如果目录不存在，则它将从当前SELinux策略中或其父策略（如果策略中未指定）获取安全上下文。如果目录已存在，则其安全上下文不会更改（即使与策略中的不同）。
>
> _action_ 可以是以下之一：
>
>  * `None`：不采取加密操作；如果父目录已经加密，则该目录也会被加密。
>  * `Require`：加密目录，如果加密失败则中止引导过程。
>  * `Attempt`：尝试设置加密策略，但如果失败则继续。
>  * `DeleteIfNecessary`：如果需要设置加密策略，则递归删除目录。
>
> _key_ 可以是以下之一：
>
>  * `ref`：使用系统范围的DE密钥。
>  * `per_boot_ref`：在每次启动时使用新生成的密钥。

`mount_all [ <fstab> ] [--<option>]`

> 调用给定的 fs\_mgr 格式 fstab 上的 fs\_mgr\_mount\_all，带有可选选项 "early" 和 "late"。
> 设置 "--early" 后，init 可执行文件将跳过带有 "latemount" 标志的挂载条目，并触发文件系统加密状态事件；设置 "--late" 后，init 可执行文件将仅挂载带有 "latemount" 标志的条目。默认情况下，未设置任何选项，并且 mount\_all 将处理给定 fstab 中的所有条目。如果未指定 fstab 参数，则将在 /odm/etc、/vendor/etc 或 / 下运行时扫描 fstab.${ro.boot.fstab_suffix}、fstab.${ro.hardware} 或 fstab.${ro.hardware.platform}，按顺序进行扫描。

`mount <type> <device> <dir> [ <flag>\* ] [<options>]`

> 尝试将名为的设备挂载到目录 _dir_。_flags_ 包括 "ro"、"rw"、"remount"、"noatime" 等。_options_ 包括 "barrier=1"、"noauto_da_alloc"、"discard" 等，作为逗号分隔的字符串，例如 barrier=1,noauto_da_alloc。

`perform_apex_config [--bootstrap]`

> 在APEX被挂载后执行任务。例如，为挂载的APEX创建数据目录、解析其配置文件并更新链接器配置。仅在apexd将`apexd.status`设置为ready以通知挂载事件时使用。在引导挂载命名空间中调用时，请使用--bootstrap选项。

`restart [--only-if-running] <service>`

> 如果服务正在运行，则停止并重新启动该服务；如果服务当前正在重新启动，则不执行任何操作；否则，仅启动该服务。如果指定了"--only-if-running"，则只有在服务已经在运行时才会重新启动。

`restorecon <path> [ <path>\* ]`

> 将由 _path_ 指定的文件恢复到file_contexts 配置中指定的安全上下文中。
> 对于由 init.rc 创建的目录，这不是必需的，因为这些目录会由 init 自动正确标记。

`restorecon_recursive <path> [ <path>\* ]`

> 递归将由 _path_ 指定的目录树恢复到file\_contexts 配置中指定的安全上下文。

`rm <path>`

> 调用 unlink(2) 删除给定路径。你可能想使用 "exec -- rm ..." 来代替（假设系统分区已经挂载）。

`rmdir <path>`

> 调用 rmdir(2) 删除给定路径。

`readahead <file|dir> [--fully]`

> 调用 readahead(2) 读取给定目录中的文件或文件。
> 使用选项 --fully 读取完整的文件内容。

`setprop <name> <value>`

> 将系统属性 _name_ 设置为 _value_。在 _value_ 中会扩展属性。

`setrlimit <resource> <cur> <max>`

> 设置资源的资源限制。这适用于在设置限制后启动的所有进程。建议在 init 的早期设置并全局应用。_resource_ 最好使用其文本表示（'cpu'、'rtio' 等或 'RLIM_CPU'、'RLIM_RTIO' 等）指定。也可以将其指定为与资源枚举对应的整数值。_cur_ 和 _max_ 可以是 'unlimited' 或 '-1'，表示无限制的资源限制。

`start <service>`

> 如果服务尚未运行，则启动该服务。
> 请注意，这不是同步的，即使它是同步的，也不能保证操作系统的调度程序会充分执行服务以确保服务的状态。
> 参见 `exec_start` 命令，以获取 `start` 的同步版本。

> 这带来了一个重要的结果，即如果服务向其他服务提供功能，比如提供通信渠道，仅仅在这些服务之前启动该服务是 _不够的_，不能保证该通道在这些服务请求之前已经建立。必须有一个单独的机制来确保这种保证。

`stop <service>`

> 如果当前正在运行，则停止一个服务的运行。

`swapon_all [ <fstab> ]`

> 调用 `fs_mgr_swapon_all` 函数并传入指定的 fstab 文件。
> 如果未指定 fstab 参数，则会在运行时依次在 /odm/etc、/vendor/etc 或 / 下扫描 `fstab.${ro.boot.fstab_suffix}`、`fstab.${ro.hardware}` 或 `fstab.${ro.hardware.platform}`。

`symlink <target> <path>`

> 在 _path_ 处创建一个符号链接，指向 _target_。

`sysclktz <minutes_west_of_gmt>`

> 设置系统时钟基准（如果系统时钟以GMT为基准则为0）。

`trigger <event>`

> 触发一个事件。用于从另一个动作中排队一个动作。

`umount <path>`

> 卸载该路径上挂载的文件系统。

`umount_all [ <fstab> ]`

> 在给定的fstab文件上调用`fs_mgr_umount_all`函数。如果未指定fstab参数，则将在运行时的/odm/etc、/vendor/etc或/目录下扫描`fstab.${ro.boot.fstab_suffix}`、`fstab.${ro.hardware}`或`fstab.${ro.hardware.platform}`。

`verity_update_state`

> 内部实现细节，用于更新`dm-verity`状态并设置由`adb remount`使用的`partition._mount-point_.verified`属性，因为`fs\_mgr`不能直接设置它们。这是自Android 12以来所需的，因为CtsNativeVerifiedBootTestCases将读取属性`partition.${partition}.verified.hash_alg`来检查是否未使用sha1。有关更多详细信息，请参见https://r.android.com/1546980。

`wait <path> [ <timeout> ]`

> 轮询给定文件的存在，并在找到时返回，或者超时到达时返回。如果未指定超时，则默认为五秒。超时值可以是浮点数表示的小数秒。

`wait_for_prop <name> <value>`

> 等待系统属性_name_变为_value_。_value_中的属性将被展开。如果属性_name_已经设置为_value_，立即继续。

`write <path> <content>

> 打开路径为_path_的文件，并使用write(2)向其中写入一个字符串。
> 如果文件不存在，将创建它。如果文件已存在，它将被截断。_content_ 中的属性将被展开。

## Imports（导入）

`import <path>`

> 解析一个 init 配置文件，扩展当前配置。
> 如果 _path_ 是一个目录，则目录中的每个文件都将解析为一个配置文件。它不是递归的，嵌套目录不会被解析。

import 关键字不是一个命令，而是文件自己的部分，这意味着它不是作为一个动作的一部分发生的，而是，在解析文件时处理导入并遵循以下逻辑。

init可执行文件只有三次导入 .rc 文件：

    # 1. 在初始启动期间，当它imports `/system/etc/init/hw/init.rc` 或由property `ro.boot.init_rc` 指示的脚本时。
    # 2. 在当它imports `/system/etc/init/hw/init.rc` 后立即当它imports `/{system,system_ext,vendor,odm,product}/etc/init/`。
    # 3. （已弃用）在 mount_all 期间，当它导入 `{system,vendor,odm}/etc/init/` 或指定路径下的 .rc 文件时，对于在 Q 之后启动的设备不允许。
    1. When it imports `/system/etc/init/hw/init.rc` or the script indicated by the property
         `ro.boot.init_rc` during initial boot.
      2. When it imports `/{system,system_ext,vendor,odm,product}/etc/init/` immediately after
         importing `/system/etc/init/hw/init.rc`.
      3. (Deprecated) When it imports /{system,vendor,odm}/etc/init/ or .rc files
         at specified paths during mount_all, not allowed for devices launching
         after Q.

文件导入的顺序由于历史原因有些复杂。以下是保证的顺序：

1. 首先解析 `/system/etc/init/hw/init.rc`，然后递归地解析其每个导入的文件。
2. `/system/etc/init/` 的内容按字母顺序排序，依次解析，每个文件解析后递归导入其后续文件。
3. 对 `/system_ext/etc/init`、`/vendor/etc/init`、`/odm/etc/init`、`/product/etc/init` 重复步骤 2。

以下伪代码可能更清楚地解释了这一点：

    fn Import(file)
      Parse(file)
      for (import : file.imports)
        Import(import)
    
    Import(/system/etc/init/hw/init.rc)
    Directories = [/system/etc/init, /system_ext/etc/init, /vendor/etc/init, /odm/etc/init, /product/etc/init]
    for (directory : Directories)
      files = <Alphabetical order of directory's contents>
      for (file : files)
        Import(file)

Action按照它们被解析的顺序执行。例如，`/system/etc/init/hw/init.rc`中的`post-fs-data`操作总是按照在该文件中出现的顺序首先执行。然后按顺序执行`/system/etc/init/hw/init.rc`中导入的`post-fs-data`操作，等等。

## Properties（系统属性）

Init提供以下属性的状态信息。

  `init.svc.<name>`

  > 指定服务的状态（“stopped”、“stopping”、“running”、“restarting”）

  `dev.mnt.dev.<mount_point>`, `dev.mnt.blk.<mount_point>`, `dev.mnt.rootdisk.<mount_point>`

  > 与*挂载点（mount_point）*相关联的块设备（Block device）基本名称。
  > *挂载点（mount_point）*中的”/“被替换为”.“，如果是指向根挂载点"/"，则使用"/root"。
  > `dev.mnt.dev.<mount_point>`表示附加到文件系统的块设备（block device）。
  > （例如，dm-N或sdaN/mmcblk0pN 可以访问 `/sys/fs/ext4/${dev.mnt.dev.<mount_point>}/`）

    `dev.mnt.blk.<mount_point>` indicates the disk partition to the above block device.
      (e.g., sdaN / mmcblk0pN to access `/sys/class/block/${dev.mnt.blk.<mount_point>}/`)
    
    `dev.mnt.rootdisk.<mount_point>` indicates the root disk to contain the above disk partition.
      (e.g., sda / mmcblk0 to access `/sys/class/block/${dev.mnt.rootdisk.<mount_point>}/queue`)

Init 对以 `ctl.` 开头的属性作出响应。这些属性的格式为 `ctl.[<target>_]<command>`，系统属性的 _value_ 用作参数。 _target_ 是可选的，指定 _value_ 意味着与之匹配的服务选项。 _target_ 只有一个选项，即 `interface`，表示 _value_ 将指代服务提供的接口而不是服务名称本身。

举个例子：

`SetProperty("ctl.start", "logd")` 将在 `logd` 上运行 `start` 命令。

`SetProperty("ctl.interface_start", "aidl/aidl_lazy_test_1")` 将在暴露 `aidl aidl_lazy_test_1` 接口的服务上运行 `start` 命令。

请注意，这些属性仅可设置；读取时将没有值。

以下是 _commands_。

`start`、`restart`、`stop`：这相当于在 *property* 的_value_指定的服务上使用 `start`、`restart` 和 `stop` 命令。

`oneshot_on` 和 `oneshot_off`：将为 *property* 的 _value_ 指定的服务打开或关闭 _oneshot_ 标志。这主要用于条件lazy HAL。当它们是lazy HAL 时，`oneshot` 必须打开，否则应关闭 `oneshot`。

`sigstop_on` 和 `sigstop_off`：将为 *property* 的 _value_ 指定的服务打开或关闭 _sigstop_ 功能。有关此功能的更多详细信息，请参阅下面的 _Debugging init_ 部分。

## Boot timing（启动时间）

Init在系统属性中记录了一些启动时间信息。

  `ro.boottime.init`

  > 以纳秒为单位的启动后时间（通过CLOCK_BOOTTIME时钟），表示init的第一阶段启动时刻。

  `ro.boottime.init.first_stage`

  > 第一阶段运行所花费的时间，以纳秒为单位。

  `ro.boottime.init.selinux`

  > SELinux阶段运行所花费的时间，以纳秒为单位。

  `ro.boottime.init.modules`

  > 加载内核模块所花费的时间，以毫秒为单位。

  `ro.boottime.init.cold_boot_wait`

  > init 等待 ueventd 冷启动阶段结束所花费的时间，以毫秒为单位。

  `ro.boottime.<service-name>`

  > 服务首次启动后距离启动后的时间，以纳秒为单位（通过 CLOCK_BOOTTIME 时钟）。

## Bootcharting（引导图）

此版本的init包含用于执行“bootcharting”（引导图）的代码：生成日志文件，稍后可以由http://www.bootchart.org/提供的工具进行处理。

在模拟器上，使用 `-bootchart timeout` 选项启动，bootchart激活为_timeout_秒。

在设备上执行以下命令：

      adb shell 'touch /data/bootchart/enabled'

收集数据后别忘了删除这个文件！

日志文件将被写入到 `/data/bootchart/` 目录下。提供了一个脚本来获取这些文件并创建一个 `bootchart.tgz` 文件，可以与 bootchart 命令行工具一起使用：

      sudo apt-get install pybootchartgui
      # grab-bootchart.sh uses $ANDROID_SERIAL.
      $ANDROID_BUILD_TOP/system/core/init/grab-bootchart.sh

需要注意的一点是，bootchart会显示 init 似乎是在 0 秒开始运行的。你需要查看 dmesg 来确定内核实际上何时启动了 init。

## Comparing two bootcharts（比较两个引导图）

前面提到的 `grab-bootchart.sh` 会在 `/tmp/android bootchart` 中留下一个名为 `bootchart.tgz` 的 bootchart 压缩包。如果在主机上的不同目录下保存了两个这样的压缩包，脚本可以列出时间戳的差异。例如

用法：system/core/init/compare-bootcharts.py _base-bootchart-dir_ _exp-bootchart-dir_

      process: baseline experiment (delta) - Unit is ms (a jiffy is 10 ms on the system)
      ------------------------------------
      /init: 50 40 (-10)
      /system/bin/surfaceflinger: 4320 4470 (+150)
      /system/bin/bootanimation: 6980 6990 (+10)
      zygote64: 10410 10640 (+230)
      zygote: 10410 10640 (+230)
      system_server: 15350 15150 (-200)
      bootanimation ends at: 33790 31230 (-2560)

## Systrace

Systrace（<http://developer.android.com/tools/help/systrace.html>）可用于在userdebug或eng版本上在开机启动获取性能分析报告。

下面是 "wm "和 "am "类别的跟踪事件示例：

      $ANDROID_BUILD_TOP/external/chromium-trace/systrace.py \
            wm am --boot

这个命令会导致设备重新启动。设备重新启动并完成启动序列后，通过按下Ctrl+C从设备获取跟踪报告，并在主机上将其写入为trace.html。

限制：在加载persist系统属性之后才会启动记录跟踪事件，因此在此之前发出的trace事件不会被记录。受此限制影响的几个服务包括vold、surfaceflinger和servicemanager，因为它们是在加载persist系统属性之前启动的。Zygote初始化和从Zygote分叉的进程不受影响。



## Debugging init（调试init）

当服务从 init 启动时，可能无法调用服务的`execv()`。这种情况并不常见，可能是链接器在启动新服务时发生了错误。Android 中的链接器会将日志打印到`logd`和`stderr`，因此这些错误在`logcat` 中是可以看到。如果在`logcat`之前遇到错误，则可以使用`stdio_to_kmsg`服务选项，将链接器打印的日志重定向到`stderr`到`kmsg`，从而可以通过串口读取这些日志。

在没有init的情况下启动init服务不是推荐的做法，因为init初始化了大量的环境（用户、组、安全标签、权限等），手动复制这些环境很困难。

如果需要从服务的最开始调试，可以添加 `sigstop` 服务（service）选项（option）。
该选项（option）会在调用`exec`之前立即向服务发送`SIGSTOP`信号。这会提供一个窗口，以供开发人员可以在继续使用`SIGCONT`之前附加调试器、strace等来调试服务（service）。

该标志也可以通过`ctl.sigstop_on`和`ctl.sigstop_off`属性进行动态控制。

下面是通过上述方法动态调试 logd 的示例：

      stop logd
      setprop ctl.sigstop_on logd
      start logd
      ps -e | grep logd
      > logd          4343     1   18156   1684 do_signal_stop 538280 T init
      gdbclient.py -p 4343
      b main
      c
      c
      c
      > Breakpoint 1, main (argc=1, argv=0x7ff8c9a488) at system/core/logd/main.cpp:427

下面是一个同样的示例，但使用的是 strace

      stop logd
      setprop ctl.sigstop_on logd
      start logd
      ps -e | grep logd
      > logd          4343     1   18156   1684 do_signal_stop 538280 T init
      strace -p 4343
      
      (From a different shell)
      kill -SIGCONT 4343
      
      > strace runs



## Host Init Script Verification（主机init脚本校验）

在编译系统过程中会检查初始脚本的正确性。具体检查内容如下：

    1) 良好g二十的 action、service 和 import 部分等等， 在“on”行之前没有action，在“import”语句之后没有额外的行；
    2) 所有command都映射到一个有效的关键字，且参数数在正确范围内；
    3) 所有service的option均有效。这比command的检查方式更严格，因为服务选项的参数已完全解析，例如 UID 和 GID 必须解析。

Init脚本的其他部分只在运行时进行解析，因此不会在编译系统时进行检查，其中包括以下部分：

1. command参数的有效性，例如不检查文件路径是否实际存在、SELinux 是否允许操作或 UID 和 GID 是否解析；
2. 不检查服务是否存在或是否定义了有效的SELinux域；
3. 不检查以前是否没有在不同的init脚本中定义过服务；

## Early Init Boot Sequence（Early Init 启动顺序）

early init 启动顺序分为三个阶段：第一阶段 init、SELinux 设置和第二阶段 init。（1st --> SELinux --> 2rd）

第一阶段启动负责设置加载系统其余部分的最低要求。具体来说，这包括挂载 /dev、/proc、挂载'early mount' 分区（需要包括所有包含系统代码的分区，例如 system 和 vendor），以及将 system.img 挂载到带有 ramdisk 的设备根目录/上。

请注意，在 Android Q 中，system.img 始终包含 TARGET_ROOT_OUT，并且在第一阶段启动结束时始终挂载在根目录/上。Android Q 还需要动态分区，因此需要使用ramdisk 启动 Android。recovery ramdisk 也替代专用的ramdisk，可用于启动 Android。

根据设备配置的不同，第一阶段启动有三种不同的方式：

1) 对于 system-as-root 的设备，第一阶段 init 是 /system/bin/init 的一部分，为了向后兼容，/init 的符号链接
   的符号链接指向 /system/bin/init，以实现向后兼容。这些设备不需要做任何事情来挂载 system.img，因为根据定义，它已经被内核挂载为 rootfs。
2) 对于带有 ramdisk 的设备，第一阶段 init 是位于 /init 的静态可执行文件。这些设备会将 system.img 挂载到 /system，然后执行切换 root 操作，将挂载在 /system 的内容移动到 /。挂载完成后，ramdisk 中的内容将被释放。
3) 对于将 recovery 用作 ramdisk 的设备，第一阶段 init 包含在 recovery ramdisk ，位于 /init 的共享 init 中。这些设备首先将根目录切换到/first_stage_ramdisk，以从环境中删除恢复组件，然后继续执行与上面第2点相同的操作；请注意，如果androidboot.force_normal_boot=1出现在内核命令行中，或者出现在安卓S和更高版本的引导配置中，则会决定正常引导到安卓系统，而不是引导到recovery模式。

第一阶段启动完成后，它会执行带有 "selinux_setup "参数的 /system/bin/init。在这一阶段，SELinux 会被编译并加载到系统中。selinux.cpp包含了关于此过程的具体细节的更多信息。

最后，一旦该阶段结束，它将再次执行 /system/bin/init，并使用 "second_stage "参数。此时，init 的主阶段运行，并通过 init.rc 脚本继续启动过程。



---

# Android Init Language README.md

## Android Init Language

The Android Init Language consists of five broad classes of statements: Actions, Commands, Services, Options, and Imports.

All of these are line-oriented, consisting of tokens separated by whitespace. The c-style backslash escapes may be used to insert whitespace into a token. Double quotes may also be used to prevent whitespace from breaking text into multiple tokens. The backslash, when it is the last character on a line, may be used for line-folding.

Lines which start with a `#` (leading whitespace allowed) are comments.

System properties can be expanded using the syntax `${property.name}`. This also works in contexts where concatenation is required, such as `import /init.recovery.${ro.hardware}.rc`.

Actions and Services implicitly declare a new section. All commands or options belong to the section most recently declared. Commands or options before the first section are ignored.

Services have unique names. If a second Service is defined with the same name as an existing one, it is ignored and an error message is logged.

## Init .rc Files

The init language is used in plain text files that take the .rc file extension. There are typically multiple of these in multiple locations on the system, described below.

`/system/etc/init/hw/init.rc` is the primary .rc file and is loaded by the init executable at the beginning of its execution. It is responsible for the initial set up of the system.

Init loads all of the files contained within the `/{system,system_ext,vendor,odm,product}/etc/init/` directories immediately after loading the primary `/system/etc/init/hw/init.rc`. This is explained in more details in the [Imports](https://cs.android.com/android/platform/superproject/main/+/main:system/core/init/README.md#imports) section of this file.

Legacy devices without the first stage mount mechanism previously were able to import init scripts during mount_all, however that is deprecated and not allowed for devices launching after Q.

The intention of these directories is:

1. /system/etc/init/ is for core system items such as SurfaceFlinger, MediaService, and logd.
2. /vendor/etc/init/ is for SoC vendor items such as actions or daemons needed for core SoC functionality.
3. /odm/etc/init/ is for device manufacturer items such as actions or daemons needed for motion sensor or other peripheral functionality.

All services whose binaries reside on the system, vendor, or odm partitions should have their service entries placed into a corresponding init .rc file, located in the /etc/init/ directory of the partition where they reside. There is a build system macro, LOCAL_INIT_RC, that handles this for developers. Each init .rc file should additionally contain any actions associated with its service.

An example is the userdebug logcatd.rc and Android.mk files located in the system/core/logcat directory. The LOCAL_INIT_RC macro in the Android.mk file places logcatd.rc in /system/etc/init/ during the build process. Init loads logcatd.rc during the mount_all command and allows the service to be run and the action to be queued when appropriate.

This break up of init .rc files according to their daemon is preferred to the previously used monolithic init .rc files. This approach ensures that the only service entries that init reads and the only actions that init performs correspond to services whose binaries are in fact present on the file system, which was not the case with the monolithic init .rc files. This additionally will aid in merge conflict resolution when multiple services are added to the system, as each one will go into a separate file.

## Versioned RC files within APEXs

With the arrival of mainline on Android Q, the individual mainline modules carry their own init.rc files within their boundaries. Init processes these files according to the naming pattern `/apex/*/etc/*rc`.

Because APEX modules must run on more than one release of Android, they may require different parameters as part of the services they define. This is achieved, starting in Android T, by incorporating the SDK version information in the name of the init file. The suffix is changed from `.rc` to `.#rc` where # is the first SDK where that RC file is accepted. An init file specific to SDK=31 might be named `init.31rc`. With this scheme, an APEX may include multiple init files. An example is appropriate.

For an APEX module with the following files in /apex/sample-module/apex/etc/:

1. init.rc
2. init.32rc
3. init.35rc

The selection rule chooses the highest `.#rc` value that does not exceed the SDK of the currently running system. The unadorned `.rc` is interpreted as sdk=0.

When this APEX is installed on a device with SDK <=31, the system will process init.rc. When installed on a device running SDK 32, 33, or 34, it will use init.32rc. When installed on a device running SDKs >= 35, it will choose init.35rc

This versioning scheme is used only for the init files within APEX modules; it does not apply to the init files stored in /system/etc/init, /vendor/etc/init, or other directories.

This naming scheme is available after Android S.

## Actions

Actions are named sequences of commands. Actions have a trigger which is used to determine when the action is executed. When an event occurs which matches an action's trigger, that action is added to the tail of a to-be-executed queue (unless it is already on the queue).

Each action in the queue is dequeued in sequence and each command in that action is executed in sequence. Init handles other activities (device creation/destruction, property setting, process restarting) "between" the execution of the commands in activities.

Actions take the form of:

```
on <trigger> [&& <trigger>]*
   <command>
   <command>
   <command>
```

Actions are added to the queue and executed based on the order that the file that contains them was parsed (see the Imports section), then sequentially within an individual file.

For example if a file contains:

```
on boot
   setprop a 1
   setprop b 2

on boot && property:true=true
   setprop c 1
   setprop d 2

on boot
   setprop e 1
   setprop f 2
```

Then when the `boot` trigger occurs and assuming the property `true` equals `true`, then the order of the commands executed will be:

```
setprop a 1
setprop b 2
setprop c 1
setprop d 2
setprop e 1
setprop f 2
```

If the property `true` wasn't `true` when the `boot` was triggered, then the order of the commands executed will be:

```
setprop a 1
setprop b 2
setprop e 1
setprop f 2
```

If the property `true` becomes `true` *AFTER* `boot` was triggered, nothing will be executed. The condition `boot && property:true=true` will be evaluated to false because the `boot` trigger is a past event.

Note that when `ro.property_service.async_persist_writes` is `true`, there is no defined ordering between persistent setprops and non-persistent setprops. For example:

```
on boot
    setprop a 1
    setprop persist.b 2
```

When `ro.property_service.async_persist_writes` is `true`, triggers for these two properties may execute in any order.

## Services

Services are programs which init launches and (optionally) restarts when they exit. Services take the form of:

```
service <name> <pathname> [ <argument> ]*
   <option>
   <option>
   ...
```

## Options

Options are modifiers to services. They affect how and when init runs the service.

```
capabilities [ <capability>\* ]
```

> Set capabilities when exec'ing this service. 'capability' should be a Linux capability without the "CAP_" prefix, like "NET_ADMIN" or "SETPCAP". See http://man7.org/linux/man-pages/man7/capabilities.7.html for a list of Linux capabilities. If no capabilities are provided, then behaviour depends on the user the service runs under: * if it's root, then the service will run with all the capabitilies (note: whether the service can actually use them is controlled by selinux); * otherwise all capabilities will be dropped.

```
class <name> [ <name>\* ]
```

> Specify class names for the service. All services in a named class may be started or stopped together. A service is in the class "default" if one is not specified via the class option. Additional classnames beyond the (required) first one are used to group services. The `animation` class should include all services necessary for both boot animation and shutdown animation. As these services can be launched very early during bootup and can run until the last stage of shutdown, access to /data partition is not guaranteed. These services can check files under /data but it should not keep files opened and should work when /data is not available.

```
console [<console>]
```

> This service needs a console. The optional second parameter chooses a specific console instead of the default. The default "/dev/console" can be changed by setting the "androidboot.console" kernel parameter. In all cases the leading "/dev/" should be omitted, so "/dev/tty0" would be specified as just "console tty0". This option connects stdin, stdout, and stderr to the console. It is mutually exclusive with the stdio_to_kmsg option, which only connects stdout and stderr to kmsg.

```
critical [window=<fatal crash window mins>] [target=<fatal reboot target>]
```

> This is a device-critical service. If it exits more than four times in *fatal crash window mins* minutes or before boot completes, the device will reboot into *fatal reboot target*. The default value of *fatal crash window mins* is 4, and default value of *fatal reboot target* is 'bootloader'. For tests, the fatal reboot can be skipped by setting property `init.svc_debug.no_fatal.<service-name>` to `true` for specified critical service.

```
disabled
```

> This service will not automatically start with its class. It must be explicitly started by name or by interface name.

```
enter_namespace <type> <path>
```

> Enters the namespace of type *type* located at *path*. Only network namespaces are supported with *type* set to "net". Note that only one namespace of a given *type* may be entered.

```
file <path> <type>
```

> Open a file path and pass its fd to the launched process. *type* must be "r", "w" or "rw". For native executables see libcutils android_get_control_file().

```
gentle_kill
```

> This service will be sent SIGTERM instead of SIGKILL when stopped. After a 200 ms timeout, it will be sent SIGKILL.

```
group <groupname> [ <groupname>\* ]
```

> Change to 'groupname' before exec'ing this service. Additional groupnames beyond the (required) first one are used to set the supplemental groups of the process (via setgroups()). Currently defaults to root. (??? probably should default to nobody)

```
interface <interface name> <instance name>
```

> Associates this service with a list of the AIDL or HIDL services that it provides. The interface name must be a fully-qualified name and not a value name. For instance, this is used to allow servicemanager or hwservicemanager to lazily start services. When multiple interfaces are served, this tag should be used multiple times. An example of an entry for a HIDL interface is `interface vendor.foo.bar@1.0::IBaz default`. For an AIDL interface, use `interface aidl <instance name>`. The instance name for an AIDL interface is whatever is registered with servicemanager, and these can be listed with `adb shell dumpsys -l`.

```
ioprio <class> <priority>
```

> Sets the IO priority and IO priority class for this service via the SYS_ioprio_set syscall. *class* must be one of "rt", "be", or "idle". *priority* must be an integer in the range 0 - 7.

```
keycodes <keycode> [ <keycode>\* ]
```

> Sets the keycodes that will trigger this service. If all of the keys corresponding to the passed keycodes are pressed at once, the service will start. This is typically used to start the bugreport service.

> This option may take a property instead of a list of keycodes. In this case, only one option is provided: the property name in the typical property expansion format. The property must contain a comma separated list of keycode values or the text 'none' to indicate that this service does not respond to keycodes.

> For example, `keycodes ${some.property.name:-none}` where some.property.name expands to "123,124,125". Since keycodes are handled very early in init, only PRODUCT_DEFAULT_PROPERTY_OVERRIDES properties can be used.

```
memcg.limit_in_bytes <value>` and `memcg.limit_percent <value>
```

> Sets the child's memory.limit_in_bytes to the minimum of `limit_in_bytes` bytes and `limit_percent` which is interpreted as a percentage of the size of the device's physical memory (only if memcg is mounted). Values must be equal or greater than 0.

```
memcg.limit_property <value>
```

> Sets the child's memory.limit_in_bytes to the value of the specified property (only if memcg is mounted). This property will override the values specified via `memcg.limit_in_bytes` and `memcg.limit_percent`.

```
memcg.soft_limit_in_bytes <value>
```

> Sets the child's memory.soft_limit_in_bytes to the specified value (only if memcg is mounted), which must be equal or greater than 0.

```
memcg.swappiness <value>
```

> Sets the child's memory.swappiness to the specified value (only if memcg is mounted), which must be equal or greater than 0.

```
namespace <pid|mnt>
```

> Enter a new PID or mount namespace when forking the service.

```
oneshot
```

> Do not restart the service when it exits.

```
onrestart
```

> Execute a Command (see below) when service restarts.

```
oom_score_adjust <value>
```

> Sets the child's /proc/self/oom_score_adj to the specified value, which must range from -1000 to 1000.

```
override
```

> Indicates that this service definition is meant to override a previous definition for a service with the same name. This is typically meant for services on /odm to override those defined on /vendor. The last service definition that init parses with this keyword is the service definition will use for this service. Pay close attention to the order in which init.rc files are parsed, since it has some peculiarities for backwards compatibility reasons. The 'imports' section of this file has more details on the order.

```
priority <priority>
```

> Scheduling priority of the service process. This value has to be in range -20 to 19. Default priority is 0. Priority is set via setpriority().

```
reboot_on_failure <target>
```

> If this process cannot be started or if the process terminates with an exit code other than CLD_EXITED or an status other than '0', reboot the system with the target specified in *target*. *target* takes the same format as the parameter to sys.powerctl. This is particularly intended to be used with the `exec_start` builtin for any must-have checks during boot.

```
restart_period <seconds>
```

> If a non-oneshot service exits, it will be restarted at its previous start time plus this period. The default value is 5s. This can be used to implement periodic services together with the `timeout_period` command below. For example, it may be set to 3600 to indicate that the service should run every hour or 86400 to indicate that the service should run every day. This can be set to a value shorter than 5s for example 0, but the minimum 5s delay is enforced if the restart was due to a crash. This is to rate limit persistentally crashing services. In other words, `<seconds>` smaller than 5 is respected only when the service exits deliverately and successfully (i.e. by calling exit(0)).

```
rlimit <resource> <cur> <max>
```

> This applies the given rlimit to the service. rlimits are inherited by child processes, so this effectively applies the given rlimit to the process tree started by this service. It is parsed similarly to the setrlimit command specified below.

```
seclabel <seclabel>
```

> Change to 'seclabel' before exec'ing this service. Primarily for use by services run from the rootfs, e.g. ueventd, adbd. Services on the system partition can instead use policy-defined transitions based on their file security context. If not specified and no transition is defined in policy, defaults to the init context.

```
setenv <name> <value>
```

> Set the environment variable *name* to *value* in the launched process.

```
shutdown <shutdown_behavior>
```

> Set shutdown behavior of the service process. When this is not specified, the service is killed during shutdown process by using SIGTERM and SIGKILL. The service with shutdown_behavior of "critical" is not killed during shutdown until shutdown times out. When shutdown times out, even services tagged with "shutdown critical" will be killed. When the service tagged with "shutdown critical" is not running when shut down starts, it will be started.

```
sigstop
```

> Send SIGSTOP to the service immediately before exec is called. This is intended for debugging. See the below section on debugging for how this can be used.

```
socket <name> <type> <perm> [ <user> [ <group> [ <seclabel> ] ] ]
```

> Create a UNIX domain socket named /dev/socket/*name* and pass its fd to the launched process. The socket is created synchronously when the service starts. *type* must be "dgram", "stream" or "seqpacket". *type* may end with "+passcred" to enable SO_PASSCRED on the socket or "+listen" to synchronously make it a listening socket. User and group default to 0. 'seclabel' is the SELinux security context for the socket. It defaults to the service security context, as specified by seclabel or computed based on the service executable file security context. For native executables see libcutils android_get_control_socket().

```
stdio_to_kmsg
```

> Redirect stdout and stderr to /dev/kmsg_debug. This is useful for services that do not use native Android logging during early boot and whose logs messages we want to capture. This is only enabled when /dev/kmsg_debug is enabled, which is only enabled on userdebug and eng builds. This is mutually exclusive with the console option, which additionally connects stdin to the given console.

```
task_profiles <profile> [ <profile>\* ]
```

> Set task profiles. Before Android U, the profiles are applied to the main thread of the service. For Android U and later, the profiles are applied to the entire service process. This is designed to replace the use of writepid option for moving a process into a cgroup.

```
timeout_period <seconds>
```

> Provide a timeout after which point the service will be killed. The oneshot keyword is respected here, so oneshot services do not automatically restart, however all other services will. This is particularly useful for creating a periodic service combined with the restart_period option described above.

```
updatable
```

> Mark that the service can be overridden (via the 'override' option) later in the boot sequence by APEXes. When a service with updatable option is started before APEXes are all activated, the execution is delayed until the activation is finished. A service that is not marked as updatable cannot be overridden by APEXes.

```
user <username>
```

> Change to 'username' before exec'ing this service. Currently defaults to root. (??? probably should default to nobody) As of Android M, processes should use this option even if they require Linux capabilities. Previously, to acquire Linux capabilities, a process would need to run as root, request the capabilities, then drop to its desired uid. There is a new mechanism through fs_config that allows device manufacturers to add Linux capabilities to specific binaries on a file system that should be used instead. This mechanism is described on http://source.android.com/devices/tech/config/filesystem.html. When using this new mechanism, processes can use the user option to select their desired uid without ever running as root. As of Android O, processes can also request capabilities directly in their .rc files. See the "capabilities" option above.

```
writepid <file> [ <file>\* ]
```

> Write the child's pid to the given files when it forks. Meant for cgroup/cpuset usage. If no files under /dev/cpuset/ are specified, but the system property 'ro.cpuset.default' is set to a non-empty cpuset name (e.g. '/foreground'), then the pid is written to file /dev/cpuset/*cpuset_name*/tasks. The use of this option for moving a process into a cgroup is obsolete. Please use task_profiles option instead.

## Triggers

Triggers are strings which can be used to match certain kinds of events and used to cause an action to occur.

Triggers are subdivided into event triggers and property triggers.

Event triggers are strings triggered by the 'trigger' command or by the QueueEventTrigger() function within the init executable. These take the form of a simple string such as 'boot' or 'late-init'.

Property triggers are strings triggered when a named property changes value to a given new value or when a named property changes value to any new value. These take the form of 'property:

An Action can have multiple property triggers but may only have one event trigger.

For example: `on boot && property:a=b` defines an action that is only executed when the 'boot' event trigger happens and the property a equals b at the moment. This will NOT be executed when the property a transitions to value b after the `boot` event was triggered.

`on property:a=b && property:c=d` defines an action that is executed at three times:

1. During initial boot if property a=b and property c=d.
2. Any time that property a transitions to value b, while property c already equals d.
3. Any time that property c transitions to value d, while property a already equals b.

## Trigger Sequence

Init uses the following sequence of triggers during early boot. These are the built-in triggers defined in init.cpp.

1. `early-init` - The first in the sequence, triggered after cgroups has been configured but before ueventd's coldboot is complete.
2. `init` - Triggered after coldboot is complete.
3. `charger` - Triggered if `ro.bootmode == "charger"`.
4. `late-init` - Triggered if `ro.bootmode != "charger"`, or via healthd triggering a boot from charging mode.

Remaining triggers are configured in `init.rc` and are not built-in. The default sequence for these is specified under the "on late-init" event in `init.rc`. Actions internal to `init.rc` have been omitted.

1. `early-fs` - Start vold.
2. `fs` - Vold is up. Mount partitions not marked as first-stage or latemounted.
3. `post-fs` - Configure anything dependent on early mounts.
4. `late-fs` - Mount partitions marked as latemounted.
5. `post-fs-data` - Mount and configure `/data`; set up encryption. `/metadata` is reformatted here if it couldn't mount in first-stage init.
6. `zygote-start` - Start the zygote.
7. `early-boot` - After zygote has started.
8. `boot` - After `early-boot` actions have completed.

## Commands

```
bootchart [start|stop]
```

> Start/stop bootcharting. These are present in the default init.rc files, but bootcharting is only active if the file /data/bootchart/enabled exists; otherwise bootchart start/stop are no-ops.

```
chmod <octal-mode> <path>
```

> Change file access permissions.

```
chown <owner> <group> <path>
```

> Change file owner and group.

```
class_start <serviceclass>
```

> Start all services of the specified class if they are not already running. See the start entry for more information on starting services.

```
class_stop <serviceclass>
```

> Stop and disable all services of the specified class if they are currently running.

```
class_reset <serviceclass>
```

> Stop all services of the specified class if they are currently running, without disabling them. They can be restarted later using `class_start`.

```
class_restart [--only-enabled] <serviceclass>
```

> Restarts all services of the specified class. If `--only-enabled` is specified, then disabled services are skipped.

```
copy <src> <dst>
```

> Copies a file. Similar to write, but useful for binary/large amounts of data. Regarding to the src file, copying from symbolic link file and world-writable or group-writable files are not allowed. Regarding to the dst file, the default mode created is 0600 if it does not exist. And it will be truncated if dst file is a normal regular file and already exists.

```
copy_per_line <src> <dst>
```

> Copies a file line by line. Similar to copy, but useful for dst is a sysfs node that doesn't handle multiple lines of data.

```
domainname <name>
```

> Set the domain name.

```
enable <servicename>
```

> Turns a disabled service into an enabled one as if the service did not specify disabled. If the service is supposed to be running, it will be started now. Typically used when the bootloader sets a variable that indicates a specific service should be started when needed. E.g.

```
on property:ro.boot.myfancyhardware=1
    enable my_fancy_service_for_my_fancy_hardware
exec [ <seclabel> [ <user> [ <group>\* ] ] ] -- <command> [ <argument>\* ]
```

> Fork and execute command with the given arguments. The command starts after "--" so that an optional security context, user, and supplementary groups can be provided. No other commands will be run until this one finishes. *seclabel* can be a - to denote default. Properties are expanded within *argument*. Init halts executing commands until the forked process exits.

```
exec_background [ <seclabel> [ <user> [ <group>\* ] ] ] -- <command> [ <argument>\* ]
```

> Fork and execute command with the given arguments. This is handled similarly to the `exec` command. The difference is that init does not halt executing commands until the process exits for `exec_background`.

```
exec_start <service>
```

> Start a given service and halt the processing of additional init commands until it returns. The command functions similarly to the `exec` command, but uses an existing service definition in place of the exec argument vector.

```
export <name> <value>
```

> Set the environment variable *name* equal to *value* in the global environment (which will be inherited by all processes started after this command is executed)

```
hostname <name>
```

> Set the host name.

```
ifup <interface>
```

> Bring the network interface *interface* online.

```
insmod [-f] <path> [<options>]
```

> Install the module at *path* with the specified options. -f: force installation of the module even if the version of the running kernel and the version of the kernel for which the module was compiled do not match.

```
interface_start <name>`
`interface_restart <name>`
`interface_stop <name>
```

> Find the service that provides the interface *name* if it exists and run the `start`, `restart`, or `stop` commands on it respectively. *name* may be either a fully qualified HIDL name, in which case it is specified as `<interface>/<instance>`, or an AIDL name, in which case it is specified as `aidl/<interface>` for example `android.hardware.secure_element@1.1::ISecureElement/eSE1` or `aidl/aidl_lazy_test_1`.

> Note that these commands only act on interfaces specified by the `interface` service option, not on interfaces registered at runtime.

> Example usage of these commands:
> `interface_start android.hardware.secure_element@1.1::ISecureElement/eSE1` will start the HIDL Service that provides the `android.hardware.secure_element@1.1` and `eSI1` instance.
> `interface_start aidl/aidl_lazy_test_1` will start the AIDL service that provides the `aidl_lazy_test_1` interface.

```
load_exports <path>
```

> Open the file at *path* and export global environment variables declared there. Each line must be in the format `export <name> <value>`, as described above.

```
load_system_props
```

> (This action is deprecated and no-op.)

```
load_persist_props
```

> Loads persistent properties when /data has been decrypted. This is included in the default init.rc.

```
loglevel <level>
```

> Sets init's log level to the integer level, from 7 (all logging) to 0 (fatal logging only). The numeric values correspond to the kernel log levels, but this command does not affect the kernel log level. Use the `write` command to write to `/proc/sys/kernel/printk` to change that. Properties are expanded within *level*.

```
mark_post_data
```

> Used to mark the point right after /data is mounted.

```
mkdir <path> [<mode>] [<owner>] [<group>] [encryption=<action>] [key=<key>]
```

> Create a directory at *path*, optionally with the given mode, owner, and group. If not provided, the directory is created with permissions 755 and owned by the root user and root group. If provided, the mode, owner and group will be updated if the directory exists already. If the directory does not exist, it will receive the security context from the current SELinux policy or its parent if not specified in the policy. If the directory exists, its security context will not be changed (even if different from the policy).
>
> *action* can be one of:
>
> - `None`: take no encryption action; directory will be encrypted if parent is.
> - `Require`: encrypt directory, abort boot process if encryption fails
> - `Attempt`: try to set an encryption policy, but continue if it fails
> - `DeleteIfNecessary`: recursively delete directory if necessary to set encryption policy.
>
> *key* can be one of:
>
> - `ref`: use the systemwide DE key
> - `per_boot_ref`: use the key freshly generated on each boot.

```
mount_all [ <fstab> ] [--<option>]
```

> Calls fs_mgr_mount_all on the given fs_mgr-format fstab with optional options "early" and "late". With "--early" set, the init executable will skip mounting entries with "latemount" flag and triggering fs encryption state event. With "--late" set, init executable will only mount entries with "latemount" flag. By default, no option is set, and mount_all will process all entries in the given fstab. If the fstab parameter is not specified, fstab.${ro.boot.fstab_suffix}, fstab.${ro.hardware} or fstab.${ro.hardware.platform} will be scanned for under /odm/etc, /vendor/etc, or / at runtime, in that order.

```
mount <type> <device> <dir> [ <flag>\* ] [<options>]
```

> Attempt to mount the named device at the directory *dir* _flag_s include "ro", "rw", "remount", "noatime", ... *options* include "barrier=1", "noauto_da_alloc", "discard", ... as a comma separated string, e.g. barrier=1,noauto_da_alloc

```
perform_apex_config [--bootstrap]
```

> Performs tasks after APEXes are mounted. For example, creates data directories for the mounted APEXes, parses config file(s) from them, and updates linker configurations. Intended to be used only once when apexd notifies the mount event by setting `apexd.status` to ready. Use --bootstrap when invoking in the bootstrap mount namespace.

```
restart [--only-if-running] <service>
```

> Stops and restarts a running service, does nothing if the service is currently restarting, otherwise, it just starts the service. If "--only-if-running" is specified, the service is only restarted if it is already running.

```
restorecon <path> [ <path>\* ]
```

> Restore the file named by *path* to the security context specified in the file_contexts configuration. Not required for directories created by the init.rc as these are automatically labeled correctly by init.

```
restorecon_recursive <path> [ <path>\* ]
```

> Recursively restore the directory tree named by *path* to the security contexts specified in the file_contexts configuration.

```
rm <path>
```

> Calls unlink(2) on the given path. You might want to use "exec -- rm ..." instead (provided the system partition is already mounted).

```
rmdir <path>
```

> Calls rmdir(2) on the given path.

```
readahead <file|dir> [--fully]
```

> Calls readahead(2) on the file or files within given directory. Use option --fully to read the full file content.

```
setprop <name> <value>
```

> Set system property *name* to *value*. Properties are expanded within *value*.

```
setrlimit <resource> <cur> <max>
```

> Set the rlimit for a resource. This applies to all processes launched after the limit is set. It is intended to be set early in init and applied globally. *resource* is best specified using its text representation ('cpu', 'rtio', etc or 'RLIM_CPU', 'RLIM_RTIO', etc). It also may be specified as the int value that the resource enum corresponds to. *cur* and *max* can be 'unlimited' or '-1' to indicate an infinite rlimit.

```
start <service>
```

> Start a service running if it is not already running. Note that this is *not* synchronous, and even if it were, there is no guarantee that the operating system's scheduler will execute the service sufficiently to guarantee anything about the service's status. See the `exec_start` command for a synchronous version of `start`.

> This creates an important consequence that if the service offers functionality to other services, such as providing a communication channel, simply starting this service before those services is *not* sufficient to guarantee that the channel has been set up before those services ask for it. There must be a separate mechanism to make any such guarantees.

```
stop <service>
```

> Stop a service from running if it is currently running.

```
swapon_all [ <fstab> ]
```

> Calls fs_mgr_swapon_all on the given fstab file. If the fstab parameter is not specified, fstab.${ro.boot.fstab_suffix}, fstab.${ro.hardware} or fstab.${ro.hardware.platform} will be scanned for under /odm/etc, /vendor/etc, or / at runtime, in that order.

```
symlink <target> <path>
```

> Create a symbolic link at *path* with the value *target*

```
sysclktz <minutes_west_of_gmt>
```

> Set the system clock base (0 if system clock ticks in GMT)

```
trigger <event>
```

> Trigger an event. Used to queue an action from another action.

```
umount <path>
```

> Unmount the filesystem mounted at that path.

```
umount_all [ <fstab> ]
```

> Calls fs_mgr_umount_all on the given fstab file. If the fstab parameter is not specified, fstab.${ro.boot.fstab_suffix}, fstab.${ro.hardware} or fstab.${ro.hardware.platform} will be scanned for under /odm/etc, /vendor/etc, or / at runtime, in that order.

```
verity_update_state
```

> Internal implementation detail used to update dm-verity state and set the partition.*mount-point*.verified properties used by adb remount because fs_mgr can't set them directly itself. This is required since Android 12, because CtsNativeVerifiedBootTestCases will read property "partition.${partition}.verified.hash_alg" to check that sha1 is not used. See https://r.android.com/1546980 for more details.

```
wait <path> [ <timeout> ]
```

> Poll for the existence of the given file and return when found, or the timeout has been reached. If timeout is not specified it currently defaults to five seconds. The timeout value can be fractional seconds, specified in floating point notation.

```
wait_for_prop <name> <value>
```

> Wait for system property *name* to be *value*. Properties are expanded within *value*. If property *name* is already set to *value*, continue immediately.

```
write <path> <content>
```

> Open the file at *path* and write a string to it with write(2). If the file does not exist, it will be created. If it does exist, it will be truncated. Properties are expanded within *content*.

## Imports

```
import <path>
```

> Parse an init config file, extending the current configuration. If *path* is a directory, each file in the directory is parsed as a config file. It is not recursive, nested directories will not be parsed.

The import keyword is not a command, but rather its own section, meaning that it does not happen as part of an Action, but rather, imports are handled as a file is being parsed and follow the below logic.

There are only three times where the init executable imports .rc files:

1. When it imports `/system/etc/init/hw/init.rc` or the script indicated by the property `ro.boot.init_rc` during initial boot.
2. When it imports `/{system,system_ext,vendor,odm,product}/etc/init/` immediately after importing `/system/etc/init/hw/init.rc`.
3. (Deprecated) When it imports /{system,vendor,odm}/etc/init/ or .rc files at specified paths during mount_all, not allowed for devices launching after Q.

The order that files are imported is a bit complex for legacy reasons. The below is guaranteed:

1. `/system/etc/init/hw/init.rc` is parsed then recursively each of its imports are parsed.
2. The contents of `/system/etc/init/` are alphabetized and parsed sequentially, with imports happening recursively after each file is parsed.
3. Step 2 is repeated for `/system_ext/etc/init`, `/vendor/etc/init`, `/odm/etc/init`, `/product/etc/init`

The below pseudocode may explain this more clearly:

```
fn Import(file)
  Parse(file)
  for (import : file.imports)
    Import(import)

Import(/system/etc/init/hw/init.rc)
Directories = [/system/etc/init, /system_ext/etc/init, /vendor/etc/init, /odm/etc/init, /product/etc/init]
for (directory : Directories)
  files = <Alphabetical order of directory's contents>
  for (file : files)
    Import(file)
```

Actions are executed in the order that they are parsed. For example the `post-fs-data` action(s) in `/system/etc/init/hw/init.rc` are always the first `post-fs-data` action(s) to be executed in order of how they appear in that file. Then the `post-fs-data` actions of the imports of `/system/etc/init/hw/init.rc` in the order that they're imported, etc.

## Properties

Init provides state information with the following properties.

```
init.svc.<name>
```

> State of a named service ("stopped", "stopping", "running", "restarting")

```
dev.mnt.dev.<mount_point>`, `dev.mnt.blk.<mount_point>`, `dev.mnt.rootdisk.<mount_point>
```

> Block device base name associated with a *mount_point*. The *mount_point* has / replaced by . and if referencing the root mount point "/", it will use "/root". `dev.mnt.dev.<mount_point>` indicates a block device attached to filesystems. (e.g., dm-N or sdaN/mmcblk0pN to access `/sys/fs/ext4/${dev.mnt.dev.<mount_point>}/`)

`dev.mnt.blk.<mount_point>` indicates the disk partition to the above block device. (e.g., sdaN / mmcblk0pN to access `/sys/class/block/${dev.mnt.blk.<mount_point>}/`)

`dev.mnt.rootdisk.<mount_point>` indicates the root disk to contain the above disk partition. (e.g., sda / mmcblk0 to access `/sys/class/block/${dev.mnt.rootdisk.<mount_point>}/queue`)

Init responds to properties that begin with `ctl.`. These properties take the format of `ctl.[<target>_]<command>` and the *value* of the system property is used as a parameter. The *target* is optional and specifies the service option that *value* is meant to match with. There is only one option for *target*, `interface` which indicates that *value* will refer to an interface that a service provides and not the service name itself.

For example:

`SetProperty("ctl.start", "logd")` will run the `start` command on `logd`.

`SetProperty("ctl.interface_start", "aidl/aidl_lazy_test_1")` will run the `start` command on the service that exposes the `aidl aidl_lazy_test_1` interface.

Note that these properties are only settable; they will have no value when read.

The *commands* are listed below.

`start`
`restart`
`stop`
These are equivalent to using the `start`, `restart`, and `stop` commands on the service specified by the *value* of the property.

`oneshot_on` and `oneshot_off` will turn on or off the *oneshot* flag for the service specified by the *value* of the property. This is particularly intended for services that are conditionally lazy HALs. When they are lazy HALs, oneshot must be on, otherwise oneshot should be off.

`sigstop_on` and `sigstop_off` will turn on or off the *sigstop* feature for the service specified by the *value* of the property. See the *Debugging init* section below for more details about this feature.

## Boot timing

Init records some boot timing information in system properties.

```
ro.boottime.init
```

> Time after boot in ns (via the CLOCK_BOOTTIME clock) at which the first stage of init started.

```
ro.boottime.init.first_stage
```

> How long in ns it took to run first stage.

```
ro.boottime.init.selinux
```

> How long in ns it took to run SELinux stage.

```
ro.boottime.init.modules
```

> How long in ms it took to load kernel modules.

```
ro.boottime.init.cold_boot_wait
```

> How long init waited for ueventd's coldboot phase to end.

```
ro.boottime.<service-name>
```

> Time after boot in ns (via the CLOCK_BOOTTIME clock) that the service was first started.

## Bootcharting

This version of init contains code to perform "bootcharting": generating log files that can be later processed by the tools provided by http://www.bootchart.org/.

On the emulator, use the -bootchart *timeout* option to boot with bootcharting activated for *timeout* seconds.

On a device:

```
adb shell 'touch /data/bootchart/enabled'
```

Don't forget to delete this file when you're done collecting data!

The log files are written to /data/bootchart/. A script is provided to retrieve them and create a bootchart.tgz file that can be used with the bootchart command-line utility:

```
sudo apt-get install pybootchartgui
# grab-bootchart.sh uses $ANDROID_SERIAL.
$ANDROID_BUILD_TOP/system/core/init/grab-bootchart.sh
```

One thing to watch for is that the bootchart will show init as if it started running at 0s. You'll have to look at dmesg to work out when the kernel actually started init.

## Comparing two bootcharts

A handy script named compare-bootcharts.py can be used to compare the start/end time of selected processes. The aforementioned grab-bootchart.sh will leave a bootchart tarball named bootchart.tgz at /tmp/android-bootchart. If two such tarballs are preserved on the host machine under different directories, the script can list the timestamps differences. For example:

Usage: system/core/init/compare-bootcharts.py *base-bootchart-dir* *exp-bootchart-dir*

```
process: baseline experiment (delta) - Unit is ms (a jiffy is 10 ms on the system)
------------------------------------
/init: 50 40 (-10)
/system/bin/surfaceflinger: 4320 4470 (+150)
/system/bin/bootanimation: 6980 6990 (+10)
zygote64: 10410 10640 (+230)
zygote: 10410 10640 (+230)
system_server: 15350 15150 (-200)
bootanimation ends at: 33790 31230 (-2560)
```

## Systrace

Systrace (http://developer.android.com/tools/help/systrace.html) can be used for obtaining performance analysis reports during boot time on userdebug or eng builds.

Here is an example of trace events of "wm" and "am" categories:

```
$ANDROID_BUILD_TOP/external/chromium-trace/systrace.py \
      wm am --boot
```

This command will cause the device to reboot. After the device is rebooted and the boot sequence has finished, the trace report is obtained from the device and written as trace.html on the host by hitting Ctrl+C.

Limitation: recording trace events is started after persistent properties are loaded, so the trace events that are emitted before that are not recorded. Several services such as vold, surfaceflinger, and servicemanager are affected by this limitation since they are started before persistent properties are loaded. Zygote initialization and the processes that are forked from the zygote are not affected.

## Debugging init

When a service starts from init, it may fail to `execv()` the service. This is not typical, and may point to an error happening in the linker as the new service is started. The linker in Android prints its logs to `logd` and `stderr`, so they are visible in `logcat`. If the error is encountered before it is possible to access `logcat`, the `stdio_to_kmsg` service option may be used to direct the logs that the linker prints to `stderr` to `kmsg`, where they can be read via a serial port.

Launching init services without init is not recommended as init sets up a significant amount of environment (user, groups, security label, capabilities, etc) that is hard to replicate manually.

If it is required to debug a service from its very start, the `sigstop` service option is added. This option will send SIGSTOP to a service immediately before calling exec. This gives a window where developers can attach a debugger, strace, etc before continuing the service with SIGCONT.

This flag can also be dynamically controlled via the ctl.sigstop_on and ctl.sigstop_off properties.

Below is an example of dynamically debugging logd via the above:

```
stop logd
setprop ctl.sigstop_on logd
start logd
ps -e | grep logd
> logd          4343     1   18156   1684 do_signal_stop 538280 T init
gdbclient.py -p 4343
b main
c
c
c
> Breakpoint 1, main (argc=1, argv=0x7ff8c9a488) at system/core/logd/main.cpp:427
```

Below is an example of doing the same but with strace

```
stop logd
setprop ctl.sigstop_on logd
start logd
ps -e | grep logd
> logd          4343     1   18156   1684 do_signal_stop 538280 T init
strace -p 4343

(From a different shell)
kill -SIGCONT 4343

> strace runs
```

## Host Init Script Verification

Init scripts are checked for correctness during build time. Specifically the below is checked.

1. Well formatted action, service and import sections, e.g. no actions without a preceding 'on' line, and no extraneous lines after an 'import' statement.
2. All commands map to a valid keyword and the argument count is within the correct range.
3. All service options are valid. This is stricter than how commands are checked as the service options' arguments are fully parsed, e.g. UIDs and GIDs must resolve.

There are other parts of init scripts that are only parsed at runtime and therefore not checked during build time, among them are the below.

1. The validity of the arguments of commands, e.g. no checking if file paths actually exist, if SELinux would permit the operation, or if the UIDs and GIDs resolve.
2. No checking if a service exists or has a valid SELinux domain defined
3. No checking if a service has not been previously defined in a different init script.

## Early Init Boot Sequence

The early init boot sequence is broken up into three stages: first stage init, SELinux setup, and second stage init.

First stage init is responsible for setting up the bare minimum requirements to load the rest of the system. Specifically this includes mounting /dev, /proc, mounting 'early mount' partitions (which needs to include all partitions that contain system code, for example system and vendor), and moving the system.img mount to / for devices with a ramdisk.

Note that in Android Q, system.img always contains TARGET_ROOT_OUT and always is mounted at / by the time first stage init finishes. Android Q will also require dynamic partitions and therefore will require using a ramdisk to boot Android. The recovery ramdisk can be used to boot to Android instead of a dedicated ramdisk as well.

First stage init has three variations depending on the device configuration:

1. For system-as-root devices, first stage init is part of /system/bin/init and a symlink at /init points to /system/bin/init for backwards compatibility. These devices do not need to do anything to mount system.img, since it is by definition already mounted as the rootfs by the kernel.
2. For devices with a ramdisk, first stage init is a static executable located at /init. These devices mount system.img as /system then perform a switch root operation to move the mount at /system to /. The contents of the ramdisk are freed after mounting has completed.
3. For devices that use recovery as a ramdisk, first stage init it contained within the shared init located at /init within the recovery ramdisk. These devices first switch root to /first_stage_ramdisk to remove the recovery components from the environment, then proceed the same as 2). Note that the decision to boot normally into Android instead of booting into recovery mode is made if androidboot.force_normal_boot=1 is present in the kernel commandline, or in bootconfig with Android S and later.

Once first stage init finishes it execs /system/bin/init with the "selinux_setup" argument. This phase is where SELinux is optionally compiled and loaded onto the system. selinux.cpp contains more information on the specifics of this process.

Lastly once that phase finishes, it execs /system/bin/init again with the "second_stage" argument. At this point the main phase of init runs and continues the boot process via the init.rc scripts.
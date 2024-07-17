# 【Android系统启动】 Android Zygote 进程启动流程源码解析

![e09bbb73e74ac183b226f49fdfcb6c1](./【Android系统启动】 Android Zygote 进程启动流程源码解析.assets/e09bbb73e74ac183b226f49fdfcb6c1.jpg)

## 前言

1. 文章源码按照AOSP官网源码[platform/superproject/main - Android Code Search](https://cs.android.com/android/platform/superproject/main/+/main:)进程代码进行解读；
2. 如有不当之处，麻烦指出作者进行修正



## 代码位置

> 1. frameworks/base/cmds/app_process/app_main.cpp



> 题外话， 之前找zygote源码的时候，本来想直接通过进程名找这个模块的源码，结果发现根本没有zygote这个名字的命令。通过命令查找到对应的进程目录发现，原来的进程的名字当时编译为`app_process`，实际文件一般在/system/bin下面。



## 源码解析

### Init拉起zygote

在`system/core/rootdir/init.rc`中， 

```rc
# It is recommended to put unnecessary data/ initialization from post-fs-data
# to start-zygote in device's init.rc to unblock zygote start.
on zygote-start
    wait_for_prop odsign.verification.done 1
    # A/B update verifier that marks a successful boot.
    exec_start update_verifier
    start statsd
    start netd
    start zygote
    start zygote_secondary
```

根据之前init.rc的官方README说明文档，以及源码解析，均可得知这里`start zygote`开始了zygote服务；分析见下方。

```markdown
Start a service running if it is not already running. Note that this is not synchronous, and even if it were, there is no guarantee that the operating system’s scheduler will execute the service sufficiently to guarantee anything about the service’s status. See the exec_start command for a synchronous version of start.
如果服务尚未运行，则启动该服务。
请注意，这不是同步的，即使它是同步的，也不能保证操作系统的调度程序会充分执行服务以确保服务的状态。
参见 exec_start 命令，以获取 start 的同步版本。
```



在init第二阶段的时候，有获取内置命令的逻辑，这部分命令用于解析执行init.rc

```C++
// system/core/init/init.cpp
	const BuiltinFunctionMap& function_map = GetBuiltinFunctionMap();
    Action::set_function_map(&function_map);
```

这里的Map实际对应下面这个Map，并且可以得知start方法调用的是do_start；

do_start先从服务列表里面找到这个服务，然后调用封装好的Service::Start()方法进行调用。


```C++

// system/core/init/builtins.cpp
// Builtin-function-map start
const BuiltinFunctionMap& GetBuiltinFunctionMap() {
    constexpr std::size_t kMax = std::numeric_limits<std::size_t>::max();
    // clang-format off
    static const BuiltinFunctionMap builtin_functions = {
        {"bootchart",               {1,     1,    {false,  do_bootchart}}},
        {"chmod",                   {2,     2,    {true,   do_chmod}}},
        {"chown",                   {2,     3,    {true,   do_chown}}},
        {"class_reset",             {1,     1,    {false,  do_class_reset}}},
        {"class_restart",           {1,     2,    {false,  do_class_restart}}},
        {"class_start",             {1,     1,    {false,  do_class_start}}},
        {"class_stop",              {1,     1,    {false,  do_class_stop}}},
        {"copy",                    {2,     2,    {true,   do_copy}}},
        {"copy_per_line",           {2,     2,    {true,   do_copy_per_line}}},
        {"domainname",              {1,     1,    {true,   do_domainname}}},
        {"enable",                  {1,     1,    {false,  do_enable}}},
        {"exec",                    {1,     kMax, {false,  do_exec}}},
        {"exec_background",         {1,     kMax, {false,  do_exec_background}}},
        {"exec_start",              {1,     1,    {false,  do_exec_start}}},
        {"export",                  {2,     2,    {false,  do_export}}},
        {"hostname",                {1,     1,    {true,   do_hostname}}},
        {"ifup",                    {1,     1,    {true,   do_ifup}}},
        {"init_user0",              {0,     0,    {false,  do_init_user0}}},
        {"insmod",                  {1,     kMax, {true,   do_insmod}}},
        {"installkey",              {1,     1,    {false,  do_installkey}}},
        {"interface_restart",       {1,     1,    {false,  do_interface_restart}}},
        {"interface_start",         {1,     1,    {false,  do_interface_start}}},
        {"interface_stop",          {1,     1,    {false,  do_interface_stop}}},
        {"load_exports",            {1,     1,    {false,  do_load_exports}}},
        {"load_persist_props",      {0,     0,    {false,  do_load_persist_props}}},
        {"load_system_props",       {0,     0,    {false,  do_load_system_props}}},
        {"loglevel",                {1,     1,    {false,  do_loglevel}}},
        {"mark_post_data",          {0,     0,    {false,  do_mark_post_data}}},
        {"mkdir",                   {1,     6,    {true,   do_mkdir}}},
        // TODO: Do mount operations in vendor_init.
        // mount_all is currently too complex to run in vendor_init as it queues action triggers,
        // imports rc scripts, etc.  It should be simplified and run in vendor_init context.
        // mount and umount are run in the same context as mount_all for symmetry.
        {"mount_all",               {0,     kMax, {false,  do_mount_all}}},
        {"mount",                   {3,     kMax, {false,  do_mount}}},
        {"perform_apex_config",     {0,     1,    {false,  do_perform_apex_config}}},
        {"umount",                  {1,     1,    {false,  do_umount}}},
        {"umount_all",              {0,     1,    {false,  do_umount_all}}},
        {"update_linker_config",    {0,     0,    {false,  do_update_linker_config}}},
        {"readahead",               {1,     2,    {true,   do_readahead}}},
        {"remount_userdata",        {0,     0,    {false,  do_remount_userdata}}},
        {"restart",                 {1,     2,    {false,  do_restart}}},
        {"restorecon",              {1,     kMax, {true,   do_restorecon}}},
        {"restorecon_recursive",    {1,     kMax, {true,   do_restorecon_recursive}}},
        {"rm",                      {1,     1,    {true,   do_rm}}},
        {"rmdir",                   {1,     1,    {true,   do_rmdir}}},
        {"setprop",                 {2,     2,    {true,   do_setprop}}},
        {"setrlimit",               {3,     3,    {false,  do_setrlimit}}},
        {"start",                   {1,     1,    {false,  do_start}}},
        {"stop",                    {1,     1,    {false,  do_stop}}},
        {"swapon_all",              {0,     1,    {false,  do_swapon_all}}},
        {"enter_default_mount_ns",  {0,     0,    {false,  do_enter_default_mount_ns}}},
        {"symlink",                 {2,     2,    {true,   do_symlink}}},
        {"sysclktz",                {1,     1,    {false,  do_sysclktz}}},
        {"trigger",                 {1,     1,    {false,  do_trigger}}},
        {"verity_update_state",     {0,     0,    {false,  do_verity_update_state}}},
        {"wait",                    {1,     2,    {true,   do_wait}}},
        {"wait_for_prop",           {2,     2,    {false,  do_wait_for_prop}}},
        {"write",                   {2,     2,    {true,   do_write}}},
    };
    // clang-format on
    return builtin_functions;
}

static Result<void> do_start(const BuiltinArguments& args) {
    Service* svc = ServiceList::GetInstance().FindService(args[1]);
    if (!svc) return Error() << "service " << args[1] << " not found";
    errno = 0;
    if (auto result = svc->Start(); !result.ok()) {
        return ErrorIgnoreEnoent() << "Could not start service: " << result.error();
    }
    return {};
}
```



Service::Start()比较冗长，省略了部分代码；其实质是通过判断配置值决定是调用 `fork()` 还是 `clone()` 来创建子进程或克隆进程。

```C++
Result<void> Service::Start() {
    
    // ...
    
    pid_t pid = -1;
    if (namespaces_.flags) {
        pid = clone(nullptr, nullptr, namespaces_.flags | SIGCHLD, nullptr);
    } else {
        pid = fork();
    }

    if (pid == 0) {
        umask(077);
        cgroups_activated.CloseWriteFd();
        setsid_finished.CloseReadFd();
        RunService(descriptors, std::move(cgroups_activated), std::move(setsid_finished));
        _exit(127);
    } else {
        cgroups_activated.CloseReadFd();
        setsid_finished.CloseWriteFd();
    }

    if (pid < 0) {
        pid_ = 0;
        return ErrnoError() << "Failed to fork";
    }

    // ...

    LOG(INFO) << "... started service '" << name_ << "' has pid " << pid_;

    return {};
}
```



然后补充一下，这个是system/core/rootdir/init.zygote32.rc，zygote通过initr.rc拉起时会逐一解析这些命令并且启动。（如果是64位系统，则为init.zygote64.rc）

```rc
service zygote /system/bin/app_process -Xzygote /system/bin --zygote --start-system-server
    class main
    priority -20
    user root
    group root readproc reserved_disk
    socket zygote stream 660 root system
    socket usap_pool_primary stream 660 root system
    onrestart exec_background - system system -- /system/bin/vdc volume abort_fuse
    onrestart write /sys/power/state on
    # NOTE: If the wakelock name here is changed, then also
    # update it in SystemSuspend.cpp
    onrestart write /sys/power/wake_lock zygote_kwl
    onrestart restart audioserver
    onrestart restart cameraserver
    onrestart restart media
    onrestart restart media.tuner
    onrestart restart netd
    onrestart restart wificond
    task_profiles ProcessCapacityHigh
    critical window=${zygote.critical_window.minute:-off} target=zygote-fatal
```





### Zygote Main

上面已经讲完Init如何拉起zygote了。下面进入zygote模块本身的代码。从进程名查找到该命令为app_process，然后再从bp或者mk源码中找app_process，即可找到这个命令的位置了。



```C++
int main(int argc, char* const argv[])
{
    
    // --------- LOG -----------
    if (!LOG_NDEBUG) {
      String8 argv_String;
      for (int i = 0; i < argc; ++i) {
        argv_String.append("\"");
        argv_String.append(argv[i]);
        argv_String.append("\" ");
      }
      ALOGV("app_process main with argv: %s", argv_String.c_str());
    }

    // ------------ Runtime初始化 ------------
    AppRuntime runtime(argv[0], computeArgBlockSize(argc, argv));
    // Process command line arguments
    // ignore argv[0]
    argc--;
    argv++;

    // Everything up to '--' or first non '-' arg goes to the vm.
    //
    // The first argument after the VM args is the "parent dir", which
    // is currently unused.
    //
    // After the parent dir, we expect one or more the following internal
    // arguments :
    //
    // --zygote : Start in zygote mode
    // --start-system-server : Start the system server.
    // --application : Start in application (stand alone, non zygote) mode.
    // --nice-name : The nice name for this process.
    //
    // For non zygote starts, these arguments will be followed by
    // the main class name. All remaining arguments are passed to
    // the main method of this class.
    //
    // For zygote starts, all remaining arguments are passed to the zygote.
    // main function.
    //
    // Note that we must copy argument string values since we will rewrite the
    // entire argument block when we apply the nice name to argv0.
    //
    // As an exception to the above rule, anything in "spaced commands"
    // goes to the vm even though it has a space in it.
    const char* spaced_commands[] = { "-cp", "-classpath" };
    // Allow "spaced commands" to be succeeded by exactly 1 argument (regardless of -s).
    bool known_command = false;

    // ------------ 解析参数
    int i;
    for (i = 0; i < argc; i++) {
        if (known_command == true) {
          runtime.addOption(strdup(argv[i]));
          // The static analyzer gets upset that we don't ever free the above
          // string. Since the allocation is from main, leaking it doesn't seem
          // problematic. NOLINTNEXTLINE
          ALOGV("app_process main add known option '%s'", argv[i]);
          known_command = false;
          continue;
        }

        for (int j = 0;
             j < static_cast<int>(sizeof(spaced_commands) / sizeof(spaced_commands[0]));
             ++j) {
          if (strcmp(argv[i], spaced_commands[j]) == 0) {
            known_command = true;
            ALOGV("app_process main found known command '%s'", argv[i]);
          }
        }

        if (argv[i][0] != '-') {
            break;
        }
        if (argv[i][1] == '-' && argv[i][2] == 0) {
            ++i; // Skip --.
            break;
        }

        runtime.addOption(strdup(argv[i]));
        // The static analyzer gets upset that we don't ever free the above
        // string. Since the allocation is from main, leaking it doesn't seem
        // problematic. NOLINTNEXTLINE
        ALOGV("app_process main add option '%s'", argv[i]);
    }

    // Parse runtime arguments.  Stop at first unrecognized option.
    bool zygote = false;
    bool startSystemServer = false;
    bool application = false;
    String8 niceName;
    String8 className;

    ++i;  // Skip unused "parent dir" argument.
    while (i < argc) {
        const char* arg = argv[i++];
        if (strcmp(arg, "--zygote") == 0) {
            zygote = true;
            niceName = ZYGOTE_NICE_NAME;
        } else if (strcmp(arg, "--start-system-server") == 0) {
            startSystemServer = true;
        } else if (strcmp(arg, "--application") == 0) {
            application = true;
        } else if (strncmp(arg, "--nice-name=", 12) == 0) {
            niceName = (arg + 12);
        } else if (strncmp(arg, "--", 2) != 0) {
            className = arg;
            break;
        } else {
            --i;
            break;
        }
    }

    Vector<String8> args;
    if (!className.empty()) {
        // We're not in zygote mode, the only argument we need to pass
        // to RuntimeInit is the application argument.
        //
        // The Remainder of args get passed to startup class main(). Make
        // copies of them before we overwrite them with the process name.
        args.add(application ? String8("application") : String8("tool"));
        runtime.setClassNameAndArgs(className, argc - i, argv + i);

        if (!LOG_NDEBUG) {
          String8 restOfArgs;
          char* const* argv_new = argv + i;
          int argc_new = argc - i;
          for (int k = 0; k < argc_new; ++k) {
            restOfArgs.append("\"");
            restOfArgs.append(argv_new[k]);
            restOfArgs.append("\" ");
          }
          ALOGV("Class name = %s, args = %s", className.c_str(), restOfArgs.c_str());
        }
    } else {
        // We're in zygote mode.
        maybeCreateDalvikCache();

        if (startSystemServer) {
            args.add(String8("start-system-server"));
        }

        char prop[PROP_VALUE_MAX];
        if (property_get(ABI_LIST_PROPERTY, prop, NULL) == 0) {
            LOG_ALWAYS_FATAL("app_process: Unable to determine ABI list from property %s.",
                ABI_LIST_PROPERTY);
            return 11;
        }

        String8 abiFlag("--abi-list=");
        abiFlag.append(prop);
        args.add(abiFlag);

        // In zygote mode, pass all remaining arguments to the zygote
        // main() method.
        for (; i < argc; ++i) {
            args.add(String8(argv[i]));
        }
    }

    if (!niceName.empty()) {
        runtime.setArgv0(niceName.c_str(), true /* setProcName */);
    }

    // -------------------- runtime start 
    if (zygote) {
        runtime.start("com.android.internal.os.ZygoteInit", args, zygote);
    } else if (!className.empty()) {
        runtime.start("com.android.internal.os.RuntimeInit", args, zygote);
    } else {
        fprintf(stderr, "Error: no class name or --zygote supplied.\n");
        app_usage();
        LOG_ALWAYS_FATAL("app_process: no class name or --zygote supplied.");
    }
}
```

上面主要干了这几件大事：

**Debug Logging**：如果 `LOG_NDEBUG` 为 false，将命令行参数以调试日志的形式输出。

**AppRuntime 初始化**：创建 `AppRuntime` 实例，用于处理应用程序的运行时环境。

**处理命令行参数**

- 忽略程序名 `argv[0]`。
- 将一些特定的命令行参数添加到运行时选项中。
- 根据 "--" 或非 '-' 开头的参数分隔命令行参数，一部分传递给虚拟机（VM），一部分用于启动类的 main() 方法。

**解析运行时参数**

- 根据特定参数设置标志和属性（如 `--zygote`、`--start-system-server`、`--application`、`--nice-name=<name>`）。
- 如果遇到 "--" 开头的参数或非 '-' 开头的参数，则停止解析。

**准备运行时参数列表**

- 如果存在类名 (`className`)，则将其作为参数传递给 `RuntimeInit`。
- 在 zygote 模式下，准备 ABI 列表和其他参数传递给 `ZygoteInit`。

**设置进程名称**

- 如果指定了 `--nice-name=<name>`，则设置进程名称。

**根据模式调用 `runtime` 的 `start()` 方法**

- 如果是 zygote 模式，则调用 `start()` 方法启动 `ZygoteInit`。
- 如果存在类名 (`className`)，则调用 `start()` 方法启动 `RuntimeInit`。
- 否则，输出错误信息并退出程序。

总的来说就是，准备AppRuntime，解析参数，设置进程名，调用runtime start()方法。

从上面zygote的rc文件也可以看到，一开始的参数为--start-system-server

```rc
service zygote /system/bin/app_process -Xzygote /system/bin --zygote --start-system-server
```



### AppRuntime start()

> frameworks/base/core/jni/AndroidRuntime.cpp

```C++
/*
 * Start the Android runtime.  This involves starting the virtual machine
 * and calling the "static void main(String[] args)" method in the class
 * named by "className".
 *
 * Passes the main function two arguments, the class name and the specified
 * options string.
 */
void AndroidRuntime::start(const char* className, const Vector<String8>& options, bool zygote)
{
    // 打印启动信息，包括类名和用户ID
    ALOGD(">>>>>> START %s uid %d <<<<<<\n",
            className != NULL ? className : "(unknown)", getuid());

    // 判断是否是主要的 zygote 进程
    static const String8 startSystemServer("start-system-server");
    bool primary_zygote = false;

    // 检查是否需要打印启动事件
    for (size_t i = 0; i < options.size(); ++i) {
        if (options[i] == startSystemServer) {
            primary_zygote = true;
            const int LOG_BOOT_PROGRESS_START = 3000;
            LOG_EVENT_LONG(LOG_BOOT_PROGRESS_START,  ns2ms(systemTime(SYSTEM_TIME_MONOTONIC)));
        }
    }

    // 设置环境变量
    const char* rootDir = getenv("ANDROID_ROOT");
    if (rootDir == NULL) {
        rootDir = "/system";
        if (!hasDir("/system")) {
            LOG_FATAL("No root directory specified, and /system does not exist.");
            return;
        }
        setenv("ANDROID_ROOT", rootDir, 1);
    }

    const char* artRootDir = getenv("ANDROID_ART_ROOT");
    if (artRootDir == NULL) {
        LOG_FATAL("No ART directory specified with ANDROID_ART_ROOT environment variable.");
        return;
    }

    const char* i18nRootDir = getenv("ANDROID_I18N_ROOT");
    if (i18nRootDir == NULL) {
        LOG_FATAL("No runtime directory specified with ANDROID_I18N_ROOT environment variable.");
        return;
    }

    const char* tzdataRootDir = getenv("ANDROID_TZDATA_ROOT");
    if (tzdataRootDir == NULL) {
        LOG_FATAL("No tz data directory specified with ANDROID_TZDATA_ROOT environment variable.");
        return;
    }

    // 初始化 JNI 调用
    JniInvocation jni_invocation;
    jni_invocation.Init(NULL);
    JNIEnv* env;

    // 启动虚拟机
    if (startVm(&mJavaVM, &env, zygote, primary_zygote) != 0) {
        return;
    }
    onVmCreated(env);

    // 注册 Android 原生方法
    if (startReg(env) < 0) {
        ALOGE("Unable to register all android natives\n");
        return;
    }

    // 创建 String 数组，用于传递给 Java 的 main 方法
    jclass stringClass;
    jobjectArray strArray;
    jstring classNameStr;

    stringClass = env->FindClass("java/lang/String");
    assert(stringClass != NULL);
    strArray = env->NewObjectArray(options.size() + 1, stringClass, NULL);
    assert(strArray != NULL);
    classNameStr = env->NewStringUTF(className);
    assert(classNameStr != NULL);
    env->SetObjectArrayElement(strArray, 0, classNameStr);

    for (size_t i = 0; i < options.size(); ++i) {
        jstring optionsStr = env->NewStringUTF(options.itemAt(i).c_str());
        assert(optionsStr != NULL);
        env->SetObjectArrayElement(strArray, i + 1, optionsStr);
    }

    // 调用 Java 的 main 方法启动应用程序
    char* slashClassName = toSlashClassName(className != NULL ? className : "");
    jclass startClass = env->FindClass(slashClassName);
    if (startClass == NULL) {
        ALOGE("JavaVM unable to locate class '%s'\n", slashClassName);
        /* keep going */
    } else {
        jmethodID startMeth = env->GetStaticMethodID(startClass, "main",
            "([Ljava/lang/String;)V");
        if (startMeth == NULL) {
            ALOGE("JavaVM unable to find main() in '%s'\n", className);
            /* keep going */
        } else {
            env->CallStaticVoidMethod(startClass, startMeth, strArray);
        }
    }
    free(slashClassName);

    ALOGD("Shutting down VM\n");
    // 分离主线程
    if (mJavaVM->DetachCurrentThread() != JNI_OK)
        ALOGW("Warning: unable to detach main thread\n");
    // 销毁虚拟机
    if (mJavaVM->DestroyJavaVM() != 0)
        ALOGW("Warning: VM did not shut down cleanly\n");
}

```

这里的主要职责：

1. **初始化**：打印启动信息、判断是否为systemserver进程、设置环境变量等；
2. **初始化 JNI 调用和启动虚拟机**
   1. 使用 `JniInvocation` 初始化 JNI 调用；
   2. 调用 `startVm` 方法启动虚拟机，并在虚拟机创建后调用 `onVmCreated`；
   3. 调用 `startReg` 方法注册 Android 原生方法，里面遍历调用`gRegJNI`数组，数组是一组 JNI 函数的函数指针；
3. **创建并传递参数给 Java 的 main 方法**
   1. 创建 `String` 类型的数组 `strArray`，用于传递给 Java 的 `main` 方法；
   2. 将类名和选项字符串转换为 Java 的 `String` 对象，并设置到 `strArray` 中；
4. **调用 Java 的 main 方法**
   1. 根据类名查找 `startClass`，并获取 `main` 方法的 `startMeth`；
   2. 使用 `env->CallStaticVoidMethod` 调用 Java 的 `main` 方法启动应用程序；
5. **关闭虚拟机**
   1. 执行完 `main` 方法后，分离主线程并销毁虚拟机。

这里总体就是初始化打印、环境变量、参数等，然后启动虚拟机-传递参数-调用main方法-关闭虚拟机。

不过通过观察这里会发现：

1. 每次上层的进程启动会调用这个start方法，而start方法开启且仅开启了一个虚拟机，那就是zygote基础上每一个进程，都会对应一个自己的虚拟环境；
2. 每个上层应用需要逐步调到系统层，都通过zygote这里JNI方式进行了调用。



### ZygoteInit.Main()

通过上面传下来的参数，"com.android.internal.os.ZygoteInit"，可以得知Java层的包名，以此找到Java代码。

> frameworks/base/core/java/com/android/internal/os/ZygoteInit.java

```Java
/**
 * This is the entry point for a Zygote process.  It creates the Zygote server, loads resources,
 * and handles other tasks related to preparing the process for forking into applications.
 *
 * This process is started with a nice value of -20 (highest priority).  All paths that flow
 * into new processes are required to either set the priority to the default value or terminate
 * before executing any non-system code.  The native side of this occurs in SpecializeCommon,
 * while the Java Language priority is changed in ZygoteInit.handleSystemServerProcess,
 * ZygoteConnection.handleChildProc, and Zygote.childMain.
 *
 * @param argv  Command line arguments used to specify the Zygote's configuration.
 */
@UnsupportedAppUsage
public static void main(String[] argv) {
    ZygoteServer zygoteServer = null;

    // 标记 Zygote 启动 确保在此后创建线程会抛出错误。
    // Mark zygote start. This ensures that thread creation will throw
    // an error.
    ZygoteHooks.startZygoteNoThreadCreation();

    // 调用 Os.setpgid(0, 0) 将 Zygote 放入自己的进程组。
    // Zygote goes into its own process group.
    try {
        Os.setpgid(0, 0);
    } catch (ErrnoException ex) {
        throw new RuntimeException("Failed to setpgid(0,0)", ex);
    }

    Runnable caller;
    try {
        // 解析命令行参数 argv，包括是否启动系统服务器 (start-system-server)、是否启用延迟预加载 (--enable-lazy-preload)、ABI 列表等。
        // Store now for StatsLogging later.
        final long startTime = SystemClock.elapsedRealtime();
        final boolean isRuntimeRestarted = "1".equals(
                SystemProperties.get("sys.boot_completed"));

        String bootTimeTag = Process.is64Bit() ? "Zygote64Timing" : "Zygote32Timing";
        TimingsTraceLog bootTimingsTraceLog = new TimingsTraceLog(bootTimeTag,
                Trace.TRACE_TAG_DALVIK);
        bootTimingsTraceLog.traceBegin("ZygoteInit");
        RuntimeInit.preForkInit();

        boolean startSystemServer = false;
        String zygoteSocketName = "zygote";
        String abiList = null;
        boolean enableLazyPreload = false;
        for (int i = 1; i < argv.length; i++) {
            if ("start-system-server".equals(argv[i])) {
                startSystemServer = true;
            } else if ("--enable-lazy-preload".equals(argv[i])) {
                enableLazyPreload = true;
            } else if (argv[i].startsWith(ABI_LIST_ARG)) {
                abiList = argv[i].substring(ABI_LIST_ARG.length());
            } else if (argv[i].startsWith(SOCKET_NAME_ARG)) {
                zygoteSocketName = argv[i].substring(SOCKET_NAME_ARG.length());
            } else {
                throw new RuntimeException("Unknown command line argument: " + argv[i]);
            }
        }

        final boolean isPrimaryZygote = zygoteSocketName.equals(Zygote.PRIMARY_SOCKET_NAME);
        if (!isRuntimeRestarted) {
            if (isPrimaryZygote) {
                FrameworkStatsLog.write(FrameworkStatsLog.BOOT_TIME_EVENT_ELAPSED_TIME_REPORTED,
                        BOOT_TIME_EVENT_ELAPSED_TIME__EVENT__ZYGOTE_INIT_START,
                        startTime);
            } else if (zygoteSocketName.equals(Zygote.SECONDARY_SOCKET_NAME)) {
                FrameworkStatsLog.write(FrameworkStatsLog.BOOT_TIME_EVENT_ELAPSED_TIME_REPORTED,
                        BOOT_TIME_EVENT_ELAPSED_TIME__EVENT__SECONDARY_ZYGOTE_INIT_START,
                        startTime);
            }
        }

        if (abiList == null) {
            throw new RuntimeException("No ABI list supplied.");
        }

        // 记录启动时间、预加载
        // In some configurations, we avoid preloading resources and classes eagerly.
        // In such cases, we will preload things prior to our first fork.
        // 根据配置，预加载资源和类。如果未启用延迟预加载，则在第一次fork()之前预加载。
        if (!enableLazyPreload) {
            bootTimingsTraceLog.traceBegin("ZygotePreload");
            EventLog.writeEvent(LOG_BOOT_PROGRESS_PRELOAD_START,
                    SystemClock.uptimeMillis());
            preload(bootTimingsTraceLog);
            EventLog.writeEvent(LOG_BOOT_PROGRESS_PRELOAD_END,
                    SystemClock.uptimeMillis());
            bootTimingsTraceLog.traceEnd(); // ZygotePreload
        }

        // Do an initial gc to clean up after startup
        bootTimingsTraceLog.traceBegin("PostZygoteInitGC");
        gcAndFinalize();
        bootTimingsTraceLog.traceEnd(); // PostZygoteInitGC

        bootTimingsTraceLog.traceEnd(); // ZygoteInit

        // 初始化native状态
        Zygote.initNativeState(isPrimaryZygote);

        // 停止 Zygote 无线程创建标记
        ZygoteHooks.stopZygoteNoThreadCreation();

        // 创建 ZygoteServer 实例。
        zygoteServer = new ZygoteServer(isPrimaryZygote);

        
        // 如果需要启动SystemServer，则调用 forkSystemServer 创建SystemServer的子进程，并在子进程中运行。
        if (startSystemServer) {
            Runnable r = forkSystemServer(abiList, zygoteSocketName, zygoteServer);

            // {@code r == null} in the parent (zygote) process, and {@code r != null} in the
            // child (system_server) process.
            if (r != null) {
                r.run();
                return;
            }
        }

        
        // 接受命令套接字连接
        Log.i(TAG, "Accepting command socket connections");

        // select 循环在 fork 后在子进程中提前返回，并在 zygote 中永远循环
        // The select loop returns early in the child process after a fork and
        // loops forever in the zygote.
        caller = zygoteServer.runSelectLoop(abiList);
    } catch (Throwable ex) {
        Log.e(TAG, "System zygote died with fatal exception", ex);
        throw ex;
    } finally {
        // 异常处理和资源清理 在最后关闭 zygoteServer 的服务器套接字。
        if (zygoteServer != null) {
            zygoteServer.closeServerSocket();
        }
    }

    // We're in the child process and have exited the select loop. Proceed to execute the
    // command.
    // 执行命令 如果 caller 不为 null，则在子进程中执行命令。
    if (caller != null) {
        caller.run();
    }
}

```

> 补充一下注释翻译（这里告诉了修改进程优先级的native层和java层的地方）：
>
> 这是 Zygote 进程的入口点。它创建 Zygote 服务器、加载资源并处理与准备进程以分叉到应用程序相关的其他任务。
>
> 此进程以 -20（最高优先级）的 nice 值启动。所有流入新进程的路径都必须将优先级设置为默认值或在执行任何非系统代码之前终止。native方面发生在 SpecializeCommon 中， 而 Java 语言优先级在 ZygoteInit.handleSystemServerProcess、ZygoteConnection.handleChildProc 和 Zygote.childMain 中更改。

这里主要的职责有：

1. 初始化：标记zygote无线程启动、设置进程组、处理命令行参数；

   > `int setpgid(pid_t pid, pid_t pgid)` 可以将一个进程加入一个现有的进程组，或者创建一个新的进程组且当前调用进程作为进程组组长（`setpgid(0, 0)`）。`pid` 参数只能是 0 （当前进程）、当前进程 id、子进程 id（孙子进程不行）。

2. 记录启动时间，并根据是否为主要 Zygote 进程写入启动时间事件；
3. **预加载**，根据配置在第一次fork前预加载；
4. 初始化native层状态；
5. 停止标记zygote无线程启动；
6. **创建 ZygoteServer，并且启动systemserver；**
7. zygoteServer.runSelectLoop(abiList)，建立systemserver和zygote的socket通信；
8. 关闭zygoteserver的socket；

然后挑一些重要的职责细讲一下：

#### ZygoteInit PreLoad

这里预加载的主要是一些系统类、资源、共享库so、文字、webview等等；

```C++
    static void preload(TimingsTraceLog bootTimingsTraceLog) {
        Log.d(TAG, "begin preload");
        bootTimingsTraceLog.traceBegin("BeginPreload");
        beginPreload();
        bootTimingsTraceLog.traceEnd(); // BeginPreload
        bootTimingsTraceLog.traceBegin("PreloadClasses");
        preloadClasses();
        bootTimingsTraceLog.traceEnd(); // PreloadClasses
        bootTimingsTraceLog.traceBegin("CacheNonBootClasspathClassLoaders");
        cacheNonBootClasspathClassLoaders();
        bootTimingsTraceLog.traceEnd(); // CacheNonBootClasspathClassLoaders
        bootTimingsTraceLog.traceBegin("PreloadResources");
        Resources.preloadResources();
        bootTimingsTraceLog.traceEnd(); // PreloadResources
        Trace.traceBegin(Trace.TRACE_TAG_DALVIK, "PreloadAppProcessHALs");
        nativePreloadAppProcessHALs();
        Trace.traceEnd(Trace.TRACE_TAG_DALVIK);
        Trace.traceBegin(Trace.TRACE_TAG_DALVIK, "PreloadGraphicsDriver");
        maybePreloadGraphicsDriver();
        Trace.traceEnd(Trace.TRACE_TAG_DALVIK);
        preloadSharedLibraries();
        preloadTextResources();
        // Ask the WebViewFactory to do any initialization that must run in the zygote process,
        // for memory sharing purposes.
        WebViewFactory.prepareWebViewInZygote();
        endPreload();
        warmUpJcaProviders();
        Log.d(TAG, "end preload");

        sPreloadComplete = true;
    }
```

而且preload也有个前提条件 enableLazyPreload = true --> 带有--enable-lazy-preload，只有system/core/rootdir/init.zygote64_32.rc才有这个参数 --> 只有在32和64位均需要启动的时候，才需要preload；

> - init.zygote32.rc：zygote 进程对应的执行程序是 app_process (纯 32bit 模式)
> - init.zygote64.rc：zygote 进程对应的执行程序是 app_process64 (纯 64bit 模式)
> - init.zygote32_64.rc：启动两个 zygote 进程 (名为 zygote 和 zygote_secondary)，对应的执行程序分别是 app_process32 (主模式)、app_process64
> - init.zygote64_32.rc：启动两个 zygote 进程 (名为 zygote 和 zygote_secondary)，对应的执行程序分别是 app_process64 (主模式)、app_process32





#### ZygoteInit forkSystemServer

```Java
    /**
     * Prepare the arguments and forks for the system server process.
     *
     * @return A {@code Runnable} that provides an entrypoint into system_server code in the child
     * process; {@code null} in the parent.
     */
    private static Runnable forkSystemServer(String abiList, String socketName,
            ZygoteServer zygoteServer) {
        long capabilities = posixCapabilitiesAsBits(
                OsConstants.CAP_IPC_LOCK,
                OsConstants.CAP_KILL,
                OsConstants.CAP_NET_ADMIN,
                OsConstants.CAP_NET_BIND_SERVICE,
                OsConstants.CAP_NET_BROADCAST,
                OsConstants.CAP_NET_RAW,
                OsConstants.CAP_SYS_MODULE,
                OsConstants.CAP_SYS_NICE,
                OsConstants.CAP_SYS_PTRACE,
                OsConstants.CAP_SYS_TIME,
                OsConstants.CAP_SYS_TTY_CONFIG,
                OsConstants.CAP_WAKE_ALARM,
                OsConstants.CAP_BLOCK_SUSPEND
        );
        /* Containers run without some capabilities, so drop any caps that are not available. */
        StructCapUserHeader header = new StructCapUserHeader(
                OsConstants._LINUX_CAPABILITY_VERSION_3, 0);
        StructCapUserData[] data;
        try {
            data = Os.capget(header);
        } catch (ErrnoException ex) {
            throw new RuntimeException("Failed to capget()", ex);
        }
        capabilities &= Integer.toUnsignedLong(data[0].effective) |
                (Integer.toUnsignedLong(data[1].effective) << 32);

        /* Hardcoded command line to start the system server */
        String[] args = {
                "--setuid=1000",
                "--setgid=1000",
                "--setgroups=1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1018,1021,1023,"
                        + "1024,1032,1065,3001,3002,3003,3005,3006,3007,3009,3010,3011,3012",
                "--capabilities=" + capabilities + "," + capabilities,
                "--nice-name=system_server",
                "--runtime-args",
                "--target-sdk-version=" + VMRuntime.SDK_VERSION_CUR_DEVELOPMENT,
                "com.android.server.SystemServer",
        };
        ZygoteArguments parsedArgs;

        int pid;

        try {
            ZygoteCommandBuffer commandBuffer = new ZygoteCommandBuffer(args);
            try {
                parsedArgs = ZygoteArguments.getInstance(commandBuffer);
            } catch (EOFException e) {
                throw new AssertionError("Unexpected argument error for forking system server", e);
            }
            commandBuffer.close();
            Zygote.applyDebuggerSystemProperty(parsedArgs);
            Zygote.applyInvokeWithSystemProperty(parsedArgs);

            if (Zygote.nativeSupportsMemoryTagging()) {
                String mode = SystemProperties.get("persist.arm64.memtag.system_server", "");
                if (mode.isEmpty()) {
                  /* The system server has ASYNC MTE by default, in order to allow
                   * system services to specify their own MTE level later, as you
                   * can't re-enable MTE once it's disabled. */
                  mode = SystemProperties.get("persist.arm64.memtag.default", "async");
                }
                if (mode.equals("async")) {
                    parsedArgs.mRuntimeFlags |= Zygote.MEMORY_TAG_LEVEL_ASYNC;
                } else if (mode.equals("sync")) {
                    parsedArgs.mRuntimeFlags |= Zygote.MEMORY_TAG_LEVEL_SYNC;
                } else if (!mode.equals("off")) {
                    /* When we have an invalid memory tag level, keep the current level. */
                    parsedArgs.mRuntimeFlags |= Zygote.nativeCurrentTaggingLevel();
                    Slog.e(TAG, "Unknown memory tag level for the system server: \"" + mode + "\"");
                }
            } else if (Zygote.nativeSupportsTaggedPointers()) {
                /* Enable pointer tagging in the system server. Hardware support for this is present
                 * in all ARMv8 CPUs. */
                parsedArgs.mRuntimeFlags |= Zygote.MEMORY_TAG_LEVEL_TBI;
            }

            /* Enable gwp-asan on the system server with a small probability. This is the same
             * policy as applied to native processes and system apps. */
            parsedArgs.mRuntimeFlags |= Zygote.GWP_ASAN_LEVEL_LOTTERY;

            if (shouldProfileSystemServer()) {
                parsedArgs.mRuntimeFlags |= Zygote.PROFILE_SYSTEM_SERVER;
            }

            /* Request to fork the system server process */
            pid = Zygote.forkSystemServer(
                    parsedArgs.mUid, parsedArgs.mGid,
                    parsedArgs.mGids,
                    parsedArgs.mRuntimeFlags,
                    null,
                    parsedArgs.mPermittedCapabilities,
                    parsedArgs.mEffectiveCapabilities);
        } catch (IllegalArgumentException ex) {
            throw new RuntimeException(ex);
        }

        /* For child process */
        if (pid == 0) {
            if (hasSecondZygote(abiList)) {
                waitForSecondaryZygote(socketName);
            }

            zygoteServer.closeServerSocket();
            return handleSystemServerProcess(parsedArgs);
        }

        return null;
    }
```

里面的整体逻辑还是很简单的 ， 就是整理出参数，然后调用zygote的方法；主要调用了applyDebuggerSystemProperty、applyInvokeWithSystemProperty、forkSystemServer方法，

1. applyDebuggerSystemProperty：

   > Applies debugger system properties to the zygote arguments.
   > For eng builds all apps are debuggable with JDWP and ptrace.
   > On userdebug builds if persist.debug.dalvik.vm.jdwp.enabled is 1 all apps are debuggable with JDWP and ptrace. Otherwise, the debugger state is specified via the "--enable-jdwp" flag in the
   > spawn request.
   > On userdebug builds if persist.debug.ptrace.enabled is 1 all apps are debuggable with ptrace.
   >
   > 将调试器系统属性应用于 zygote 参数。
   > 对于 eng 版本，所有应用均可使用 JDWP 和 ptrace 进行调试。
   > 在 userdebug 版本中，如果 persist.debug.dalvik.vm.jdwp.enabled 为 1，则所有应用均可使用 JDWP 和 ptrace 进行调试。否则，调试器状态通过 spawn 请求中的“--enable-jdwp”标志指定。
   > 在 userdebug 版本中，如果 persist.debug.ptrace.enabled 为 1，则所有应用均可使用 ptrace 进行调试。

2. applyInvokeWithSystemProperty：将invoke-with系统属性应用于zygote参数

3. forkSystemServer 最终会调用到native层，fork出子进程；

4. closeServerSocket 关闭socket通信；

5. handleSystemServerProcess：完成新建子进程后剩余工作；



## Q&A

### 为什么zygote要用socket，而不是用binder？

[Zygote通信为什么用Socket，而不是Binder? - 简书 (jianshu.com)](https://www.jianshu.com/p/cfc0adc55911)



## 参考

1. [platform/superproject/main - Android Code Search](https://cs.android.com/android/platform/superproject/main/+/main:)
2. [Android系统启动(二)- Zygote篇 - 掘金 (juejin.cn)](https://juejin.cn/post/7082272398610792461#heading-10)
3. [Android O系统启动流程--zygote篇 - Vane的博客 | Vane's Blog (vanelst.site)](https://vanelst.site/2019/11/07/android-startup-zygote/)


# 【Android系统启动】 Android SystemServer 进程启动流程源码解析

![0b98e065f489f8d683c5a98f63294ca](./【Android系统启动】 Android SystemServer 进程启动流程源码解析.assets/0b98e065f489f8d683c5a98f63294ca.jpg)



## 前言

1. 文章源码按照AOSP官网源码[platform/superproject/main - Android Code Search](https://cs.android.com/android/platform/superproject/main)代码进行解读；
2. 如有不当之处，麻烦指出作者进行修正



## 代码位置

> 1. frameworks/base/services/java/com/android/server/SystemServer.java



## 源码解析

### SystemServer启动

从zygote启动篇讲到，启动zygote的时候会将systemserver通过fork形式，创建systemserver进程。如何找到systemserver的入口呢？我们从`ZygoteInit.java`中看到， 传递给zygote的参数中， 含有systemserver的包名"com.android.server.SystemServer"，通过搜索此包名得知systemserver位置。

```java
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
```



### 

> frameworks/base/services/java/com/android/server/SystemServer.java

```java
    /**
     * The main entry point from zygote.
     */
    public static void main(String[] args) {
        new SystemServer().run();
    }

    public SystemServer() {
        // Check for factory test mode.
        // 获取工厂测试模式， 有三种模式， 通过获取ro.factorytest系统属性确定。用于工厂测试。
        mFactoryTestMode = FactoryTest.getMode();

        // Record process start information.
        mStartCount = SystemProperties.getInt(SYSPROP_START_COUNT, 0) + 1;
        mRuntimeStartElapsedTime = SystemClock.elapsedRealtime();
        mRuntimeStartUptime = SystemClock.uptimeMillis();
        Process.setStartTimes(mRuntimeStartElapsedTime, mRuntimeStartUptime,
                mRuntimeStartElapsedTime, mRuntimeStartUptime);

        // Remember if it's runtime restart or reboot.
        mRuntimeRestart = mStartCount > 1;
    }
```

SystemServer的main方法中，只做了构造对象和调用run()方法。

### new SystemServer()

在new的时候：

1. 获取工厂测试模式；
2. 获取sys.system_server.start_count系统属性，当前启动次数+1；
3. 通过SystemClock.elapsedRealtime()和SystemClock.uptimeMillis()计算当前，启动时间。
4. 判断启动次数是否大于1，来确定runtime是否重启；

> elapsedRealtime : Returns milliseconds since boot, including time spent in sleep. 启动后的时间，包含睡眠时间；
>
> uptimeMillis：Returns milliseconds since boot, not counting time spent in deep sleep.启动后的时间，不包含睡眠时间；

### SystemServer.run()

```java
    private void run() {
        TimingsTraceAndSlog t = new TimingsTraceAndSlog();
        try {
            // 开启trace
            t.traceBegin("InitBeforeStartServices");

            // 记录启动次数、启动时间（含睡眠时间）、启动时间（不含睡眠时间）
            // Record the process start information in sys props.
            SystemProperties.set(SYSPROP_START_COUNT, String.valueOf(mStartCount));
            SystemProperties.set(SYSPROP_START_ELAPSED, String.valueOf(mRuntimeStartElapsedTime));
            SystemProperties.set(SYSPROP_START_UPTIME, String.valueOf(mRuntimeStartUptime));

            // 写入到logcat event
            EventLog.writeEvent(EventLogTags.SYSTEM_SERVER_START,
                    mStartCount, mRuntimeStartUptime, mRuntimeStartElapsedTime);

            // 初始化时区
            // Set the device's time zone (a system property) if it is not set or is invalid.
            SystemTimeZone.initializeTimeZoneSettingsIfRequired();

            // 设置地区和语言
            // If the system has "persist.sys.language" and friends set, replace them with
            // "persist.sys.locale". Note that the default locale at this point is calculated
            // using the "-Duser.locale" command line flag. That flag is usually populated by
            // AndroidRuntime using the same set of system properties, but only the system_server
            // and system apps are allowed to set them.
            //
            // NOTE: Most changes made here will need an equivalent change to
            // core/jni/AndroidRuntime.cpp
            if (!SystemProperties.get("persist.sys.language").isEmpty()) {
                final String languageTag = Locale.getDefault().toLanguageTag();

                SystemProperties.set("persist.sys.locale", languageTag);
                SystemProperties.set("persist.sys.language", "");
                SystemProperties.set("persist.sys.country", "");
                SystemProperties.set("persist.sys.localevar", "");
            }

            // 设置binder位非oneway模式，调用方会阻塞
            // The system server should never make non-oneway calls
            Binder.setWarnOnBlocking(true);
            
            // 使用安全标签
            // The system server should always load safe labels
            PackageItemInfo.forceSafeLabels();

            // SQLite默认模式
            // Default to FULL within the system server.
            SQLiteGlobal.sDefaultSyncMode = SQLiteGlobal.SYNC_MODE_FULL;

            // 禁用SQLite能力直到settings provider已经初始化
            // Deactivate SQLiteCompatibilityWalFlags until settings provider is initialized
            SQLiteCompatibilityWalFlags.init(null);

            // Here we go!
            // 进入android 系统
            Slog.i(TAG, "Entered the Android system server!");
            // 记录时间，如果runtime restart， 记录framework日志
            final long uptimeMillis = SystemClock.elapsedRealtime();
            EventLog.writeEvent(EventLogTags.BOOT_PROGRESS_SYSTEM_RUN, uptimeMillis);
            if (!mRuntimeRestart) {
                FrameworkStatsLog.write(FrameworkStatsLog.BOOT_TIME_EVENT_ELAPSED_TIME_REPORTED,
                        FrameworkStatsLog
                                .BOOT_TIME_EVENT_ELAPSED_TIME__EVENT__SYSTEM_SERVER_INIT_START,
                        uptimeMillis);
            }

            // 设置runtime库版本
            // In case the runtime switched since last boot (such as when
            // the old runtime was removed in an OTA), set the system
            // property so that it is in sync. We can't do this in
            // libnativehelper's JniInvocation::Init code where we already
            // had to fallback to a different runtime because it is
            // running as root and we need to be the system user to set
            // the property. http://b/11463182
            SystemProperties.set("persist.sys.dalvik.vm.lib.2", VMRuntime.getRuntime().vmLibrary());

            // 消除任何增长限制，允许应用程序分配最大堆大小 ---> 能够拿到更多内存
            // Mmmmmm... more memory!
            VMRuntime.getRuntime().clearGrowthLimit();

            // 一些机器依赖runtime指纹生成，确保在启动前定义
            // Some devices rely on runtime fingerprint generation, so make sure
            // we've defined it before booting further.
            Build.ensureFingerprintProperty();

            // 强制指定用户访问环境路径
            // Within the system server, it is an error to access Environment paths without
            // explicitly specifying a user.
            Environment.setUserRequired(true);

            // 解包传入的Bundles时避免BadParcelableException
            // Within the system server, any incoming Bundles should be defused
            // to avoid throwing BadParcelableException.
            BaseBundle.setShouldDefuse(true);

			// 序列化例外时包含堆栈跟踪
            // Within the system server, when parceling exceptions, include the stack trace
            Parcel.setStackTraceParceling(true);
			
            // 确保系统中的binder调用始终以前台优先级运行
            // Ensure binder calls into the system always run at foreground priority.
            BinderInternal.disableBackgroundScheduling(true);

            // 增加system_server中的binder线程数量，这里sMaxBinderThreads是31
            // Increase the number of binder threads in system_server
            BinderInternal.setMaxThreads(sMaxBinderThreads);

            // 这里设置了进程优先级，为前台优先级
            // Prepare the main looper thread (this thread).
            android.os.Process.setThreadPriority(
                    android.os.Process.THREAD_PRIORITY_FOREGROUND);
            android.os.Process.setCanSelfBackground(false);
            
            // 开启systemserver主线程looper
            Looper.prepareMainLooper();
            Looper.getMainLooper().setSlowLogThresholdMs(
                    SLOW_DISPATCH_THRESHOLD_MS, SLOW_DELIVERY_THRESHOLD_MS);

            SystemServiceRegistry.sEnableServiceNotFoundWtf = true;

            // 初始化native层服务
            // Initialize native services.
            System.loadLibrary("android_servers");

            // 允许堆 / 性能分析
            // Allow heap / perf profiling.
            initZygoteChildHeapProfiling();

            // Debug构建 - 生成一个线程来监视fd泄漏
            // Debug builds - spawn a thread to monitor for fd leaks.
            if (Build.IS_DEBUGGABLE) {
                spawnFdLeakCheckThread();
            }

            // 检查上次是否未能关机
            // Check whether we failed to shut down last time we tried.
            // This call may not return.
            performPendingShutdown();

            // 创建系统上下文
            // Initialize the system context.
            createSystemContext();

            // 初始化模块
            // Call per-process mainline module initialization.
            ActivityThread.initializeMainlineModules();

            // 设置转储服务
            // Sets the dumper service
            ServiceManager.addService("system_server_dumper", mDumper);
            mDumper.addDumpable(this);

            // 创建系统服务管理器
            // Create the system service manager.
            mSystemServiceManager = new SystemServiceManager(mSystemContext);
            mSystemServiceManager.setStartInfo(mRuntimeRestart,
                    mRuntimeStartElapsedTime, mRuntimeStartUptime);
            mDumper.addDumpable(mSystemServiceManager);

            // 准备并行初始化任务的线程池
            LocalServices.addService(SystemServiceManager.class, mSystemServiceManager);
            // Prepare the thread pool for init tasks that can be parallelized
            SystemServerInitThreadPool tp = SystemServerInitThreadPool.start();
            mDumper.addDumpable(tp);

            // 加载预安装的系统字体
            // Lazily load the pre-installed system font map in SystemServer only if we're not doing
            // the optimized font loading in the FontManagerService.
            if (!com.android.text.flags.Flags.useOptimizedBoottimeFontLoading()
                    && Typeface.ENABLE_LAZY_TYPEFACE_INITIALIZATION) {
                Slog.i(TAG, "Loading pre-installed system font map.");
                Typeface.loadPreinstalledSystemFontMap();
            }

            // 调试版本中附加JVMTI代理
            // Attach JVMTI agent if this is a debuggable build and the system property is set.
            if (Build.IS_DEBUGGABLE) {
                // Property is of the form "library_path=parameters".
                String jvmtiAgent = SystemProperties.get("persist.sys.dalvik.jvmtiagent");
                if (!jvmtiAgent.isEmpty()) {
                    int equalIndex = jvmtiAgent.indexOf('=');
                    String libraryPath = jvmtiAgent.substring(0, equalIndex);
                    String parameterList =
                            jvmtiAgent.substring(equalIndex + 1, jvmtiAgent.length());
                    // Attach the agent.
                    try {
                        Debug.attachJvmtiAgent(libraryPath, parameterList, null);
                    } catch (Exception e) {
                        Slog.e("System", "*************************************************");
                        Slog.e("System", "********** Failed to load jvmti plugin: " + jvmtiAgent);
                    }
                }
            }
        } finally {
            // 结束trace
            t.traceEnd();  // InitBeforeStartServices
        }

        // 设置默认的WTF处理程序
        // Setup the default WTF handler
        RuntimeInit.setDefaultApplicationWtfHandler(SystemServer::handleEarlySystemWtf);

        // 启动服务
        // Start services.
        try {
            t.traceBegin("StartServices");
            // 启动启动相关的核心服务， 如看门狗、AMS等
            startBootstrapServices(t);
            // 启动核心服务，如电池、系统配置等
            startCoreServices(t);
            // 启动其他服务， 
            startOtherServices(t);
            // 启动apex服务
            startApexServices(t);
            // 仅在启动所有服务后更新超时，以便我们使用默认超时来启动系统服务器。
            // Only update the timeout after starting all the services so that we use
            // the default timeout to start system server.
            updateWatchdogTimeout(t);
            CriticalEventLog.getInstance().logSystemServerStarted();
        } catch (Throwable ex) {
            Slog.e("System", "******************************************");
            Slog.e("System", "************ Failure starting system services", ex);
            throw ex;
        } finally {
            t.traceEnd(); // StartServices
        }

        // 严格模式初始化
        StrictMode.initVmDefaults(null);

        // 记录系统服务器已准备好
        if (!mRuntimeRestart && !isFirstBootOrUpgrade()) {
            final long uptimeMillis = SystemClock.elapsedRealtime();
            FrameworkStatsLog.write(FrameworkStatsLog.BOOT_TIME_EVENT_ELAPSED_TIME_REPORTED,
                    FrameworkStatsLog.BOOT_TIME_EVENT_ELAPSED_TIME__EVENT__SYSTEM_SERVER_READY,
                    uptimeMillis);
            final long maxUptimeMillis = 60 * 1000;
            if (uptimeMillis > maxUptimeMillis) {
                Slog.wtf(SYSTEM_SERVER_TIMING_TAG,
                        "SystemServer init took too long. uptimeMillis=" + uptimeMillis);
            }
        }

        // 设置binder事务回调
        // Set binder transaction callback after starting system services
        Binder.setTransactionCallback(new IBinderCallback() {
            @Override
            public void onTransactionError(int pid, int code, int flags, int err) {
                mActivityManagerService.frozenBinderTransactionDetected(pid, code, flags, err);
            }
        });

        // 进入循环
        // Loop forever.
        Looper.loop();
        
        // 如果loop走到了这里， 会抛出运行时异常
        throw new RuntimeException("Main thread loop unexpectedly exited");
    }
```



我把上面的代码分为这几部分：

1. 初始化：Trace、设置开机时间、开机次数等系统属性、写入logcat event；
2. 设置：
   1. 初始化时区、语言、国家等；
   2. Binder设置，设置Binder的一些参数，如非oneway调用警告、后台调度禁用以及最大线程数；
   3. SQLite 设置，设置SQLite的默认同步模式和WalFlags初始化；
   4. 虚拟机设置：设置虚拟机库版本；
   5. 内存管理：清除内存增长限制，允许应用程序分配更多内存；
   6. 其他设置：确保设备指纹属性、设置用户访问环境路径、设置Bundle解析选项、设置序列化异常时包含堆栈信息等；
   7. 进程优先级设置：设置为前台优先级；
3. 加载各种服务，并启动各种检查：
   1. **looper准备；**
   2. 加载native库"android_servers"；
   3. 初始化堆分析和文件描述符检查、检查未完成的关机；
   4. 创建系统上下文和ServiceManager；
   5. 加载预安装系统字体；
   6. JVMTI 代理：如果是调试版本并且设置了相应系统属性，附加 JVMTI 代理；
   7. **启动服务：先后启动各类Java层核心服务；**
   8. 严格模式初始化；
   9. 设置 Binder 事务回调；
   10. **进入主线程循环，Looper.loop()；**
4. 异常处理，如果主线程循环意外退出，抛出运行时异常"Main thread loop unexpectedly exited"。



#### 核心服务启动

```java
// Start services.
        try {
            t.traceBegin("StartServices");
            startBootstrapServices(t);
            startCoreServices(t);
            startOtherServices(t);
            startApexServices(t);
            // Only update the timeout after starting all the services so that we use
            // the default timeout to start system server.
            updateWatchdogTimeout(t);
            CriticalEventLog.getInstance().logSystemServerStarted();
        } catch (Throwable ex) {
            Slog.e("System", "******************************************");
            Slog.e("System", "************ Failure starting system services", ex);
            throw ex;
        } finally {
            t.traceEnd(); // StartServices
        }
```

这里可以看出先后顺序为BootstrapServices - CoreServices - OtherServices - ApexServices；



##### startBootstrapServices

```java
  /**
     * Starts the small tangle of critical services that are needed to get the system off the
     * ground.  These services have complex mutual dependencies which is why we initialize them all
     * in one place here.  Unless your service is also entwined in these dependencies, it should be
     * initialized in one of the other functions.
     */
	// 启动系统启动所需的关键服务。这些服务具有复杂的相互依赖关系，因此我们在这里将它们全部初始化。除非您的服务也与这些依赖关系有关，否则应在其他函数之一中初始化它。
    private void startBootstrapServices(@NonNull TimingsTraceAndSlog t) {
        t.traceBegin("startBootstrapServices");

        t.traceBegin("ArtModuleServiceInitializer");
        // This needs to happen before DexUseManagerLocal init. We do it here to avoid colliding
        // with a GC. ArtModuleServiceInitializer is a class from a separate dex file
        // "service-art.jar", so referencing it involves the class linker. The class linker and the
        // GC are mutually exclusive (b/263486535). Therefore, we do this here to force trigger the
        // class linker earlier. If we did this later, especially after PackageManagerService init,
        // the class linker would be consistently blocked by a GC because PackageManagerService
        // allocates a lot of memory and almost certainly triggers a GC.
        // 设置 {@link ArtModuleServiceManager} 的实例，允许 ART 主线模块获取 ART 绑定服务。平台在系统服务器初始化期间调用此方法。
        ArtModuleServiceInitializer.setArtModuleServiceManager(new ArtModuleServiceManager());
        t.traceEnd();

        // 尽早启动 Watchdog，以防在早期启动过程中死锁导致系统服务崩溃。
        // Start the watchdog as early as possible so we can crash the system server
        // if we deadlock during early boot
        t.traceBegin("StartWatchdog");
        final Watchdog watchdog = Watchdog.getInstance();
        watchdog.start();
        mDumper.addDumpable(watchdog);
        t.traceEnd();

        // 读取系统配置
        Slog.i(TAG, "Reading configuration...");
        final String TAG_SYSTEM_CONFIG = "ReadingSystemConfig";
        t.traceBegin(TAG_SYSTEM_CONFIG);
        SystemServerInitThreadPool.submit(SystemConfig::getInstance, TAG_SYSTEM_CONFIG);
        t.traceEnd();

      	// 平台兼容服务，被 ActivityManagerService、PackageManagerService 使用，以及未来可能的其他服务。
        // Platform compat service is used by ActivityManagerService, PackageManagerService, and
        // possibly others in the future. b/135010838.
        t.traceBegin("PlatformCompat");
        PlatformCompat platformCompat = new PlatformCompat(mSystemContext);
        ServiceManager.addService(Context.PLATFORM_COMPAT_SERVICE, platformCompat);
        ServiceManager.addService(Context.PLATFORM_COMPAT_NATIVE_SERVICE,
                new PlatformCompatNative(platformCompat));
        AppCompatCallbacks.install(new long[0]);
        t.traceEnd();

        // FileIntegrityService 响应应用程序和系统的请求，需要在源（例如密钥库）准备好之后运行。
        // FileIntegrityService responds to requests from apps and the system. It needs to run after
        // the source (i.e. keystore) is ready, and before the apps (or the first customer in the
        // system) run.
        t.traceBegin("StartFileIntegrityService");
        mSystemServiceManager.startService(FileIntegrityService.class);
        t.traceEnd();
        
 	    // 等待 Installd 启动完成，确保它有机会创建必要的目录。
        // Wait for installd to finish starting up so that it has a chance to
        // create critical directories such as /data/user with the appropriate
        // permissions.  We need this to complete before we initialize other services.
        t.traceBegin("StartInstaller");
        Installer installer = mSystemServiceManager.startService(Installer.class);
        t.traceEnd();

        // 在启动应用程序管理器之前注册设备标识符策略。
        // In some cases after launching an app we need to access device identifiers,
        // therefore register the device identifier policy before the activity manager.
        t.traceBegin("DeviceIdentifiersPolicyService");
        mSystemServiceManager.startService(DeviceIdentifiersPolicyService.class);
        t.traceEnd();

    	// 启动 FeatureFlagsService，用于管理运行时标志的读取和应用。
        // Starts a service for reading runtime flag overrides, and keeping processes
        // in sync with one another.
        t.traceBegin("StartFeatureFlagsService");
        mSystemServiceManager.startService(FeatureFlagsService.class);
        t.traceEnd();

        // UriGrantsManagerService 管理 URI 授权。
        // Uri Grants Manager.
        t.traceBegin("UriGrantsManagerService");
        mSystemServiceManager.startService(UriGrantsManagerService.Lifecycle.class);
        t.traceEnd();

    	// PowerStatsService 跟踪电源统计数据。
        t.traceBegin("StartPowerStatsService");
        // Tracks rail data to be used for power statistics.
        mSystemServiceManager.startService(PowerStatsService.class);
        t.traceEnd();

        // IStatsService 提供系统性能统计信息。
        t.traceBegin("StartIStatsService");
        startIStatsService();
        t.traceEnd();

        // MemtrackProxyService 在 ActivityManagerService 之前启动，以便早期调用 Memtrack::getMemory() 不会失败。
        // Start MemtrackProxyService before ActivityManager, so that early calls
        // to Memtrack::getMemory() don't fail.
        t.traceBegin("MemtrackProxyService");
        startMemtrackProxyService();
        t.traceEnd();

        // AccessCheckingService 提供新的权限和应用操作实现。
        // Start AccessCheckingService which provides new implementation for permission and app op.
        t.traceBegin("StartAccessCheckingService");
        LocalServices.addService(PermissionMigrationHelper.class,
                new PermissionMigrationHelperImpl());
        LocalServices.addService(AppOpMigrationHelper.class,
                new AppOpMigrationHelperImpl());
        mSystemServiceManager.startService(AccessCheckingService.class);
        t.traceEnd();

        // ActivityManagerService 是系统的核心服务。
        // Activity manager runs the show.
        t.traceBegin("StartActivityManager");
        // TODO: Might need to move after migration to WM.
        ActivityTaskManagerService atm = mSystemServiceManager.startService(
                ActivityTaskManagerService.Lifecycle.class).getService();
        mActivityManagerService = ActivityManagerService.Lifecycle.startService(
                mSystemServiceManager, atm);
        mActivityManagerService.setSystemServiceManager(mSystemServiceManager);
        mActivityManagerService.setInstaller(installer);
        mWindowManagerGlobalLock = atm.getGlobalLock();
        t.traceEnd();

       // DataLoaderManagerService 管理数据加载器服务。
       // Data loader manager service needs to be started before package manager
        t.traceBegin("StartDataLoaderManagerService");
        mDataLoaderManagerService = mSystemServiceManager.startService(
                DataLoaderManagerService.class);
        t.traceEnd();
        
    	// IncrementalService 处理增量安装相关服务。
        // Incremental service needs to be started before package manager
        t.traceBegin("StartIncrementalService");
        mIncrementalServiceHandle = startIncrementalService();
        t.traceEnd();

    	// PowerManagerService 用于管理设备电源相关功能。
        // Power manager needs to be started early because other services need it.
        // Native daemons may be watching for it to be registered so it must be ready
        // to handle incoming binder calls immediately (including being able to verify
        // the permissions for those calls).
        t.traceBegin("StartPowerManager");
        mPowerManagerService = mSystemServiceManager.startService(PowerManagerService.class);
        t.traceEnd();

        // ThermalManagerService 管理设备的热管理。
        t.traceBegin("StartThermalManager");
        mSystemServiceManager.startService(ThermalManagerService.class);
        t.traceEnd();

        // HintManagerService 提供提示管理服务。
        t.traceBegin("StartHintManager");
        mSystemServiceManager.startService(HintManagerService.class);
        t.traceEnd();

        // 初始化电源管理特性。
        // Now that the power manager has been started, let the activity manager
        // initialize power management features.
        t.traceBegin("InitPowerManagement");
        mActivityManagerService.initPowerManagement();
        t.traceEnd();

        // 启动恢复系统服务，以备需要时重启系统。
        // Bring up recovery system in case a rescue party needs a reboot
        t.traceBegin("StartRecoverySystemService");
        mSystemServiceManager.startService(RecoverySystemService.Lifecycle.class);
        t.traceEnd();

        // Now that we have the bare essentials of the OS up and running, take
        // note that we just booted, which might send out a rescue party if
        // we're stuck in a runtime restart loop.
        RescueParty.registerHealthObserver(mSystemContext);
        PackageWatchdog.getInstance(mSystemContext).noteBoot();
        
        // LightsService 管理 LED 和显示背光。
        // Manages LEDs and display backlight so we need it to bring up the display.
        t.traceBegin("StartLightsService");
        mSystemServiceManager.startService(LightsService.class);
        t.traceEnd();

        // DisplayOffloadService 在显示管理器服务启动后立即启动，以便尽早处理显示。
        t.traceBegin("StartDisplayOffloadService");
        // Package manager isn't started yet; need to use SysProp not hardware feature
        if (SystemProperties.getBoolean("config.enable_display_offload", false)) {
            mSystemServiceManager.startService(WEAR_DISPLAYOFFLOAD_SERVICE_CLASS);
        }
        t.traceEnd();

        // DisplayManagerService 需要在 Package Manager 之前启动，用于提供显示度量信息。
        // Display manager is needed to provide display metrics before package manager
        // starts up.
        t.traceBegin("StartDisplayManager");
        mDisplayManagerService = mSystemServiceManager.startService(DisplayManagerService.class);
        t.traceEnd();

        // 等待获取默认显示之后，再继续执行。
        // We need the default display before we can initialize the package manager.
        t.traceBegin("WaitForDisplay");
        mSystemServiceManager.startBootPhase(t, SystemService.PHASE_WAIT_FOR_DEFAULT_DISPLAY);
        t.traceEnd();

        // 启动 Package Manager。
        // Start the package manager.
        if (!mRuntimeRestart) {
            FrameworkStatsLog.write(FrameworkStatsLog.BOOT_TIME_EVENT_ELAPSED_TIME_REPORTED,
                    FrameworkStatsLog
                            .BOOT_TIME_EVENT_ELAPSED_TIME__EVENT__PACKAGE_MANAGER_INIT_START,
                    SystemClock.elapsedRealtime());
        }

        t.traceBegin("StartDomainVerificationService");
        DomainVerificationService domainVerificationService = new DomainVerificationService(
                mSystemContext, SystemConfig.getInstance(), platformCompat);
        mSystemServiceManager.startService(domainVerificationService);
        t.traceEnd();

        t.traceBegin("StartPackageManagerService");
        try {
            Watchdog.getInstance().pauseWatchingCurrentThread("packagemanagermain");
            mPackageManagerService = PackageManagerService.main(
                    mSystemContext, installer, domainVerificationService,
                    mFactoryTestMode != FactoryTest.FACTORY_TEST_OFF);
        } finally {
            Watchdog.getInstance().resumeWatchingCurrentThread("packagemanagermain");
        }

        mFirstBoot = mPackageManagerService.isFirstBoot();
        mPackageManager = mSystemContext.getPackageManager();
        t.traceEnd();

    	// DexUseManagerLocal 需要在 PackageManagerService 处理 binder 调用前注册。
        t.traceBegin("DexUseManagerLocal");
        // DexUseManagerLocal needs to be loaded after PackageManagerLocal has been registered, but
        // before PackageManagerService starts processing binder calls to notifyDexLoad.
        LocalManagerRegistry.addManager(
                DexUseManagerLocal.class, DexUseManagerLocal.createInstance(mSystemContext));
        t.traceEnd();

        if (!mRuntimeRestart && !isFirstBootOrUpgrade()) {
            FrameworkStatsLog.write(FrameworkStatsLog.BOOT_TIME_EVENT_ELAPSED_TIME_REPORTED,
                    FrameworkStatsLog
                            .BOOT_TIME_EVENT_ELAPSED_TIME__EVENT__PACKAGE_MANAGER_INIT_READY,
                    SystemClock.elapsedRealtime());
        }

        // OtaDexOptService 管理 A/B OTA 的 dexopt 过程。
        // Manages A/B OTA dexopting. This is a bootstrap service as we need it to rename
        // A/B artifacts after boot, before anything else might touch/need them.
        boolean disableOtaDexopt = SystemProperties.getBoolean("config.disable_otadexopt", false);
        if (!disableOtaDexopt) {
            t.traceBegin("StartOtaDexOptService");
            try {
                Watchdog.getInstance().pauseWatchingCurrentThread("moveab");
                OtaDexoptService.main(mSystemContext, mPackageManagerService);
            } catch (Throwable e) {
                reportWtf("starting OtaDexOptService", e);
            } finally {
                Watchdog.getInstance().resumeWatchingCurrentThread("moveab");
                t.traceEnd();
            }
        }

     	// 如果是 Android Runtime for Chrome OS，启动相关健康服务。
        if (Build.IS_ARC) {
            t.traceBegin("StartArcSystemHealthService");
            mSystemServiceManager.startService(ARC_SYSTEM_HEALTH_SERVICE);
            t.traceEnd();
        }

        // 启动 UserManagerService 管理用户信息。
        t.traceBegin("StartUserManagerService");
        mSystemServiceManager.startService(UserManagerService.LifeCycle.class);
        t.traceEnd();

        // 初始化用于缓存来自包的资源的属性缓存。
        // Initialize attribute cache used to cache resources from packages.
        t.traceBegin("InitAttributerCache");
        AttributeCache.init(mSystemContext);
        t.traceEnd();

        // 设置系统进程的 Application 实例。
        // Set up the Application instance for the system process and get started.
        t.traceBegin("SetSystemProcess");
        mActivityManagerService.setSystemProcess();
        t.traceEnd();

        // 平台兼容性服务注册包接收器。
        // The package receiver depends on the activity service in order to get registered.
        platformCompat.registerPackageReceiver(mSystemContext);

        // 初始化 Watchdog 以及监听重启。
        // Complete the watchdog setup with an ActivityManager instance and listen for reboots
        // Do this only after the ActivityManagerService is properly started as a system process
        t.traceBegin("InitWatchdog");
        watchdog.init(mSystemContext, mActivityManagerService);
        t.traceEnd();

        // DisplayManagerService 需要设置 Android 显示调度相关策略。
        // DisplayManagerService needs to setup android.display scheduling related policies
        // since setSystemProcess() would have overridden policies due to setProcessGroup
        mDisplayManagerService.setupSchedulerPolicies();

        // 管理 Overlay 包。
        // Manages Overlay packages
        t.traceBegin("StartOverlayManagerService");
        mSystemServiceManager.startService(new OverlayManagerService(mSystemContext));
        t.traceEnd();

        // 管理资源包。
        // Manages Resources packages
        t.traceBegin("StartResourcesManagerService");
        ResourcesManagerService resourcesService = new ResourcesManagerService(mSystemContext);
        resourcesService.setActivityManagerService(mActivityManagerService);
        mSystemServiceManager.startService(resourcesService);
        t.traceEnd();

        // SensorPrivacyService 管理传感器隐私。
        t.traceBegin("StartSensorPrivacyService");
        mSystemServiceManager.startService(new SensorPrivacyService(mSystemContext));
        t.traceEnd();

        // 如果配置了 displayinset.top，则立即更新系统 UI 上下文。
        if (SystemProperties.getInt("persist.sys.displayinset.top", 0) > 0) {
            // DisplayManager needs the overlay immediately.
            mActivityManagerService.updateSystemUiContext();
            LocalServices.getService(DisplayManagerInternal.class).onOverlayChanged();
        }

        // SensorService 需要访问 PackageManagerService、AppOpsService 和 PermissionsService。

        // The sensor service needs access to package manager service, app ops
        // service, and permissions service, therefore we start it after them.
        t.traceBegin("StartSensorService");
        mSystemServiceManager.startService(SensorService.class);
        t.traceEnd();
        t.traceEnd(); // startBootstrapServices
    }
```

这段代码按照系统服务的依赖关系和启动顺序，列出了如下服务的启动顺序和功能：

1. **ArtModuleServiceInitializer**：初始化 ART 模块服务管理器。
2. **Watchdog**：系统守护进程，确保系统服务不会死锁。
3. **SystemConfig**：读取系统配置。
4. **PlatformCompat**：平台兼容性服务，为其他服务提供兼容性支持。
5. **FileIntegrityService**：文件完整性服务，响应应用和系统的完整性请求。
6. **Installer**：安装器服务，等待 Installd 启动完成。
7. **DeviceIdentifiersPolicyService**：设备标识符策略服务，注册在启动应用程序管理器之前。
8. **FeatureFlagsService**：特性标志服务，管理运行时标志的读取和应用。
9. **UriGrantsManagerService**：URI 授权管理服务。
10. **PowerStatsService**：电源统计数据跟踪服务。
11. **IStatsService**：系统性能统计信息服务。
12. **MemtrackProxyService**：内存跟踪代理服务，早于 ActivityManagerService 启动。
13. **AccessCheckingService**：访问检查服务，提供新的权限和应用操作实现。
14. **ActivityManagerService**：系统核心服务，管理活动和任务。
15. **DataLoaderManagerService**：数据加载器管理服务。
16. **IncrementalService**：增量安装服务。
17. **PowerManagerService**：电源管理服务，其他服务的基础。
18. **ThermalManagerService**：热管理服务。
19. **HintManagerService**：提示管理服务。
20. **LightsService**：LED 和显示背光管理服务。
21. **DisplayOffloadService**：显示卸载服务。
22. **DisplayManagerService**：显示管理器服务。
23. **DomainVerificationService**：域验证服务。
24. **PackageManagerService**：包管理器服务，管理应用程序包和应用程序。
25. **DexUseManagerLocal**：本地 Dex 使用管理器。
26. **OtaDexOptService**：A/B OTA dexopt 管理服务。
27. **ArcSystemHealthService**：适用于 Chrome OS 的 Android 运行时健康服务。
28. **UserManagerService**：用户管理服务。
29. **ResourcesManagerService**：资源管理器服务。
30. **SensorPrivacyService**：传感器隐私管理服务。
31. **SensorService**：传感器服务。

具体服务的作用之后学习，我们继续看下其他阶段启动的服务；



##### startCoreServices

```java
 /**
     * Starts some essential services that are not tangled up in the bootstrap process.
     */
    private void startCoreServices(@NonNull TimingsTraceAndSlog t) {
        t.traceBegin("startCoreServices");

        // Service for system config
        t.traceBegin("StartSystemConfigService");
        mSystemServiceManager.startService(SystemConfigService.class);
        t.traceEnd();

        t.traceBegin("StartBatteryService");
        // Tracks the battery level.  Requires LightService.
        mSystemServiceManager.startService(BatteryService.class);
        t.traceEnd();

        // Tracks application usage stats.
        t.traceBegin("StartUsageService");
        mSystemServiceManager.startService(UsageStatsService.class);
        mActivityManagerService.setUsageStatsManager(
                LocalServices.getService(UsageStatsManagerInternal.class));
        t.traceEnd();

        // Tracks whether the updatable WebView is in a ready state and watches for update installs.
        if (mPackageManager.hasSystemFeature(PackageManager.FEATURE_WEBVIEW)) {
            t.traceBegin("StartWebViewUpdateService");
            mWebViewUpdateService = mSystemServiceManager.startService(WebViewUpdateService.class);
            t.traceEnd();
        }

        // Tracks and caches the device state.
        t.traceBegin("StartCachedDeviceStateService");
        mSystemServiceManager.startService(CachedDeviceStateService.class);
        t.traceEnd();

        // Tracks cpu time spent in binder calls
        t.traceBegin("StartBinderCallsStatsService");
        mSystemServiceManager.startService(BinderCallsStatsService.LifeCycle.class);
        t.traceEnd();

        // Tracks time spent in handling messages in handlers.
        t.traceBegin("StartLooperStatsService");
        mSystemServiceManager.startService(LooperStatsService.Lifecycle.class);
        t.traceEnd();

        // Manages apk rollbacks.
        t.traceBegin("StartRollbackManagerService");
        mSystemServiceManager.startService(ROLLBACK_MANAGER_SERVICE_CLASS);
        t.traceEnd();

        // Tracks native tombstones.
        t.traceBegin("StartNativeTombstoneManagerService");
        mSystemServiceManager.startService(NativeTombstoneManagerService.class);
        t.traceEnd();

        // Service to capture bugreports.
        t.traceBegin("StartBugreportManagerService");
        mSystemServiceManager.startService(BugreportManagerService.class);
        t.traceEnd();

        // Service for GPU and GPU driver.
        t.traceBegin("GpuService");
        mSystemServiceManager.startService(GpuService.class);
        t.traceEnd();

        // Handles system process requests for remotely provisioned keys & data.
        t.traceBegin("StartRemoteProvisioningService");
        mSystemServiceManager.startService(RemoteProvisioningService.class);
        t.traceEnd();

        // TODO(b/277600174): Start CpuMonitorService on all builds and not just on debuggable
        // builds once the Android JobScheduler starts using this service.
        if (Build.IS_DEBUGGABLE || Build.IS_ENG) {
          // Service for CPU monitor.
          t.traceBegin("CpuMonitorService");
          mSystemServiceManager.startService(CpuMonitorService.class);
          t.traceEnd();
        }

        t.traceEnd(); // startCoreServices
    }

```

这里先后启动了

1. **SystemConfigService**: 启动系统配置服务，用于管理系统配置信息。
2. **BatteryService**: 启动电池服务，跟踪电池电量。依赖于LightsService。
3. **UsageStatsService**: 启动应用程序使用统计服务，跟踪应用程序的使用情况。
4. **WebViewUpdateService**: 如果系统支持 WebView 功能，启动 WebView 更新服务。
5. **CachedDeviceStateService**: 跟踪并缓存设备状态的服务。
6. **BinderCallsStatsService**: 跟踪在 Binder 调用中花费的 CPU 时间的服务。
7. **LooperStatsService**: 跟踪在处理消息时花费的时间的服务。
8. **RollbackManagerService**: 管理 APK 回滚的服务。
9. **NativeTombstoneManagerService**: 跟踪本地堆栈溢出的服务。
10. **BugreportManagerService**: 管理 bug 报告的服务。
11. **GpuService**: 管理 GPU 和 GPU 驱动相关任务的服务。
12. **RemoteProvisioningService**: 处理远程配置密钥和数据的服务。
13. **CpuMonitorService**: 在调试或工程构建中监控 CPU 使用情况的服务。



##### startOtherServices

这个就不贴代码了，看了下源码有近2k行代码。主要也是负责启动各种服务和应用，通过过滤其中trace，可以看出大概启动了多个service或者manager，部分是根据配置是否启动的。

```java

StartKeyAttestationApplicationIdProviderService
StartKeyChainSystemService
StartBinaryTransparencyService
StartSchedulingPolicyService
StartTelecomLoaderService
StartTelephonyRegistry
StartEntropyMixer
StartAccountManagerService
StartContentService
InstallSystemProviders
StartDropBoxManager
StartEnhancedConfirmationService
StartRoleManagerService
StartVibratorManagerService
StartDynamicSystemService
StartConsumerIrService
StartResourceEconomy
StartAlarmManagerService
StartInputManagerService
DeviceStateManagerService
StartCameraServiceProxy
StartWindowManagerService
SetWindowManagerService
WindowManagerServiceOnInitReady
StartVrManagerService
StartInputManager
DisplayManagerWindowManagerAndInputReady
StartBluetoothService
IpConnectivityMetrics
NetworkWatchlistService
PinnerService
ProfcollectForwardingService
SignedConfigService
AppIntegrityService
StartLogcatManager
StartInputMethodManagerLifecycle
StartAccessibilityManagerService
MakeDisplayReady
StartStorageManagerService
StartStorageStatsService
StartUiModeManager
StartLocaleManagerService
StartGrammarInflectionService
StartAppHibernationService
ArtManagerLocal
UpdatePackagesIfNeeded
PerformFstrimIfNeeded
StartLockSettingsService
StartPersistentDataBlock
StartArcPersistentDataBlock
StartTestHarnessMode
StartOemLockService
StartDeviceIdleController
StartDevicePolicyManager
StartStatusBarManagerService
StartMusicRecognitionManagerService
StartAmbientContextService
StartSpeechRecognitionManagerService
StartAppPredictionService
StartContentSuggestionsService
StartSearchUiService
StartSmartspaceService
InitConnectivityModuleConnector
InitNetworkStackClient
StartNetworkManagementService
StartFontManagerService
StartTextServicesManager
StartTextClassificationManagerService
StartNetworkScoreService
StartNetworkStatsService
StartNetworkPolicyManagerService
StartWifi
StartWifiScanning
StartArcNetworking
StartRttService
StartWifiAware
StartWifiP2P
StartLowpan
StartPacProxyService
StartConnectivityService
StartSecurityStateManagerService
StartVpnManagerService
StartVcnManagementService
StartSystemUpdateManagerService
StartUpdateLockService
StartNotificationManager
StartDeviceMonitor
StartTimeDetectorService
StartLocationManagerService
StartCountryDetectorService
StartTimeZoneDetectorService
StartAltitudeService
StartLocationTimeZoneManagerService
StartGnssTimeUpdateService
StartSearchManagerService
StartWallpaperManagerService
StartWallpaperEffectsGenerationService
StartAudioService
StartSoundTriggerMiddlewareService
StartBroadcastRadioService
StartDockObserver
StartThermalObserver
StartWiredAccessoryManager
StartMidiManager
StartAdbService
StartUsbService
StartSerialService
StartHardwarePropertiesManagerService
StartTwilightService
StartColorDisplay
StartJobScheduler
StartSoundTrigger
StartTrustManager
StartBackupManager
StartAppWidgetService
StartVoiceRecognitionManager
StartGestureLauncher
StartSensorNotification
StartContextHubSystemService
StartDiskStatsService
RuntimeService
StartNetworkTimeUpdateService
CertBlocklister
StartEmergencyAffordanceService
TART_BLOB_STORE_SERVICE);
StartDreamManager
AddGraphicsStatsService
AddCoverageService
StartPrintManager
StartAttestationVerificationService
StartCompanionDeviceManager
StartVirtualDeviceManager
StartRestrictionManager
StartMediaSessionService
StartHdmiControlService
StartTvInteractiveAppManager
StartTvInputManager
StartTunerResourceManager
StartMediaResourceMonitor
StartTvRemoteService
StartMediaRouterService
StartFaceSensor
StartIrisSensor
StartFingerprintSensor
StartBiometricService
StartAuthService
StartAdaptiveAuthService
StartDynamicCodeLoggingService
StartPruneInstantAppsJobService
StartSelinuxAuditLogsService
StartShortcutServiceLifecycle
StartLauncherAppsService
StartCrossProfileAppsService
StartPeopleService
StartMediaMetricsManager
StartBackgroundInstallControlService
StartMediaProjectionManager
StartWearPowerService
StartHealthService
StartSystemStateDisplayService
StartWearConnectivityService
StartWearDisplayService
StartWearDebugService
StartWearTimeService
StartWearSettingsService
StartWearModeService
StartWristOrientationService
StartSliceManagerService
StartIoTSystemService
StartStatsCompanion
StartRebootReadinessManagerService
StartStatsPullAtomService
StatsBootstrapAtomService
StartIncidentCompanionService
StarSdkSandboxManagerService
StartAdServicesManagerService
StartOnDevicePersonalizationSystemService
StartProfilingCompanion
StartMmsService
StartAutoFillService
StartCredentialManagerService
StartTranslationManagerService
StartClipboardService
AppServiceManager
startTracingServiceProxy
MakeLockSettingsServiceReady
StartBootPhaseLockSettingsReady
HsumBootUserInitializer.init
CommunalProfileInitializer.init
CommunalProfileInitializer.removeCommunalProfileIfPresent
StartBootPhaseSystemServicesReady
MakeWindowManagerServiceReady
RegisterLogMteState
StartPermissionPolicyService
MakePackageManagerServiceReady
MakeDisplayManagerServiceReady
StartDeviceSpecificServices
StartDeviceSpecificServices
GameManagerService
UwbService
StartBootPhaseDeviceSpecificServicesReady
StartSafetyCenterService
AppSearchModule
IsolatedCompilationService
StartMediaCommunicationService
AppCompatOverridesService
HealthConnectManagerService
DeviceLockService
StartSensitiveContentProtectionManager
StartActivityManagerReadyPhase
StartObservingNativeCrashes
RegisterAppOpsPolicy
StartCarServiceHelperService
StartWearService
EnableAirplaneModeInSafeMode
MakeNetworkManagementServiceReady
MakeConnectivityServiceReady
MakeVpnManagerServiceReady
MakeVcnManagementServiceReady
MakeNetworkPolicyServiceReady
PhaseThirdPartyAppsCanStart
HsumBootUserInitializer.systemRunning
StartNetworkStack
StartTethering
MakeCountryDetectionServiceReady
MakeNetworkTimeUpdateReady
MakeInputManagerServiceReady
MakeTelephonyRegistryReady
MakeMediaRouterServiceReady
MakeMmsServiceReady
IncidentDaemonReady
MakeIncrementalServiceReady
OdsignStatsLogger
LockSettingsThirdPartyAppsStarted
StartSystemUI
```

从代码中可以看到，启动到不同阶段的时候，会调用`mSystemServiceManager.startBootPhase`方法进行类似埋点的操作，systemservice会将启动阶段通知到各个服务，各个服务能够根据不同阶段完成自己的一些车初始化工作。其中有下面这些阶段：

```java
PHASE_WAIT_FOR_DEFAULT_DISPLAY 			100 最早的系统引导阶段，等待默认显示器准备完成  
PHASE_WAIT_FOR_SENSOR_SERVICE 			200 阻塞于传感器服务可用性的引导阶段，该服务异步启动，因其初始化可能需要一段时间
PHASE_LOCK_SETTINGS_READY 				480 获得锁定设置数据的引导阶段  
PHASE_SYSTEM_SERVICES_READY 			500 核心系统服务（如PowerManager或PackageManager）就绪的引导阶段  
PHASE_DEVICE_SPECIFIC_SERVICES_READY 	520 设备特定服务就绪的引导阶段  
PHASE_ACTIVITY_MANAGER_READY 			550 可以广播Intent的引导阶段  
PHASE_THIRD_PARTY_APPS_CAN_START 		600 可以启动/绑定第三方应用的引导阶段，此时应用可以向服务发起Binder调用  
PHASE_BOOT_COMPLETED 					1000 引导完成的引导阶段，此时已完成引导并启动了主屏幕应用
// 其中PHASE_WAIT_FOR_DEFAULT_DISPLAY在startBootstrapServices
// PHASE_WAIT_FOR_SENSOR_SERVICE~PHASE_THIRD_PARTY_APPS_CAN_START在startOtherServices
// PHASE_BOOT_COMPLETED在ActivityManagerService.java  final void finishBooting()方法中设置
```



这里同时要留意一下，在`startOtherServices`方法中，调用了各种Service的systemReady方法，**其中AMS的systemReady方法中`mAtmInternal.startHomeOnAllDisplays(currentUserId, "systemReady");`启动了Launcher服务；**

```java
// frameworks/base/services/java/com/android/server/SystemServer.java

		// We now tell the activity manager it is okay to run third party
        // code.  It will call back into us once it has gotten to the state
        // where third party code can really run (but before it has actually
        // started launching the initial applications), for us to complete our
        // initialization.
        mActivityManagerService.systemReady(() -> {
            Slog.i(TAG, "Making services ready");
            //...
            t.traceEnd();
        }, t);
```



```java
// frameworks/base/services/core/java/com/android/server/am/ActivityManagerService.java
	/**
     * Ready. Set. Go!
     */
    public void systemReady(final Runnable goingCallback, @NonNull TimingsTraceAndSlog t) {
        t.traceBegin("PhaseActivityManagerReady");
        mSystemServiceManager.preSystemReady();
        // ...

            boolean isBootingSystemUser = currentUserId == UserHandle.USER_SYSTEM;

            // Some systems - like automotive - will explicitly unlock system user then switch
            // to a secondary user.
            // TODO(b/266158156): this workaround shouldn't be necessary once we move
            // the headless-user start logic to UserManager-land.
            if (isBootingSystemUser && !UserManager.isHeadlessSystemUserMode()) {
                t.traceBegin("startHomeOnAllDisplays");
                mAtmInternal.startHomeOnAllDisplays(currentUserId, "systemReady");
                t.traceEnd();
            }

            mHandler.post(mAtmInternal::showSystemReadyErrorDialogsIfNeeded);

       
      		// ....
            t.traceEnd(); // PhaseActivityManagerReady
        }
    }
```



并且`startOtherServices`方法的最后，调用`startServiceAsUser`启动了SystemUI；

```java
// frameworks/base/services/java/com/android/server/SystemServer.java
		t.traceBegin("StartSystemUI");
        try {
            startSystemUi(context, windowManagerF);
        } catch (Throwable e) {
            reportWtf("starting System UI", e);
        }
        t.traceEnd();
```



```java
// frameworks/base/services/java/com/android/server/SystemServer.java
	private static void startSystemUi(Context context, WindowManagerService windowManager) {
        PackageManagerInternal pm = LocalServices.getService(PackageManagerInternal.class);
        Intent intent = new Intent();
        intent.setComponent(pm.getSystemUiServiceComponent());
        intent.addFlags(Intent.FLAG_DEBUG_TRIAGED_MISSING);
        //Slog.d(TAG, "Starting service: " + intent);
        context.startServiceAsUser(intent, UserHandle.SYSTEM);
        windowManager.onSystemUiStarted();
    }
```







##### startApexServices

```java
/**
     * Starts system services defined in apexes.
     *
     * <p>Apex services must be the last category of services to start. No other service must be
     * starting after this point. This is to prevent unnecessary stability issues when these apexes
     * are updated outside of OTA; and to avoid breaking dependencies from system into apexes.
     */
    private void startApexServices(@NonNull TimingsTraceAndSlog t) {
        t.traceBegin("startApexServices");
        // TODO(b/192880996): get the list from "android" package, once the manifest entries
        // are migrated to system manifest.
        List<ApexSystemServiceInfo> services = ApexManager.getInstance().getApexSystemServices();
        for (ApexSystemServiceInfo info : services) {
            String name = info.getName();
            String jarPath = info.getJarPath();
            t.traceBegin("starting " + name);
            if (TextUtils.isEmpty(jarPath)) {
                mSystemServiceManager.startService(name);
            } else {
                mSystemServiceManager.startServiceFromJar(name, jarPath);
            }
            t.traceEnd();
        }

        // make sure no other services are started after this point
        mSystemServiceManager.sealStartedServices();

        t.traceEnd(); // startApexServices
    }
```

启动在apex中定义的系统服务。

确保apex服务是启动的最后一类服务，避免在其后启动其他服务。



## 参考

1. [platform/superproject/main - Android Code Search](https://cs.android.com/android/platform/superproject/main/+/main:)
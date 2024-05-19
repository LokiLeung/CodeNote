# 【Android经验技巧】 Android14全部系统属性含义

> 属性来源： Android14 虚拟设备中， getprop获取；
>
> 因为该系统属性太多，部分可能存在纰漏，如发现错误，可联系作者，谢谢大家



####  [apex.all.ready]: [true]

- 含义：该属性表示所有的 APEX 模块是否已准备就绪。APEX（Android Python EXecutable）是 Android 12 中引入的一种新的软件包管理机制，用于将系统服务和可执行文件打包为模块，以便更轻松地更新和管理系统组件。
- 代码来源：system/apex/apexd/apexd.cpp

> Set a system property to let other components know that APEXs are  correctly mounted and ready to be used. Before using any file from APEXs,  they can query this system property to ensure that they are okay to  access. Or they may have a on-property trigger to delay a task until APEXs become ready.
>
> Since apexd.status property is a system property, we expose yet another property as system_restricted_prop so that, for example, vendor can rely on the "ready" event.
>
> 设置一个系统属性，让其他组件知道 APEX 已正确安装并准备就绪。在使用 APEX 中的任何文件之前，它们可以查询此系统属性，以确保可以访问这些文件。或者，它们可以使用一个 on-property 触发器来延迟任务，直到 APEX 准备就绪。
>
> 由于 apexd.status 属性是一个系统属性，我们将另一个属性公开为 system_restricted_prop，这样，例如，供应商就可以依赖 “ready ”事件。

#### [bluetooth.device.class_of_device]: [90,2,12]

+ 含义：这个属性指定了蓝牙设备的设备类别。在这里，数值"90,2,12"表示设备类别为"90"，服务类别为"2"，主要服务类别为"12"。这些数字与蓝牙规范中定义的设备类别对应，但具体含义取决于每个数字的组合。
+ 代码来源：device/generic/goldfish/product/bluetooth.prop
+ 补充device/generic/goldfish/product/bluetooth.prop代码

```makefile
# Set the Bluetooth Class of Device
# Service Field: 0x5A -> 90
#    Bit 17: Networking
#    Bit 19: Capturing
#    Bit 20: Object Transfer
#    Bit 22: Telephony
# MAJOR_CLASS: 0x02 -> 2 (Phone)
# MINOR_CLASS: 0x0C -> 12 (Smart Phone)
bluetooth.device.class_of_device=90,2,12

# Set supported Bluetooth profiles to enabled

# Disable asha profile as it will disable
# the cts-verifier multi advertising tests (b/249536741)
# bluetooth.profile.asha.central.enabled=true

# Disable LeAudio related profile as there is no support for it
bluetooth.profile.bap.broadcast.assist.enabled=false
bluetooth.profile.bap.unicast.client.enabled=false
bluetooth.profile.bas.client.enabled=false
bluetooth.profile.ccp.server.enabled=false
bluetooth.profile.hap.client.enabled=false
bluetooth.profile.csip.set_coordinator.enabled=false
bluetooth.profile.vcp.controller.enabled=false

bluetooth.profile.a2dp.source.enabled=true
bluetooth.profile.avrcp.target.enabled=true
bluetooth.profile.gatt.enabled=true
bluetooth.profile.hfp.ag.enabled=true
bluetooth.profile.hid.device.enabled=true
bluetooth.profile.hid.host.enabled=true
bluetooth.profile.map.server.enabled=true
bluetooth.profile.mcp.server.enabled=true
bluetooth.profile.opp.enabled=true
bluetooth.profile.pan.nap.enabled=true
bluetooth.profile.pan.panu.enabled=true
bluetooth.profile.pbap.server.enabled=true
```

#### [bluetooth.profile.a2dp.source.enabled]: [true]

- 含义：此属性指示是否启用了 A2DP（高级音频分发配置文件）源的蓝牙配置文件。A2DP 是一种用于通过蓝牙无线传输高质量音频的协议，它允许设备作为音频源（例如手机）向另一个设备（例如耳机或扬声器）发送音频流。
- 代码来源：device/generic/goldfish/product/bluetooth.prop

#### [bluetooth.profile.avrcp.target.enabled]: [true]

- 含义：此属性指示是否启用了 AVRCP（音频/视频远程控制配置文件）目标的蓝牙配置文件。AVRCP 允许设备（如手机或音频播放器）通过蓝牙远程控制另一个设备（如蓝牙音频设备）的音频/视频播放。
- 代码来源：device/generic/goldfish/product/bluetooth.prop

#### [bluetooth.profile.bap.broadcast.assist.enabled]: [false]

- 含义：此属性指示是否启用了 BAP（蓝牙访问点）广播辅助的蓝牙配置文件。BAP 是一种允许蓝牙设备通过广播方式提供互联网接入服务的协议。
- 代码来源：device/generic/goldfish/product/bluetooth.prop

#### [bluetooth.profile.bap.unicast.client.enabled]: [false]

- 含义：此属性指示是否启用了 BAP（蓝牙访问点）单播客户端的蓝牙配置文件。BAP 单播客户端允许蓝牙设备通过与远程蓝牙访问点建立单播连接来访问互联网服务。
- 代码来源：device/generic/goldfish/product/bluetooth.prop

#### [bluetooth.profile.bas.client.enabled]: [false]

- 含义：此属性指示是否启用了 BAS（蓝牙电池服务）客户端的蓝牙配置文件。BAS 允许蓝牙设备获取远程设备（如耳机或手表）的电池电量信息。
- 代码来源：device/generic/goldfish/product/bluetooth.prop

#### [bluetooth.profile.ccp.server.enabled]: [false]

- 含义：此属性指示是否启用了 CCP（蓝牙车载电话控制配置文件）服务器的蓝牙配置文件。CCP 允许蓝牙设备控制与车载电话系统的通信。
- 代码来源：device/generic/goldfish/product/bluetooth.prop

#### [bluetooth.profile.csip.set_coordinator.enabled]: [false]

- 含义：此属性指示是否启用了 CSIP（蓝牙增强坐席控制配置文件）设置协调器的蓝牙配置文件。CSIP 允许蓝牙设备作为增强坐席控制器，管理多个蓝牙连接。
- 代码来源：device/generic/goldfish/product/bluetooth.prop

#### [bluetooth.profile.gatt.enabled]: [true]

- 含义：此属性指示是否启用了 GATT（通用属性配置文件）的蓝牙配置文件。GATT 是蓝牙低功耗（BLE）通信协议的核心部分，用于在蓝牙设备之间传输数据。
- 代码来源：device/generic/goldfish/product/bluetooth.prop

#### [bluetooth.profile.hap.client.enabled]: [false]

- 含义：此属性指示是否启用了 HAP（蓝牙人体活动监测配置文件）客户端的蓝牙配置文件。HAP 允许蓝牙设备接收来自另一设备（如健康监测设备）的人体活动数据。
- 代码来源：device/generic/goldfish/product/bluetooth.prop

####  [bluetooth.profile.hfp.ag.enabled]: [true]

- 含义：此属性指示是否启用了 HFP（蓝牙电话音频网关）AG（音频网关）的蓝牙配置文件。HFP 允许蓝牙设备充当电话音频网关，用于在车辆和蓝牙手机之间传输电话音频。
- 代码来源：device/generic/goldfish/product/bluetooth.prop

#### [bluetooth.profile.hid.device.enabled]: [true]

- 含义：此属性指示是否启用了 HID（人机接口设备）设备的蓝牙配置文件。HID 设备允许蓝牙设备（如键盘或鼠标）将其输入传输到其他设备（如手机或电脑）。
- 代码来源：device/generic/goldfish/product/bluetooth.prop

#### [bluetooth.profile.hid.host.enabled]: [true]

- 含义：此属性指示是否启用了 HID（人机接口设备）主机的蓝牙配置文件。HID 主机允许蓝牙设备（如手机或电脑）接收来自其他设备（如键盘或鼠标）的输入。
- 代码来源：device/generic/goldfish/product/bluetooth.prop

#### [bluetooth.profile.map.server.enabled]: [true]

- 含义：此属性指示是否启用了 MAP（消息访问配置文件）服务器的蓝牙配置文件。MAP 允许蓝牙设备通过消息访问配置文件与手机通信，以便在车载系统上读取和发送消息。
- 代码来源：device/generic/goldfish/product/bluetooth.prop

#### [bluetooth.profile.mcp.server.enabled]: [true]

- 含义：此属性指示是否启用了 MCP（蓝牙消息通知配置文件）服务器的蓝牙配置文件。MCP 允许蓝牙设备将手机上的通知推送到其他蓝牙设备（如智能手表或耳机）上显示。
- 代码来源：device/generic/goldfish/product/bluetooth.prop

#### [bluetooth.profile.opp.enabled]: [true]

- 含义：此属性指示是否启用了 OPP（对象推送配置文件）的蓝牙配置文件。OPP 允许蓝牙设备之间直接传输文件，例如图片、视频或联系人。
- 代码来源：device/generic/goldfish/product/bluetooth.prop

#### [bluetooth.profile.pan.nap.enabled]: [true]

- 含义：此属性指示是否启用了 PAN（个人区域网络）NAP（网络接入点）的蓝牙配置文件。PAN 允许蓝牙设备充当网络接入点，以便其他设备（如电脑或平板电脑）通过蓝牙连接到互联网。
- 代码来源：device/generic/goldfish/product/bluetooth.prop

#### [bluetooth.profile.pan.panu.enabled]: [true]

- 含义：此属性指示是否启用了 PAN（个人区域网络）PANU（个人区域网络用户）的蓝牙配置文件。PANU 允许蓝牙设备连接到另一个设备的网络接入点，以便访问互联网。
- 代码来源：device/generic/goldfish/product/bluetooth.prop

#### [bluetooth.profile.pbap.server.enabled]: [true]

- 含义：此属性指示是否启用了 PBAP（电话本访问配置文件）服务器的蓝牙配置文件。PBAP 允许蓝牙设备访问另一设备（如手机）的电话簿和联系人信息。
- 代码来源：device/generic/goldfish/product/bluetooth.prop

#### [bluetooth.profile.vcp.controller.enabled]: [false]

- 含义：此属性指示是否启用了 VCP（虚拟串口控制器）控制器的蓝牙配置文件。VCP 允许蓝牙设备模拟串口通信，以便通过蓝牙与其他设备进行数据交换。
- 代码来源：device/generic/goldfish/product/bluetooth.prop

####  [bootreceiver.enable]: [1]

- 含义：此属性指示启动接收器是否已启用。启动接收器是一个组件，它可以在设备启动时接收系统广播，用于执行特定的操作或初始化任务。
- 代码来源：system/core/rootdir/init.rc

```rc
# Only enable the bootreceiver tracing instance for kernels 5.10 and above.
on late-fs && property:ro.kernel.version=4.9
    setprop bootreceiver.enable 0
on late-fs && property:ro.kernel.version=4.14
    setprop bootreceiver.enable 0
on late-fs && property:ro.kernel.version=4.19
    setprop bootreceiver.enable 0
on late-fs && property:ro.kernel.version=5.4
    setprop bootreceiver.enable 0
on late-fs
    # Bootreceiver tracing instance is enabled by default.
    setprop bootreceiver.enable ${bootreceiver.enable:-1}
```



#### [build.version.extensions.xxx]

```bash
[build.version.extensions.ad_services]: [7]
[build.version.extensions.r]: [7]
[build.version.extensions.s]: [7]
[build.version.extensions.t]: [7]
```

> [SDK 扩展  | Android 开发者  | Android Developers](https://developer.android.com/guide/sdk-extensions?hl=zh-cn#java)
>
> SDK 扩展利用[模块化系统组件](https://source.android.com/docs/core/ota/modular-system?hl=zh-cn)将 API 添加到之前发布的特定 API 级别的公共 SDK 中。当最终用户通过 [Google Play 系统更新](https://support.google.com/product-documentation/answer/11462338?hl=zh-cn)收到模块更新后，这些 API 即可在设备上使用。应用开发者可以在其应用中利用这些 API，以提供这些先前 Android 版本的 SDK 原本不支持的其他功能。（Google Play == 不开源）

- 代码来源：packages/modules/SdkExtensions/java/android/os/ext/SdkExtensions.java（这里只获取，不设置）





### [cache_key.bluetooth.bluetooth_adapter_get_connection_state]: [513599002842172890]

+ 含义：此属性用于缓存蓝牙适配器的连接状态信息。
+ 代码来源：frameworks/base/core/java/android/bluetooth/BluetoothAdapter.java

### [cache_key.bluetooth.bluetooth_adapter_get_profile_connection_state]: [513599002842172891]

+ 含义：此属性用于缓存蓝牙适配器的配置文件连接状态信息。
+ 代码来源：frameworks/base/core/java/android/bluetooth/BluetoothAdapter.java

### [cache_key.bluetooth.bluetooth_adapter_get_state]: [513599002842172892]

+ 含义：此属性用于缓存蓝牙适配器的状态信息。
+ 代码来源：frameworks/base/core/java/android/bluetooth/BluetoothAdapter.java

### [cache_key.bluetooth.bluetooth_adapter_is_offloaded_filtering_supported]: [513599002842172886]

+ 含义：此属性用于缓存蓝牙适配器是否支持蓝牙数据包的离线过滤。
+ 代码来源：frameworks/base/core/java/android/bluetooth/BluetoothAdapter.java

### [cache_key.bluetooth.bluetooth_device_get_bond_state]: [513599002842172883]

+ 含义：此属性用于缓存蓝牙设备的绑定状态。
+ 代码来源：frameworks/base/core/java/android/bluetooth/BluetoothDevice.java

### [cache_key.bluetooth.bluetooth_map_get_connection_state]: [513599002842172889]

+ 含义：此属性用于缓存蓝牙消息访问档案（MAP）的连接状态。
+ 代码来源：frameworks/base/core/java/android/bluetooth/BluetoothMap.java

### [cache_key.bluetooth.bluetooth_sap_get_connection_state]: [513599002842172885]

+ 含义：此属性用于缓存蓝牙模拟接入协议（SAP）的连接状态。
+ 代码来源：frameworks/base/core/java/android/bluetooth/BluetoothSap.java

### [cache_key.display_info]: [-5786075127245555287]

+ 含义：此属性用于缓存显示信息。
+ 代码来源：frameworks/base/core/java/android/view/DisplayInfo.java

### [cache_key.get_packages_for_uid]: [-5786075127245555139]

+ 含义：此属性用于缓存给定 UID 的应用程序包列表。
+ 代码来源：frameworks/base/services/core/java/com/android/server/pm/PackageManagerService.java

### [cache_key.has_system_feature]: [-5786075127245555327]

+ 含义：此属性用于缓存系统功能的存在。
+ 代码来源：frameworks/base/core/java/android/content/pm/PackageManager.java

### [cache_key.is_compat_change_enabled]: [-5786075127245555141]

+ 含义：此属性用于缓存兼容性更改的启用状态。
+ 代码来源：frameworks/base/core/java/android/app/AppGlobals.java

### [cache_key.is_interactive]: [-5786075127245555340]

+ 含义：此属性用于缓存设备的交互状态，即设备是否处于交互模式。
+ 代码来源：frameworks/base/core/java/android/content/Context.java

### [cache_key.is_power_save_mode]: [-5786075127245555312]

+ 含义：此属性用于缓存设备的省电模式状态。
+ 代码来源：frameworks/base/core/java/android/os/PowerManager.java

### [cache_key.is_user_unlocked]: [-5786075127245555270]

+ 含义：此属性用于缓存用户是否已解锁设备。
+ 代码来源：frameworks/base/core/java/android/os/UserManager.java

### [cache_key.location_enabled]: [-5786075127245555314]

+ 含义：此属性用于缓存位置服务的启用状态。
+ 代码来源：frameworks/base/core/java/android/location/LocationManager.java

### [cache_key.package_info]: [-5786075127245555140]

+ 含义：此属性用于缓存应用程序包的信息。
+ 代码来源：frameworks/base/core/java/android/app/ActivityManager.java

### [cache_key.system_server.accounts_data]: [-5786075127245555255]

+ 含义：此属性用于缓存系统服务中的帐户数据。
+ 代码来源：frameworks/base/services/core/java/com/android/server/accounts/AccountManagerService.java

### [cache_key.system_server.device_policy_manager_caches]: [-5786075127245555316]

+ 含义：此属性用于缓存系统服务中设备策略管理器的缓存。
+ 代码来源：frameworks/base/services/core/java/com/android/server/devicepolicy/DevicePolicyManagerService.java

### [cache_key.system_server.get_credential_type]: [-5786075127245555313]

+ 含义：此属性用于缓存系统服务中的凭据类型。
+ 代码来源：frameworks/base/services/core/java/com/android/server/SystemServer.java

### [cache_key.telephony.phone_account_to_subid]: [7486266560909763048]

+ 含义：此属性用于缓存电话帐户到子 ID 的映射。
+ 代码来源：frameworks/base/telephony/java/android/telephony/SubscriptionManager.java

### [cache_key.telephony.subscription_manager_service]: [7486266560909763046]

+ 含义：此属性用于缓存订阅管理器服务的信息。
+ 代码来源：frameworks/base/telephony/java/com/android/internal/telephony/SubscriptionController.java

> 

### [camera.enable_landscape_to_portrait]: [true]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.appimageformat]: [lz4]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.dex2oat-Xms]: [64m]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.dex2oat-Xmx]: [512m]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.dex2oat-max-image-block-size]: [524288]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.dex2oat-minidebuginfo]: [true]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.dex2oat-resolve-startup-strings]: [true]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.dex2oat64.enabled]: [true]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.dexopt.secondary]: [true]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.dexopt.thermal-cutoff]: [2]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.heapgrowthlimit]: [192m]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.heapmaxfree]: [8m]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.heapminfree]: [512k]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.heapsize]: [512m]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.heapstartsize]: [8m]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.heaptargetutilization]: [0.75]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.image-dex2oat-Xms]: [64m]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.image-dex2oat-Xmx]: [64m]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.isa.x86_64.features]: [default]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.isa.x86_64.variant]: [x86_64]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.lockprof.threshold]: [500]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.madvise.artfile.size]: [4294967295]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.madvise.odexfile.size]: [104857600]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.madvise.vdexfile.size]: [104857600]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.minidebuginfo]: [true]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.usap_pool_enabled]: [false]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.usap_pool_refill_delay_ms]: [3000]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.usap_pool_size_max]: [3]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.usap_pool_size_min]: [1]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.usap_refill_threshold]: [1]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.useartservice]: [true]
+ 含义：
+ 代码来源：
> 

### [dalvik.vm.usejit]: [true]
+ 含义：
+ 代码来源：
> 

### [debug.atrace.tags.enableflags]: [0]
+ 含义：
+ 代码来源：
> 

### [debug.force_rtl]: [false]
+ 含义：
+ 代码来源：
> 

### [debug.hwui.renderer]: [skiagl]
+ 含义：
+ 代码来源：
> 

### [debug.sf.vsync_reactor_ignore_present_fences]: [true]
+ 含义：
+ 代码来源：
> 

### [debug.stagefright.c2inputsurface]: [-1]
+ 含义：
+ 代码来源：
> 

### [debug.stagefright.ccodec]: [4]
+ 含义：
+ 代码来源：
> 

### [debug.tracing.battery_stats.audio]: [0]
+ 含义：
+ 代码来源：
> 

### [debug.tracing.battery_stats.ble_scan]: [1]
+ 含义：
+ 代码来源：
> 

### [debug.tracing.battery_stats.brightness]: [2]
+ 含义：
+ 代码来源：
> 

### [debug.tracing.battery_stats.data_conn]: [10]
+ 含义：
+ 代码来源：
> 

### [debug.tracing.battery_stats.mobile_radio]: [1]
+ 含义：
+ 代码来源：
> 

### [debug.tracing.battery_stats.phone_signal_strength]: [4]
+ 含义：
+ 代码来源：
> 

### [debug.tracing.battery_stats.phone_state]: [0]
+ 含义：
+ 代码来源：
> 

### [debug.tracing.battery_stats.running]: [1]
+ 含义：
+ 代码来源：
> 

### [debug.tracing.battery_stats.screen]: [1]
+ 含义：
+ 代码来源：
> 

### [debug.tracing.battery_stats.sensor]: [1]
+ 含义：
+ 代码来源：
> 

### [debug.tracing.battery_stats.wake_lock]: [1]
+ 含义：
+ 代码来源：
> 

### [debug.tracing.battery_stats.wifi]: [1]
+ 含义：
+ 代码来源：
> 

### [debug.tracing.battery_stats.wifi_scan]: [0]
+ 含义：
+ 代码来源：
> 

### [debug.tracing.battery_status]: [4]
+ 含义：
+ 代码来源：
> 

### [debug.tracing.device_state]: [0:DEFAULT]
+ 含义：
+ 代码来源：
> 

### [debug.tracing.mcc]: [310]
+ 含义：
+ 代码来源：
> 

### [debug.tracing.mnc]: [260]
+ 含义：
+ 代码来源：
> 

### [debug.tracing.plug_type]: [0]
+ 含义：
+ 代码来源：
> 

### [debug.tracing.screen_brightness]: [0.39763778]
+ 含义：
+ 代码来源：
> 

### [dev.bootcomplete]: [1]
+ 含义：
+ 代码来源：
> 

### [dev.mnt.blk.metadata]: [vdd1]
+ 含义：
+ 代码来源：
> 

### [dev.mnt.blk.product]: [vda2]
+ 含义：
+ 代码来源：
> 

### [dev.mnt.blk.root]: [vda2]
+ 含义：
+ 代码来源：
> 

### [dev.mnt.blk.system_dlkm]: [vda2]
+ 含义：
+ 代码来源：
> 

### [dev.mnt.blk.system_ext]: [vda2]
+ 含义：
+ 代码来源：
> 

### [dev.mnt.blk.vendor]: [vda2]
+ 含义：
+ 代码来源：
> 

### [dev.mnt.dev.metadata]: [vdd1]
+ 含义：
+ 代码来源：
> 

### [dev.mnt.dev.product]: [dm-3]
+ 含义：
+ 代码来源：
> 

### [dev.mnt.dev.root]: [dm-5]
+ 含义：
+ 代码来源：
> 

### [dev.mnt.dev.system_dlkm]: [dm-1]
+ 含义：
+ 代码来源：
> 

### [dev.mnt.dev.system_ext]: [dm-2]
+ 含义：
+ 代码来源：
> 

### [dev.mnt.dev.vendor]: [dm-4]
+ 含义：
+ 代码来源：
> 

### [dev.mnt.rootdisk.metadata]: [vdd]
+ 含义：
+ 代码来源：
> 

### [dev.mnt.rootdisk.product]: [vda]
+ 含义：
+ 代码来源：
> 

### [dev.mnt.rootdisk.root]: [vda]
+ 含义：
+ 代码来源：
> 

### [dev.mnt.rootdisk.system_dlkm]: [vda]
+ 含义：
+ 代码来源：
> 

### [dev.mnt.rootdisk.system_ext]: [vda]
+ 含义：
+ 代码来源：
> 

### [dev.mnt.rootdisk.vendor]: [vda]
+ 含义：
+ 代码来源：
> 

### [gsm.current.phone-type]: [1]
+ 含义：
+ 代码来源：
> 

### [gsm.network.type]: [HSPA]
+ 含义：
+ 代码来源：
> 

### [gsm.operator.alpha]: [T-Mobile]
+ 含义：
+ 代码来源：
> 

### [gsm.operator.iso-country]: [us]
+ 含义：
+ 代码来源：
> 

### [gsm.operator.isroaming]: [false]
+ 含义：
+ 代码来源：
> 

### [gsm.operator.numeric]: [310260]
+ 含义：
+ 代码来源：
> 

### [gsm.sim.operator.alpha]: [T-Mobile]
+ 含义：
+ 代码来源：
> 

### [gsm.sim.operator.iso-country]: [us]
+ 含义：
+ 代码来源：
> 

### [gsm.sim.operator.numeric]: [310260]
+ 含义：
+ 代码来源：
> 

### [gsm.sim.state]: [LOADED]
+ 含义：
+ 代码来源：
> 

### [gsm.version.baseband]: [1.0.0.0]
+ 含义：
+ 代码来源：
> 

### [gsm.version.ril-impl]: [android reference-ril 1.0]
+ 含义：
+ 代码来源：
> 

### [hwservicemanager.ready]: [true]
+ 含义：
+ 代码来源：
> 

### [init.svc.adbd]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.android-hardware-media-c2-goldfish-hal-1-0]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.apexd]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.apexd-bootstrap]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.apexd-snapshotde]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.art_boot]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.audioserver]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.bootanim]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.boringssl_self_test64]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.boringssl_self_test64_vendor]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.boringssl_self_test_apex64]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.bpfloader]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.bt_vhci_forwarder]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.cameraserver]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.console]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.credstore]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.derive_classpath]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.derive_sdk]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.dhcpclient_wifi]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.dmesgd]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.drm]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.gatekeeperd]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.goldfish-logcat]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.gpu]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.heapprofd]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.hidl_memory]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.hwservicemanager]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.idmap2d]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.incidentd]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.installd]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.keystore2]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.lmkd]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.logd]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.logd-auditctl]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.logd-reinit]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.mdnsd]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.media]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.media.swcodec]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.mediadrm]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.mediaextractor]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.mediametrics]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.netd]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.neuralnetworks_hal_service_aidl_sample_all]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.neuralnetworks_hal_service_aidl_sample_limited]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.neuralnetworks_hal_service_shim_sample]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.odsign]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.prng_seeder]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.qemu-adb-keys]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.qemu-adb-setup]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.qemu-device-state]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.qemu-props]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.qemu-props-bootcomplete]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.ranchu-net]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.ranchu-setup]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.servicemanager]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.statsd]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.storaged]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.surfaceflinger]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.system_suspend]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.tombstoned]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.traced]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.traced_perf]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.traced_probes]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.ueventd]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.update_verifier_nonencrypted]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.usbd]: [stopped]
+ 含义：
+ 代码来源：
> 

### [init.svc.vold]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.wificond]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.wpa_supplicant]: [running]
+ 含义：
+ 代码来源：
> 

### [init.svc.zygote]: [running]
+ 含义：
+ 代码来源：
> 

### [log.tag.APM_AudioPolicyManager]: [D]
+ 含义：
+ 代码来源：
> 

### [log.tag.stats_log]: [I]
+ 含义：
+ 代码来源：
> 

### [logd.logpersistd.enable]: [true]
+ 含义：
+ 代码来源：
> 

### [logd.ready]: [true]
+ 含义：
+ 代码来源：
> 

### [media.mediadrmservice.enable]: [true]
+ 含义：
+ 代码来源：
> 

### [net.bt.name]: [Android]
+ 含义：
+ 代码来源：
> 

### [odsign.key.done]: [1]
+ 含义：
+ 代码来源：
> 

### [odsign.verification.done]: [1]
+ 含义：
+ 代码来源：
> 

### [odsign.verification.success]: [1]
+ 含义：
+ 代码来源：
> 

### [partition.system.verified]: [2]
+ 含义：
+ 代码来源：
> 

### [partition.system.verified.check_at_most_once]: [0]
+ 含义：
+ 代码来源：
> 

### [partition.system.verified.hash_alg]: [sha256]
+ 含义：
+ 代码来源：
> 

### [partition.system.verified.root_digest]: [029db0fd5a0d206cbbf73f3afc1e7ba5ed8ea6293d6a9149d47498f40a1a8dfa]
+ 含义：
+ 代码来源：
> 

### [persist.debug.dalvik.vm.core_platform_api_policy]: [just-warn]
+ 含义：
+ 代码来源：
> 

### [persist.device_config.nnapi_native.current_feature_level]: [7]
+ 含义：
+ 代码来源：
> 

### [persist.device_config.nnapi_native.telemetry_enable]: [false]
+ 含义：
+ 代码来源：
> 

### [persist.device_config.runtime_native.metrics.reporting-mods]: [0]
+ 含义：
+ 代码来源：
> 

### [persist.device_config.runtime_native.metrics.reporting-mods-server]: [0]
+ 含义：
+ 代码来源：
> 

### [persist.device_config.runtime_native.metrics.reporting-num-mods]: [100]
+ 含义：
+ 代码来源：
> 

### [persist.device_config.runtime_native.metrics.reporting-num-mods-server]: [100]
+ 含义：
+ 代码来源：
> 

### [persist.device_config.runtime_native.metrics.write-to-statsd]: [false]
+ 含义：
+ 代码来源：
> 

### [persist.device_config.runtime_native.use_app_image_startup_cache]: [true]
+ 含义：
+ 代码来源：
> 

### [persist.device_config.runtime_native_boot.disable_lock_profiling]: [false]
+ 含义：
+ 代码来源：
> 

### [persist.device_config.runtime_native_boot.enable_uffd_gc_2]: [false]
+ 含义：
+ 代码来源：
> 

### [persist.device_config.runtime_native_boot.force_disable_uffd_gc]: [false]
+ 含义：
+ 代码来源：
> 

### [persist.device_config.runtime_native_boot.iorap_blacklisted_packages]: []
+ 含义：
+ 代码来源：
> 

### [persist.device_config.runtime_native_boot.iorap_perfetto_enable]: [false]
+ 含义：
+ 代码来源：
> 

### [persist.device_config.runtime_native_boot.iorap_readahead_enable]: [false]
+ 含义：
+ 代码来源：
> 

### [persist.device_config.runtime_native_boot.iorapd_options]: []
+ 含义：
+ 代码来源：
> 

### [persist.radio.is_vonr_enabled_0]: [false]
+ 含义：
+ 代码来源：
> 

### [persist.sys.boot.reason]: []
+ 含义：
+ 代码来源：
> 

### [persist.sys.boot.reason.history]: [reboot,1713968588
+ 含义：
+ 代码来源：
> 

### reboot,factory_reset,1705842858
+ 含义：
+ 代码来源：
> 

### reboot,1705842814]
+ 含义：
+ 代码来源：
> 

### [persist.sys.dalvik.vm.lib.2]: [libart.so]
+ 含义：
+ 代码来源：
> 

### [persist.sys.disable_rescue]: [true]
+ 含义：
+ 代码来源：
> 

### [persist.sys.displayinset.top]: [0]
+ 含义：
+ 代码来源：
> 

### [persist.sys.fuse]: [true]
+ 含义：
+ 代码来源：
> 

### [persist.sys.gps.lpp]: [2]
+ 含义：
+ 代码来源：
> 

### [persist.sys.lmk.reportkills]: [true]
+ 含义：
+ 代码来源：
> 

### [persist.sys.timezone]: [GMT]
+ 含义：
+ 代码来源：
> 

### [persist.sys.usb.config]: [adb]
+ 含义：
+ 代码来源：
> 

### [persist.traced.enable]: [1]
+ 含义：
+ 代码来源：
> 

### [persist.wm.extensions.enabled]: [true]
+ 含义：
+ 代码来源：
> 

### [pm.dexopt.ab-ota]: [speed-profile]
+ 含义：
+ 代码来源：
> 

### [pm.dexopt.bg-dexopt]: [speed-profile]
+ 含义：
+ 代码来源：
> 

### [pm.dexopt.boot-after-mainline-update]: [verify]
+ 含义：
+ 代码来源：
> 

### [pm.dexopt.boot-after-ota]: [verify]
+ 含义：
+ 代码来源：
> 

### [pm.dexopt.cmdline]: [verify]
+ 含义：
+ 代码来源：
> 

### [pm.dexopt.first-boot]: [verify]
+ 含义：
+ 代码来源：
> 

### [pm.dexopt.inactive]: [verify]
+ 含义：
+ 代码来源：
> 

### [pm.dexopt.install]: [speed-profile]
+ 含义：
+ 代码来源：
> 

### [pm.dexopt.install-bulk]: [speed-profile]
+ 含义：
+ 代码来源：
> 

### [pm.dexopt.install-bulk-downgraded]: [verify]
+ 含义：
+ 代码来源：
> 

### [pm.dexopt.install-bulk-secondary]: [verify]
+ 含义：
+ 代码来源：
> 

### [pm.dexopt.install-bulk-secondary-downgraded]: [extract]
+ 含义：
+ 代码来源：
> 

### [pm.dexopt.install-fast]: [skip]
+ 含义：
+ 代码来源：
> 

### [pm.dexopt.post-boot]: [extract]
+ 含义：
+ 代码来源：
> 

### [pm.dexopt.shared]: [speed]
+ 含义：
+ 代码来源：
> 

### [qemu.sf.lcd_density]: [440]
+ 含义：
+ 代码来源：
> 

### [remote_provisioning.enable_rkpd]: [true]
+ 含义：
+ 代码来源：
> 

### [remote_provisioning.hostname]: [remoteprovisioning.googleapis.com]
+ 含义：
+ 代码来源：
> 

### [ro.actionable_compatible_property.enabled]: [true]
+ 含义：
+ 代码来源：
> 

### [ro.adb.secure]: [0]
+ 含义：
+ 代码来源：
> 

### [ro.allow.mock.location]: [0]
+ 含义：
+ 代码来源：
> 

### [ro.apex.updatable]: [true]
+ 含义：
+ 代码来源：
> 

### [ro.baseband]: [unknown]
+ 含义：
+ 代码来源：
> 

### [ro.board.platform]: []
+ 含义：
+ 代码来源：
> 

### [ro.boot.avb_version]: [1.2]
+ 含义：
+ 代码来源：
> 

### [ro.boot.boot_devices]: [pci0000:00/0000:00:03.0]
+ 含义：
+ 代码来源：
> 

### [ro.boot.bootreason]: [reboot]
+ 含义：
+ 代码来源：
> 

### [ro.boot.dalvik.vm.heapsize]: [512m]
+ 含义：
+ 代码来源：
> 

### [ro.boot.debug.hwui.renderer]: [skiagl]
+ 含义：
+ 代码来源：
> 

### [ro.boot.dynamic_partitions]: [true]
+ 含义：
+ 代码来源：
> 

### [ro.boot.hardware]: [ranchu]
+ 含义：
+ 代码来源：
> 

### [ro.boot.logcat]: [*:V]
+ 含义：
+ 代码来源：
> 

### [ro.boot.opengles.version]: [196609]
+ 含义：
+ 代码来源：
> 

### [ro.boot.qemu]: [1]
+ 含义：
+ 代码来源：
> 

### [ro.boot.qemu.avd_name]: [Pixel_3a_API_34_extension_level_7_x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.boot.qemu.camera_hq_edge_processing]: [0]
+ 含义：
+ 代码来源：
> 

### [ro.boot.qemu.camera_protocol_ver]: [1]
+ 含义：
+ 代码来源：
> 

### [ro.boot.qemu.cpuvulkan.version]: [4202496]
+ 含义：
+ 代码来源：
> 

### [ro.boot.qemu.gltransport.drawFlushInterval]: [800]
+ 含义：
+ 代码来源：
> 

### [ro.boot.qemu.gltransport.name]: [pipe]
+ 含义：
+ 代码来源：
> 

### [ro.boot.qemu.hwcodec.avcdec]: [2]
+ 含义：
+ 代码来源：
> 

### [ro.boot.qemu.hwcodec.hevcdec]: [2]
+ 含义：
+ 代码来源：
> 

### [ro.boot.qemu.hwcodec.vpxdec]: [2]
+ 含义：
+ 代码来源：
> 

### [ro.boot.qemu.settings.system.screen_off_timeout]: [2147483647]
+ 含义：
+ 代码来源：
> 

### [ro.boot.qemu.virtiowifi]: [1]
+ 含义：
+ 代码来源：
> 

### [ro.boot.qemu.vsync]: [60]
+ 含义：
+ 代码来源：
> 

### [ro.boot.serialno]: [EMULATOR33X1X24X0]
+ 含义：
+ 代码来源：
> 

### [ro.boot.vbmeta.digest]: [b49736a9ec7427d8534087a1a2f3c7a5458eb89935a7df46bce7aeb595977c2d]
+ 含义：
+ 代码来源：
> 

### [ro.boot.vbmeta.hash_alg]: [sha256]
+ 含义：
+ 代码来源：
> 

### [ro.boot.vbmeta.size]: [6656]
+ 含义：
+ 代码来源：
> 

### [ro.boot.veritymode]: [enforcing]
+ 含义：
+ 代码来源：
> 

### [ro.bootimage.build.date]: [Sat Dec 16 23:01:15 UTC 2023]
+ 含义：
+ 代码来源：
> 

### [ro.bootimage.build.date.utc]: [1702767675]
+ 含义：
+ 代码来源：
> 

### [ro.bootimage.build.fingerprint]: [google/sdk_gphone64_x86_64/emu64xa:14/UE1A.230829.036.A1/11228894:userdebug/dev-keys]
+ 含义：
+ 代码来源：
> 

### [ro.bootimage.build.id]: [UE1A.230829.036.A1]
+ 含义：
+ 代码来源：
> 

### [ro.bootimage.build.tags]: [dev-keys]
+ 含义：
+ 代码来源：
> 

### [ro.bootimage.build.type]: [userdebug]
+ 含义：
+ 代码来源：
> 

### [ro.bootimage.build.version.incremental]: [11228894]
+ 含义：
+ 代码来源：
> 

### [ro.bootimage.build.version.release]: [14]
+ 含义：
+ 代码来源：
> 

### [ro.bootimage.build.version.release_or_codename]: [14]
+ 含义：
+ 代码来源：
> 

### [ro.bootimage.build.version.sdk]: [34]
+ 含义：
+ 代码来源：
> 

### [ro.bootloader]: [unknown]
+ 含义：
+ 代码来源：
> 

### [ro.bootmode]: [unknown]
+ 含义：
+ 代码来源：
> 

### [ro.build.ab_update]: [false]
+ 含义：
+ 代码来源：
> 

### [ro.build.characteristics]: [emulator]
+ 含义：
+ 代码来源：
> 

### [ro.build.date]: [Sat Dec 16 23:01:15 UTC 2023]
+ 含义：
+ 代码来源：
> 

### [ro.build.date.utc]: [1702767675]
+ 含义：
+ 代码来源：
> 

### [ro.build.description]: [sdk_gphone64_x86_64-userdebug 14 UE1A.230829.036.A1 11228894 dev-keys]
+ 含义：
+ 代码来源：
> 

### [ro.build.display.id]: [sdk_gphone64_x86_64-userdebug 14 UE1A.230829.036.A1 11228894 dev-keys]
+ 含义：
+ 代码来源：
> 

### [ro.build.fingerprint]: [google/sdk_gphone64_x86_64/emu64xa:14/UE1A.230829.036.A1/11228894:userdebug/dev-keys]
+ 含义：
+ 代码来源：
> 

### [ro.build.flavor]: [sdk_gphone64_x86_64-userdebug]
+ 含义：
+ 代码来源：
> 

### [ro.build.host]: [abfarm-release-2004-0129]
+ 含义：
+ 代码来源：
> 

### [ro.build.id]: [UE1A.230829.036.A1]
+ 含义：
+ 代码来源：
> 

### [ro.build.product]: [emu64xa]
+ 含义：
+ 代码来源：
> 

### [ro.build.tags]: [dev-keys]
+ 含义：
+ 代码来源：
> 

### [ro.build.type]: [userdebug]
+ 含义：
+ 代码来源：
> 

### [ro.build.user]: [android-build]
+ 含义：
+ 代码来源：
> 

### [ro.build.version.all_codenames]: [REL]
+ 含义：
+ 代码来源：
> 

### [ro.build.version.base_os]: []
+ 含义：
+ 代码来源：
> 

### [ro.build.version.codename]: [REL]
+ 含义：
+ 代码来源：
> 

### [ro.build.version.incremental]: [11228894]
+ 含义：
+ 代码来源：
> 

### [ro.build.version.known_codenames]: [Base,Base11,Cupcake,Donut,Eclair,Eclair01,EclairMr1,Froyo,Gingerbread,GingerbreadMr1,Honeycomb,HoneycombMr1,HoneycombMr2,IceCreamSandwich,IceCreamSandwichMr1,JellyBean,JellyBeanMr1,JellyBeanMr2,Kitkat,KitkatWatch,Lollipop,LollipopMr1,M,N,NMr1,O,OMr1,P,Q,R,S,Sv2,Tiramisu,UpsideDownCake]
+ 含义：
+ 代码来源：
> 

### [ro.build.version.min_supported_target_sdk]: [28]
+ 含义：
+ 代码来源：
> 

### [ro.build.version.preview_sdk]: [0]
+ 含义：
+ 代码来源：
> 

### [ro.build.version.preview_sdk_fingerprint]: [REL]
+ 含义：
+ 代码来源：
> 

### [ro.build.version.release]: [14]
+ 含义：
+ 代码来源：
> 

### [ro.build.version.release_or_codename]: [14]
+ 含义：
+ 代码来源：
> 

### [ro.build.version.release_or_preview_display]: [14]
+ 含义：
+ 代码来源：
> 

### [ro.build.version.sdk]: [34]
+ 含义：
+ 代码来源：
> 

### [ro.build.version.security_patch]: [2023-09-05]
+ 含义：
+ 代码来源：
> 

### [ro.carrier]: [unknown]
+ 含义：
+ 代码来源：
> 

### [ro.com.android.dataroaming]: [true]
+ 含义：
+ 代码来源：
> 

### [ro.com.google.acsa]: [true]
+ 含义：
+ 代码来源：
> 

### [ro.com.google.locationfeatures]: [1]
+ 含义：
+ 代码来源：
> 

### [ro.config.alarm_alert]: [Alarm_Classic.ogg]
+ 含义：
+ 代码来源：
> 

### [ro.config.notification_sound]: [pixiedust.ogg]
+ 含义：
+ 代码来源：
> 

### [ro.config.ringtone]: [Ring_Synth_04.ogg]
+ 含义：
+ 代码来源：
> 

### [ro.control_privapp_permissions]: [enforce]
+ 含义：
+ 代码来源：
> 

### [ro.cp_system_other_odex]: [0]
+ 含义：
+ 代码来源：
> 

### [ro.cpuvulkan.version]: [4202496]
+ 含义：
+ 代码来源：
> 

### [ro.crypto.dm_default_key.options_format.version]: [2]
+ 含义：
+ 代码来源：
> 

### [ro.crypto.metadata.enabled]: [true]
+ 含义：
+ 代码来源：
> 

### [ro.crypto.state]: [encrypted]
+ 含义：
+ 代码来源：
> 

### [ro.crypto.type]: [file]
+ 含义：
+ 代码来源：
> 

### [ro.crypto.uses_fs_ioc_add_encryption_key]: [true]
+ 含义：
+ 代码来源：
> 

### [ro.crypto.volume.filenames_mode]: [aes-256-cts]
+ 含义：
+ 代码来源：
> 

### [ro.dalvik.vm.enable_uffd_gc]: [false]
+ 含义：
+ 代码来源：
> 

### [ro.dalvik.vm.isa.arm]: [x86]
+ 含义：
+ 代码来源：
> 

### [ro.dalvik.vm.isa.arm64]: [x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.dalvik.vm.native.bridge]: [libndk_translation.so]
+ 含义：
+ 代码来源：
> 

### [ro.debuggable]: [1]
+ 含义：
+ 代码来源：
> 

### [ro.enable.native.bridge.exec]: [1]
+ 含义：
+ 代码来源：
> 

### [ro.force.debuggable]: [0]
+ 含义：
+ 代码来源：
> 

### [ro.fuse.bpf.is_running]: [true]
+ 含义：
+ 代码来源：
> 

### [ro.hardware]: [ranchu]
+ 含义：
+ 代码来源：
> 

### [ro.hardware.egl]: [emulation]
+ 含义：
+ 代码来源：
> 

### [ro.hardware.gralloc]: [ranchu]
+ 含义：
+ 代码来源：
> 

### [ro.hardware.power]: [ranchu]
+ 含义：
+ 代码来源：
> 

### [ro.hardware.vulkan]: [ranchu]
+ 含义：
+ 代码来源：
> 

### [ro.hwui.use_vulkan]: []
+ 含义：
+ 代码来源：
> 

### [ro.kernel.qemu]: [1]
+ 含义：
+ 代码来源：
> 

### [ro.kernel.version]: [6.1]
+ 含义：
+ 代码来源：
> 

### [ro.logd.kernel]: [true]
+ 含义：
+ 代码来源：
> 

### [ro.logd.size]: [1M]
+ 含义：
+ 代码来源：
> 

### [ro.logd.size.stats]: [64K]
+ 含义：
+ 代码来源：
> 

### [ro.monkey]: [1]
+ 含义：
+ 代码来源：
> 

### [ro.ndk_translation.flags]: [accurate-sigsegv]
+ 含义：
+ 代码来源：
> 

### [ro.ndk_translation.version]: [0.2.3]
+ 含义：
+ 代码来源：
> 

### [ro.nnapi.extensions.deny_on_product]: [true]
+ 含义：
+ 代码来源：
> 

### [ro.odm.build.date]: [Sat Dec 16 23:01:15 UTC 2023]
+ 含义：
+ 代码来源：
> 

### [ro.odm.build.date.utc]: [1702767675]
+ 含义：
+ 代码来源：
> 

### [ro.odm.build.fingerprint]: [google/sdk_gphone64_x86_64/emu64xa:14/UE1A.230829.036.A1/11228894:userdebug/dev-keys]
+ 含义：
+ 代码来源：
> 

### [ro.odm.build.version.incremental]: [11228894]
+ 含义：
+ 代码来源：
> 

### [ro.opengles.version]: [196609]
+ 含义：
+ 代码来源：
> 

### [ro.organization_owned]: [false]
+ 含义：
+ 代码来源：
> 

### [ro.postinstall.fstab.prefix]: [/system]
+ 含义：
+ 代码来源：
> 

### [ro.product.board]: [goldfish_x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.product.bootimage.brand]: [google]
+ 含义：
+ 代码来源：
> 

### [ro.product.bootimage.device]: [emu64xa]
+ 含义：
+ 代码来源：
> 

### [ro.product.bootimage.manufacturer]: [Google]
+ 含义：
+ 代码来源：
> 

### [ro.product.bootimage.model]: [sdk_gphone64_x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.product.bootimage.name]: [sdk_gphone64_x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.product.brand]: [google]
+ 含义：
+ 代码来源：
> 

### [ro.product.build.date]: [Sat Dec 16 23:01:15 UTC 2023]
+ 含义：
+ 代码来源：
> 

### [ro.product.build.date.utc]: [1702767675]
+ 含义：
+ 代码来源：
> 

### [ro.product.build.fingerprint]: [google/sdk_gphone64_x86_64/emu64xa:14/UE1A.230829.036.A1/11228894:userdebug/dev-keys]
+ 含义：
+ 代码来源：
> 

### [ro.product.build.id]: [UE1A.230829.036.A1]
+ 含义：
+ 代码来源：
> 

### [ro.product.build.tags]: [dev-keys]
+ 含义：
+ 代码来源：
> 

### [ro.product.build.type]: [userdebug]
+ 含义：
+ 代码来源：
> 

### [ro.product.build.version.incremental]: [11228894]
+ 含义：
+ 代码来源：
> 

### [ro.product.build.version.release]: [14]
+ 含义：
+ 代码来源：
> 

### [ro.product.build.version.release_or_codename]: [14]
+ 含义：
+ 代码来源：
> 

### [ro.product.build.version.sdk]: [34]
+ 含义：
+ 代码来源：
> 

### [ro.product.cpu.abi]: [x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.product.cpu.abilist]: [x86_64,arm64-v8a]
+ 含义：
+ 代码来源：
> 

### [ro.product.cpu.abilist32]: []
+ 含义：
+ 代码来源：
> 

### [ro.product.cpu.abilist64]: [x86_64,arm64-v8a]
+ 含义：
+ 代码来源：
> 

### [ro.product.cpu.pagesize.max]: [65536]
+ 含义：
+ 代码来源：
> 

### [ro.product.device]: [emu64xa]
+ 含义：
+ 代码来源：
> 

### [ro.product.first_api_level]: [34]
+ 含义：
+ 代码来源：
> 

### [ro.product.locale]: [en-US]
+ 含义：
+ 代码来源：
> 

### [ro.product.manufacturer]: [Google]
+ 含义：
+ 代码来源：
> 

### [ro.product.model]: [sdk_gphone64_x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.product.name]: [sdk_gphone64_x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.product.odm.brand]: [google]
+ 含义：
+ 代码来源：
> 

### [ro.product.odm.device]: [emu64xa]
+ 含义：
+ 代码来源：
> 

### [ro.product.odm.manufacturer]: [Google]
+ 含义：
+ 代码来源：
> 

### [ro.product.odm.model]: [sdk_gphone64_x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.product.odm.name]: [sdk_gphone64_x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.product.product.brand]: [google]
+ 含义：
+ 代码来源：
> 

### [ro.product.product.device]: [emu64xa]
+ 含义：
+ 代码来源：
> 

### [ro.product.product.manufacturer]: [Google]
+ 含义：
+ 代码来源：
> 

### [ro.product.product.model]: [sdk_gphone64_x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.product.product.name]: [sdk_gphone64_x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.product.system.brand]: [google]
+ 含义：
+ 代码来源：
> 

### [ro.product.system.device]: [generic]
+ 含义：
+ 代码来源：
> 

### [ro.product.system.manufacturer]: [Google]
+ 含义：
+ 代码来源：
> 

### [ro.product.system.model]: [mainline]
+ 含义：
+ 代码来源：
> 

### [ro.product.system.name]: [mainline]
+ 含义：
+ 代码来源：
> 

### [ro.product.system_dlkm.brand]: [google]
+ 含义：
+ 代码来源：
> 

### [ro.product.system_dlkm.device]: [emu64xa]
+ 含义：
+ 代码来源：
> 

### [ro.product.system_dlkm.manufacturer]: [Google]
+ 含义：
+ 代码来源：
> 

### [ro.product.system_dlkm.model]: [sdk_gphone64_x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.product.system_dlkm.name]: [sdk_gphone64_x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.product.system_ext.brand]: [google]
+ 含义：
+ 代码来源：
> 

### [ro.product.system_ext.device]: [emu64xa]
+ 含义：
+ 代码来源：
> 

### [ro.product.system_ext.manufacturer]: [Google]
+ 含义：
+ 代码来源：
> 

### [ro.product.system_ext.model]: [sdk_gphone64_x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.product.system_ext.name]: [sdk_gphone64_x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.product.vendor.brand]: [google]
+ 含义：
+ 代码来源：
> 

### [ro.product.vendor.device]: [emu64xa]
+ 含义：
+ 代码来源：
> 

### [ro.product.vendor.manufacturer]: [Google]
+ 含义：
+ 代码来源：
> 

### [ro.product.vendor.model]: [sdk_gphone64_x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.product.vendor.name]: [sdk_gphone64_x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.product.vendor_dlkm.brand]: [google]
+ 含义：
+ 代码来源：
> 

### [ro.product.vendor_dlkm.device]: [emu64xa]
+ 含义：
+ 代码来源：
> 

### [ro.product.vendor_dlkm.manufacturer]: [Google]
+ 含义：
+ 代码来源：
> 

### [ro.product.vendor_dlkm.model]: [sdk_gphone64_x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.product.vendor_dlkm.name]: [sdk_gphone64_x86_64]
+ 含义：
+ 代码来源：
> 

### [ro.product.vndk.version]: [34]
+ 含义：
+ 代码来源：
> 

### [ro.property_service.version]: [2]
+ 含义：
+ 代码来源：
> 

### [ro.revision]: [0]
+ 含义：
+ 代码来源：
> 

### [ro.secure]: [1]
+ 含义：
+ 代码来源：
> 

### [ro.serialno]: [EMULATOR33X1X24X0]
+ 含义：
+ 代码来源：
> 

### [ro.setupwizard.mode]: [DISABLED]
+ 含义：
+ 代码来源：
> 

### [ro.soc.manufacturer]: [AOSP]
+ 含义：
+ 代码来源：
> 

### [ro.soc.model]: [ranchu]
+ 含义：
+ 代码来源：
> 

### [ro.surface_flinger.has_HDR_display]: [false]
+ 含义：
+ 代码来源：
> 

### [ro.surface_flinger.has_wide_color_display]: [false]
+ 含义：
+ 代码来源：
> 

### [ro.surface_flinger.protected_contents]: [false]
+ 含义：
+ 代码来源：
> 

### [ro.surface_flinger.supports_background_blur]: [1]
+ 含义：
+ 代码来源：
> 

### [ro.surface_flinger.use_color_management]: [false]
+ 含义：
+ 代码来源：
> 

### [ro.system.build.date]: [Sat Dec 16 23:01:15 UTC 2023]
+ 含义：
+ 代码来源：
> 

### [ro.system.build.date.utc]: [1702767675]
+ 含义：
+ 代码来源：
> 

### [ro.system.build.fingerprint]: [google/sdk_gphone64_x86_64/emu64xa:14/UE1A.230829.036.A1/11228894:userdebug/dev-keys]
+ 含义：
+ 代码来源：
> 

### [ro.system.build.id]: [UE1A.230829.036.A1]
+ 含义：
+ 代码来源：
> 

### [ro.system.build.tags]: [dev-keys]
+ 含义：
+ 代码来源：
> 

### [ro.system.build.type]: [userdebug]
+ 含义：
+ 代码来源：
> 

### [ro.system.build.version.incremental]: [11228894]
+ 含义：
+ 代码来源：
> 

### [ro.system.build.version.release]: [14]
+ 含义：
+ 代码来源：
> 

### [ro.system.build.version.release_or_codename]: [14]
+ 含义：
+ 代码来源：
> 

### [ro.system.build.version.sdk]: [34]
+ 含义：
+ 代码来源：
> 

### [ro.system.product.cpu.abilist]: [x86_64,arm64-v8a]
+ 含义：
+ 代码来源：
> 

### [ro.system.product.cpu.abilist32]: []
+ 含义：
+ 代码来源：
> 

### [ro.system.product.cpu.abilist64]: [x86_64,arm64-v8a]
+ 含义：
+ 代码来源：
> 

### [ro.system_dlkm.build.date]: [Sat Dec 16 23:01:15 UTC 2023]
+ 含义：
+ 代码来源：
> 

### [ro.system_dlkm.build.date.utc]: [1702767675]
+ 含义：
+ 代码来源：
> 

### [ro.system_dlkm.build.fingerprint]: [google/sdk_gphone64_x86_64/emu64xa:14/UE1A.230829.036.A1/11228894:userdebug/dev-keys]
+ 含义：
+ 代码来源：
> 

### [ro.system_dlkm.build.id]: [UE1A.230829.036.A1]
+ 含义：
+ 代码来源：
> 

### [ro.system_dlkm.build.tags]: [dev-keys]
+ 含义：
+ 代码来源：
> 

### [ro.system_dlkm.build.type]: [userdebug]
+ 含义：
+ 代码来源：
> 

### [ro.system_dlkm.build.version.incremental]: [11228894]
+ 含义：
+ 代码来源：
> 

### [ro.system_dlkm.build.version.release]: [14]
+ 含义：
+ 代码来源：
> 

### [ro.system_dlkm.build.version.release_or_codename]: [14]
+ 含义：
+ 代码来源：
> 

### [ro.system_dlkm.build.version.sdk]: [34]
+ 含义：
+ 代码来源：
> 

### [ro.system_ext.build.date]: [Sat Dec 16 23:01:15 UTC 2023]
+ 含义：
+ 代码来源：
> 

### [ro.system_ext.build.date.utc]: [1702767675]
+ 含义：
+ 代码来源：
> 

### [ro.system_ext.build.fingerprint]: [google/sdk_gphone64_x86_64/emu64xa:14/UE1A.230829.036.A1/11228894:userdebug/dev-keys]
+ 含义：
+ 代码来源：
> 

### [ro.system_ext.build.id]: [UE1A.230829.036.A1]
+ 含义：
+ 代码来源：
> 

### [ro.system_ext.build.tags]: [dev-keys]
+ 含义：
+ 代码来源：
> 

### [ro.system_ext.build.type]: [userdebug]
+ 含义：
+ 代码来源：
> 

### [ro.system_ext.build.version.incremental]: [11228894]
+ 含义：
+ 代码来源：
> 

### [ro.system_ext.build.version.release]: [14]
+ 含义：
+ 代码来源：
> 

### [ro.system_ext.build.version.release_or_codename]: [14]
+ 含义：
+ 代码来源：
> 

### [ro.system_ext.build.version.sdk]: [34]
+ 含义：
+ 代码来源：
> 

### [ro.test_harness]: [1]
+ 含义：
+ 代码来源：
> 

### [ro.treble.enabled]: [true]
+ 含义：
+ 代码来源：
> 

### [ro.vendor.api_level]: [34]
+ 含义：
+ 代码来源：
> 

### [ro.vendor.build.date]: [Sat Dec 16 23:01:15 UTC 2023]
+ 含义：
+ 代码来源：
> 

### [ro.vendor.build.date.utc]: [1702767675]
+ 含义：
+ 代码来源：
> 

### [ro.vendor.build.fingerprint]: [google/sdk_gphone64_x86_64/emu64xa:14/UE1A.230829.036.A1/11228894:userdebug/dev-keys]
+ 含义：
+ 代码来源：
> 

### [ro.vendor.build.id]: [UE1A.230829.036.A1]
+ 含义：
+ 代码来源：
> 

### [ro.vendor.build.security_patch]: []
+ 含义：
+ 代码来源：
> 

### [ro.vendor.build.tags]: [dev-keys]
+ 含义：
+ 代码来源：
> 

### [ro.vendor.build.type]: [userdebug]
+ 含义：
+ 代码来源：
> 

### [ro.vendor.build.version.incremental]: [11228894]
+ 含义：
+ 代码来源：
> 

### [ro.vendor.build.version.release]: [14]
+ 含义：
+ 代码来源：
> 

### [ro.vendor.build.version.release_or_codename]: [14]
+ 含义：
+ 代码来源：
> 

### [ro.vendor.build.version.sdk]: [34]
+ 含义：
+ 代码来源：
> 

### [ro.vendor.product.cpu.abilist]: [x86_64,arm64-v8a]
+ 含义：
+ 代码来源：
> 

### [ro.vendor.product.cpu.abilist32]: []
+ 含义：
+ 代码来源：
> 

### [ro.vendor.product.cpu.abilist64]: [x86_64,arm64-v8a]
+ 含义：
+ 代码来源：
> 

### [ro.vendor_dlkm.build.date]: [Sat Dec 16 23:01:15 UTC 2023]
+ 含义：
+ 代码来源：
> 

### [ro.vendor_dlkm.build.date.utc]: [1702767675]
+ 含义：
+ 代码来源：
> 

### [ro.vendor_dlkm.build.fingerprint]: [google/sdk_gphone64_x86_64/emu64xa:14/UE1A.230829.036.A1/11228894:userdebug/dev-keys]
+ 含义：
+ 代码来源：
> 

### [ro.vendor_dlkm.build.id]: [UE1A.230829.036.A1]
+ 含义：
+ 代码来源：
> 

### [ro.vendor_dlkm.build.tags]: [dev-keys]
+ 含义：
+ 代码来源：
> 

### [ro.vendor_dlkm.build.type]: [userdebug]
+ 含义：
+ 代码来源：
> 

### [ro.vendor_dlkm.build.version.incremental]: [11228894]
+ 含义：
+ 代码来源：
> 

### [ro.vendor_dlkm.build.version.release]: [14]
+ 含义：
+ 代码来源：
> 

### [ro.vendor_dlkm.build.version.release_or_codename]: [14]
+ 含义：
+ 代码来源：
> 

### [ro.vendor_dlkm.build.version.sdk]: [34]
+ 含义：
+ 代码来源：
> 

### [ro.vndk.version]: [34]
+ 含义：
+ 代码来源：
> 

### [ro.wifi.channels]: []
+ 含义：
+ 代码来源：
> 

### [ro.zygote]: [zygote64]
+ 含义：
+ 代码来源：
> 

### [ro.zygote.disable_gl_preload]: [1]
+ 含义：
+ 代码来源：
> 

### [security.perf_harden]: [1]
+ 含义：
+ 代码来源：
> 

### [selinux.restorecon_recursive]: [/data/misc_ce/0]
+ 含义：
+ 代码来源：
> 

### [service.sf.present_timestamp]: [0]
+ 含义：
+ 代码来源：
> 

### [servicemanager.ready]: [true]
+ 含义：
+ 代码来源：
> 

### [setupwizard.feature.deferred_setup_notification]: [false]
+ 含义：
+ 代码来源：
> 

### [setupwizard.feature.deferred_setup_suggestion]: [false]
+ 含义：
+ 代码来源：
> 

### [sys.boot.reason]: [reboot]
+ 含义：
+ 代码来源：
> 

### [sys.boot.reason.last]: [reboot]
+ 含义：
+ 代码来源：
> 

### [sys.boot_completed]: [1]
+ 含义：
+ 代码来源：
> 

### [sys.bootstat.first_boot_completed]: [1]
+ 含义：
+ 代码来源：
> 

### [sys.fuse.transcode_enabled]: [true]
+ 含义：
+ 代码来源：
> 

### [sys.init.perf_lsm_hooks]: [1]
+ 含义：
+ 代码来源：
> 

### [sys.rescue_boot_count]: [1]
+ 含义：
+ 代码来源：
> 

### [sys.sysctl.extra_free_kbytes]: [28096]
+ 含义：
+ 代码来源：
> 

### [sys.system_server.start_count]: [1]
+ 含义：
+ 代码来源：
> 

### [sys.system_server.start_elapsed]: [13782]
+ 含义：
+ 代码来源：
> 

### [sys.system_server.start_uptime]: [13782]
+ 含义：
+ 代码来源：
> 

### [sys.usb.config]: [adb]
+ 含义：
+ 代码来源：
> 

### [sys.usb.configfs]: [0]
+ 含义：
+ 代码来源：
> 

### [sys.usb.controller]: [dummy_udc.0]
+ 含义：
+ 代码来源：
> 

### [sys.usb.state]: [adb]
+ 含义：
+ 代码来源：
> 

### [sys.use_memfd]: [false]
+ 含义：
+ 代码来源：
> 

### [sys.user.0.ce_available]: [true]
+ 含义：
+ 代码来源：
> 

### [sys.wifitracing.started]: [1]
+ 含义：
+ 代码来源：
> 

### [vendor.qemu.sf.fake_camera]: [both]
+ 含义：
+ 代码来源：
> 

### [vendor.qemu.timezone]: [Unknown/Unknown]
+ 含义：
+ 代码来源：
> 

### [vendor.qemu.vport.bluetooth]: [/dev/vport8p2]
+ 含义：
+ 代码来源：
> 

### [vendor.qemu.vport.modem]: [/dev/vport9p1]
+ 含义：
+ 代码来源：
> 

### [vold.has_adoptable]: [1]
+ 含义：
+ 代码来源：
> 

### [vold.has_compress]: [0]
+ 含义：
+ 代码来源：
> 

### [vold.has_quota]: [1]
+ 含义：
+ 代码来源：
> 

### [vold.has_reserved]: [1]
+ 含义：
+ 代码来源：
> 


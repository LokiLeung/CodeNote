# 【Android Framewrok】Handler源码解析

![f6ff46eb9b03a9bcc634739c09bf992](./%E3%80%90Android%20Framewrok%E3%80%91Handler%E6%BA%90%E7%A0%81%E8%A7%A3%E6%9E%90.assets/f6ff46eb9b03a9bcc634739c09bf992.jpg)

> 日期：2023-06-29
>
> 学习资料：
>
> 1. [Handler.java - Android Code Search](https://cs.android.com/android/platform/superproject/+/master:frameworks/base/core/java/android/os/Handler.java;l=1?q=Handler.java&sq=&ss=android%2Fplatform%2Fsuperproject&hl=zh-cn)
> 2. [Android之Handler机制（终极篇）：面试常见问题汇总，解锁大牛的乐趣 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/269485733)
> 3. [关于Handler的20个问题 - 掘金 (juejin.cn)](https://juejin.cn/post/7026560379270463501)
> 4. [android 为什么handler不会阻塞 android handler的机制和原理_feiry的技术博客_51CTO博客](https://blog.51cto.com/u_14152/6573620#:~:text=Handler理解与常见问题 1 1、子线程到主线程通信都有哪些方式？ 子线程到主线程通信的原理？ 2 2、一个线程可以有几个Handler？ 3,3、一个线程有几个Looper？ 如何保证？ 4 4、Handler内存泄漏原因？ 为什么其他的内部类没有说过这个问题？ 5 5、使用Handler导致内存泄露的解决方法%3F)

[TOC]



## 基本流程

### Q1：初始化流程

#### 基本的使用方法

一般我们使用Handler的时候就分为以下几步：

1. Looper.prepare();
2. Looper.loop();
3. 创建Handler处理回调；
4. Handler使用post或者sendMessage方法进行异步消息的发送；

而在源码的注释中也给出了典型的用法：

1. Looper.prepare();
2. 创建Handler处理回调；
3. Looper.loop();

```java
class LooperThread extends Thread {
    public Handler mHandler;

    public void run() {
        Looper.prepare();

        mHandler = new Handler(Looper.myLooper()) {
            public void handleMessage(Message msg) {
                // process incoming messages here
                // 此处处理即将到来的消息
            }
        };

        Looper.loop();
    }
}
```



##### 根据4部分用法分析初始化流程

###### Looper.prepare();

```java
/** Initialize the current thread as a looper.
      * This gives you a chance to create handlers that then reference
      * this looper, before actually starting the loop. Be sure to call
      * {@link #loop()} after calling this method, and end it by calling
      * {@link #quit()}.
      */
public static void prepare() {
    prepare(true);
}

private static void prepare(boolean quitAllowed) {
	// Looper.prepare的时候，此线程的Looper一定是为空的，否则会抛出异常
    if (sThreadLocal.get() != null) {
        throw new RuntimeException("Only one Looper may be created per thread");
    }
    // 将这个Looper保存为线程变量，然后跟线程绑定起来
    sThreadLocal.set(new Looper(quitAllowed));
}

/**
     * Initialize the current thread as a looper, marking it as an
     * application's main looper. See also: {@link #prepare()}
     *
     * @deprecated The main looper for your application is created by the Android environment,
     *   so you should never need to call this function yourself.
     */
@Deprecated
public static void prepareMainLooper() {
    // 主线程的Looper传入的quitAllowed为false，子线程的为true
    prepare(false);
    synchronized (Looper.class) {
        if (sMainLooper != null) {
            throw new IllegalStateException("The main Looper has already been prepared.");
        }
        sMainLooper = myLooper();
    }
}

// prepare方法最终都会走到构造函数，构造函数值做了两件事：
// 1. new了一个消息队列，并且子线程的消息队列是允许退出的，主线程的消息队列是不允许退出的；
// 2. 获取当前线程；
private Looper(boolean quitAllowed) {
    mQueue = new MessageQueue(quitAllowed);
    mThread = Thread.currentThread();
}


    /**
     * Return the Looper object associated with the current thread.  Returns
     * null if the calling thread is not associated with a Looper.
     */
public static @Nullable Looper myLooper() {
    return sThreadLocal.get();
}

    /**
     * Return the {@link MessageQueue} object associated with the current
     * thread.  This must be called from a thread running a Looper, or a
     * NullPointerException will be thrown.
     */
public static @NonNull MessageQueue myQueue() {
    return myLooper().mQueue;
}
```

1. 这一步骤主要是创建Looper，将Looper保存为线程变量，与线程绑定起来；
2. 注意Looper.prepare之前线程的Looper一定是空的，否则会抛出异常；
3. 主线程的Looper是不允许退出的，子线程的可以；

###### Handler的构造

Handler有多个构造函数：

```java
@Deprecated public Handler()   // 构造函数1 废弃
    
@Deprecated public Handler(@Nullable Callback callback)   // 构造函数2 废弃
    
public Handler(@NonNull Looper looper)  // 构造函数3 最终 -》  构造函数7
    
public Handler(@NonNull Looper looper, @Nullable Callback callback) // 构造函数4 最终 -》  构造函数7
@UnsupportedAppUsage(maxTargetSdk = Build.VERSION_CODES.R, trackingBug = 170729553) public Handler(boolean async)  // 构造函数5 不开放给App 最终-》构造函数6
public Handler(@Nullable Callback callback, boolean async) // 构造函数6
@UnsupportedAppUsage public Handler(@NonNull Looper looper, @Nullable Callback callback, boolean async)  // 构造函数7 不开放给App
```

> 因为最终只会走到构造函数6、7，因此只记录6、7

Handler的构造函数6：

```java
public Handler(@Nullable Callback callback, boolean async) {
    // 检查潜在的内存泄漏
    if (FIND_POTENTIAL_LEAKS) {
        final Class<? extends Handler> klass = getClass();
        // 匿名类、成员类、局部类，并且不是静态的，警告提示（以下Handler类应该是静态的，否则可能会发生泄漏）。
        if ((klass.isAnonymousClass() || klass.isMemberClass() || klass.isLocalClass()) &&
            (klass.getModifiers() & Modifier.STATIC) == 0) {
            Log.w(TAG, "The following Handler class should be static or leaks might occur: " +
                  klass.getCanonicalName());
        }
    }

    // 获取当前线程的Looper，若Looper为空，直接抛出运行时异常
    mLooper = Looper.myLooper();
    if (mLooper == null) {
        throw new RuntimeException(
            "Can't create handler inside thread " + Thread.currentThread()
            + " that has not called Looper.prepare()");
    }
    // 获取Looper的消息队列
    mQueue = mLooper.mQueue;
    // 获取回调处理
    mCallback = callback;
    // 是否异步，默认为false
    mAsynchronous = async;
}
```

Handler的构造函数7：

```java
@UnsupportedAppUsage
public Handler(@NonNull Looper looper, @Nullable Callback callback, boolean async) {
    // 无特殊处理，只对4个变量进行一一赋值
    mLooper = looper;
    mQueue = looper.mQueue;
    mCallback = callback;
    mAsynchronous = async;
}
```

从Handler的构造函数看到：

1. Handler的构造函数主要是将Looper、callback、mQueue、mAsynchronous 4个变量进行赋值；
2. callback一般是用户自己进行处理的；looper是用户注入的，或者是通过Looper.myLooper()进行赋值的；mQueue是从Looper中获取的；mAsynchronous是用户注入的，默认为false；

###### Looper.loop()

```java
/**
 * Run the message queue in this thread. Be sure to call
 * {@link #quit()} to end the loop.
 */
@SuppressWarnings("AndroidFrameworkBinderIdentity")
public static void loop() {
    // 首先判断这个线程中是否已经有Looper存在，若不存在直接抛出异常
    final Looper me = myLooper();
    if (me == null) {
        throw new RuntimeException("No Looper; Looper.prepare() wasn't called on this thread.");
    }
    // 判断这个looper是不是已经在 inloop 状态， 再次loop将使队列中的消息在此消息完成之前被执行
    if (me.mInLoop) {
        Slog.w(TAG, "Loop again would have the queued messages be executed"
               + " before this one completed.");
    }

    // 标志这个线程的Looper为 inloop 状态
    me.mInLoop = true;

    // Make sure the identity of this thread is that of the local process,
    // and keep track of what that identity token actually is.
    // 确保这个线程的标识是本地进程的标识，并跟踪标识token实际上是什么。
    Binder.clearCallingIdentity();
    final long ident = Binder.clearCallingIdentity();

    // Allow overriding a threshold with a system prop. e.g.
    // adb shell 'setprop log.looper.1000.main.slow 1 && stop && start'
    // 允许用系统属性（adb命令）覆盖一个阈值，例如：
    // adb shell 'setprop log.looper.1000.main.slow 1 && stop && start'
    final int thresholdOverride =
        SystemProperties.getInt("log.looper."
                                + Process.myUid() + "."
                                + Thread.currentThread().getName()
                                + ".slow", 0);

    // True if a message delivery takes longer than {@link #mSlowDeliveryThresholdMs}.
    // 如果一个消息分发大于 mSlowDeliveryThresholdMs 时间， 这个状态置为true
    me.mSlowDeliveryDetected = false;

    for (;;) {
        if (!loopOnce(me, ident, thresholdOverride)) {
            return;
        }
    }
}

/**
 * Poll and deliver single message, return true if the outer loop should continue.
 * 轮询并分发每一个消息，如果外部循坏应该继续，则返回true
 */
@SuppressWarnings("AndroidFrameworkBinderIdentity")
private static boolean loopOnce(final Looper me,
                                final long ident, final int thresholdOverride) {
    // 首先获取下一个消息，并判空
    Message msg = me.mQueue.next(); // might block
    if (msg == null) {
        // No message indicates that the message queue is quitting.
        return false;
    }

    // 如果有设置打printer，就能够将Looper的东西打印出来
    // This must be in a local variable, in case a UI event sets the logger
    final Printer logging = me.mLogging;
    if (logging != null) {
        logging.println(">>>>> Dispatching to " + msg.target + " "
                        + msg.callback + ": " + msg.what);
    }
    // Make sure the observer won't change while processing a transaction.
    // 确保当处理一个事务的时候 observer 不会被改变
    final Observer observer = sObserver;

    // 获取Trace的标记
    final long traceTag = me.mTraceTag;
    // 获取消息分发阈值
    long slowDispatchThresholdMs = me.mSlowDispatchThresholdMs;
    // 获取消息交付阈值
    long slowDeliveryThresholdMs = me.mSlowDeliveryThresholdMs;
    // 有覆盖的（adb命令传入），则用覆盖的值。
    if (thresholdOverride > 0) {
        slowDispatchThresholdMs = thresholdOverride;
        slowDeliveryThresholdMs = thresholdOverride;
    }
    // 是否记录慢交付
    final boolean logSlowDelivery = (slowDeliveryThresholdMs > 0) && (msg.when > 0);
    // 是否记录慢分发
    final boolean logSlowDispatch = (slowDispatchThresholdMs > 0);
    // 是否需要获取开始时刻
    final boolean needStartTime = logSlowDelivery || logSlowDispatch;
    // 是否需要获取结束时刻
    final boolean needEndTime = logSlowDispatch;

    if (traceTag != 0 && Trace.isTagEnabled(traceTag)) {
        // 开始Trace
        Trace.traceBegin(traceTag, msg.target.getTraceName(msg));
    }

    // 分发开始时刻
    final long dispatchStart = needStartTime ? SystemClock.uptimeMillis() : 0;
    final long dispatchEnd;
    Object token = null;
    // 获取token，通知Observer消息分发开始。
    if (observer != null) {
        token = observer.messageDispatchStarting();
    }
    // 设置当前线程的Uid
    long origWorkSource = ThreadLocalWorkSource.setUid(msg.workSourceUid);
    try {
        // 通知Message的Handler进行分发消息（重要！！！）
        msg.target.dispatchMessage(msg);
        if (observer != null) {
            // 通知Observer消息分发结束
            observer.messageDispatched(token, msg);
        }
        // 分发结束，记录结束时间
        dispatchEnd = needEndTime ? SystemClock.uptimeMillis() : 0;
    } catch (Exception exception) {
        if (observer != null) {
            // 通知Observer消息分发异常
            observer.dispatchingThrewException(token, msg, exception);
        }
        throw exception;
    } finally {
        // 恢复当前线程的Uid
        ThreadLocalWorkSource.restore(origWorkSource);
        if (traceTag != 0) {
            // Trace结束
            Trace.traceEnd(traceTag);
        }
    }
    if (logSlowDelivery) {
        // 记录慢交付，如果（dispatchStart - msg.when）时间大于阈值，则进行Slog提示警告。
        if (me.mSlowDeliveryDetected) {
            if ((dispatchStart - msg.when) <= 10) {
                Slog.w(TAG, "Drained");
                me.mSlowDeliveryDetected = false;
            }
        } else {
            if (showSlowLog(slowDeliveryThresholdMs, msg.when, dispatchStart, "delivery",
                            msg)) {
                // Once we write a slow delivery log, suppress until the queue drains.
                // 一旦我们记录慢交付Log，一直持续到队列为空
                me.mSlowDeliveryDetected = true;
            }
        }
    }
    // 记录慢分发
    if (logSlowDispatch) {
        showSlowLog(slowDispatchThresholdMs, dispatchStart, dispatchEnd, "dispatch", msg);
    }

    // 记录Log
    if (logging != null) {
        logging.println("<<<<< Finished to " + msg.target + " " + msg.callback);
    }

    // Make sure that during the course of dispatching the
    // identity of the thread wasn't corrupted.
    // 确保在分发过程中线程的标识没有损坏。
    final long newIdent = Binder.clearCallingIdentity();
    if (ident != newIdent) {
        // 已损坏，提示。
        Log.wtf(TAG, "Thread identity changed from 0x"
                + Long.toHexString(ident) + " to 0x"
                + Long.toHexString(newIdent) + " while dispatching to "
                + msg.target.getClass().getName() + " "
                + msg.callback + " what=" + msg.what);
    }
    // 回收消息（不检查，直接回收）
    msg.recycleUnchecked();

    return true;
}
```

Lopper.loop()会将开启一个死循环，然后进行每一次消息的分发与交付。其中loop()和loopOnce()中为Debug做了一些Trace、记录开始结束时间等操作。

> 其实loop方法做的操作不是很多，只是多了Trace、Log、stats等相关的系统调试代码，如果要调试framework的时候，这些方法可以好好利用起来。

###### Handler发送消息

Handler发送消息有2种方式：

1. post

   1. post方法包括：

      ```java
      public final boolean post(@NonNull Runnable r)
      public final boolean postAtTime(@NonNull Runnable r, long uptimeMillis)
      public final boolean postAtTime(@NonNull Runnable r, @Nullable Object token, long uptimeMillis)
      public final boolean postDelayed(@NonNull Runnable r, long delayMillis)
      public final boolean postDelayed(Runnable r, int what, long delayMillis)
      public final boolean postDelayed(@NonNull Runnable r, @Nullable Object token, long delayMillis)
      public final boolean postAtFrontOfQueue(@NonNull Runnable r)
      ```

   2. post的本质也是sendMessage

      ```java
          public final boolean post(@NonNull Runnable r) {
              // 其中里面的Message通过Message getPostMessage(Runnable r)或者Message getPostMessage(Runnable r, Object token)方法获取
             return  sendMessageDelayed(getPostMessage(r), 0);
          }
      
      ```

      ```java
          @UnsupportedAppUsage
          private static Message getPostMessage(Runnable r, Object token) {
      	    // Message也是通过obtain获取，然后对消息进行复用的
              Message m = Message.obtain();
              m.obj = token;
              m.callback = r;
              return m;
          }
      ```

   3. 不要随便使用boolean postAtFrontOfQueue(@NonNull Runnable r)

      ```java
      /**
           * Posts a message to an object that implements Runnable.
           * Causes the Runnable r to executed on the next iteration through the
           * message queue. The runnable will be run on the thread to which this
           * handler is attached.
           * <b>This method is only for use in very special circumstances -- it
           * can easily starve the message queue, cause ordering problems, or have
           * other unexpected side-effects.
           * 此方法仅适用于非常特殊的情况 - 它很容易使消息队列匮乏，
           * 导致排序问题或产生其他意外的副作用。</b>
           *  
           * @param r The Runnable that will be executed.
           * 
           * @return Returns true if the message was successfully placed in to the 
           *         message queue.  Returns false on failure, usually because the
           *         looper processing the message queue is exiting.
           */
          public final boolean postAtFrontOfQueue(@NonNull Runnable r) {
              return sendMessageAtFrontOfQueue(getPostMessage(r));
          }
      ```

      

2. sendMessage

   1. sendMessage方法包括：

      ```java
      boolean sendMessage(@NonNull Message msg) 
      boolean sendEmptyMessage(int what)
      boolean sendEmptyMessageDelayed(int what, long delayMillis)
      boolean sendEmptyMessageAtTime(int what, long uptimeMillis)
      boolean sendMessageDelayed(@NonNull Message msg, long delayMillis)
      boolean sendMessageAtTime(@NonNull Message msg, long uptimeMillis)
      boolean sendMessageAtFrontOfQueue(@NonNull Message msg)
      ```

   2. 所有上面的方法，最终都会走到sendMessageAtTime

      ```java
      public final boolean sendMessageAtFrontOfQueue(@NonNull Message msg) {
          // 把队列赋值给局部变量
          MessageQueue queue = mQueue;
          if (queue == null) {
              // 如果队列为空，直接抛出运行时异常
              RuntimeException e = new RuntimeException(
                  this + " sendMessageAtTime() called with no mQueue");
              Log.w("Looper", e.getMessage(), e);
              return false;
          }
          return enqueueMessage(queue, msg, 0);
      }
      
      
      
      private boolean enqueueMessage(@NonNull MessageQueue queue, @NonNull Message msg,
                                      long uptimeMillis) {
           // 将msg的Target和UID、是否异步补充，调用MessageQueue的enqueueMessage
           // enqueue 入列
           msg.target = this;
           msg.workSourceUid = ThreadLocalWorkSource.getUid();
       
           if (mAsynchronous) {
               msg.setAsynchronous(true);
           }
      	// 而sendMessageAtTime最终是调用了MessageQueue的enqueueMessage入列方法；
          return queue.enqueueMessage(msg, uptimeMillis);
       }
      ```

3. MessageQueue的enqueueMessage入队方法：

4.  ```java
    boolean enqueueMessage(Message msg, long when) {
        // 如果Target为空，直接抛异常
        if (msg.target == null) {
            throw new IllegalArgumentException("Message must have a target.");
        }
    
        // 这里加了handler的锁
        synchronized (this) {
            // 如果消息正在使用，抛异常
            if (msg.isInUse()) {
                throw new IllegalStateException(msg + " This message is already in use.");
            }
    
            // 如果正在退出，打Log，然后回收消息
            if (mQuitting) {
                IllegalStateException e = new IllegalStateException(
                    msg.target + " sending message to a Handler on a dead thread");
                Log.w(TAG, e.getMessage(), e);
                msg.recycle();
                return false;
            }
    
            // 标志消息使用中，将传过来的时间当做消息时间
            msg.markInUse();
            msg.when = when;
            // 拿到正在使用的message，即队头
            Message p = mMessages;
            boolean needWake;
            // p等于空说明队列是空的
            // when等于0表示强制把此消息插入队列头部，最先处理
            // when小于队列头的when说明此消息应该被处理的时间比队列中第一个要处理的时间还早
            // 以上情况满足任意一种直接将消息插入队列头部
            if (p == null || when == 0 || when < p.when) {
                // New head, wake up the event queue if blocked.
                msg.next = p;
                mMessages = msg;
                needWake = mBlocked;
            } else {
                // Inserted within the middle of the queue.  Usually we don't have to wake
                // up the event queue unless there is a barrier at the head of the queue
                // and the message is the earliest asynchronous message in the queue.
                // 线程已经被阻塞&&消息存在宿主Handler&&消息是异步的
                needWake = mBlocked && p.target == null && msg.isAsynchronous();
                //如果上述条件都不满足就要按照消息应该被处理的时间插入队列中    
                Message prev;
                // 这段是队列入队的写法
                for (;;) {
                    // 两根相邻的引用一前一后从队列头开始依次向后移动
                    prev = p;
                    p = p.next;
                    // 如果队列到尾部了或者找到了处理时间早于自身的消息就结束循环
                    if (p == null || when < p.when) { 
                        break;
                    }
                    // 如果入队的消息是异步的而排在它前面的消息有异步的就不需要唤醒
                    if (needWake && p.isAsynchronous()) {
                        needWake = false;
                    }
                }
                msg.next = p; // invariant: p == prev.next
                prev.next = msg;
            }
    
            // We can assume mPtr != 0 because mQuitting is false.
            // 判断是否需要唤醒线程
            if (needWake) {
                nativeWake(mPtr);
            }
        }
        return true;
    }
    ```

5. 这里的的MessageQueue从一开始是从Looper中获取过来的，所以Handler的消息其实是塞到了Looper里面的MessageQueue中。之前在Loop.loop提到，loop会开启一个死循环进行轮询，当轮询到了消息之后，就会进行分发；

6. 至此，Handler从初始化、发送到回调的整个流程已经结束。

###### 总结

Handler用简单的话概括：

Looper开启了一个轮询消息队列，不断相对应的Handler进行分发消息的功能，而不同的Handler会对其进行发送消息，将消息塞到Looper的消息队列中。



## 常见问题

上面只是了解了一下最基础的用法，继续学习网上的一些常见问题

### Q1: 主线程为什么不用初始化Looper?

主线程在ActivityThread的类中已经调用，因此不需要手动调用Looper.prepare()；

> 这里先不深究main方法的调用时机了，这部分在研究App启动流程的时候再学习

```java
public static void main(String[] args) {
    Trace.traceBegin(Trace.TRACE_TAG_ACTIVITY_MANAGER, "ActivityThreadMain");

    //...

    Looper.prepareMainLooper();

    //...
    throw new RuntimeException("Main thread loop unexpectedly exited");
}
```



### Q2：为什么主线程的Looper是一个死循环，但是却不会ANR？

> 参考：[深入理解Handler(四) --- 主线程的Looper为什么不会导致应用的ANR_handler的阻塞为什么不会导致app anr_soso密斯密斯的博客-CSDN博客](https://blog.csdn.net/qq_38366777/article/details/108956270)

分析的步骤：

1. 了解ANR的概念： 

   1. ANR 是Application Not Responding的简称；
   2. ANR类型：
      1. 服务超时 前台服务20s，后台服务200s
      2. 广播超时 前台广播10s，后台广播60s
      3. ContentProvider超时 10s
      4. 输入事件超时 5s

2. ANR产生原因：

   1. 以Service为例，ContextWrapper::startService最终会走到ActiveServices::scheduleServiceTimeoutLocked，此处会对ANR发送延时消息；
      ```java
          // How long we wait for a service to finish executing.
          static final int SERVICE_TIMEOUT = 20*1000;
      
          // How long we wait for a service to finish executing.
          static final int SERVICE_BACKGROUND_TIMEOUT = SERVICE_TIMEOUT * 10;
          void scheduleServiceTimeoutLocked(ProcessRecord proc) {
              if (proc.executingServices.size() == 0 || proc.thread == null) {
                  return;
              }
              Message msg = mAm.mHandler.obtainMessage(
                      ActivityManagerService.SERVICE_TIMEOUT_MSG);
              msg.obj = proc;
              mAm.mHandler.sendMessageDelayed(msg,
                      proc.execServicesFg ? SERVICE_TIMEOUT : SERVICE_BACKGROUND_TIMEOUT);
          }
      ```

   2. 如果走到ActiveServices::serviceDoneExecutingLocked，就会将消息remove；
      ```java
       private void serviceDoneExecutingLocked(ServiceRecord r, boolean inDestroying,
                  boolean finishing) {
                    ...
      mAm.mHandler.removeMessages(ActivityManagerService.SERVICE_TIMEOUT_MSG, r.app);
               ...
                  }
      ```

   3. 消息最终分发到ActivityManagerService::MainHandler::handleMessage
      ```java
       final class MainHandler extends Handler {
          @Override
              public void handleMessage(Message msg) {
                  switch (msg.what) {
                  ...
                     case SERVICE_FOREGROUND_TIMEOUT_MSG: {
                      mServices.serviceForegroundTimeout((ServiceRecord)msg.obj);
                  } break;
                     ...  
                  }}
       }
      ```

   4. ActiveServices::serviceForegroundTimeout里调用了ANR方法
      ```java
      void serviceForegroundTimeout(ServiceRecord r) {
              ProcessRecord app;
              synchronized (mAm) {
                  if (!r.fgRequired || r.destroying) {
                      return;
                  }
      
                  app = r.app;
                  if (app != null && app.debugging) {
                      // The app's being debugged; let it ride
                      return;
                  }
      
                  if (DEBUG_BACKGROUND_CHECK) {
                      Slog.i(TAG, "Service foreground-required timeout for " + r);
                  }
                  r.fgWaiting = false;
                  stopServiceLocked(r);
              }
      
              if (app != null) {
                  mAm.mAppErrors.appNotResponding(app, null, null, false,
                          "Context.startForegroundService() did not then call Service.startForeground(): "
                              + r);
              }
          }
      ```

   5. AppErrors::appNotResponding
      ```java
         final void appNotResponding(ProcessRecord app, ActivityRecord activity,
                  ActivityRecord parent, boolean aboveSystem, final String annotation) {
                      ...
                       // Set the app's notResponding state, and look up the errorReportReceiver
                  makeAppNotRespondingLocked(app,
                          activity != null ? activity.shortComponentName : null,
                          annotation != null ? "ANR " + annotation : "ANR",
                          info.toString());
      
                  // Bring up the infamous App Not Responding dialog
                  Message msg = Message.obtain();
                  msg.what = ActivityManagerService.SHOW_NOT_RESPONDING_UI_MSG;
                  msg.obj = new AppNotRespondingDialog.Data(app, activity, aboveSystem);
      
                  mService.mUiHandler.sendMessage(msg);
                  }
      ```

   6. 简而言之，ANR的实现实际就是一个消息的处理，当service启动的时候，发送延时消息，消息会在服务启动完后回收，如果消息在20s/200s后仍未回收，则做ANR处理。

3. 以此看来，ANR只是一个消息发送与处理过程，依赖于Looper机制，ANR与Looper完全是两个概念，因此不会造成主线程ANR；

### Q3：Handler如何保证MessageQueue并发访问安全？

> 《Java并发编程》中对线程安全的定义：
>
> 当多个线程访问一个对象时，如果不用考虑这些线程在运行时环境下的调度和交替执行，也不需要进行额外的同步，或者在调用方进行任何其他的协调操作，调用这个对象的行为都可以获得正确的结果，那这个对象就是线程安全的。
>
> 原子性、可见性、有序性
>
> 具体锁的实现和逻辑，后续学习。

> 参考：
>
> [Android之Handler机制（终极篇）：面试常见问题汇总，解锁大牛的乐趣 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/269485733)
>
> [Android 中 MessageQueue 的 nativePollOnce - just_yang - 博客园 (cnblogs.com)](https://www.cnblogs.com/jiy-for-you/p/11707356.html)
>
> **答：循环加锁，配合阻塞唤醒机制。**
>
> 我们可以发现MessageQueue其实是“生产者-消费者”模型，Handler不断地放入消息，Looper不断地取出，这就涉及到死锁问题。如果Looper拿到锁，但是队列中没有消息，就会一直等待，而Handler需要把消息放进去，锁却被Looper拿着无法入队，这就造成了死锁。Handler机制的解决方法是**循环加锁**。在MessageQueue的next方法中：
>
> ```kotlin
> Message next() {
>    ...
>     for (;;) {
>   ...
>         nativePollOnce(ptr, nextPollTimeoutMillis);
>         synchronized (this) {
>             ...
>         }
>     }
> }
> ```
>
> 我们可以看到他的等待是在锁外的，当队列中没有消息的时候，他会先释放锁，再进行等待，直到被唤醒。这样就不会造成死锁问题了。
>
> 那在入队的时候会不会因为队列已经满了然后一边在等待消息处理一边拿着锁呢？这一点不同的是MessageQueue的消息没有上限，或者说他的上限就是JVM给程序分配的内存，如果超出内存会抛出异常，但一般情况下是不会的。

### Q4：Handler是如何切换线程的？

在创建Handler的时候传入了Looper，Looper是与线程一一对应的。

Handler发送消息的时候可以在任意一个线程，但是最终塞入的消息队列是保存在Looper中，Looper轮询消息队列，一直处于本来的线程。

### Q5：Handler的阻塞唤醒机制是怎么回事？

Handler的阻塞唤醒机制是基于Linux的阻塞唤醒机制。

> 参考：[java - android - what is message queue native poll once in android? - Stack Overflow](https://stackoverflow.com/questions/38818642/android-what-is-message-queue-native-poll-once-in-android)
>
> 因为主线程负责绘制 UI 和处理各种事件, 所以主线程拥有一个处理所有这些事件的循环. 该循环由 `Looper` 管理, 其工作非常简单: 它处理 `MessageQueue` 中的所有 `Message`.
> 例如, 响应于输入事件, 将消息添加到队列, 帧渲染回调, 甚至您的 `Handler.post` 调用. 有时主线程无事可做（即队列中没有消息), 例如在完成渲染单帧之后(线程刚绘制了一帧, 并准备好下一帧, 等待适当的时间). 
>
> `MessageQueue` 类中的两个 Java 方法对我们很有趣: `Message next()`和 `boolean enqueueMessage(Message, long)`. 顾名思义, `Message next()` 从队列中获取并返回下一个消息. 如果队列为空(无返回值), 则该方法将调用 `native void nativePollOnce(long, int)`, 该方法将一直阻塞直到添加新消息为止. 此时,您可能会问`nativePollOnce` 如何知道何时醒来. 这是一个很好的问题. 当将 `Message` 添加到队列时, 框架调用 `enqueueMessage` 方法, 该方法不仅将消息插入队列, 而且还会调用`native static void nativeWake(long)`.
>
>  `nativePollOnce` 和 `nativeWake` 的核心魔术发生在 native 代码中. native `MessageQueue` 利用名为 `epoll` 的 Linux 系统调用, 该系统调用可以监视文件描述符中的 IO 事件. `nativePollOnce` 在某个文件描述符上调用 `epoll_wait`, 而 `nativeWake` 写入一个 IO 操作到描述符, `epoll_wait` 等待. 然后, 内核从等待状态中取出 `epoll` 等待线程, 并且该线程继续处理新消息. 如果您熟悉 Java 的 `Object.wait()`和 `Object.notify()`方法,可以想象一下 `nativePollOnce` 大致等同于 `Object.wait()`, `nativeWake` 等同于 `Object.notify()`,但它们的实现完全不同: `nativePollOnce` 使用 `epoll`, 而 `Object.wait` 使用 `futex` Linux 调用. 
>
> 值得注意的是, `nativePollOnce` 和 `Object.wait` 都不会浪费 CPU 周期, 因为当线程进入任一方法时, 出于线程调度的目的, 该线程将被禁用(引用Object类的javadoc). 但是, 某些事件探查器可能会错误地将等待 `epoll` 等待(甚至是 Object.wait)的线程识别为正在运行并消耗 CPU 时间, 这是不正确的. 如果这些方法实际上浪费了 CPU 周期, 则所有空闲的应用程序都将使用 100％ 的 CPU, 从而加热并降低设备速度.

### Q6：能不能让一个Message加急被处理？/ 什么是Handler同步屏障？

**答：可以 / 一种使得异步消息可以被更快处理的机制**

##### 何为同步屏障？

message分为**同步消息**、**异步消息**、**屏障消息**；

通常使用Handler发出去的消息均为同步消息，一般情况下，同步消息和异步消息的处理没有区别。但是设置了同步屏障后，所有的同步消息会被屏蔽，不能被执行，异步消息可以被执行。

##### 如何插入同步屏障？

同步屏障使用`MessageQueue`中的`postSyncBarrier()`进行插入，`postSyncBarrier()`是一个隐藏方法，使用的时候需要反射调用。返回的int类型值是一个可以用来移除屏障的token。

```java
public int postSyncBarrier() {
    return postSyncBarrier(SystemClock.uptimeMillis());
}
```
```java
private int postSyncBarrier(long when) {
    synchronized (this) {
        final int token = mNextBarrierToken++;
        final Message msg = Message.obtain();
        msg.markInUse();
        msg.when = when;
        msg.arg1 = token;
 
        Message prev = null;
        Message p = mMessages;
        // 把当前需要执行的Message全部执行
        if (when != 0) {
            while (p != null && p.when <= when) {
                prev = p;
                p = p.next;
            }
        }
        // 插入同步屏障，注意这里消息屏障是不会将handler写入到message的
        if (prev != null) { // invariant: p == prev.next
            msg.next = p;
            prev.next = msg;
        } else {
            msg.next = p;
            mMessages = msg;
        }
        return token;
    }
}
```



##### 如何发送异步消息？

+ 第一种：直接使用异步Handler，在Handler构造参数将async设为true；
```java
public Handler(@Nullable Callback callback, boolean async)
```
+ 第二种：通过message.setAsynchronous(boolean async)将消息设置为异步消息；
```java
 public void setAsynchronous(boolean async) {
        if (async) {
            flags |= FLAG_ASYNCHRONOUS;
        } else {
            flags &= ~FLAG_ASYNCHRONOUS;
        }
    }
```

##### 消息的处理过程

我们来看看Handler中的mAsynchronous字段有什么作用？
在Handler的源码中可以看到，如果mAsynchronous = true，实际也是在塞入消息队列的时候，调用了message.setAsynchronous(boolean async)方法；
```java
    private boolean enqueueMessage(@NonNull MessageQueue queue, @NonNull Message msg,
            long uptimeMillis) {
        // 将msg的Target和UID、是否异步补充，调用MessageQueue的enqueueMessage
        // enqueue 入列
        msg.target = this;
        msg.workSourceUid = ThreadLocalWorkSource.getUid();
        if (mAsynchronous) {
            msg.setAsynchronous(true);
        }
        return queue.enqueueMessage(msg, uptimeMillis);
    }
```

而Message中对此字段只提供了简单的get、set方法，在MessageQueue中，我们看看next方法中是怎么利用这个异步标志位的。

```java
 @UnsupportedAppUsage
    Message next() {
        // ... 此处省略
        for (;;) {
            if (nextPollTimeoutMillis != 0) {
                Binder.flushPendingCommands();
            }

            nativePollOnce(ptr, nextPollTimeoutMillis);

            synchronized (this) {
                // Try to retrieve the next message.  Return if found.
                final long now = SystemClock.uptimeMillis();
                Message prevMsg = null;
                Message msg = mMessages;
                // 此处是一个消息屏障，只有消息屏障才会没有target
                // 当有消息屏障的时候，优先寻找队列中的异步消息
                if (msg != null && msg.target == null) {
                    // Stalled by a barrier.  Find the next asynchronous message in the queue.
                    do {
                        prevMsg = msg;
                        msg = msg.next;
                    } while (msg != null && !msg.isAsynchronous());
                }
                // 如果有消息屏障，这里就是找到了下一个的异步消息；
                // 如果没有消息屏障，这里就是找到了下一个消息，同步消息和异步消息没有差异。
                // 这样子在有消息屏障的情况下，异步消息就会被处理，而同步消息不会进行处理。
                if (msg != null) {
                    if (now < msg.when) {
                        // Next message is not ready.  Set a timeout to wake up when it is ready.
                        nextPollTimeoutMillis = (int) Math.min(msg.when - now, Integer.MAX_VALUE);
                    } else {
                        // Got a message.
                        mBlocked = false;
                        if (prevMsg != null) {
                            prevMsg.next = msg.next;
                        } else {
                            mMessages = msg.next;
                        }
                        msg.next = null;
                        if (DEBUG) Log.v(TAG, "Returning message: " + msg);
                        msg.markInUse();
                        return msg;
                    }
                } else {
                    // No more messages.
                    nextPollTimeoutMillis = -1;
                }

                // Process the quit message now that all pending messages have been handled.
                if (mQuitting) {
                    dispose();
                    return null;
                }
            }
        }
    }

```

**注意，同步屏障不会自动移除，使用完成之后需要手动进行移除，不然会造成同步消息无法被处理**。从源码中可以看到如果不移除同步屏障，那么他会一直在那里，这样同步消息就永远无法被执行了。

有了同步屏障，那么唤醒的判断条件就必须再加一个：**MessageQueue中有同步屏障且处于阻塞中，此时插入在所有异步消息前插入新的异步消息**。这个也很好理解，跟同步消息是一样的。如果把所有的同步消息先忽视，就是插入新的链表头且队列处于阻塞状态，这个时候就需要被唤醒了。看一下源码：

```java
boolean enqueueMessage(Message msg, long when) {
    ...
 
    // 对MessageQueue进行加锁
    synchronized (this) {
        ...
        if (p == null || when == 0 || when < p.when) {
            msg.next = p;
            mMessages = msg;
            needWake = mBlocked;
        } else {
            /**
            * 1
            */
            // 当线程被阻塞，且目前有同步屏障，且入队的消息是异步消息
            needWake = mBlocked && p.target == null && msg.isAsynchronous();
            Message prev;
            for (;;) {
                prev = p;
                p = p.next;
                if (p == null || when < p.when) {
                    break;
                }
                /**
                * 2
                */
                // 如果找到一个异步消息，说明前面有延迟的异步消息需要被处理，不需要被唤醒
                if (needWake && p.isAsynchronous()) {
                    needWake = false;
                }
            }
            msg.next = p; 
            prev.next = msg;
        }
  
        // 如果需要则唤醒队列
        if (needWake) {
            nativeWake(mPtr);
        }
    }
    return true;
}
```

同样，这个方法我之前讲过，把无关同步屏障的代码忽视，看到注释1处的代码。如果插入的消息是异步消息，且有同步屏障，同时MessageQueue正处于阻塞状态，那么就需要唤醒。而如果这个异步消息的插入位置不是所有异步消息之前，那么不需要唤醒，如注释2。

**但是！！！！**，其实同步屏障对于我们的日常使用的话其实是没有多大用处。因为设置同步屏障和创建异步Handler的方法都是标志为hide，说明谷歌不想要我们去使用他。所以这里同步屏障也作为一个了解，可以更加全面地理解源码中的内容。

> 参考：
>
> + [Android之Handler机制（终极篇）：面试常见问题汇总，解锁大牛的乐趣 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/269485733)
> + [什么是Handler的同步屏障机制？ - 掘金 (juejin.cn)](https://juejin.cn/post/6971981915934949390#heading-2)

### Q7：什么是IdleHandler？

答： 当MessageQueue为空或者目前没有需要执行的Message时会回调的接口对象。

IdleHandler看起来好像是个Handler，但他其实只是一个有单方法的接口，也称为函数型接口：

```kotlin
public static interface IdleHandler {
    boolean queueIdle();
}
```

在MessageQueue中有一个List存储了IdleHandler对象，当MessageQueue没有需要被执行的Message时就会遍历回调所有的IdleHandler。所以IdleHandler主要用于在消息队列空闲的时候处理一些**轻量级**的工作。

IdleHandler的调用是在next方法中：

```kotlin
Message next() {
    // 如果looper已经退出了，这里就返回null
    final long ptr = mPtr;
    if (ptr == 0) {
        return null;
    }
 
    // IdleHandler的数量
    int pendingIdleHandlerCount = -1; 
    // 阻塞时间
    int nextPollTimeoutMillis = 0;
    for (;;) {
        if (nextPollTimeoutMillis != 0) {
            Binder.flushPendingCommands();
        }
        // 阻塞对应时间 
        nativePollOnce(ptr, nextPollTimeoutMillis);
  // 对MessageQueue进行加锁，保证线程安全
        synchronized (this) {
            final long now = SystemClock.uptimeMillis();
            Message prevMsg = null;
            Message msg = mMessages;
            if (msg != null && msg.target == null) {
                // 同步屏障，找到下一个异步消息
                do {
                    prevMsg = msg;
                    msg = msg.next;
                } while (msg != null && !msg.isAsynchronous());
            }
            if (msg != null) {
                if (now < msg.when) {
                    // 下一个消息还没开始，等待两者的时间差
                    nextPollTimeoutMillis = (int) Math.min(msg.when - now, Integer.MAX_VALUE);
                } else {
                    // 获得消息且现在要执行，标记MessageQueue为非阻塞
                    mBlocked = false;
                    // 一般只有异步消息才会从中间拿走消息，同步消息都是从链表头获取
                    if (prevMsg != null) {
                        prevMsg.next = msg.next;
                    } else {
                        mMessages = msg.next;
                    }
                    msg.next = null;
                    msg.markInUse();
                    return msg;
                }
            } else {
                // 没有消息，进入阻塞状态
                nextPollTimeoutMillis = -1;
            }
 
            // 当调用Looper.quitSafely()时候执行完所有的消息后就会退出
            if (mQuitting) {
                dispose();
                return null;
            }
 
            // 当队列中的消息用完了或者都在等待时间延迟执行同时给pendingIdleHandlerCount<0
            // 给pendingIdleHandlerCount赋值MessageQueue中IdleHandler的数量
            if (pendingIdleHandlerCount < 0
                    && (mMessages == null || now < mMessages.when)) {
                pendingIdleHandlerCount = mIdleHandlers.size();
            }
            // 没有需要执行的IdleHanlder直接continue
            if (pendingIdleHandlerCount <= 0) {
                // 执行IdleHandler，标记MessageQueue进入阻塞状态
                mBlocked = true;
                continue;
            }
 
            // 把List转化成数组类型
            if (mPendingIdleHandlers == null) {
                mPendingIdleHandlers = new IdleHandler[Math.max(pendingIdleHandlerCount, 4)];
            }
            mPendingIdleHandlers = mIdleHandlers.toArray(mPendingIdleHandlers);
        }
 
        // 执行IdleHandler
        for (int i = 0; i < pendingIdleHandlerCount; i++) {
            final IdleHandler idler = mPendingIdleHandlers[i];
            mPendingIdleHandlers[i] = null; // 释放IdleHandler的引用
            boolean keep = false;
            try {
                keep = idler.queueIdle();
            } catch (Throwable t) {
                Log.wtf(TAG, "IdleHandler threw exception", t);
            }
            // 如果返回false，则把IdleHanlder移除
            if (!keep) {
                synchronized (this) {
                    mIdleHandlers.remove(idler);
                }
            }
        }
 
        // 最后设置pendingIdleHandlerCount为0，防止再执行一次
        pendingIdleHandlerCount = 0;
 
        // 当在执行IdleHandler的时候，可能有新的消息已经进来了
        // 所以这个时候不能阻塞，要回去循环一次看一下
        nextPollTimeoutMillis = 0;
    }
}
```

代码很多，可能看着有点乱，我梳理一下逻辑，然后再回去看源码就会很清晰了：

1. 当调用next方法的时候，会给`pendingIdleHandlerCount`赋值为-1
2. 如果队列中没有需要处理的消息的时候，就会判断`pendingIdleHandlerCount`是否为`<0`，如果是则把存储IdleHandler的list的长度赋值给`pendingIdleHandlerCount`
3. 把list中的所有IdleHandler放到数组中。这一步是为了不让在执行IdleHandler的时候List被插入新的IdleHandler，造成逻辑混乱
4. 然后遍历整个数组执行所有的IdleHandler
5. 最后给`pendingIdleHandlerCount`赋值为0。然后再回去看一下这个期间有没有新的消息插入。因为`pendingIdleHandlerCount`的值为0不是-1，所以IdleHandler只会在空闲的时候执行一次
6. 同时注意，如果IdleHandler返回了false，那么执行一次之后就被丢弃了。

> 参考：
> + [Android之Handler机制（终极篇）：面试常见问题汇总，解锁大牛的乐趣 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/269485733)

### Q8：一个线程可以有几个Handler？

多个，Handler在很多地方都可以创建。

### Q9：Handler内存泄漏原因？为什么其他的内部类没有说过这个问题？

内部类持有对外部类的引用。

```java
Handler handler = new Handler() {

    @Override
    public void handleMessage(Message msg) {
        MainActivity.this.click();
        //click();
    }
};

public void click(){
    ...
}
```

类似上述的代码，会引起内存泄漏。Handler中使用click()方法，默认对外部MainActivity.this进行引用。

即便onDestroy的时候进行释放，也无法进行回收，因为在Java进行释放的时候，会对引用进行可达性分析。

具体引用的流程：Handler默认持有MainActivity.this的引用： Handler发送消息 -> Handler源码中将Handler.this赋值给Mesasge.target -> msg对handler持有引用 -> msg进入消息队列 -> looper还没有处理次消息的时候，一直会持有对这个msg的引用，msg也一直会对mainActivity持有引用 -> Activity销毁了，但是在消息分发之前，msg一直持有activity的引用 -> 内存泄漏

### Q10： 使用Handler导致内存泄露的解决方法?

方法1：静态内部类 + 弱引用
```java
static class MyHandler extends Handler {
    @Override
    public void handleMessage(Message msg) {
        // ...
    }
}

static class MyHandler extends Handler {
    WeakReference<Activity > mActivityReference;

    MyHandler(Activity activity) {
        mActivityReference= new WeakReference<Activity>(activity);
    }

    @Override
    public void handleMessage(Message msg) {
        final Activity activity = mActivityReference.get();
        if (activity != null) {
            //...
        }
    }
}
/* 弱引用的特点： 在垃圾回收器一旦发现了只具有弱引用的对象，不管当前内存空间足够与否，都会回收它的内存。 所以用户在关闭 Activity 之后，就算后台线程还没结束，但由于仅有一条来自 Handler 的弱引用指向 Activity，Activity 也会被回收掉。这样，内存泄露的问题就不会出现了。*/
```



方法2：onDestroy的时候，移除所有消息

```java
@Override
protected void onDestroy() {
    super.onDestroy();
    if (mHandler != null)  {
        mHandler.removeCallbacksAndMessages(null);
    }
}
```



### Q11： 为何主线程可以new Handler？如果想要在子线程中new Handler要做些哪些准备？

1. 主线程可以直接new Handler 是因为 在 ActivityThread 中已经调用 Looper.prepareMainLooper();
2. 在子线程调用，需要先调用Looper.prepare(); Looper.loop(); 再进行new Handler();

### Q12： Android为什么只能通过Handler机制更新UI？



### Q13： ThreadLocal的作用？

> 在Java的多线程并发执行过程中，为了保证多个线程对变量的安全访问，可以将变量放到ThreadLocal类型的对象中，使变量在每个线程中都有独立值，不会出现一个线程读取变量时被另一个线程修改的现象。
>
> ThreadLocal类通常被翻译为“线程本地变量”类或者“线程局部变量”类。

每个线程有自己的变量副本，称为线程局部变量。以此保证Looper与线程一一对应。

### Q14： 使用handler发送消息实现定时器时候，removeCallBack方法失效，是什么原因？

### Q15： 主线程 Main Looper 和一般 Looper 的异同？

异：

1. MainLooper不可以quit，其他线程的Looper可以；

   > 主线程需要不断读取系统消息和用书输入，是进程的入口，只可被系统直接终止。进而其 Looper 在创建的时候设置了不可 quit 的标志，而其他线程的 Looper 则可以也必须手动 quit

2. MainLooper实例可以被静态缓存；

   > 为了便于每个线程获得主线程 Looper 实例，见 Looper#getMainLooper()，Main Looper 实例还作为 sMainLooper 属性缓存到了 Looper 类中。

同：

1. 都是通过 Looper#prepare() 间接调用 Looper 构造函数创建的实例
2. 都被静态实例 ThreadLocal 管理，方便每个线程获取自己的 Looper 实例

### Q16： Looper 存在哪？如何可以保证线程独有？

使用ThreadLocal，将Looper保存在线程局部变量中，以此保证线程独有。

### Q17：Looper死循环为什么不会导致CPU占用率过高

> 参考：[深入理解Handler(四) --- 主线程的Looper为什么不会导致应用的ANR_handler的阻塞为什么不会导致app anr_soso密斯密斯的博客-CSDN博客](https://blog.csdn.net/qq_38366777/article/details/108956270)

```C++
- Looper.cpp
struct epoll_event eventItems[EPOLL_MAX_EVENTS];
   //等待事件发生或者超时，在nativeWake()方法，向管道写端写入字符，则该方法会返回；
int eventCount = epoll_wait(mEpollFd.get(), eventItems, EPOLL_MAX_EVENTS, timeoutMillis);
```

```C++
   // Allocate the new epoll instance and register the wake pipe.
mEpollFd.reset(epoll_create1(EPOLL_CLOEXEC));
int result = epoll_ctl(mEpollFd.get(), EPOLL_CTL_ADD, mWakeEventFd.get(), &eventItem);
```

在消息队列空的时候，会调用 epoll_wait，会等待文件的消息，文件有消息后，才会唤醒。阻塞是不会消耗CPU的时间片，不会导致CPU占用率高。这一点大家要理清楚。

##### 其他的一些问题

上面学习了整个Handler机制的流程，接下来了解下每个类里面的一些方法等。

1. 异步Handler有什么用？
2. Mesage的obtain机制有什么说法？
3. LooperStats的数据如何作用于debug？
4. 如何使用Handler、Looper等里面的调试方法？





## 其他问题

#### Q1：FIND_POTENTIAL_LEAKS字段有什么用？

FIND_POTENTIAL_LEAKS 字段的作用是用于在 Handler 源码中的一些位置进行条件编译。当该字段为 true 时，会启用与潜在内存泄漏相关的额外代码，以用于辅助检测和调试潜在的问题。在发布版本中，该字段会被设置为 false，以避免不必要的性能开销。

对于应用开发者来说，无法直接通过代码来开启或关闭 FIND_POTENTIAL_LEAKS 功能。这个字段是由 Android 源代码管理的，并且只能在 Android 源代码的构建过程中进行设置。

因此，如果你希望开启 FIND_POTENTIAL_LEAKS 功能，可以尝试构建和运行带有调试模式的 Android 源代码版本，以便获得潜在内存泄漏的警告信息。然而，在实际的应用程序开发中，我们通常不需要直接操作该字段，而是使用其他工具和方法来检测和解决内存泄漏问题。

（GPT参考回答，答案其实差不多）


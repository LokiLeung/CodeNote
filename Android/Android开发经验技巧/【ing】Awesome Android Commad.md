# Awesome Android Command


## ADB

### logcat

```bash
Usage: logcat [options] [filterspecs]

General options:
  -b, --buffer=<buffer>       Request alternate ring buffer(s):
                                main system radio events crash default all
                              Additionally, 'kernel' for userdebug and eng builds, and
                              'security' for Device Owner installations.
                              Multiple -b parameters or comma separated list of buffers are
                              allowed. Buffers are interleaved.
                              Default -b main,system,crash,kernel.
  -L, --last                  Dump logs from prior to last reboot from pstore.
  -c, --clear                 Clear (flush) the entire log and exit.
                              if -f is specified, clear the specified file and its related rotated
                              log files instead.
                              if -L is specified, clear pstore log instead.
  -d                          Dump the log and then exit (don't block).
  --pid=<pid>                 Only print logs from the given pid.
  --wrap                      Sleep for 2 hours or when buffer about to wrap whichever
                              comes first. Improves efficiency of polling by providing
                              an about-to-wrap wakeup.

Formatting:
  -v, --format=<format>       Sets log print format verb and adverbs, where <format> is one of:
                                brief help long process raw tag thread threadtime time
                              Modifying adverbs can be added:
                                color descriptive epoch monotonic printable uid usec UTC year zone
                              Multiple -v parameters or comma separated list of format and format
                              modifiers are allowed.
  -D, --dividers              Print dividers between each log buffer.
  -B, --binary                Output the log in binary.

Outfile files:
  -f, --file=<file>           Log to file instead of stdout.
  -r, --rotate-kbytes=<n>     Rotate log every <n> kbytes. Requires -f option.
  -n, --rotate-count=<count>  Sets max number of rotated logs to <count>, default 4.
  --id=<id>                   If the signature <id> for logging to file changes, then clear the
                              associated files and continue.

Logd control:
 These options send a control message to the logd daemon on device, print its return message if
 applicable, then exit. They are incompatible with -L, as these attributes do not apply to pstore.
  -g, --buffer-size           Get the size of the ring buffers within logd.
  -G, --buffer-size=<size>    Set size of a ring buffer in logd. May suffix with K or M.
                              This can individually control each buffer's size with -b.
  -S, --statistics            Output statistics.
                              --pid can be used to provide pid specific stats.
  -p, --prune                 Print prune white and ~black list. Service is specified as UID,
                              UID/PID or /PID. Weighed for quicker pruning if prefix with ~,
                              otherwise weighed for longevity if unadorned. All other pruning
                              activity is oldest first. Special case ~! represents an automatic
                              quicker pruning for the noisiest UID as determined by the current
                              statistics.
  -P, --prune='<list> ...'    Set prune white and ~black list, using same format as listed above.
                              Must be quoted.

Filtering:
  -s                          Set default filter to silent. Equivalent to filterspec '*:S'
  -e, --regex=<expr>          Only print lines where the log message matches <expr> where <expr> is
                              an ECMAScript regular expression.
  -m, --max-count=<count>     Quit after printing <count> lines. This is meant to be paired with
                              --regex, but will work on its own.
  --print                     This option is only applicable when --regex is set and only useful if
                              --max-count is also provided.
                              With --print, logcat will print all messages even if they do not
                              match the regex. Logcat will quit after printing the max-count number
                              of lines that match the regex.
  -t <count>                  Print only the most recent <count> lines (implies -d).
  -t '<time>'                 Print the lines since specified time (implies -d).
  -T <count>                  Print only the most recent <count> lines (does not imply -d).
  -T '<time>'                 Print the lines since specified time (not imply -d).
                              count is pure numerical, time is 'MM-DD hh:mm:ss.mmm...'
                              'YYYY-MM-DD hh:mm:ss.mmm...' or 'sssss.mmm...' format.

filterspecs are a series of 
  <tag>[:priority]

where <tag> is a log component tag (or * for all) and priority is:
  V    Verbose (default for <tag>)
  D    Debug (default for '*')
  I    Info
  W    Warn
  E    Error
  F    Fatal
  S    Silent (suppress all output)

'*' by itself means '*:D' and <tag> by itself means <tag>:V.
If no '*' filterspec or -s on command line, all filter defaults to '*:V'.
eg: '*:S <tag>' prints only <tag>, '<tag>:S' suppresses all <tag> log messages.

If not specified on the command line, filterspec is set from ANDROID_LOG_TAGS.

If not specified with -v on command line, format is set from ANDROID_PRINTF_LOG
or defaults to "threadtime"
```


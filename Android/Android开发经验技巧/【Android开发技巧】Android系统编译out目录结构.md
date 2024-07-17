# 【Android开发技巧】Android系统编译out目录结构

![be1fa0fff374a448b66813a15ce4f73](./【Android开发技巧】Android系统编译out目录结构.assets/be1fa0fff374a448b66813a15ce4f73.jpg)



文章为Android系统编译后out目录树结构，系统版本为Android13，以供参考。



```bash
卷 Data 的文件夹 PATH 列表
卷序列号为 6C69-15C1
A:.
│  ..path_interposer.lock
│  ..path_interposer_hash
│  .lock
│  .lock_build.trace.gz
│  .lock_dumpvars-build.trace.gz
│  .lock_dumpvars-error.log
│  .lock_dumpvars-soong.log
│  .lock_dumpvars-verbose.log.gz
│  .lock_error.log
│  .lock_soong.log
│  .lock_verbose.log.gz
│  .microfactory_Linux.lock
│  .microfactory_Linux_hash
│  .microfactory_Linux_version
│  .mk2rbc.lock
│  .mk2rbc.trace
│  .mk2rbc_hash
│  .ninja_deps
│  .ninja_fifo
│  .ninja_log
│  .out-dir
│  .path_interposer
│  .path_interposer_origpath
│  .rbcrun.lock
│  .rbcrun.trace
│  .rbcrun_hash
│  .soong_ui.lock
│  .soong_ui.trace
│  .soong_ui_hash
│  Android.mk
│  build.trace.1.gz
│  build.trace.2.gz
│  build.trace.3.gz
│  build.trace.4.gz
│  build.trace.5.gz
│  build.trace.gz
│  build_date.txt
│  build_progress.pb
│  CaseCheck.txt
│  casecheck.txt
│  CleanSpec.mk
│  dumpvars-build.trace.1.gz
│  dumpvars-build.trace.2.gz
│  dumpvars-build.trace.gz
│  dumpvars-error.1.log
│  dumpvars-error.2.log
│  dumpvars-error.log
│  dumpvars-soong.1.log
│  dumpvars-soong.2.log
│  dumpvars-soong.log
│  dumpvars-soong_metrics
│  dumpvars-verbose.log.1.gz
│  dumpvars-verbose.log.2.gz
│  dumpvars-verbose.log.gz
│  error.1.log
│  error.2.log
│  error.3.log
│  error.4.log
│  error.5.log
│  error.log
│  microfactory_Linux
│  mk2rbc
│  ninja_build
│  rbcrun
│  soong.1.log
│  soong.2.log
│  soong.3.log
│  soong.4.log
│  soong.5.log
│  soong.log
│  soong_metrics
│  soong_ui
│  tree.txt
│  verbose.log.1.gz
│  verbose.log.2.gz
│  verbose.log.3.gz
│  verbose.log.4.gz
│  verbose.log.5.gz
│  verbose.log.gz
│  
├─..path_interposer_intermediates
│  ├─android-soong-ui-build-paths
│  │  └─android
│  │      └─soong
│  │          └─ui
│  │              └─build
│  │                      paths.a
│  │                      paths.a.hash
│  │                      
│  └─main
│          main.a
│          main.a.hash
│          
├─.microfactory_Linux_intermediates
│  ├─github.com-google-blueprint-microfactory
│  │  └─github.com
│  │      └─google
│  │          └─blueprint
│  │                  microfactory.a
│  │                  microfactory.a.hash
│  │                  
│  ├─main
│  │      main.a
│  │      main.a.hash
│  │      
│  └─src
│          microfactory.go
│          
├─.mk2rbc_intermediates
│  ├─android-soong-androidmk-parser
│  │  └─android
│  │      └─soong
│  │          └─androidmk
│  │                  parser.a
│  │                  parser.a.hash
│  │                  
│  ├─android-soong-mk2rbc
│  │  └─android
│  │      └─soong
│  │              mk2rbc.a
│  │              mk2rbc.a.hash
│  │              
│  └─main
│          main.a
│          main.a.hash
│          
├─.module_paths
│      Android.bp.list
│      Android.mk.list
│      AndroidProducts.mk.list
│      bazel.list
│      CleanSpec.mk.list
│      configuration.list
│      files.db
│      OWNERS.list
│      TEST_MAPPING.list
│      
├─.path
│      aa-enabled
│      aa-exec
│      aa-features-abi
│      aa-remove-unknown
│      aa-status
│      aa-teardown
│      accessdb
│      acloud
│      acov
│      acov-llvm.py
│      aday
│      add-accounts
│      add-accounts-sdk
│      add-apt-repository
│      add-shell
│      add3prf.py
│      add3prf_test.py
│      addgnupghome
│      addgroup
│      addpart
│      addr2line
│      adduser
│      agetty
│      aidegen
│      android
│      android-info.txt
│      android.bat
│      Android.bp
│      Android.mk
│      apparmor_parser
│      apparmor_status
│      applygnupgdefaults
│      apport-bug
│      apport-cli
│      apport-collect
│      apport-unpack
│      apropos
│      apt
│      apt-add-repository
│      apt-cache
│      apt-cdrom
│      apt-config
│      apt-extracttemplates
│      apt-ftparchive
│      apt-get
│      apt-key
│      apt-mark
│      apt-sortpkgs
│      arch
│      architecture.py
│      arpd
│      arptables
│      arptables-nft
│      arptables-nft-restore
│      arptables-nft-save
│      arptables-restore
│      arptables-save
│      atest
│      atest-py2
│      atest-py3
│      attr
│      awk
│      b2sum
│      badblocks
│      base32
│      base64
│      basename
│      basenc
│      bash
│      bashbug
│      bash_util.bash
│      battery_simulator.py
│      biosdecode
│      bison
│      bison.yacc
│      blkdeactivate
│      blkdiscard
│      blkid
│      blkzone
│      blockdev
│      boardconfig_usage_analysis.py
│      bootctl
│      bridge
│      BUILD.bazel
│      bunzip2
│      busctl
│      busybox
│      byobu
│      byobu-config
│      byobu-ctrl-a
│      byobu-disable
│      byobu-disable-prompt
│      byobu-enable
│      byobu-enable-prompt
│      byobu-export
│      byobu-janitor
│      byobu-keybindings
│      byobu-launch
│      byobu-launcher
│      byobu-launcher-install
│      byobu-launcher-uninstall
│      byobu-layout
│      byobu-prompt
│      byobu-quiet
│      byobu-reconnect-sockets
│      byobu-screen
│      byobu-select-backend
│      byobu-select-profile
│      byobu-select-session
│      byobu-shell
│      byobu-silent
│      byobu-status
│      byobu-status-detail
│      byobu-tmux
│      byobu-ugraph
│      byobu-ulevel
│      bzcat
│      bzcmp
│      bzdiff
│      bzegrep
│      bzexe
│      bzfgrep
│      bzgrep
│      bzip2
│      bzip2recover
│      bzless
│      bzmore
│      c++
│      c++filt
│      c89
│      c89-gcc
│      c99
│      c99-gcc
│      capsh
│      captoinfo
│      cargo2android.py
│      cat
│      catman
│      chage
│      chattr
│      chcon
│      chcpu
│      chfn
│      chgpasswd
│      chgrp
│      chmem
│      chmod
│      choom
│      chown
│      chpasswd
│      chroot
│      chrt
│      chsh
│      chvt
│      ckbcomp
│      cksum
│      clear
│      clear_console
│      cmp
│      codegen
│      codepage
│      col
│      col1
│      col2
│      col3
│      col4
│      col5
│      col6
│      col7
│      col8
│      col9
│      colcrt
│      colrm
│      column
│      combine_sdks.sh
│      comm
│      compare-installed-size.py
│      corelist
│      cp
│      cpan
│      cpan5.34-x86_64-linux-gnu
│      cpgr
│      cpio
│      cpp
│      cpp-11
│      cppw
│      crashpad_handler
│      cron
│      crontab
│      csplit
│      ctail
│      ctrlaltdel
│      ctstat
│      curl
│      cut
│      cvtsudoers
│      c_rehash
│      dash
│      date
│      dbus-cleanup-sockets
│      dbus-daemon
│      dbus-launch
│      dbus-monitor
│      dbus-run-session
│      dbus-send
│      dbus-update-activation-environment
│      dbus-uuidgen
│      dcb
│      dd
│      ddms
│      ddms.bat
│      deallocvt
│      deb-systemd-helper
│      deb-systemd-invoke
│      debconf
│      debconf-apt-progress
│      debconf-communicate
│      debconf-copydb
│      debconf-escape
│      debconf-gettextize
│      debconf-set-selections
│      debconf-show
│      debconf-updatepo
│      debian-distro-info
│      debugfs
│      delgroup
│      delpart
│      deluser
│      delv
│      depmod
│      devlink
│      df
│      dhclient
│      dhclient-script
│      dh_bash-completion
│      diff
│      diff3
│      dig
│      dir
│      dircolors
│      dirmngr
│      dirmngr-client
│      dirname
│      disassemble_test.py
│      disassemble_test_input.py
│      disassemble_tombstone.py
│      distro-info
│      dmesg
│      dmidecode
│      dmsetup
│      dmstats
│      dnsdomainname
│      do-release-upgrade
│      domainname
│      dosfsck
│      dosfslabel
│      dpkg
│      dpkg-architecture
│      dpkg-buildflags
│      dpkg-buildpackage
│      dpkg-checkbuilddeps
│      dpkg-deb
│      dpkg-distaddfile
│      dpkg-divert
│      dpkg-genbuildinfo
│      dpkg-genchanges
│      dpkg-gencontrol
│      dpkg-gensymbols
│      dpkg-maintscript-helper
│      dpkg-mergechangelogs
│      dpkg-name
│      dpkg-parsechangelog
│      dpkg-preconfigure
│      dpkg-query
│      dpkg-realpath
│      dpkg-reconfigure
│      dpkg-scanpackages
│      dpkg-scansources
│      dpkg-shlibdeps
│      dpkg-source
│      dpkg-split
│      dpkg-statoverride
│      dpkg-trigger
│      dpkg-vendor
│      draw9patch
│      draw9patch.bat
│      dtc
│      du
│      dumpe2fs
│      dumpkeys
│      dwp
│      e2freefrag
│      e2fsck
│      e2image
│      e2label
│      e2mmpstatus
│      e2scrub
│      e2scrub_all
│      e2undo
│      e4crypt
│      e4defrag
│      ebtables
│      ebtables-nft
│      ebtables-nft-restore
│      ebtables-nft-save
│      ebtables-restore
│      ebtables-save
│      echo
│      ed
│      editor
│      egrep
│      eject
│      elfedit
│      emulator
│      emulator-check
│      enc2xs
│      encguess
│      env
│      envsubst
│      eqn
│      ex
│      example_crashes.py
│      expand
│      expiry
│      expr
│      extract_dtb
│      factor
│      faillock
│      faillog
│      faked-sysv
│      faked-tcp
│      fakeroot
│      fakeroot-sysv
│      fakeroot-tcp
│      fallocate
│      false
│      fatlabel
│      fc-cache
│      fc-cat
│      fc-conflist
│      fc-list
│      fc-match
│      fc-pattern
│      fc-query
│      fc-scan
│      fc-validate
│      fgconsole
│      fgrep
│      file
│      filefrag
│      fincore
│      find
│      findfs
│      findmnt
│      flex
│      flex++
│      flock
│      fmt
│      fold
│      free
│      fsck
│      fsck.cramfs
│      fsck.ext2
│      fsck.ext3
│      fsck.ext4
│      fsck.fat
│      fsck.minix
│      fsck.msdos
│      fsck.vfat
│      fsfreeze
│      fstab-decode
│      fstrim
│      ftp
│      funzip
│      fuser
│      fusermount
│      fusermount3
│      g++-11
│      gapplication
│      gawk
│      gcc-11
│      gcc-ar
│      gcc-ar-11
│      gcc-nm
│      gcc-nm-11
│      gcc-ranlib
│      gcc-ranlib-11
│      gcov
│      gcov-11
│      gcov-dump
│      gcov-dump-11
│      gcov-tool
│      gcov-tool-11
│      gdbclient.py
│      gdbus
│      gencat
│      genl
│      geqn
│      getcap
│      getconf
│      getent
│      getfattr
│      getkeycodes
│      getopt
│      getpcaps
│      gettext
│      gettext.sh
│      gettextize
│      getty
│      get_rust_pkg.py
│      ginstall-info
│      gio
│      gio-querymodules
│      git
│      git-receive-pack
│      git-shell
│      git-upload-archive
│      git-upload-pack
│      glib-compile-schemas
│      gmake
│      gold
│      goldfish-webrtc-bridge
│      gotestmain
│      gotestrunner
│      gpasswd
│      gpg
│      gpg-agent
│      gpg-connect-agent
│      gpg-wks-server
│      gpg-zip
│      gpgcompose
│      gpgconf
│      gpgparsemail
│      gpgsm
│      gpgsplit
│      gpgtar
│      gpgv
│      gpic
│      gprof
│      grep
│      gresource
│      groff
│      grog
│      grops
│      grotty
│      groupadd
│      groupdel
│      groupmems
│      groupmod
│      groups
│      grpck
│      grpconv
│      grpunconv
│      gsettings
│      gtbl
│      gunzip
│      gzexe
│      gzip
│      h2ph
│      h2xs
│      halt
│      hardlink
│      hd
│      hdparm
│      head
│      helpztags
│      hexdump
│      hierarchyviewer
│      hierarchyviewer.bat
│      host
│      hostid
│      hostname
│      hostnamectl
│      htop
│      hwclock
│      hwe-support-status
│      i386
│      iconv
│      iconvconfig
│      id
│      info
│      infobrowser
│      infocmp
│      infotocap
│      init
│      insmod
│      install
│      install-info
│      installkernel
│      instmodsh
│      invoke-rc.d
│      ionice
│      ip
│      ip6tables
│      ip6tables-apply
│      ip6tables-legacy
│      ip6tables-legacy-restore
│      ip6tables-legacy-save
│      ip6tables-nft
│      ip6tables-nft-restore
│      ip6tables-nft-save
│      ip6tables-restore
│      ip6tables-restore-translate
│      ip6tables-save
│      ip6tables-translate
│      ipcmk
│      ipcrm
│      ipcs
│      iptables
│      iptables-apply
│      iptables-legacy
│      iptables-legacy-restore
│      iptables-legacy-save
│      iptables-nft
│      iptables-nft-restore
│      iptables-nft-save
│      iptables-restore
│      iptables-restore-translate
│      iptables-save
│      iptables-translate
│      iptables-xml
│      irqbalance
│      irqbalance-ui
│      ischroot
│      isosize
│      jaotc
│      jar
│      jarsigner
│      java
│      javac
│      javac_remote_toolchain_inputs
│      javadoc
│      javap
│      java_remote_toolchain_inputs
│      jcmd
│      jconsole
│      jdb
│      jdeprscan
│      jdeps
│      jfr
│      jhsdb
│      jimage
│      jinfo
│      jjs
│      jlink
│      jmap
│      jmod
│      jobb
│      jobb.bat
│      join
│      journalctl
│      jps
│      jrunscript
│      jshell
│      json_pp
│      jstack
│      jstat
│      jstatd
│      kbdinfo
│      kbdrate
│      kbd_mode
│      kbxutil
│      keep-one-running
│      kernel-install
│      keyring
│      keytool
│      kill
│      killall
│      killall5
│      kmod
│      last
│      lastb
│      lastlog
│      lcf
│      ldattach
│      ldconfig
│      ldconfig.real
│      ldd
│      less
│      lessecho
│      lessfile
│      lesskey
│      lesspipe
│      lex
│      lexgrog
│      libnetcfg
│      LICENSE
│      link
│      lint
│      lint.bat
│      linux32
│      linux64
│      lldbclient.py
│      llvm-addr2line
│      llvm-ar
│      llvm-as
│      llvm-cov
│      llvm-cxxfilt
│      llvm-dis
│      llvm-dwarfdump
│      llvm-gcov
│      llvm-link
│      llvm-modextract
│      llvm-nm
│      llvm-objcopy
│      llvm-objdump
│      llvm-profdata
│      llvm-ranlib
│      llvm-readelf
│      llvm-readobj
│      llvm-size
│      llvm-strings
│      llvm-strip
│      llvm-symbolizer
│      ln
│      lnstat
│      loadkeys
│      loadplugins
│      loadunimap
│      locale
│      locale-check
│      locale-gen
│      localectl
│      localedef
│      logger
│      login
│      loginctl
│      logname
│      logrotate
│      logsave
│      look
│      losetup
│      lowntfs-3g
│      ls
│      lsattr
│      lsblk
│      lsb_release
│      lscpu
│      lshw
│      lsipc
│      lslocks
│      lslogins
│      lsmem
│      lsmod
│      lsns
│      lsof
│      lspci
│      lspgpot
│      lsusb
│      lto-dump-11
│      lzcat
│      lzcmp
│      lzdiff
│      lzegrep
│      lzfgrep
│      lzgrep
│      lzless
│      lzma
│      lzmainfo
│      lzmore
│      m4
│      make
│      make-first-existing-target
│      man
│      man-recode
│      mandb
│      manifest
│      manpath
│      mapscrn
│      mawk
│      mcookie
│      md5sum
│      md5sum.textutils
│      mdig
│      memusage
│      memusagestat
│      mesg
│      migrate-pubring-from-classic-gpg
│      mkdir
│      mkdosfs
│      mkdtimg
│      mke2fs
│      mkfifo
│      mkfs
│      mkfs.bfs
│      mkfs.cramfs
│      mkfs.ext2
│      mkfs.ext3
│      mkfs.ext4
│      mkfs.fat
│      mkfs.minix
│      mkfs.msdos
│      mkfs.ntfs
│      mkfs.vfat
│      mkhomedir_helper
│      mklost+found
│      mknod
│      mkntfs
│      mksdcard
│      mksquashfs
│      mkswap
│      mktemp
│      mk_modmap
│      modinfo
│      modprobe
│      monkeyrunner
│      monkeyrunner.bat
│      more
│      mount
│      mount.drvfs
│      mount.fuse
│      mount.fuse3
│      mount.lowntfs-3g
│      mount.ntfs
│      mount.ntfs-3g
│      mountpoint
│      msgattrib
│      msgcat
│      msgcmp
│      msgcomm
│      msgconv
│      msgen
│      msgexec
│      msgfilter
│      msgfmt
│      msggrep
│      msginit
│      msgmerge
│      msgunfmt
│      msguniq
│      mt
│      mt-gnu
│      mtr
│      mtr-packet
│      mtrace
│      mv
│      namei
│      nano
│      nawk
│      nc
│      nc.openbsd
│      ncurses5-config
│      ncurses6-config
│      ncursesw5-config
│      ncursesw6-config
│      neqn
│      netcat
│      netplan
│      networkctl
│      networkd-dispatcher
│      newgrp
│      newusers
│      NF
│      nfnl_osf
│      nft
│      ngettext
│      nice
│      nimble_bridge
│      nisdomainname
│      nl
│      nm
│      nohup
│      nologin
│      NOTICE.csv
│      NOTICE.txt
│      nproc
│      nroff
│      nsenter
│      nslookup
│      nstat
│      nsupdate
│      ntfs-3g
│      ntfs-3g.probe
│      ntfscat
│      ntfsclone
│      ntfscluster
│      ntfscmp
│      ntfscp
│      ntfsdecrypt
│      ntfsfallocate
│      ntfsfix
│      ntfsinfo
│      ntfslabel
│      ntfsls
│      ntfsmove
│      ntfsrecover
│      ntfsresize
│      ntfssecaudit
│      ntfstruncate
│      ntfsundelete
│      ntfsusermap
│      ntfswipe
│      numfmt
│      objcopy
│      objdump
│      od
│      oem-getlogs
│      on_ac_power
│      openssl
│      openvt
│      OWNERS
│      ownership
│      pack200
│      pager
│      pam-auth-update
│      pam_extrausers_chkpwd
│      pam_extrausers_update
│      pam_getenv
│      pam_timestamp_check
│      parted
│      partprobe
│      partx
│      passwd
│      paste
│      pastebinit
│      patch
│      pathchk
│      pbget
│      pbput
│      pbputs
│      pdb3
│      pdb3.10
│      peekfd
│      perl
│      perl5.34-x86_64-linux-gnu
│      perl5.34.0
│      perlbug
│      perldoc
│      perlivp
│      perlthanks
│      pic
│      pico
│      piconv
│      pid
│      pidof
│      pidwait
│      pinentry
│      pinentry-curses
│      ping
│      ping4
│      ping6
│      pinky
│      pivot_root
│      pkaction
│      pkcheck
│      pkcon
│      pkexec
│      pkmon
│      pkttyagent
│      pl2pm
│      pldd
│      plymouth
│      plymouthd
│      pmap
│      po2debconf
│      pod2html
│      pod2man
│      pod2text
│      pod2usage
│      podchecker
│      podebconf-display-po
│      podebconf-report-po
│      poweroff
│      pr
│      PREBUILT
│      preconv
│      printenv
│      printf
│      prlimit
│      pro
│      prove
│      prtstat
│      psfaddtable
│      psfgettable
│      psfstriptable
│      psfxtable
│      pslog
│      pstree
│      pstree.x11
│      ptar
│      ptardiff
│      ptargrep
│      ptx
│      purge-old-kernels
│      pwck
│      pwconv
│      pwd
│      pwdx
│      pwunconv
│      py3clean
│      py3compile
│      py3versions
│      pydoc3
│      pydoc3.10
│      pygettext3
│      pygettext3.10
│      python
│      python3
│      python3.10
│      qemu-img
│      qsn
│      ranlib
│      rbash
│      rcp
│      rdma
│      readelf
│      readlink
│      readprofile
│      realpath
│      reboot
│      recode-sr-latin
│      red
│      remove-shell
│      renice
│      repo
│      reset
│      resize2fs
│      resizecons
│      resizepart
│      resolvectl
│      rev
│      reverse_tether.sh
│      rgrep
│      rlogin
│      rm
│      rmdir
│      rmic
│      rmid
│      rmiregistry
│      rmmod
│      rmt
│      rmt-tar
│      rnano
│      routef
│      routel
│      rpcgen
│      rrsync
│      rsh
│      rsync
│      rsync-ssl
│      rsyslogd
│      rtacct
│      rtcwake
│      rtmon
│      rtstat
│      run-one
│      run-one-constantly
│      run-one-until-failure
│      run-one-until-success
│      run-parts
│      run-this-one
│      runahat
│      runcon
│      runlevel
│      runuser
│      rview
│      rvim
│      savelog
│      scp
│      screen
│      screendump
│      screenshot2
│      script
│      scriptlive
│      scriptreplay
│      sdiff
│      sed
│      select-editor
│      sensible-browser
│      sensible-editor
│      sensible-pager
│      seq
│      serialver
│      service
│      setarch
│      setcap
│      setfattr
│      setfont
│      setkeycodes
│      setleds
│      setlogcons
│      setmetamode
│      setpci
│      setpriv
│      setsid
│      setterm
│      setupcon
│      setvesablank
│      setvtrgb
│      sftp
│      sg
│      sh
│      sha1sum
│      sha224sum
│      sha256sum
│      sha384sum
│      sha512sum
│      shadowconfig
│      shasum
│      showconsolefont
│      showkey
│      shred
│      shuf
│      shutdown
│      size
│      skill
│      slabtop
│      sleep
│      slogin
│      snap
│      snapctl
│      snapfuse
│      snice
│      soelim
│      soong_build
│      sort
│      sotruss
│      source.properties
│      splain
│      split
│      splitfont
│      sprof
│      sqfscat
│      sqfstar
│      ss
│      ssh
│      ssh-add
│      ssh-agent
│      ssh-argv0
│      ssh-copy-id
│      ssh-keygen
│      ssh-keyscan
│      stack
│      stacks
│      stack_core.py
│      start-stop-daemon
│      stat
│      static-sh
│      stdbuf
│      strace
│      strace-log-merge
│      streamzip
│      strings
│      strip
│      stty
│      su
│      sudo
│      sudoedit
│      sudoreplay
│      sudo_logsrvd
│      sudo_sendlog
│      sulogin
│      sum
│      swaplabel
│      swapoff
│      swapon
│      switch_root
│      symbol-tests.xml
│      symbol.py
│      sync
│      sysctl
│      systemctl
│      systemd
│      systemd-analyze
│      systemd-ask-password
│      systemd-cat
│      systemd-cgls
│      systemd-cgtop
│      systemd-cryptenroll
│      systemd-delta
│      systemd-detect-virt
│      systemd-escape
│      systemd-hwdb
│      systemd-id128
│      systemd-inhibit
│      systemd-machine-id-setup
│      systemd-mount
│      systemd-notify
│      systemd-path
│      systemd-run
│      systemd-socket-activate
│      systemd-stdio-bridge
│      systemd-sysext
│      systemd-sysusers
│      systemd-tmpfiles
│      systemd-tty-ask-password-agent
│      systemd-umount
│      tabs
│      tac
│      tail
│      tar
│      tarcat
│      taskset
│      tbl
│      tc
│      tcpdump
│      tee
│      telinit
│      telnet
│      telnet.netkit
│      tempfile
│      test
│      TEST_MAPPING
│      tic
│      time
│      timedatectl
│      timeout
│      tipc
│      tload
│      tmux
│      tnftp
│      toe
│      top
│      touch
│      tput
│      tr
│      tracepath
│      traceview
│      traceview.bat
│      troff
│      true
│      truncate
│      tset
│      tsort
│      tty
│      tune2fs
│      tzconfig
│      tzselect
│      ua
│      ubuntu-advantage
│      ubuntu-bug
│      ubuntu-core-launcher
│      ubuntu-desktop-installer
│      ubuntu-desktop-installer.os-prober
│      ubuntu-desktop-installer.probert
│      ubuntu-desktop-installer.subiquity-loadkeys
│      ubuntu-distro-info
│      ubuntu-security-status
│      ucf
│      ucfq
│      ucfr
│      uclampset
│      udevadm
│      ufdt_apply_overlay
│      ufw
│      uiautomatorviewer
│      uiautomatorviewer.bat
│      ul
│      umount
│      uname
│      unattended-upgrade
│      unattended-upgrades
│      uncompress
│      unexpand
│      unicode_start
│      unicode_stop
│      uniq
│      unix_chkpwd
│      unix_update
│      unlink
│      unlzma
│      unpack200
│      unshare
│      unsquashfs
│      unxz
│      unzip
│      unzipsfx
│      update-alternatives
│      update-ca-certificates
│      update-info-dir
│      update-locale
│      update-mime-database
│      update-motd
│      update-passwd
│      update-pciids
│      update-rc.d
│      update-shells
│      update_crate_tests.py
│      uptime
│      usb-devices
│      usb-reset-by-serial.py
│      usbhid-dump
│      usbreset
│      useradd
│      userdel
│      usermod
│      users
│      utmpdump
│      uuidd
│      uuidgen
│      uuidparse
│      validlocale
│      vcstime
│      vdir
│      vdpa
│      vi
│      view
│      vigpg
│      vigr
│      vim
│      vim.basic
│      vim.tiny
│      vimdiff
│      vimtutor
│      vipw
│      visudo
│      vmstat
│      vpddecode
│      w
│      wall
│      watch
│      watchgnupg
│      wc
│      wdctl
│      wget
│      whatis
│      whereis
│      which
│      which.debianutils
│      whiptail
│      who
│      whoami
│      wifi-status
│      wipefs
│      write
│      write.ul
│      wslpath
│      x86_64
│      x86_64-linux-gnu-addr2line
│      x86_64-linux-gnu-ar
│      x86_64-linux-gnu-as
│      x86_64-linux-gnu-c++filt
│      x86_64-linux-gnu-cpp
│      x86_64-linux-gnu-cpp-11
│      x86_64-linux-gnu-dwp
│      x86_64-linux-gnu-elfedit
│      x86_64-linux-gnu-g++
│      x86_64-linux-gnu-g++-11
│      x86_64-linux-gnu-gcc
│      x86_64-linux-gnu-gcc-11
│      x86_64-linux-gnu-gcc-ar
│      x86_64-linux-gnu-gcc-ar-11
│      x86_64-linux-gnu-gcc-nm
│      x86_64-linux-gnu-gcc-nm-11
│      x86_64-linux-gnu-gcc-ranlib
│      x86_64-linux-gnu-gcc-ranlib-11
│      x86_64-linux-gnu-gcov
│      x86_64-linux-gnu-gcov-11
│      x86_64-linux-gnu-gcov-dump
│      x86_64-linux-gnu-gcov-dump-11
│      x86_64-linux-gnu-gcov-tool
│      x86_64-linux-gnu-gcov-tool-11
│      x86_64-linux-gnu-gold
│      x86_64-linux-gnu-gprof
│      x86_64-linux-gnu-ld
│      x86_64-linux-gnu-ld.bfd
│      x86_64-linux-gnu-ld.gold
│      x86_64-linux-gnu-lto-dump-11
│      x86_64-linux-gnu-nm
│      x86_64-linux-gnu-objcopy
│      x86_64-linux-gnu-objdump
│      x86_64-linux-gnu-ranlib
│      x86_64-linux-gnu-readelf
│      x86_64-linux-gnu-size
│      x86_64-linux-gnu-strings
│      x86_64-linux-gnu-strip
│      xargs
│      xauth
│      xdg-user-dir
│      xdg-user-dirs-update
│      xgettext
│      xmlcatalog
│      xmllint
│      xsltproc
│      xsubpp
│      xtables-legacy-multi
│      xtables-monitor
│      xtables-nft-multi
│      xxd
│      xz
│      xzcat
│      xzcmp
│      xzdiff
│      xzegrep
│      xzfgrep
│      xzgrep
│      xzless
│      xzmore
│      yacc
│      yes
│      ypdomainname
│      zcat
│      zcmp
│      zdiff
│      zdump
│      zegrep
│      zfgrep
│      zforce
│      zgrep
│      zic
│      zip
│      zipcloak
│      zipdetails
│      zipgrep
│      zipinfo
│      zipnote
│      zipsplit
│      zless
│      zmore
│      znew
│      zramctl
│      [
│      
├─.rbcrun_intermediates
│  ├─go.starlark.net-internal-compile
│  │  └─go.starlark.net
│  │      └─internal
│  │              compile.a
│  │              compile.a.hash
│  │              
│  ├─go.starlark.net-internal-spell
│  │  └─go.starlark.net
│  │      └─internal
│  │              spell.a
│  │              spell.a.hash
│  │              
│  ├─go.starlark.net-resolve
│  │  └─go.starlark.net
│  │          resolve.a
│  │          resolve.a.hash
│  │          
│  ├─go.starlark.net-starlark
│  │  └─go.starlark.net
│  │          starlark.a
│  │          starlark.a.hash
│  │          
│  ├─go.starlark.net-starlarkstruct
│  │  └─go.starlark.net
│  │          starlarkstruct.a
│  │          starlarkstruct.a.hash
│  │          
│  ├─go.starlark.net-syntax
│  │  └─go.starlark.net
│  │          syntax.a
│  │          syntax.a.hash
│  │          
│  ├─main
│  │      main.a
│  │      main.a.hash
│  │      
│  └─rbcrun
│          rbcrun.a
│          rbcrun.a.hash
│          
├─.soong_ui_intermediates
│  ├─android-soong-bazel
│  │  └─android
│  │      └─soong
│  │              bazel.a
│  │              bazel.a.hash
│  │              
│  ├─android-soong-finder
│  │  └─android
│  │      └─soong
│  │              finder.a
│  │              finder.a.hash
│  │              
│  ├─android-soong-finder-fs
│  │  └─android
│  │      └─soong
│  │          └─finder
│  │                  fs.a
│  │                  fs.a.hash
│  │                  
│  ├─android-soong-shared
│  │  └─android
│  │      └─soong
│  │              shared.a
│  │              shared.a.hash
│  │              
│  ├─android-soong-ui-build
│  │  └─android
│  │      └─soong
│  │          └─ui
│  │                  build.a
│  │                  build.a.hash
│  │                  
│  ├─android-soong-ui-build-paths
│  │  └─android
│  │      └─soong
│  │          └─ui
│  │              └─build
│  │                      paths.a
│  │                      paths.a.hash
│  │                      
│  ├─android-soong-ui-logger
│  │  └─android
│  │      └─soong
│  │          └─ui
│  │                  logger.a
│  │                  logger.a.hash
│  │                  
│  ├─android-soong-ui-metrics
│  │  └─android
│  │      └─soong
│  │          └─ui
│  │                  metrics.a
│  │                  metrics.a.hash
│  │                  
│  ├─android-soong-ui-metrics-metrics_proto
│  │  └─android
│  │      └─soong
│  │          └─ui
│  │              └─metrics
│  │                      metrics_proto.a
│  │                      metrics_proto.a.hash
│  │                      
│  ├─android-soong-ui-metrics-mk_metrics_proto
│  │  └─android
│  │      └─soong
│  │          └─ui
│  │              └─metrics
│  │                      mk_metrics_proto.a
│  │                      mk_metrics_proto.a.hash
│  │                      
│  ├─android-soong-ui-metrics-upload_proto
│  │  └─android
│  │      └─soong
│  │          └─ui
│  │              └─metrics
│  │                      upload_proto.a
│  │                      upload_proto.a.hash
│  │                      
│  ├─android-soong-ui-signal
│  │  └─android
│  │      └─soong
│  │          └─ui
│  │                  signal.a
│  │                  signal.a.hash
│  │                  
│  ├─android-soong-ui-status
│  │  └─android
│  │      └─soong
│  │          └─ui
│  │                  status.a
│  │                  status.a.hash
│  │                  
│  ├─android-soong-ui-status-build_error_proto
│  │  └─android
│  │      └─soong
│  │          └─ui
│  │              └─status
│  │                      build_error_proto.a
│  │                      build_error_proto.a.hash
│  │                      
│  ├─android-soong-ui-status-build_progress_proto
│  │  └─android
│  │      └─soong
│  │          └─ui
│  │              └─status
│  │                      build_progress_proto.a
│  │                      build_progress_proto.a.hash
│  │                      
│  ├─android-soong-ui-status-ninja_frontend
│  │  └─android
│  │      └─soong
│  │          └─ui
│  │              └─status
│  │                      ninja_frontend.a
│  │                      ninja_frontend.a.hash
│  │                      
│  ├─android-soong-ui-terminal
│  │  └─android
│  │      └─soong
│  │          └─ui
│  │                  terminal.a
│  │                  terminal.a.hash
│  │                  
│  ├─android-soong-ui-tracer
│  │  └─android
│  │      └─soong
│  │          └─ui
│  │                  tracer.a
│  │                  tracer.a.hash
│  │                  
│  ├─github.com-google-blueprint
│  │  └─github.com
│  │      └─google
│  │              blueprint.a
│  │              blueprint.a.hash
│  │              
│  ├─github.com-google-blueprint-bootstrap
│  │  └─github.com
│  │      └─google
│  │          └─blueprint
│  │                  bootstrap.a
│  │                  bootstrap.a.hash
│  │                  
│  ├─github.com-google-blueprint-bootstrap-bpdoc
│  │  └─github.com
│  │      └─google
│  │          └─blueprint
│  │              └─bootstrap
│  │                      bpdoc.a
│  │                      bpdoc.a.hash
│  │                      
│  ├─github.com-google-blueprint-deptools
│  │  └─github.com
│  │      └─google
│  │          └─blueprint
│  │                  deptools.a
│  │                  deptools.a.hash
│  │                  
│  ├─github.com-google-blueprint-metrics
│  │  └─github.com
│  │      └─google
│  │          └─blueprint
│  │                  metrics.a
│  │                  metrics.a.hash
│  │                  
│  ├─github.com-google-blueprint-microfactory
│  │  └─github.com
│  │      └─google
│  │          └─blueprint
│  │                  microfactory.a
│  │                  microfactory.a.hash
│  │                  
│  ├─github.com-google-blueprint-parser
│  │  └─github.com
│  │      └─google
│  │          └─blueprint
│  │                  parser.a
│  │                  parser.a.hash
│  │                  
│  ├─github.com-google-blueprint-pathtools
│  │  └─github.com
│  │      └─google
│  │          └─blueprint
│  │                  pathtools.a
│  │                  pathtools.a.hash
│  │                  
│  ├─github.com-google-blueprint-proptools
│  │  └─github.com
│  │      └─google
│  │          └─blueprint
│  │                  proptools.a
│  │                  proptools.a.hash
│  │                  
│  ├─google.golang.org-protobuf-encoding-prototext
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─encoding
│  │                  prototext.a
│  │                  prototext.a.hash
│  │                  
│  ├─google.golang.org-protobuf-encoding-protowire
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─encoding
│  │                  protowire.a
│  │                  protowire.a.hash
│  │                  
│  ├─google.golang.org-protobuf-internal-descfmt
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─internal
│  │                  descfmt.a
│  │                  descfmt.a.hash
│  │                  
│  ├─google.golang.org-protobuf-internal-descopts
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─internal
│  │                  descopts.a
│  │                  descopts.a.hash
│  │                  
│  ├─google.golang.org-protobuf-internal-detrand
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─internal
│  │                  detrand.a
│  │                  detrand.a.hash
│  │                  
│  ├─google.golang.org-protobuf-internal-encoding-defval
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─internal
│  │              └─encoding
│  │                      defval.a
│  │                      defval.a.hash
│  │                      
│  ├─google.golang.org-protobuf-internal-encoding-messageset
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─internal
│  │              └─encoding
│  │                      messageset.a
│  │                      messageset.a.hash
│  │                      
│  ├─google.golang.org-protobuf-internal-encoding-tag
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─internal
│  │              └─encoding
│  │                      tag.a
│  │                      tag.a.hash
│  │                      
│  ├─google.golang.org-protobuf-internal-encoding-text
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─internal
│  │              └─encoding
│  │                      text.a
│  │                      text.a.hash
│  │                      
│  ├─google.golang.org-protobuf-internal-errors
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─internal
│  │                  errors.a
│  │                  errors.a.hash
│  │                  
│  ├─google.golang.org-protobuf-internal-filedesc
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─internal
│  │                  filedesc.a
│  │                  filedesc.a.hash
│  │                  
│  ├─google.golang.org-protobuf-internal-filetype
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─internal
│  │                  filetype.a
│  │                  filetype.a.hash
│  │                  
│  ├─google.golang.org-protobuf-internal-flags
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─internal
│  │                  flags.a
│  │                  flags.a.hash
│  │                  
│  ├─google.golang.org-protobuf-internal-genid
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─internal
│  │                  genid.a
│  │                  genid.a.hash
│  │                  
│  ├─google.golang.org-protobuf-internal-impl
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─internal
│  │                  impl.a
│  │                  impl.a.hash
│  │                  
│  ├─google.golang.org-protobuf-internal-order
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─internal
│  │                  order.a
│  │                  order.a.hash
│  │                  
│  ├─google.golang.org-protobuf-internal-pragma
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─internal
│  │                  pragma.a
│  │                  pragma.a.hash
│  │                  
│  ├─google.golang.org-protobuf-internal-set
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─internal
│  │                  set.a
│  │                  set.a.hash
│  │                  
│  ├─google.golang.org-protobuf-internal-strs
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─internal
│  │                  strs.a
│  │                  strs.a.hash
│  │                  
│  ├─google.golang.org-protobuf-internal-version
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─internal
│  │                  version.a
│  │                  version.a.hash
│  │                  
│  ├─google.golang.org-protobuf-proto
│  │  └─google.golang.org
│  │      └─protobuf
│  │              proto.a
│  │              proto.a.hash
│  │              
│  ├─google.golang.org-protobuf-reflect-protoreflect
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─reflect
│  │                  protoreflect.a
│  │                  protoreflect.a.hash
│  │                  
│  ├─google.golang.org-protobuf-reflect-protoregistry
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─reflect
│  │                  protoregistry.a
│  │                  protoregistry.a.hash
│  │                  
│  ├─google.golang.org-protobuf-runtime-protoiface
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─runtime
│  │                  protoiface.a
│  │                  protoiface.a.hash
│  │                  
│  ├─google.golang.org-protobuf-runtime-protoimpl
│  │  └─google.golang.org
│  │      └─protobuf
│  │          └─runtime
│  │                  protoimpl.a
│  │                  protoimpl.a.hash
│  │                  
│  └─main
│          main.a
│          main.a.hash
│          
├─host
│  └─linux-x86
│      └─bin
│          │  gotestmain
│          │  gotestrunner
│          │  loadplugins
│          │  soong_build
│          │  
│          └─go
│              ├─aidl-soong-rules
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              aidl.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  aidl.a
│              │                  
│              ├─androidmk-parser
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │          └─androidmk
│              │  │                  parser.a
│              │  │                  
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │              └─androidmk
│              │                      parser.a
│              │                      
│              ├─arm_compute_library_nn_driver
│              │  └─pkg
│              │          arm_compute_library_nn_driver.a
│              │          
│              ├─blueprint
│              │  ├─pkg
│              │  │  └─github.com
│              │  │      └─google
│              │  │              blueprint.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─github.com
│              │          └─google
│              │                  blueprint.a
│              │                  
│              ├─blueprint-bootstrap
│              │  └─pkg
│              │      └─github.com
│              │          └─google
│              │              └─blueprint
│              │                      bootstrap.a
│              │                      
│              ├─blueprint-bootstrap-bpdoc
│              │  ├─pkg
│              │  │  └─github.com
│              │  │      └─google
│              │  │          └─blueprint
│              │  │              └─bootstrap
│              │  │                      bpdoc.a
│              │  │                      
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─github.com
│              │          └─google
│              │              └─blueprint
│              │                  └─bootstrap
│              │                          bpdoc.a
│              │                          
│              ├─blueprint-deptools
│              │  └─pkg
│              │      └─github.com
│              │          └─google
│              │              └─blueprint
│              │                      deptools.a
│              │                      
│              ├─blueprint-metrics
│              │  └─pkg
│              │      └─github.com
│              │          └─google
│              │              └─blueprint
│              │                      metrics.a
│              │                      
│              ├─blueprint-parser
│              │  ├─pkg
│              │  │  └─github.com
│              │  │      └─google
│              │  │          └─blueprint
│              │  │                  parser.a
│              │  │                  
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─github.com
│              │          └─google
│              │              └─blueprint
│              │                      parser.a
│              │                      
│              ├─blueprint-pathtools
│              │  ├─pkg
│              │  │  └─github.com
│              │  │      └─google
│              │  │          └─blueprint
│              │  │                  pathtools.a
│              │  │                  
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─github.com
│              │          └─google
│              │              └─blueprint
│              │                      pathtools.a
│              │                      
│              ├─blueprint-proptools
│              │  ├─pkg
│              │  │  └─github.com
│              │  │      └─google
│              │  │          └─blueprint
│              │  │                  proptools.a
│              │  │                  
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─github.com
│              │          └─google
│              │              └─blueprint
│              │                      proptools.a
│              │                      
│              ├─cuttlefish-soong-rules
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │                  cuttlefish.a
│              │                  
│              ├─gki-soong-rules
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              gki.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  gki.a
│              │                  
│              ├─go-cmp
│              │  ├─pkg
│              │  │  └─github.com
│              │  │      └─google
│              │  │          └─go-cmp
│              │  │                  cmp.a
│              │  │                  
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─github.com
│              │          └─google
│              │              └─go-cmp
│              │                      cmp.a
│              │                      
│              ├─go-cmp-internal-diff
│              │  ├─pkg
│              │  │  └─github.com
│              │  │      └─google
│              │  │          └─go-cmp
│              │  │              └─cmp
│              │  │                  └─internal
│              │  │                          diff.a
│              │  │                          
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─github.com
│              │          └─google
│              │              └─go-cmp
│              │                  └─cmp
│              │                      └─internal
│              │                              diff.a
│              │                              
│              ├─go-cmp-internal-flags
│              │  └─pkg
│              │      └─github.com
│              │          └─google
│              │              └─go-cmp
│              │                  └─cmp
│              │                      └─internal
│              │                              flags.a
│              │                              
│              ├─go-cmp-internal-function
│              │  ├─pkg
│              │  │  └─github.com
│              │  │      └─google
│              │  │          └─go-cmp
│              │  │              └─cmp
│              │  │                  └─internal
│              │  │                          function.a
│              │  │                          
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─github.com
│              │          └─google
│              │              └─go-cmp
│              │                  └─cmp
│              │                      └─internal
│              │                              function.a
│              │                              
│              ├─go-cmp-internal-testprotos
│              │  └─pkg
│              │      └─github.com
│              │          └─google
│              │              └─go-cmp
│              │                  └─cmp
│              │                      └─internal
│              │                              testprotos.a
│              │                              
│              ├─go-cmp-internal-teststructs
│              │  └─pkg
│              │      └─github.com
│              │          └─google
│              │              └─go-cmp
│              │                  └─cmp
│              │                      └─internal
│              │                              teststructs.a
│              │                              
│              ├─go-cmp-internal-value
│              │  ├─pkg
│              │  │  └─github.com
│              │  │      └─google
│              │  │          └─go-cmp
│              │  │              └─cmp
│              │  │                  └─internal
│              │  │                          value.a
│              │  │                          
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─github.com
│              │          └─google
│              │              └─go-cmp
│              │                  └─cmp
│              │                      └─internal
│              │                              value.a
│              │                              
│              ├─golang-protobuf-android
│              │  └─pkg
│              │      └─google.golang.org
│              │          └─protobuf
│              │                  android.a
│              │                  
│              ├─golang-protobuf-encoding-prototext
│              │  └─pkg
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─encoding
│              │                      prototext.a
│              │                      
│              ├─golang-protobuf-encoding-protowire
│              │  ├─pkg
│              │  │  └─google.golang.org
│              │  │      └─protobuf
│              │  │          └─encoding
│              │  │                  protowire.a
│              │  │                  
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─encoding
│              │                      protowire.a
│              │                      
│              ├─golang-protobuf-internal-descfmt
│              │  ├─pkg
│              │  │  └─google.golang.org
│              │  │      └─protobuf
│              │  │          └─internal
│              │  │                  descfmt.a
│              │  │                  
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─internal
│              │                      descfmt.a
│              │                      
│              ├─golang-protobuf-internal-descopts
│              │  └─pkg
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─internal
│              │                      descopts.a
│              │                      
│              ├─golang-protobuf-internal-detrand
│              │  └─pkg
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─internal
│              │                      detrand.a
│              │                      
│              ├─golang-protobuf-internal-encoding-defval
│              │  └─pkg
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─internal
│              │                  └─encoding
│              │                          defval.a
│              │                          
│              ├─golang-protobuf-internal-encoding-messageset
│              │  └─pkg
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─internal
│              │                  └─encoding
│              │                          messageset.a
│              │                          
│              ├─golang-protobuf-internal-encoding-tag
│              │  └─pkg
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─internal
│              │                  └─encoding
│              │                          tag.a
│              │                          
│              ├─golang-protobuf-internal-encoding-text
│              │  └─pkg
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─internal
│              │                  └─encoding
│              │                          text.a
│              │                          
│              ├─golang-protobuf-internal-errors
│              │  ├─pkg
│              │  │  └─google.golang.org
│              │  │      └─protobuf
│              │  │          └─internal
│              │  │                  errors.a
│              │  │                  
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─internal
│              │                      errors.a
│              │                      
│              ├─golang-protobuf-internal-filedesc
│              │  └─pkg
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─internal
│              │                      filedesc.a
│              │                      
│              ├─golang-protobuf-internal-filetype
│              │  └─pkg
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─internal
│              │                      filetype.a
│              │                      
│              ├─golang-protobuf-internal-flags
│              │  └─pkg
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─internal
│              │                      flags.a
│              │                      
│              ├─golang-protobuf-internal-genid
│              │  └─pkg
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─internal
│              │                      genid.a
│              │                      
│              ├─golang-protobuf-internal-impl
│              │  ├─pkg
│              │  │  └─google.golang.org
│              │  │      └─protobuf
│              │  │          └─internal
│              │  │                  impl.a
│              │  │                  
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─internal
│              │                      impl.a
│              │                      
│              ├─golang-protobuf-internal-order
│              │  ├─pkg
│              │  │  └─google.golang.org
│              │  │      └─protobuf
│              │  │          └─internal
│              │  │                  order.a
│              │  │                  
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─internal
│              │                      order.a
│              │                      
│              ├─golang-protobuf-internal-pragma
│              │  └─pkg
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─internal
│              │                      pragma.a
│              │                      
│              ├─golang-protobuf-internal-set
│              │  ├─pkg
│              │  │  └─google.golang.org
│              │  │      └─protobuf
│              │  │          └─internal
│              │  │                  set.a
│              │  │                  
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─internal
│              │                      set.a
│              │                      
│              ├─golang-protobuf-internal-strs
│              │  ├─pkg
│              │  │  └─google.golang.org
│              │  │      └─protobuf
│              │  │          └─internal
│              │  │                  strs.a
│              │  │                  
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─internal
│              │                      strs.a
│              │                      
│              ├─golang-protobuf-internal-version
│              │  └─pkg
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─internal
│              │                      version.a
│              │                      
│              ├─golang-protobuf-proto
│              │  └─pkg
│              │      └─google.golang.org
│              │          └─protobuf
│              │                  proto.a
│              │                  
│              ├─golang-protobuf-reflect-protoreflect
│              │  ├─pkg
│              │  │  └─google.golang.org
│              │  │      └─protobuf
│              │  │          └─reflect
│              │  │                  protoreflect.a
│              │  │                  
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─reflect
│              │                      protoreflect.a
│              │                      
│              ├─golang-protobuf-reflect-protoregistry
│              │  └─pkg
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─reflect
│              │                      protoregistry.a
│              │                      
│              ├─golang-protobuf-runtime-protoiface
│              │  └─pkg
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─runtime
│              │                      protoiface.a
│              │                      
│              ├─golang-protobuf-runtime-protoimpl
│              │  └─pkg
│              │      └─google.golang.org
│              │          └─protobuf
│              │              └─runtime
│              │                      protoimpl.a
│              │                      
│              ├─gotestmain
│              │  └─obj
│              │          a.out
│              │          gotestmain.a
│              │          
│              ├─gotestrunner
│              │  └─obj
│              │          a.out
│              │          gotestrunner.a
│              │          
│              ├─hidl-soong-rules
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │                  hidl.a
│              │                  
│              ├─kernel-config-soong-rules
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─kernel
│              │                      configs.a
│              │                      
│              ├─loadplugins
│              │  └─obj
│              │          a.out
│              │          loadplugins.a
│              │          
│              ├─sbox_proto
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─cmd
│              │                  └─sbox
│              │                          sbox_proto.a
│              │                          
│              ├─soong
│              │  └─pkg
│              │      └─android
│              │              soong.a
│              │              
│              ├─soong-android
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              android.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  android.a
│              │                  
│              ├─soong-android-allowlists
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─android
│              │                      allowlists.a
│              │                      
│              ├─soong-android-sdk
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              android_sdk.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  android_sdk.a
│              │                  
│              ├─soong-android-soongconfig
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │          └─android
│              │  │                  soongconfig.a
│              │  │                  
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │              └─android
│              │                      soongconfig.a
│              │                      
│              ├─soong-apex
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              apex.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  apex.a
│              │                  
│              ├─soong-api
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │                  api.a
│              │                  
│              ├─soong-art
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │                  art.a
│              │                  
│              ├─soong-bazel
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              bazel.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  bazel.a
│              │                  
│              ├─soong-bloaty
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │                  bloaty.a
│              │                  
│              ├─soong-bp2build
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              bp2build.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  bp2build.a
│              │                  
│              ├─soong-bpf
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              bpf.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  bpf.a
│              │                  
│              ├─soong-ca-certificates
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─system
│              │                      ca-certificates.a
│              │                      
│              ├─soong-cc
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              cc.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  cc.a
│              │                  
│              ├─soong-cc-config
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │          └─cc
│              │  │                  config.a
│              │  │                  
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │              └─cc
│              │                      config.a
│              │                      
│              ├─soong-clang
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─external
│              │                      clang.a
│              │                      
│              ├─soong-clang-prebuilts
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─prebuilts
│              │                  └─clang
│              │                      └─host
│              │                          └─linux-x86
│              │                                  clangprebuilts.a
│              │                                  
│              ├─soong-cquery
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │          └─bazel
│              │  │                  cquery.a
│              │  │                  
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │              └─bazel
│              │                      cquery.a
│              │                      
│              ├─soong-csuite
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              csuite.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  csuite.a
│              │                  
│              ├─soong-dexpreopt
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              dexpreopt.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  dexpreopt.a
│              │                  
│              ├─soong-display_defaults
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─hardware
│              │                  └─qcom
│              │                      └─sm8150
│              │                              display.a
│              │                              
│              ├─soong-display_defaults_sm7250
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─hardware
│              │                  └─qcom
│              │                      └─sm7250
│              │                              display.a
│              │                              
│              ├─soong-etc
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              etc.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  etc.a
│              │                  
│              ├─soong-filesystem
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              filesystem.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  filesystem.a
│              │                  
│              ├─soong-fluoride
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │                  fluoride.a
│              │                  
│              ├─soong-fs_config
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │                  fs_config.a
│              │                  
│              ├─soong-fuzz
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │                  fuzz.a
│              │                  
│              ├─soong-genrule
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              genrule.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  genrule.a
│              │                  
│              ├─soong-icu
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │                  icu.a
│              │                  
│              ├─soong-java
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              java.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  java.a
│              │                  
│              ├─soong-java-config
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─java
│              │                      config.a
│              │                      
│              ├─soong-java-config-error_prone
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─java
│              │                  └─config
│              │                          error_prone.a
│              │                          
│              ├─soong-kernel
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              kernel.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  kernel.a
│              │                  
│              ├─soong-libchrome
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─external
│              │                      libchrome.a
│              │                      
│              ├─soong-linkerconfig
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              linkerconfig.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  linkerconfig.a
│              │                  
│              ├─soong-llvm
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─external
│              │                      llvm.a
│              │                      
│              ├─soong-phony
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │                  phony.a
│              │                  
│              ├─soong-provenance
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              provenance.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  provenance.a
│              │                  
│              ├─soong-python
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              python.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  python.a
│              │                  
│              ├─soong-remoteexec
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              remoteexec.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  remoteexec.a
│              │                  
│              ├─soong-response
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              response.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  response.a
│              │                  
│              ├─soong-robolectric
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │                  robolectric.a
│              │                  
│              ├─soong-rust
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              rust.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  rust.a
│              │                  
│              ├─soong-rust-config
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─rust
│              │                      config.a
│              │                      
│              ├─soong-rust-prebuilts
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─prebuilts
│              │                  └─rust
│              │                          rustprebuilts.a
│              │                          
│              ├─soong-sdk
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              sdk.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  sdk.a
│              │                  
│              ├─soong-selinux
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │                  selinux.a
│              │                  
│              ├─soong-sh
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              sh.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  sh.a
│              │                  
│              ├─soong-shared
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              shared.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  shared.a
│              │                  
│              ├─soong-snapshot
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              snapshot.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  snapshot.a
│              │                  
│              ├─soong-starlark-format
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              starlark_fmt.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  starlark_fmt.a
│              │                  
│              ├─soong-suite-harness
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─tradefed
│              │                      suite_harness.a
│              │                      
│              ├─soong-sysprop
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              sysprop.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  sysprop.a
│              │                  
│              ├─soong-tradefed
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │                  tradefed.a
│              │                  
│              ├─soong-ui-bp2build_metrics_proto
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─ui
│              │                  └─metrics
│              │                          bp2build_metrics_proto.a
│              │                          
│              ├─soong-ui-logger
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │          └─ui
│              │  │                  logger.a
│              │  │                  
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │              └─ui
│              │                      logger.a
│              │                      
│              ├─soong-ui-metrics
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │          └─ui
│              │  │                  metrics.a
│              │  │                  
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │              └─ui
│              │                      metrics.a
│              │                      
│              ├─soong-ui-metrics_proto
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─ui
│              │                  └─metrics
│              │                          metrics_proto.a
│              │                          
│              ├─soong-ui-metrics_upload_proto
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─ui
│              │                  └─metrics
│              │                          upload_proto.a
│              │                          
│              ├─soong-ui-mk_metrics_proto
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─ui
│              │                  └─metrics
│              │                          mk_metrics_proto.a
│              │                          
│              ├─soong-ui-status
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │          └─ui
│              │  │                  status.a
│              │  │                  
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │              └─ui
│              │                      status.a
│              │                      
│              ├─soong-ui-status-build_error_proto
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─ui
│              │                  └─status
│              │                          build_error_proto.a
│              │                          
│              ├─soong-ui-status-build_progress_proto
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─ui
│              │                  └─status
│              │                          build_progress_proto.a
│              │                          
│              ├─soong-ui-status-ninja_frontend
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─ui
│              │                  └─status
│              │                          ninja_frontend.a
│              │                          
│              ├─soong-ui-tracer
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─ui
│              │                      tracer.a
│              │                      
│              ├─soong-wayland-protocol-codegen
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │              └─external
│              │                      wayland-protocol.a
│              │                      
│              ├─soong-xml
│              │  ├─pkg
│              │  │  └─android
│              │  │      └─soong
│              │  │              xml.a
│              │  │              
│              │  └─test
│              │      │  test
│              │      │  test.a
│              │      │  test.go
│              │      │  test.passed
│              │      │  
│              │      └─android
│              │          └─soong
│              │                  xml.a
│              │                  
│              ├─soong_build
│              │  ├─gen
│              │  │      plugin.go
│              │  │      
│              │  └─obj
│              │          a.out
│              │          soong_build.a
│              │          
│              ├─vintf-compatibility-matrix-soong-rules
│              │  └─pkg
│              │      └─android
│              │          └─soong
│              │                  vintf-compatibility-matrix.a
│              │                  
│              └─xsdc-soong-rules
│                  └─pkg
│                      └─android
│                          └─soong
│                                  xsdc.a
│                                  
└─soong
    │  .bpglob.lock
    │  .bpglob_hash
    │  .soong.bootstrap.epoch.1
    │  .soong.kati_enabled
    │  bootstrap.ninja
    │  bootstrap.ninja.d
    │  bpglob
    │  dexpreopt.config
    │  globs-bp2build.ninja
    │  globs-build.ninja
    │  globs-modulegraph.ninja
    │  globs-queryview.ninja
    │  globs-soong_docs.ninja
    │  soong.environment.available
    │  soong.variables
    │  
    ├─.bpglob_intermediates
    │  ├─github.com-google-blueprint-deptools
    │  │  └─github.com
    │  │      └─google
    │  │          └─blueprint
    │  │                  deptools.a
    │  │                  deptools.a.hash
    │  │                  
    │  ├─github.com-google-blueprint-pathtools
    │  │  └─github.com
    │  │      └─google
    │  │          └─blueprint
    │  │                  pathtools.a
    │  │                  pathtools.a.hash
    │  │                  
    │  └─main
    │          main.a
    │          main.a.hash
    │          
    ├─.temp
    └─soong_injection
        └─product_config
                BUILD
                product_variables.bzl
                

```




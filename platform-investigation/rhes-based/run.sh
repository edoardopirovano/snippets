#!/bin/bash

yum install -y strace gcc glibc-devel.x86_64 glibc-devel.i686 libgcc.i686 libstdc++-devel.i686 ncurses-devel.i686
gcc -m32 main.c -o main32
gcc main.c -o main64
strace -E LD_PRELOAD='xxxxxx/platform_$PLATFORM-lib_$LIB/xxxxxx' /main32 2>&1 | sed -n 's/.*xxxxxx\/\(.*\)\/xxxxxx.*/\1/p' | sort -u > /output32
strace -E LD_PRELOAD='xxxxxx/platform_$PLATFORM-lib_$LIB/xxxxxx' /main64 2>&1 | sed -n 's/.*xxxxxx\/\(.*\)\/xxxxxx.*/\1/p' | sort -u > /output64

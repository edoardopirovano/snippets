#!/bin/bash

apt update
apt install -y strace gcc gcc-multilib
gcc -m32 main.c -o main32
gcc main.c -o main64
strace -E LD_PRELOAD='xxxxxx/platform_$PLATFORM-lib_$LIB/xxxxxx' /main32 2>&1 | sed -n 's/.*xxxxxx\/\(.*\)\/xxxxxx.*/\1/p' | sort -u > /output32
strace -E LD_PRELOAD='xxxxxx/platform_$PLATFORM-lib_$LIB/xxxxxx' /main64 2>&1 | sed -n 's/.*xxxxxx\/\(.*\)\/xxxxxx.*/\1/p' | sort -u > /output64

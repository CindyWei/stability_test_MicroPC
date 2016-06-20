#!/usr/bin/env python
#coding=utf-8
import subprocess

def getcpuinfo(info):

    cmd = "adb shell cat /proc/meminfo"
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    while True:
        line = result.stdout.readline()
        if not line:
            break
        elif line.split(":")[0] == "MemFree":
            f = open("cpuinfo.txt", "ab")
            f.write(info + '\n')
            f.write('\n')
            f.write(line + '\n')
            f.close()
    result.wait()

# if __name__ == "__main__":
#     getcpuinfo()


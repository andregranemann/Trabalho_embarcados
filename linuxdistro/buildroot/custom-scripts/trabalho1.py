#!/usr/bin/env python
import os, platform, subprocess, re
import datetime
from typing import Any, Union

now=datetime.datetime.now()

def get_processor_name():
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command ="sysctl -n machdep.cpu.brand_string"
        return subprocess.check_output(command).strip()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub( ".*model name.*:", "", line,1)
    return ""

def get_cpu_usage():
    last_idle = last_total = 0
    with open('/proc/stat') as f:
        fields = [float(column) for column in f.readline().strip().split()[1:]]
    idle, total = fields[3], sum(fields)
    idle_delta, total_delta = idle - last_idle, total - last_total
    last_idle, last_total = idle, total
    utilisation = 100*(1-idle_delta / total_delta)
    return utilisation

def get_uptime():
     try:
         f = open( "/proc/uptime" )
         contents = f.read().split()
         f.close()
     except:
        return "Cannot open uptime file: /proc/uptime"

     total_seconds = float(contents[0])
     return total_seconds;


def getFree():
    free = os.popen("free -h")
    i = 0
    while True:
        i = i + 1
        line = free.readline()
        if i == 2:
            return (line.split()[0:7])

def HardDiskUsage():
    mem = getFree()
    strg='%sb / %sb' %(mem[2], mem[1])
    return strg

def MemUsage():
    mem = str(os.popen('free -t -m').readlines())
    T_ind = mem.index('T')

    mem_G = mem[T_ind + 14:-4]

    S1_ind = mem_G.index(' ')
    mem_T = mem_G[0:S1_ind]
    mem_G1 = mem_G[S1_ind + 8:]
    S2_ind = mem_G1.index(' ')
    mem_U = mem_G1[0:S2_ind]

    tot=round(float(mem_T)-float(mem_U))

    strg = '%sMb / %sMb' %(mem_U, tot)
    return strg




arquivo = open('index.html', 'w')

html= """<!DOCTYPE html>
<html>
<body>

<h1>Target do sistema</h1>

<p> Uptime do sistema: %s segundos</p>

<p> Nome do processador: %s </p>

<p> Uso do processador: %s </p>

<p> HD usado / total: %s </p>

<p> RAM usada / total: %s </p>

<p> Versão do sistema: %s </p>

<p>Relatório gerado em: %s</p>

</body>
</html>
""" %(str(get_uptime()), platform.processor(), str(round(get_cpu_usage(),2))+'%', str(HardDiskUsage()),
      str(MemUsage()), str(platform.version()), str(now.strftime('%d/%m/%Y %H:%M:%S')))
arquivo.write(html)
arquivo.close()

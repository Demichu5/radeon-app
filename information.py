import os
import requests

APP_VERSION = "1.0.0"

hwmon_dir = 0
for i in range(10):
    if(os.path.exists(f"/sys/class/drm/card0/device/hwmon/hwmon{i}")):
        hwmon_dir = i
        break

GPU_CLC = "/sys/class/drm/card0/device/pp_dpm_sclk"
GPU_VOLTAGE = f"/sys/class/drm/card0/device/hwmon/hwmon{hwmon_dir}/in0_input"
GPU_FANS = f"/sys/class/drm/card0/device/hwmon/hwmon{hwmon_dir}/fan1_input"
GPU_TEMP = f"/sys/class/drm/card0/device/hwmon/hwmon{hwmon_dir}/temp1_input"
GPU_VENDOR = "/sys/class/drm/card0/device/vendor"
GPU_VRAM_TOTAL = "/sys/class/drm/card0/device/mem_info_vram_total"
GPU_VRAM_USED = "/sys/class/drm/card0/device/mem_info_vram_used"
GPU_PCI_WIDTH = "/sys/class/drm/card0/device/current_link_width"
GPU_PCI_SPEED = "/sys/class/drm/card0/device/current_link_speed"
GPU_UTILIZATION = "/sys/class/drm/card0/device/gpu_busy_percent"

AMD_VENDOR = 0x1002
NVIDIA_VENDOR = 0x10de
INTEL_VENDOR = 0x8086

import time

def cpuUtil():
    try:
        with open("/proc/stat", "r") as f:
            # Odczytujemy pierwszą linię zawierającą dane o CPU
            cpu_line = f.readline().strip().split()

            # Wyciągamy odpowiednie wartości z linii (ignorujemy pierwszy element "cpu")
            user, nice, system, idle, iowait = map(int, cpu_line[1:6])

            # Obliczamy procentowe zużycie CPU
            total = user + nice + system + idle + iowait
            active = user + nice + system
            cpu_usage = (active / total) * 100

            return cpu_usage

    except FileNotFoundError:
        return 0


def memLoad():
    try:
        with open("/proc/meminfo", "r") as file:
            memInfo = file.readlines()

        memTotal = 0
        memAvailable = 0

        for line in memInfo:
            if(line.startswith("MemTotal")):
                memTotal = int(line.split()[1])
            elif(line.startswith("MemAvailable")):
                memAvailable = int(line.split()[1])

        if((memTotal is not 0)and(memAvailable is not 0)):
            usedMem = ((memTotal/memAvailable)-1)*100
            return usedMem

        return 0
    except FileNotFoundError:
        return 0

def getMemTotal():
    with open("/proc/meminfo", "r") as f:
        for line in f:
            if line.startswith("MemTotal:"):
                return int(line.split()[1]) // 1024 // 1024  # Konwersja z kB na MB
    return "Error"

def getMemSwap():
    with open("/proc/meminfo", "r") as f:
        for line in f:
            if line.startswith("SwapTotal:"):
                return int(line.split()[1]) // 1024 // 1024  # Konwersja z kB na MB
    return "Error"

def getKernelName():
    stream = os.popen('uname -n')
    return stream.read().strip()

def getKernelVer():
    stream = os.popen('uname -r')
    return stream.read().strip()

def checkUpdate():
    url = "http://192.168.0.200/gpu_app_ver.txt"
    try:
        response = requests.get(url)
        latestVer = response.text.strip()

        if latestVer > APP_VERSION:
            return "Out Of Date"
        else:
            return "Up To Date"

    except Exception as e:
        return "Error"

def getCpuModel():
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "model name" in line:
                    cpu_name = line.split(":")[1].strip()
                    if "Core Processor" in cpu_name:
                        cpu_name = " ".join(cpu_name.split()[:-2])
                    return cpu_name
    except Exception as e:
        return f"Error: {e}"

def getGpuModel():
    stream = os.popen("lspci -nn | grep -i 'VGA' | grep -i 'AMD'")
    output = stream.read().strip()
    if output:
        start = output.find("Radeon")
        if start != -1:
            gpu_name = output[start:].split("[")[0].strip()
            gpu_name = gpu_name.split('/')[0].strip()
            return f"AMD {gpu_name}"

    return "Error"

def getGpuDriver():
    stream = os.popen('glxinfo | grep "OpenGL version"')
    output = stream.read().strip()

    if "Mesa" in output:
        parts = output.split()
        for i, part in enumerate(parts):
            if part == "Mesa":
                return "{} {}".format(part, parts[i+1])

    return "Error"

def readFile(filePath):
    try:
        with open(filePath, "r") as file:
            information = file.read()
        return information
    except FileNotFoundError:
        return None

def checkCompatibility():
    vendorInfo = readFile(GPU_VENDOR)
    if(vendorInfo is not None):
        vendorInfo = vendorInfo.strip()
        vendorINT = int(vendorInfo, 16)
        if(vendorINT == AMD_VENDOR):
            return True
    return False

def gpuClock():
    try:
        with open(GPU_CLC, "r") as file:
            for line in file:
                if(line.startswith("1:")):
                    clcValue = line.split()[1].replace('Mhz', '')
                    return int(clcValue)

    except FileNotFoundError:
        return None

def gpuVramLoad(filePath):
    try:
        with open(filePath, "r") as file:
            vram = file.read().strip()
            return ((int(vram) // 1024) // 1024)
    except FileNotFoundError:
        return 0

def gpuVram():
    vramUsed = gpuVramLoad(GPU_VRAM_USED)
    vramTotal = gpuVramLoad(GPU_VRAM_TOTAL)
    usage = (vramUsed / vramTotal) * 100
    return f"{usage:.0f}"

def gpuUTIL():
    try:
        with open(GPU_UTILIZATION, "r") as file:
            util= file.read().strip()
            return int(util)
    except FileNotFoundError:
        return None

def gpuTemp():
    try:
        with open(GPU_TEMP, "r") as file:
            temp = file.read().strip()
            return int(temp) // 1000
    except FileNotFoundError:
        return None

def gpuVolt():
    try:
        with open(GPU_VOLTAGE, "r") as file:
            volt = file.read().strip()
            return int(volt) / 1000
    except FileNotFoundError:
        return None

def gpuFans():
    try:
        with open(GPU_FANS, "r") as file:
            fans = file.read().strip()
            return int(fans)
    except FileNotFoundError:
        return None

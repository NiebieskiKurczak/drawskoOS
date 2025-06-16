import platform
import subprocess

def get_cpu():
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("model name"):
                    return line.split(":")[1].strip()
    except:
        return "Unknown CPU"

def get_ram():
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal"):
                    mem_kb = int(line.split()[1])
                    return f"{round(mem_kb / (1024**2), 1)} GB"
    except:
        return "Unknown RAM"

def get_os():
    try:
        return platform.system() + " " + platform.release()
    except:
        return "Unknown OS"

def get_gpu():
    try:
        output = subprocess.check_output("lspci | grep VGA", shell=True, text=True)
        return output.strip().split(":")[-1].strip()
    except:
        return "Unknown GPU"

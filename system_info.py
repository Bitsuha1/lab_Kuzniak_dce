import os
import datetime
import platform

import psutil

def append_with_limit(buff: list[int], item: int, n: int):
    buff.append(item)
    while len(buff) > n:
        buff.pop(0)

class SystemInfo:
    def __init__(self):
        self.update()
    
    def update(self):
        self.os: str = f"{platform.system()} {platform.release()}"
        self.processor: str = platform.processor()
        self.p_cpu_count: int = psutil.cpu_count(logical=False)
        self.l_cpu_count: int = psutil.cpu_count(logical=True)
        self.ram: int = psutil.virtual_memory().total
        self.partitions: list[str] = [partition.device for partition in psutil.disk_partitions()]
        self.cpu_load: int = psutil.cpu_percent(interval=1)
        self.ram_load: int = psutil.virtual_memory().percent

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_system_info(info: SystemInfo):
    print(f"Update time   : {datetime.datetime.now().isoformat()}")
    print(f"OS            : {info.os}")
    print(f"Processor     : {info.processor}")
    print(f"Cpu count     : {info.p_cpu_count} physical, {info.l_cpu_count} logical")
    print(f"RAM           : {(info.ram / 1024**3):.2f} GB")
    print(f"Partitions    : ", ', '.join(info.partitions))
    print(f"Cpu load      : {info.cpu_load} %")
    print(f"RAM load      : {info.ram_load} %")

if __name__ == "__main__":
    system_info = SystemInfo()
    cpu_last_20: list[int] = []

    while True:
        clear_screen()
        display_system_info(system_info)
        append_with_limit(cpu_last_20, system_info.cpu_load, 20)
        if len(cpu_last_20):
            print(f"\nAverage cpu load of last 20 updates: {(sum(cpu_last_20) / len(cpu_last_20)):.2f} %")
        system_info.update()

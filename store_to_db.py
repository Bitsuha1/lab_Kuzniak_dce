import datetime
import os

from tinydb import TinyDB, Query
import psutil
import matplotlib.pyplot as plt
import time

from system_info import SystemInfo

class ExtendedSystemInfo(SystemInfo):
    def update(self):
        super().update()
        self.disc_usage: float = psutil.disk_usage('/').percent
        self.net = psutil.net_io_counters()

def update_diagnostics(tinydb: TinyDB, ESysInfo: ExtendedSystemInfo, timestamp: str, table_name: str = 'diagnostics'):
    diagnostics = tinydb.table(table_name)
    diagnostics.insert({
        'timestamp'     : timestamp,
        'cpu_usage'     : ESysInfo.cpu_load,
        'memory_usage'  : ESysInfo.ram_load,
        'disk_usage'    : ESysInfo.disc_usage,
        'bytes_sent_MB' : ESysInfo.net.bytes_sent,
        'bytes_recv_MB' : ESysInfo.net.bytes_recv
    })

if __name__ == "__main__":
    db_file: str = "system_diagnostics.json"
    system_info = ExtendedSystemInfo()
    start_time: float = time.time()
    time_vals: list[float] = []
    cpu_vals: list[float] = []
    mem_vals: list[float] = []
    disk_vals: list[float] = []

    if not os.path.exists(db_file):
        open(db_file, "w").close()

    db: TinyDB = TinyDB(db_file)

    while time.time() - start_time < 40:
        timestamp = datetime.datetime.now()
        time_vals.append(timestamp.strftime("%H:%M:%S"))
        cpu_vals.append(system_info.cpu_load)
        mem_vals.append(system_info.ram_load)
        disk_vals.append(system_info.disc_usage)
        update_diagnostics(db, system_info, timestamp.isoformat())
        system_info.update()
         
    plt.figure(figsize=(8, 6))
    plt.plot(time_vals, cpu_vals, label='cpu_load', color='blue')
    plt.plot(time_vals, mem_vals, label='ram_load', color='red')
    plt.plot(time_vals, disk_vals, label='disk_load', color='green')
    plt.title("System productivity, last 40 seconds")
    plt.xlabel("Time, t")
    plt.ylabel("Load, %")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(cpu_vals, mem_vals, disk_vals, c='red', marker='o')
    ax.set_xlabel(r'CPU load, %')
    ax.set_ylabel(r'RAM load, %')
    ax.set_zlabel(r'Disk load, %')
    plt.show()

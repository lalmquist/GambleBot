import psutil

cpu = psutil.cpu_percent(interval = 0.5)
boot = (psutil.boot_time()/100000000)

print(cpu)
print(boot)


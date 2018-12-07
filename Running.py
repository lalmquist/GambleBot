import psutil
found = 0
for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict(attrs=['name'])
    except psutil.NoSuchProcess:
        pass
    if 'Steam.exe' in pinfo['name']:
        found = 1
if found == 1:
    print("Running")
else:
    print("Not Running")

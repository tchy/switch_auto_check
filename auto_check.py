from netmiko import ConnectHandler
from datetime import datetime
import re

with open("device_info.csv", "r", encoding="utf-8-sig") as f:
    # 获取交换机登录信息，去掉第一行数据
    # <序号>,<品牌>,<ip>,<账号>,<密码>
    device_info = f.read().split("\n")[1:]

for index, info in enumerate(device_info):
    device_type = info.split(",")[1]
    ipaddr =   info.split(",")[2]
    username = info.split(",")[3]
    password = info.split(",")[4]
    out_info = "log for:" + ",".join([str(index+1), device_type, ipaddr, username])
    
    print(str(datetime.now())+" connecting to device {}".format(ipaddr))
    device_connect = {}
    device_connect = {
        'device_type': device_type,
        'host':   ipaddr,
        'username': username,
        'password': password,
        'port' : 22,      # optional, defaults to 22
        'secret': '',     # optional, defaults to ''
    }
    print(device_connect)
    conect = ConnectHandler(**device_connect)
    conect.enable()

    _clock = conect.send_command("dis clock")
    print(_clock)
    clock = _clock.split("\n")[0].replace(" bj","")
    print(clock)
    if len(_clock.split("\n")) > 3:
        print("请人工检查clock！")
    print("===============================================")

    _cpu = conect.send_command("dis cpu")
    print(_cpu)
    cpu = re.search("\d+%", _cpu.split("\n")[3]).group()
    print(cpu)
    if len(_cpu.split("\n")) > 5:
        print("请人工检查cpu！")
    print("===============================================")

    _memory = conect.send_command("dis memory")
    print(_memory)
    memory = re.search("(\d+\.?\d*)%", _memory.split("\n")[3]).group(1)
    # 计算内存占用，保留两位小数
    memory = str(round(100 - float(memory),2)) + "%"    
    print(memory)
    if len(_memory.split("\n")) > 7:
        print("请人工检查memory！")
    print("===============================================")

    _power = conect.send_command("dis power")
    print(_power)
    power = re.findall("\d +([a-zA-Z]+)", _power)
    print(power)
    if len(_power.split("\n")) > 5:
        print("请人工检查power！")
    print("===============================================")

    _fan = conect.send_command("dis fan")
    print(_fan)
    fan = re.findall("State    : ([a-zA-Z]+)", _fan)
    print(fan)
    if len(_fan.split("\n")) > 11:
        print("请人工检查fan！")
    print("===============================================")
    
    _environment = conect.send_command("dis environment")
    print(_environment)
    environment = re.findall(" [\d]     hotspot 1 (\d+)", _environment)
    print(environment)
    if len(_environment.split("\n")) > 7:
        print("请人工检查fan！")
    print("===============================================")

    print(str(datetime.now()) + " saveing config from device {}".format(ipaddr))

    out_logs = "\n".join(["\n\n"+"="*80, out_info, "time:"+str(datetime.now()), "<clock>\n"+_clock, 
                        "<cpu>\n"+_cpu, "<memory>\n"+_memory, "<power>\n"+_power,
                         "<fan>\n"+_fan, "<environment>\n"+_environment])
    with open("logs.txt", "a+", encoding="utf-8") as f:
        f.write(out_logs)
    print("===============================================")


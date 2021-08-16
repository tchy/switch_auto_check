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
    out_info = "log for:  " + ",".join([str(index+1), device_type, ipaddr, username])
    
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
    try:
        # 连接交换机
        conect = ConnectHandler(**device_connect)
        conect.enable()

        # 获取系统时钟，并提取
        _clock = conect.send_command("dis clock")
        clock = _clock.split("\n")[0].replace(" bj","")
        if len(_clock.split("\n")) > 3:
            print("请人工检查clock！")
        
        # 获取CPU利用率，并提取五分钟时cpu利用率
        _cpu = conect.send_command("dis cpu")
        cpu = re.search("\d+%", _cpu.split("\n")[3]).group()
        if len(_cpu.split("\n")) > 5:
            print("请人工检查cpu！")
        
        # 获取内存利用率，原数据为空闲内存率，经计算得到利用率
        _memory = conect.send_command("dis memory")
        memory = re.search("(\d+\.?\d*)%", _memory.split("\n")[3]).group(1)

        # 计算内存占用，保留两位小数
        memory = str(round(100 - float(memory),2)) + "%"    
        if len(_memory.split("\n")) > 7:
            print("请人工检查memory！")
        
        # 获取设备日志， “dis log” 命令运行报错，暂未实现
        
        # 获取电源模块状态，有两个PowerID，列表存储
        _power = conect.send_command("dis power")
        power = re.findall("\d +([a-zA-Z]+)", _power)
        if len(_power.split("\n")) > 5:
            print("请人工检查power！")
        
        # 获取设备风扇状态，有两个风扇，列表依次存储
        _fan = conect.send_command("dis fan")
        fan = re.findall("State    : ([a-zA-Z]+)", _fan)
        if len(_fan.split("\n")) > 11:
            print("请人工检查fan！")
        # 获取设备温度(℃)，可能有多个测温点，列表依次存储
        _environment = conect.send_command("dis environment")
        environment = re.findall(" [\d]     hotspot 1 (\d+)", _environment)
        if len(_environment.split("\n")) > 7:
            print("请人工检查fan！")

        print(str(datetime.now()) + " saveing config from device {}".format(ipaddr))
        
        # 写入日志（logs.txt），完整记录
        out_logs = "\n".join(["\n\n"+"="*80, out_info, "time:"+str(datetime.now()), "<clock>\n"+_clock, 
                            "<cpu>\n"+_cpu, "<memory>\n"+_memory, "<power>\n"+_power,
                            "<fan>\n"+_fan, "<environment>\n"+_environment])
        with open("logs.txt", "a+", encoding="utf-8") as f:
            f.write(out_logs)
        
        # 写入日志（short_logs.txt），提取关键运维数据
        short_logs = "\n".join(["="*80, out_info, "time:  "+str(datetime.now()), "clock:  "+clock, 
                            "cpu:  "+cpu, "memory:  "+memory, "power:"+",".join(power),
                            "fan:  "+",".join(fan), "environment:  "+",".join(environment)+"\n"])
        with open("short_logs.txt", "a+", encoding="utf-8") as f:
            f.write(short_logs)    
    except Exception as e:
        print("发生以下异常：\n%s\n%s"%(e,"="*40))

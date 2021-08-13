from netmiko import ConnectHandler
from datetime import datetime
import re

with open("device_info.csv", "r", encoding="utf-8-sig") as f:
    # 获取交换机登录信息，去掉第一行数据
    # <序号>,<品牌>,<ip>,<账号>,<密码>
    device_info = f.read().split("\n")[1:]

for info in device_info:
    device_type = info.split(",")[1]
    ipaddr =   info.split(",")[2]
    username = info.split(",")[3]
    password = info.split(",")[4]
    
    print(str(datetime.now())+"connecting to device {}".format(ipaddr))
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
    _ = conect.send_command("dis clock")
    print(_)
    clock = _.split("\n")[0].replace(" bj","")
    print(clock)
    print("===============================================")
    _ = conect.send_command("dis cpu")
    print(_)
    cpu = re.search("\d+%", _.split("\n")[3]).group()
    print(cpu)
    print("===============================================")
    _ = conect.send_command("dis memory")
    print(_)
    mem = re.search("\d+\.?\d*%", _.split("\n")[3]).group()
    print(mem)
    print("===============================================")


    print(str(datetime.now()) + "saveing config from device {}".format(ipaddr))
    #f = open("dev_"+ipaddr+"_cfg","w")
    #f.write(running_config)
    #f.close()
    print("===============================================")


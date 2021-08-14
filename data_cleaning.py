import re
with open("dev_10.95.54.130_cfg", "r") as f:
    _ = f.read()
    memory = re.search("(\d+\.?\d*)%", _.split("\n")[3]).group(1)
    memory = str(round(100 - float(memory),2)) + "%"
    print(memory)

def get_info(message):
    pass

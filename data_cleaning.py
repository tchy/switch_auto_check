import re
with open("dev_10.95.54.130_cfg", "r") as f:
    _ = f.read()
    print(_.split("\n")[0].replace(" bj","") )

def get_info(message):
    pass

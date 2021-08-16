#!/usr/bin/python
# -*- coding=utf-8 -*-

# ======================================================================
# Note：这种方法可以实现输入显示星号，而且还有退格功能，但该方法仅在Windows上使用
import msvcrt
def pwd_input():    
    chars = []   
    while True:  
        try:  
            newChar = msvcrt.getch().decode(encoding="utf-8")  
        except:  
            return input("你很可能不是在cmd命令行下运行，密码输入将不能隐藏:")  
        if newChar in '\r\n': # 如果是换行，则输入结束               
             break   
        elif newChar == '\b': # 如果是退格，则删除密码末尾一位并且删除一个星号   
             if chars:    
                 del chars[-1]   
                 msvcrt.putch('\b'.encode(encoding='utf-8')) # 光标回退一格  
                 msvcrt.putch( ' '.encode(encoding='utf-8')) # 输出一个空格覆盖原来的星号  
                 msvcrt.putch('\b'.encode(encoding='utf-8')) # 光标回退一格准备接受新的输入                   
        else:  
            chars.append(newChar)  
            msvcrt.putch('*'.encode(encoding='utf-8')) # 显示为星号  
    return (''.join(chars) )  
# ======================================================================

# ======================================================================
# Note：这种方法可以实现输入显示星号，而且还有退格功能，该方法仅在Linux上使用。
'''
import sys, tty, termios 
def getch():  
  fd = sys.stdin.fileno() 
  old_settings = termios.tcgetattr(fd) 
  try: 
    tty.setraw(sys.stdin.fileno()) 
    ch = sys.stdin.read(1) 
  finally: 
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 
  return ch 

def getpass(maskchar = "*"): 
  password = "" 
  while True: 
    ch = getch() 
    if ch == "\r" or ch == "\n": 
      print 
      return password 
    elif ch == "\b" or ord(ch) == 127: 
      if len(password) > 0: 
        sys.stdout.write("\b \b") 
        password = password[:-1] 
    else: 
      if maskchar != None: 
        sys.stdout.write(maskchar) 
      password += ch 
'''
# ======================================================================

# ======================================================================
# Note：这种方法很安全，但是看不到输入的位数，让人看着有点不太习惯，而且没有退格效果。通用全平台。
'''
import getpass
input = getpass.getpass("Please input your password:")
'''
# ======================================================================

if __name__ == '__main__':
    print("Please input your password:")
    pwd = pwd_input()  
    print("\nyour password is:{0}".format(pwd))

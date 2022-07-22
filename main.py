# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tkinter import *
#import tkMessageBox
import tkinter as tk
import io
import random
import subprocess
import string
import adbutils
from adbutils import adb as adbclient
import threading
from threading import Lock,Thread
import time,os

device_receive=0
device_send=0
device_conf=0
pairmode=0
device_wifi = 0
host_wifi = 0
serial_enc=''
def buttonCallBack():
    global device_receive
    global device_send
    global pairmode
    global device_wifi
    global host_wifi
    global device_conf
    global serial_enc
    device_receive=0
    device_send=0
    if device_wifi==1 or host_wifi==1 or device_conf==1:
        return
    for d in adbclient.device_list():
        if d.serial == '0123456789ABCDEF':
            device_receive += 1
#            serialdmac = d.shell("cat /sys/class/net/wlan0/address")
#            if serialdmac.encode().find('cat: can'.encode()) != -1:
#                label['text'] = '接收端wifi模块有问题，请换一个板！'
#                label.config(fg='red')
#                pairmode = 3
#                return
        else:
            device_send += 1
            serial = d.shell("cat /sys/class/net/wlan0/address")

            count=0
            for letter in serial:
                sStr1 = chr (ord(serial[count])+count+5)
                if count==0 :
                    serial_enc=sStr1
                else :
                    serial_enc+= sStr1
                count=count+1
#            print(serial_enc)
        #            for (i = 0; i < maclength; i++)
#            print(serial)
#            if serial.encode().find('cat: can'.encode())!=-1 :
#                print("error222")
#                label['text'] = '发射端wifi模块有问题，请换一个板！'
#                label.config(fg='red')
#                pairmode = 3
#                return

    if device_receive > 0 and device_receive < 2 and device_send > 0 and device_send < 2 :
#        label['text'] = '配对中...'
        pairmode=1
        for d in adbclient.device_list():
            if d.serial=='0123456789ABCDEF':
#                rtn = d.shell("cat /data/misc/wifi/lollipop.conf")
                d.sync.pull("/data/misc/wifi/lollipop.conf", "dlollipop.conf")

                fdr = open('dlollipop.conf', 'rb')
                if fdr==-1:
                    label['text'] = '配对失败，配置文件读取失败！'
                    label.config(fg='red')
                    pairmode = 3
                    return
                strr=fdr.read()
                fdr.close()
                strd=b''
                strh=b''
                while strr.find('\n'.encode())>0 :
                    sStr1 = strr[0:strr.find('\n'.encode()) + 1]
                    strr = strr[strr.find('\n'.encode()) + 1:]
                    if sStr1.find('device_name_prefix='.encode()) == 0:
                        strd=sStr1
                    elif sStr1.find('device_name='.encode())==0 :
                        strh=sStr1
                        strn=b'function_mode=DLNA\n'
                        strh+=strn
                        strd+=sStr1
                    elif sStr1.find('hm_mode='.encode()) == 0:
                        strmac=b'hm_mode=%s\n'%(serial_enc.encode())
                        strd +=strmac
                    elif sStr1.find('config='.encode())!=-1 :
                        strn=b'config=0\n'
                        strd+=strn
                    elif sStr1.find('softap_password='.encode())== 0:
                        ran=random.randint(10000000,99999999)
                        sStr1=b'softap_password=%d\n'%(ran)
                        strd+=sStr1
                        sStr1=b'password=%d\n'%(ran)
                        strh+=sStr1
                    else :
                        strd+=sStr1
                if  strd!=b'' and strh!=b'' :
                    for d in adbclient.device_list():
                     if d.serial == '0123456789ABCDEF':
                        d.sync.push(io.BytesIO(strd), "/data/misc/wifi/lollipop.conf")
#                        time.sleep(1)
#                        d.shell("reboot")
#                        print("Hello Python")
                     else:
                        d.sync.push(io.BytesIO(strh), "/userdata/lollipop.conf")
                        d.sync.push(io.BytesIO(strh), "/userdata/lollipop.bak")
                        time.sleep(0.2)
                        d.shell("rmmod /vendor/lib/modules/8821cs.ko")
                        d.shell("reboot")
                        pairmode=2
                        label['text'] = '配对成功！'
                        label.config(fg='blue')
                else :
                        label['text'] = '配对失败！'
                        label.config(fg='red')
                        pairmode = 3
#                        print("Hello Python")
#    for d in adb.device_list(): 
#        if d.serial=='0123456789ABCDEF':
#	        dreceive.sync.pull("/data/misc/wifi/lollipop.conf", "lollipop.conf")	

    else :
             print("error")
#   tkMessageBox.showinfo( "Hello Python", "Hello Runoob")
def detectadbdevice(ctime):
    global pairmode
    global device_wifi
    global host_wifi
    global device_conf
    while True :
        device_usb = 0
        host_usb = 0
        if pairmode == 2:
#            pairmode = 3
#            print('reboot')
            for d in adbclient.device_list():
                if d.serial == '0123456789ABCDEF':
                    time.sleep(0.2)
                    d.shell("reboot")
                    time.sleep(3)
                    pairmode = 0
        elif pairmode == 3:
            time.sleep(5)
            pairmode = 0
        elif pairmode==0 :
          for d in adbclient.device_list():
            if d.serial == '0123456789ABCDEF':
                device_usb += 1
                rtn = d.shell("cat /data/misc/wifi/lollipop.conf")
                if rtn.encode().find('No such file or directory'.encode()) != -1:
                    device_conf=1
                else :
                    device_conf = 0
                serialdmac = d.shell("cat /sys/class/net/wlan0/address")
#                print(serialdmac)
                if serialdmac.encode().find('cat: can'.encode()) != -1:
                    device_wifi=1
                else :
                    device_wifi = 0
#                print(device_wifi)
            else:
                 host_usb+= 1
                 serialhmac = d.shell("cat /sys/class/net/wlan0/address")
#                 print(serialhmac)
                 if serialhmac.encode().find('cat: can'.encode()) != -1:
                     host_wifi = 1
                 else :
                     host_wifi = 0
 #                print(host_wifi)
          if device_usb > 0 and device_usb < 2 and host_usb > 0 and host_usb < 2 and device_wifi==0 and host_wifi==0 and device_conf==0 :
            label['text'] = '检测到发送端和接收端各一，可以配对'
            label.config(fg='blue')
          elif device_wifi == 1 and host_wifi == 1:
              label['text'] = '接收端和发送端wifi模块都有问题，请换板测试！'
              label.config(fg='red')
          elif device_wifi == 0 and host_wifi == 1:
              label['text'] = '发送端wifi模块有问题，请换板测试！'
              label.config(fg='red')
          elif device_wifi == 1 and host_wifi == 0:
              label['text'] = '接收端wifi模块有问题，请换板测试！'
              label.config(fg='red')
          elif  device_conf==1 :
              label['text'] = '接收端配置文件有问题，请换板测试！'
              label.config(fg='red')
          elif device_usb == 0 and host_usb == 0:
              label['text'] = '发送端和接收端都没插入，请插入发送端和接收端各一，再配对！'
              label.config(fg='red')
          elif device_usb > 0 and device_usb < 2 and host_usb == 0:
              label['text'] = '接收端已插入，请再插入发送端再配对！'
              label.config(fg='red')
          elif host_usb > 0 and host_usb < 2 and device_usb == 0:
              label['text'] = '发送端已插入，请再插入接收端再配对！'
              label.config(fg='red')
          else :
             label['text']='检测到多个设备，请插入发送端和接收端各一，再配对'
             label.config(fg='red')
        time.sleep(1)
    else :
        time.sleep(0.1)



root = tk.Tk()

root.title("配对程序V1.1")
cmd = 'adb devices'
res = subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
device_receive=0
device_send=0
#os.system('start /B adb devices')
for d in adbclient.device_list():
    if d.serial=='0123456789ABCDEF':
        device_receive+=1
    else :
      device_send+=1
#print("-", device_receive, device_send)
#	  print(d.serial)
#	print("-", d.serial, d.prop.name, d.prop.model)
#    # print device serial

root.geometry('800x480')
root.maxsize(800,480)
root.minsize(800,480)

frame1 = tk.Frame(root)
frame1.grid()

button = tk.Button(frame1, text="配对", fg = 'blue',height = 4,width = 10,font=50, command=buttonCallBack)
#button.place()
#button.place(relx=0.7, relheight=1, relwidth=0.3)    
#B = tk.Button(frame1, text ="配对", command = helloCallBack)
button.pack()

lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

label = tk.Label(lower_frame,font=50)
label.place(relwidth=1, relheight=1)
#print(device_receive)
#print(device_send)
# and device_send==1
#if device_receive==0 and device_send==0 :
#    label['text'] = '发送端和接收端都没插入，请插入发送端和接收端各一，再配对！'
#    label.config(fg='red')
#elif device_receive > 0 and device_receive < 2 and device_send > 0 and device_send < 2:
#    label['text']='检测到发送端和接收端各一，可以配对'
#    label.config(fg='blue')
 # label.Style.Add('color','red')
#elif  device_receive > 0 and device_receive < 2 and device_send==0:
#    label['text'] = '接收端已插入，请再插入发送端再配对！'
#    label.config(fg='red')
#elif  device_send > 0 and device_send < 2 and device_receive==0 :
#    label['text'] = '发送端已插入，请再插入接收端再配对！'
#    label.config(fg='red')
#else :
#     label['text']='检测到多个设备，请插入发送端和接收端各一，再配对'
#     label.config(fg='red')

detectadbdevice=threading.Thread(target=detectadbdevice,args=('MINT',))
detectadbdevice.start()
root.mainloop()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

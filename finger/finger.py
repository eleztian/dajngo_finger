import serial
import serial.tools.list_ports
import threading
from urllib import request,parse
import time,binascii,re
from PIL import Image
serverhost = 'http://www.elezt.cn/finger/put/'

'''FM180 设备指令'''
VPWD      = 'ef 01 00 00 00 00 01 00 07 13 00 00 00 00 00 1b'   #设备验证
Enroll_c  = 'ef 01 00 00 00 00 01 00 03 10 00 14'               #快速注册
UPIMAGE   = 'ef 01 00 00 00 00 01 00 03 0a 00 0e'               #将图像缓冲区中的图像上传到上位机
LOADCHAR1 = 'ef 01 00 00 00 00 01 00 06 07 01 00 00 00 0f'     #12 从flash中读出指定的模板到charBuffer1
UPCHAR1   = 'ef 01 00 00 00 00 01 00 04 08 01 00 0e'            #12 将charbuffer1 的模板 传到上位机
PS_GetImage = 'ef 01 00 00 00 00 01 00 03 01 00 05'             #12探测手指获取图像
PS_GenChar1  = 'ef 01 00 00 00 00 01 00 04 02 01 00 08'         #12imgbuffer生成特征文件存于charBuffer1
PS_GenChar2  = 'ef 01 00 00 00 00 01 00 04 02 02 00 09'         #12imgbuffer生成特征文件存于charBuffer2
PS_RegModel  = 'ef 01 00 00 00 00 01 00 03 05 00 09'            #12合成特征文件（生成模板）CharBuffer1 与CharBuffer2
PS_StoreChar = 'ef 01 00 00 00 00 01 00 06 06 01 00 00 00 0e'   #12将charBuffer的特征文件存储模板


ser = None
ser_thread = None
Finger_id = None
def getPortList():
    port_list = list(serial.tools.list_ports.comports())
    return port_list
fm180_label = None
fm180_img = None

#验证设备
def connect_fm180(com,batus):
    global ser,ser_thread
    print(com[0:4],batus)
    try:
        ser = serial.Serial(com[0:4],int(batus))
        d = bytes.fromhex(VPWD)
        ser.write(d)
        while 1:
            n = ser.inWaiting()
            str = ser.read(n)
            if str:
                print(str)
                if 1:      #验证
                    ser_thread = threading.Thread(target = ser_fm180_server_task)
                    ser_thread.setDaemon(True)
                    ser_thread.start()
                    return True
                else:
                    return False
    except :
        print('ERROR')
        ser.close()
    return False

def disConnect_fm180():
    global ser,ser_thread
    try:
        ser_thread.sleep(2)
        ser_thread.join()
        ser.close()
        return True
    except:
        return False

def ser_fm180_server_task():
    pass

def getFinger(fingerinfor,fingerimg):
    global fm180_label,fm180_img
    fm180_label = fingerinfor
    fm180_img = fingerimg
    try:
        getFinger = threading.Thread(target = getFinger_task)
        getFinger.setDaemon(True)
        getFinger.start()
        return True
    except:
        return False

def sendComToFM180(com,replay_num,usetime):
    global ser
    try:
        while True:
            d = bytes.fromhex(com)
            print(d)
            ser.write(d)
            count = 0
            while count < usetime:
                if ser.inWaiting() >= replay_num :
                    rec = ser.read(replay_num)
                    if rec:
                        rec_hex_Str = str(binascii.b2a_hex(rec))[2:-1]
                        return rec_hex_Str
                count += 1
                time.sleep(0.001)
            time.sleep(1)
    except Exception as e:
        ser_thread.sleep(1)
        ser_thread.join()
        ser.close()
        print(e)

def FM180_GetImg_GenCharx(charid):
    rec_hex_Str = sendComToFM180(PS_GetImage,12,2000)
    rec_hex_List = re.findall(r'.{2}', rec_hex_Str)
    print(rec_hex_List)
    if rec_hex_List[9] == '00':
        getFingerImage()
        if charid == 1:
            rec_hex_Str = sendComToFM180(PS_GenChar1,12,500)
        else:
            rec_hex_Str = sendComToFM180(PS_GenChar2, 12, 500)
        rec_hex_List = re.findall(r'.{2}', rec_hex_Str)
        print(rec_hex_List)
        if rec_hex_List[9] == '00':
            print(charid,'ok')
            return True
        elif rec_hex_List[9] == '06':
            fm180_label['text'] = '指纹太乱'
        elif rec_hex_List[9] == '07':
            fm180_label['text'] = '特征点太少'
        elif rec_hex_List[9] == '15':
            fm180_label['text'] = '缓冲区没有图像'
        else:
            fm180_label['text'] = '生成失败'
    elif rec_hex_List[9] == '01':
        fm180_label['text'] = '请将手指放在设备上'
    elif rec_hex_List[9] == '03':
        fm180_label['text'] = '录入失败'
    return False

def FM180_PS_RegModel():
    global fm180_label
    rec_hex_Str = sendComToFM180(PS_RegModel, 12, 10000)
    rec_hex_List = re.findall(r'.{2}', rec_hex_Str)
    print(rec_hex_List)
    if rec_hex_List[9] == '00':
        fm180_label['text'] = '合成 ok'
        return True
    elif rec_hex_List[9] == '0a':
        fm180_label['text'] = '不是同一个手指'
    else:
        fm180_label['text'] = '合成失败'
    return False

def getFinger_task():
    global fm180_label
    while True:
        while not FM180_GetImg_GenCharx(1):
            time.sleep(1)
        fm180_label['text'] = '第1次 ok '
        time.sleep(2)
        while not FM180_GetImg_GenCharx(2):
            time.sleep(1)
        fm180_label['text'] = '第2次 ok '
        time.sleep(2)
        if FM180_PS_RegModel():
            print('get ok')
            break
    return True

def readTempToBuffer():
    rec_hex_Str = sendComToFM180(LOADCHAR1,12,500)
    rec_hex_List = re.findall(r'.{2}', rec_hex_Str)
    print(rec_hex_List)
    if rec_hex_List[9] == '00':
        return True
    return False

def getPackFromFm180(pack_size, num):
    global ser
    i = 0
    f = ''
    for i in range(num):
        while ser.inWaiting() < pack_size:
            pass
        rec = ser.read(pack_size)
        rec_str = str(binascii.b2a_hex(rec))[2:-1]
        f += rec_str
    return f

def getTemp():
    global F1,F2
    rec_hex_Str = sendComToFM180(UPCHAR1, 12, 500)
    rec_hex_List = re.findall(r'.{2}', rec_hex_Str)
    print(rec_hex_List)
    if rec_hex_List[9] == '00':
        recpack = getPackFromFm180(267,2)
        print(len(recpack))
        F1 = recpack[0:267*2]
        F2 = recpack[267*2:]
        print('%s\n%s'%(F1,F2))
        return True
    return False

def submit_finger_server(id,F1,F2):
    data = {
        'Id':id,
        'F1':F1,
        'F2':F2,
    }
    data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url = serverhost,data = data)
    try:
        page = request.urlopen(req).read().decode('utf-8')
        if 'OK'in page:
           print('ok')
        else:
            print('信息错误')
    except Exception as e:
        print(e)
def getFingerid():
    req = request.Request(serverhost)
    finger_id = request.urlopen(req).read().decode('utf-8')
    return finger_id[:3]

def getFingerImage():
    global Finger_id,fm180_img
    rec_hex_Str = sendComToFM180(UPIMAGE,12,500)
    img = getPackFromFm180(267,144)
    img_list = re.findall(r'.{18}(.{512}).{4}', img)
    img ="".join(img_list)
    print(img.__len__())
    print(img)
    im = Image.new(size = (256, 288), mode = 'RGB')
    index = 0
    for x in range(288):
        for y in range(256):
            a = int(img[index], 16) << 4
            im.putpixel((y, 287 - x), (a,a,a))
            index += 1
    Finger_id = getFingerid()
    im.save(Finger_id + '.gif')
    fm180_img['image'] = tk.PhotoImage(file=Finger_id+'.gif')

if __name__=="__main__":
    tim = Image.open('000000.bmp')
    for x in range(144):
        for y in range(256):
            print(tim.getpixel((x,y)))
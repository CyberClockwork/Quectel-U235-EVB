# -*- coding: UTF-8 -*-
import log
from audio import TTS
import utime
import _thread
import modem
from machine import Pin


lock = _thread.allocate_lock()
# 设置日志输出级别
log.basicConfig(level=log.INFO)
tts_Log = log.getLogger("TTS")


#根据PCB设置开关
if modem.getDevSN() == 'MPQ22EI060454000P' :
    gpio1 = Pin(Pin.GPIO11, Pin.OUT, Pin.PULL_DISABLE, 1)
    print('GPIO11')
else:
    gpio1 = Pin(Pin.GPIO27, Pin.OUT, Pin.PULL_DISABLE, 1)
    print('GPIO27')


#定义回调函数
def UsrFunc(event):
    global lock
    if event == 2:
        print("开始播放")
    elif event == 3:
        print("停止播放")
    elif event == 4:
        print("播放完成")
        lock.release()

def thread_entry_A(id):
    global lock
    while True:
        print('thread {} is running.'.format(id))
        lock.acquire()
        tts.play(1, 0, 2, '你好') 
        utime.sleep(5)



if __name__ == '__main__':
    # 参数1：device （0：听筒，1：耳机，2：喇叭）
    tts = TTS(2)

    #注册用户回调函数
    tts.setCallback(UsrFunc)
    _thread.start_new_thread(thread_entry_A, ('A',))

    # 获取当前播放音量大小
    volume_num = tts.getVolume()
    tts_Log.info("Current TTS volume is %d" %volume_num)

    # 设置音量为6
    volume_num = 1
    tts.setVolume(volume_num)

    #  参数1：优先级 (0-4)
    #  参数2：打断模式，0表示不允许被打断，1表示允许被打断
    #  参数3：模式 低四位：（1：UNICODE16(Size end conversion)  2：UTF-8  3：UNICODE16(Don't convert)），高四位：wtts_enable，wtts_ul_enable， wtts_dl_enable
    #  参数4：数据字符串 （待播放字符
        

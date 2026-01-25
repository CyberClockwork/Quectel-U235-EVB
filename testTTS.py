# -*- coding: UTF-8 -*-

import log
import audio
import utime
import modem
from machine import Pin

print('固件版本：',modem.getDevFwVersion())

#根据PCB设置开关
if modem.getDevSN() == 'MPQ22EI060454000P' :

    gpio1 = Pin(Pin.GPIO11, Pin.OUT, Pin.PULL_DISABLE, 1)
else:
    gpio1 = Pin(Pin.GPIO27, Pin.OUT, Pin.PULL_DISABLE, 1)


# 设置日志输出级别
log.basicConfig(level=log.INFO)
tts_Log = log.getLogger("TTS")

#定义回调函数
def UsrFunc(event):
    if event == 2:
        print("开始播放")
    elif event == 3:
        print("停止播放")
    elif event == 4:
        print("播放完成")

if __name__ == '__main__':
    # 参数1：device （0：听筒，1：耳机，2：喇叭）
    tts = audio.TTS(2)

    #注册用户回调函数
    tts.setCallback(UsrFunc)

    # 获取当前播放音量大小
    volume_num = tts.getVolume()
    tts_Log.info("Current TTS volume is %d" %volume_num)

    # 设置音量为6
    volume_num = 1
    tts.setVolume(volume_num)

    #  参数1：优先级 (0-4)
    #  参数2：打断模式，0表示不允许被打断，1表示允许被打断
    #  参数3：模式 低四位：（1：UNICODE16(Size end conversion)  2：UTF-8  3：UNICODE16(Don't convert)），高四位：wtts_enable，wtts_ul_enable， wtts_dl_enable
    #  参数4：数据字符串 （待播放字符串）
    tts_play_ret = tts.play(3, 0, 2, '执行播放12345') # 执行播放
    if tts_play_ret == 1:
        print('无法立即播放，加入播放队列')
    elif tts_play_ret == 0:
        print('播放成功')
    utime.sleep(5)

    tts_state = tts.getState()
    print('TTS状态:',tts_state)

    tts_play_ret = tts.play(3,0,2, 'abc')
    if tts_play_ret == 1:
        print('无法立即播放，加入播放队列')
    elif tts_play_ret == 0:
        print('播放成功')

    tts_state = tts.getState()
    print('TTS状态:',tts_state)

    utime.sleep(5)
    tts2 = tts.stopAll()
    if tts2 == -1:
        print('停止失败')
    elif tts2 == 0:
        print('停止成功')

    utime.sleep(3)

    tts_close_ret = tts.close()   # 关闭TTS功能
    if tts_close_ret == -1:
        print('关闭失败')
    elif tts_close_ret == 0:
        print('关闭成功')

    utime.sleep(3)

    tts_2 = audio.TTS(2)
    utime.sleep(3)

    tts_state = tts_2.getState()
    print('TTS状态:',tts_state)

    tts_play_ret = tts_2.play(4,1,2, 'abc')
    if tts_play_ret == 1:
        print('无法立即播放，加入播放队列')
    elif tts_play_ret == 0:
        print('播放成功')

    tts_state = tts_2.getState()
    print('TTS状态:',tts_state)

    tts_2.stopAll()
    tts_2.close()   # 关闭TTS功能


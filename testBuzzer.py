import log
import utime
from machine import Timer,Pin
import checkNet

# 设置日志输出级别
log.basicConfig(level=log.INFO)
Timer_Log = log.getLogger("Timer")

num = 0
state = 1
# 注：EC100YCN支持定时器Timer0 ~ Timer3
t = Timer(Timer.Timer1)
gpio1 = Pin(Pin.GPIO39, Pin.OUT, Pin.PULL_DISABLE, 1)

gpio2 = Pin(Pin.GPIO29, Pin.IN, Pin.PULL_PU, 1)

# 创建一个执行函数，并将timer实例传入
def timer_test(t):
    global num
    global state
    # Timer_Log.info('num is %d' % num)
    # num += 1
    if state ==0:
        gpio1.write(1)
        state =1
    else:
        gpio1.write(0)
        state =0

    if gpio2.read() == 0:
    	Timer_Log.info('num > 10, timer exit')
    	t.stop()   # 结束该定时器实例


if __name__ == '__main__':
    t.start(period=1, mode=t.PERIODIC, callback=timer_test)   # 启动定时器

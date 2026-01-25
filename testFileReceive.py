from machine import Pin,UART

#LOAR设置为透传模式
LoRa_M0 = Pin(Pin.GPIO37, Pin.OUT, Pin.PULL_PU, 0) 
LoRa_M1 = Pin(Pin.GPIO38, Pin.OUT, Pin.PULL_PU, 0) 

uart485 = UART(UART.UART1, 9600, 8, 0, 1, 0)

def UartCallback(para):
    with open("/usr/ReceiveRecord.wav",'ab') as xfile1 :
        UartReadBuf = uart485.read(para[2])
        xfile1.write(UartReadBuf)
        if para[0] == 0:
            print('get data :{}'.format(para[2]))
        else :
            print(para[0])

uart485.set_callback(UartCallback)



        # xfile2.write(filebuf)
        # print(type(filebuf))
        
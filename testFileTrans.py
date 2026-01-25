from machine import UART,Pin
import utime

LoRa_M0 = Pin(Pin.GPIO37, Pin.OUT, Pin.PULL_PU, 0) 
LoRa_M1 = Pin(Pin.GPIO38, Pin.OUT, Pin.PULL_PU, 0) 

LoRa_port = UART(UART.UART1, 9600, 8, 0, 1, 0)

LoRa_port.write('	Hello LoRa UART1\r\n')


with open("/usr/myrecord.wav",'rb') as xfile1 :
	mysendcnt =0
	while True:
		filebuf = xfile1.read(256)
		# print(type(filebuf),filebuf)
		if filebuf == 0:
		    break
		LoRa_port.write(filebuf)
		print('写入',len(filebuf))
		mysendcnt += 1
		print('send ',str(mysendcnt))
		utime.sleep(1)



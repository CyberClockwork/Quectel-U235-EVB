import audio
import utime

def cbRecordBack(args):
    print(args)
    print("record end")
    RecordPath = xMIC.getFilePath("myrecord.wav")
    print(RecordPath)

xMIC = audio.Record(0)
RecoodCheck = xMIC.start("myrecord.wav",5)
if xMIC.exists("myrecord.wav") :
    print('文件存在',RecoodCheck)


xMIC.end_callback(cbRecordBack)
print("END")

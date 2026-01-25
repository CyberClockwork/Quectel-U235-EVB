import gc
import uos

usr = uos.statvfs("/usr")

print('获取usr目录状态信息:', usr)
print('f_bsize – 文件系统块大小，单位字节：', usr[0])
print('f_bfree – 可用块数：', usr[3])
print('usr剩下总空间 {} 字节'.format(usr[0] * usr[3]))
print('usr剩下总空间 {} KB'.format((usr[0] * usr[3])/1024))
print('usr剩下总空间 {} MB'.format((usr[0] * usr[3]) / 1024 / 1024))

bak = uos.statvfs("/bak")

print('获取bak目录状态信息:', bak)
print('f_bsize – 文件系统块大小，单位字节：', bak[0])
print('f_bfree – 可用块数：', bak[3])
print('bak剩下总空间 {} 字节'.format(bak[0] * bak[3]))
print('bak剩下总空间 {} KB'.format((bak[0] * bak[3])/1024))
print('bak剩下总空间 {} MB'.format((bak[0] * bak[3]) / 1024 / 1024))

mem = gc.mem_free()
print('剩余可用RAM空间:{}KB'.format(mem / 1024))

# -*- coding: UTF-8 -*-
import utime
import log
import modem
from machine import Pin,LCD
import gc
import lvgl as lv
from tp import gt9xx

print('固件版本：',modem.getDevFwVersion())

log.basicConfig(log.DEBUG)

log_LCD = log.getLogger('LCD')
log_LVGL = log.getLogger('LVGL')

# LCD initialization parameters
init_480X854_local = (
0x11,0,0,
0xFF,120,5,0x77,0x01,0x00,0x00,0x10,
0xC0,0,2,0xE9,0x03,
0xC1,0,2,0x11,0x02,
0xC2,0,2,0x31,0x08,
0xCC,0,1,0x10,
0xB0,0,16,0x00,0x0D,0x14,0x0D,0x10,0x05,0x02,0x08,0x08,0x1E,0x05,0x13,0x11,0xA3,0x29,0x18,
0xB1,0,16,0x00,0x0C,0x14,0x0C,0x10,0x05,0x03,0x08,0x07,0x20,0x05,0x13,0x11,0xA4,0x29,0x18,
0xFF,0,5,0x77,0x01,0x00,0x00,0x11,
0xB0,0,1,0x6C,
0xB1,0,1,0x43,
0xB2,0,1,0x07,
0xB3,0,1,0x80,
0xB5,0,1,0x47,
0xB7,0,1,0x85,
0xB8,0,1,0x20,
0xB9,0,1,0x10,
0xC1,0,1,0x78,
0xC2,0,1,0x78,
0xD0,0,1,0x88,
0xE0,100,3,0x00,0x00,0x02,
0xE1,0,11,0x08,0x00,0x0A,0x00,0x07,0x00,0x09,0x00,0x00,0x33,0x33,
0xE2,0,13,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0xE3,0,4,0x00,0x00,0x33,0x33,
0xE4,0,2,0x44,0x44,
0xE5,0,16,0x0E,0x60,0xA0,0xA0,0x10,0x60,0xA0,0xA0,0x0A,0x60,0xA0,0xA0,0x0C,0x60,0xA0,0xA0,
0xE6,0,4,0x00,0x00,0x33,0x33,
0xE7,0,2,0x44,0x44,
0xE8,0,16,0x0D,0x60,0xA0,0xA0,0x0F,0x60,0xA0,0xA0,0x09,0x60,0xA0,0xA0,0x0B,0x60,0xA0,0xA0,
0xEB,0,7,0x02,0x01,0xE4,0xE4,0x44,0x00,0x40,
0xEC,0,2,0x02,0x01,
0xED,0,16,0xAB,0x89,0x76,0x54,0x01,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x10,0x45,0x67,0x98,0xBA,
0xFF,0,5,0x77,0x01,0x00,0x00,0x00,
0x3A,0,1,0x77,
0x36,0,1,0x00,
0x35,0,1,0x00,
0x29,0,0)


PWM_LED=Pin(Pin.GPIO8, Pin.OUT, Pin.PULL_PU, 1)
gc.enable()

mipilcd = LCD()
mipilcd.mipi_init(initbuf=bytearray(init_480X854_local), width=480, hight=854,DataLane=2,TransMode=1)

# LVGL初始化
lv.init()
# 创建一个显示缓冲区对象
disp_buf1 = lv.disp_draw_buf_t()
# 显示缓冲区对象大小为：width * height * 2
buf1_1 = bytes(480 * 854 * 2)
disp_buf1.init(buf1_1, None, len(buf1_1))

# 创建LVGL显示驱动对象
disp_drv = lv.disp_drv_t()
# 初始化LVGL显示驱动对象
disp_drv.init()
# 将显示缓冲区对象赋值给驱动对象的draw_buf属性
disp_drv.draw_buf = disp_buf1
# 将LCD对象的刷新回调函数lcd_write赋值给驱动对象的flush_cb属性
disp_drv.flush_cb = mipilcd.lcd_write
# 此处基于实际的屏幕宽度来设置水平分辨率
disp_drv.hor_res = 480
# 此处基于实际的屏幕高度来设置垂直分辨率
disp_drv.ver_res = 854
# 此处设置是否需要旋转
disp_drv.sw_rotate = 1
# 旋转角度
disp_drv.rotated = lv.DISP_ROT._270
# 注册LVGL显示驱动对象
disp_drv.register()

# Touchpad(触摸板)初始化
tp_gt911 = gt9xx(irq=40, reset=20)
tp_gt911.activate()
tp_gt911.init()
print("GT911 init...")

# 创建LVGL输入设备驱动对象
indev_drv = lv.indev_drv_t()
indev_drv.init()
indev_drv.type = lv.INDEV_TYPE.POINTER
# 将Touchpad对象的读取函数read赋值给LVGL输入设备驱动对象的read_cb属性
indev_drv.read_cb = tp_gt911.read
indev_drv.register()
gpio4 = Pin(Pin.GPIO40, Pin.OUT, Pin.PULL_PU, 0)
# 启动LVGL 线程
lv.tick_inc(5)
lv.task_handler()

# 创建一个界面
screen = lv.obj()

# 创建button对象
btn1 = lv.btn(screen)
# button设置位置
btn1.center()
# button添加文字
label = lv.label(btn1)
label.set_text("click")

# 创建样式对象
style_btn = lv.style_t()
style_btn.init()
# 设置背景颜色
style_btn.set_bg_color(lv.palette_main(lv.PALETTE.YELLOW))
# 设置字体颜色
style_btn.set_text_color(lv.palette_darken(lv.PALETTE.YELLOW, 4))

# 给button对象添加样式
btn1.add_style(style_btn, 0)

# 定义事件回调函数
def event_handler(evt):
    code = evt.get_code()
    if code == lv.EVENT.CLICKED:
        print("Clicked event detected")

# 给button对象添加事件，在点击时触发
btn1.add_event_cb(event_handler, lv.EVENT.CLICKED, None)



# Create screen_btn_1
screen_btn_1 = lv.btn(screen)
screen_btn_1_label = lv.label(screen_btn_1)
screen_btn_1_label.set_text("Button")
screen_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_1_label.set_width(lv.pct(100))
screen_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_1.set_pos(190, 111)
screen_btn_1.set_size(100, 50)
# Set style for screen_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_1.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_border_width(2, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_border_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_border_color(lv.color_hex(0xff5e00), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
# screen_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)
# Set style for screen_btn_1, Part: lv.PART.MAIN, State: lv.STATE.FOCUSED.
screen_btn_1.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.FOCUSED)
screen_btn_1.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.FOCUSED)
screen_btn_1.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.FOCUSED)
screen_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.FOCUSED)
screen_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.FOCUSED)
screen_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.FOCUSED)
screen_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.FOCUSED)
# screen_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.FOCUSED)
screen_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.FOCUSED)
# Set style for screen_btn_1, Part: lv.PART.MAIN, State: lv.STATE.PRESSED.
screen_btn_1.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.PRESSED)
screen_btn_1.set_style_bg_color(lv.color_hex(0x1400ff), lv.PART.MAIN|lv.STATE.PRESSED)
screen_btn_1.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.PRESSED)
screen_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.PRESSED)
screen_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.PRESSED)
screen_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.PRESSED)
screen_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.PRESSED)
# screen_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.PRESSED)
screen_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.PRESSED)

# Create screen_led_1
screen_led_1 = lv.led(screen)
screen_led_1.set_brightness(255)
screen_led_1.set_color(lv.color_hex(0x00a1b5))
screen_led_1.set_pos(369, 104)
screen_led_1.set_size(40, 40)

# Create screen_btn_2
screen_btn_2 = lv.btn(screen)
screen_btn_2_label = lv.label(screen_btn_2)
screen_btn_2_label.set_text("Button")
screen_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_2_label.set_width(lv.pct(100))
screen_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_2.set_pos(52, 111)
screen_btn_2.set_size(100, 50)
# Set style for screen_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_2.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_2.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_2.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
# screen_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen.update_layout()

# def screen_event_handler(e):
#     code = e.get_code()
#     if (code == lv.EVENT.PRESSED):
#         pass
#         screen_led_1.set_color(lv.color_hex(0xff0059))
#     if (code == lv.EVENT.RELEASED):
#         pass
#         screen_led_1.set_color(lv.color_hex(0x00ff2a))
# screen.add_event_cb(lambda e: screen_event_handler(e), lv.EVENT.ALL, None)

def screen_btn_1_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.PRESSED):
        pass
        screen_led_1.set_color(lv.color_hex(0xf50000))
    if (code == lv.EVENT.RELEASED):
        pass
        screen_led_1.set_color(lv.color_hex(0x00fa11))
screen_btn_1.add_event_cb(lambda e: screen_btn_1_event_handler(e), lv.EVENT.ALL, None)

lv.scr_load(screen)
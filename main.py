import utime
from wheel import Wheel


TIMER0 = 0
TIMER1 = 1
TIMER2 = 2
CHANNEL0 = 0
CHANNEL1 = 1
CHANNEL2 = 2
CHANNEL3 = 3

LEVEL1 = 1
LEVEL2 = 2
LEVEL3 = 3
LEVEL4 = 4
LEVEL5 = 5
DEFAULT_LEVEL = LEVEL2

left_front = Wheel(19, 20, TIMER0, CHANNEL0, TIMER0, CHANNEL1) # 左前轮
left_back = Wheel(15, 17, TIMER0, CHANNEL2, TIMER0, CHANNEL3) # 左后轮
right_front = Wheel(33, 34, TIMER1, CHANNEL0, TIMER1, CHANNEL1) # 前右轮
right_back = Wheel(35, 30, TIMER1, CHANNEL2, TIMER1, CHANNEL3) # 后右轮

def forward(time_ms):
    left_front.forward(DEFAULT_LEVEL)
    left_back.forward(DEFAULT_LEVEL)
    right_front.forward(DEFAULT_LEVEL)
    right_back.forward(DEFAULT_LEVEL)
    utime.sleep_ms(time_ms)

def back(time_ms):
    left_front.back(LEVEL1)
    left_back.back(LEVEL1)
    right_front.back(LEVEL1)
    right_back.back(LEVEL1)
    utime.sleep_ms(time_ms)

def right(time_ms):
    left_front.forward(DEFAULT_LEVEL)
    left_back.back(DEFAULT_LEVEL)
    right_front.back(DEFAULT_LEVEL)
    right_back.forward(DEFAULT_LEVEL)
    utime.sleep_ms(time_ms)

def left(time_ms):
    left_front.back(DEFAULT_LEVEL)
    left_back.forward(DEFAULT_LEVEL)
    right_front.forward(DEFAULT_LEVEL)
    right_back.back(DEFAULT_LEVEL)
    utime.sleep_ms(time_ms)

def breakcar():
    left_front.break_car()
    left_back.break_car()
    right_front.break_car()
    right_back.break_car()
    utime.sleep_ms(500)

def stop():
    left_front.stop()
    left_back.stop()
    right_front.stop()
    right_back.stop()
    utime.sleep_ms(1000)


forward(2000)
breakcar()
back(2000)
breakcar()
right(3000)
breakcar()
left(3000)
stop()

print('FINISH')

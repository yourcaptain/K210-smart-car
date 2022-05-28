from machine import Timer,PWM
import utime

class Wheel:
    # 正转 pin1 = 1/pwm, pin2 = 0
    # 反转 pin1 = 0, pin2 = 1/pwm
    # 停止 pin1 = 0, pin2 = 0
    # 刹车 pin1 = 1, pin2 = 1
    def __init__(self, pin1, pin2, timer_num1, channel_num1, timer_num2, channel_num2):
        timers = [Timer.TIMER0, Timer.TIMER1, Timer.TIMER2]
        channels = [Timer.CHANNEL0, Timer.CHANNEL1, Timer.CHANNEL2, Timer.CHANNEL3]

        self.pin1 = pin1
        self.pin2 = pin2

        self.timer1 = Timer(timers[timer_num1], channels[channel_num1], mode=Timer.MODE_PWM)
        self.timer2 = Timer(timers[timer_num2], channels[channel_num2], mode=Timer.MODE_PWM)
        self.pwmpin1 = PWM(self.timer1, freq=300, duty=0, pin=self.pin1)
        self.pwmpin2 = PWM(self.timer2, freq=300, duty=0, pin=self.pin2)

        self.unit_duty = 10

    # 前进（档位 1-6档）
    def forward(self, level):
        self.pwmpin1.duty(self.unit_duty * level)
        self.pwmpin2.duty(0)

    # 慢速后退
    def back(self):
        self.pwmpin1.duty(0)
        self.pwmpin2.duty(self.unit_duty) #慢速倒车

    # 后退
    def back(self, level):
        self.pwmpin1.duty(0)
        self.pwmpin2.duty(self.unit_duty * level) #慢速倒车

    # 停车
    def stop(self):
        self.pwmpin1.duty(0)
        self.pwmpin2.duty(0)

    # 刹车
    def break_car(self):
        self.pwmpin1.duty(100)
        self.pwmpin2.duty(100)

# 测试
if __name__ == '__main__':

    TIMER0 = 0
    TIMER1 = 1
    TIMER2 = 2
    CHANNEL0 = 0
    CHANNEL1 = 1
    CHANNEL2 = 2
    CHANNEL3 = 3

    LEFT_FORWARD = Wheel(19, 20, TIMER0, CHANNEL0, TIMER0, CHANNEL1) # 左前轮
    LEFT_BACK = Wheel(15, 17, TIMER0, CHANNEL2, TIMER0, CHANNEL3) # 左前轮
    RIGHT_FORWARD = Wheel(33, 34, TIMER1, CHANNEL0, TIMER1, CHANNEL1) # 左前轮
    RIGHT_BACK = Wheel(35, 30, TIMER1, CHANNEL2, TIMER1, CHANNEL3) # 左前轮

    LEFT_FORWARD.forward(1)
    utime.sleep_ms(1000)
    LEFT_FORWARD.stop()
    #LEFT_FORWARD.forward(2)
    #utime.sleep_ms(500)
    #LEFT_FORWARD.forward(3)
    #utime.sleep_ms(500)
    #LEFT_FORWARD.forward(4)
    #utime.sleep_ms(500)
    #LEFT_FORWARD.forward(5)
    #utime.sleep_ms(500)
    #LEFT_FORWARD.forward(6)
    #utime.sleep_ms(500)
    #LEFT_FORWARD.break_car()
    #utime.sleep_ms(500)
    #LEFT_FORWARD.stop()
    #utime.sleep_ms(500)

    #LEFT_BACK.forward(1)
    #utime.sleep_ms(500)
    #LEFT_BACK.stop()
    #utime.sleep_ms(500)

    #RIGHT_FORWARD.forward(1)
    #utime.sleep_ms(500)
    #RIGHT_FORWARD.stop()
    #utime.sleep_ms(500)

    #RIGHT_BACK.forward(1)
    #utime.sleep_ms(500)
    #RIGHT_BACK.stop()
    #utime.sleep_ms(500)


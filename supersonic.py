from Maix import GPIO
from fpioa_manager import fm
from machine import Timer
import utime

class SuperSonicDistance:

    def __init__(self, trig, echo, timer, channel):
        self.trig = trig
        self.echo = echo

        self.interval_us = 0
        self.distance_mm = -1

        self.timer_period = 100

        fm.register(trig, fm.fpioa.GPIO1, force=True)
        fm.register(echo, fm.fpioa.GPIOHS0, force=True)
        self.TRIG_IO = GPIO(GPIO.GPIO1, GPIO.OUT, value = 0)
        self.ECHO_IO = GPIO(GPIO.GPIOHS0, GPIO.PULL_DOWN, value = 0)

        #
        self.ECHO_IO.irq(self.on_echo_rcved, GPIO.IRQ_FALLING)

        self.timer1 = Timer(timer, channel, mode=Timer.MODE_PERIODIC, period=self.timer_period, unit=Timer.UNIT_US, callback=self.on_timer, arg="none", start=False, priority=1, div=0)

    def get_interval_us(self):
        return self.interval_us

    def get_distance_mm(self):
        return self.distance_mm

    def start(self):
        self.interval_us = 0 #重置
        self.distance_mm = -1

        self.ECHO_IO.value(0) # 初始时设置echo引脚为0  34000
        self.ECHO_IO.irq(self.on_trig_sent, GPIO.IRQ_RISING)

        self.TRIG_IO.value(1)
        utime.sleep_us(21)
        self.TRIG_IO.value(0)

    def on_trig_sent(self, tt):
        print("TRIG SENT")
        self.timer1.start()
        self.ECHO_IO.irq(self.on_echo_rcved, GPIO.IRQ_FALLING)

    def on_echo_rcved(self, pin):
        print("ECHO RCVD")
        self.timer1.stop()
        self.distance_mm = (340 * 10 * 10 * 10) * (self.interval_us/1000000 ) * 0.5 # 按声音在空气中传播速度每秒340米计算单程距离，再换算成毫米

    def on_timer(self, timer):
        print("time up:",timer)
        #print("param:",timer.callback_arg())
        self.interval_us = self.interval_us + self.timer_period
        print(self.interval_us)


if __name__ == "__main__":
    TIMER2 = 2
    CHANNEL0 = 0
    Y9 = 7
    Y10 = 6
    TRIG_PIN = Y9
    ECHO_PIN = Y10
    SUPER_SONIC = SuperSonicDistance(TRIG_PIN, ECHO_PIN, TIMER2, CHANNEL0)
    SUPER_SONIC.start()
    utime.sleep_ms(500)
    print("\n")
    print("distance is " + str(SUPER_SONIC.get_distance_mm()) + "mm")
    print("time is " + str(SUPER_SONIC.get_interval_us()) + "us")






from Maix import GPIO
from fpioa_manager import fm
from machine import Timer
import utime

class SuperSonicDistance:

    def __init__(self, trig, echo):
        self.trig = trig
        self.echo = echo

        self.interval_us_start = 0
        self.interval_us_end = 0
        self.interval_us = 0
        self.distance_mm = -1

        fm.register(trig, fm.fpioa.GPIO7, force=True)
        fm.register(echo, fm.fpioa.GPIOHS0, force=True)
        self.TRIG_IO = GPIO(GPIO.GPIO7, GPIO.OUT, value = 0)
        self.ECHO_IO = GPIO(GPIO.GPIOHS0, GPIO.PULL_DOWN, value = 0)

        #
        self.ECHO_IO.irq(self.on_echo_rcved, GPIO.IRQ_FALLING)



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
        self.ECHO_IO.irq(self.on_echo_rcved, GPIO.IRQ_FALLING)
        self.interval_us_start = utime.ticks_us()

    def on_echo_rcved(self, pin):
        self.interval_us_end = utime.ticks_us()
        self.interval_us = self.interval_us_end - self.interval_us_start
        print("ECHO RCVD")
        print("interval_us: ", self.interval_us)
        self.distance_mm = (340 * 10 * 10 * 10) * (self.interval_us/1000000 ) * 0.5 # 按声音在空气中传播速度每秒340米计算单程距离，再换算成毫米
        print("distance_mm: ", self.distance_mm)



if __name__ == "__main__":
    TIMER2 = 2
    CHANNEL0 = 0
    TRIG_PIN = 27
    ECHO_PIN = 29
    SUPER_SONIC = SuperSonicDistance2(TRIG_PIN, ECHO_PIN)
    SUPER_SONIC.start()
    utime.sleep_ms(500)
    print("\n")
    print("distance is " + str(SUPER_SONIC.get_distance_mm()) + "mm")
    print("time is " + str(SUPER_SONIC.get_interval_us()) + "us")






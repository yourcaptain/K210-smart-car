from machine import Timer,PWM
import utime

class Servo:
    def __init__(self, timer, channel, pin):
        self.TIMER = timer
        self.CHANNEL = channel
        self.PIN = pin
        self.tim = Timer(self.TIMER, self.CHANNEL, mode=Timer.MODE_PWM)
        self.servo = PWM(self.tim, freq=50, duty=0, pin=self.PIN)

    # 旋转 -90度 到 90度
    def rotate(self, angle):
        self.servo.duty((-angle+90)/180*10+2.5)
        utime.sleep_ms(5)

if __name__ == '__main__':
    TIMER2 = 2
    CHANNEL1 = 1
    SERVO_PIN = 9
    servo = Servo(TIMER2, CHANNEL1, SERVO_PIN)

    for index in range(1):
        servo.rotate(-90)
        utime.sleep_ms(1000)

        servo.rotate(0)
        utime.sleep_ms(1000)

        servo.rotate(90)
        utime.sleep_ms(1000)

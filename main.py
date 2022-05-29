import utime, lcd
from duducar import DuduCar
from Maix import GPIO
from fpioa_manager import fm

lcd.init() #初始化 LCD
lcd.clear(lcd.WHITE) #清屏白色

duduCar = DuduCar()
duduCar.radar_init()
fm.register(16, fm.fpioa.GPIO1)
KEY = GPIO(GPIO.GPIO1, GPIO.IN)

while True:
    if KEY.value()==0: #按键被按下
        lcd.clear(lcd.WHITE) #清屏白色
        lcd.draw_string(10, 20, "start " , lcd.BLACK, lcd.WHITE)
        for i in range(100):
            lcd.draw_string(10, 40, "index:"+str(i) , lcd.BLACK, lcd.WHITE)
            obstacle_distance = duduCar.obstacle_distance()
            lcd.draw_string(10, 60, "obstical distance: " + str(obstacle_distance) + "mm", lcd.BLACK, lcd.WHITE)

            if obstacle_distance < 500:
                # 停车观察
                duduCar.stop()
                optimal_angle = duduCar.radar_scan()
                lcd.draw_string(10, 80, "next direction: " + str(optimal_angle) + " degree", lcd.BLACK, lcd.WHITE)
                if optimal_angle < 0:
                    # 左拐
                    duduCar.front_left()
                    lcd.draw_string(10, 200, "front left", lcd.BLACK, lcd.WHITE)
                    utime.sleep_ms(3000)#花3秒时间拐弯
                elif optimal_angle > 0:
                    # 右拐
                    duduCar.front_right()
                    lcd.draw_string(10, 200, "front right", lcd.BLACK, lcd.WHITE)
                    utime.sleep_ms(3000)#花3秒时间拐弯
                else:
                    duduCar.forward()
                    lcd.draw_string(10, 200, "forward", lcd.BLACK, lcd.WHITE)
            else:
                duduCar.forward()
                lcd.draw_string(10, 200, "forward", lcd.BLACK, lcd.WHITE)
                utime.sleep_ms(100)#直行-持续运行100毫秒（期间无需探测障碍物距离）
    else:
        lcd.clear(lcd.WHITE) #清屏白色
        lcd.draw_string(110, 120, "PRESS KEY TO START", lcd.RED, lcd.WHITE)
        duduCar.stop()
        utime.sleep_ms(1000)


import utime
from duducar import DuduCar

duduCar = DuduCar()
duduCar.radar_init()

for i in range(2):
    if duduCar.obstacle_distance() < 300:
        # 停车观察
        duduCar.stop()
        optimal_angle = duduCar.radar_scan()
        if optimal_angle < 0:
            # 左拐
            duduCar.front_left()
            print('left')
        elif optimal_angle > 0:
            # 右拐
            duduCar.front_right()
            print('right')
    else:
        duduCar.forward()
        print('forward')

    utime.sleep_ms(1000)

duduCar.radar_init()
duduCar.stop()

print('FINISH')

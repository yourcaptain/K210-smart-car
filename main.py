import utime
from duducar import DuduCar

duduCar = DuduCar()
# duduCar.radar_scan()
print('obstacle distance ', duduCar.obstacle_distance())

for i in range(1000):
    duduCar.forward(2000)
    if duduCar.obstacle_distance() < 300:
        # 停车观察
        duduCar.stop()
        optimal_angle = duduCar.radar_scan()
        if optimal_angle < 0:
            # 左拐
        else if optimal_angle > 0:
            # 右拐
    # sleep 1秒

breakcar()
back(2000)
breakcar()
right(3000)
breakcar()
left(3000)
stop()

print('FINISH')

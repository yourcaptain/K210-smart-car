import utime
from wheel import Wheel
from supersonic import SuperSonicDistance
from servo import Servo

class DuduCar:

    def __init__(self, distance_threshold):
        self.SUPER_SONIC_TRIG_WAIT_TIME_MS = 80
        self.SERVO_ROTATED_DELAY_MS = 250 #给舵机时间转动到位（假设每次探测旋转不超过45度）（按0.22秒/60度计算）
        self.distance_threshold = distance_threshold

        self.TIMER0 = 0
        self.TIMER1 = 1
        self.TIMER2 = 2
        self.CHANNEL0 = 0
        self.CHANNEL1 = 1
        self.CHANNEL2 = 2
        self.CHANNEL3 = 3

        self.LEVEL1 = 2
        self.LEVEL2 = 3
        self.LEVEL3 = 4
        self.LEVEL4 = 5
        self.LEVEL5 = 6
        self.DEFAULT_LEVEL = self.LEVEL1
        self.DEFAULT_FORWARD_LEVEL = self.LEVEL1
        self.DEFAULT_BACKWARD_LEVEL = self.LEVEL1

        self.left_front = Wheel(19, 20, self.TIMER0, self.CHANNEL0, self.TIMER0, self.CHANNEL1) # 左前轮

        self.right_front = Wheel(33, 34, self.TIMER1, self.CHANNEL0, self.TIMER1, self.CHANNEL1) # 前右轮
        self.right_back = Wheel(35, 30, self.TIMER2, self.CHANNEL2, self.TIMER2, self.CHANNEL3) # 后右轮
        self.left_back = Wheel(15, 17, self.TIMER0, self.CHANNEL2, self.TIMER0, self.CHANNEL3) # 左后轮


        self.TRIG_PIN = 27 # 超声波trig
        self.ECHO_PIN = 29 # 超声波echo
        self.supersonic = SuperSonicDistance(self.TRIG_PIN, self.ECHO_PIN)

        self.SERVO_PIN = 9 #舵机信号
        self.servo = Servo(self.TIMER2, self.CHANNEL1, self.SERVO_PIN)

    def forward(self):
        self.left_front.forward(self.DEFAULT_FORWARD_LEVEL)
        self.left_back.forward(self.DEFAULT_FORWARD_LEVEL)
        self.right_front.forward(self.DEFAULT_FORWARD_LEVEL*1.2)
        self.right_back.forward(self.DEFAULT_FORWARD_LEVEL*1.2)

    def back(self):
        left_front.back(self.DEFAULT_BACKWARD_LEVEL)
        left_back.back(self.DEFAULT_BACKWARD_LEVEL)
        right_back.back(self.DEFAULT_BACKWARD_LEVEL*1.2)
        right_front.back(self.DEFAULT_BACKWARD_LEVEL*1.2)

    # 右方侧移
    def right(self):
        self.right_front.back(self.DEFAULT_LEVEL)
        self.left_front.forward(self.DEFAULT_LEVEL)
        self.left_back.back(self.DEFAULT_LEVEL)
        self.right_back.forward(self.DEFAULT_LEVEL)

    # 左方侧移
    def left(self):
        self.left_front.back(self.DEFAULT_LEVEL)
        self.left_back.forward(self.DEFAULT_LEVEL)
        self.right_front.forward(self.DEFAULT_LEVEL)
        self.right_back.back(self.DEFAULT_LEVEL)

    # 左前方拐弯
    def front_left(self):
        self.left_front.stop()
        self.left_back.forward(self.DEFAULT_FORWARD_LEVEL)
        self.right_front.forward(self.DEFAULT_FORWARD_LEVEL)
        self.right_back.forward(self.DEFAULT_FORWARD_LEVEL)

    # 右前方拐弯
    def front_right(self):
        self.right_front.stop()
        self.left_front.forward(self.DEFAULT_FORWARD_LEVEL)
        self.left_back.forward(self.DEFAULT_FORWARD_LEVEL)
        self.right_back.forward(self.DEFAULT_FORWARD_LEVEL)

    def breakcar(self):
        self.left_front.break_car()
        self.left_back.break_car()
        self.right_front.break_car()
        self.right_back.break_car()

    def stop(self):
        self.left_front.stop()
        self.left_back.stop()
        self.right_front.stop()
        self.right_back.stop()

    def obstacle_distance(self):
        self.servo.rotate(0)
        # 探测N次，取最小距离（作为障碍物距离）
        distances_in_this_degree = []
        for detection_degree in (-10, 0, 0, 10):
            self.servo.rotate(detection_degree)
            utime.sleep_ms(self.SERVO_ROTATED_DELAY_MS)

            self.supersonic.start()
            utime.sleep_ms(self.SUPER_SONIC_TRIG_WAIT_TIME_MS)
            distance_mm = self.supersonic.get_distance_mm()
            distances_in_this_degree.append(distance_mm)
        #
        most_short_one = min(distances_in_this_degree)
        #
        print("distances_in_this_degree:", distances_in_this_degree, " most_long_one: ", most_long_one)
        self.servo.rotate(0)
        return most_short_one

    def radar_init(self):
        self.servo.rotate(0)

    # 雷达扫描，获取最佳前进角度
    # return 最佳前进角度
    def radar_scan(self):
        # 5个方向的障碍物距离
        scan_results = {'-90': 0, '-45': 0, '0': 0, '45': 0, '90': 0}

        #分别扫描5个方向
        self.servo.rotate(0) #舵机返回0度位置-正前方
        for degree in (-90, -45, 0, 45, 90):
            self.servo.rotate(degree)
            utime.sleep_ms(self.SERVO_ROTATED_DELAY_MS)

            # 每个方向探测2次，取最大长度
            distances_in_this_degree = []
            for i in (0, 1):
                self.supersonic.start()
                utime.sleep_ms(self.SUPER_SONIC_TRIG_WAIT_TIME_MS)
                distance_mm = self.supersonic.get_distance_mm()
                print("degree:", degree, " count:", i, " distance is ", distance_mm, "mm")
                distances_in_this_degree.append(distance_mm)
            #
            most_long_one = -1
            for item in distances_in_this_degree:
                if item > most_long_one:
                    most_long_one = item

            #
            scan_results[str(degree)] = most_long_one

        self.servo.rotate(0) #舵机返回0度位置-正前方

        # 取距离最长的方向。先过滤距离超过{self.distance_threshold}的方向，并取其最大值所在方向作为最终目标方向
        # 分三个方向。左（-90， -45）；前（0度）；右（45， 90）
        print('scan_results', scan_results)
        filtered_scan_results = {'left':0, 'forward':0, 'right':0}
        filtered_scan_results['left'] = max(scan_results['-90'], scan_results['-45'])
        filtered_scan_results['forward'] = scan_results['0']
        filtered_scan_results['right'] = max(scan_results['45'], scan_results['90'])
        print('filtered_scan_results', filtered_scan_results)

        the_most_long_distance = 0
        the_most_long_distance_direction = 'unknown'
        for direction in filtered_scan_results:
            distance = filtered_scan_results[direction]
            if distance > the_most_long_distance:
                the_most_long_distance = distance
                the_most_long_distance_direction = direction
        print("the_most_long_distance_direction:", the_most_long_distance_direction)

        # 返回距离最长的方向的角度
        return the_most_long_distance_direction

if __name__ == '__main__':
    OBSTACLE_WARNING_DISTANCE = 500 #毫米
    duduCar = DuduCar(OBSTACLE_WARNING_DISTANCE)
    #duduCar.radar_scan()
    duduCar.obstacle_distance()

    #duduCar.forward()
    #utime.sleep(10)
    #duduCar.stop()

    #for i in range(2):
        #if duduCar.obstacle_distance() < 300:
            ## 停车观察
            #duduCar.stop()
            #optimal_angle = duduCar.radar_scan()
            #if optimal_angle < 0:
                ## 左拐
                #duduCar.front_left()
                #print('left')
            #elif optimal_angle > 0:
                ## 右拐
                #duduCar.front_right()
                #print('right')
        #else:
            #duduCar.forward()
            #print('forward')

        #utime.sleep_ms(1000)





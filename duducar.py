import utime
from wheel import Wheel
from supersonic import SuperSonicDistance
from servo import Servo

class DuduCar:

    def __init__(self):
        self.TIMER0 = 0
        self.TIMER1 = 1
        self.TIMER2 = 2
        self.CHANNEL0 = 0
        self.CHANNEL1 = 1
        self.CHANNEL2 = 2
        self.CHANNEL3 = 3

        self.LEVEL1 = 1
        self.LEVEL2 = 2
        self.LEVEL3 = 3
        self.LEVEL4 = 4
        self.LEVEL5 = 5
        self.DEFAULT_LEVEL = self.LEVEL1
        self.DEFAULT_FORWARD_LEVEL = self.LEVEL2
        self.DEFAULT_BACKWARD_LEVEL = self.LEVEL1

        self.left_front = Wheel(19, 20, self.TIMER0, self.CHANNEL0, self.TIMER0, self.CHANNEL1) # 左前轮
        self.left_back = Wheel(15, 17, self.TIMER0, self.CHANNEL2, self.TIMER0, self.CHANNEL3) # 左后轮
        self.right_front = Wheel(33, 34, self.TIMER1, self.CHANNEL0, self.TIMER1, self.CHANNEL1) # 前右轮
        self.right_back = Wheel(35, 30, self.TIMER1, self.CHANNEL2, self.TIMER1, self.CHANNEL3) # 后右轮


        self.TRIG_PIN = 7 # 超声波trig
        self.ECHO_PIN = 6 # 超声波echo
        self.supersonic = SuperSonicDistance(self.TRIG_PIN, self.ECHO_PIN, self.TIMER2, self.CHANNEL0)

        self.SERVO_PIN = 9 #舵机信号
        self.servo = Servo(self.TIMER2, self.CHANNEL1, self.SERVO_PIN)

    def forward(self, time_ms):
        self.left_front.forward(self.DEFAULT_FORWARD_LEVEL)
        self.left_back.forward(self.DEFAULT_FORWARD_LEVEL)
        self.right_front.forward(self.DEFAULT_FORWARD_LEVEL)
        self.right_back.forward(self.DEFAULT_FORWARD_LEVEL)
        #utime.sleep_ms(time_ms)

    def back(self, time_ms):
        left_front.back(self.DEFAULT_BACKWARD_LEVEL)
        left_back.back(self.DEFAULT_BACKWARD_LEVEL)
        right_front.back(self.DEFAULT_BACKWARD_LEVEL)
        right_back.back(self.DEFAULT_BACKWARD_LEVEL)
        #utime.sleep_ms(time_ms)

    def right(self, time_ms):
        self.left_front.forward(self.DEFAULT_LEVEL)
        self.left_back.back(self.DEFAULT_LEVEL)
        self.right_front.back(self.DEFAULT_LEVEL)
        self.right_back.forward(self.DEFAULT_LEVEL)
        #utime.sleep_ms(time_ms)

    def left(self, time_ms):
        self.left_front.back(self.DEFAULT_LEVEL)
        self.left_back.forward(self.DEFAULT_LEVEL)
        self.right_front.forward(self.DEFAULT_LEVEL)
        self.right_back.back(self.DEFAULT_LEVEL)
        #utime.sleep_ms(time_ms)

    def breakcar(self):
        self.left_front.break_car()
        self.left_back.break_car()
        self.right_front.break_car()
        self.right_back.break_car()
        #utime.sleep_ms(500)

    def stop(self):
        self.left_front.stop()
        self.left_back.stop()
        self.right_front.stop()
        self.right_back.stop()
        #utime.sleep_ms(1000)

    def obstacle_distance(self):
        # 探测N次，取最大长度
        distances_in_this_degree = []
        for i in (0, 1, 3):
            self.supersonic.start()
            utime.sleep_ms(50)
            distance_mm = self.supersonic.get_distance_mm()
            print(" count:", i, " distance is ", distance_mm, "mm")
            distances_in_this_degree.append(distance_mm)
        #
        most_long_one = 0
        for item in distances_in_this_degree:
            if item > most_long_one:
                most_long_one = item
        #
        return most_long_one

    # 雷达扫描，获取最佳前进角度
    # return 最佳前进角度
    def radar_scan(self):
        # 5个方向的障碍物距离
        scan_results = {'-90': 0, '-45': 0, '0': 0, '45': 0, '90': 0}

        #分别扫描5个方向
        for degree in (-90, -45, 0, 45, 90):
            self.servo.rotate(degree)

            # 每个方向探测2次，取最大长度
            distances_in_this_degree = []
            for i in (0, 1):
                self.supersonic.start()
                utime.sleep_ms(500)
                distance_mm = self.supersonic.get_distance_mm()
                print("degree:", degree, " count:", i, " distance is ", distance_mm, "mm")
                distances_in_this_degree.append(distance_mm)
            #
            most_long_one = 0
            for item in distances_in_this_degree:
                if item > most_long_one:
                    most_long_one = item

            #
            scan_results[str(degree)] = most_long_one

        # 取距离最长的方向
        the_most_long_distance = 0
        the_most_long_distance_degree = -1
        for degree in scan_results:
            distance = scan_results[degree]
            if distance > the_most_long_distance:
                the_most_long_distance = distance
                the_most_long_distance_degree = int(degree)

        self.servo.rotate(0) #舵机返回0度位置-正前方

        # 返回距离最长的方向的角度
        print("DEGREE OF THE MOST LONG DISTANCE IS ", the_most_long_distance_degree, " ", the_most_long_distance , 'mm')
        return the_most_long_distance_degree



if __name__ == '__main__':
    duduCar = DuduCar()
    duduCar.radar_scan()
    #print('obstacle distance ', duduCar.obstacle_distance())





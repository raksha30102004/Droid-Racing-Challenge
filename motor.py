import RPi.GPIO as GPIO          
from time import sleep

# Left Motor setup:
# IN1   :   direction control
# ENA   :   speed control
in1 = 14
enA = 15

# Right Motor setup:
# IN2   :   direction control
# ENB   :   speed control
in2 = 23
enB = 24

class Motor:
    def __init__(self):
        self.left_dir = in1
        self.left_en = enA
        self.right_dir = in2
        self.right_en = enB

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.left_dir,GPIO.OUT)
        GPIO.setup(self.left_en,GPIO.OUT)
        GPIO.setup(self.right_dir,GPIO.OUT)
        GPIO.setup(self.right_en,GPIO.OUT)
        self.left_pwm = GPIO.PWM(self.left_en, 100)		# set pwm for M1
        self.right_pwm = GPIO.PWM(self.right_en, 100)	# set pwm for M2

    def forward(self, speed):
        GPIO.output(self.left_dir,GPIO.HIGH)
        GPIO.output(self.right_dir,GPIO.LOW)
        self.left_pwm.start(speed)
        self.right_pwm.start(speed)    
    
    # left wheel direction = forward
    # right wheel direction = backward
    def right(self, speed):
        GPIO.output(self.left_dir,GPIO.HIGH)
        GPIO.output(self.right_dir,GPIO.HIGH)
        self.left_pwm.start(speed)
        self.right_pwm.start(speed-5)

    # left wheel direction = backward
    # right wheel direction = forward
    def left(self, speed):
        GPIO.output(self.left_dir,GPIO.LOW)
        GPIO.output(self.right_dir,GPIO.LOW)
        self.left_pwm.start(speed)
        self.right_pwm.start(speed)

    def back(self, speed):
        GPIO.output(self.left_dir,GPIO.LOW)
        GPIO.output(self.right_dir,GPIO.HIGH)
        self.left_pwm.start(speed)
        self.right_pwm.start(speed)

    def pid_drive(self, left, right):
        GPIO.output(self.left_dir,GPIO.HIGH)
        GPIO.output(self.right_dir,GPIO.LOW)

        # if left speed < 0, reverse left wheel
        if left < 0:
            GPIO.output(self.left_dir,GPIO.LOW)
            left = -left
        # if right speed < 0, reverse left wheel
        if right < 0:
            GPIO.output(self.left_dir,GPIO.HIGH)
            right = -right

        if left > 100:
            GPIO.output(self.left_dir,GPIO.HIGH)
            left = 100
        if right > 100:
            GPIO.output(self.left_dir,GPIO.LOW)
            right = 100
        
        self.left_pwm.start(left)
        self.right_pwm.start(right)

    def stop(self):
        self.left_pwm.start(0)
        self.right_pwm.start(0)

# run = True
# m = Motor()

# speed = 30

# while (run):
#     m.right(speed)
#     sleep(3)
#     m.stop()
#     run = False
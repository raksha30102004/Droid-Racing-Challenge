import cv2
import numpy as np
import math
from motor import Motor
from colours import Blue, Yellow, Green, Obstacle, Arrow
import helper
from pid import PID

# Assign colour filtering
left = Yellow()
right = Blue()
end = Green()
obstacle = Obstacle()
arrow = Arrow()

# enable pi camera:
cap = cv2.VideoCapture(0) 

# enable usb laptop camera:
# cap = cv2.VideoCapture(1) 

car = Motor()
speed = 80
turnSpeed = 60
# speed = 60
# turnSpeed = 40

# Proportional control tuning:
angle_p = 0.47
dist_p = 0.3

# Invoking the command processor and calling the pause command 
input("Press the Enter key to continue: ") 

while True:
    # Read Image
    ret, raw = cap.read()
    image = helper.perspective_warp(raw)
    position = (int(image.shape[1]/2), image.shape[0])
    
    # apply colour filtering
    r_half = helper.right_half(image)
    l_half = helper.left_half(image)
    # take centre parts of camera image
    l = helper.filter(left, helper.right_half(l_half))
    r = helper.filter(right, helper.left_half(r_half))

    # filter obstacle on left and right halves of image
    o_l = helper.filter(obstacle, helper.left_half(image))
    o_r = helper.filter(obstacle, helper.right_half(image))
    angle_l, box_l = helper.detectLine(o_l, "left")
    angle_r, box_r = helper.detectLine(o_r, "right")

    theta_l, lane_l = helper.detectLine(l, "left")
    theta_r, lane_r = helper.detectLine(r, "right")

    error_l = helper.error(lane_l, theta_l) 
    error_r = helper.error(lane_r, theta_r)

    g_l = cv2.cvtColor(o_l, cv2.COLOR_BGR2GRAY) 
    g_r = cv2.cvtColor(o_r, cv2.COLOR_BGR2GRAY) 
    if cv2.countNonZero(g_l) > cv2.countNonZero(g_r):
        error_l = helper.error(lane_l, theta_l) + helper.error(box_l, angle_l)/2
    elif cv2.countNonZero(g_l) <= cv2.countNonZero(g_r):
        error_r = helper.error(lane_r, theta_r) + helper.error(box_r, angle_r)/2

    if angle_l != 0 or angle_r != 0:
        print("l ", angle_l)
        print("r ", angle_r)
    
    # helper.create_guide(theta_l, theta_r, image)
            
    # error_l = helper.error(lane_l, theta_l) + helper.error(box_l, angle_l)/2
    # error_r = helper.error(lane_r, theta_r) + helper.error(box_r, angle_r)/2
    

    # take average of errors:
    if error_l != 0 and error_r != 0:
        error = (error_l+error_r)/2
    # if an error is 0, just take that value
    else:
        error = error_l+error_r
    
    dist_r = helper.distance(lane_r, position)
    dist_l = helper.distance(lane_l, position)
    d_thresh = 250
    p_error = int(abs(error)*angle_p)
    thresh = 5
    if dist_r < d_thresh:
        d_error = int(abs(dist_r - d_thresh)*dist_p)
        print("too close: go left")
        car.pid_drive(speed-d_error, speed+d_error)
        if error < -thresh:
            print("left")
            car.pid_drive(turnSpeed-int(p_error), turnSpeed+int(p_error))
        
    elif dist_l < d_thresh:
        d_error = int(abs(dist_l - d_thresh)*dist_p)
        print("too close: go right")
        car.pid_drive(speed+d_error, speed-d_error)
        if error > thresh:
            print("right")
            car.pid_drive(turnSpeed+int(p_error), turnSpeed-int(p_error))
        
    elif error > thresh:
        print("right")
        car.pid_drive(turnSpeed+p_error, turnSpeed-p_error)
    elif error < -thresh:
        print("left")
        car.pid_drive(turnSpeed-p_error, turnSpeed+p_error)
    else:
        print("forward") 
        car.forward(speed)
    
    # img = cv2.hconcat([l, r]) 

    # cv2.imshow("img", img)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

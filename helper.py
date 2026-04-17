import cv2
import numpy as np
import math

pixel_count = 70

def filter(colour, img):
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array([colour.h_min, colour.s_min, colour.v_min])
    upper = np.array([colour.h_max, colour.s_max, colour.v_max])
    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)
    return result

def left_half(img):
    return img[:, :int(img.shape[1]/2)]

def right_half(img):
    return img[:, int(img.shape[1]/2):]

def detectLine(img, dir):
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    # if no colour detected, return None for angle and lane
    if cv2.countNonZero(grey) < pixel_count:
        return None, []
    
    #Finding edges of the image
    edge_image = cv2.Canny(img,250,200)
    # Finding all the lines in an image based on given parameters
    contours, __ = cv2.findContours(edge_image, 
        cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    j = 0
    if len(contours) > 1:
        # sort from shortest -> longest contour
        num = np.zeros(len(contours))
        for i in range(len(contours)):
            num[i] = contours[i].shape[0]
        sorted = np.argsort(num)
        j = sorted[-1]

    # display longest contour
    # cv2.drawContours(img, contours, j, (0, 255, 0), 3)

    line = contours[j].reshape(-1,2)
    # sort points in increasing order of y
    line = line[line[:, 1].argsort()]

    # take mean of all points along contour
    x1 = int(np.mean(line[:,0]))
    y1 = int(np.mean(line[:,1]))

    # get lowest point on lane
    x2 = line[-1,0]
    y2 = line[-1,1]
    
    # calculate angle
    if abs(x1-x2) == 0:
        return 0, line
        
    angle = calc_angle(x1, x2, y1, y2)

    # cv2.line(img,(x2, y2), (x1, y1),(255,0,0),3)
    # cv2.imshow(dir,img)
    return angle - 90, line


# p1 = centre bottom of camera view
def create_guide(angle_l, angle_r, img):
    y1 = img.shape[0]
    x1 = int(img.shape[1]/2)

    # if no angle found, go forward
    if angle_l == None:
        lx = x1
        ly = 0
    else:
        lx = int(y1 - 100*math.sin(math.radians(angle_l)))
        ly = int(x1 - 100*math.cos(math.radians(angle_l)))
    if angle_r == None:
        rx = x1
        ry = 0
    else:
        rx = int(y1 - 100*math.sin(math.radians(angle_r)))
        ry = int(x1 - 100*math.cos(math.radians(angle_r)))

    # green line = left guide line
    cv2.line(img, (x1, y1), (lx, ly),(0,255,0),3)
    # blue line = right guide line
    cv2.line(img, (x1, y1), (rx, ry),(0,0,255),3)
    cv2.imshow("guides",img)

def error(lane, angle):
    # if no lane or angle found, go forward
    if (angle == None) | (lane == []):
        return 0
    
    return angle

def distance(lane, pos):
    if lane == []:
        return 250

    # calculate distance from car to all lane points
    distance = np.zeros(len(lane))
    for i in range(len(lane)):
        x = lane[i][0] 
        y = lane[i][1] - pos[1]
        distance[i] = math.sqrt(pow(x, 2) + pow(y, 2))
    
    return min(distance)

def detect_obstacle(img, col):
    position = (int(img.shape[1]/2), img.shape[0])

    obstacle = filter(col, img)
    cv2.imshow("o", obstacle)
    theta, box = detectLine(obstacle, "left")
    print(box)
    # get left most obstacle point
    idx_max = obstacle[:,1].argmax()

    max = obstacle[idx_max,:]
    # print(max)
    # get right most obstacle point
    idx_min = obstacle[:,1].argmin()
    min = obstacle[idx_min,:]
    # print(min)

    # angle_l = calc_angle(max[1], position[0], max[0], position[1])
    # angle_r = calc_angle(min[1], position[0], min[0], position[1])

    # print("l: ", angle_l)
    # print("r: ", angle_r)
    

    
def calc_angle(x1, x2, y1, y2):
    angle = math.degrees(math.atan((y1-y2)/(x1-x2)))
    if angle < 0:
        angle = angle + 180
    return angle  

def perspective_warp(img,
                     src=np.float32([(0.2,0.3),(0.8,0.3),(0,0.8),(1,0.8)]),
                     dst=np.float32([(0,0), (1, 0), (0,1), (1,1)]),
                     reverse=False):
    # gets image size and maps the src ratios to actual points in img
    img_size = np.float32([(img.shape[1],img.shape[0])])
    src = src* img_size
    # maps the dst ratios to actual points in the final img
    dst = dst * img_size

    # Given src and dst points, calculate the perspective transform matrix
    M = cv2.getPerspectiveTransform(src, dst)
    # Warp the image 
    if reverse:
        M = cv2.getPerspectiveTransform(dst, src)
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))
    return warped


# # define a video capture object 
# cap = cv2.VideoCapture(1) 

# while True:
#     # Read Image
#     ret, image = cap.read()
#     warp = perspective_warp(image)

#     img = cv2.hconcat([image, warp]) 
#     cv2.imshow("img", img)

#     if cv2.waitKey(1) and 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
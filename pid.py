# PID tuning
Kp = 1
Ki = 1
Kd = 1

p = 1
i = 0
d = 0
speed = 20
prevError = 0

def PID(error):
    global Kp, Ki, Kd, p, i, d, speed, prevError

    p = error
    i = i + error
    d = error - prevError

    Pval = Kp*p
    Ival = Ki*i
    Dval = Kd*d

    PIDval = Pval + Ival + Dval
    prevError = error

    speedL = speed - PIDval
    speedR = speed + PIDval

    if speedL > 100:
        speedL = 100
    if speedR > 100:
        speedR = 100

    return speedL, speedR

# error = [10,9,8,5,2,1,0]

# for e in error:
#     print("p:   ", p)
#     print("i:   ", i)
#     print("d:   ", d)
#     l, r = PID(e)
#     print("speedL:   ", l)
#     print("speedR:   ", r)
#     print()
    

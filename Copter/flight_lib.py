import math
import rospy
from clever import srv
import RPi.GPIO as GPIO
from time import sleep as s
from std_srvs.srv import Trigger

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
p = GPIO.PWM(11, 50)
p.start(0)

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
land = rospy.ServiceProxy('land', Trigger)


def sleep(time):
    rospy.sleep(time)


def get_distance_global(lat1, lon1, lat2, lon2):
    return math.hypot(lat1 - lat2, lon1 - lon2) * 1.113195e5


def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(03, True)
    pwm.ChangeDutyCycle(duty)
    s(1)
    GPIO.output(03, False)
    pwm.ChangeDutyCycle(0)


def take_off(height=10, speed=1):
    navigate(x=0, y=0, z=height, speed=speed, frame_id='body', auto_arm=True)
    sleep(height / speed)


def goto(lat, lon, speed=3):
    navigate_global(lat=lat, lon=lon, z=0, speed=speed, frame_id='body')
    telem = get_telemetry()
    self_lat = telem['lat']
    self_lon = telem['lon']
    distance = get_distance_global(lat, lon, self_lat, self_lon)
    sleep(distance / speed + 5)


def throw_off():
    set_angle(90)
    rospy.sleep(5)
    pwm.stop()
    GPIO.cleanup()


def get_coordinates():
    telem = get_telemetry()
    return telem['lat'], telem['lon']


set_angle(0)

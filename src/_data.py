#!/usr/bin/env python

import rospy
import numpy as np

# from sss_data_generator.msg import hydroacoustic_ping as gen_data
from sss_data_generator.msg import channel_data
from sss_data_generator.srv import *


def create_x_data(x):
    return np.arange(0, x)


def create_image_data(curr_data, out_data):
    curr_data.append(out_data)
    return np.asarray(curr_data)


def take_current_length(got_data):
    return len(got_data)


class Channel1:
    def __init__(self):
        self.last_length = 150
        rospy.wait_for_service('/play/ping')
        play = rospy.ServiceProxy('/play/ping', PlayService)
        data = play([0], False, False)
        rospy.Subscriber('/get/ping/ch0', channel_data, self.callback)
        self.got_msg = channel_data()
        self.got_data = self.got_msg.message

    def callback(self, data):
        self.got_data = data.message

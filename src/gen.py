#!/usr/bin/env python

import rospy
import math as m
import random as r

from dynamic_reconfigure.server import Server as DynamicReconfigureServer
from sss_data_generator.msg import hydroacoustic_ping as par_data
from sss_data_generator.cfg import ParamsConfig as ConfigType


class Generator:
    def __init__(self):
        self.rate = rospy.Rate(1)
        self.A = rospy.get_param('~Amplitude', 430.0)
        self.R = rospy.get_param('~RandomAdd', 30.0)
        self.f = rospy.get_param('~Frequency', 590.0)
        self.MsgLen = rospy.get_param('~MessageLength', 150)
        self.server = DynamicReconfigureServer(ConfigType, self.reconfigure)
        self.ch_1 = rospy.Publisher('Channel_1', par_data, queue_size=10)
        self.ch_2 = rospy.Publisher('Channel_2', par_data, queue_size=10)
        self.msg = par_data()

    def gen_data(self):
        while not rospy.is_shutdown():
            sent_data_1 = [0] * self.MsgLen
            sent_data_2 = [0] * self.MsgLen
            for i in range(self.MsgLen):
                sent_data_1[i] = int(m.fabs(self.A * m.sin(self.f * i) / (i+1)) + r.uniform(0, self.R))
                sent_data_2[i] = int(m.fabs(self.A * m.sin(self.f * i) / (i+1)))
            self.msg.chan_1 = sent_data_1
            self.msg.chan_2 = sent_data_2
            self.ch_1.publish(self.msg)
            self.ch_2.publish(self.msg)
            self.rate.sleep()

    # level is transmitted by Dynamic Reconfigure
    def reconfigure(self, config, level):
        self.A = config["Amplitude"]
        self.R = config["RandomAdd"]
        self.f = config["Frequency"]
        self.MsgLen = config["MessageLength"]
        return config


if __name__ == '__main__':
    rospy.init_node('Channel_1', anonymous=True)
    try:
        x = Generator()
        x.gen_data()
    except rospy.ROSInterruptException:
        pass

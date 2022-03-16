#!/usr/bin/env python

import sys
import rospy
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRunnable, QThreadPool
from UI_SSSPingVisualizerMainWindow import *
from plots import PingGraphicWidget, WaterFallWidget
from _data import *


class ChannelThread(QRunnable):
    def __init__(self, tab, channel, number):
        QRunnable.__init__(self)
        self.number = number
        self.tab = tab
        self.data = channel
        self.img_data = []
        self.flag = False
        self.counter = 0

    def run(self):
        while not rospy.is_shutdown():
            got_data = list(self.data.got_data)
            if self.counter >= 2:
                if self.tab[0].checkbox_2.isChecked() and self.flag is False:
                    self.flag = True
                    self.img_data = []
                    self.tab[2].change_layout_settings()
                if not self.tab[0].checkbox_2.isChecked() and self.flag:
                    self.flag = False
                    self.tab[2].return_layout_settings()
                    self.tab[2].counter_ch = 0
                    self.img_data = []
                if self.data.last_length != take_current_length(self.data.got_data):
                    self.data.last_length = 0
                    self.tab[2].counter_ch = 0
                    self.img_data = []
                self.data.last_length = len(self.data.got_data)
                if self.tab[0].checkbox_1.isChecked():
                    got_data.reverse()
                x = create_x_data(len(got_data))
                y = create_image_data(self.img_data, got_data)
                rospy.loginfo('Received data from channel %s, ping %s', self.number, self.counter-1)
                self.tab[1].update_plot(x, got_data)
                if self.tab[0].checkbox_2.isChecked():
                    self.tab[2].update_waterfall_plot_rev(y, self.tab[0].histogram)
                else:
                    self.tab[2].update_waterfall_plot(y, self.tab[0].histogram)
            self.counter += 1
            rospy.Rate(1).sleep()


class PingVisualizer(PingVisualizerMainWindowUI):
    def __init__(self):
        PingVisualizerMainWindowUI.__init__(self)
        self.tabs_number = 2
        self.tabs = []
        self.channels = []
        for i in range(self.tabs_number):
            self.tabs.append([TabWidget(), PingGraphicWidget(), WaterFallWidget(), i+1])
            if i <= 1:
                if i == 0:
                    self.channels.append(ChannelThread(self.tabs[i], Channel1(), self.tabs[i][3]))
        for i in self.tabs:
            i[0].create_tab(self.tabsWidget, i[3])
            i[1].create_plot()
            i[2].create_waterfall_plot(i[0].histogram)
            add_plots(i[0], i[1].plot_layout, i[2].waterfall_layout)
            i[0].create_splitter(i[1].plot_layout, i[2].waterfall_layout)
            i[1].ping_plot.setXLink(i[2].waterfall_plot)
        QThreadPool.globalInstance().setMaxThreadCount(6)
        QThreadPool.globalInstance().start(self.channels[0])


def add_plots(tab, pp, wp):
    tab.graph_layout.addWidget(pp)
    tab.graph_layout.addWidget(wp)


def main():
    visualizer = QApplication(sys.argv)
    app = PingVisualizer()
    app.show()
    sys.exit(visualizer.exec_())


if __name__ == '__main__':
    try:
        rospy.init_node('Data_receiver', anonymous=True)
        main()
    except rospy.ROSInterruptException:
        pass

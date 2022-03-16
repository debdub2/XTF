#!/usr/bin/env python
import numpy as np
import pyqtgraph as pg

pg.setConfigOptions(antialias=True)


class PingGraphicWidget:
    def __init__(self):
        self.plot_layout = pg.GraphicsLayoutWidget()
        self.ping_plot = self.plot_layout.addPlot()
        self.curve = self.ping_plot.plot(pen='r')

    def create_plot(self):
        self.ping_plot.showGrid(x=True, y=True)
        self.ping_plot.setLabel("left", "Last Ping")
        self.ping_plot.setLimits(xMin=0)
        self.curve.setZValue(900)

    def update_plot(self, data_x, data_y):
        self.curve.setData(data_x, data_y)


class WaterFallWidget:
    def __init__(self):
        self.amount_of_str = 175
        self.counter_ch = 0
        self.waterfall_layout = pg.GraphicsLayoutWidget()
        self.waterfall_plot = self.waterfall_layout.addPlot()
        self.waterfall_image = pg.ImageItem()

    def create_waterfall_plot(self, histogram):
        self.waterfall_plot.setLimits(xMin=0, yMax=0)
        self.waterfall_plot.setYRange(0, -self.amount_of_str)
        self.waterfall_plot.enableAutoRange('y', False)
        self.waterfall_image.scale(1, 1)
        self.waterfall_plot.addItem(self.waterfall_image)
        histogram.setImageItem(self.waterfall_image)

    def update_waterfall_plot(self, data, histogram):
        self.counter_ch += 1
        if self.counter_ch == 1:
            histogram.setImageItem(self.waterfall_image)
            self.waterfall_image.setImage(data.T)
            self.waterfall_image.setPos(0, -self.counter_ch)
        else:
            self.waterfall_image.setImage(data.T, autoLevels=False, autoRange=False)
            self.waterfall_image.setPos(0, -self.counter_ch)

    def update_waterfall_plot_rev(self, data, histogram):
        if self.counter_ch == 1:
            histogram.setImageItem(self.waterfall_image)
            self.waterfall_image.setImage(data.T)
            self.waterfall_image.setPos(0, 0)
        else:
            self.waterfall_image.setImage(data.T, autoLevels=False, autoRange=False)
            self.waterfall_image.setPos(0, 0)

    def change_layout_settings(self):
        self.waterfall_plot.setLimits(yMax=np.Inf, yMin=0)
        self.waterfall_plot.setYRange(0, self.amount_of_str)

    def return_layout_settings(self):
        self.waterfall_plot.setLimits(yMax=0, yMin=-np.Inf)
        self.waterfall_plot.setYRange(0, -self.amount_of_str)

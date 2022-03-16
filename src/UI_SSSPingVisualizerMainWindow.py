#!/usr/bin/env python

import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSplitter, QTabWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QWidget
from PyQt5.QtWidgets import QMainWindow as mw


class PingVisualizerMainWindowUI(mw):
    def __init__(self):
        mw.__init__(self)
        self.setWindowTitle("SSS Ping Visualizer")
        self.setFixedSize(1450, 850)
        self.tabsWidget = QTabWidget()
        self._centralWidget = QWidget(self)
        self._centralLayout = QHBoxLayout()
        self._centralLayout.addWidget(self.tabsWidget)
        self._centralWidget.setLayout(self._centralLayout)
        self.setCentralWidget(self._centralWidget)


class TabWidget:
    def __init__(self):
        self.plot_splitter = QSplitter()
        self.histogram = pg.HistogramLUTItem()
        self.splitter = QSplitter()
        self.checkbox_1 = QCheckBox('&Reversive ping direction')
        self.checkbox_2 = QCheckBox('&Changed flow direction')
        self.tab_layout = QHBoxLayout()
        self.graph_layout = QVBoxLayout()
        self.hist_layout = pg.GraphicsLayoutWidget()

    def create_tab(self, tabs, number):
        tab = QWidget()
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.checkbox_1)
        buttons_layout.addWidget(self.checkbox_2)
        buttons_widget = QWidget()
        buttons_widget.setLayout(buttons_layout)
        vert_layout = QVBoxLayout()
        self.hist_layout.addItem(self.histogram)
        self.histogram.gradient.loadPreset("flame")
        vert_layout.addWidget(self.hist_layout, 6)
        vert_layout.addWidget(buttons_widget, 1)
        control_widget = QWidget()
        control_widget.setLayout(vert_layout)
        graph_widget = QWidget()
        graph_widget.setLayout(self.graph_layout)
        self.tab_layout.addWidget(graph_widget, 5)
        self.tab_layout.addWidget(control_widget, 1)
        tab.setLayout(self.tab_layout)
        tabs.addTab(tab, 'Channel {}'.format(number))

    def create_splitter(self, wid1, wid2):
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.addWidget(wid1)
        self.splitter.addWidget(wid2)
        self.graph_layout.addWidget(self.splitter)

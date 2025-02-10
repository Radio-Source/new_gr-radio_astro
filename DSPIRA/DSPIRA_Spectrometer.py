#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: DSPIRA Spectrometer
# Author: DSPIRA
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from datetime import datetime
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import radio_astro
import numpy as np
import osmosdr
import time
import sip



class DSPIRA_Spectrometer(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "DSPIRA Spectrometer", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("DSPIRA Spectrometer")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "DSPIRA_Spectrometer")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.vec_length = vec_length = 4096
        self.sinc_sample_locations = sinc_sample_locations = np.arange(-np.pi*4/2.0, np.pi*4/2.0, np.pi/vec_length)
        self.samp_rate = samp_rate = 2.5e6
        self.min_integration = min_integration = 16
        self.integration_time2 = integration_time2 = 10
        self.integration_time1 = integration_time1 = .4
        self.timenow = timenow = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        self.sinc = sinc = np.sinc(sinc_sample_locations/np.pi)
        self.short_long_time_scale = short_long_time_scale = int((integration_time2*samp_rate/vec_length/min_integration)/(integration_time1*samp_rate/vec_length/min_integration))
        self.prefix = prefix = ""
        self.freq = freq = 1419e6
        self.ymin = ymin = 0
        self.ymax = ymax = 200
        self.spectrumcapture_toggle = spectrumcapture_toggle = 'False'
        self.save_toggle_csv = save_toggle_csv = "False"
        self.reset_integration_button = reset_integration_button = 0
        self.rectfile = rectfile = prefix + timenow + ".h5"
        self.location = location = 'Anytown'
        self.integration_select = integration_select = 0
        self.graphprint_toggle = graphprint_toggle = "False"
        self.graphinfo = graphinfo = ""
        self.freq_step = freq_step = samp_rate/vec_length
        self.freq_start = freq_start = freq - samp_rate/2
        self.elev = elev = '0'
        self.custom_window = custom_window = sinc*np.hamming(4*vec_length)
        self.collect = collect = "nocal"
        self.clip_toggle = clip_toggle = "True"
        self.az = az = '0'
        self.N_long_integration = N_long_integration = int(short_long_time_scale*(integration_time1*samp_rate/vec_length/min_integration))

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_tab_widget_0 = Qt.QTabWidget()
        self.qtgui_tab_widget_0_widget_0 = Qt.QWidget()
        self.qtgui_tab_widget_0_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_0_widget_0)
        self.qtgui_tab_widget_0_grid_layout_0 = Qt.QGridLayout()
        self.qtgui_tab_widget_0_layout_0.addLayout(self.qtgui_tab_widget_0_grid_layout_0)
        self.qtgui_tab_widget_0.addTab(self.qtgui_tab_widget_0_widget_0, 'Spectrum')
        self.qtgui_tab_widget_0_widget_1 = Qt.QWidget()
        self.qtgui_tab_widget_0_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_0_widget_1)
        self.qtgui_tab_widget_0_grid_layout_1 = Qt.QGridLayout()
        self.qtgui_tab_widget_0_layout_1.addLayout(self.qtgui_tab_widget_0_grid_layout_1)
        self.qtgui_tab_widget_0.addTab(self.qtgui_tab_widget_0_widget_1, 'System Temp/Gain')
        self.top_layout.addWidget(self.qtgui_tab_widget_0)
        self._ymin_range = qtgui.Range(-200, 1000, 10, 0, 5)
        self._ymin_win = qtgui.RangeWidget(self._ymin_range, self.set_ymin, "y-axis min", "counter_slider", float, QtCore.Qt.Horizontal)
        self.qtgui_tab_widget_0_grid_layout_0.addWidget(self._ymin_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.qtgui_tab_widget_0_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.qtgui_tab_widget_0_grid_layout_0.setColumnStretch(c, 1)
        self._ymax_range = qtgui.Range(0, 10000, 10, 200, 5)
        self._ymax_win = qtgui.RangeWidget(self._ymax_range, self.set_ymax, "y-axis max", "counter_slider", float, QtCore.Qt.Horizontal)
        self.qtgui_tab_widget_0_grid_layout_0.addWidget(self._ymax_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.qtgui_tab_widget_0_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.qtgui_tab_widget_0_grid_layout_0.setColumnStretch(c, 1)
        _spectrumcapture_toggle_push_button = Qt.QPushButton('Capture Current Spectrum')
        _spectrumcapture_toggle_push_button = Qt.QPushButton('Capture Current Spectrum')
        self._spectrumcapture_toggle_choices = {'Pressed': 'True', 'Released': 'False'}
        _spectrumcapture_toggle_push_button.pressed.connect(lambda: self.set_spectrumcapture_toggle(self._spectrumcapture_toggle_choices['Pressed']))
        _spectrumcapture_toggle_push_button.released.connect(lambda: self.set_spectrumcapture_toggle(self._spectrumcapture_toggle_choices['Released']))
        self.qtgui_tab_widget_0_grid_layout_0.addWidget(_spectrumcapture_toggle_push_button, 1, 4, 1, 3)
        for r in range(1, 2):
            self.qtgui_tab_widget_0_grid_layout_0.setRowStretch(r, 1)
        for c in range(4, 7):
            self.qtgui_tab_widget_0_grid_layout_0.setColumnStretch(c, 1)
        # Create the options list
        self._save_toggle_csv_options = ['False', 'True']
        # Create the labels list
        self._save_toggle_csv_labels = ['Not writing to file', 'Writing to file']
        # Create the combo box
        # Create the radio buttons
        self._save_toggle_csv_group_box = Qt.QGroupBox("Write to csv files" + ": ")
        self._save_toggle_csv_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._save_toggle_csv_button_group = variable_chooser_button_group()
        self._save_toggle_csv_group_box.setLayout(self._save_toggle_csv_box)
        for i, _label in enumerate(self._save_toggle_csv_labels):
            radio_button = Qt.QRadioButton(_label)
            self._save_toggle_csv_box.addWidget(radio_button)
            self._save_toggle_csv_button_group.addButton(radio_button, i)
        self._save_toggle_csv_callback = lambda i: Qt.QMetaObject.invokeMethod(self._save_toggle_csv_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._save_toggle_csv_options.index(i)))
        self._save_toggle_csv_callback(self.save_toggle_csv)
        self._save_toggle_csv_button_group.buttonClicked[int].connect(
            lambda i: self.set_save_toggle_csv(self._save_toggle_csv_options[i]))
        self.qtgui_tab_widget_0_grid_layout_0.addWidget(self._save_toggle_csv_group_box, 0, 6, 1, 1)
        for r in range(0, 1):
            self.qtgui_tab_widget_0_grid_layout_0.setRowStretch(r, 1)
        for c in range(6, 7):
            self.qtgui_tab_widget_0_grid_layout_0.setColumnStretch(c, 1)
        _reset_integration_button_push_button = Qt.QPushButton('Integration Reset')
        _reset_integration_button_push_button = Qt.QPushButton('Integration Reset')
        self._reset_integration_button_choices = {'Pressed': 1, 'Released': 0}
        _reset_integration_button_push_button.pressed.connect(lambda: self.set_reset_integration_button(self._reset_integration_button_choices['Pressed']))
        _reset_integration_button_push_button.released.connect(lambda: self.set_reset_integration_button(self._reset_integration_button_choices['Released']))
        self.qtgui_tab_widget_0_grid_layout_0.addWidget(_reset_integration_button_push_button, 1, 2, 1, 1)
        for r in range(1, 2):
            self.qtgui_tab_widget_0_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.qtgui_tab_widget_0_grid_layout_0.setColumnStretch(c, 1)
        self._location_tool_bar = Qt.QToolBar(self)
        self._location_tool_bar.addWidget(Qt.QLabel("location (hit 'Enter' after typing)" + ": "))
        self._location_line_edit = Qt.QLineEdit(str(self.location))
        self._location_tool_bar.addWidget(self._location_line_edit)
        self._location_line_edit.editingFinished.connect(
            lambda: self.set_location(str(str(self._location_line_edit.text()))))
        self.qtgui_tab_widget_0_grid_layout_0.addWidget(self._location_tool_bar, 2, 3, 1, 4)
        for r in range(2, 3):
            self.qtgui_tab_widget_0_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 7):
            self.qtgui_tab_widget_0_grid_layout_0.setColumnStretch(c, 1)
        # Create the options list
        self._integration_select_options = [0, 1]
        # Create the labels list
        self._integration_select_labels = ['Short Integration', 'Long Integration']
        # Create the combo box
        # Create the radio buttons
        self._integration_select_group_box = Qt.QGroupBox("Integration Time" + ": ")
        self._integration_select_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._integration_select_button_group = variable_chooser_button_group()
        self._integration_select_group_box.setLayout(self._integration_select_box)
        for i, _label in enumerate(self._integration_select_labels):
            radio_button = Qt.QRadioButton(_label)
            self._integration_select_box.addWidget(radio_button)
            self._integration_select_button_group.addButton(radio_button, i)
        self._integration_select_callback = lambda i: Qt.QMetaObject.invokeMethod(self._integration_select_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._integration_select_options.index(i)))
        self._integration_select_callback(self.integration_select)
        self._integration_select_button_group.buttonClicked[int].connect(
            lambda i: self.set_integration_select(self._integration_select_options[i]))
        self.qtgui_tab_widget_0_grid_layout_0.addWidget(self._integration_select_group_box, 0, 2, 1, 1)
        for r in range(0, 1):
            self.qtgui_tab_widget_0_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.qtgui_tab_widget_0_grid_layout_0.setColumnStretch(c, 1)
        _graphprint_toggle_push_button = Qt.QPushButton('Print Graph to File')
        _graphprint_toggle_push_button = Qt.QPushButton('Print Graph to File')
        self._graphprint_toggle_choices = {'Pressed': "True", 'Released': "False"}
        _graphprint_toggle_push_button.pressed.connect(lambda: self.set_graphprint_toggle(self._graphprint_toggle_choices['Pressed']))
        _graphprint_toggle_push_button.released.connect(lambda: self.set_graphprint_toggle(self._graphprint_toggle_choices['Released']))
        self.qtgui_tab_widget_0_layout_0.addWidget(_graphprint_toggle_push_button)
        self._graphinfo_tool_bar = Qt.QToolBar(self)
        self._graphinfo_tool_bar.addWidget(Qt.QLabel("Info added to png filename (hit 'Enter' after typing)" + ": "))
        self._graphinfo_line_edit = Qt.QLineEdit(str(self.graphinfo))
        self._graphinfo_tool_bar.addWidget(self._graphinfo_line_edit)
        self._graphinfo_line_edit.editingFinished.connect(
            lambda: self.set_graphinfo(str(str(self._graphinfo_line_edit.text()))))
        self.qtgui_tab_widget_0_layout_0.addWidget(self._graphinfo_tool_bar)
        self._elev_tool_bar = Qt.QToolBar(self)
        self._elev_tool_bar.addWidget(Qt.QLabel("elevation (hit 'Enter' after typing)" + ": "))
        self._elev_line_edit = Qt.QLineEdit(str(self.elev))
        self._elev_tool_bar.addWidget(self._elev_line_edit)
        self._elev_line_edit.editingFinished.connect(
            lambda: self.set_elev(str(str(self._elev_line_edit.text()))))
        self.qtgui_tab_widget_0_grid_layout_0.addWidget(self._elev_tool_bar, 3, 0, 1, 2)
        for r in range(3, 4):
            self.qtgui_tab_widget_0_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.qtgui_tab_widget_0_grid_layout_0.setColumnStretch(c, 1)
        # Create the options list
        self._collect_options = ['nocal', 'cal', 'hot', 'cold', 'nocal_nofilter']
        # Create the labels list
        self._collect_labels = ['Filtered spectrum with no calibration', 'Spectrum with calibration', 'Hot calibration', 'Cold calibration', 'Unfiltered spectrum with no calibration']
        # Create the combo box
        # Create the radio buttons
        self._collect_group_box = Qt.QGroupBox("Spectrum Display" + ": ")
        self._collect_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._collect_button_group = variable_chooser_button_group()
        self._collect_group_box.setLayout(self._collect_box)
        for i, _label in enumerate(self._collect_labels):
            radio_button = Qt.QRadioButton(_label)
            self._collect_box.addWidget(radio_button)
            self._collect_button_group.addButton(radio_button, i)
        self._collect_callback = lambda i: Qt.QMetaObject.invokeMethod(self._collect_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._collect_options.index(i)))
        self._collect_callback(self.collect)
        self._collect_button_group.buttonClicked[int].connect(
            lambda i: self.set_collect(self._collect_options[i]))
        self.qtgui_tab_widget_0_grid_layout_0.addWidget(self._collect_group_box, 0, 1, 1, 1)
        for r in range(0, 1):
            self.qtgui_tab_widget_0_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.qtgui_tab_widget_0_grid_layout_0.setColumnStretch(c, 1)
        # Create the options list
        self._clip_toggle_options = ['True', 'False']
        # Create the labels list
        self._clip_toggle_labels = ['Clipped spectrum', 'Full spectrum']
        # Create the combo box
        # Create the radio buttons
        self._clip_toggle_group_box = Qt.QGroupBox("Full or Clipped Spectrum" + ": ")
        self._clip_toggle_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._clip_toggle_button_group = variable_chooser_button_group()
        self._clip_toggle_group_box.setLayout(self._clip_toggle_box)
        for i, _label in enumerate(self._clip_toggle_labels):
            radio_button = Qt.QRadioButton(_label)
            self._clip_toggle_box.addWidget(radio_button)
            self._clip_toggle_button_group.addButton(radio_button, i)
        self._clip_toggle_callback = lambda i: Qt.QMetaObject.invokeMethod(self._clip_toggle_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._clip_toggle_options.index(i)))
        self._clip_toggle_callback(self.clip_toggle)
        self._clip_toggle_button_group.buttonClicked[int].connect(
            lambda i: self.set_clip_toggle(self._clip_toggle_options[i]))
        self.qtgui_tab_widget_0_grid_layout_0.addWidget(self._clip_toggle_group_box, 0, 4, 1, 1)
        for r in range(0, 1):
            self.qtgui_tab_widget_0_grid_layout_0.setRowStretch(r, 1)
        for c in range(4, 5):
            self.qtgui_tab_widget_0_grid_layout_0.setColumnStretch(c, 1)
        self._az_tool_bar = Qt.QToolBar(self)
        self._az_tool_bar.addWidget(Qt.QLabel("azimuth (hit 'Enter' after typing)" + ": "))
        self._az_line_edit = Qt.QLineEdit(str(self.az))
        self._az_tool_bar.addWidget(self._az_line_edit)
        self._az_line_edit.editingFinished.connect(
            lambda: self.set_az(str(str(self._az_line_edit.text()))))
        self.qtgui_tab_widget_0_grid_layout_0.addWidget(self._az_tool_bar, 2, 0, 1, 2)
        for r in range(2, 3):
            self.qtgui_tab_widget_0_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.qtgui_tab_widget_0_grid_layout_0.setColumnStretch(c, 1)
        self.radio_astro_vector_moving_average_0 = radio_astro.vector_moving_average(float,vec_length, short_long_time_scale, reset_integration_button)
        self.radio_astro_systemp_calibration_0 = radio_astro.systemp_calibration(vec_length, collect, samp_rate, freq, prefix, spectrumcapture_toggle, clip_toggle, az, elev, location)
        self.radio_astro_png_print_spectrum_0 = radio_astro.png_print_spectrum(vec_length, samp_rate, freq, prefix, graphprint_toggle, graphinfo)
        self.radio_astro_integration_0 = radio_astro.integration(vec_length, (int(integration_time1*samp_rate/vec_length/min_integration)))
        self.radio_astro_csv_filesink_0 = radio_astro.csv_filesink( vec_length, samp_rate, freq, prefix, save_toggle_csv, integration_select, short_long_time_scale, az, elev, location)
        self.qtgui_vector_sink_f_0_0_1 = qtgui.vector_sink_f(
            vec_length,
            ((freq - samp_rate/2)/1e6),
            ((samp_rate/vec_length)/1e6),
            "Frequency (MHz)",
            "Signal",
            "Spectrum",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0_1.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0_1.set_y_axis(ymin, ymax)
        self.qtgui_vector_sink_f_0_0_1.enable_autoscale(True)
        self.qtgui_vector_sink_f_0_0_1.enable_grid(True)
        self.qtgui_vector_sink_f_0_0_1.set_x_axis_units("MHz")
        self.qtgui_vector_sink_f_0_0_1.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0_1.set_ref_level(0)


        labels = ['Spectrum', '', '', '', '',
            '', '', '', '', '']
        widths = [2, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0_1.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0_1.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0_1.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_1_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0_1.qwidget(), Qt.QWidget)
        self.qtgui_tab_widget_0_grid_layout_0.addWidget(self._qtgui_vector_sink_f_0_0_1_win, 4, 0, 20, 10)
        for r in range(4, 24):
            self.qtgui_tab_widget_0_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 10):
            self.qtgui_tab_widget_0_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_vector_sink_f_0_0_0 = qtgui.vector_sink_f(
            vec_length,
            ((freq - samp_rate/2)/1e6),
            ((samp_rate/vec_length)/1e6),
            "Frequency (MHz)",
            "System Temperature (K)",
            "System Temperature",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0_0.set_y_axis(0, 400)
        self.qtgui_vector_sink_f_0_0_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0_0_0.enable_grid(True)
        self.qtgui_vector_sink_f_0_0_0.set_x_axis_units("MHz")
        self.qtgui_vector_sink_f_0_0_0.set_y_axis_units("K")
        self.qtgui_vector_sink_f_0_0_0.set_ref_level(0)


        labels = ['Temp', '', '', '', '',
            '', '', '', '', '']
        widths = [3, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0_0.qwidget(), Qt.QWidget)
        self.qtgui_tab_widget_0_layout_1.addWidget(self._qtgui_vector_sink_f_0_0_0_win)
        self.qtgui_vector_sink_f_0_0 = qtgui.vector_sink_f(
            vec_length,
            ((freq - samp_rate/2)/1e6),
            ((samp_rate/vec_length)/1e6),
            "Frequency (MHz)",
            "Gain",
            "Gain",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0.set_y_axis(0, 5)
        self.qtgui_vector_sink_f_0_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0_0.enable_grid(True)
        self.qtgui_vector_sink_f_0_0.set_x_axis_units("MHz")
        self.qtgui_vector_sink_f_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_ref_level(0)


        labels = ['Gain', '', '', '', '',
            '', '', '', '', '']
        widths = [3, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0.qwidget(), Qt.QWidget)
        self.qtgui_tab_widget_0_layout_1.addWidget(self._qtgui_vector_sink_f_0_0_win)
        self.qtgui_histogram_sink_x_0 = qtgui.histogram_sink_f(
            1024,
            100,
            (-.5),
            .5,
            "System Heartbeat",
            1,
            None # parent
        )

        self.qtgui_histogram_sink_x_0.set_update_time(1)
        self.qtgui_histogram_sink_x_0.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0.enable_grid(False)
        self.qtgui_histogram_sink_x_0.enable_axis_labels(True)


        labels = ['Histogram', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers= [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_histogram_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_histogram_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_histogram_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_histogram_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_histogram_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_histogram_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_histogram_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_histogram_sink_x_0_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0.qwidget(), Qt.QWidget)
        self.qtgui_tab_widget_0_grid_layout_0.addWidget(self._qtgui_histogram_sink_x_0_win, 0, 8, 3, 1)
        for r in range(0, 3):
            self.qtgui_tab_widget_0_grid_layout_0.setRowStretch(r, 1)
        for c in range(8, 9):
            self.qtgui_tab_widget_0_grid_layout_0.setColumnStretch(c, 1)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ''
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(21, 0)
        self.osmosdr_source_0.set_if_gain(0, 0)
        self.osmosdr_source_0.set_bb_gain(0, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.fft_vxx_0 = fft.fft_vcc(vec_length, True, window.rectangular(vec_length), True, 1)
        self.blocks_stream_to_vector_0_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_stream_to_vector_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_float*vec_length,integration_select,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_multiply_const_vxx_0_0_0_0 = blocks.multiply_const_vcc(custom_window[0:vec_length])
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_vcc(custom_window[1*vec_length:2*vec_length])
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc(custom_window[2*vec_length:3*vec_length])
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc(custom_window[-vec_length:])
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(vec_length)
        self.blocks_integrate_xx_0_0_0 = blocks.integrate_ff(min_integration, vec_length)
        self.blocks_delay_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, (3*vec_length))
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, (2*vec_length))
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_complex_to_real_1 = blocks.complex_to_real(vec_length)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_add_xx_0 = blocks.add_vcc(vec_length)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.qtgui_histogram_sink_x_0, 0))
        self.connect((self.blocks_complex_to_real_1, 0), (self.blocks_integrate_xx_0_0_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_stream_to_vector_0_0_0, 0))
        self.connect((self.blocks_delay_0_0_0, 0), (self.blocks_stream_to_vector_0_0_0_0, 0))
        self.connect((self.blocks_integrate_xx_0_0_0, 0), (self.radio_astro_integration_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_complex_to_real_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0, 0), (self.blocks_add_xx_0, 3))
        self.connect((self.blocks_selector_0, 0), (self.radio_astro_systemp_calibration_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_delay_0_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.radio_astro_integration_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.radio_astro_integration_0, 0), (self.radio_astro_vector_moving_average_0, 0))
        self.connect((self.radio_astro_systemp_calibration_0, 1), (self.qtgui_vector_sink_f_0_0, 0))
        self.connect((self.radio_astro_systemp_calibration_0, 2), (self.qtgui_vector_sink_f_0_0_0, 0))
        self.connect((self.radio_astro_systemp_calibration_0, 0), (self.qtgui_vector_sink_f_0_0_1, 0))
        self.connect((self.radio_astro_systemp_calibration_0, 0), (self.radio_astro_csv_filesink_0, 0))
        self.connect((self.radio_astro_systemp_calibration_0, 0), (self.radio_astro_png_print_spectrum_0, 0))
        self.connect((self.radio_astro_vector_moving_average_0, 0), (self.blocks_selector_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "DSPIRA_Spectrometer")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_vec_length(self):
        return self.vec_length

    def set_vec_length(self, vec_length):
        self.vec_length = vec_length
        self.set_N_long_integration(int(self.short_long_time_scale*(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))
        self.set_custom_window(self.sinc*np.hamming(4*self.vec_length))
        self.set_freq_step(self.samp_rate/self.vec_length)
        self.set_short_long_time_scale(int((self.integration_time2*self.samp_rate/self.vec_length/self.min_integration)/(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))
        self.set_sinc_sample_locations(np.arange(-np.pi*4/2.0, np.pi*4/2.0, np.pi/self.vec_length))
        self.blocks_delay_0.set_dly(int(self.vec_length))
        self.blocks_delay_0_0.set_dly(int((2*self.vec_length)))
        self.blocks_delay_0_0_0.set_dly(int((3*self.vec_length)))
        self.blocks_multiply_const_vxx_0.set_k(self.custom_window[-self.vec_length:])
        self.blocks_multiply_const_vxx_0_0.set_k(self.custom_window[2*self.vec_length:3*self.vec_length])
        self.blocks_multiply_const_vxx_0_0_0.set_k(self.custom_window[1*self.vec_length:2*self.vec_length])
        self.blocks_multiply_const_vxx_0_0_0_0.set_k(self.custom_window[0:self.vec_length])
        self.qtgui_vector_sink_f_0_0.set_x_axis(((self.freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))
        self.qtgui_vector_sink_f_0_0_0.set_x_axis(((self.freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))
        self.qtgui_vector_sink_f_0_0_1.set_x_axis(((self.freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))
        self.radio_astro_integration_0.set_n_integrations((int(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))

    def get_sinc_sample_locations(self):
        return self.sinc_sample_locations

    def set_sinc_sample_locations(self, sinc_sample_locations):
        self.sinc_sample_locations = sinc_sample_locations
        self.set_sinc(np.sinc(self.sinc_sample_locations/np.pi))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_N_long_integration(int(self.short_long_time_scale*(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))
        self.set_freq_start(self.freq - self.samp_rate/2)
        self.set_freq_step(self.samp_rate/self.vec_length)
        self.set_short_long_time_scale(int((self.integration_time2*self.samp_rate/self.vec_length/self.min_integration)/(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_vector_sink_f_0_0.set_x_axis(((self.freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))
        self.qtgui_vector_sink_f_0_0_0.set_x_axis(((self.freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))
        self.qtgui_vector_sink_f_0_0_1.set_x_axis(((self.freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))
        self.radio_astro_integration_0.set_n_integrations((int(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))

    def get_min_integration(self):
        return self.min_integration

    def set_min_integration(self, min_integration):
        self.min_integration = min_integration
        self.set_N_long_integration(int(self.short_long_time_scale*(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))
        self.set_short_long_time_scale(int((self.integration_time2*self.samp_rate/self.vec_length/self.min_integration)/(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))
        self.radio_astro_integration_0.set_n_integrations((int(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))

    def get_integration_time2(self):
        return self.integration_time2

    def set_integration_time2(self, integration_time2):
        self.integration_time2 = integration_time2
        self.set_short_long_time_scale(int((self.integration_time2*self.samp_rate/self.vec_length/self.min_integration)/(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))

    def get_integration_time1(self):
        return self.integration_time1

    def set_integration_time1(self, integration_time1):
        self.integration_time1 = integration_time1
        self.set_N_long_integration(int(self.short_long_time_scale*(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))
        self.set_short_long_time_scale(int((self.integration_time2*self.samp_rate/self.vec_length/self.min_integration)/(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))
        self.radio_astro_integration_0.set_n_integrations((int(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))

    def get_timenow(self):
        return self.timenow

    def set_timenow(self, timenow):
        self.timenow = timenow
        self.set_rectfile(self.prefix + self.timenow + ".h5")

    def get_sinc(self):
        return self.sinc

    def set_sinc(self, sinc):
        self.sinc = sinc
        self.set_custom_window(self.sinc*np.hamming(4*self.vec_length))
        self.set_sinc(np.sinc(self.sinc_sample_locations/np.pi))

    def get_short_long_time_scale(self):
        return self.short_long_time_scale

    def set_short_long_time_scale(self, short_long_time_scale):
        self.short_long_time_scale = short_long_time_scale
        self.set_N_long_integration(int(self.short_long_time_scale*(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))

    def get_prefix(self):
        return self.prefix

    def set_prefix(self, prefix):
        self.prefix = prefix
        self.set_rectfile(self.prefix + self.timenow + ".h5")

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_freq_start(self.freq - self.samp_rate/2)
        self.osmosdr_source_0.set_center_freq(self.freq, 0)
        self.qtgui_vector_sink_f_0_0.set_x_axis(((self.freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))
        self.qtgui_vector_sink_f_0_0_0.set_x_axis(((self.freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))
        self.qtgui_vector_sink_f_0_0_1.set_x_axis(((self.freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))

    def get_ymin(self):
        return self.ymin

    def set_ymin(self, ymin):
        self.ymin = ymin
        self.qtgui_vector_sink_f_0_0_1.set_y_axis(self.ymin, self.ymax)

    def get_ymax(self):
        return self.ymax

    def set_ymax(self, ymax):
        self.ymax = ymax
        self.qtgui_vector_sink_f_0_0_1.set_y_axis(self.ymin, self.ymax)

    def get_spectrumcapture_toggle(self):
        return self.spectrumcapture_toggle

    def set_spectrumcapture_toggle(self, spectrumcapture_toggle):
        self.spectrumcapture_toggle = spectrumcapture_toggle
        self.radio_astro_systemp_calibration_0.set_spectrumcapture_toggle(self.spectrumcapture_toggle)

    def get_save_toggle_csv(self):
        return self.save_toggle_csv

    def set_save_toggle_csv(self, save_toggle_csv):
        self.save_toggle_csv = save_toggle_csv
        self._save_toggle_csv_callback(self.save_toggle_csv)
        self.radio_astro_csv_filesink_0.set_save_toggle(self.save_toggle_csv)

    def get_reset_integration_button(self):
        return self.reset_integration_button

    def set_reset_integration_button(self, reset_integration_button):
        self.reset_integration_button = reset_integration_button
        self.radio_astro_vector_moving_average_0.set_reset_integration(self.reset_integration_button)

    def get_rectfile(self):
        return self.rectfile

    def set_rectfile(self, rectfile):
        self.rectfile = rectfile

    def get_location(self):
        return self.location

    def set_location(self, location):
        self.location = location
        Qt.QMetaObject.invokeMethod(self._location_line_edit, "setText", Qt.Q_ARG("QString", str(self.location)))
        self.radio_astro_csv_filesink_0.set_location(self.location)
        self.radio_astro_systemp_calibration_0.set_location(self.location)

    def get_integration_select(self):
        return self.integration_select

    def set_integration_select(self, integration_select):
        self.integration_select = integration_select
        self._integration_select_callback(self.integration_select)
        self.blocks_selector_0.set_input_index(self.integration_select)
        self.radio_astro_csv_filesink_0.set_integration_select(self.integration_select)

    def get_graphprint_toggle(self):
        return self.graphprint_toggle

    def set_graphprint_toggle(self, graphprint_toggle):
        self.graphprint_toggle = graphprint_toggle
        self.radio_astro_png_print_spectrum_0.set_graphprint_toggle(self.graphprint_toggle)

    def get_graphinfo(self):
        return self.graphinfo

    def set_graphinfo(self, graphinfo):
        self.graphinfo = graphinfo
        Qt.QMetaObject.invokeMethod(self._graphinfo_line_edit, "setText", Qt.Q_ARG("QString", str(self.graphinfo)))
        self.radio_astro_png_print_spectrum_0.set_graphinfo(self.graphinfo)

    def get_freq_step(self):
        return self.freq_step

    def set_freq_step(self, freq_step):
        self.freq_step = freq_step

    def get_freq_start(self):
        return self.freq_start

    def set_freq_start(self, freq_start):
        self.freq_start = freq_start

    def get_elev(self):
        return self.elev

    def set_elev(self, elev):
        self.elev = elev
        Qt.QMetaObject.invokeMethod(self._elev_line_edit, "setText", Qt.Q_ARG("QString", str(self.elev)))
        self.radio_astro_csv_filesink_0.set_elev(self.elev)
        self.radio_astro_systemp_calibration_0.set_elev(self.elev)

    def get_custom_window(self):
        return self.custom_window

    def set_custom_window(self, custom_window):
        self.custom_window = custom_window
        self.blocks_multiply_const_vxx_0.set_k(self.custom_window[-self.vec_length:])
        self.blocks_multiply_const_vxx_0_0.set_k(self.custom_window[2*self.vec_length:3*self.vec_length])
        self.blocks_multiply_const_vxx_0_0_0.set_k(self.custom_window[1*self.vec_length:2*self.vec_length])
        self.blocks_multiply_const_vxx_0_0_0_0.set_k(self.custom_window[0:self.vec_length])

    def get_collect(self):
        return self.collect

    def set_collect(self, collect):
        self.collect = collect
        self._collect_callback(self.collect)
        self.radio_astro_systemp_calibration_0.set_collect(self.collect)

    def get_clip_toggle(self):
        return self.clip_toggle

    def set_clip_toggle(self, clip_toggle):
        self.clip_toggle = clip_toggle
        self._clip_toggle_callback(self.clip_toggle)
        self.radio_astro_systemp_calibration_0.set_clip_toggle(self.clip_toggle)

    def get_az(self):
        return self.az

    def set_az(self, az):
        self.az = az
        Qt.QMetaObject.invokeMethod(self._az_line_edit, "setText", Qt.Q_ARG("QString", str(self.az)))
        self.radio_astro_csv_filesink_0.set_az(self.az)
        self.radio_astro_systemp_calibration_0.set_az(self.az)

    def get_N_long_integration(self):
        return self.N_long_integration

    def set_N_long_integration(self, N_long_integration):
        self.N_long_integration = N_long_integration




def main(top_block_cls=DSPIRA_Spectrometer, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()

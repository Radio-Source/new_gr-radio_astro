#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Top Block
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import radio_astro
import osmosdr
import time
import sip



class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")

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
        self.samp_rate = samp_rate = 20e6
        self.min_integration = min_integration = 16
        self.integration_time2 = integration_time2 = 10
        self.integration_time1 = integration_time1 = .4
        self.short_long_time_scale = short_long_time_scale = int((integration_time2*samp_rate/vec_length/min_integration)/(integration_time1*samp_rate/vec_length/min_integration))
        self.save_toggle_csv = save_toggle_csv = '0'
        self.reset_integration_button = reset_integration_button = 0
        self.prefix_phase = prefix_phase = "/home/john/dspira_2021/interferometer_data/test_files/phase/"
        self.prefix_mag = prefix_mag = "/home/john/dspira_2021/interferometer_data/test_files/magnitude/"
        self.prefix_hornB = prefix_hornB = "/home/john/dspira_2021/interferometer_data/test_files/hornB/"
        self.prefix_hornA = prefix_hornA = "/home/john/dspira_2021/interferometer_data/test_files/hornA/"
        self.integration_select = integration_select = 0
        self.center_freq = center_freq = 1419e6
        self.N_long_integration = N_long_integration = int(short_long_time_scale*(integration_time1*samp_rate/vec_length/min_integration))

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_tab_widget_0 = Qt.QTabWidget()
        self.qtgui_tab_widget_0_widget_0 = Qt.QWidget()
        self.qtgui_tab_widget_0_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_0_widget_0)
        self.qtgui_tab_widget_0_grid_layout_0 = Qt.QGridLayout()
        self.qtgui_tab_widget_0_layout_0.addLayout(self.qtgui_tab_widget_0_grid_layout_0)
        self.qtgui_tab_widget_0.addTab(self.qtgui_tab_widget_0_widget_0, 'Interference Spectrometer')
        self.qtgui_tab_widget_0_widget_1 = Qt.QWidget()
        self.qtgui_tab_widget_0_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_0_widget_1)
        self.qtgui_tab_widget_0_grid_layout_1 = Qt.QGridLayout()
        self.qtgui_tab_widget_0_layout_1.addLayout(self.qtgui_tab_widget_0_grid_layout_1)
        self.qtgui_tab_widget_0.addTab(self.qtgui_tab_widget_0_widget_1, 'Individual Spectra')
        self.top_layout.addWidget(self.qtgui_tab_widget_0)
        # Create the options list
        self._save_toggle_csv_options = ['0', '1']
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
        self.qtgui_tab_widget_0_layout_0.addWidget(self._save_toggle_csv_group_box)
        _reset_integration_button_push_button = Qt.QPushButton('Integration Reset')
        _reset_integration_button_push_button = Qt.QPushButton('Integration Reset')
        self._reset_integration_button_choices = {'Pressed': 1, 'Released': 0}
        _reset_integration_button_push_button.pressed.connect(lambda: self.set_reset_integration_button(self._reset_integration_button_choices['Pressed']))
        _reset_integration_button_push_button.released.connect(lambda: self.set_reset_integration_button(self._reset_integration_button_choices['Released']))
        self.qtgui_tab_widget_0_layout_0.addWidget(_reset_integration_button_push_button)
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
        self.qtgui_tab_widget_0_layout_0.addWidget(self._integration_select_group_box)
        self.radio_astro_vector_moving_average_0_0_0 = radio_astro.vector_moving_average(complex,vec_length, short_long_time_scale, reset_integration_button)
        self.radio_astro_vector_moving_average_0_0 = radio_astro.vector_moving_average(complex,vec_length, short_long_time_scale, reset_integration_button)
        self.radio_astro_vector_moving_average_0 = radio_astro.vector_moving_average(complex,vec_length, short_long_time_scale, reset_integration_button)
        self.radio_astro_csv_filesink_0_1_0 = radio_astro.csv_filesink( vec_length, samp_rate, center_freq, prefix_hornB, save_toggle_csv, integration_select, short_long_time_scale, "", "", "")
        self.radio_astro_csv_filesink_0_1 = radio_astro.csv_filesink( vec_length, samp_rate, center_freq, prefix_hornA, save_toggle_csv, integration_select, short_long_time_scale, "", "", "")
        self.radio_astro_csv_filesink_0_0 = radio_astro.csv_filesink( vec_length, samp_rate, center_freq, prefix_phase, save_toggle_csv, integration_select, short_long_time_scale, "", "", "")
        self.radio_astro_csv_filesink_0 = radio_astro.csv_filesink( vec_length, samp_rate, center_freq, prefix_mag, save_toggle_csv, integration_select, short_long_time_scale, "", "", "")
        self.qtgui_vector_sink_f_0_1_0 = qtgui.vector_sink_f(
            vec_length,
            ((center_freq - samp_rate/2)/1e6),
            ((samp_rate/vec_length)/1e6),
            "Frequency",
            "Signal",
            "Horn B",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_1_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_1_0.set_y_axis(0, 10000)
        self.qtgui_vector_sink_f_0_1_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0_1_0.enable_grid(True)
        self.qtgui_vector_sink_f_0_1_0.set_x_axis_units("MHz")
        self.qtgui_vector_sink_f_0_1_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_1_0.set_ref_level(0)


        labels = ["Magnitude", "Phase", '', '', '',
            '', '', '', '', '']
        widths = [2, 2, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_1_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_1_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_1_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_1_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_1_0.qwidget(), Qt.QWidget)
        self.qtgui_tab_widget_0_layout_1.addWidget(self._qtgui_vector_sink_f_0_1_0_win)
        self.qtgui_vector_sink_f_0_1 = qtgui.vector_sink_f(
            vec_length,
            ((center_freq - samp_rate/2)/1e6),
            ((samp_rate/vec_length)/1e6),
            "Frequency",
            "Signal",
            "Horn A",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_1.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_1.set_y_axis(0, 2000)
        self.qtgui_vector_sink_f_0_1.enable_autoscale(True)
        self.qtgui_vector_sink_f_0_1.enable_grid(True)
        self.qtgui_vector_sink_f_0_1.set_x_axis_units("MHz")
        self.qtgui_vector_sink_f_0_1.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_1.set_ref_level(0)


        labels = ["Magnitude", "Phase", '', '', '',
            '', '', '', '', '']
        widths = [2, 2, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_1.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_1.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_1.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_1_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_1.qwidget(), Qt.QWidget)
        self.qtgui_tab_widget_0_layout_1.addWidget(self._qtgui_vector_sink_f_0_1_win)
        self.qtgui_vector_sink_f_0_0 = qtgui.vector_sink_f(
            vec_length,
            ((center_freq - samp_rate/2)/1e6),
            ((samp_rate/vec_length)/1e6),
            "Frequency",
            "Phase",
            "Correlation Phase",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0.set_y_axis((-1), 4)
        self.qtgui_vector_sink_f_0_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0_0.enable_grid(False)
        self.qtgui_vector_sink_f_0_0.set_x_axis_units("MHz")
        self.qtgui_vector_sink_f_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_ref_level(0)


        labels = ["Phase", "Phase", '', '', '',
            '', '', '', '', '']
        widths = [2, 2, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["red", "red", "green", "black", "cyan",
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
        self.qtgui_tab_widget_0_layout_0.addWidget(self._qtgui_vector_sink_f_0_0_win)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            vec_length,
            ((center_freq - samp_rate/2)/1e6),
            ((samp_rate/vec_length)/1e6),
            "Frequency",
            "Magnitude",
            "Correlation Magnitude",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis(0, 250)
        self.qtgui_vector_sink_f_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0.enable_grid(False)
        self.qtgui_vector_sink_f_0.set_x_axis_units("MHz")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)


        labels = ["Magnitude", "Phase", '', '', '',
            '', '', '', '', '']
        widths = [2, 2, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.qtgui_tab_widget_0_layout_0.addWidget(self._qtgui_vector_sink_f_0_win)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(2) + " " + ""
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(center_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.osmosdr_source_0.set_center_freq(center_freq, 1)
        self.osmosdr_source_0.set_freq_corr(0, 1)
        self.osmosdr_source_0.set_dc_offset_mode(0, 1)
        self.osmosdr_source_0.set_iq_balance_mode(0, 1)
        self.osmosdr_source_0.set_gain_mode(False, 1)
        self.osmosdr_source_0.set_gain(10, 1)
        self.osmosdr_source_0.set_if_gain(20, 1)
        self.osmosdr_source_0.set_bb_gain(20, 1)
        self.osmosdr_source_0.set_antenna('', 1)
        self.osmosdr_source_0.set_bandwidth(0, 1)
        self.fft_vxx_0_0 = fft.fft_vcc(vec_length, True, window.blackmanharris(vec_length), True, 1)
        self.fft_vxx_0 = fft.fft_vcc(vec_length, True, window.blackmanharris(vec_length), True, 1)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_multiply_conjugate_cc_0_0_0 = blocks.multiply_conjugate_cc(vec_length)
        self.blocks_multiply_conjugate_cc_0_0 = blocks.multiply_conjugate_cc(vec_length)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(vec_length)
        self.blocks_integrate_xx_0_0_0_1_0_0 = blocks.integrate_cc((int(integration_time1*samp_rate/vec_length/min_integration)), vec_length)
        self.blocks_integrate_xx_0_0_0_1_0 = blocks.integrate_cc((int(integration_time1*samp_rate/vec_length/min_integration)), vec_length)
        self.blocks_integrate_xx_0_0_0_1 = blocks.integrate_cc((int(integration_time1*samp_rate/vec_length/min_integration)), vec_length)
        self.blocks_integrate_xx_0_0_0_0_0 = blocks.integrate_cc(min_integration, vec_length)
        self.blocks_integrate_xx_0_0_0_0 = blocks.integrate_cc(min_integration, vec_length)
        self.blocks_integrate_xx_0_0_0 = blocks.integrate_cc(min_integration, vec_length)
        self.blocks_complex_to_real_1_0 = blocks.complex_to_real(vec_length)
        self.blocks_complex_to_real_1 = blocks.complex_to_real(vec_length)
        self.blocks_complex_to_magphase_0 = blocks.complex_to_magphase(vec_length)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_magphase_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.blocks_complex_to_magphase_0, 1), (self.qtgui_vector_sink_f_0_0, 0))
        self.connect((self.blocks_complex_to_magphase_0, 0), (self.radio_astro_csv_filesink_0, 0))
        self.connect((self.blocks_complex_to_magphase_0, 1), (self.radio_astro_csv_filesink_0_0, 0))
        self.connect((self.blocks_complex_to_real_1, 0), (self.qtgui_vector_sink_f_0_1, 0))
        self.connect((self.blocks_complex_to_real_1, 0), (self.radio_astro_csv_filesink_0_1, 0))
        self.connect((self.blocks_complex_to_real_1_0, 0), (self.qtgui_vector_sink_f_0_1_0, 0))
        self.connect((self.blocks_complex_to_real_1_0, 0), (self.radio_astro_csv_filesink_0_1_0, 0))
        self.connect((self.blocks_integrate_xx_0_0_0, 0), (self.blocks_integrate_xx_0_0_0_1, 0))
        self.connect((self.blocks_integrate_xx_0_0_0_0, 0), (self.blocks_integrate_xx_0_0_0_1_0, 0))
        self.connect((self.blocks_integrate_xx_0_0_0_0_0, 0), (self.blocks_integrate_xx_0_0_0_1_0_0, 0))
        self.connect((self.blocks_integrate_xx_0_0_0_1, 0), (self.radio_astro_vector_moving_average_0, 0))
        self.connect((self.blocks_integrate_xx_0_0_0_1_0, 0), (self.radio_astro_vector_moving_average_0_0, 0))
        self.connect((self.blocks_integrate_xx_0_0_0_1_0_0, 0), (self.radio_astro_vector_moving_average_0_0_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_integrate_xx_0_0_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0_0, 0), (self.blocks_integrate_xx_0_0_0_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0_0_0, 0), (self.blocks_integrate_xx_0_0_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_conjugate_cc_0_0, 1))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_conjugate_cc_0_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_multiply_conjugate_cc_0_0_0, 1))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_multiply_conjugate_cc_0_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.osmosdr_source_0, 1), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.radio_astro_vector_moving_average_0, 0), (self.blocks_complex_to_magphase_0, 0))
        self.connect((self.radio_astro_vector_moving_average_0_0, 0), (self.blocks_complex_to_real_1, 0))
        self.connect((self.radio_astro_vector_moving_average_0_0_0, 0), (self.blocks_complex_to_real_1_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_vec_length(self):
        return self.vec_length

    def set_vec_length(self, vec_length):
        self.vec_length = vec_length
        self.set_N_long_integration(int(self.short_long_time_scale*(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))
        self.set_short_long_time_scale(int((self.integration_time2*self.samp_rate/self.vec_length/self.min_integration)/(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))
        self.qtgui_vector_sink_f_0.set_x_axis(((self.center_freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))
        self.qtgui_vector_sink_f_0_0.set_x_axis(((self.center_freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))
        self.qtgui_vector_sink_f_0_1.set_x_axis(((self.center_freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))
        self.qtgui_vector_sink_f_0_1_0.set_x_axis(((self.center_freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_N_long_integration(int(self.short_long_time_scale*(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))
        self.set_short_long_time_scale(int((self.integration_time2*self.samp_rate/self.vec_length/self.min_integration)/(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_vector_sink_f_0.set_x_axis(((self.center_freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))
        self.qtgui_vector_sink_f_0_0.set_x_axis(((self.center_freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))
        self.qtgui_vector_sink_f_0_1.set_x_axis(((self.center_freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))
        self.qtgui_vector_sink_f_0_1_0.set_x_axis(((self.center_freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))

    def get_min_integration(self):
        return self.min_integration

    def set_min_integration(self, min_integration):
        self.min_integration = min_integration
        self.set_N_long_integration(int(self.short_long_time_scale*(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))
        self.set_short_long_time_scale(int((self.integration_time2*self.samp_rate/self.vec_length/self.min_integration)/(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))

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

    def get_short_long_time_scale(self):
        return self.short_long_time_scale

    def set_short_long_time_scale(self, short_long_time_scale):
        self.short_long_time_scale = short_long_time_scale
        self.set_N_long_integration(int(self.short_long_time_scale*(self.integration_time1*self.samp_rate/self.vec_length/self.min_integration)))

    def get_save_toggle_csv(self):
        return self.save_toggle_csv

    def set_save_toggle_csv(self, save_toggle_csv):
        self.save_toggle_csv = save_toggle_csv
        self._save_toggle_csv_callback(self.save_toggle_csv)
        self.radio_astro_csv_filesink_0.set_save_toggle(self.save_toggle_csv)
        self.radio_astro_csv_filesink_0_0.set_save_toggle(self.save_toggle_csv)
        self.radio_astro_csv_filesink_0_1.set_save_toggle(self.save_toggle_csv)
        self.radio_astro_csv_filesink_0_1_0.set_save_toggle(self.save_toggle_csv)

    def get_reset_integration_button(self):
        return self.reset_integration_button

    def set_reset_integration_button(self, reset_integration_button):
        self.reset_integration_button = reset_integration_button
        self.radio_astro_vector_moving_average_0.set_reset_integration(self.reset_integration_button)
        self.radio_astro_vector_moving_average_0_0.set_reset_integration(self.reset_integration_button)
        self.radio_astro_vector_moving_average_0_0_0.set_reset_integration(self.reset_integration_button)

    def get_prefix_phase(self):
        return self.prefix_phase

    def set_prefix_phase(self, prefix_phase):
        self.prefix_phase = prefix_phase

    def get_prefix_mag(self):
        return self.prefix_mag

    def set_prefix_mag(self, prefix_mag):
        self.prefix_mag = prefix_mag

    def get_prefix_hornB(self):
        return self.prefix_hornB

    def set_prefix_hornB(self, prefix_hornB):
        self.prefix_hornB = prefix_hornB

    def get_prefix_hornA(self):
        return self.prefix_hornA

    def set_prefix_hornA(self, prefix_hornA):
        self.prefix_hornA = prefix_hornA

    def get_integration_select(self):
        return self.integration_select

    def set_integration_select(self, integration_select):
        self.integration_select = integration_select
        self._integration_select_callback(self.integration_select)
        self.radio_astro_csv_filesink_0.set_integration_select(self.integration_select)
        self.radio_astro_csv_filesink_0_0.set_integration_select(self.integration_select)
        self.radio_astro_csv_filesink_0_1.set_integration_select(self.integration_select)
        self.radio_astro_csv_filesink_0_1_0.set_integration_select(self.integration_select)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.osmosdr_source_0.set_center_freq(self.center_freq, 0)
        self.osmosdr_source_0.set_center_freq(self.center_freq, 1)
        self.qtgui_vector_sink_f_0.set_x_axis(((self.center_freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))
        self.qtgui_vector_sink_f_0_0.set_x_axis(((self.center_freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))
        self.qtgui_vector_sink_f_0_1.set_x_axis(((self.center_freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))
        self.qtgui_vector_sink_f_0_1_0.set_x_axis(((self.center_freq - self.samp_rate/2)/1e6), ((self.samp_rate/self.vec_length)/1e6))

    def get_N_long_integration(self):
        return self.N_long_integration

    def set_N_long_integration(self, N_long_integration):
        self.N_long_integration = N_long_integration




def main(top_block_cls=top_block, options=None):

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

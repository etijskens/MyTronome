# -*- coding: utf-8 -*-

"""
Package mytronome
=================

Top-level package for mytronome.
"""

# import mytronome.cli_beat
__version__ = "0.0.0"

from PyQt5 import QtWidgets, QtCore, QtMultimedia
import pickle, os

from time import time

class MyTronome(QtWidgets.QWidget):

    def __init__(self, start=False):
        super(MyTronome, self).__init__()
        self.initUI()

        if os.path.exists('MyTronome.data'):
            print("Reading 'MyTronome.data'")
            with open('MyTronome.data', 'rb') as pickled:
                data = pickle.load(pickled)
                #                 print(data)
                self.beats_per_minute_spinbox.setValue(data['beats_per_minute'])
                self.beats_per_measure_spinbox.setValue(data['beats_per_measure'])
                self.ticks_per_beat_spinbox.setValue(data['ticks_per_beat'])
                self.swing.setChecked(data['swing'])

        if start:
            self.start_stop()

    def initUI(self):
        #         self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('MyTronome')

        qvlayout = QtWidgets.QVBoxLayout()

        beats_per_minute_label = QtWidgets.QLabel("beats per minute:")
        self.beats_per_minute_spinbox = QtWidgets.QSpinBox(self)
        self.beats_per_minute_spinbox.setMinimum(10)
        self.beats_per_minute_spinbox.setMaximum(250)
        self.beats_per_minute_spinbox.setSingleStep(5)
        self.beats_per_minute_spinbox.setValue(60)
        self.beats_per_minute_spinbox.valueChanged.connect(self.beats_per_minute_spinbox_valueChanged)
        qhlayout = QtWidgets.QHBoxLayout()
        qhlayout.addWidget(beats_per_minute_label)
        qhlayout.addWidget(self.beats_per_minute_spinbox)
        qvlayout.addLayout(qhlayout)

        beats_per_measure_label = QtWidgets.QLabel("beats per measure:")
        self.beats_per_measure_spinbox = QtWidgets.QSpinBox(self)
        self.beats_per_measure_spinbox.setMinimum(1)
        self.beats_per_measure_spinbox.setMaximum(12)
        self.beats_per_measure_spinbox.setValue(4)
        self.beats_per_measure_spinbox.valueChanged.connect(self.beats_per_minute_spinbox_valueChanged)
        qhlayout = QtWidgets.QHBoxLayout()
        qhlayout.addWidget(beats_per_measure_label)
        qhlayout.addWidget(self.beats_per_measure_spinbox)
        qvlayout.addLayout(qhlayout)

        ticks_per_beat_label = QtWidgets.QLabel("ticks per beat:")
        self.ticks_per_beat_spinbox = QtWidgets.QSpinBox(self)
        self.ticks_per_beat_spinbox.setMinimum(0)
        self.ticks_per_beat_spinbox.setMaximum(6)
        self.ticks_per_beat_spinbox.setValue(0)
        self.ticks_per_beat_old_value = self.ticks_per_beat_spinbox.value()
        self.ticks_per_beat_spinbox.valueChanged.connect(self.ticks_per_beat_valueChanged)
        qhlayout = QtWidgets.QHBoxLayout()
        qhlayout.addWidget(ticks_per_beat_label)
        qhlayout.addWidget(self.ticks_per_beat_spinbox)
        qvlayout.addLayout(qhlayout)

        self.start_stop_button = QtWidgets.QPushButton('start', self)
        qhlayout = QtWidgets.QHBoxLayout()
        qhlayout.addWidget(self.start_stop_button)
        qvlayout.addLayout(qhlayout)

        self.linear = QtWidgets.QRadioButton('Linear', self)
        self.swing = QtWidgets.QRadioButton('Swing', self)
        #         self.soft_swing = QtWidgets.QRadioButton('Soft swing',self)
        #         self.hard_swing = QtWidgets.QRadioButton('Hard swing',self)
        style = QtWidgets.QButtonGroup(self)
        style.addButton(self.linear)
        #         style.addButton(self.soft_swing)
        style.addButton(self.swing)
        #         style.addButton(self.hard_swing)
        style.buttonClicked.connect(self.style_changed)
        self.linear.setChecked(True)
        self.beep = self.beep_linear
        qhlayout = QtWidgets.QHBoxLayout()
        qhlayout.addWidget(self.linear)
        #         qhlayout.addWidget(self.soft_swing)
        qhlayout.addWidget(self.swing)
        #         qhlayout.addWidget(self.hard_swing)
        qvlayout.addLayout(qhlayout)

        self.setLayout(qvlayout)
        self.show()

        self.start_stop_button.clicked.connect(self.start_stop)
        self.started = False

        self.sound_accent = QtMultimedia.QSound("mytronome/accent.wav")
        self.sound_beat   = QtMultimedia.QSound("mytronome/beat.wav")
        self.sound_click  = QtMultimedia.QSound("mytronome/click2.wav")

    def style_changed(self, button):
        if hasattr(self, 'tmr'):
            self.start_stop()
            restart = True
        else:
            restart = False

        #         print(button)
        if button == self.linear:
            self.beep = self.beep_linear
            self.ticks_per_beat_spinbox.setValue(0)
            self.ticks_per_beat_spinbox.setEnabled(True)
        elif button == self.swing:
            self.beep = self.beep_swing
            self.ticks_per_beat_spinbox.setValue(3)
            self.ticks_per_beat_spinbox.setEnabled(False)
        #         elif button==self.soft_swing:
        #             raise NotImplemented
        #         elif button==self.hard_swing:
        #             raise NotImplemented
        if restart:
            self.start_stop()

    def start_stop(self):
        if self.started:
            # stop
            self.tmr.stop()
            del self.tmr
            self.started = False
            self.start_stop_button.setText('Start')
        else:
            # start
            self.counter = 0
            #             self.bpmeasure=

            if self.linear.isChecked() and self.ticks_per_beat_spinbox.value() == 0:
                ms = 60000 / self.beats_per_minute_spinbox.value()
                print(f'linear: {ms=}')
            else:
                ms = 60000 / (self.beats_per_minute_spinbox.value() * self.ticks_per_beat_spinbox.value())
                print(f'swing: {ms=}')

            self.tmr = QtCore.QTimer(self)
            self.tmr.setInterval(ms)
            self.tmr.timeout.connect(self.beep)

            self.started = True
            self.start_stop_button.setText('Stop')
            # self.t0 = time()
            self.minute_counter = 0
            self.minute = time()

            self.tmr.start()

    def keyPressEvent(self, e):
        #         print(e)
        #         print(e.key())
        #         print(QtCore.Qt.Key_Return)
        if e.key() == QtCore.Qt.Key_Return:
            self.start_stop()
        elif e.key() == QtCore.Qt.Key_Up:
            pass

    def beep_linear(self):
        if self.counter == 0:
            self.sound_accent.play()
        else:
            self.sound_beat.play()
        self.counter += 1
        self.counter = self.counter % self.beats_per_measure_spinbox.value()
        t1 = time()
        # print(t1-self.t0)
        # self.t0 = t1
        self.minute_counter +=1
        self.minute_counter %= self.beats_per_minute_spinbox.value()
        if self.minute_counter == 0:
            m = (t1 - self.minute)/60
            oops = 'oop' if abs(1-m) > 0.005 else ''
            print(m,oops)
            self.minute = t1

    #         print(self.counter)

    def beep_linear_with_ticks(self):
        i = self.counter % self.ticks_per_beat_spinbox.value()
        if self.counter == 0:
            self.sound_accent.play()
        elif not i == 0:
            self.sound_click.play()
        else:
            self.sound_beat.play()
        self.counter += 1
        self.counter = self.counter % (self.beats_per_measure_spinbox.value() * self.ticks_per_beat_spinbox.value())

            # print(self.counter)

    def beep_swing(self):
        i = self.counter % self.ticks_per_beat_spinbox.value()
        if self.counter == 0:
            self.sound_accent.play()
            # print('sound_accent')
        elif i == 1:
            pass
        elif i == 2:
            self.sound_click.play()
            # print('sound_click')
        #         elif self.counter%3==3:
        else:
            self.sound_beat.play()
            # print('sound_beat')
        self.counter += 1
        self.counter = self.counter % (self.beats_per_measure_spinbox.value() * 3)

    #         print(self.counter)

    def beats_per_minute_spinbox_valueChanged(self, new_value):
        if hasattr(self, 'tmr') and self.started:
            # restart with the new settings
            self.start_stop()
            self.start_stop()

    def beats_per_measure_spinbox_valueChanged(self, new_value):
        if hasattr(self, 'tmr') and self.started:
            # restart with the new settings
            self.start_stop()
            self.start_stop()

    def ticks_per_beat_valueChanged(self, new_value):
        if hasattr(self, 'tmr'):
            self.start_stop()
            restart = True
        else:
            restart = False

        if self.swing.isChecked():
            self.ticks_per_beat_spinbox.setValue(3)
        elif self.linear.isChecked():
            if new_value == 1:
                if self.ticks_per_beat_old_value < new_value:
                    self.ticks_per_beat_spinbox.setValue(2)
                else:
                    self.ticks_per_beat_spinbox.setValue(0)
            else:
                if new_value == 0:
                    self.beep = self.beep_linear
                else:
                    self.beep = self.beep_linear_with_ticks
        self.ticks_per_beat_old_value = self.ticks_per_beat_spinbox.value()
        #         print(new_value)
        if restart:
            self.start_stop()

    def closeEvent(self, a0):
        print("Writing 'MyTronome.data'")
        data = {'beats_per_minute': self.beats_per_minute_spinbox.value()
            , 'beats_per_measure': self.beats_per_measure_spinbox.value()
            , 'ticks_per_beat': self.ticks_per_beat_spinbox.value()
            , 'swing': self.swing.isChecked()
        }
        pickled = open('MyTronome.data', 'wb')
        pickle.dump(data, pickled)

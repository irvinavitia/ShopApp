# Created on Fri Feb 18 06:58:09 2022

# @author: iavitia

#importations needed to set up PyQt
import sys
import os
from time import strftime, gmtime
import threading
from time import sleep


from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtQuick import QQuickWindow
from PyQt6.QtCore import QObject, pyqtSignal #imported Signal


class Backend(QObject): # part of signal
    def __init__(self):
        QObject.__init__(self)
        
    updated = pyqtSignal(str, arguments=['updater'])
        
    def updater(self, curr_time):
        self.updated.emit(curr_time)
        
    def bootUp(self):
        t_thread = threading.Thread(target=self._bootUp)
        t_thread.daemon = True
        t_thread.start()
        
    def _bootUp(self):
        while True:
            curr_time = strftime("%H:%M:%S", gmtime())
            self.updater(curr_time)
            sleep(0.1)

QQuickWindow.setSceneGraphBackend('software')

app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('./UI/main.qml')

back_end = Backend()

engine.rootObjects()[0].setProperty('backend', back_end)

back_end.bootUp()


"""
The QQuickWindow.setSceneGraphBackend('software') is included in the 
code as a fallback option for uses with old hardware specs, other than that 
they would see an error information as seen below:
    
>>> Failed to create vertex shader: Error 0x80070057: The parameter is 
incorrect.
>>> Failed to build graphics pipeline state
"""

sys.exit(app.exec())





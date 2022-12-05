# -*- coding: utf-8 -*-

import os, sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ConwaysCanvas import *

class ConwaysApp(QMainWindow):
    """ Conway App """
    def __init__(self, gridwidth=10, gridheight=10, parent=None):
        super(ConwaysApp, self).__init__()
        self.title        = "Conway's Game of Life"
        self.gridwidth    = gridwidth
        self.gridheight   = gridheight
        self.cellsize     = 25
        self.margin_left  = 200
        self.margin_top   = 200

        # Window width is equal to number of cells * width of each cell
        self.width        = self.gridwidth*self.cellsize
        # Window width is equal to number of cells * width of each cell
        # -4 just makes the cell height a little shorter than the width so that all cells fit in the grid
        self.height       = self.gridheight*self.cellsize - 4

        self.timer_period = 125
        self.timer_state  = False

        self._initUI()
        self._initMenus()
        self.timer  = QTimer()
        self.timer.timeout.connect(self.conway_canvas.updateGridEvent)

    def _initUI(self):
        self.setWindowTitle(self.title + " - [PAUSED]")
        self.setWindowIcon(QIcon('lib/ico.png'))
        self.setGeometry(self.margin_left, self.margin_top, self.width + 16, self.height + 20)
        self.setFixedSize(self.size())
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.conway_canvas = ConwaysCanvas(self.cellsize, self.gridwidth, self.gridheight)

        # Create parent widget
        self.widget = QWidget(self)
        # Create vertical layout
        self.vbox = QVBoxLayout(self.widget)
        self.vbox.addWidget(self.conway_canvas) 
        # Set vertical layout as layout 
        self.widget.setLayout(self.vbox) 

        # Create Horizontal layout to hold buttons
        self.hbox = QHBoxLayout(self.widget)

        # Create clear button
        self.clear_button = QPushButton(self, text = "Clear")
        self.clear_button.clicked.connect(self.onClearButton)
        self.hbox.addWidget(self.clear_button)

        # Create Start button
        self.start_button = QPushButton(self, text = "Start")
        self.start_button.clicked.connect(self.onStartButton)
        self.hbox.addWidget(self.start_button)

        # Create Reset button
        self.reset_button = QPushButton(self, text = "Reset")
        self.reset_button.clicked.connect(self.onResetButton)
        self.hbox.addWidget(self.reset_button)

        # Create Quit button
        self.quit_button = QPushButton(self, text = "Quit")
        self.quit_button.clicked.connect(self.onQuitButton)
        self.hbox.addWidget(self.quit_button)

        self.vbox.addLayout(self.hbox)

        self.setCentralWidget(self.widget)
    
        self.show()

    # Add menu options to menu bar
    def _initMenus(self):
        mainMenu      = self.menuBar()
        appMenu       = mainMenu.addMenu('Conway')

        #Menu buttons
        exitButton = QAction('Exit', self)
        exitButton.setShortcut('Ctrl + Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close) # Run self.close() if trigerred
        appMenu.addAction(exitButton)

    # Function called when Keyboard keys are pressed
    def keyPressEvent(self, event):
        # If <Space> Start or stop
        if   event.key() == Qt.Key_Space:
            # If Game is running, pause it
            if self.timer_state == True :
                self.timer_state = False
                self.timer.stop()
                self.setWindowTitle(self.title +" - [PAUSED]")
            # If Game is paused, run it
            else :
                self.timer_state = True
                self.timer.start(self.timer_period)
                self.setWindowTitle(self.title)

        # If <Escape> is pressed close window
        elif event.key() == Qt.Key_Escape:
            self.close()

        # If <R> is generate random grid
        elif event.key() == Qt.Key_R:
            self.conway_canvas.regen()

        # If <C> is pressed clear grid
        elif event.key() == Qt.Key_C:
            self.conway_canvas.cleargrid()

    # Function called when clear button is pressed
    def onClearButton(self):
        self.conway_canvas.cleargrid()

    # Function called when start button is pressed
    def onStartButton(self):
        # If Game is running, pause it
        if self.timer_state == True :
            self.timer_state = False
            self.timer.stop()
            self.setWindowTitle(self.title +" - [PAUSED]")
            self.start_button.setText("Start")
        # If Game is paused, start it
        else :
            self.timer_state = True
            self.timer.start(self.timer_period)
            self.setWindowTitle(self.title)
            self.start_button.setText("Pause")

    # Function Called when reset button is pressed
    def onResetButton(self):
        self.conway_canvas.regen()

     # Function Called when reset button is pressed
    def onQuitButton(self):
        self.close()


if __name__ == """__main__""":
    app = QApplication(sys.argv)
    ex = ConwaysApp(38,20) #76,40
    sys.exit(app.exec_())

#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Mandelbrot Background
author: Craig Warner
    This program generates a desktop background composed of several
Mandlebrot images.  The images are a sequence of images start with a
standard Mandelbortt images, then setep by step magnify the and focus
in on one location in the Mandelbrt space.     
"""

# External Imports
import os
import platform
import sys
import argparse
import hjson
import json
from jsonformatter import JsonFormatter
from time import sleep

# GUI  Imports
from PyQt5 import (QtWidgets, QtCore)
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider,
    QHBoxLayout, QVBoxLayout, QToolBar, QAction, QStatusBar,
    QDialog, QDialogButtonBox, QFileDialog, QWidget, QProgressBar
)
from PyQt5.QtCore import ( 
    Qt, QRect
)
from PyQt5.QtGui import ( 
    QPainter, QColor, QFont
)

# MBG Imports  
from mbg.version import __version__
import mbg.mimage as mimage
import mbg.bmp as bmp 

class PositionerWidget(QWidget):
    def __init__(self,parent):
        super(PositionerWidget, self).__init__(parent)
        self.init_settings()

        self.image = mimage.MandelImage(
            self.min_real_x,
            self.min_real_y,
            self.max_real_x,
            self.max_real_y,
            200, # x dots
            200, # y dots
            4, # bits per color
            False) # high precision
        self.setGeometry(QRect(0, 0, 200, 200))
        self.parent = parent

        self.zoomValue = 0.5 

        print("Positioner Widget")

    def getPoints(self):
        return(self.pointsDefined)

    def getZoomPath(self,inum):
        return (
            (self.zoomPath["min_x"][inum],
            self.zoomPath["min_x"][inum],
            self.zoomPath["min_x"][inum],
            self.zoomPath["min_x"][inum]))

    def setZoom(self, zoomValue):
        self.zoomValue = zoomValue

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        for x in range(0,40):
            for y in range(0,40):
                x1 = x*5 + 5 
                y1 = y*5 + 5
                self.drawRect(qp,x1,y1,5,5, self.image.CalcColorDot(x*5,y*5))

    def drawRect(self,painter,x,y,width,height,colornum):
        color = QColor(colornum)
        painter.fillRect(x , y , width, height, color)

    def mousePressEvent(self,event):
        if not self.pathAllDefined:
            #self.point_set_x = event.pos().x() - 100
            #self.point_set_y = event.pos().y() - 100
            self.point_set_x = event.pos().x()
            self.point_set_y = event.pos().y()
            if(args.verbose):
                print("x: %d y: %d " % (event.pos().x(),event.pos().y()))
                print("minx: %f miny: %f " % (self.min_real_x,self.min_real_y))
                print("maxx: %f maxy: %f " % (self.max_real_x,self.max_real_y))
            center_x = (self.min_real_x + float(self.point_set_x)/200.0 * self.real_length)
            center_y  = (self.max_real_y - float(self.point_set_y)/200.0 * self.real_length)
            if(args.verbose):
                print("crx: %f cry: %f " % (center_x,center_y))
            self.min_real_x = center_x - self.real_length/float(2)
            self.max_real_x = center_x + self.real_length/float(2)
            self.min_real_y = center_y - self.real_length/float(2)
            self.max_real_y = center_y + self.real_length/float(2)
            self.real_length = self.real_length * self.zoomValue 
            self.image.RePosition(
                    self.min_real_x,
                    self.min_real_y,
                    self.max_real_x,
                    self.max_real_y
                    )
            self.repaint()
            self.appendPoint(self.min_real_x,self.max_real_x,self.min_real_y,self.max_real_y)
            self.parent.updateAfterZoomSelect()
        
    def appendPoint(self,min_x,max_x,min_y,max_y):
        self.zoomPath["min_x"].append(min_x)
        self.zoomPath["max_x"].append(max_x)
        self.zoomPath["min_y"].append(min_y)
        self.zoomPath["max_y"].append(max_y)
        self.pointsDefined = self.pointsDefined + 1 
        if(self.pointsDefined == template["num_images"]):
            self.pathAllDefined = True 
        else:
            self.pathAllDefined = False 

    def init_settings(self):
        self.pointsDefined = 0 
        self.zoomPath = {} 
        self.zoomPath["min_x"] = []
        self.zoomPath["max_x"] = []
        self.zoomPath["min_y"] = []
        self.zoomPath["max_y"] = []
        self.appendPoint(-1.0,2.0,-1.5,1.5)

        self.pathAllDefined = False
        self.pointsDefined = 0 

        self.min_real_x = float('-1.0')
        self.max_real_x = float('2.0')
        self.min_real_y = float('-1.5')
        self.max_real_y = float('1.5')
        self.real_length = float('3.0')

    def reset(self):
        self.init_settings()
        self.image.RePosition(
                    self.min_real_x,
                    self.min_real_y,
                    self.max_real_x,
                    self.max_real_y
                    )
        self.repaint()

    def writeZoomPathFile(self):
        if args.verbose:
            print("Wrining Zoom Path to file:",args.ozfile)
        lines = []
        file_obj = open(args.ozfile,"w")
        #lines = hjson.dumpsJSON(self.zoomPath,file_obj)
        #file_obj.close()

        lines = json.dumps(self.zoomPath, indent=4, separators=(", ", " : "))
        for l in (lines):
            file_obj.write(l)

        file_obj.close()

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Mandelbrot Background")

        QBtn = QDialogButtonBox.Ok 

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()

        message_str = "Mandelbrot Background\nVersion: %s\n" % (__version__)
        message_str = message_str + "Copyright 2023 Craig Warner all rights reserved."
        message = QLabel(message_str)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class FlexDialog(QDialog):
    def __init__(self,win_text,msg_text):
        super().__init__()

        self.setWindowTitle(win_text)

        QBtn = QDialogButtonBox.Ok 

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        message = QLabel(msg_text)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        # Start the GUI 
        self.initUI()

    def initUI(self):
        self.wid = QtWidgets.QWidget(self)
        self.setCentralWidget(self.wid)
        self.setGeometry(0,100,512,384)
        self.setWindowTitle("Mandelbrot Background")
        self.createActions()
        self.addMenuToWindow()
        self.addBody()
        self.show()

    def createActions(self):
    #    self.loadTemplateAction= QAction()
    #    self.loadTemplateAction.setText("Load Template")
    #    self.loadZoomAction= QAction()
    #    self.loadZoomAction.setText("Load Zoom File")
        self.generateBackgroundAction= QAction()
        self.generateBackgroundAction.setText("Generate Background")
        self.exitAppAction= QAction()
        self.exitAppAction.setText("Quit")

        self.aboutAction= QAction()
        self.aboutAction.setText("About")

    def addMenuToWindow(self):

    #    toolbar = QToolBar("Toolbar")
    #    self.addToolBar(toolbar)

    #    toolbar.addAction(self.loadTemplateAction)
    #    self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
     #   file_menu.addAction(self.loadTemplateAction)
     #   file_menu.addAction(self.loadZoomAction)
        file_menu.addAction(self.generateBackgroundAction)
        file_menu.addSeparator()
        file_menu.addAction(self.exitAppAction)

        help_menu = menu.addMenu("&Help")
        help_menu.addAction(self.aboutAction)

     #   self.loadTemplateAction.triggered.connect(self.doLoadTemplate)
     #   self.loadZoomAction.triggered.connect(self.doLoadZoom)
        self.generateBackgroundAction.triggered.connect(self.doDrawButton)
        self.exitAppAction.triggered.connect(self.doExitApp)
        self.aboutAction.triggered.connect(self.doAbout)

    def doLoadTemplate(self):
        if(args.verbose):
            print("Load Template")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.template_file_name, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","JSON Files (*.json);; HJSON Files (*.hjson)", options=options)
        template = hjson.load(open(self.template_file_name))

    #def doLoadZoom(self):
    #    if(args.verbose):
    #        print("Load Zoom")
    #    options = QFileDialog.Options()
    #    options |= QFileDialog.DontUseNativeDialog
    #    self.zoom_file_name, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","JSON Files (*.json);; HJSON Files (*.hjson)", options=options)
    #    zoom = hjson.load(open(self.zoom_file_name))

    #def doGenerateBackground(self):
    #    if(args.verbose):
    #        print("Generating Background")
    #    genBackground()

    def doExitApp(self):
        exit(0)

    def doAbout(self):
        print("About")
        dlg = AboutDialog(self)
        dlg.exec()

    def addBody(self):
        # V1
        #   H1
        #     V2 V3
        #   V4
        #     w
        #     H2
        #     H3

        vbox1 = QtWidgets.QVBoxLayout()
        vbox2 = QtWidgets.QVBoxLayout()
        vbox3 = QtWidgets.QVBoxLayout()
        vbox4 = QtWidgets.QVBoxLayout()

        hbox1 = QtWidgets.QHBoxLayout()
        hbox2 = QtWidgets.QHBoxLayout()
        hbox3 = QtWidgets.QHBoxLayout()

        self.positionerWidget = PositionerWidget(self)
        vbox2.addWidget(self.positionerWidget)

        vbox2_widget = QWidget()
        vbox2_widget.setLayout(vbox2)
        vbox2_widget.setFixedWidth(200)

        slider_title= QtWidgets.QLabel()
        slider_title.setText("Zoom In Magnification (1x to 20x)")
        slider_title.setFont(QFont('SansSerif', 10))
        vbox3.addWidget(slider_title)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(20)
        self.slider.setValue(2)
        self.slider.valueChanged.connect(self.doSliderValueChange)
        vbox3.addWidget(self.slider)

        reset_button = QtWidgets.QPushButton('Reset Zoom Path', self)
        reset_button.setCheckable(True)
        reset_button.clicked[bool].connect(self.doResetButton)
        vbox3.addWidget(reset_button)

        self.zoom_path_cnt = QtWidgets.QLabel()
        zoom_path_cnt_text = self.genZoomCountText()
        self.zoom_path_cnt.setText(zoom_path_cnt_text)
        self.zoom_path_cnt.setFont(QFont('SansSerif', 10))
        vbox3.addWidget(self.zoom_path_cnt)

        draw_button = QtWidgets.QPushButton('Generate Background', self)
        draw_button.setCheckable(True)
        draw_button.clicked[bool].connect(self.doDrawButton)
        vbox4.addWidget(draw_button)

        bg_progress_label = QtWidgets.QLabel()
        bg_progress_label.setText("Background Generation Progress:")
        bg_progress_label.setFont(QFont('SansSerif', 10))
        hbox2.addWidget(bg_progress_label)

        self.bg_progress_bar = QProgressBar(self)
        self.updateBgProgressBar(0)
        hbox2.addWidget(self.bg_progress_bar)

        img_progress_label = QtWidgets.QLabel()
        img_progress_label.setText("Image Generation Progress:")
        img_progress_label.setFont(QFont('SansSerif', 10))
        hbox3.addWidget(img_progress_label)

        self.img_progress_bar = QProgressBar(self)
        self.updateImgProgressBar(0)
        hbox3.addWidget(self.img_progress_bar)

        hbox1.addWidget(vbox2_widget)
        hbox1.addLayout(vbox3)
        vbox1.addLayout(hbox1)
        vbox1.addLayout(vbox4)
        vbox1.addLayout(hbox2)
        vbox1.addLayout(hbox3)

        self.wid.setLayout(vbox1)

    def doSliderValueChange(self):
        value = self.slider.value()
        zoomValue =  (float(1.0)/float(value))
        self.positionerWidget.setZoom(zoomValue)

    def doResetButton(self):
        if args.verbose:
            print("Reset Button")
        self.positionerWidget.reset()
        self.updateAfterZoomSelect()

    def doDrawButton(self):
        if args.verbose:
            print("Draw Button")
        if template["num_images"] != self.positionerWidget.getPoints():
            print("Error")
            dlg = FlexDialog("Error","Not enough image locations defined.\nClick on the Mandelbrot image to define more image locations.")
            dlg.exec()
        else:
            self.genImagesInteractive()

    def updateBgProgressBar(self,value):
        self.bg_progress_bar.setValue(value)

    def updateImgProgressBar(self,value):
        self.img_progress_bar.setValue(value)

    def updateAfterZoomSelect(self):
        if args.verbose:
            print("Update After Zoom Select")
        zoom_path_cnt_text = self.genZoomCountText()
        self.zoom_path_cnt.setText(zoom_path_cnt_text)
        if args.verbose:
            print(zoom_path_cnt_text)
        self.checkWriteZoomPath()

    def checkWriteZoomPath(self):
        if(args.ozfile != ""):
            if (self.positionerWidget.getPoints() == template["num_images"]):
                self.positionerWidget.writeZoomPathFile()

    def genImagesInteractive(self):
        num_bits = template["bits_per_color"]

        for inum in range(0,template["num_images"]):
            (min_x, max_x , min_y , max_y) = self.positionerWidget.getZoomPath(inum)
            num_dots = template["pixels_per_unit"] * template["images"][inum]["side_size"]
            new_image = mimage.MandelImage(min_x,min_y,max_x,max_y,num_dots,num_dots,num_bits,template["high_precision"])
            for y in range(0,num_dots): 
                new_image.CalcColorOneLine(y)
                img_value = int(((y+1)*100) / num_dots)
                self.updateImgProgressBar(img_value)
            all_images.append(new_image)
            if args.verbose:
                print("Interactive Gened image:",inum)    
            bg_value = int(((inum+1)*100) /  template["num_images"])
            if args.verbose:
                print("BG :",bg_value)    
            self.updateBgProgressBar(bg_value)
        genBackgroundFile()
        msg_txt = "The Background Imageas was Gernated.\nFile location:%s" % (args.ozfile)
        dlg = FlexDialog("Success",msg_text)
        dlg.exec()


    def genZoomCountText(self):
        text  = "Zoom Path Points Defined: %d (out of %d)" % (self.positionerWidget.getPoints(), (template["num_images"]))
        return text


#
# mbg Helper Functions 
#

def genImages():
    num_bits = template["bits_per_color"]

    for inum in range(0,template["num_images"]):
        min_x = zoom["min_x"][inum]
        max_x = zoom["max_x"][inum]
        min_y = zoom["min_y"][inum]
        max_y = zoom["max_y"][inum]

        num_dots = template["pixels_per_unit"] * template["images"][inum]["side_size"]
        new_image = mimage.MandelImage(min_x,min_y,max_x,max_y,num_dots,num_dots,num_bits,template["high_precision"])
        new_image.CalcColorAll()
        all_images.append(new_image)
        if args.verbose:
            print("Gened image:",inum)

def genBackgroundFile():
    bgImage = bmp.BmpFile( template["width"], template["height"]) 
    for inum in range(0,template["num_images"]):
        bgImage.ColorImage(
                template["images"][inum]["bg_x"], # start x
                template["images"][inum]["bg_y"], # start y
                template["pixels_per_unit"] * template["images"][inum]["side_size"], # size
                template["rgb"], # rbg
                template["bits_per_color"], # bits_per_color
                template["brightness_shift"], # bright_shift
                all_images[inum])
        if args.verbose:
            print("Moved image to Background. Image:",inum)
    bgImage.Save(args.ofile)

def genBackground():
    genImages()            
    genBackgroundFile()

#
# mbg Start
#

all_images = []

# CLI Parser
parser = argparse.ArgumentParser(description='Mandelbrot Background')
parser.add_argument("--ifile", help="Template file (.hjson)", default="templates/eight.json")
parser.add_argument("--izfile", help="Input Zoom path file (.hjson)", default="zoom/default_eight.json")
parser.add_argument("--ofile", help="Output file (.bmp)", default="bg.bmp")
parser.add_argument("--ozfile", help="Output Zoom path file (.hjson)", default="")
parser.add_argument("-v", "--verbose", help="Increase output verbosity",action ="store_true") 
parser.add_argument("--nogui", help="No Graphical User Interface",action ="store_true") 
parser.add_argument('-V', '--version', action='version', version="%(prog)s ("+__version__+")")
args = parser.parse_args()

# Template File Read 
is_real_template = os.path.isfile(args.ifile)
if(is_real_template):
    if args.verbose:
        print("Opening:",args.ifile)
    template = hjson.load(open(args.ifile))
else:
    err_line = "Error: Template File (%s) not found" % args.ifile
    print(err_line)
    exit(1)
# Zoom File Read
is_real_zoom = os.path.isfile(args.izfile)
if is_real_zoom:
    if args.verbose:
        print("Opening:",args.izfile)
    zoom = hjson.load(open(args.izfile))
# Gui or Not
if(args.nogui):
    if(is_real_zoom == False):
        err_line = "Error: Zoom File (%s) not found" % args.izfile
        print(err_line)
        exit(1)
    else:
        genBackground()
else:
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
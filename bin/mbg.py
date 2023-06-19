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

# High Precision Floating Point
from decimal import *
# more than 3 days to finish
#getcontext().prec = 1024
getcontext().prec = 64 
Decimal('Infinity')
# 1024 Decimal precision

# GUI  Imports
from PyQt5 import (QtWidgets, QtCore)
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QListWidgetItem, QLineEdit,
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
from version import __version__
import mimage as mimage
import bmp as bmp
import desktop as desktop

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

        self.zoomValue = 0.95 
        self.zoomIn= True 

        print("Positioner Widget")

    def getPoints(self):
        return(self.pointsDefined)

    def getZoomPath(self,inum):
        return (
            (self.zoomPath["min_x"][inum],
            self.zoomPath["max_x"][inum],
            self.zoomPath["min_y"][inum],
            self.zoomPath["max_y"][inum]))

    def setZoomIn(self, zoom_in):
        self.zoomIn.zoom_in

    def setZoom(self, zoomValue):
        self.zoomValue = zoomValue

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        for y in range(0,40):
            for x in range(0,40):
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
            if(self.zoomIn):
                self.real_length = self.real_length * self.zoomValue 
            else:
                self.real_length = self.real_length / self.zoomValue 
            self.min_real_x = center_x - self.real_length/float(2)
            self.max_real_x = center_x + self.real_length/float(2)
            self.min_real_y = center_y - self.real_length/float(2)
            self.max_real_y = center_y + self.real_length/float(2)
            self.image.RePosition(
                    self.min_real_x,
                    self.min_real_y,
                    self.max_real_x,
                    self.max_real_y
                    )
            self.repaint()
            self.appendPoint(self.min_real_x,self.max_real_x,self.min_real_y,self.max_real_y)
            self.parent.updateAfterZoomSelect()
        else:
            self.parent.tellUserTooManyZooms()
        
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
        self.pathAllDefined = False
        self.pointsDefined = 0 
        self.zoomPath = {} 
        self.zoomPath["min_x"] = []
        self.zoomPath["max_x"] = []
        self.zoomPath["min_y"] = []
        self.zoomPath["max_y"] = []
        self.appendPoint(-1.0,2.0,-1.5,1.5)

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
            print("Writing Zoom Path to file:",args.ozfile)
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
        self.desktop_helper = desktop.Desktop()
        self.initUI()

    def initUI(self):
        self.wid = QtWidgets.QWidget(self)
        self.setCentralWidget(self.wid)
        self.setGeometry(100,100,512,384)
        self.setFixedSize(512,384)
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
        #          H2
        #   V4
        #     w
        #     H3
        #     H4

        vbox1 = QtWidgets.QVBoxLayout()
        vbox2 = QtWidgets.QVBoxLayout()
        vbox3 = QtWidgets.QVBoxLayout()
        vbox4 = QtWidgets.QVBoxLayout()

        hbox1 = QtWidgets.QHBoxLayout()
        hbox2 = QtWidgets.QHBoxLayout()
        hbox3 = QtWidgets.QHBoxLayout()
        hbox4 = QtWidgets.QHBoxLayout()

        self.positionerWidget = PositionerWidget(self)
        vbox2.addWidget(self.positionerWidget)

        vbox2_widget = QWidget()
        vbox2_widget.setLayout(vbox2)
        vbox2_widget.setFixedWidth(200)

        template_label  =  QtWidgets.QLabel()
        template_label_text = "Template File: %s" % (args.ifile)
        template_label.setText(template_label_text)
        template_label.setFont(QFont('SansSerif', 10))
        vbox3.addWidget(template_label)

        desktop_size_label  =  QtWidgets.QLabel()
        desktop_size_label_text = "Select your desktop size"
        desktop_size_label.setText(desktop_size_label_text)
        desktop_size_label.setFont(QFont('SansSerif', 10))
        vbox3.addWidget(desktop_size_label)

        self.desktop_list_widget =  QListWidget(self)
        all_desktops = self.desktop_helper.GetAllSizes()
        all_desktop_items = []
        for d in all_desktops:
            all_desktop_items.append(QListWidgetItem(d))    
        for di in all_desktop_items:
            self.desktop_list_widget.addItem(di)
        self.desktop_list_widget.setCurrentRow(self.desktop_helper.GetDefault())
        vbox3.addWidget(self.desktop_list_widget)

        slider_title= QtWidgets.QLabel()
        slider_title.setText("Zoom In Magnification (1x to 10x)")
        slider_title.setFont(QFont('SansSerif', 10))
        vbox3.addWidget(slider_title)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(20)
        self.slider.setValue(2)
        self.slider.valueChanged.connect(self.doSliderValueChange)
        hbox2.addWidget(self.slider)

        self.zoomin_check_box = QCheckBox("Zoom In")
        self.zoomin_check_box.setChecked(True)
        self.zoomin_check_box.stateChanged.connect(self.doZoomInChanged)
        hbox2.addWidget(self.zoomin_check_box)
        vbox3.addLayout(hbox2)

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
        hbox3.addWidget(bg_progress_label)

        self.bg_progress_bar = QProgressBar(self)
        self.updateBgProgressBar(0)
        hbox3.addWidget(self.bg_progress_bar)

        img_progress_label = QtWidgets.QLabel()
        img_progress_label.setText("Image Generation Progress:")
        img_progress_label.setFont(QFont('SansSerif', 10))
        hbox4.addWidget(img_progress_label)

        self.img_progress_bar = QProgressBar(self)
        self.updateImgProgressBar(0)
        hbox4.addWidget(self.img_progress_bar)

        hbox1.addWidget(vbox2_widget)
        hbox1.addLayout(vbox3)
        vbox1.addLayout(hbox1)
        vbox1.addLayout(vbox4)
        vbox1.addLayout(hbox3)
        vbox1.addLayout(hbox4)

        self.wid.setLayout(vbox1)

    def doZoomInChanged(self):
        if args.verbose:
            print("ZoomIn Change")
        self.positionerWidget.setZoomIn(self.zoomin_check_box.isChecked())

    def doSliderValueChange(self):
        value = self.slider.value()
        zoomValue =  (float(0.05) * (21-value))
        self.positionerWidget.setZoom(zoomValue)

    def doResetButton(self):
        if args.verbose:
            print("Reset Button")
        self.positionerWidget.reset()
        self.updateAfterZoomSelect()

    def doDrawButton(self):
        # Get DesktopSize
        desktop_size_num = self.desktop_list_widget.currentRow()
        self.desktop_helper.SetDefault(desktop_size_num)
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

    def tellUserTooManyZooms(self):
        msg_txt = "All image locations are defined"
        dlg = FlexDialog("Error",msg_txt)
        dlg.exec()

    def checkWriteZoomPath(self):
        if(args.ozfile != ""):
            if (self.positionerWidget.getPoints() == template["num_images"]):
                self.positionerWidget.writeZoomPathFile()

    def genImagesInteractive(self):
        num_bits = template["bits_per_color"]

        (pixels_per_unit,xpad,ypad) = desktop_helper.GetPixelsPerUnitAndPads(template["x_units"],template["y_units"])
        for inum in range(0,template["num_images"]):
            (min_x, max_x , min_y , max_y) = self.positionerWidget.getZoomPath(inum)
            num_dots = pixels_per_unit * template["images"][inum]["side_size"]
            new_image = mimage.MandelImage(min_x,min_y,max_x,max_y,num_dots,num_dots,num_bits,template["high_precision"])
            for y in range(0,num_dots): 
                new_image.CalcColorOneLine(y)
                img_value = int(((y+1)*100) / num_dots)
                self.updateImgProgressBar(img_value)
            all_images.append(new_image)
            if args.verbose:
                print("Interactive Gened image:",(inum+1))    
            bg_value = int(((inum+1)*100) /  template["num_images"])
            self.updateBgProgressBar(bg_value)
        genBackgroundFile(pixels_per_unit,xpad,ypad)
        msg_txt = "The Background Image was Gernated.\nFile location:%s" % (args.ozfile)
        dlg = FlexDialog("Success",msg_txt)
        dlg.exec()
        exit(0)


    def genZoomCountText(self):
        text  = "Zoom Path Points Defined: %d (out of %d)" % (self.positionerWidget.getPoints(), (template["num_images"]))
        return text


#
# mbg Helper Functions 
#

def genImages(pixels_per_unit):
    num_bits = template["bits_per_color"]

    for inum in range(0,template["num_images"]):
        min_x = zoom["min_x"][inum]
        max_x = zoom["max_x"][inum]
        min_y = zoom["min_y"][inum]
        max_y = zoom["max_y"][inum]

        num_dots = pixels_per_unit * template["images"][inum]["side_size"]
        new_image = mimage.MandelImage(min_x,min_y,max_x,max_y,num_dots,num_dots,num_bits,template["high_precision"])
        new_image.CalcColorAll()
        all_images.append(new_image)
        if args.verbose:
            print("Gened image:",inum+1)

def genBackgroundFile(pixels_per_unit,padx,pady):
    width = desktop_helper.GetXSize()
    height = desktop_helper.GetYSize()
    bgImage = bmp.BmpFile( width, height) 
    for inum in range(0,template["num_images"]):
        bgImage.ColorImage(
                template["images"][inum]["bg_x"]*pixels_per_unit+padx, # start x
                template["images"][inum]["bg_y"]*pixels_per_unit+pady, # start y
                pixels_per_unit * template["images"][inum]["side_size"], # size
                template["rgb"], # rbg
                template["bits_per_color"], # bits_per_color
                template["brightness_shift"], # bright_shift
                all_images[inum])
        if verbose:
            print("Moved image to Background. Image:",(inum+1))
    bgImage.Save(args.ofile)

def genBackground():
    (pixels_per_unit,padx,pady) = desktop_helper.GetPixelsPerUnitAndPads(template["x_units"],template["y_units"])
    genImages(pixels_per_unit)            
    genBackgroundFile(pixels_per_unit,padx,pady)

#
# mbg Start
#

all_images = []

# CLI Parser
#parser = argparse.ArgumentParser(description='Mandelbrot Background')
#parser.add_argument("--ifile", help="Template file (.hjson)", default="~/eight.json")
#parser.add_argument("--ofile", help="Output file (.bmp)", default="images/bg.bmp")
#parser.add_argument("--ozfile", help="Output Zoom path file (.hjson)", default="")
#parser.add_argument("-v", "--verbose", help="Increase output verbosity",action ="store_true") 
#parser.add_argument("--nogui", help="No Graphical User Interface",action ="store_true") 
#parser.add_argument("--izfile", help="NoGUI: Input Zoom path file (.hjson)", default="")
#parser.add_argument("--display", help="NoGUI: Display Size File (.hjson)",default="display/sz1920x1080.json") 
#parser.add_argument('-V', '--version', action='version', version="%(prog)s ("+__version__+")")
#args = parser.parse_args()
verbose = False
# Template File Read 
template={}
template["num_images"] = 8
template["rgb"] =  "bgr"
template["bits_per_color"]=  4
template["brightness_shift"]=  4
template["x_units"]= 16
template["y_units"]=  8
template["high_precision"] = False
template["images"][0]["side_size"] = 2
template["images"][0]["bg_x"] = 0
template["images"][0]["bg_y"] = 6
template["images"][1]["side_size"] = 2
template["images"][1]["bg_x"] = 2
template["images"][1]["bg_y"] = 6
template["images"][2]["side_size"] = 2
template["images"][2]["bg_x"] = 0
template["images"][2]["bg_y"] = 4
template["images"][3]["side_size"] = 2
template["images"][3]["bg_x"] = 2
template["images"][3]["bg_y"] = 4
template["images"][4]["side_size"] = 4
template["images"][4]["bg_x"] = 4
template["images"][4]["bg_y"] = 4
template["images"][5]["side_size"] = 4
template["images"][5]["bg_x"] = 0
template["images"][5]["bg_y"] = 0
template["images"][6]["side_size"] = 4
template["images"][6]["bg_x"] = 4
template["images"][6]["bg_y"] = 0
template["images"][7]["side_size"] = 8
template["images"][7]["bg_x"] = 8
template["images"][7]["bg_y"] = 0
app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

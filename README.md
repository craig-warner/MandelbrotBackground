# Mandelbrot Background Drawer

Mandelbrot-background generates custom Descktop backgrounds for you personal computer.  The backgrounds
are made up of Mandelbrot fractal images of different sizes and different positions in the real number, complex
number coordinate system.   By selecting the Mandelbrot image locations you want to me part of your desktop
background, you can make wallpaper that looks like this.

<img src="snap/gui/sz1920x1080.png">

The program also supports a Command Line Interface (CLI) for sophisticated users who want more control.
The CLI is:
```
usage: mandelbrot-background [-h] [--ifile IFILE] [--ofile OFILE] [--ozfile OZFILE] [-v] [--nogui] [--izfile IZFILE]
                             [--display DISPLAY] [-V]

Mandelbrot Background

options:
  -h, --help         show this help message and exit
  --ifile IFILE      Template file (.hjson)
  --ofile OFILE      Output file (.bmp)
  --ozfile OZFILE    Output Zoom path file (.hjson)
  -v, --verbose      Increase output verbosity
  --nogui            No Graphical User Interface
  --izfile IZFILE    NoGUI: Input Zoom path file (.hjson)
  --display DISPLAY  NoGUI: Display Size File (.hjson)
  -V, --version      show program's version number and exit
```




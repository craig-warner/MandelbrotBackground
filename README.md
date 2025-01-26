# Mandelbrot Background Drawer

Mandelbrot-background generates custom Desktop backgrounds for you personal computer.  The backgrounds
are made up of Mandelbrot fractal images of different sizes and different positions in the real number, complex
number coordinate system.   By selecting the Mandelbrot image locations you can personalize your wallpaper. Below is an example background image.

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

## Snap Build Steps

<pre>
%snapcraft
// debug snapcraft
%snapcraft --debug
// Install locally
%snap install --dangerous mandelbrot-background_1.10_amd64.snap
// debug 
%snap run --shell mandelbrot-background
// remove app from machine 
%snap remove mandelbrot-background
// start over snapping 
 %snapcraft clean
</pre>
## LXD Steps
<pre>
 %sudo apt install lxd
 %sudo adduser username lxd
</pre>




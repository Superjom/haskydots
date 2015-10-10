dependencies
---------------
* `convert` from ImageMagick
* python2.7


texi2pdf -q 1.tex
convert -density 300 1.pdf -quality 100 -sharpen 0x1.0 1.png

#!/bin/bash
set -e -x

python rnnsearch.py > rnnsearch.dot

sh build_images.sh

dot -Tpdf rnnsearch.dot -o rnnsearch.pdf
dot -Tpng rnnsearch.dot -o rnnsearch.png

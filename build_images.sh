#!/bin/bash
set -e -x

ROOT="_tmp"

# check if the tex file is compiled
need_to_compile() {
    texfile=$1
    basefile=${texfile%.*}
    md5file=${basefile}.md5
    md5code=`md5 $texfile`
    if [ -f $md5file ]; then
        if [ "$md5code" == "`cat $md5file`" ]; then
            echo 0
            exit 0
        fi
    fi

    echo $md5code > $md5file

    echo 1
}

for name in `ls $ROOT`; do
    if [ ${name: -4} == ".tex" ]; then

        texfile=$ROOT/$name
        basefile=${texfile%.*}
        pdfile="${basefile}.pdf"
        pngfile="${basefile}.png"
        if [ "`need_to_compile $texfile`" -eq "1" ]; then
            texi2pdf -q $texfile -o $pdfile
            convert -trim -density 150 $pdfile -quality 100 -sharpen 0x1.0 $pngfile
        fi
    fi
done

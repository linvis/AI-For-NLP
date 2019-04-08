#!/bin/bash

if [ ! -n "$1" ]
then
    echo "usage: ./zht2zhs.sh [dir]"
    exit
fi

CUR_DIR=$1

function transfer()
{
    echo $1
    for file in `ls $1`
    do
        # echo $file
        `opencc -i $1'/'$file -o $1'/'chs_$file -c t2s.json`
    done

}

for file_dir in `ls $CUR_DIR`
do
    # echo $file_dir
    # transfer $CUR_DIR'/'$file_dir
    extra_file=$CUR_DIR'/'$file_dir'/.DS_Store'
    rm $extra_file
done



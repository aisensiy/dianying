#!/bin/sh

# workpath=/Users/xushanchuan/projects/dianying
workpath=/home/bae/app

echo "$(date)" >> $workpath/log/cron.log
set -x
cd $workpath
export PYTHONPATH=$PYTHONPATH:$workpath
python $workpath/get_douban_movies.py 2>&1 >> $workpath/log/cron.log

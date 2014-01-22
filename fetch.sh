#!/bin/sh

# workpath=/Users/xushanchuan/projects/dianying
workpath=/home/bae/app
logpath=/home/bae/log

echo "$(date)" >> $logpath/cron.log
set -x
cd $workpath
export PYTHONPATH=$PYTHONPATH:$workpath:/home/bae/app/deps
SERVER_SOFTWARE=bae python $workpath/get_douban_movies.py 2>&1 >> $logpath/cron.log

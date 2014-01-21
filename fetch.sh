echo "$(date)" >> /home/bae/log/cron.log
cd /home/bae/app
PYTHONPATH=$PYTHONPATH:/home/bae/app
python /home/bae/app/get_douban_movies.py 2>&1 >> /home/bae/log/cron.log

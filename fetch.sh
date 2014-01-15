echo "$(date)" >> /home/bae/log/cron.log
python /home/bae/app/get_douban_movies.py

echo "$(date)" >> /home/bae/log/cron.log
python /home/bae/app/test.py 2>&1 >> /home/bae/log/cron.log

HOME=/home/ftr
PYTHON=/home/ftr/anaconda3/envs/python34/bin/python

run:
	nohup $(PYTHON) runserver.py  > app.log 2>&1 &

stop:
	PS="`ps -ef | grep runserver | grep -v grep | awk '{print $2}'`"
	kill -9 $(PS)

status:
	ps -ef | grep runserver

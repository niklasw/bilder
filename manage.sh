#!/usr/bin/env bash

source $PWD/venv/bin/activate
#FLASK_SERVER='192.168.10.210'
#FLASK_PORT=5000
LOG_DIR=./log
LOG_NAME=bilder
LOG_FILE=$LOG_NAME.log

function start_app()
{
	if [ -f $LOG_DIR/$LOG_FILE ]
	then
		OLD_LOG=${LOG_NAME}.$(date +%s).log
		mv $LOG_DIR/$LOG_FILE $LOG_DIR/$OLD_LOG
		gzip $LOG_DIR/$OLD_LOG
	fi
	
	python3 app.py $@ > $LOG_DIR/$LOG_FILE 2>&1 &
}

function stop_app()
{
	if [ -f $LOG_DIR/$LOG_FILE ]
	then
		TUB_PID=$(awk '$1 == "PID:" {print $2}' $LOG_DIR/$LOG_FILE)

		read -p "Kill process $TUB_PID? y/[n]" ans

		if [[ "$ans" == "y" ]]
		then
			kill $TUB_PID
			# wait for pid to finish
			tail --pid=$TUB_PID -f /dev/null
		else
			echo "No action"
		fi
	else
		echo "No log file found ($LOG_DIR/$LOG_FILE). Can not stop."
	fi
}

function tail_log()
{
	tail -f $LOG_DIR/$LOG_FILE -n 100
}

function usage()
{
	echo -e "\n\tmanage.sh [start|stop|log|debug]\n"
	exit 1
}

TASK=$1

case $TASK in
	start|run)
		start_app
		;;
	debug)
		start_app -g
		tail_log
		;;
	stop|quit|abort)
		stop_app
		;;
	restart)
		stop_app
		start_app
		;;
	tail|log)
		tail_log
		;;
	*)
		usage
		;;
esac

#!/bin/bash
### BEGIN INIT INFO
#
# Provides:		geiger-counter.sh
# Required-Start:	$remote_fs
# Required-Stop:	$remote_fs
# Default-Start:	2 3 4 5
# Default-Stop:		0 1 6
# Short-Description:	geiger-counter initscript

#
### END INIT INFO
## Fill in name of program here.
PROG="geiger-counter.py"
PROG_PATH="/home/pi/geiger-counter"
PROG_ARGS=""
PIDFILE="/var/run/geiger-counter.pid"

start() {
      if [ -e $PIDFILE ]; then
          ## Program is running, exit with error.
          echo "Error! $PROG is currently running!" 1>&2
          exit 1
      else
          ## Change from /dev/null to something like /var/log/$PROG if you want to save output.
          cd $PROG_PATH
          ./$PROG $PROG_ARGS 2>&1 >/dev/null &
          echo "$PROG started"
          touch $PIDFILE
      fi
}

stop() {
      if [ -e $PIDFILE ]; then
          ## Program is running, so stop it
         echo "$PROG is running"
         killall $PROG
         rm -f $PIDFILE
         echo "$PROG stopped"
      else
          ## Program is not running, exit with error.
          echo "Error! $PROG not started!" 1>&2
          exit 1
      fi
}

## Check to see if we are running as root first.
## Found at http://www.cyberciti.biz/tips/shell-root-user-check-script.html
if [ "$(id -u)" != "0" ]; then
      echo "This script must be run as root" 1>&2
      exit 1
fi

case "$1" in
      start)
          start
          exit 0
      ;;
      stop)
          stop
          exit 0
      ;;
      reload|restart|force-reload)
          stop
          start
          exit 0
      ;;
      **)
          echo "Usage: $0 {start|stop|reload}" 1>&2
          exit 1
      ;;
esac
exit 0

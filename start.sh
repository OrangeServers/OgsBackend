#!/bin/bash
dir=$(dirname $0)
case $1 in
  'start')
  echo 'start orangeservers .......'
  nohup /data/server/python371/bin/python3 ${dir}/init.py > /data/logs/orangeservers.log 2>&1 &
  [[ $? == 0 ]] && echo 'start orangeservers is ok' || exit 4
  echo 'start orangeservers .......'
  nohup /data/server/python371/bin/python3 ${dir}/ogsssh/run.py > /data/logs/orangessh.log 2>&1 &
  [[ $? == 0 ]] && echo 'start orangessh is ok' || exit 4
  ;;
  'stop')
  echo 'stop orangeservers .......'
  ps aux |grep "/data/server/python371/bin/python3 ${dir}/init.py"|grep -v grep|awk '{print $2}'| xargs kill
  [[ $? == 0 ]] && echo 'stop orangeservers is ok' || exit 4
  echo 'stop orangessh .......'
  ps aux |grep "/data/server/python371/bin/python3 ${dir}/ogsssh/run.py"|grep -v grep|awk '{print $2}'| xargs kill
  [[ $? == 0 ]] && echo 'stop orangessh is ok' || exit 4
  ;;
  'restart')
    echo 'stop orangeservers .......'
    ps aux |grep "/data/server/python371/bin/python3 ${dir}/init.py"|grep -v grep|awk '{print $2}'| xargs kill -9
    if [ $? == 0 ]; then
        echo 'start orangeservers .......'
        nohup /data/server/python371/bin/python3 ${dir}/init.py > /data/logs/orangeservers.log 2>&1 &
        [[ $? == 0 ]] && echo 'start orangeservers is ok' || exit 4
    else
      echo 'stop orangeservers is error!'
      exit 4
    fi
    echo 'stop orangessh .......'
    ps aux |grep "/data/server/python371/bin/python3 ${dir}/ogsssh/run.py"|grep -v grep|awk '{print $2}'| xargs kill
    if [ $? == 0 ]; then
        nohup /data/server/python371/bin/python3 ${dir}/init.py > /data/logs/orangeservers.log 2>&1 &
        [[ $? == 0 ]] && echo 'start orangessh is ok' || exit 4
    else
      echo 'stop orangessh is error!'
      exit 4
    fi
    ;;
    *)
    echo 'Please enter parameters start|stop|restart !'
esac

#!/bin/bash
# python环境变量路径，默认 python3 根据需求指定全路径
python3_path='python3'
dir=$(cd "$(dirname "$0")";pwd)

function start_app() {
  echo 'start orangeservers .......'
  nohup $python3_path ${dir}/init.py > /data/logs/orangeservers.log 2>&1 &
  [[ $? == 0 ]] && echo 'start orangeservers is ok' || echo 'start orangeservers error'; exit 4
  echo 'start orangeservers .......'
  nohup $python3_path ${dir}/ogsssh/run.py > /data/logs/orangessh.log 2>&1 &
  [[ $? == 0 ]] && echo 'start orangessh is ok' || echo 'start orangessh error'; exit 4
}

function stop_app() {
  echo 'stop orangeservers .......'
  ps aux |grep "$python3_path ${dir}/init.py"|grep -v grep|awk '{print $2}'| xargs kill
  [[ $? == 0 ]] && echo 'stop orangeservers is ok' || echo 'stop orangeservers error'; exit 4
  echo 'stop orangessh .......'
  ps aux |grep "$python3_path ${dir}/ogsssh/run.py"|grep -v grep|awk '{print $2}'| xargs kill
  [[ $? == 0 ]] && echo 'stop orangessh is ok' || echo 'stop orangessh error'; exit 4
}

case $1 in
  'start')
  start_app
  ;;
  'stop')
  stop_app
  ;;
  'restart')
  stop_app
  start_app
    ;;
    *)
    echo 'Please enter parameters start|stop|restart !'
esac

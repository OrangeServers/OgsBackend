#!/bin/bash
# python环境变量路径，默认 python3 根据需求指定全路径
python3_path='python3'

dir=$(cd "$(dirname "$0")";pwd)

log_dir="${dir}/logs"

[[ ! -d $log_dir ]] && mkdir $log_dir

function start_app() {
  echo 'start orangeservers .......'
  nohup $python3_path ${dir}/init.py > ${log_dir}/orangeservers.log 2>&1 &
  sleep 2
  orangeservers_num=$(ps aux |grep "$python3_path ${dir}/init.py"|grep -v grep|wc -l)
  [[ $orangeservers_num != 0 ]] && echo 'start orangeservers is ok' || tail ${log_dir}/orangeservers.log
  echo 'start orangessh .......'
  nohup $python3_path ${dir}/ogsssh/run.py >  ${log_dir}/orangessh.log 2>&1 &
  sleep 2
  orangessh_num=$(ps aux |grep "$python3_path ${dir}/ogsssh/run.py"|grep -v grep|wc -l)
  [[ $orangessh_num != 0 ]] && echo 'start orangessh is ok' || tail ${log_dir}/orangessh.log
}

function stop_app() {
  echo 'stop orangeservers .......'
  orangeservers_num=$(ps aux |grep "$python3_path ${dir}/init.py"|grep -v grep|wc -l)
  sleep 1
  if [ $orangeservers_num != 0 ]; then
      ps aux |grep "$python3_path ${dir}/init.py"|grep -v grep|awk '{print $2}'| xargs kill -9
      [[ $? == 0 ]] && echo 'stop orangeservers is ok' || echo 'stop orangeservers error'
  else
    echo 'orangeservers is not running!'
  fi

  echo 'stop orangessh .......'
  orangessh_num=$(ps aux |grep "$python3_path ${dir}/ogsssh/run.py"|grep -v grep|wc -l)
  sleep 1
  if [ $orangessh_num != 0 ]; then
      ps aux |grep "$python3_path ${dir}/ogsssh/run.py"|grep -v grep|awk '{print $2}'| xargs kill -9
      [[ $? == 0 ]] && echo 'stop orangessh is ok' || echo 'stop orangessh error'
  else
    echo 'orangessh is not running!'
  fi
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

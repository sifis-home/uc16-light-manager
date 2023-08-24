#!/bin/sh
FILE=/services/leader_file.txt

function start_light_manager() {
  echo "Starting Light Manager"
  /launch_light_manager.sh &

}


function stop_light_manager() {

  cont=0
  while pgrep -f /launch_light_manager.sh > /dev/null 2>&1; do

    force=""

    if [ $cont -gt 9 ]; then
      echo "Forcing kill /launch_light_manager.sh"
      force="-9"
    fi

    ppid=$(ps | grep /launch_light_manager.sh | awk '{print $1}' | head -n 1)

    pkill $force -P $ppid


    if [ $? -eq 0 ]; then  # il processo esisteva ed è stato killato
      echo "Killed /launch_light_manager.sh "
    fi

    echo "Waiting for /launch_light_manager.sh death ..."

    sleep 1
    cont=$((cont+1))
  done

}


function check() {

  if [[ -f $FILE ]] ; then

     # il file esiste

     if ! pgrep -f /launch_light_manager.sh > /dev/null 2>&1 ; then
       start_light_manager
     fi

  else

     # il file non esiste
     stop_light_manager

  fi

}

trap "echo 'Ricevuto Signal SIGUSR1'; check" SIGUSR1

while true;
  do
   check
   sleep 5 &
   wait $!
done

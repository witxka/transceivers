#!/bin/sh

# @param FQDN name Tecnair conditioner FQDN for modbus tcp/ip

  ip=`host $1 | awk '{print $NF;}'`

  cat bad_signals.csv | 
  awk -v ip=$ip  -F ',' '{$torun="./agent_modbus "ip" 502 "$2":1:bool:\""$4"\" 2>/dev/null|iconv -c -t koi-7| tr a-zA-Z A-Za-z"; system($torun);}' | 
  awk 'BEGIN {signalOK=0;signalERROR=0;signalWARNING=0;} 
    { if($2!=0) {
        if ($1==630 || $1==801) {
          signalWARNING+=1;
	  printf("(WARN)%s , ", $0);
	} else {	
          signalERROR+=1;
	  printf("(CRIT)%s , ", $0);
        }  
      } else {
        signalOK+=1;
      }
    } END {
      print("Technair signals proceeded: total="signalOK+signalERROR", OK="signalOK", ERROR="signalERROR", WARNING="signalWARNING);
      print(" | total="signalOK+signalERROR", OK="signalOK", ERROR="signalERROR", WARNING="signalWARNING);
      if (signalERROR!=0) {
	exit(2);       
      } else if (signalWARNING!=0) {
        exit(1);
      } else {
        exit(0);
      }
    }'

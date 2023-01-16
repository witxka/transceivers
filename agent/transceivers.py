#!/usr/bin/env python3
# encoding: utf-8

# Description  : Read optical transceiver info throught ethtool and ouput it as JSON.
#                Parameters to read are given with csv file. 
# Author       : witxka@gmail.com 

import subprocess
import re
import json
import sys
import csv
import socket
import logging
import traceback

def strToFloat(strVal):
  try:
    return float(strVal)
  except ValueError as e:
    return None

def get_info(sensors, scope, interface):
    """Get optical transceiver parameters from ethtool and output them as JSON.

    @param sensors   The dictionary of parameters to read and format output.
    @param scope     The scope for the parameters.
    @param interface The network interface to read.
    @return The dictionary for parameter values.
    """

    infoFor = {}
    info = {}
    info["Adapter"] = scope
    outputDict = {}

    for sensor in sensors:
      sensorDict = {}
      ethtoolInfo = subprocess.check_output(["sudo", "ethtool", "-m", interface])
      stringToSearch = sensor["sensor"] + ".*:.*"
      stringToSearchTranslated = stringToSearch.translate(str.maketrans({'(': '\(', ')': '\)'}))
      sensor_input = re.search(stringToSearchTranslated, ethtoolInfo.decode('utf-8'), re.MULTILINE).group(0).split()[int(sensor["pos"])]
      
      sensorDict[sensor["name"] + "_input"] = round(strToFloat(sensor_input),2)
      sensorDict[sensor["name"] + "_max"] = strToFloat(sensor["warn"])
      sensorDict[sensor["name"] + "_crit"] = strToFloat(sensor["crit"])
    

      info[sensor["sensor"] + ", " + sensor["type"]] = sensorDict

    outputDict[interface] = info
    return outputDict

def read_csv(filename):
  with open(filename) as f:
    file_data=csv.reader(f)
    headers=next(file_data)
    return [dict(zip(headers,i)) for i in file_data]

def main():
  """Main function. Read optical transceiver parameters from ethtool and 
    output them as JSON.
    
  @param argv[1] The network interface.
  @param argv[2] The csv file with parameters to read.
  @param argv[3,4,...] Additional interface and parameters.
  @return The output in JSON format.
  """

  try:
    # add param checking
    if (len(sys.argv) < 3):
      print("Usage: {0} interface1 transceiver1.csv [interface2 trasceiver2.csv ...] ".format(sys.argv[0]))
      print("  interface1: The network interface to use.")
      print("  transceiver1.csv: The csv file with parameters to read.")
      print("  ...: Additional interfaces and csv files to read.")
      sys.exit(0)

    interface = sys.argv[1]
    info = {}
    for i in range(1,len(sys.argv),2):
      interface = sys.argv[i]
      sensors = read_csv(sys.argv[i+1])
      scope = sys.argv[i+1].split(".")[0]
      info.update(get_info(sensors, scope, interface).items());
    print(json.dumps(info))
  except Exception as e:
    logging.error(traceback.format_exc())

if __name__ == "__main__":
    main()

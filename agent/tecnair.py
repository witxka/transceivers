#!/usr/bin/env python
# encoding: utf-8

# Description  : Read tecnair conditioner sensors through modbus and ouput it as JSON.
#                Sensors are given with csv file. The output with check_mk header.
#                The script use agent_modbus cpp application.
# Author       : witxka@gmail.com 

import subprocess
import json
import sys
import csv
import socket
import logging

def strToFloat(strVal):
  try:
    return float(strVal)
  except ValueError as e:
    return None

def get_info(sensors, tecnairIP):
    """Get sensors values from tecnair conditioner through modbus over IP and output them as JSON.

    @param sensors   The dictionary of sensors to read and format output.
    @param tecnairIP The IP address for tecnair conditioner to connect to modbus over IP.
    @return The dictionary for sensors values with their parameters.
    """

    infoFor = {}
    info = {}
    info["Adapter"] = "parameters"
    for sensor in sensors:
      sensorDict = {}
      modbusSensor = subprocess.check_output(["./tecnair_sensors_modbus", tecnairIP,
        "502", sensor["addr"] + ":1"])
      sensorDict[sensor["name"] + "_input"] = round(strToFloat(modbusSensor)*strToFloat(sensor["multiply"]),2)
      sensorDict[sensor["name"] + "_max"] = strToFloat(sensor["warn"])
      sensorDict[sensor["name"] + "_crit"] = strToFloat(sensor["crit"])

      info[sensor["name"]] = sensorDict

    infoFor[socket.gethostbyaddr(tecnairIP)[0]] = info
    return infoFor  

def read_csv(filename):
  with open(filename) as f:
    file_data=csv.reader(f)
    headers=next(file_data)
    return [dict(zip(headers,i)) for i in file_data]

def main():
  """Main function. Read sensors for tecnair conditioner and 
    output them as JSON.
    
  @param argv[1] The csv file with tecnair sensors to check.
  @param argv[2] The IP address for tecnair conditioner.
  @return The output in JSON format.
  """

  try:
    # add param checking
    if (len(sys.argv) != 3):
      print("Usage: {0} sensors.csv IP".format(sys.argv[0]))
      print("  sensors.csv: The csv file with tenair modbus sensors to check")
      print("  IP: The IP address for modbus over IP for tecnair conditioner")
      sys.exit(0)

    sensors = read_csv(sys.argv[1])
    print(json.dumps(get_info(sensors, sys.argv[2])))
  except Exception as e:
    logging.error(traceback.format_exc())

if __name__ == "__main__":
    main()

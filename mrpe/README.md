check_mk mrpe plugin setup for tecnair conditioner sensors for alarm signals.
Files need to be added to /etc/check_mk dir for mrpe plugin to work.
Alarm signals presentend in csv file generated as documentation pdf->xls->csv.

To build agent_modbus:
  g++ agent_modbus.cpp -o agent_modbus `pkg-config --libs --cflags libmodbus`

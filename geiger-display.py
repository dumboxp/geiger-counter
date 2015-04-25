#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import datetime
import time

# --------------------------------------------------------------
# Geiger Counter - Display Radiation
# read radiation level from MightyOhm Geiger Counter v1.0
# via serial (USB) interface and dispays radiation level
# by Roland Ortner (2015)
# --------------------------------------------------------------

# serial port interface e.g. /dev/serial/by-id/*usb* or /dev/cu.usbserial
SERIAL_PORT = '/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0' 

# interval between readings in seconds (default: 10 sec)
INTERVAL = 10
 
# open serial port using 9600 baud, 8 data bit, 1 stop bit, no parity, no flow control
ser = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False) 
ser.flushInput()
ser.flushOutput()

while True:
  # read values from serial interface
  data_raw = ser.readline()
  # print(data_raw)

  # split csv formated string e.g. CPS, 0, CPM, 21, uSv/hr, 0.11, SLOW
  array = data_raw.split(",")
  cps = array[1].strip()
  cpm = array[3].strip()
  radiation = array[5].strip()
  mode = array[6].strip()

  # get current timestamp
  now = datetime.datetime.utcnow()

  # output current radiation measurements 
  print("Time:      %s" % now.strftime('%Y-%m-%d %H:%M:%S'))
  print("Radiation: %s uSv/h" % radiation)
  print("CPM:       %s" % cpm)
  print("CPS:       %s" % cps)
  print("Mode:      %s" % mode)

  # wait and loop
  time.sleep(INTERVAL)

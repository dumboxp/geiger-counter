#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import xively
import datetime
import time
import requests
import logging

# ---------------------------------------------------------------
# Geiger Counter - Display Radiation
# read radiation level from MightyOhm Geiger Counter v1.0
# via serial (USB) interface and upload to Xively.com data feed.
# by Roland Ortner (2015)
# ---------------------------------------------------------------

# serial port interface e.g. /dev/serial/by-id/*usb* or /dev/cu.usbserial
SERIAL_PORT = '/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0'

# xively.com data feed configuration
XIVELY_API_KEY = 'iPM6CaQHsJcnJea7BMnCQsohBLuChVsr7Wx0WmkXpcXbg7NT'
XIVELY_FEED_ID = '115042809'
XIVELY_FEED_NAME = 'Radioactivity'

# logfile path and filename
LOG_FILE = './geiger-counter.log'

# interval between readings in seconds (default: 10 sec)
INTERVAL = 10

# init xively data feed api client
api = xively.XivelyAPIClient(XIVELY_API_KEY)

# init logger
logger = logging.getLogger('geiger-counter')
hdlr = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)

# main geiger-counter program 
def run():
  logger.info("starting geiger-counter...");
 
  # get xively feed and datastream 
  feed = api.feeds.get(XIVELY_FEED_ID)
  datastream = get_datastream(feed, XIVELY_FEED_NAME)
  datastream.max_value = None
  datastream.min_value = None

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

    # get current timestamp of readings
    now = datetime.datetime.utcnow()

    # update data feed at xively.com
    datastream.at = now
    datastream.current_value = radiation
    try:
      datastream.update()
    except requests.HTTPError as e:
      logger.error("HTTPError({0}): {1}".format(e.errno, e.strerror))

    # log data 
    logger.info("%s; %s CPM, %s CPM, %s uSv" % (now.strftime('%Y-%m-%d %H:%M:%S'), cpm, cps, radiation))  

    # wait interval and loop
    time.sleep(INTERVAL)

# get or create new xively datastream
def get_datastream(feed, feedname):
  try:
    datastream = feed.datastreams.get(feedname)
    logger.info("found existing datastream: "+feedname)
    return datastream
  except:
    logger.info("creating new datastream: "+feedname)
    datastream = feed.datastreams.create(feedname, tags=feedname)
    return datastream

run()

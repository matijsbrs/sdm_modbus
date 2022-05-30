#!/usr/bin/env python3

import argparse
from itertools import product
import json
from socket import SO_ACCEPTCONN
from sqlite3 import Timestamp
from time import sleep


from rx import catch
import src
from src.sdm_modbus.climatron import *

import mysql.connector

from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_nano(dt, offset=-2):
    return int(((dt - epoch).total_seconds() + (offset*3600) )* 1000000000.0)


# You can generate an API token from the "API Tokens Tab" in the UI
token = "aTteDSivr4Hh5xIhYZG5T6facXubuR7mBYA1FnOEJBu_4JCXMpPGB0VGBKwV5oNCzzKjIBrfmje16vsTCJYXoA=="
org = "Behrens"
bucket = "Energy2"


mydb = mysql.connector.connect(
  host="192.168.2.201",
  user="broker",
  password="nopassword",
  database="datastore"
)



mycursor = mydb.cursor()

tijden = [
    {
    'time': '2018-01-01 00:00:00',
    'to'  : '2018-03-25 02:00:00',
    'offset': -1,
    'text' : 'Winter 2017'
    },{
    'time': '2018-03-25 02:00:00',
    'to'  : '2018-10-28 02:00:00',
    'offset': -2,
    'text' : 'Summer 2018'
    },{
    'time': '2018-10-28 02:00:00',
    'to'  : '2019-03-31 02:00:00',
    'offset': -1,
    'text' : 'Winter 2018'
    },{
    'time': '2019-03-31 02:00:00',
    'to'  : '2019-10-27 02:00:00',
    'offset': -2,
    'text' : 'Summer 2019'
    },{
    'time': '2019-10-27 02:00:00',
    'to'  : '2020-03-29 02:00:00',
    'offset': -1,
    'text' : 'Winter 2019'
    },{
    'time': '2020-03-29 02:00:00',
    'to'  : '2020-10-25 02:00:00',
    'offset': -2,
    'text' : 'Summer 2020'
    },{
    'time': '2020-10-25 02:00:00',
    'to'  : '2021-03-28 02:00:00',
    'offset': -1,
    'text' : 'Winter 2020'
    },{
    'time': '2021-03-28 02:00:00',
    'to'  : '2021-10-31 02:00:00',
    'offset': -2,
    'text' : 'Summer 2021'
    },{
    'time': '2021-10-31 02:00:00',
    'to'  : '2022-03-27 02:00:00',
    'offset': -1,
    'text' : 'Winter 2021'
    }
    # ,{
    # 'time': '2022-03-27 02:00:00',
    # 'to'  : '2022-03-31 00:00:00',
    # 'offset': -2,
    # 'text' : 'Summer 2022'
    # }
]


def updateRange(Start, End, Offset):
    mycursor.execute(f"SELECT * FROM EnergyCounters WHERE TimeStamp BETWEEN '{Start}' AND '{End}'") # AND TimeStamp < '2021-01-01 00:00:00'")

    myresult = mycursor.fetchall()

    prev_grid = 0
    prev_solar = 0
    grid_export =0
    solar_import =0
    with InfluxDBClient(url="http://192.168.2.200:8086", token=token, org=org) as client:

        write_api = client.write_api(write_options=SYNCHRONOUS)
            
        for x in myresult:
            Timestamp = unix_time_nano(x[0],offset=Offset)
            grid = x[1]
            solar = x[2]
            if ( prev_grid > 0 ):
                grid_delta = int(grid - prev_grid)
                grid_watt = int(round(grid_delta * 60))

                solar_delta = int(solar - prev_solar)
                solar_watt = int(round(solar_delta * 60))             
                    
                point = Point("mem") \
                    .measurement("energymeter") \
                    .tag("host", "Grid") \
                    .tag("location", "Alkmaar") \
                    .field("export", float(grid_export)) \
                    .field("import", float(grid)) \
                    .field("watt", float(grid_watt-solar_watt)) \
                    .time(Timestamp, WritePrecision.NS)

                write_api.write(bucket, org, point)

                point = Point("mem") \
                    .measurement("energymeter") \
                    .tag("host", "Home") \
                    .tag("location", "Alkmaar") \
                    .field("export", 0.0) \
                    .field("import", 0.0) \
                    .field("watt", float(grid_watt)) \
                    .time(Timestamp, WritePrecision.NS)

                write_api.write(bucket, org, point)

                point = Point("mem") \
                    .measurement("energymeter") \
                    .tag("host", "Solar") \
                    .tag("location", "Alkmaar") \
                    .field("import", float(solar_import)) \
                    .field("export", float(solar)) \
                    .field("watt", float(solar_watt)) \
                    .time(Timestamp, WritePrecision.NS)

                write_api.write(bucket, org, point)


            prev_grid = grid
            prev_solar = solar


subset = []
# subset.append(tijden[-2])
subset.append(tijden[-1])
for moment in tijden:
    print(f"SELECT * FROM EnergyCounters WHERE TimeStamp BETWEEN '{moment['time']}' AND '{moment['to']}'  ({moment['text']})")
    updateRange(moment['time'], moment['to'], moment['offset'])


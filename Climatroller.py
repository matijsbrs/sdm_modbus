#!/usr/bin/env python3

import argparse
from ctypes.wintypes import INT
from itertools import product
import json
from time import sleep


from rx import catch
import src
from src.sdm_modbus.climatron import *

import mysql.connector

from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

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


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--host", type=str, default="192.168.2.200", help="Modbus TCP address")
    argparser.add_argument("--port", type=int, default="502", help="Modbus TCP port")
    argparser.add_argument("--timeout", type=int, default=1, help="Connection timeout")
    argparser.add_argument("--unit", type=int, default=1, help="Modbus device address")
    argparser.add_argument("--json", action="store_true", default=True, help="Output as JSON")
    args = argparser.parse_args()

    huis = src.sdm_modbus.SDM120(
        host=args.host,
        port=args.port,
        timeout=args.timeout,
        unit = 4
    )

    # omnik = src.sdm_modbus.SDM120 (
    #     parent = huis,
    #     unit = 5
    # )

    # sems = src.sdm_modbus.SDM120 (
    #     parent = huis,
    #     unit = 6
    # )

    clima = Clima(
        parent=huis,
        unit=30
    )



    if args.json:
        # print(json.dumps(clima.read_all(scaling=True), indent=4))
        clima.write("freekoeling",data=int(1))
        clima.write("bypass",data=int(1))
        clima.write("highflow",data=int(1))
        
        print(json.dumps(clima.read_all(scaling=True), indent=4))
    else:
        clima.write("bypass",data=int(0) )
        

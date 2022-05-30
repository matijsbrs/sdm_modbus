#!/usr/bin/env python3

import argparse
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
    argparser.add_argument("--json", action="store_true", default=False, help="Output as JSON")
    args = argparser.parse_args()

    huis = src.sdm_modbus.SDM120(
        host=args.host,
        port=args.port,
        timeout=args.timeout,
        unit = 4
    )

    omnik = src.sdm_modbus.SDM120 (
        parent = huis,
        unit = 5
    )

    sems = src.sdm_modbus.SDM120 (
        parent = huis,
        unit = 6
    )

    clima = Clima(
        parent=huis,
        unit=30
    )

    if args.json:
        print(json.dumps(meter.read_all(scaling=True), indent=4))
    else:
        #clima.write("bypass",2);
        for i in range(10000000):
            try:
                # invert 
                huis_watt =  int(huis.read("power_active"))
                omnik_watt = int(omnik.read("power_active"))
                sems_watt =  int(sems.read("power_active")) 

                # omnik_watt = -1000
                # sems_watt  = -250
                # huis_watt  = 3000

                usage_watt = huis_watt
                if sems_watt < 0:
                    usage_watt = (sems_watt*-1) + huis_watt
                
                solar_watt = int((omnik_watt + sems_watt) * -1)
                netto_watt = int(omnik_watt + huis_watt + sems_watt)

                omnik_watt = int(omnik_watt*-1)
                sems_watt = int(sems_watt * -1)

                print(f"huis : {huis_watt}W ")
                print(f"omnik: {omnik_watt}W ")
                print(f"sems : {sems_watt}W ")
                print(f"solar: {solar_watt}W ")
                print(f"grid : {netto_watt}W ")
                print(f"Usage: {usage_watt}W ")

                huis_import_kwh = round(float((huis.read("import_energy_active")) - 14.723999977111816)*1000,4)
                omnik_import_kwh = round(float((omnik.read("import_energy_active")) - 10.350000381469727)*1000,4)
                sems_import_kwh = round(float((sems.read("import_energy_active")) - 0.004999999888241291)*1000,4)

                huis_export_kwh = round(float((huis.read("export_energy_active")) - 2.8359999656677246)*1000,4)
                omnik_export_kwh = round(float((omnik.read("export_energy_active")) - 22.288999557495117)*1000,4)
                sems_export_kwh = round(float((sems.read("export_energy_active")) - 0.041999999433755875)*1000,4)

                solar_export_kwh = (sems_export_kwh + omnik_export_kwh)
                solar_import_kwh = (sems_import_kwh + omnik_import_kwh)

                grid_export_kwh = round(  (
                                            (huis_import_kwh + omnik_import_kwh) + \
                                            (sems_export_kwh - huis_export_kwh)  \
                                        ) )

                
                db_import_kwh = grid_export_kwh + 17491730
                db_export_kwh = solar_export_kwh + 20278076
                
                print(f'db  import(WhUsage):{db_import_kwh} db  export(WhProduction):{db_export_kwh}')
                print(f'sol import         :{solar_import_kwh} sol export:{solar_export_kwh}')
                
                with InfluxDBClient(url="http://192.168.2.200:8086", token=token, org=org) as client:

                    write_api = client.write_api(write_options=SYNCHRONOUS)
                   
                    point = []

                    point.append( Point("mem") \
                        .measurement("energymeter") \
                        .tag("host", "Omnik") \
                        .tag("location", "Alkmaar") \
                        .field("export", float(omnik_export_kwh)) \
                        .field("import", float(omnik_import_kwh)) \
                        .field("watt", float(omnik_watt)) \
                        .field("volt", float(omnik.read('voltage'))) \
                        .field("current", float(omnik.read('current'))) \
                        .field("frequency", float(omnik.read('frequency'))) \
                        .field("power_factor", float(omnik.read('power_factor'))) )
                        # .time(Timestamp, WritePrecision.NS)

                    point.append(Point("mem") \
                        .measurement("energymeter") \
                        .tag("host", "Sems") \
                        .tag("location", "Alkmaar") \
                        .field("export", float(sems_export_kwh)) \
                        .field("import", float(sems_import_kwh)) \
                        .field("watt", float(sems_watt)) \
                        .field("volt", float(sems.read('voltage'))) \
                        .field("current", float(sems.read('current'))) \
                        .field("frequency", float(sems.read('frequency'))) \
                        .field("power_factor", float(sems.read('power_factor'))) )

                    point.append(Point("mem") \
                        .measurement("energymeter") \
                        .tag("host", "Home") \
                        .tag("location", "Alkmaar") \
                        .field("export", float(huis_export_kwh)) \
                        .field("import", float(huis_import_kwh)) \
                        .field("watt", float(usage_watt)) \
                        .field("volt", float(huis.read('voltage'))) \
                        .field("current", float(huis.read('current'))) \
                        .field("frequency", float(huis.read('frequency'))) \
                        .field("power_factor", float(huis.read('power_factor'))))

                    point.append(Point("mem") \
                        .measurement("energymeter") \
                        .tag("host", "Grid") \
                        .tag("location", "Alkmaar") \
                        .field("export", float(grid_export_kwh)) \
                        .field("import", float(db_import_kwh)) \
                        .field("watt", float(netto_watt)))
                       
                    point.append(Point("mem") \
                        .measurement("energymeter") \
                        .tag("host", "Solar") \
                        .tag("location", "Alkmaar") \
                        .field("export", float(db_export_kwh)) \
                        .field("import", float(solar_import_kwh)) \
                        .field("watt", float(solar_watt)))
                       
                    point.append(Point("mem") \
                        .measurement("Climate") \
                        .tag("host", "circulation") \
                        .tag("location", "Alkmaar") \
                        .field("temperature", float(clima.read('temperature_circulation',scaling=True))) \
                        .field("humidity", float(clima.read('humidity_circulation',scaling=True)))) 

                    point.append(Point("mem") \
                        .measurement("Climate") \
                        .tag("host", "outside") \
                        .tag("location", "Alkmaar") \
                        .field("temperature", float(clima.read('temperature_outside',scaling=True))) \
                        .field("humidity", float(clima.read('humidity_outside',scaling=True)))) 

                    point.append(Point("mem") \
                        .measurement("Climate") \
                        .tag("host", "intake") \
                        .tag("location", "Alkmaar") \
                        .field("temperature", float(clima.read('temperature_intake',scaling=True))) \
                        .field("humidity", float(clima.read('humidity_intake',scaling=True)))) 

                    point.append(Point("mem") \
                        .measurement("Climate") \
                        .tag("host", "extracted") \
                        .tag("location", "Alkmaar") \
                        .field("temperature", float(clima.read('temperature_extracted',scaling=True))) \
                        .field("humidity", float(clima.read('humidity_extracted',scaling=True)))) 
                       

                    for single_point in point:
                        write_api.write(bucket, org, single_point)
                
                mycursor = mydb.cursor()


                sql = "update LiveData set Solar=%s,Grid=%s,Gas=0,Heating=0 where ID=1"
                val = (solar_watt, huis_watt)
                mycursor.execute(sql, val)
                
                mydb.commit()
                
            except Exception as e:
                print('mislukt.')
                print (e)

            sleep(5)

        # for k, v in huis.read_all(src.sdm_modbus.registerType.INPUT).items():
        #     address, length, rtype, dtype, vtype, label, fmt, batch, sf = huis.registers[k]

        #     if type(fmt) is list or type(fmt) is dict:
        #         print(f"\t{label}: {fmt[str(v)]}")
        #     elif vtype is float:
        #         print(f"\t{label}: {v:.2f}{fmt}")
        #     else:
        #         print(f"\t{label}: {v}{fmt}")

        # # print("\nHolding Registers:")

        # for k, v in omnik.read_all(src.sdm_modbus.registerType.HOLDING).items():
        #     address, length, rtype, dtype, vtype, label, fmt, batch, sf = omnik.registers[k]

        #     if type(fmt) is list:
        #         print(f"\t{label}: {fmt[v]}")
        #     elif type(fmt) is dict:
        #         print(f"\t{label}: {fmt[str(v)]}")
        #     elif vtype is float:
        #         print(f"\t{label}: {v:.2f}{fmt}")
        #     else:
        #         print(f"\t{label}: {v}{fmt}")

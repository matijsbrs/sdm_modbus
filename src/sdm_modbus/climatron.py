from src.sdm_modbus import meter
from pymodbus.constants import Endian


class Climatron(meter.Meter):
    pass


class Clima(Climatron):

    def __init__(self, *args, **kwargs):
        self.model = "Climatron"
        self.wordorder = Endian.Little

        super().__init__(*args, **kwargs)

        self.registers = {
            "humidity_circulation": (40, 1, meter.registerType.HOLDING, meter.registerDataType.INT16, float, "Circulatie", "%", 1, 0.1),
            "humidity_extracted": (41, 1, meter.registerType.HOLDING, meter.registerDataType.INT16, float, "Extracted", "%", 1, 0.1),
            "humidity_outside": (42, 1, meter.registerType.HOLDING, meter.registerDataType.INT16, float, "Outside", "%", 1, 0.1),
            "humidity_intake": (43, 1, meter.registerType.HOLDING, meter.registerDataType.INT16, float, "Intake", "%", 1, 0.1),
            "temperature_circulation": (44, 1, meter.registerType.HOLDING, meter.registerDataType.INT16, float, "Circulatie", "C", 1, 0.1),
            "temperature_extracted": (45, 1, meter.registerType.HOLDING, meter.registerDataType.INT16, float, "Extracted", "C", 1, 0.1),
            "temperature_outside": (46, 1, meter.registerType.HOLDING, meter.registerDataType.INT16, float, "Outside", "C", 1, 0.1),
            "temperature_intake": (47, 1, meter.registerType.HOLDING, meter.registerDataType.INT16, float, "Intake", "C", 1, 0.1),
            
            "power_ac24": (65, 1, meter.registerType.HOLDING, meter.registerDataType.UINT16, int, "Relais 0", "s", 1, 1),
            "air_valve_1": (66, 1, meter.registerType.HOLDING, meter.registerDataType.UINT16, int, "Relais 1", "s", 1, 1),
            "air_valve_2": (67, 1, meter.registerType.HOLDING, meter.registerDataType.UINT16, int, "Relais 2", "s", 1, 1),
            "cv_value": (68, 1, meter.registerType.HOLDING, meter.registerDataType.UINT16, int, "Relais 3", "s", 1, 1),
            "highflow": (69, 1, meter.registerType.HOLDING, meter.registerDataType.UINT16, int, "Relais 4", "s", 1, 1),
            "ventilation": (70, 1, meter.registerType.HOLDING, meter.registerDataType.UINT16, int, "Relais 5", "s", 1, 1),
            "bypass": (71, 1, meter.registerType.HOLDING, meter.registerDataType.UINT16, int, "Bypass", "s", 1, 1),
            "freekoeling": (72, 1, meter.registerType.HOLDING, meter.registerDataType.UINT16, int, "Relais 7", "s", 1, 1)
            
            
            # "l3_current": (0x0010, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L3 Current", "A", 1, 0.001),
            # "l1_power_active": (0x0012, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L1 Power (Active)", "W", 1, 0.1),
            # "l2_power_active": (0x0014, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L2 Power (Active)", "W", 1, 0.1),
            # "l3_power_active": (0x0016, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L3 Power (Active)", "W", 1, 0.1),
            # "l1_energy_apparent": (0x0018, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L1 Energy (Apparent)", "VA", 1, 0.1),
            # "l2_energy_apparent": (0x001A, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L2 Energy (Apparent)", "VA", 1, 0.1),
            # "l3_energy_apparent": (0x001C, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L3 Energy (Apparent)", "VA", 1, 0.1),
            # "l1_energy_reactive": (0x001E, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L1 Energy (Reactive)", "VAr", 1, 0.1),
            # "l2_energy_reactive": (0x0020, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L2 Energy (Reactive)", "VAr", 1, 0.1),
            # "l3_energy_reactive": (0x0022, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L3 Energy (Reactive)", "VAr", 1, 0.1),
            # "voltage_ln": (0x0024, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L-N Voltage", "V", 2, 0.1),
            # "voltage_ll": (0x0026, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L-L Voltage", "V", 2, 0.1),
            # "power_active": (0x0028, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "Power (Active)", "W", 2, 0.1),
            # "power_apparent": (0x002A, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "Power (Apparent)", "VA", 2, 0.1),
            # "power_reactive": (0x002C, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "Power (Reactive)", "VAr", 2, 0.1),
            # "l1_power_factor": (0x002E, 1, meter.registerType.INPUT, meter.registerDataType.INT16, int, "L1 Power Factor", "", 2, 0.001),
            # "l2_power_factor": (0x002F, 1, meter.registerType.INPUT, meter.registerDataType.INT16, int, "L2 Power Factor", "", 2, 0.001),
            # "l3_power_factor": (0x0030, 1, meter.registerType.INPUT, meter.registerDataType.INT16, int, "L3 Power Factor", "", 2, 0.001),
            # "power_factor": (0x0031, 1, meter.registerType.INPUT, meter.registerDataType.INT16, int, "Power Factor", "", 2, 0.001),
            # "frequency": (0x0033, 1, meter.registerType.INPUT, meter.registerDataType.INT16, int, "Frequency", "Hz", 2, 0.1),
            # "import_energy_active": (0x0034, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "Imported Energy (Active)", "kWh", 2, 0.1),
            # "import_energy_reactive": (0x0036, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "Imported Energy (Reactive)", "kVArh", 2, 0.1),
            # "demand_power_active": (0x0038, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "Demand Power (Active)", "W", 2, 0.1),
            # "maximum_demand_power_active": (0x003A, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "Maximum Demand Power (Active)", "W", 2, 0.1),
            # "l1_import_energy_active": (0x0040, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L1 Imported Energy (Active)", "kWh", 2, 0.1),
            # "l2_import_energy_active": (0x0042, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L2 Imported Energy (Active)", "kWh", 2, 0.1),
            # "l3_import_energy_active": (0x0044, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "L3 Imported Energy (Active)", "kWh", 2, 0.1),
            # "export_energy_active": (0x004E, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "Exported Energy (Active)", "kWh", 2, 0.1),
            # "export_energy_reactive": (0x0050, 2, meter.registerType.INPUT, meter.registerDataType.INT32, int, "Exported Energy (Reactive)", "kVArh", 2, 0.1)
        }

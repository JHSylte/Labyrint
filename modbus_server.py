from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from threading import Thread

# === Dette er "store" du kan importere i main ===
store = ModbusSlaveContext(
    di = ModbusSequentialDataBlock(0, [0]*100),
    co = ModbusSequentialDataBlock(0, [0]*100),
    hr = ModbusSequentialDataBlock(0, [0]*100),
    ir = ModbusSequentialDataBlock(0, [0]*100)
)
context = ModbusServerContext(slaves=store, single=True)

identity = ModbusDeviceIdentification()
identity.VendorName = "RasberryPi"
identity.ProductCode = "RPIModbusSlave"
identity.VendorUrl = "https://rasberrypi.org"
identity.ProductName = "Modbus Slave"
identity.ModelName = "PiSlave1"
identity.MajorMinorRevision = "1.0"

def start_modbus_server():
    print("Starter Modbus TCP-server...")
    StartTcpServer(context=context, identity=identity, address=("0.0.0.0", 1502))

# Start server i bakgrunnen
Thread(target=start_modbus_server, daemon=True).start()

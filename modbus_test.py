from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from threading import Thread
import time


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

def update_counter():
    counter = 0
    while True:
        counter += 1
        store.setValues(3, 0, [counter])
        print(f"Tellerverdi: {counter}")
        time.sleep(1)

Thread(target=update_counter, daemon=True,).start()

print("Starter Modbus TCP-server på Rasberry Pi...")
StartTcpServer(context=context, identity=identity, address=("0.0.0.0", 1502))
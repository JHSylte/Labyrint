from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from threading import Thread
import time
import pygame

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

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Ingen joystick funnet!")
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    
    running = True
    while running:
        pygame.event.pump()  

        x_axis = joystick.get_axis(0)*-1
        y_axis = joystick.get_axis(1)*-1

        store.setValues(3, 1, x_axis)
        store.setValues(3, 2, y_axis)

        print(f"X: {x_axis:.2f}, Y: {y_axis:.2f}")

        pygame.time.wait(100)
pygame.quit()

print("Starter Modbus TCP-server på Rasberry Pi...")
StartTcpServer(context=context, identity=identity, address=("0.0.0.0", 1502))
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

def start_modbus_server():
    print("Starter Modbus TCP-server på Rasberry Pi...")
    StartTcpServer(context=context, identity=identity, address=("0.0.0.0", 1502))

def to_two_compliment(value):
    if value < 0:
       return 65535 + value
    return value

def pygame_loop():
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

            scale_factor = 100
            int_x_axis = int(x_axis *scale_factor)
            int_y_axis = int(y_axis *scale_factor)

            store.setValues(3, 1, [to_two_compliment(int_x_axis)])
            store.setValues(3, 2, [to_two_compliment(int_y_axis)])

            print(f"X: {x_axis:.2f}, Y: {y_axis:.2f}")

            pygame.time.wait(100)
    pygame.quit()

Thread(target=start_modbus_server, daemon=True).start()

Thread(target=pygame_loop, daemon=True).start()

while True:
    time.sleep
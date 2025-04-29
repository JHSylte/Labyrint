import pygame

def initialize_joystick():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("Ingen joystick funnet!")
        return None
    else:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(f"Joystick '{joystick.get_name()}' er klar.")
        return joystick

def read_joystick_axes(joystick):
    pygame.event.pump()
    x_axis = joystick.get_axis(0) * -1
    y_axis = joystick.get_axis(1) * -1
    return x_axis, y_axis
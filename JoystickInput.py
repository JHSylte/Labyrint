import pygame

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

        print(f"X: {x_axis:.2f}, Y: {y_axis:.2f}")

        pygame.time.wait(100)
pygame.quit()

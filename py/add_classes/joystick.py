import serial
import serial.tools.list_ports
import sys


class Joystick():

    def __init__(self, w, h) -> None:
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "Arduino Uno" in p.description:
                port = p.name
            else:
                print("No Arduino Uno connected")
                sys.exit()
        self.ser = serial.Serial(port, 9600)
        self.width = w
        self.heigth = h
        pass

    def update_position(self):
        data = self.ser.readline().decode().strip().split(',')
        if len(data) == 3:
            x_pos, y_pos, is_pressed = map(int, data)

            # Update coordinate system
            x_mapped = int((1023 - x_pos) / 1023 * self.width)
            y_mapped = int((y_pos / 1023) * self.heigth)  # Invert the Y-axis
            return x_mapped, y_mapped
        return self.update_position()

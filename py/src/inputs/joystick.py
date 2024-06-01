import serial
import serial.tools.list_ports
import sys
from helper.arduino_port_detection import find_arduino_port


class Joystick():

    def __init__(self, w, h) -> None:
        port = find_arduino_port()
        self.is_joystick_connected = True
        if (port == None):
            self.is_joystick_connected = False
        else:
            self.ser = serial.Serial(port, 9600)
        self.width = w
        self.heigth = h
        pass

    def update_position(self):
        temp_port = find_arduino_port()
        if (temp_port == None):
            self.is_joystick_connected = False
            return 0, 0
        else:
            if (self.is_joystick_connected == False):
                self.ser = serial.Serial(temp_port, 9600)
            self.is_joystick_connected = True
        data = self.ser.readline().decode().strip().split(',')
        if len(data) == 3:
            x_pos, y_pos, is_pressed = map(int, data)

            # Update coordinate system
            x_mapped = int((1023 - x_pos) / 1023 * self.width)
            y_mapped = int((y_pos / 1023) * self.heigth)  # Invert the Y-axis
            return x_mapped, y_mapped
        return self.update_position()

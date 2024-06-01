import serial.tools.list_ports
ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)
if "Arduino Uno" in p.description:
    print(p.name)

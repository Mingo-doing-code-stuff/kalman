import serial.tools.list_ports


def find_arduino_port():
    arduino_vendors = {
        # Arduino VID and common PIDs for Uno, Mega, Nano, etc.
        "2341": ["0043", "0001", "0243"],
        "0403": ["6001"],  # FTDI VID and common PID
        "1A86": ["7523"],  # CH340 VID and common PID
        "2A03": ["0043"],  # Another VID for Arduino
    }

    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        vid_pid = (p.vid, p.pid)
        # print(
            # f"Found port: {p.device} - VID: {p.vid:04X} PID: {p.pid:04X} - {p.description}")
        if p.vid and p.pid:
            vid_hex = f"{p.vid:04X}"
            pid_hex = f"{p.pid:04X}"
            if vid_hex in arduino_vendors and pid_hex in arduino_vendors[vid_hex]:
                print(f"Arduino found on port: {p.device}")
                # Return the device name (e.g., /dev/tty.usbserial-XXXXX)
                return p.device
    return None


arduino_port = find_arduino_port()
if arduino_port:
    print(f"Arduino is connected on port: {arduino_port}")
else:
    print("Arduino not found")

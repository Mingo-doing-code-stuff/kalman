#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>
#include <string.h>

#define BUFFER_SIZE 256
#define PORT "/dev/tty.usbmodem2201"

int main()
{
  /*
  Öffnen des Ports, das setzen weiterer Einstellungen:
  - O_RDWR   = Lese-/Schreibe Modus
  - O_NOCTTY = Keine Steuerung übernehmen
  - O_NDELAY = Nicht blockierender Modus
  */
  int serial_port = open(PORT, O_RDWR | O_NOCTTY | O_NDELAY);

  // Ensure Port was successfully opened
  if (serial_port < 0)
  {
    perror("Error opening serial port");
    return 1;
  }

  /*-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
  Initialisieren des Termios Structs, wird benötigt um
  See: https://man7.org/linux/man-pages/man3/termios.3.html
  -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=*/
  struct termios tty;
  memset(&tty, 0, sizeof tty);

  /*
  Getting current serial port settings...
  */
  if (tcgetattr(serial_port, &tty) != 0)
  {
    perror("Error getting tty attributes");
    close(serial_port);
    return 1;
  }

  /*
  Configuring serial port...
  */
  cfsetispeed(&tty, B9600);
  cfsetospeed(&tty, B9600);

  tty.c_cflag &= ~PARENB; // No parity bit
  tty.c_cflag &= ~CSTOPB; // One stop bit
  tty.c_cflag &= ~CSIZE;
  tty.c_cflag |= CS8; // 8 data bits

  tty.c_cflag &= ~CRTSCTS;       // Disable RTS/CTS hardware flow control
  tty.c_cflag |= CREAD | CLOCAL; // Enable receiver, ignore modem control lines

  tty.c_lflag &= ~ICANON;
  tty.c_lflag &= ~ECHO;
  tty.c_lflag &= ~ECHOE;
  tty.c_lflag &= ~ECHONL;
  tty.c_lflag &= ~ISIG;

  tty.c_iflag &= ~(IXON | IXOFF | IXANY);
  tty.c_iflag &= ~(IGNBRK | BRKINT | PARMRK | ISTRIP | INLCR | IGNCR | ICRNL);

  tty.c_oflag &= ~OPOST;
  tty.c_oflag &= ~ONLCR;

  tty.c_cc[VTIME] = 10; // Read timeout in deciseconds (1 second)
  tty.c_cc[VMIN] = 0;   // Minimum number of characters for non-canonical read

  /*
  Versuche die Schnitstelle zu starten.
  Falls ein Fehler auftreten sollte wird das Programm beendet
  */
  if (tcsetattr(serial_port, TCSANOW, &tty) != 0)
  {
    perror("Error setting tty attributes");
    close(serial_port);
    return 1;
  }

  char read_buffer[BUFFER_SIZE];
  char line_buffer[BUFFER_SIZE];
  int line_buf_pos = 0;

  printf("x ; y ; z\n");

  // while (1)
  for (int lim = 0; lim <= 100000;)
  {
    int read_buffer_size = sizeof(read_buffer) - 1;
    int num_bytes = read(serial_port, &read_buffer, read_buffer_size);

    if (num_bytes < 0)
    {
      perror("Error reading from serial port");
      break;
    }
    else if (num_bytes == 0)
    {
      continue;
    }

    // Null-terminate the string read
    read_buffer[num_bytes] = '\0';

    // Process the buffer
    for (int i = 0; i < num_bytes; i++)
    {
      if (read_buffer[i] == '\n')
      {
        // Null-terminate the line buffer and print the line
        line_buffer[line_buf_pos] = '\0';
        printf("%s\n", line_buffer);
        line_buf_pos = 0; // Reset the line buffer position
        lim++;
      }
      else
      {
        // Add character to line buffer
        if (line_buf_pos < BUFFER_SIZE - 1)
        {
          line_buffer[line_buf_pos++] = read_buffer[i];
        }
      }
    }
  }

  /*
  Closing serial port end end the programm..
  */
  close(serial_port);
  return 0;
}

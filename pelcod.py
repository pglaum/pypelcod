from serial import Serial
from typing import List
from time import sleep


class PelcoD():

    def __init__(self, port: str = '/dev/tty.usbserial-2',
                 baudrate: str = 9600):
        """Initialize the serial com.
        """

        self.serial = Serial(port, baudrate)

        self.camera_address = 0x01
        self.debug = False

    def set_camera_address(self, address: int):
        """Set the camera address (1-255).
        """

        self.camera_address = address

    def send_command(self, command: List[int]):
        """The command consists of: 2 bytes command, 2 bytes data.
        """

        if len(command) != 4:
            if self.debug:
                print('send_command: invalid length of command')
                print(command)

            return False

        full = [0xff, self.camera_address] + command
        checksum = sum(full[1:]) % 256
        full.append(checksum)
        full_bytes = bytes(full)

        if self.debug:
            print('send_command:', full_bytes)

        self.serial.write(full_bytes)

        return True

    def stop(self):
        """Stop all actions (panning, tilting, zooming, ...).
        """

        command = [0x00, 0x00, 0x00, 0x00]
        self.send_command(command)

    def pan_tilt(self, command, time=0.25):
        """Pan or tilt for a certain amount of time.
        """

        # speed is not used by the tenveo camera
        commands = {
            'right': [0x00, 0x02, 0x20, 0x00],
            'left':  [0x00, 0x04, 0x20, 0x00],
            'up':    [0x00, 0x08, 0x00, 0x20],
            'down':  [0x00, 0x10, 0x00, 0x20],
        }

        if command not in commands:
            return

        self.send_command(commands[command])

        if time > 0:
            sleep(time)
            self.stop()

    def up(self, time=0.25):
        """Tilt up for a certain amount of time.
        """

        self.pan_tilt('up', time)

    def down(self, time=0.25):
        """Tilt down for a certain amount of time.
        """

        self.pan_tilt('down', time)

    def left(self, time=0.25):
        """Pan left for a certain amount of time.
        """

        self.pan_tilt('left', time)

    def right(self, time=0.25):
        """Pan right for a certain amount of time.
        """

        self.pan_tilt('right', time)

    def zoom_in(self, time=0.25):
        """Zoom in for a certain amount of time.
        """

        command = [0x00, 0x20, 0x00, 0x00]
        self.send_command(command)

        if time:
            sleep(time)
            self.stop()

    def zoom_out(self, time=0.25):
        """Zoom out for a certain amount of time.
        """

        command = [0x00, 0x40, 0x00, 0x00]
        self.send_command(command)

        if time:
            sleep(time)
            self.stop()

    def set_preset(self, preset_id):
        """Save the current position to a preset.
        """

        preset_id = self.clamp(preset_id, 0x00, 0x7f)
        command = [0x00, 0x03, 0x00, preset_id]
        self.send_command(command)

    def clear_preset(self, preset_id):
        """Clear a preset.
        """

        preset_id = self.clamp(preset_id, 0x00, 0x7f)
        command = [0x00, 0x05, 0x00, preset_id]
        self.send_command(command)

    def goto_preset(self, preset_id):
        """Go to a preset.
        """

        preset_id = self.clamp(preset_id, 0x00, 0x7f)
        command = [0x00, 0x07, 0x00, preset_id]
        self.send_command(command)

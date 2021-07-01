from serial import Serial
from typing import List
from time import sleep


class PelcoD():

    def __init__(self, port: str = '/dev/tty.usbserial-2',
                 baudrate: str = 9600):

        self.serial = Serial(port, baudrate)

        self.camera_address = 0x01
        self.debug = True

    def set_camera_address(self, address: int):

        self.camera_address = address

    def send_command(self, command: List[int]):
        """The command consists of: 2 bytes command, 2 bytes data.
        """

        if len(command) != 4:
            if self.debug:
                print('invalid length of command:')
                print(command)

            return False

        full = [0xff, self.camera_address] + command
        checksum = sum(full[1:]) % 256
        full.append(checksum)
        full_bytes = bytes(full)

        if self.debug:
            print(full_bytes)

        self.serial.write(full_bytes)

        return True

    def clamp(self, value, minv, maxv):
        if value < minv:
            return minv
        if value > maxv:
            return maxv
        return value

    #
    # stop all actions
    #
    def stop(self):

        command = [0x00, 0x00, 0x00, 0x00]
        self.send_command(command)

    #
    # pan & tilt
    #
    def pan_tilt(self, command, time=0.25):

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
        self.pan_tilt('up', time)

    def down(self, time=0.25):
        self.pan_tilt('down', time)

    def left(self, time=0.25):
        self.pan_tilt('left', time)

    def right(self, time=0.25):
        self.pan_tilt('right', time)

    #
    # zoom & focus
    #
    def zoom_in(self, time=0.25):

        command = [0x00, 0x20, 0x00, 0x00]
        self.send_command(command)

        if time:
            sleep(time)
            self.stop()

    def zoom_out(self, time=0.25):

        command = [0x00, 0x40, 0x00, 0x00]
        self.send_command(command)

        if time:
            sleep(time)
            self.stop()

    #
    # presets
    #
    def set_preset(self, preset_id):

        preset_id = self.clamp(preset_id, 0x00, 0x7f)
        command = [0x00, 0x03, 0x00, preset_id]
        self.send_command(command)

    def clear_preset(self, preset_id):

        preset_id = self.clamp(preset_id, 0x00, 0x7f)
        command = [0x00, 0x05, 0x00, preset_id]
        self.send_command(command)

    def goto_preset(self, preset_id):

        preset_id = self.clamp(preset_id, 0x00, 0x7f)
        command = [0x00, 0x07, 0x00, preset_id]
        self.send_command(command)

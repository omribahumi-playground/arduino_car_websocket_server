#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from serial import Serial

def arr_has_items(arr, items):
    """
    Checks if every item in "items" is inside "arr"
    """
    return set(items).issubset(set(arr))


class CarDispatcher:
    """
    This class dispatches commands to the car serial interface.
    """

    LEFT_REAR_FORWARD = 1
    LEFT_REAR_BACKWARD = 2
    LEFT_FRONT_FORWARD = 4
    LEFT_FRONT_BACKWARD = 8
    RIGHT_FRONT_FORWARD = 16
    RIGHT_FRONT_BACKWARD = 32
    RIGHT_REAR_FORWARD = 64
    RIGHT_REAR_BACKWARD = 128
    
    LEFT_WHEELS_FORWARD = LEFT_REAR_FORWARD|LEFT_FRONT_FORWARD
    LEFT_WHEELS_BACKWARD = LEFT_REAR_BACKWARD|LEFT_FRONT_BACKWARD
    RIGHT_WHEELS_FORWARD = RIGHT_REAR_FORWARD|RIGHT_FRONT_FORWARD
    RIGHT_WHEELS_BACKWARD = RIGHT_REAR_BACKWARD|RIGHT_FRONT_BACKWARD

    ALL_WHEELS_FORWARD = LEFT_WHEELS_FORWARD|RIGHT_WHEELS_FORWARD
    ALL_WHEELS_BACKWARD = LEFT_WHEELS_BACKWARD|RIGHT_WHEELS_BACKWARD

    _instance = None

    def __init__(self, serialPort='/dev/ttyUSB0', baudRate=9600):
        self.serialPort = serialPort
        self.baudRate = baudRate
        self.serialInterface = Serial(self.serialPort, self.baudRate)
        self.serialInterface.open()

    @classmethod
    def init(cls, *args, **kwargs):
        cls._instance = cls(*args, **kwargs)
    
    @classmethod
    def instance(cls):
        return cls._instance

    def _write(self, data):
        """
        Send raw data on the serial interface
        """
        print repr(data)
        self.serialInterface.write(data)

    def sendCommand(self, wheels, left_rear_speed, left_front_speed, right_front_speed, right_rear_speed):
        """
        Change the direction of the wheels in the car and set the wheel speed
        wheels is a bitwise or of LEFT_* and RIGHT_* constants.
        *_speed variables can contain values between 0 and 3 to control the wheel speed.
        Note that 0 speed is still spinning. For the wheel not to spin you shouldn't include it in the wheels bit field.
        """
        speed = 0
        speed |= (left_rear_speed & 0x3)
        speed |= (left_front_speed & 0x3) << 2
        speed |= (right_front_speed & 0x3) << 4
        speed |= (right_rear_speed & 0x3) << 6
        
        self._write(chr(wheels & 0xff) + chr(speed))

    def dispatch(self, direction, speed=3):
        print "command=%r, speed=%r" % (direction, speed)

        if arr_has_items(direction, ('forward', 'left')):
            print 'forward+left'
            self.sendCommand(CarDispatcher.RIGHT_WHEELS_FORWARD, 0, 0, 3, 3)
        elif arr_has_items(direction, ('forward', 'right')):
            print 'forward+right'
            self.sendCommand(CarDispatcher.LEFT_WHEELS_FORWARD, 3, 3, 0, 0)
        elif arr_has_items(direction, ('reverse', 'left')):
            print 'reverse+left'
            self.sendCommand(CarDispatcher.RIGHT_WHEELS_BACKWARD, 0, 0, 3, 3)
        elif arr_has_items(direction, ('reverse', 'right')):
            print 'reverse+right'
            self.sendCommand(CarDispatcher.LEFT_WHEELS_BACKWARD, 3, 3, 0, 0)
        elif 'forward' in direction:
            print 'forward'
            self.sendCommand(CarDispatcher.ALL_WHEELS_FORWARD, speed, speed, speed, speed)
        elif 'reverse' in direction:
            print 'reverse'
            self.sendCommand(CarDispatcher.ALL_WHEELS_BACKWARD, speed, speed, speed, speed)
        elif 'left' in direction:
            print 'left'
            self.sendCommand(CarDispatcher.RIGHT_WHEELS_FORWARD|CarDispatcher.LEFT_WHEELS_BACKWARD, speed, speed, speed, speed)
        elif 'right' in direction:
            print 'right'
            self.sendCommand(CarDispatcher.LEFT_WHEELS_FORWARD|CarDispatcher.RIGHT_WHEELS_BACKWARD, speed, speed, speed, speed)
        else:
            print 'release'
            self.sendCommand(0, 0, 0, 0, 0)

__all__ = ['CarDispatcher']

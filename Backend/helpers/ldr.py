import spidev
import time
import threading


class ldr:

    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 10**5

    def readldr(self,channel):
        # if read_spi > 7 or read_spi < 0:
        #     return -1
        spidata = self.spi.xfer2([1, (8 | channel) << 4, 0])
        data = ((spidata[1] & 3) << 8) | spidata[2]
        print(data)
        return data



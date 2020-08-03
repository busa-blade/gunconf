import usb.core
import usb.util
import logging
from .conversion import *
import gunconf
import time
import binascii


class Aimtrak(object):
    """ driver for aimtrak gun """

    vendorId = 0xd209

    def __init__(self, pBus=None, pAddress=None):
        """ build instance """
        self._l = logging.getLogger('gunconf.drivers.Aimtrak')

        args = {'idVendor': self.vendorId}
        if pBus:
            args['bus'] = pBus
        if pAddress:
            args['address'] = pAddress

        self._dev = None
        try:
            self._dev = usb.core.find(**args)
        except:
            pass

        if not self._dev:
            self._l.critical("no device found")
            raise ValueError('Device not found')

        self._l.debug("trying to connect to %s", self._dev)

        # get interface
        cnf = self._dev.get_active_configuration()
        self._intf = cnf.interfaces()[0] # get interface 0
        if self._dev.is_kernel_driver_active(0):
            try:
            # Detach kernel drivers and claim through libusb
                self._dev.detach_kernel_driver(0)
                print("Kernel driver detached")
            except usb.core.USBError as e:
                sys.exit("Could not detach kernel driver: %s" % str(e))
        else:
            print ("No kernel driver attached")
        try:
            usb.util.claim_interface(self._dev, 0)
            print ("claimed device")
        except:
            sys.exit("Could not claim the device: %s" % str(e))

        # flush interrupt IN pipe
        self._getReport(timeout=500)


    def _setReport(self, pReport):
        """ set a report on the device """
        bytessent = self._dev.ctrl_transfer(bmRequestType = 0x21, # Set_Report Request
                                bRequest      = 0x09, # SET_REPORT
                                wValue        = 0x200, # report type = output, report ID = 0
                                wIndex        = 0, # interface 0
                                data_or_wLength = pReport)
        print(f"Sent {bytessent} over interface")


    def _getReport(self, length=-1, timeout=None):
        if length == -1:
            readlength = 256
        else:
            readlength = length
        bytesatatime = 4
        """ read from the device """
        print (f"Length to read is {length} and timeout is {timeout}")
        ret = []
        ep = self._intf.endpoints()[0] # interrupt IN endpoint (there is only one)
        try:
            while len(ret) < readlength:
                # it seems that a timeout of 100msecs is ok
                ret += self._dev.read(ep, bytesatatime, timeout=timeout)
                print ("Read %d bytes from interface" % len(ret))
            print (f"Bytes: {ret}")
        except usb.USBError as e:
            if e.errno == 110: #timeout (can't find a const in pyusb for it...)
                self._l.info("operation timeout")
                print(str(e))
            else:
                self._l.error("can't get report \"%s\"", e)

        return ret


    def _getConfig(self):
        self._setReport([0x5A, 0xEE, 0x00, 0x00])
        return self._getReport(length=40)


    def getConfig(self):
        """ get config """
        cnf = config_from_buffer(self._getConfig())
        # add idVendor
        cnf['idProduct'] = self._dev.idProduct
        return cnf


    def setConfig(self, cnf):
        """ set config """
        buf = self._getConfig()
        print (f"Gun configuration is {buf}")

        # modify it
        buf = config_to_buffer(cnf, buf)
        buf[0] = 0x50 # set report type

        # set modification
        for i in range(0,len(buf),4):
            self._setReport(buf[i:i+4])

        if cnf['idProduct'] != self._dev.idProduct:
            id = cnf['idProduct'] - 0x1600
            if 1<= id <= 8:
                self._l.info("change devID to 0x%x (old was 0x%x)",
                             cnf['idProduct'], self._dev.idProduct)
                self._setReport([0x50+id, 0xEE, 0x00, 0x00])
                # device shall be disconnected
                return True

        return False


    def recoil(self):
        self._setReport([0x5C, 0xEE, 0x00, 0x00])
        # we lose the gun if we don't sleep here
        time.sleep(0.5)


    def getDynData(self):
        """ get dynamic data """
        self._setReport([0x59, 0xEE, 0x00, 0x00])
        ret = self._getReport(length=32)

        return dyn_data_from_buffer(ret)


    def close(self):
        if self._dev:
            try:
                usb.util.release_interface(self._dev, 0)
                self._dev.attach_kernel_driver(0)
            except usb.USBError as e:
                self._l.error("can't close device \"%s\"", e)


# find our device
# we need interface number 0 (from lsusb)
#lsusb -d d209: -vvv

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)

    gun = Aimtrak()
    cnf = gun.getConfig()

    print (f"configuration is {cnf}")

    #cnf['joystick'] = False

    #tstCfg = {'irGain'      : 1,
    #          'autoGain'    : False,
    #          'calDelay'    : 5,
    #          'recoil'      : 100,
    #          'joystick'    : False,
    #          'tilt'        : 'continuous',
    #          'offActTrig'  : 'left',
    #          'onActTrig'   : 'left',
    #          'offActLeft'  : 'middle',
    #          'onActLeft'   : 'middle',
    #          'offActRight' : 'right',
    #          'onActRight'  : 'right',
    #          'onCalTrig'   : False,
    #          'offCalTrig'  : False,
    #          'onCalLeft'   : True,
    #          'offCalLeft'  : True,
    #          'onCalRight'  : True,
    #          'offCalRight' : True,
    #          'idProduct'   : 0x1601}

    #cnf.update(tstCfg)

    disconnect = gun.setConfig(cnf)
    #import IPython; IPython.embed() # XXX BREAKPOINT


    if disconnect:
        gun.close()
        time.sleep(5)

        print ("sleep 5 seconds to let device reboot")
        gun = Aimtrak()
        gun.getConfig()

    try:
        while True:
            print (gun.getDynData())
    except KeyboardInterrupt:
        gun.close()

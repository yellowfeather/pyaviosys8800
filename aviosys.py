# Copyright (C) 2014 Chris Richards
#
# The following terms apply to all files associated
# with the software unless explicitly disclaimed in individual files.
#
# The authors hereby grant permission to use, copy, modify, distribute,
# and license this software and its documentation for any purpose, provided
# that existing copyright notices are retained in all copies and that this
# notice is included verbatim in any distributions. No written agreement,
# license, or royalty fee is required for any of the authorized uses.
# Modifications to this software may be copyrighted by their authors
# and need not follow the licensing terms described here, provided that
# the new terms are clearly indicated on the first page of each file where
# they apply.
#
# IN NO EVENT SHALL THE AUTHORS OR DISTRIBUTORS BE LIABLE TO ANY PARTY
# FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
# ARISING OUT OF THE USE OF THIS SOFTWARE, ITS DOCUMENTATION, OR ANY
# DERIVATIVES THEREOF, EVEN IF THE AUTHORS HAVE BEEN ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# THE AUTHORS AND DISTRIBUTORS SPECIFICALLY DISCLAIM ANY WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.  THIS SOFTWARE
# IS PROVIDED ON AN "AS IS" BASIS, AND THE AUTHORS AND DISTRIBUTORS HAVE
# NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
# MODIFICATIONS.



import usb
import usb.legacy


class Aviosys8800(object):
  def __init__(self):
    self.handle = None
    self.dev = None

  def open(self):
    # Find my device - idVendor = 0x067b idProduct = 0x2303
    newDev = usb.core.find(idVendor=0x067b, idProduct=0x2303)
    if newDev is None:
      raise ValueError('USB switch not found')

    newDev.set_configuration()
    # newDev.detach_kernel_driver(0)
    self.dev = usb.legacy.Device(newDev)
    self.handle = self.dev.open()
    # handle.detachKernelDriver(0)
    self.handle.claimInterface(0)

  def close(self):
    self.USB1(0x21,34,2,0,0)
    self.USB1(0x21,34,0,0,0)
    self.handle.releaseInterface()

  def init(self):
    self.USB2(0x40,1,1028.0)
    self.USB2(0x40,1,1028,1)
    self.USB2(0x40,1,1028,32)
    self.USB2(0x40,1,1028,33)
    self.USB2(0x40,1,1028,64)
    self.USB2(0x40,1,1028,65)
    self.USB2(0x40,1,1028,96)
    self.USB2(0x40,1,1028,97)
    self.USB2(0x40,1,1028,128)
    self.USB2(0x40,1,1028,129)
    self.USB2(0x40,1,1028,160)
    self.USB2(0x40,1,1028,161)
    self.USB1(0x40,1,0,1)
    self.USB1(0x40,1,1,0)
    self.USB1(0x40,1,2,68)
    #800
    self.USB1(0,1,1,0,0)
    self.USB1(0x21,32,0,0,7)
    self.USB1(0xc0,1,128,0,2)
    self.USB1(0xc0,1,129,0,2)
    #804
    self.USB1(0x40,1,1,0)
    self.USB1(0x40,1,0,1)
    self.USB1(0x21,34,1,0,0)
    #807
    self.USB1(0xc0,1,128,0,2)
    self.USB1(0xc0,1,129,0,2)
    self.USB1(0x40,1,1,0,0)
    #810
    self.USB1(0x40,1,0,1,0)
    self.USB1(0x21,34,3,0,0)
    self.USB1(0xc0,1,128,0,2)
    self.USB1(0x40,1,0,1,0)
    self.USB1(0xc0,1,128,0,2)
    #815
    self.USB1(0x40,1,0,1,0)
    self.USB1(0x21,32,0,0,7)
    self.USB1(0x40,1,2827,2,0)
    #818
    self.USB1(0x40,1,2313,0,0)
    self.USB1(0x40,1,2056,0,0)
    #820
    self.USB1(0xc0,1,129,0,2)
    self.USB1(0x40,1,1,32)
    self.USB1(0xc0,1,36237,0,4)

  def getStatus(self):
    status = self.USB1(0xc0,1,129,0,2)
    if status[0] == 0x20:
      return False
    if status[0] == 0xA0:
      return True
    raise ValueError('Unrecognised status')

  def turnOn(self):
    self.USB1(0x40,1,1,160)

  def turnOff(self):
    self.USB1(0x40,1,1,32)


  def USB1 (self, utype=0xC0, ureq=1, uvalue=0, uindex=1028, ubytes=0):
    if ubytes != 7:
      status=self.handle.controlMsg(int(utype), int(ureq), int(ubytes),  int(uvalue),int( uindex))
    else:
      ubuffer = 0xB0,0x4,0x0,0x0,0x2,0x7
      status=self.handle.controlMsg(int(utype), int(ureq), ubuffer,  int(uvalue), int(uindex))
    return status

  def USB2 (self, vtype, vreq=1, vvalue=1028, vindex=0, vbytes=0):
    self.USB1(0xc0,1,33924,0,1)
    self.USB1(vtype,vreq,vvalue,vindex,vbytes)
    self.USB1(0xc0,1,33924,0,1)
    self.USB1(0xc0,1,33667,0,1)
    return

#! /usr/bin/python3

import mmap
import time, struct
import sys


class RegBlock:
    def __init__(self, baseAddress, size):
        self.baseAddress = baseAddress
        self.size = size
        #print(baseAddress)
        with open("/dev/mem", "r+b" ) as f:
            self.mem = mmap.mmap(f.fileno(), size, 
                       offset = baseAddress)
    def close(self):
        self.mem.close()
        
    def set_u32(self, address, val):
        address = address * 4
        self.mem[address:address+4] = struct.pack("<L", val & 0xffffffff)

    def get_u32(self, address):
        address = address * 4
        return struct.unpack("L", self.mem[address:address+4])[0]
        
   

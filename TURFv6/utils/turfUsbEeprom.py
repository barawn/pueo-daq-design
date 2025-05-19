from electronics.devices import EEPROM

# 1. checkout https://github.com/barawn/pyElectronics
# make sure your PYTHONPATH points there. you might
# need smbus2.
#
# 2. from turfUsbEeprom import program
#
# 3. get a gateway somehow - e.g. with a Bus Pirate, do
#
# from electronics.gateways import BusPirate
# gw = BusPirate(com port)
#
# 4. program(gw, #)
# where # is the TURF serial number intended (as an int)
#
# n.b. if the programming fails just try it again
#
def getEeprom(ser):
    eeprom = bytearray(256)
    # vid
    eeprom[0:2] = b'\x24\x04'
    # pid
    eeprom[2:4] = b'\x14\x25'
    # device
    eeprom[4:6] = b'\x00\x00'
    # config byte 1
    eeprom[6] = 0x9B    
    # config byte 2
    eeprom[7] = 0x20    
    # config byte 3
    eeprom[8] = 0x01    
    # nr_device
    eeprom[9] = 0x00    
    # port_dis_sp - disable port 4
    eeprom[10] = 0x10    
    # port_dis_bp - disable port 4
    eeprom[11] = 0x10    
    # max_pwr_sp
    eeprom[12] = 0x01    
    # max_pwr_bp
    eeprom[13] = 0x32    
    # hc_max_c_sp
    eeprom[14] = 0x01    
    # hc_max_c_bp
    eeprom[15] = 0x32    
    # power_on_time
    eeprom[16] = 0x32    
    # lang_id_h
    eeprom[17] = 0x00    
    # lang_id_l
    eeprom[18] = 0x00
    mfr_str = "Ohio State University"
    prod_str = "Trigger Unit for RF [TURF]"
    # mfr_str_len (21)
    eeprom[19] = len(mfr_str)
    # prd_str_len (26)
    eeprom[20] = len(prod_str)
    # ser_str_len (1)
    eeprom[21] = len(ser)
    # mfr string
    mfr = mfr_str.encode('utf-16le')
    eeprom[22:22+len(mfr)] = mfr
    
    # prod string
    prod = prod_str.encode('utf-16le')
    eeprom[84:84+len(prod)] = prod
    
    # ser string
    serial = ser.encode('utf-16le')
    eeprom[146:146+len(serial)] = serial
    # bc_en
    eeprom[208] = 0x00
    # boost_up
    eeprom[246] = 0x00
    # boost_4
    eeprom[248] = 0x00
    # PRTSP
    eeprom[250] = 0x04

    return eeprom

def program(gw, serno):
    dev = EEPROM(gw)
    eepromValues = getEeprom(str(serno))
    # write
    dev.write(0, eepromValues)
    # verify
    for i in range(16):
        r = dev.read(i*16, 16)
        v = eepromValues[16*i:16*(i+1)]
        if r != v:
            print(f'mismatch at addr {hex(i*16)}')
            print(f'readback: {r}')
            print(f'desired: {v}')
            

#===============================================================================
# Philippa Richardson and Emily Syme
# 05 August 2017
# COSC 264 - Introduction to Networking and the Internet
# Packet
#===============================================================================

#===========================================
#Imports
#===========================================

import struct

#===========================================

class packet_head():
    """
     Packet head:
     magic_no   #the magic number of 0x497E
     
     pack_type  #distinguishes two packet types: data_packet & acknowledgement_packet
                #'type' on its own is a python thing already, or this would be 'type'
                    #data_packet = 0
                    #acknowledgement_packet = 1
     
     seq_no     #restricted to the values 0 and 1
     
     data_len   #number of user bytes carried in this packet
                #data_len_max #512
                #data_len_min #0
                #if data_len is 0 and pack_type is data_packet:
                    #data_packet is empty
                    #End of file transmitted to receiver
                #if data_len is not 0 and pack_type is acknowledgement_packet:
                    #Drop packet
     
     Content:
     data         #contains actual data, variable length indicated by data_len
     
     Other:
         Protocol mechanism to detect and handle bit errors
         #Not allowed to use a boolean flag; IRL channels don't tell user about bit errors
     
     
     Also:
     ##A MYSTERY FIELD##
     which we have labelled pack_format because that's probably what it is, it's a string, it's declaring that it's making a string
    """
    
    data_packet = 0
    acknowledgement_packet = 1
    
    #DATA_LEN_MAX = 512
    #DATA_LEN_MIN = 0
    ##Max and min for data_len to avoid having more magic numbers    
    
    
    def __init__(self, magic_no, pack_type, seq_no, data_len):
        """"""
        self.magic_no = magic_no
        self.pack_type = pack_type
        self.seq_no = seq_no
        self.data_len = data_len
        self.pack_format = "iiii"
        
    def encoder(self):
        """I mean I think"""
        encode = struct.pack(self.pack_format, self.magic_no, self.pack_type, self.seq_no, self.data_len)
        return encode
        
    def decoder(encode):
        """I mean I think"""
        pack_format = "iiii"
        decode = struct.unpack(pack_format, encode)
        return decode
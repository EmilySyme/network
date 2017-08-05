"""
 Philippa Richardson and Emily Syme
 05 August 2017
 COSC 264 - Introduction to Networking and the Internet
 Packet
     """

class packet_head():
    """
     Packet head:
     magic_no   #the magic number of 0x497E
     
     pack_type  #distinguishes two packet types: data_packet & acknowledgement_packet
                #'type' on its own is a python thing already, or this would be 'type'
     
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
     
     ##MYSTERY FIELD##
    """
    
    data_packet = 0
    acknowledgement_packet = 1
    
    
    def __init___(self, magic_no, pack_type, seq_no, data_len):
        self.magic_no = magicno
        self.pack_type = pack_type
        self.seq_no = seq_no
        self.data_len = data_len
        #self.mystery_field = a mystery
        
#===============================================================================
# Philippa Richardson and Emily Syme
# 05 August 2017
# COSC 264 - Introduction to Networking and the Internet
# Sender
#===============================================================================

import packet
#is the packet class we made earlier

import select
#Is the equivalent of C's select()

import socket
#I mean we'll probably need it

"""
    Other:
        Protocol mechanism to detect and handle bit errors
            #Not allowed to use a boolean flag;
            #IRL channels don't tell user about bit errors

Takes following parameters from command line:
    #sender_in port_num
        #range(1024-64,001)
    #sender_out port_num
        #range(1024-64,001)
    #c_sender_in port_num
        #sender sends to channel through sender_out to c_sender_in
    #file name for file being sent
    
    Checks parameters
    Creates/Binds both sockets
    ##Use connect() equivalent on sender_out, set default recever to c_sender_in port_num
    Check that correct file exists
        #exit sender if file does not exist
        
    Initialise local int variable next to 0 (next = 0)
    Initialise local boolean flag exit_flag to false (exit_flag = false)
    Initialise counter value, how many total packets sent over ender_out socket
        #print when program finished
    
    If sucessful, enter loop:
    
    Outer loop:
    Attempt to read max 512 bytes (n) from open file to local buffer
    Place prepared packet into separate buffer (packet_buffer)
        #if n == 0, data_packet = 
            #magic_no = 0x497E
            #type = data_packet
            #seq_no = next
            #data_len = 0
            #data = NULL (assignment states 'and an empty data field')
          exit_flag = True
        if n > 0:
            #magic_no = 0x497E
            #type = data_packet
            #seq_no = next
            #data_len = n
            #append n bytes of data
    
    Inner loop:
    Send packet in packet_buffer to channel via sender_out
    Wait for response packet on socket_in before timeout (1 second)
        #we can apparently use an equivalent of C's select() value for this
    -If no response packet (denoted as rcvd) before timeout:
        #restart _inner_ loop (retransmit content of packet_buffer)
    -else:
        #if ((rcvd.magic_no != 0x497E) or
            (rcvd.pack_type != acknowledgement_packet) or 
            (rcvd.data_len != 0)) or (rcvd.seq_no != next):
              #restart _inner_ loop (retransmit content of packet_buffer)
        #else:
            #next -= 1
            #if exit_flag == True:
                #close file
                #exit sender
            #else:
                #restart _outer_ loop
        
    Close program using equivalent of close() on open sockets or files
"""

MAGIC_NO = 0x497E
#The magic number

PORT_RANGE = range(1024,64001)
#The range of valid ports, from 1024 to 64,000

IP_ADDRESS = 127.0.0.1
#So the command line doesn't request an IP address all the time
#This is the Loopback address

DATA_LEN_MAX = 512
DATA_LEN_MIN = 0
#Max and min for data_len to avoid having more magic numbers
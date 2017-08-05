#===============================================================================
# Philippa Richardson and Emily Syme
# 05 August 2017
# COSC 264 - Introduction to Networking and the Internet
# Receiver
#===============================================================================

import packet
#is the packet class we made earlier

import socket
#I mean we'll probably need it


"""
    Other:
        Protocol mechanism to detect and handle bit errors
            #Not allowed to use a boolean flag;
            #IRL channels don't tell user about bit errors


Takes following parameters from command line:
    #receiver_in port_num
        #range(1024-64,001)
    #receiver_out port_num
        #range(1024-64,001)
    #c_receiver_in port_num
        #receiver sends to channel through receiver_out to c_receiver_in
    #file name for received file to be stored
    
    Checks ports
    Creates/Binds sockets
    ##Meant to use something like c's connect() here???
    Set default receiver to port_num used by channel's c_receiver_in socket
    Opens file with supplied filename for writing
        #aborts receiver when file already exists
    Initialises local int
        #expected = 0
    Enters blocking system call loop
    
    Waits on receiver_in for incoming packet
        #uses blocking call
    Checks magic_no
        #if magic_no != 0x497E, stop processing; restart loop
    Checks packet_type
        #if packet_type != data_packet (i.e. packet_type != 0), stop processing; restart loop
        
    If seq_no != expected (rcvd.seq_no, apparently???)
        #send acknowledgement_packet via received_out:
           magic_no = 0c497E
           type = acknowledgement_packet
           seq_no = rcvd.seq_no
           data_len = 0
        #stop processing; restart loop
        
    If seq_no == expected (rcvd.seq_no, apparently???)
        #send acknowledgement_packet via received_out:
           magic_no = 0c497E
           type = acknowledgement_packet
           seq_no = rcvd.seq_no
           data_len = 0
        #expected -= 1
        
    If received packet contains actual data (if rcvd.data_len > 0)
        #append data to output file
        #stop processing; restart loop
    
    If rececived packet contains no data (if rcvd.data_len == 0)
        #close output file
        #close all sockets
        #exit program
        
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
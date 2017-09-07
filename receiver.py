#===============================================================================
# Philippa Richardson and Emily Syme
# 05 August 2017
# COSC 264 - Introduction to Networking and the Internet
# Receiver
#===============================================================================

#import packet
##is the packet class we made earlier

#import socket
##I mean we'll probably need it

import commons



def cmd_input():
    """Import information from the command line"""
    command_input = sys.stdin
    return command_input

def param_check(port_receiver_in, port_receiver_out, port_c_receiver_in):
    """
    #receiver_in port_num
        #range(1024-64,001)
    #receiver_out port_num
        #range(1024-64,001)
    #c_receiver_in port_num
        #receiver sends to channel through receiver_out to c_receiver_in
    
    Creates/Binds Sockets
    Uses connect() on receiver_out to set c_receiver_in default receiver for port number for channel.py
        """
    if ( (commons.port_num(port_receiver_in)) and
         (commons.port_num(port_receiver_out)) and
         (commons.port_num(port_c_receiver_in))):
        return True
    
def create_bind_connect():
        #create:
        socket_receiver_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_receiver_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_c_receiver_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        #bind:
        socket_receiver_in.bind(IP_ADDRESS, port_receiver_in)
        socket_receiver_out.bind(IP_ADDRESS, port_receiver_out)
        
        #connect:
        socket_receiver_out.connect(IP_ADDRESS, port_c_receiver_in) 
        
        
def write_file(filename):
    """Opens file with supplied filename for writing
        #aborts receiver when file already exists"""
    #OH GODS how do I write things to file?! *crying*
    
def acknowledged(seq_no):
    """"""
    acknowledge_packet = packet.packet_head(MAGIC_NO, ACKNOWLEDGEMENT_PACKET, seq_no, 0)
    head = acknowledge_packet.encoder()
    packet_buffer = bytearray(head)
    socket_receiver_out.send(packet_buffer)
    
def call_loop(write_file, expected):
    #Enters blocking system call loop
    #Waits on receiver_in for incoming packet
        ##uses blocking call
    #subprocess.check_call() goes here somehow
    #rcvd_packet = #receive the packet here
    rcvd_magic_no, rcvd_type, rcvd_seq_no, rcvd_data_len = packet.decoder(rcvd_packet)
    if ( (magic_no != MAGIC_NO) or
        (packet_type != DATA_PACKET) ):
        call_loop(magic_no, write_file, received)
    else:
        acknowledged(rcvd_seq_no)
        if (rcvd_seq_no != expected):
            call_loop(write_file, expected)
        else:
            expected = 1 - expected
            if (rcvd_data_len > 0):
                #append data to write_file somehow
                call_loop(write_file, expected)
            else:
                #close all the things
                socket_receiver_in.close()
                socket_receiver_out.close()
                #close the data_write somehow, probably                
                quit()
      
    
    
    
"""
    Enters blocking system call loop
            #subprocess.check_call()
        #subprocess.call()
    
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

#========================================
Half done:
    Opens file with supplied filename for writing
        #aborts receiver when file already exists
#============================================
Done, moved from top:
#===========================================
    Other:
        Protocol mechanism to detect and handle bit errors
            #Not allowed to use a boolean flag;
            #IRL channels don't tell user about bit errors
#===========================================
Done
Takes following parameters from command line:
    #receiver_in port_num
        #range(1024-64,001)
    #receiver_out port_num
        #range(1024-64,001)
    #c_receiver_in port_num
        #receiver sends to channel through receiver_out to c_receiver_in
    #file name for received file to be stored
    Done
    Checks ports
    
    Done
    Creates/Binds sockets
    ##Meant to use something like c's connect() here???
    Set default receiver to port_num used by channel's c_receiver_in socket

        
    Done
    Initialises local int
        #expected = 0

"""

def receiver_main():
    p_r_in, p_r_out, p_r_s_in, fname = cmd_input()
    
    param_check_truth = param_check(p_r_in, p_r_out, p_r_s_in, fname)
    if param_check_truth:
        data_write = write_file(fname)
        #data_length = len(data_content)
        creation_binding_connection = create_bind_connect()
        expected = 0
        #_next, exit_flag, counter = initialisation()
        call_loop(data_write, expected)
        
    else:
        #exit the receiver because the parameters aren't all there
        quit()
        

#Run the program and hope it works!
receiver_main()

#MAGIC_NO = 0x497E
##The magic number

#PORT_RANGE = range(1024,64001)
##The range of valid ports, from 1024 to 64,000

#IP_ADDRESS = 127.0.0.1
##So the command line doesn't request an IP address all the time
##This is the Loopback address

#DATA_LEN_MAX = 512
#DATA_LEN_MIN = 0
##Max and min for data_len to avoid having more magic numbers


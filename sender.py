#===============================================================================
# Philippa Richardson and Emily Syme
# 05 August 2017
# COSC 264 - Introduction to Networking and the Internet
# Sender
#===============================================================================

#import packet
##is the packet class we made earlier

#import select
##Is the equivalent of C's select()

#import socket
##I mean we'll probably need it

import commons

def cmd_input():
    """Import information from the command line"""
    command_input = sys.stdin
    return command_input
    
def filename_exists(filename):
    """check if file by that name exists"""
    if os.path.isfile(filename):
        return True
    else:
        return False
    
def param_check(port_sender_in, port_sender_out, port_c_sender_in, filename):
    """
    #sender_in port_num
        #range(1024-64,001)
    #sender_out port_num
        #range(1024-64,001)
    #c_sender_in port_num
        #sender sends to channel through sender_out to c_sender_in
    
    Creates/Binds Sockets
    Uses connect() on sender_out to set c_sender_in default receiver for port number for channel.py
        """
    if ( (commons.port_num(port_sender_in)) and
         (commons.port_num(port_sender_out)) and
         (commons.port_num(port_c_sender_in)) and
         (filename_exists(filename)) ):
        return True

        
def create_bind_connect(param_check_truth):
    if param_check_truth:
        #create:
        socket_sender_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_sender_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_c_sender_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        #bind:
        socket_sender_in.bind(IP_ADDRESS, port_sender_in)
        socket_sender_out.bind(IP_ADDRESS, port_sender_out)
        
        #connect:
        socket_sender_out.connect(IP_ADDRESS, port_c_sender_in)
        
def openfile(filename):
    with open(filename, 'r', encoding="utf8") as infile:
        return infile    


def outer_loop():
    """Initialises the things it needs, then works through the outer loop"""
    
    _next = 0
    exit_flag = False
    
    #print counter result when program completed
    counter = 0
    
    n_bytes = 0
    while n_bytes < DATA_LEN_MAX:
        
        if n_bytes == 0:
            packet.packet_head(MAGIC_NO, DATA_PACKET, _next, DATA_LEN_MIN)
            #assignment states 'and an empty data field'
            exit_flag = True
            #place this packet into packet buffer, probably with return??
            
        else if n_bytes > 0:
            packet.packet_head(MAGIC_NO, DATA_PACKET, _next, n_bytes)
            #append n_bytes amount of data to it
            #place this packet into packet buffer, probably with return??
            
def inner_loop():
    
    
    
        
"""

    
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

def sender_main():
    p_s_in, p_s_out, p_c_s_in, fname = cmd_input()
    
    param_check_truth = param_check(p_s_in, p_s_out, p_c_s_in, fname)
    if param_check_truth:
        data_content = openfile()
        data_length = len(data_content)
        creation_binding_connection = create_bind_connect()
        outer = outer_loop(data_length)
        
        #close all the things
        #except for the data_content because that's part of the 'with' function
        socket_sender_in.close()
        socket_sender_out.close()
    else:
        #exit the sender because the parameters aren't all there
        quit()
        

#Run the program and hope it works!
sender_main()
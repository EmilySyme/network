#===============================================================================
#
# Philippa Richardson and Emily Syme
# 05 August 2017
# COSC 264 - Introduction to Networking and the Internet
# Channel
#
#===============================================================================


#===========================================
#Imports
#===========================================

import packet
#is the packet class we made earlier

import random
#is for the random number generator, returns float

import select
#Is the equivalent of C's select()

import socket
#Needed for sockets

import sys
#Needed to close things properly, amongst other things


#===========================================
#Variables
#===========================================
MAGIC_NO = 0x497E
#The magic number

PORT_RANGE = range(1024,64001)
#The range of valid ports, from 1024 to 64,000

IP_ADDRESS = "127.0.0.1"
#So the command line doesn't request an IP address all the time
#This is the Loopback address for running on localhost


#===============================================================================
#Functions
#===========================================

def port_num(port):
    """Checks that each individiual port number is in the correct port range"""
    if port not in PORT_RANGE:
        return False
    else:
        return True

#===========================================

def cmd_input():
    """Import information from the command line"""
    command_input = sys.stdin
    return command_input
    
#===========================================

def param_check(port_c_sender_in, port_c_sender_out, port_r_sender_in, port_r_sender_out, port_sender_in, port_receiver_in, P):
    """Just returns true if all of the parameters required are true"""
    if ( (port_num(port_c_sender_in)) and
         (port_num(port_c_sender_out)) and
         (port_num(port_r_sender_in)) and
         (port_num(port_r_sender_out)) and
         (port_num(port_sender_in)) and
         (port_num(port_receiver_in)) and
         (0 <= P < 1) ):
        return True

#===========================================

def create_bind_connect():
    """creates the socket, binds the socket, and connects the sockets"""
    
    #create:
    socket_chan_sender_in = socket.socket(family=socket.AF_INET, socket.SOCK_STREAM)
    socket_chan_sender_out = socket.socket(family=socket.AF_INET, socket.SOCK_STREAM)
    socket_chan_receiver_in = socket.socket(family=socket.AF_INET, socket.SOCK_STREAM)
    socket_chan_receiver_out = socket.socket(family=socket.AF_INET, socket.SOCK_STREAM)

    #bind:
    socket_chan_sender_in.bind(IP_ADDRESS, port_sender_in)
    socket_chan_sender_out.bind(IP_ADDRESS, port_sender_out)
    socket_chan_receiver_in.bind(IP_ADDRESS, port_receiver_in)
    socket_chan_receiver_out.bind(IP_ADDRESS, port_receiver_out)

    #connect:
    socket_chan_sender_out.connect(IP_ADDRESS, port_c_sender_in)
    print("connected channel out")
    socket_chan_receiver_out.connect(IP_ADDRESS, port_c_receiver_in)
    print("connected receiver out")

#===========================================

def pseudo_random(start, end):
    """Creates a random number between a start number and end number"""
    return random.uniform(start,end)    

#===========================================

def packet_drop(P):
    """Returns True or False which determines if a packet will or will not be dropped"""
    u = pseudo_random(0, 1)
    if u < P:
        return True #the packet will be dropped
    else:
        return False

#===========================================

def bit_errors(data_len):
    """Determines if bit errors will be introduced"""
    v = pseudo_random(0, 1)
    if v < 0.1:
        new_len = pseudo_random(0, 10)
        return new_len
 
#===========================================

def packet_changes(rcvd, P):
    """Changes the packets as required"""
    chan_magic_no, chan_packet_type, chan_seq_no, chan_data_len = packet.decoder(rcvd_packet)
    
    if ( (chan_magic_no != MAGIC_NO) or
        (packet_drop(P)) ):
        packet_received_loop(P)
        
    else:
        new_data_len = bit_errors(data_len)
        data_field = packet.packet_head(chan_magic_no, chan_packet_type, chan_seq_no, new_data_len)
        head = data_field.encrptyer()
        packet_buffer = bytearray(head + data_content)  
        return packet_buffer

#===========================================

def packet_received_loop(P):
    """Is the packet_received loop. Runs infinitely, until there is nothing in the input_received[0]"""
    input_received = select.select([socket_chan_sender_in, socket_chan_receiver_in], [], [])
    
    if input_received[0] == NULL:
        return
    
    #sender in goes to receiver out    
    if socket_chan_sender_in in input_received[0]:
        rcvd_packet = socket_chan_sender_in.recv()
        new_packet = packet_changes(rcvd_packet, P)
        socket_chan_receiver_out.send(new_packet)
        
    #receiver in goes to sender out
    if socket_chan_receiver_in in input_received[0]:
        rcvd_packet = socket_chan_receiver_in.recv()
        new_packet = packet_changes(rcvd_packet, P)
        socket_chan_sender_out.send(new_packet)
        
    packet_received_loop(P)

#===========================================

def channel_close(c_sender_in, c_sender_out, c_receiver_in, c_receiver_out, sender_in, receiver_in):
    """Closes all the sockets"""
    c_sender_in.close()
    c_sender_out.close()
    c_receiver_in.close()
    c_receiver_out.close()
    sender_in.close()
    receiver_in.close()


#===============================================================================

def channel_main():
    """Runs the channels"""
    c_sender_in, c_sender_out, c_receiver_in, c_receiver_out, sender_in, receiver_in, P = cmd_input()
    
    param_check_true = param_check(c_sender_in, c_sender_out, c_receiver_in, c_receiver_out, sender_in, receiver_in, P)
    
    if param_check_true:
        creation_binding_connection = create_bind_connect()
        packet_received_loop(P) 
        channel_close(c_sender_in, c_sender_out, c_receiver_in, c_receiver_out, sender_in, receiver_in)
     
    else:
        sys.exit()

#runs the code and hopes it works
channel_main()
#===============================================================================
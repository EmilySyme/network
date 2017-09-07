#===============================================================================
#
# Philippa Richardson and Emily Syme
# 05 August 2017
# COSC 264 - Introduction to Networking and the Internet
# Channel
#
#===============================================================================

#import packet
##is the packet class we made earlier

#import random
##is the random number generator
##random.uniform(0,1)
##returns float

#import select
##Is the equivalent of C's select()

#import socket
##I mean we'll probably need it

import commons

def cmd_input():
    """Import information from the command line"""
    command_input = sys.stdin
    return command_input
    
def param_check(port_c_sender_in, port_c_sender_out, port_r_sender_in, port_r_sender_out, sender_in, receiver_in, P):
    """
    #c_sender_in port_num
        #range(1024-64,001)
    #c_sender_out port_num
        #range(1024-64,001)
    #r_sender_in port_num
        #range(1024-64,001)
    #r_sender_out port_num
        #range(1024-64,001)
        """

    if ( (port_num(port_c_sender_in)) and
         (port_num(port_c_sender_out)) and
         (port_num(port_r_sender_in)) and
         (port_num(port_r_sender_out)) and
         (port_num(sender_in)) and
         (port_num(receiver_in)) and
         (0 <= P < 1) ):
        return True


def create_bind_connect():
    """creates the socket, binds the socket, and connects the sockets"""
    
    #create:
    socket_chan_sender_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_chan_sender_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_chan_receiver_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_chan_receiver_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #bind:
    socket_chan_sender_in.bind(IP_ADDRESS, port_sender_in)
    socket_chan_sender_out.bind(IP_ADDRESS, port_sender_out)
    socket_chan_receiver_in.bind(IP_ADDRESS, port_receiver_in)
    socket_chan_receiver_out.bind(IP_ADDRESS, port_receiver_out)

    #connect:
    ##not sure if this bit is right
    socket_chan_sender_out.connect(IP_ADDRESS, port_c_sender_in)
    socket_chan_receiver_out.connect(IP_ADDRESS, port_c_receiver_in)
    
def pseudo_random(start, end):
    """creates a random number between a start number and end number"""
    return random.uniform(start,end)    
    
def packet_drop(P):
    """Drops whole packets!!"""
    u = pseudo_random(0, 1)
    if u < P:
        return True #the packet will be dropped
    else:
        return False
    
def bit_errors(data_len):
    """Introduces bit errors"""
    v = pseudo_random(0, 1)
    if v < 0.1:
        new_len = pseudo_random(0, 10)
        return new_len
        
def packet_changes(rcvd, P):
    """Just keeping things modular here"""
    chan_magic_no, chan_type, chan_seq_no, chan_data_len = packet.decoder(rcvd_packet)
    
    if ( (chan_magic_no != MAGIC_NO) or
        (packet_drop(P)) ):
        infinite_loop(P)
        
    else:
        new_data_len = bit_errors(data_len)
        data_field = packet.packet_head(chan_magic_no, chan_type, chan_seq_no, new_data_len)
        head = data_field.encrptyer()
        packet_buffer = bytearray(head + data_content)  
        return packet_buffer

    
def infinite_loop(P):
    """recurrecurrecurrecursionsionsionsion"""
    input_received = select.select([socket_chan_sender_in, socket_chan_receiver_in], [], [])
    
    if input_received == NULL:
        exit()
    
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
        
    infinite_loop(P)
    
def channel_close(c_sender_in, c_sender_out, c_receiver_in, c_receiver_out, sender_in, receiver_in):
    """Time to go bye bye"""
    c_sender_in.close()
    c_sender_out.close()
    c_receiver_in.close()
    c_receiver_out.close()
    sender_in.close()
    receiver_in.close()


def channel_main():
    """I make the code channels"""
    c_sender_in, c_sender_out, c_receiver_in, c_receiver_out, sender_in, receiver_in, P = cmd_input()
    param_check_true = param_check(c_sender_in, c_sender_out, c_receiver_in, c_receiver_out, sender_in, receiver_in, P)
    if param_check_true:
        creation_binding_connection = create_bind_connect()
        infinite_loop(P) 
        channel_close(c_sender_in, c_sender_out, c_receiver_in, c_receiver_out, sender_in, receiver_in)
     
    else:
        quit()


#run me some channel        
channel_main()
#===============================================================================
#
# Philippa Richardson and Emily Syme
# 05 August 2017
# COSC 264 - Introduction to Networking and the Internet
# Channel
#
#===============================================================================
print("channel is on")

#===========================================
#Imports
#===========================================

import packet  # is the packet class we made earlier

import random  # is for the random number generator, returns float

import select  # Is the equivalent of C's select()

#from socket import socket  # Needed for sockets
import socket

import sys  # Needed to close things properly, amongst other things

import argparse  # for command line arguments


#===========================================
#GLOBAL Variables
#===========================================
MAGIC_NO = 0x497E
#The magic number

PORT_RANGE = range(1024,64001)
#The range of valid ports, from 1024 to 64,000

IP_ADDRESS = "127.0.0.1"
#So the command line doesn't request an IP address all the time
#This is the Loopback address for running on localhost

CONNECTION_WAIT = 5
#is the connection time wait


#===============================================================================
#Functions
#===========================================

def port_num(port):
    """Checks that each individiual port number is in the correct port range"""
    print("checking port numbers")
    if port not in PORT_RANGE:
        return False
    else:
        return True

#===========================================

def param_check(port_c_sender_in, port_c_sender_out, port_c_receiver_in, port_c_receiver_out, port_sender_in, port_receiver_in, P):
    print("Now checking parameters")
    """Just returns true if all of the parameters required are true"""
    if ( (port_num(port_c_sender_in)) and
         (port_num(port_c_sender_out)) and
         (port_num(port_c_receiver_in)) and
         (port_num(port_c_receiver_out)) and
         (port_num(port_sender_in)) and
         (port_num(port_receiver_in)) and
         (0 <= P < 1) ):
        return True

#===========================================

def create_bind_connect(port_c_sender_in, port_c_sender_out, port_c_receiver_in, port_c_receiver_out, port_sender_in, port_receiver_in,):
    """creates the socket, binds the socket, and connects the sockets""" 
    
    print("OHAI, channel is creating")
    #create:
    #channel.py receives from sender.py socket_sender_out via socket_c_sender_in
    socket_chan_sender_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #channel.py sends to sender.py socket_sender_in
    socket_chan_sender_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #channel.py receives from receiver.py socket_receiver_out via socket)_c_receiver_in
    socket_chan_receiver_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #channel.py sends to receiver.py socket_receiver_in
    socket_chan_receiver_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("OHAI, channel is binding")
    #bind:
    socket_chan_sender_in.bind((IP_ADDRESS, port_c_sender_in))
    socket_chan_sender_out.bind((IP_ADDRESS, port_c_sender_out))
    socket_chan_receiver_in.bind((IP_ADDRESS, port_c_receiver_in))
    socket_chan_receiver_out.bind((IP_ADDRESS, port_c_receiver_out))
    
    #probably want this as listen then connect
    #the other two might need to be the opposite to what is in here
    
   
    
    #maybe put this in a while loop until it connects
    
    print("OHAI, channel is listening")
    #listen:
    socket_chan_sender_in.listen(CONNECTION_WAIT)
    #so the one that is being connected needs to be listened for in the next one 
    #so whatever sender is sending out to connect to channel,
    #channel needs to listen for that 
    print("senpai plz notice sender")
    socket_chan_receiver_in.listen(CONNECTION_WAIT) #put a time to wait for
    print("senpai plz notice receiver")
    
    print("OHAI, channel is connecting")
    #connect:
    socket_chan_sender_out.connect((IP_ADDRESS, port_sender_in))
    print("connected channel out")
    socket_chan_receiver_out.connect((IP_ADDRESS, port_receiver_in))
    print("connected receiver out")    
    
    print("OHAI, channel is accepting")
    #accept:
    ##shouldn't these be socket_chan_receiver_in?
    (port_sender_in, add) = socket_chan_sender_out.accept()
    print("channel connected from sender yeeeeee boiiii")
    (port_receiver_in, add) = socket_chan_receiver_out.accept()
    print("channel connected to receiver woop")

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
    chan_magic_no, chan_packet_type, chan_seq_no, chan_data_len = packet.decoder(rcvd)
    
    if ( (chan_magic_no != MAGIC_NO) or
        ( packet_drop(P)) ):
        packet_received_loop(P)
        
    else:
        new_data_len = bit_errors(rcvd.data_len)
        data_field = packet.packet_head(chan_magic_no, chan_packet_type, chan_seq_no, new_data_len)
        head = data_field.encoder()
        packet_buffer = bytearray(head + rcvd.data_content)  
        return packet_buffer

#===========================================

#argparse
#Main loop of the channel is currently recursive needs to be fixed
#sockets to connect, listen and accept 

def packet_received_loop(P):
    """Is the packet_received loop. Runs infinitely, until there is nothing in the input_received[0]"""
    input_received = select.select([socket_chan_sender_in, socket_chan_receiver_in], [], [])
    
    if input_received[0] == None:
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
        
    #packet_received_loop(P)

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
    parser = argparse.ArgumentParser()
    
    parser.add_argument("c_sender_in", help="The channel's sender in port number; 1024 <= port <= 64001",
                        type=int)
    parser.add_argument("c_sender_out", help="The channel's sender out port number; 1024 <= port <= 64001",
                        type=int)
    parser.add_argument("c_receiver_in", help="The channel's receiver in port number; 1024 <= port <= 64001",
                        type=int) 
    parser.add_argument("c_receiver_out", help="The channel's receiver out port number; 1024 <= port <= 64001",
                        type=int)
    parser.add_argument("sender_in", help="The sender in port number; 1024 <= port <= 64001",
                        type=int)
    parser.add_argument("receiver_in", help="The receiver in port number; 1024 <= port <= 64001",
                        type=int)    
    parser.add_argument("P", help="The channel's packet loss rate; 0 <= P < 1",
                        type=float)       
    args = parser.parse_args()
    
    param_check_true = param_check(args.c_sender_in, args.c_sender_out, args.c_receiver_in, args.c_receiver_out, args.sender_in, args.receiver_in, args.P)
    
    #This is for testing
    #param_check_true = param_check(1024, 1025, 1026, 1027, 1028, 1029, 0)
    
    if param_check_true:
        create_bind_connect(args.c_sender_in, args.c_sender_out, args.c_receiver_in, args.c_receiver_out, args.sender_in, args.receiver_in)
        packet_received_loop(P) 
        channel_close(c_sender_in, c_sender_out, c_receiver_in, c_receiver_out, sender_in, receiver_in)
     
    else:
        sys.exit()

#runs the code and hopes it works
channel_main()
#===============================================================================
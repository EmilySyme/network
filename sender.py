#===============================================================================
# Philippa Richardson and Emily Syme
# 05 August 2017
# COSC 264 - Introduction to Networking and the Internet
# Sender
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

import argparse
#Needed for reading from standard input 

import os.path
#Needed for checking path of file 

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

TIME_OUT = 1000
#Is the timeout time in milliseconds

CONNECTION_WAIT = 5
#is the connection time wait

DATA_LEN_MAX = 512
DATA_LEN_MIN = 0
#Max and min for data_len to avoid having more magic numbers


#===============================================================================
#Functions
#===========================================

def port_num(port):
    """Checks that each supplied port number is in the correct port range"""
    if port not in PORT_RANGE:
        return False
    else:
        return True

#===========================================

def filename_exists(filename):
    """Check if file by that name exists"""
    
    if os.path.isfile(filename):
        print("filename found yay")
        return True
    else:
        print("filename not found")
        return False

#===========================================

def param_check(port_sender_in, port_sender_out, port_c_sender_in, filename):
    """Just returns true if all of the parameters required are true"""
    
    if ( (port_num(port_sender_in)) and
         (port_num(port_sender_out)) and
         (port_num(port_c_sender_in)) and
         (filename_exists(filename)) ):
        return True

#===========================================

def create_bind_connect(port_sender_in, port_sender_out, port_c_sender_in):
    """creates the socket, binds the socket, and connects the sockets"""
    #create:
    
    #Connects to socket_chan_sender_out from channel.py
    socket_sender_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Connects to socket_chan_sender_in from channel.py via socket_c_sender_in here
    socket_sender_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sender.py sends to channel.py through socket_sender_out to socket_chan_sender_in via socket_c_sender_in
    socket_c_sender_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    
    #bind:
    socket_sender_in.bind((IP_ADDRESS, port_sender_in))
    socket_sender_out.bind((IP_ADDRESS, port_sender_out))
    
    #connect:
    socket_sender_out.connect((IP_ADDRESS, port_c_sender_in))
    print("check me fam")
    
    
    #maybe put this in a while loop until it connects
    
    #listen:
    socket_sender_out.listen(CONNECTION_WAIT)
    print("u wanna hook up, bae?")
    
    #accept:
    (socket_sender_in, add) = socket_c_sender_in.accept()
    print("Senpai noticed me!")

#===========================================

def openfile(filename):
    """opens the file with a given name, and returns the infile"""
    with open(filename, 'rb') as infile:
        print("open file")
        return infile 

#===========================================

def initialisation():
    """initialises some variables needed only by sender"""
    _next = 0
    exit_flag = False
    
    #print counter result when program completed
    counter = 0 
    return _next, exit_flag, counter

#===========================================

def outer_loop(_next, exit_flag, data_content):
    """Initialises the things it needs, then works through the outer loop"""
    n_bytes = 0
    print("we're in the outer loop")
    while n_bytes < DATA_LEN_MAX:
        
        if n_bytes == 0:
            data_field = packet.packet_head(MAGIC_NO, DATA_PACKET, _next, DATA_LEN_MIN)
            head = data_field.encoder()
            exit_flag = True

        elif n_bytes > 0:
            data_field = packet.packet_head(MAGIC_NO, DATA_PACKET, _next, n_bytes)
            head = data_field.encoder()

        packet_buffer = bytearray(head + data_content)
        return packet_buffer

#===========================================

def inner_loop(counter, _next, exit_flag, data_content, packet_buffer):
    """I summon Inner Loop in attack mode!"""
    packet_rcvd = False
    print("we're in the inner loop")
    while not packet_rvcd:
        socket_sender_out.send(packet_buffer)
        print("I should be sending a thing right now")
        counter += 1
        rcvd, _, _ = select.select([socket_sender_out], [], [], TIME_OUT)
        if not rcvd:
            inner_loop(counter, _next, exit_flag, data_content)
        else:
            rcvd_magic_no, rcvd_packet_type, rcvd_seq_no, rcvd_data_len = packet.decoder(rcvd)
            if ((rcvd_magic_no != MAGIC_NO) or
            (rcvd_pack_type != acknowledgement_packet) or 
            (rcvd_data_len != DATA_LEN_MIN)) or (rcvd_seq_no != _next):
                inner_loop(counter, _next, exit_flag, data_content)
            else:
                _next -= 1
                if exit_flag == True:
                    return
                else:
                    outer_loop(_next, exit_flag, data_content)


#===============================================================================

def sender_main():
    """runs the code"""
    
    parser = argparse.ArgumentParser()
    parser.add_argument("p_s_in", type=int, help="sender socket in")
    parser.add_argument("p_s_out", type=int, help="sender socket out") 
    parser.add_argument("p_c_s_in", type=int, help="channel socket")
    parser.add_argument("fname", type=str, help="filename wanting to be sent")
    args = parser.parse_args()
    
    
    param_check_truth = param_check(args.p_s_in, args.p_s_out, args.p_c_s_in, args.fname)
    
    if param_check_truth:
        
        data_content = openfile(args.fname)
        creation_binding_connection = create_bind_connect(args.p_s_in, args.p_s_out, args.p_c_s_in)
        _next, exit_flag, counter = initialisation()
        packet_buff = outer_loop(_next, exit_flag, data_content)
        inner_loop(counter,_next, exit_flag, data_content, packet_buff)
        
        #close all the things
        #except for the data_content because that's part of the 'with' function
        print(counter)
        socket_sender_in.close()
        socket_sender_out.close()
    else:
        #exit the sender because the parameters aren't all there
        sys.exit()
        

#Run the program and hope it works!
sender_main()

#===============================================================================
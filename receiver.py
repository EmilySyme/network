#===============================================================================
# Philippa Richardson and Emily Syme
# 05 August 2017
# COSC 264 - Introduction to Networking and the Internet
# Receiver
#===============================================================================

#===========================================
#Imports
#===========================================

import packet
#is the packet class we made earlier

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

DATA_LEN_MAX = 512
DATA_LEN_MIN = 0
#Max and min for data_len to avoid having more magic numbers

DATA_PACKET = 0
ACKNOWLEDGEMENT_PACKET = 0

CONNECTION_WAIT = 5
#is the connection time wait

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

def filename_exists(filename):
    """Check if file by that name exists"""
    if os.path.isfile(filename):
        return True
    else:
        return False

#===========================================

def param_check(port_receiver_in, port_receiver_out, port_c_receiver_in, filename):
    """"""
    if ( (port_num(port_receiver_in)) and
         (port_num(port_receiver_out)) and
         (port_num(port_c_receiver_in)) and
         (filename_exists(filename))):
        return True

#===========================================

def create_bind_connect(port_receiver_in, port_receiver_out, port_c_receiver_in):
    #create:
    #Connects to socket_chan_receiver_out from channel.py
    socket_receiver_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Connects to socket_chan_receiver_in from channel.py via socket_c_receiver_in here
    socket_receiver_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #receiver.py sends to channel.py through socket_receiver_out to socket_chan_receiver_in via socket)_c_recever_in
    socket_c_receiver_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #bind:
    socket_receiver_in.bind((IP_ADDRESS, port_receiver_in))
    socket_receiver_out.bind((IP_ADDRESS, port_receiver_out))
        
    #connect:
    socket_receiver_out.connect((IP_ADDRESS, port_c_receiver_in))
    print("help me")
    
    #listen:
    socket_receiver_out.listen(CONNECTION_WAIT)
    print("senpai plz notice receiver")
    
    
    #accept:
    (socket_receiver_in, add) = socket_c_receiver_in.accept()
        

#===========================================

def write_file(packet):
    """takes a packet and appends it to the end of the
    receivedpackets.txt file"""
    receiver_file = open('receivedpackets.txt', 'a')
    receiver_file.write(packet)  #use this to write to the file
    receiver_file.close() 

#===========================================

def acknowledged(seq_no):
    """"""
    acknowledge_packet = packet.packet_head(MAGIC_NO, ACKNOWLEDGEMENT_PACKET, seq_no, 0)
    head = acknowledge_packet.encoder()
    packet_buffer = bytearray(head)
    socket_receiver_out.send(packet_buffer)

#===========================================

def call_loop(expected):
    """"""
    #I think this might be how to do it; apparently select can be blocking too, from the stuff in the assignment info
    rcvd_packet = select.select([socket_receiver_in], [], [])
    rcvd_magic_no, rcvd_type, rcvd_seq_no, rcvd_data_len = packet.decoder(rcvd_packet)
    if ( (magic_no != MAGIC_NO) or
        (packet_type != DATA_PACKET) ):
        call_loop(expected)
    else:
        acknowledged(rcvd_seq_no)
        if (rcvd_seq_no != expected):
            call_loop(expected)
        else:
            expected = 1 - expected
            if (rcvd_data_len > 0):
                write_file(rcvd_packet)
                call_loop(expected)
            else:
                #close all the things
                socket_receiver_in.close()
                socket_receiver_out.close()                
                return


#===============================================================================

def receiver_main():
    """Runs the receiver"""
    
    parser = argparse.ArgumentParser()
    parser.add_argument("p_r_in", type=int, help="receiver socket in")
    parser.add_argument("p_r_out", type=int, help="receiver socket out") 
    parser.add_argument("p_r_s_in", type=int, help="channel socket")
    parser.add_argument("fname", type=str, help="filename of file being sent")
    args = parser.parse_args()    

    
    param_check_truth = param_check(args.p_r_in, args.p_r_out, args.p_r_s_in, args.fname)
    
    if param_check_truth:
        print("Params check out")
        creation_binding_connection = create_bind_connect(args.p_r_in, args.p_r_out, args.p_r_s_in)
        print("connected")
        expected = 0
        #now use the new connected socket from accept 
        call_loop(data_write, expected)
        
    else:
        #exit the receiver because the parameters aren't all there
        sys.exit()
        

#Run the program and hope it works!
receiver_main()
#===============================================================================
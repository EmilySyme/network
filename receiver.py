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

DATA_LEN_MAX = 512
DATA_LEN_MIN = 0
#Max and min for data_len to avoid having more magic numbers

DATA_PACKET = 0
ACKNOWLEDGEMENT_PACKET = 1

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

def param_check(port_receiver_in, port_receiver_out, port_c_receiver_in):
    """"""
    if ( (commons.port_num(port_receiver_in)) and
         (commons.port_num(port_receiver_out)) and
         (commons.port_num(port_c_receiver_in))):
        return True

#===========================================

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

#===========================================

def write_file(filename):
    """Opens file with supplied filename for writing
        #aborts receiver when file already exists"""
    #OH GODS how do I write things to file?! *crying*
    #Emily, fiiiiiixxxxxxxxx iiiiiiiitttttttt~~~~~

#===========================================

def acknowledged(seq_no):
    """"""
    acknowledge_packet = packet.packet_head(MAGIC_NO, ACKNOWLEDGEMENT_PACKET, seq_no, 0)
    head = acknowledge_packet.encoder()
    packet_buffer = bytearray(head)
    socket_receiver_out.send(packet_buffer)

#===========================================

def call_loop(write_file, expected):
    """"""
    #I think this might be how to do it; apparently select can be blocking too, from the stuff in the assignment info
    rcvd_packet = select.select([socket_receiver_in], [], [])
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


#===============================================================================

def receiver_main():
    """Runs the receiver"""
    
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
        sys.exit()
        

#Run the program and hope it works!
receiver_main()
#===============================================================================
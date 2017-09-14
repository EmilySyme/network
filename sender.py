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

TIME_OUT = 1000
#Is the timeout time in milliseconds


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

def cmd_input():
    """Import information from the command line"""
    command_input = sys.stdin
    return command_input

#===========================================

def filename_exists(filename):
    """Check if file by that name exists"""
    if os.path.isfile(filename):
        return True
    else:
        return False

#===========================================

def param_check(port_sender_in, port_sender_out, port_c_sender_in, filename):
    """Just returns true if all of the parameters required are true"""
    if ( (commons.port_num(port_sender_in)) and
         (commons.port_num(port_sender_out)) and
         (commons.port_num(port_c_sender_in)) and
         (filename_exists(filename)) ):
        return True

#===========================================

def create_bind_connect():
    """creates the socket, binds the socket, and connects the sockets"""
       
    #APPARENTLY we could just leave all of these as socket.socket();
    #but leaving it like this for clarity
    #also lazy
    
    #create:
    socket_sender_in = socket.socket(family=socket.AF_INET, socket.SOCK_STREAM)
    socket_sender_out = socket.socket(family=socket.AF_INET, socket.SOCK_STREAM)
    socket_c_sender_in = socket.socket(family=socket.AF_INET, socket.SOCK_STREAM)
    
    #bind:
    socket_sender_in.bind(IP_ADDRESS, port_sender_in)
    socket_sender_out.bind(IP_ADDRESS, port_sender_out)
    
    #connect:
    socket_sender_out.connect(IP_ADDRESS, port_c_sender_in)
    print("check me fam")
    
    #listen:
    socket_sender_out.listen(IP_ADDRESS, port_c_sender_in)
    print("u wanna hook up, bae?")
    
    #accept:
    (socket_sender_in, add) = socket_c_sender_in.accept()
    print("Senpai noticed me!")

#===========================================

def openfile(filename):
    """opens the file with a given name, and returns the infile"""
    with open(filename, 'r', encoding="utf8") as infile:
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
    while n_bytes < DATA_LEN_MAX:
        
        if n_bytes == 0:
            data_field = packet.packet_head(MAGIC_NO, DATA_PACKET, _next, DATA_LEN_MIN)
            head = data_field.encrptyer()
            exit_flag = True

        elif n_bytes > 0:
            data_field = packet.packet_head(MAGIC_NO, DATA_PACKET, _next, n_bytes)
            head = data_field.encrptyer()

        packet_buffer = bytearray(head + data_content)

#===========================================

def inner_loop(counter, _next, exit_flag, data_content):
    """I summon Inner Loop in attack mode!"""
    packet_rcvd = False
    
    while not packet_rvcd:
        socket_sender_out.send(packet_buffer)
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
    p_s_in, p_s_out, p_c_s_in, fname = cmd_input()
    
    param_check_truth = param_check(p_s_in, p_s_out, p_c_s_in, fname)
    if param_check_truth:
        data_content = openfile()
        creation_binding_connection = create_bind_connect()
        _next, exit_flag, counter = initialisation()
        outer_loop(_next, exit_flag, data_content)
        inner_loop(counter,_next, exit_flag, data_content)
        
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
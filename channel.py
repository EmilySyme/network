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
    #What do for sender_in and receiver_in
    if ( (port_num(port_c_sender_in)) and
         (port_num(port_c_sender_out)) and
         (port_num(port_r_sender_in)) and
         (port_num(port_r_sender_out)) and
         (port_num(sender_in)) and
         (port_num(receiver_in)) and
         (0 <= P < 1) ):
        return True


def create_bind_connect():
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
    """"""
    input_received = select.select([socket_chan_sender_in, chan_recv_in_socket], [], [])
    
    
    #sender in goes to receiver out    
    if socket_chan_sender_in in input_received[0]:
        rcvd_packet = chan_socket_sender_in.recv()
        new_packet = packet_changes(rcvd_packet, P)
        socket_chan_receiver_out.send(new_packet)
        
    #receiver in goes to sender out
    elif socket_chan_receiver_in in input_received[0]:
            rcvd_packet = chan_socket_sender_in.recv()
            new_packet = packet_changes(rcvd_packet, P)
            socket_chan_sender_out.send(new_packet)
    

"""
 Channel enters an infinite loop, doing:
     #Waits for input on either the c_sender_in or the c_receiver_in socket
     ---uses select() in C in blocking fashion to save CPU time
     #returns vaue indicating number of sockets that have data ready
         #value >= 1 (both sockets may arrive simultaneously)
         #if value > 1, ALL packets must be processed
         
 Example:
     Checks content of magicno field against fixed value of 0x497E
         #if different, processing stopped; loop restarted
     Introduces packet losses
         #generates uniformly distributed random variate between 0 and 1 (u).
             #if v < P: packet drops; loop restarted
    Introduces bit errors
        #if packet not dropped:
            #generates uniformly distributed random variate between 0 and 1 (v).
                #if v < 0.1, channel increments packet data_len by random int range(1,10) from uniform dist.
            #bit errors noticed in sender and receiver
    Forwards packet
        #if packet not dropped:
            #if packet received on c_sender_in
                #sends the packet to receiver via c_receiver_out;
                #receiver gets packet via receiver_in
            #if packet received on c_receiver_in socket
                #sends the packet to sender via c_sender_out;
                #sender gets packet via sender_in socket
    Close program using equivalent of close() on open sockets or files
    #=============================================
    Half done
    #============================================= 
    
    #need to double check on the sender/receiver_in
 -c_sender_in - check is int, port number, range(1024-64,001)
 -c_sender_out - check is int, port number, range(1024-64,001)
 -c_receiver_in - check is int, port number, range(1024-64,001)
 -c_receiver_out - check is int, port number, range(1024-64,001)
 -sender_in - check is int, port number from sender - sending packets from channel to sender via cr_out
 -receiver_in - check is int, port number to receiver - sending packets to receiver using c_receiver_out
 -P - int, packet loss rate (greater than or equal to 0, less than 1)
    #=============================================
    Done
    #=============================================
    Reads seven parameters from the command line:

 
 #done
 ##think the create/bind is working
 Checks above parameters
 Creates/Binds all of the 4 sockets
 ##We should be using something 'connect()' here??? according to the sheet???
 --this is probably a C thing
 #this isnt being used, what would it be used for?
 ##We should be also using something called 'select()' here??? according to the sheet???
 --this is definitely a C thing
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

def channel_main():
    c_sender_in, c_sender_out, c_receiver_in, c_receiver_out, sender_in, receiver_in, P = cmd_input()
    check_the_things = param_check(c_sender_in, c_sender_out, c_receiver_in, c_receiver_out, sender_in, receiver_in, P)
    if check_the_things:
        connect_the_things = create_bind_connect()
        infinite_loop(P)
        #enter infinite loop here
        #packet_drop = False
        #while stuff happens
        #check something == MAGIC_NO
        #if no:
        #stop processing, restart loop
        #if yes:
        #v = pseudo_random()
        #if v < P:
        #packet_drop = True
        #restart loop
        #if !packet_drop:
        # if packet from c_sender_in:
        #send packet to c_receiver_out
        #if packet from c_receiver_in:
        #send packet to c_sender_out
        #close program
        
        
        
        
    else:
        #probably a return back to either sender or receiver depending on where it came from?
        #I'll let you help with this, bc I am not sure
        quit()


#run me some channel        
channel_main()
#===============================================================================
#
# Philippa Richardson and Emily Syme
# 05 August 2017
# COSC 264 - Introduction to Networking and the Internet
# Channel
#
#===============================================================================

import packet
#is the packet class we made earlier

import random
#is the random number generator
#random.uniform(0,1)
#returns float

import select
#Is the equivalent of C's select()

import socket
#I mean we'll probably need it

"""
generates pseudo-random numbers with library

Reads seven parameters from the command line:
 -c_sender_in - check is int, port number, range(1024-64,001)
 -c_sender_out - check is int, port number, range(1024-64,001)
 -c_receiver_in - check is int, port number, range(1024-64,001)
 -c_receiver_out - check is int, port number, range(1024-64,001)
 -sender_in - check is int, port number from sender - sending packets from channel to sender via cr_out
 -receiver_in - check is int, port number to receiver - sending packets to receiver using c_receiver_out
 -P - int, packet loss rate (greater than or equal to 0, less than 1)
 
 Checks above parameters
 Creates/Binds all of the 4 sockets
 ##We should be using something 'connect()' here??? according to the sheet???
 --this is probably a C thing
 ##We should be also using something called 'select()' here??? according to the sheet???
 --this is definitely a C thing
 
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
"""

MAGIC_NO = 0x497E
#The magic number

PORT_RANGE = range(1024,64001)
#The range of valid ports, from 1024 to 64,000

IP_ADDRESS = 127.0.0.1
#So the command line doesn't request an IP address all the time
#This is the Loopback address
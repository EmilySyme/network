#common list of variables and imports

import packet
#is the packet class we made earlier
#needed by channel
#needed by receiver
#needed by sender

import random
#is the random number generator
#random.uniform(0,1)
#returns float
#needed by channel

import select
#Is the equivalent of C's select()
#needed by channel
#needed by sender

import socket
#I mean we'll probably need it
#needed by channel
#needed by receiver
#needed by sender

import connect
#I mean I think this is a thing we'll need to be importing???
#if it's a real thing, Sender needs it

import struct
#I think this is a thing that's needed


import argparse  # for command line arguments
import datetime  # for getting the date in a pretty way

MAGIC_NO = 0x497E
#The magic number
#needed by channel
#needed by receiver
#needed by sender

PORT_RANGE = range(1024,64001)
#The range of valid ports, from 1024 to 64,000
#needed by channel
#needed by receiver
#needed by sender

IP_ADDRESS = 127.0.0.1
#So the command line doesn't request an IP address all the time
#This is the Loopback address for running on localhost
#needed by channel
#needed by receiver
#needed by sender

DATA_LEN_MAX = 512
DATA_LEN_MIN = 0
#Max and min for data_len to avoid having more magic numbers
#needed by channel
#needed by receiver
#needed by sender

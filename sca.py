import sys
from scapy.all import *


while True:
    sniff(iface="Intel(R) Wi-Fi 6 AX201 160MHz", prn = lambda x:x.show())

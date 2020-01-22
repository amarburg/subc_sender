#!/usr/bin/env python3

import ipaddress

class CamConfig:

    # 888 is the default port for the SubC Camera interface
    def __init__(self, host, name="", port=8888, fake=False):
        self.host = host
        self.port = port
        self.fake = fake
        self.name = name


def addDefaultArgs( parser ):

    parser.add_argument("--fake", action='store_true', help="Don't actually connect to cameras" )
    parser.add_argument("--left", dest="left_ip", default="192.168.13.228")
    parser.add_argument("--right", dest="right_ip", default="192.168.13.234")
    parser.add_argument("--left-port", type=int, default=8888)
    parser.add_argument("--right-port", type=int, default=8888)

    parser.add_argument("--left-only", action="store_true")
    parser.add_argument("--right-only", action="store_true")



def camsFromArgs( args ):

    cams = []

    if not args.right_only:
        cams.append( CamConfig( ipaddress.ip_address(args.left_ip), port=args.left_port, name="LEFT" ) )

    if not args.left_only:
        cams.append( CamConfig( ipaddress.ip_address(args.right_ip), port=args.right_port, name="RIGHT" ) )

    return cams

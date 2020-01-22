import struct
import binascii
import socket
from datetime import datetime

import asyncio

class CamSocket:

    # 888 is the default port for the SubC Camera interface
    def __init__(self, cam):
        self.cam = cam
        self.sock = socket.socket(  socket.AF_INET, socket.SOCK_STREAM )
        self.connect()

    def connect(self):
        if not self.cam.fake:
            self.sock.connect( (str(self.cam.host), self.cam.port) )

    async def send( self, msg ):

        now = datetime.now().strftime("%H:%M:%S.%f")
        print("% 9s | % 5s (%3d) <--- %s" % (now, self.cam.name, len(msg), msg) )

        ## Message starts with four (little-endian) message length bytes
        outbuffer = struct.pack('<I', len(msg)) + msg.encode('ascii')

        #print(binascii.hexlify(outbuffer).decode('ascii'))

        if self.cam.fake:
            return

        msglen = len(outbuffer)

        totalsent = 0
        while totalsent < msglen:
            sent = self.sock.send(outbuffer[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    # def receive( self ):
    #
    #     if self.cam.fake:
    #         return ""
    #
    #     lenmsg = self.sock.recv(4)
    #     if lenmsg == b'':
    #         raise RuntimeError("socket connection broken")
    #
    #     #print(binascii.hexlify(lenmsg).decode('ascii'))
    #
    #     a = struct.unpack('<I', lenmsg )
    #     msglen = a[0]
    #
    #     if msglen > 256:
    #         raise RuntimeError("Unexpected msg length %d" % msglen)
    #
    #     #print("Waiting for %d bytes" % msglen)
    #
    #     chunks = []
    #     bytes_recd = 0
    #     while bytes_recd < msglen:
    #         chunk = self.sock.recv(min(msglen - bytes_recd, 2048))
    #         if chunk == b'':
    #             raise RuntimeError("socket connection broken")
    #         chunks.append(chunk)
    #         bytes_recd = bytes_recd + len(chunk)
    #     return b''.join(chunks)



class CamSender:

    def __init__( self, cameras=[] ):
        self.senders = [CamSocket(cam) for cam in cameras]

    async def send( self, fp ):
        for n,line in enumerate(fp):
            line = line.rstrip()

            for sender in self.senders:
                await sender.send(line)

# async def send( fp, cameras=[] ):
#
#     senders = [CamSocket(cam) for cam in cameras]
#
#     await asyncio.sleep(1)
#
#     for n,line in enumerate(fp):
#         line = line.rstrip()
#         #print("Sending %d: %s" % (n,line))
#
#         for sender in senders:
#             await sender.send(line)

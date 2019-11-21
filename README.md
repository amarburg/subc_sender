## Test tools for interacting with the remote TCP interface on the SubC Rayfin camera

The Rayfin cameras expose a scripting / remote control socket on TCP port 8888.

Once connected the port, the camera will stream log message out of the port (I've seen NTP updates, ambient temperatures, and timestamps).   Commands from the [Rayfin API]()  (link?) can be sent to the camera.   Responses (if there are any) will be interleaved into the returning data stream.

All messages travelling in both direction have a simple packet format:

    [4 byte message header] + [ASCII scripting command]

The first byte of the header is the length of the ASCII command.  Not sure if it's a byte length followed by 3 zeros of a 32-bit length formatted LSB?

## Test tools for interacting with the remote TCP interface on the SubC Rayfin cameras

The Rayfin cameras expose a scripting / remote control socket on TCP port 8888.

Once connected the port, the camera will stream log message out of the port (I've seen NTP updates, ambient temperatures, and timestamps).   Commands from the [Rayfin API]()  (link?) can be sent to the camera.   Responses (if there are any) will be interleaved into the returning data stream.

All messages traveling in both directions have a simple packet format:

    [4 byte message header] + [ASCII scripting command]

The header is a 32-bit LSB integer of the length of the ASCII command.

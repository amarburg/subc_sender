

def send( fp, cameras=[] ):

    for n,line in enumerate(fp):
        line = line.rstrip()
        print("Sending %d: %s" % (n,line))

        for cam in cameras:
            if cam:
                cam.send(line)


import re
from datetime import datetime,timezone
from pathlib import Path

def regularize_filename(filename):

    p = Path(filename)


    parts = re.split(r'[\. ]', p.name)

    ext = parts.pop()

    parts = [int(p) for p in parts]

    d = datetime( year=parts[0],
                    month=parts[1], day=parts[2], hour=parts[3], minute=parts[4], second=parts[5], microsecond=parts[6]*1000)

    new_filename = p.parent / ("%s.%s" % (d.isoformat(timespec='milliseconds'), ext))
    return new_filename

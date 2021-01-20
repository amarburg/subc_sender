
import re
from datetime import datetime,timezone
from pathlib import Path

def subc_file_to_datetime( filename ):
    ## Isolate just the file name itself
    filename = filename.name
    #
    # parts = re.split(r'[\. ]', p.name)
    #
    # parts = [int(p) for p in parts]
    #
    # return datetime( year=parts[0],
    #                 month=parts[1], day=parts[2], hour=parts[3], minute=parts[4], second=parts[5], microsecond=parts[6]*1000)

    return datetime.strptime(filename, "%Y.%m.%d %H.%M.%S.%f.dng")


def regularize_filename(filename):

    p = Path(filename)
    ext = p.suffix
    d = subc_file_to_datetime( p )

    new_filename = p.parent / (d.isoformat(timespec='milliseconds') + ext)
    return new_filename

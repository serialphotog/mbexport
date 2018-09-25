import argparse
import logging
import os
import sqlite3

def write_tile(output_dir, zoom_level, column, row, data):
    path = os.path.join(output_dir, str(zoom_level), str(column))
    if not os.path.exists(path):
        os.makedirs(path)

    f = open(os.path.join(path, str(row) + ".jpg"), 'w+b')
    binary_fmt = bytearray(data)
    f.write(binary_fmt)
    f.close()

def dump_tiles(mbtilePath, output_path):
    conn = sqlite3.connect(mbtilePath)

    for row in conn.execute('SELECT * FROM tiles'):
        zoom_level = row[0]
        tile_col = row[1]
        tile_row = row[2]
        tile_data = row[3]

        write_tile(output_path, zoom_level, tile_col, tile_row, tile_data)

    conn.close()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Handle command line args
parser = argparse.ArgumentParser(description="A simple utility to extract files from MBTiles")
parser.add_argument("--input", dest="mbtile_path", help="Path to the mbtile file")
parser.add_argument("--output", dest="output_path", help="Directory to dump tiles to")
args = parser.parse_args()

if not args.mbtile_path or not args.output_path:
    logger.error("You must supply an input and output!")
elif not os.path.isfile(args.mbtile_path):
    logger.error("The input file " + args.mbtile_path + " does not exist.")
elif not os.path.exists(args.output_path):
    logger.error("The output path " + args.output_path + " does not exist.")
else:
    logger.info("Dumping tiles for " + args.mbtile_path + " to " + args.output_path)

    dump_tiles(args.mbtile_path, args.output_path)


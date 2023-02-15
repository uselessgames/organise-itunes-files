#!/usr/bin/env python3
"""
    A script to un-obfuscate itunes music files
    supports .mp3
"""

from logging.handlers import RotatingFileHandler
from mutagen.easymp4 import EasyMP4Tags
from mutagen.easyid3 import EasyID3
import argparse
import logging
import os
import shutil

def setup_logging(log_path):
    logging.basicConfig(
        handlers=[
            RotatingFileHandler(
                log_path,
                maxBytes=100000,
                backupCount=10,
            )
        ],
        level=logging.INFO,
        format= "[%(asctime)s] %(levelname)s %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S',
    )

def check_tree(dir_path):
  for f in dir_path:
    if not os.path.exists(dir_path):
      os.makedirs(dir_path)  

def file_copy(copy_source, copy_dest):
  try:
    shutil.copy(copy_source, copy_dest)
    status = f"copied: {copy_dest}"
    print(status)
  except shutil.SameFileError:
    logging.info(f"duplicate, cannot copy: {copy_source}")
  except PermissionError:
    logging.info(f"permission denied, did not copy: {copy_source}")
  except:
    logging.info(f"unhandled exception while copying: {copy_source}")

def parse_args():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
  )
  parser.add_argument (
    '-d', 
    '--source_dir',
    help='the source directory to organise',
  )
  parser.add_argument (
    '-o', 
    '--out_dir', 
    default='./out',
    help=(
        'where to save new organised file. if not provided a new '
        'folder named out will be created.'
      ),
  )
  parser.add_argument (
    '-l', 
    '--log_path', 
    default='./song-fix.log',
    help='the path to the log file',
  )
  return parser.parse_args()

def parse_audio_files(source, out):
  for (root, dirs, files) in os.walk(source, topdown=True):
    for f in files:
      (base, ext) = os.path.splitext(f) 
      if ext in ('.mp3'):          
        source_name = os.path.join(root, f)      
        song = EasyID3(source_name)
        artist = str(song['artist'][0])
        album = str(song['album'][0])
        tracknumber = str(song['tracknumber'][0])
        title = str(song['title'][0])
        new_name = f"{artist} - {album} - {tracknumber} - {title}.mp3"
        new_folder = os.path.join(out,artist,album)
        new_dest = os.path.join(new_folder,new_name)
        check_tree(new_folder)
        file_copy(source_name,new_dest)

def main():
  args = parse_args()
  setup_logging(
    args.log_path
  )
  songs = parse_audio_files(args.source_dir, args.out_dir)
  
  print("finished, check log for errors")

if __name__ == "__main__":
  main()


"""
to-do
- some mp3 are not copying
- add mp4 support (m4a, m4b, m4p)

"""
#!/usr/bin/env python3
"""
    A script to un-obfuscate itunes music files
    supports .mp3 and .mp4 (m4a, m4b, m4p)
"""

from logging.handlers import RotatingFileHandler
from mutagen.easymp4 import EasyMP4
from mutagen.easyid3 import EasyID3
from re import sub
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
    logging.info (status)
    print(status)
  except:
    logging.exception(f"unhandled exception while copying: {copy_source}")

def sanitise(string):
  return sub(r'[?|$|.|!|/|\\]',r'', string)

def fix_tracknumber(track):
  return sub('(?=/)(.*)',"", track)

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
      if ext in ('.mp3','.mp4','.m4a','.m4b','.m4p'):          
        source_name = os.path.join(root, f)
        if ext in ('.mp3'):
          song = EasyID3(source_name)
        elif ext in ('.mp4','.m4a','.m4b','.m4p'):
          song = EasyMP4(source_name)
        artist = sanitise(f"{song['artist'][0]}")
        album = sanitise(f"{song['album'][0]}")
        tracknumber = fix_tracknumber(f"{song['tracknumber'][0]}")
        title = sanitise(f"{song['title'][0]}")
        if ext in ('.mp3'):
          new_name = f"{artist} - {album} - {tracknumber} - {title}.mp3"
        elif ext in ('.mp4','.m4a','.m4b','.m4p'):
          new_name = f"{artist} - {album} - {tracknumber} - {title}.m4a"
        #print(new_name)
        new_folder = os.path.join(out,artist,album)
        new_dest = os.path.join(new_folder,new_name)
        check_tree(new_folder)
        file_copy(source_name,new_dest)

def main():
  args = parse_args()
  setup_logging(
    args.log_path
  )
  try:
    songs = parse_audio_files(args.source_dir, args.out_dir)
  except:
    logging.exception("unhandled exception")
    exit(1)

  logging.info(f"EOF")
  print("finished, check log for errors")

if __name__ == "__main__":
  main()
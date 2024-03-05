import os
import mimetypes
from os import scandir, rename
from os.path import exists, join, splitext
from shutil import move

import logging

source_dir = r"c:\Users\HP\Downloads"
dest_dir_audio = r"c:\Users\HP\Downloads\Downloaded Audio"
dest_dir_video = r"c:\Users\HP\Downloads\Downloaded Videos"
dest_dir_image = r"c:\Users\HP\Downloads\Downloaded Images"
dest_dir_documents = r"c:\Users\HP\Downloads\Downloaded Documents"

logging.basicConfig(level=logging.INFO)

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(join(dest, name)):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
    return name

def get_mime_type(filename):
    return mimetypes.guess_type(filename)[0]

def move_file(dest, entry, name):
    try:
        if exists(join(dest, name)):
            unique_name = make_unique(dest, name)
            oldName = join(dest, name)
            newName = join(dest, unique_name)
            rename(oldName, newName)
        move(entry, dest)
    except Exception as e:
        logging.error(f"Error while moving file {name}: {e}")

def organize_files():
    with scandir(source_dir) as entries:
        for entry in entries:
            if entry.is_file():
                name = entry.name
                mime_type = get_mime_type(entry.path)
                if mime_type and mime_type.startswith('audio'):
                    move_file(dest_dir_audio, entry.path, name)
                    logging.info(f"Moved audio file: {name}")
                elif mime_type and mime_type.startswith('video'):
                    move_file(dest_dir_video, entry.path, name)
                    logging.info(f"Moved video file: {name}")
                elif mime_type and mime_type.startswith('image'):
                    move_file(dest_dir_image, entry.path, name)
                    logging.info(f"Moved image file: {name}")
                elif mime_type and (mime_type.startswith('application/pdf') or mime_type.startswith('application/msword') or mime_type.startswith('application/vnd.openxmlformats-officedocument') or mime_type.startswith('text/plain')):
                    move_file(dest_dir_documents, entry.path, name)
                    logging.info(f"Moved document file: {name}")
                else:
                    logging.warning(f"Unknown file type for {name}. Skipping.")

if __name__ == "__main__":
    organize_files()

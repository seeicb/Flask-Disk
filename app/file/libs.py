import hashlib
import random
import string
import os
from hdfs import *
from manage import app

hdfs_client = Client(app.config.get('HDFS_IP'))

def get_md5(md5_str):

    md5 = hashlib.md5()
    md5.update((md5_str).encode('utf-8'))
    return md5.hexdigest()

def set_type(file_ext):
    DOCUMENTS = tuple('rtf odf ods gnumeric abw doc docx xls xlsx txt csv pdf'.split())
    IMAGES = tuple('jpg jpe jpeg png gif svg bmp'.split())
    AUDIO = tuple('wav mp3 aac ogg oga flac'.split())
    VIDEO = tuple('avi rmvb rm divx mpg mpeg mpe wmv mp4 mkv vob'.split())
    if file_ext in DOCUMENTS:
        return 'doc'
    elif file_ext in IMAGES:
        return 'image'
    elif file_ext in AUDIO:
        return 'audio'
    elif file_ext in VIDEO:
        return 'video'
    else:
        return 'other'

def get_file_ext(filename):
    tempname, file_ext=os.path.splitext(filename)
    return file_ext[1:]

def get_hdfs_filename():
    letter=string.ascii_letters+string.digits
    return ''.join(random.sample(letter, 10))

def get_share_pass():
    letter=string.ascii_letters+string.digits
    return ''.join(random.sample(letter, 4))
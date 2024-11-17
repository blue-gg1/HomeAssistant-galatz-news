import os, re, requests, ffmpeg, logging, subprocess, shutil
import hashlib
from datetime import date, datetime, time
from requests_html import HTMLSession
from yt_dlp import YoutubeDL

URL_MAIN = 'https://www.kan.org.il/content/kan/kan-b/' # the website source 
def sha256sum(filename):
    with open(filename, 'rb', buffering=0) as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()
def md5sum(filename):
    with open(filename, 'rb', buffering=0) as f:
        return hashlib.file_digest(f, 'md5').hexdigest()

def sha512sum(filename):
    with open(filename, 'rb', buffering=0) as f:
        return hashlib.file_digest(f, 'sha512').hexdigest()

def set_time_and_date(): # set up dates that will be true when the code is run
    global today
    global this_year
    global this_month
    global this_day
    global this_hour
    global now
    now = datetime.now()
    today = date.today()
    this_year = today.year
    this_month = today.month
    this_day = today.day
    this_hour = now.strftime("%H")

def get_m3u8_url(URL_MAIN): # get the KAN site and only take the m3u8 url file
    global final_m3u8_url # define the URL globaly
    session = HTMLSession() # don't use requests use the html5 version
    source_page = session.get(URL_MAIN)
    print(source_page)
    if source_page.status_code != 200:
        logging.critical("Failed to get KAN page")
        print("no page")
    else:
        logging.info("Got KAN page")
        print("yes page")
        vidlinks = re.findall('https://(.*?).m3u8', source_page.text) # use regex to get the url 
        final_m3u8_url = "https://" + vidlinks[0] + ".m3u8" # get the full link and add the extension
        print(final_m3u8_url) # print it to make sure you are correct

def get_mp4_from_ydl(): # take the m3u8 file. download the file (as mp4 iso because KAN)
    os.chdir(abs_path_download_path) # set the dir to be the one for the new hour.
    with YoutubeDL() as ydl: # download the file
        ydl.download(final_m3u8_url)
        logging.info("Got the MP4 file.")

def mp4_to_mp3(): # take the mp4 and make it to an mp3 using ffmpeg
    # print(abs_mp3_file_path)
    if os.path.isfile(abs_mp3_file_path) is False: # catch if the mp3 has been made alredy. this is in case it has been run twice an hour.
        logging.info("The mp3 file does not exist. Making it with ffmpeg")
        ffmpeg.input(abs_mp4_file_path).output(abs_mp3_file_path).run()
    else:  
        logging.info("The mp3 file does exist. Was this run in the past hour?")
        print(abs_mp3_file_path)
        print("file is real")
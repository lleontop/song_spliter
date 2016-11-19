from pydub import AudioSegment
from pprint import pprint
from datetime import datetime
import os

FILE = "System Of A Down - Live In Armenia 2015 [HD]"
DEBUG = 0

OUT_FOLDER = FILE + '/'
FMT = '%H:%M:%S'
FILENAME = FILE + ".m4a"
if DEBUG:
    FILENAME = "./test.mp3"

def check_create_dir(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def fix_time_fmt(time):
    try:
        datetime.strptime(time, FMT)
    except ValueError:
        time = '00:' + time
    return time

check_create_dir(OUT_FOLDER)

songs = []
with open("./song_list", "r") as songlist:
    for i, line in enumerate(songlist):
        line = '%s) %s' % (i, line)
        no, time, title = line.split(' ', 2)
        songs += [(int(no.replace(')', '')), time, title.strip())]

sound = AudioSegment.from_file(FILENAME)

# mark the current splitting start
previous_mark = 0
for i, (no, start_time, title) in enumerate(songs):
    if title == "END":
        break  
    start_time = fix_time_fmt(start_time)
    end_time = fix_time_fmt(songs[i + 1][1])  
    
    tdelta = datetime.strptime(end_time, FMT) - datetime.strptime(start_time, FMT)
    song_duration = tdelta.total_seconds()
    print "Spliting %s: '%s' from %s to %s. Duration: %s" % (no, title, start_time, end_time, song_duration)
    
    song = sound[previous_mark * 1000:(previous_mark + song_duration) * 1000]
    song = song.fade_in(10)
    song = song.fade_out(10)
    previous_mark += song_duration
    if no == len(songs):
        song = song.fade_out(30)
    # lets save it
    song_tags = { 'title': title,
                  'artist': 'System of a Down',
                  'album_artist':'System of a Down',
                  'album': 'Live in Armenia',
                  'track': '%s' % no }
    
    song.export((OUT_FOLDER + "%s - %s.mp3" % (no, title)), format='mp3', tags=song_tags, id3v2_version='3', parameters=["-write_id3v1", "1"])
    if DEBUG:
        break


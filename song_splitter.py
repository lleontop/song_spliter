from pydub import AudioSegment
from pprint import pprint
from datetime import datetime
import os
import errno

DEBUG = 0
FMT = '%H:%M:%S'

def create_out_dir(directory):
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

def main(audio_file, times_file, output_folder=None):
    
    if not output_folder:
        output_folder = os.path.join(os.path.dirname(audio_file), os.path.splitext(os.path.basename(audio_file))[0])
    create_out_dir(output_folder)
    
    print "Starting times processing"    
    songs = []
    with open(times_file, "r") as songlist:
        for i, line in enumerate(songlist):
            line = '%s) %s' % (i, line)
            no, time, title = line.split(' ', 2)
            songs += [(int(no.replace(')', '')), time, title.strip())]
    
    print "End times processing. Songs found: "
    pprint(songs)

    print "Starting audio load"
    sound = AudioSegment.from_file(audio_file)
    print "End audio load"
    
    print "Starting audio processing"
    # mark the current splitting start
    previous_mark = 0
    for i, (no, start_time, title) in enumerate(songs):
        if title == "END":
            break  
        start_time = fix_time_fmt(start_time)
        end_time = fix_time_fmt(songs[i + 1][1])  
        
        tdelta = datetime.strptime(end_time, FMT) - datetime.strptime(start_time, FMT)
        song_duration = tdelta.total_seconds()
        print "Splitting %s: '%s' from %s to %s. Duration: %s" % (no, title, start_time, end_time, song_duration)
        
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
        
        song.export(os.path.join(output_folder, "%s - %s.mp3" % (no, title)), format='mp3', tags=song_tags, id3v2_version='3', parameters=["-write_id3v1", "1"])
        if DEBUG:
            break
    print "End audio processing"
    
if __name__ == '__main__':
    main()

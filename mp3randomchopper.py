#############################################
#############################################
# RANDOM SONG SLICER ########################
#############################################
# Jeronimo Barbosa ##########################
# jeronimo.costa [at] mail.mcgill.ca ########
# August 25th 2015 ##########################
#############################################

# dependencies: 
# Pydub - https://github.com/jiaaro/pydub
# please, note Pydub also depends on libav and ffmpeg

from pydub import AudioSegment
import os, math, random


#how long my excerpts are going to be (in seconds)?
duration = 30
#where my files are?
path = '/Users/jeronimo/Documents/sbcm 2015/mumt 621 - database'
#where my raw files are?
path_raw = path +'/raw';

#creating a file containg all random positions chosen
report=open('./mp3randomchopper-report.txt', 'w+')


for root, dirs, files in os.walk(path_raw, topdown=False):
    
    #selects only mp3 files
    files = [ fi for fi in files if fi.endswith(".mp3") ]
    
    #iterates over all mp3 files
    for name in files:
        file = os.path.join(root, name)
        
        print 'processing ' + file
        
        #processinf strings
        first_part = file[:len(path)+1]
        last_part  = file[len(path)+4:]
        
        print 'loading file';
        song = AudioSegment.from_mp3(file)
        
        print 'extracting excerpt';
        #pydub works in milisecs, thus
        duration_in_ms = int(duration*1000)
        #gets the last position possible for extracting an excerpt (30s before the end)
        last_possible_start_position = math.floor(song.duration_seconds - 30)
        #gets a random position
        pos = random.uniform(0, last_possible_start_position) * 1000
        #extracts the excerpt
        
        report.write(last_part)
        report.write(" duration: " + str(song.duration_seconds))
        report.write(" random pos: " + str(pos/1000.0) + "\n")
        excerpt = song[pos:pos+duration_in_ms]
            
        print 'saving new file';
        new_file = first_part + 'excerpts' + last_part;
        excerpt.export(new_file, format='mp3')        
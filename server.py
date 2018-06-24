#!/usr/bin/env python
import os
import json
from flask import Flask
from flask import Response, render_template
from flask import stream_with_context

from mutagen.easyid3 import EasyID3
from mutagen.oggvorbis import OggVorbis
import random


app = Flask(__name__)
songs_dir = 'static/music/'

def process_metadata(extension, filepath):
    """Process and return metadata of song."""
    info = {}

    # Detect filetype
    if extension == '.mp3':
        audio = EasyID3(filepath)
    elif extension == '.ogg':
        audio = OggVorbis(filepath)
    else:
        return info

    # Fetch data
    try:
        info['title'] = audio['title'][0]
    except KeyError:
        pass
    try:
        info['artist'] = audio['artist'][0]
    except KeyError:
        pass
    try:
        info['album'] = audio['album'][0]
    except KeyError:
        pass
    try:
        info['tracknumber'] = audio['tracknumber'][0]
    except KeyError:
        pass
    try:
        info['length'] = audio['length'][0]
    except KeyError:
        pass

    print info
    return info

from random import shuffle
from mutagen.mp3 import MP3 as mut_MP3
import pandas as pd
import numpy as np
import sys
import random


def pick_order(li, complexite):
    if len(li) == 1:
        return li[0]
    elif len(li) > 1:
        for number in range(0, len(li)):
            if li[number] > complexite:
                return li[number -1]
    else:
        return 0


def rest_choice(li, complexite):
    if len(li) == 1:
        return li[0]
    elif len(li) > 1:
        for number in range(0, len(li)):
            if li[number] > complexite:
                return random.choice(li[number:])
    else:
        return 0


def First_Loop(ds, songs):
    try:
        intro_index = ds[ds['trait'] == 'intro'].index[0]
        group = random.choice(['A1']) # 1:1
        sub_df = ds[(ds['complicated'] == group) & (ds['trait'] == 'verse1')]
        drum_state = np.random.choice(['beat','drum'], p=[0.99, 0.01])
        if drum_state not in sub_df['drum']:
            pass
        else:
            drum_state = sub_df['drum'][0]
        sub_df = sub_df[sub_df['drum'] == drum_state ]
        piano = random.choice(np.unique(sub_df['piano']).tolist())
        sub_df = sub_df[sub_df['piano'] == piano ]
        li = sorted(sub_df['complexite'].tolist()) # current state of complexity
        complexite_level = 0
        complexite_level = pick_order(li, complexite_level) # 60% chance
        random_choice = random.choice(li)
        complexity = np.random.choice([complexite_level, random_choice], p=[0.6, 0.4])
        verse1 = sub_df[sub_df['complexite']==complexity].index[0]
        sub_df = ds[ds['complicated'] == group]
        sub_df = sub_df[sub_df['trait'] == 'verse2']
        sub_df = sub_df[sub_df['drum'] == drum_state]
        sub_df = sub_df[sub_df['piano'] == piano]
        """
        if piano in sub_df['piano']:
            sub_df = sub_df[sub_df['piano'] == piano]
        else:
            piano = random.choice(sub_df['piano'].tolist())
            sub_df = sub_df[sub_df['piano'] == piano]
        """
        complexite_level = complexity # previous complexity
        li = sorted(sub_df['complexite'].tolist()) # current state of complexity
        complexite_level = pick_order(li, complexite_level) # 60% chance
        higher_choice = rest_choice(li, complexite_level) # 40% chance
        random_choice = random.choice(li)
        complexity = np.random.choice([complexite_level, higher_choice, random_choice], p=[0.5, 0.4, 0.1])
        verse2 = sub_df[sub_df['complexite']==complexity].index[0]
        # Outro
        outro_index = ds[ds['trait'] == 'outro'].index[0]
        # book-keeping for the next iteration
        section_length = 0
        index = [intro_index, verse1, verse2, outro_index]
        for ind in index:
            section_length += songs[ind]['length']
        history = {'group': group,
                    'drum': drum_state,
                    'piano': piano,
                    'complexity': complexity,
                    'length': section_length
                   }
        return [index, history]
    except:
        print sys.exc_info()[0], "occured."




def Loop(ds, last, songs):
    try:
        intro_index = last[0][0]
        group = random.choice(['A1','A2']) # 1:1
        sub_df = ds[(ds['complicated'] == group) & (ds['trait'] == 'verse1')]
        drum_state = np.random.choice(['beat','drum'], p=[0.99, 0.01])
        if drum_state not in sub_df['drum']:
            pass
        else:
            drum_state = sub_df['drum'][0]
        sub_df = sub_df[sub_df['drum'] == drum_state ]
        temp_sub = np.unique(sub_df['piano']).tolist()
        piano = last[1]['piano']
        if piano in temp_sub:
            temp_sub.remove(piano)
            piano = random.choice(temp_sub)
        else:
            piano = random.choice(temp_sub)
        sub_df = sub_df[sub_df['piano'] == piano ]
        li = sorted(sub_df['complexite'].tolist()) # current state of complexity
        complexite_level = 0
        complexite_level = pick_order(li, complexite_level) # 60% chance
        random_choice = random.choice(li)
        complexity = np.random.choice([complexite_level, random_choice], p=[0.6, 0.4])
        verse1 = sub_df[sub_df['complexite']==complexity].index[0]
        #verse2
        sub_df = ds[ds['complicated'] == group]
        sub_df = sub_df[sub_df['trait'] == 'verse2']
        sub_df = sub_df[sub_df['drum'] == drum_state]
        """
        if piano not in sub_df['piano']:
            piano = random.choice(sub_df['piano'].tolist())
            sub_df = sub_df[sub_df['piano'] == piano]
        else:
            sub_df = sub_df[sub_df['piano'] == piano]
        """
        sub_df = sub_df[sub_df['piano'] == piano]

        complexite_level = complexity # previous complexity
        li = sorted(sub_df['complexite'].tolist()) # current state of complexity
        complexite_level = pick_order(li, complexite_level) # 60% chance
        higher_choice = rest_choice(li, complexite_level) # 40% chance
        random_choice = random.choice(li)
        complexity = np.random.choice([complexite_level, higher_choice, random_choice], p=[0.5, 0.4, 0.1])
        verse2 = sub_df[sub_df['complexite']==complexity].index[0]
        # Outro
        outro_index = ds[ds['trait'] == 'outro'].index[0]
        # book-keeping for the next iteration
        section_length = 0
        index = [intro_index, verse1, verse2, outro_index]
        for ind in index:
            section_length += songs[ind]['length']
        history = ({'group': group,
                    'drum': drum_state,
                    'piano': piano,
                    'complexity': complexity,
                    'length': section_length,
                   })
        return [index, history]
    except:
        print sys.exc_info()[0], "occured."



def machine(ds, songs):
    try:
        k = First_Loop(ds, songs)
        while k == None:
            k = First_Loop(ds, songs)
        number = 0
        print k
        PL = []
        PL = PL + k[0]
        while number < 500:
            ite = Loop(ds, k, songs)
            while ite == None:
                ite = Loop(ds, k, songs)
            PL = PL + ite[0]
            number = number + ite[1]['length']
            k = ite
        return PL
    except:
        print sys.exc_info()[0], "occured."


def get_songs(rootdir, extensions=['.mp3', '.ogg']):
    """Return songs of specified type in rootdir."""
    songs = []
    jplayer_types = {
        '.mp3': 'mp3',
        '.m4a': 'm4a',
        '.m4v': 'm4v',
        '.webm': 'webma',
        '.ogg': 'oga',
        '.flv': 'fla',
         '.wav': 'wav',
     }

    for root, dirs, files in os.walk(rootdir):

        # once reload, the order of playlist is uniformly shuffled.
        shuffle(files)

        for file in files:
            extension = os.path.splitext(file)[1]

            # add more conditions to the playlist
            # to be done

            if extension in extensions:
                path_inside = os.path.join(root, file)

                song = {
                    'extension': extension,
                    'type': jplayer_types[extension],
                    'folder': root,
                    'filename': file,
                    'filepath': path_inside,
                    'length': mut_MP3(path_inside).info.length,
                }
                song.update(process_metadata(extension, song['filepath']))
                songs.append(song)

    ds = pd.DataFrame(songs)


    def instrument(s):
        start = s.find('(') + 1
        end = s.find(')', start)
        return s[start:end].split(', ')

    ds['trait'] = ds['filename'].apply(lambda x: x.split('-')[0])
    ds['number'] = ds['filename'].apply(lambda x: x.split('-')[1].split(' ')[0])
    ds['instrument'] = ds['filename'].apply(lambda x: instrument(x))
    ds['complicated'] = ds['instrument'].apply(lambda x: 'A2' if x[-1] == 'c' else 'A1')
    ds['drum'] = ds['instrument'].apply(lambda x: 'drum' if 'Drum' in x else 'beat')
    ds['piano'] = ds['instrument'].apply(lambda x: x[0])
    ds['complexite'] = ds['instrument'].apply(lambda x: len(x))

    """
    new_song = []
    for so in songs:
        if 'French' in so['filename']:
            pass
        else:
            new_song.append(so)
            print so['filename']
            print so['length']
    """
    new_song = machine(ds, songs)
    playsong = []
    for noon in new_song:
        playsong.append(songs[noon])

    # return a playlist
    # return songs
    return playsong


def prepare_jplayer_songs(songs):
    """Take a dictionary of songs and make a list of json jplayer strings
    from it."""
    jp_songs = []
    for song in songs:
        jp_song = {
            'title': song['filename'],
            song['type']: song['filepath'],
        }
        jp_songs.append(json.dumps(jp_song))
    return jp_songs

"""
import time
from mutagen.mp3 import MP3

def stream_template(template_name, **context):
    # http://flask.pocoo.org/docs/patterns/streaming/#streaming-from-templates
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    # uncomment if you don't need immediate reaction
    ##rv.enable_buffering(5)
    return rv

@app.route('/')
def home():
    def generate_output():
        while True:

            songs = get_songs(songs_dir)

            #audio = MP3(song.filepath)
            #print audio.info.length
            #audio_sleep_time = audio.info.length

            jp_songs = prepare_jplayer_songs(songs)
            context = {
                'songs_dir': songs_dir,
                'songs': songs,
                'jp_songs': jp_songs,
            }
            yield context

            time.sleep(30)

    return Response(stream_template('home.html', context = context))

"""
@app.route('/')
def home():
    songs = get_songs(songs_dir)
    jp_songs = prepare_jplayer_songs(songs)
    context = {
        'songs_dir': songs_dir, 
        'songs': songs,
        'jp_songs': jp_songs,
    }
    return render_template('home.html', **context)


@app.route('/library.m3u8')
def playlist():
    body = render_template('playlist.m3u8', songs=get_songs(songs_dir))
    response = Response(body, mimetype='audio/x-mpegurl')
    return response

if __name__ == '__main__':
    app.run(debug=True)

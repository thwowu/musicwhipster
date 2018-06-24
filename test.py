jplayer_types = {
    '.mp3': 'mp3',
    '.m4a': 'm4a',
    '.m4v': 'm4v',
    '.webm': 'webma',
    '.ogg': 'oga',
    '.flv': 'fla',
    '.wav': 'wav',
}


song1 = {'extension': '.mp3',
        'type': jplayer_types['.mp3'],
        'folder': "1",
        'filename': "verse1-12 (Piano2, Violin).mp3",
        'length': 15.1212,
         }

song2 = {'extension': '.mp3',
        'type': jplayer_types['.mp3'],
        'folder': "1",
        'filename': "verse1-25 (HarpPiano3, Beat, Beap, Violin).mp3",
        'length': 25.1212,
         }

song3 = {'extension': '.mp3',
        'type': jplayer_types['.mp3'],
        'folder': "1",
        'filename': "verse1-43 (FeltChordPiano, Oboe, Seely, Drum, Beap, Violin, Cloud, c).mp3",
        'length': 15.1212,
        }

song4 = {'extension': '.mp3',
        'type': jplayer_types['.mp3'],
        'folder': "1",
        'filename': "verse2-34 (Piano3Harp, HighHarp, Oboe, Seely, Drum, Beap, Violin, Cloud, c).mp3",
        'length': 10.1212,
        }

song5 = {'extension': '.mp3',
        'type': jplayer_types['.mp3'],
        'folder': "1",
        'filename': "intro-1 (Cloud).mp3",
        'length': 7.2,
        }

song6 = {'extension': '.mp3',
        'type': jplayer_types['.mp3'],
        'folder': "1",
        'filename': "verse1-30 (Harp, c).mp3",
        'length': 11.2,
        }

song7 = {'extension': '.mp3',
        'type': jplayer_types['.mp3'],
        'folder': "1",
        'filename': "outro-1 (Cloud).mp3",
        'length': 11.2,
        }

song8 = {'extension': '.mp3',
        'type': jplayer_types['.mp3'],
        'folder': "1",
        'filename': "verse2-3 (Piano1, Oboe, Seely, Beap, Violin, Cloud).mp3",
        'length': 25.1212,
        }

song9 = {'extension': '.mp3',
        'type': jplayer_types['.mp3'],
        'folder': "1",
        'filename': "verse2-3 (Piano2, Beat, Violin, Cloud, c).mp3",
        'length': 222.1212,
        }



songs = [song1, song2, song3, song4, song5, song6, song7, song8, song9]



import pandas as pd
import numpy as np

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


# lambda x: x*10 if x<2 else (x**2 if x<4 else x+10)


"""
L = ['NAD','BAM']
i, j = (df.applymap(lambda x: str(x).startswith(tuple(L)))).values.nonzero()
t = list(zip(i, j))
print (t)

[(0, 2), (1, 2)]


---

df = pd.DataFrame([[947.2, 1.25, 'BAM 1.25'],
                   [129.3, 2.1, 'NAD 1.25'],
                   [161.69, 0.8, 'CAD 2.00']],
                  columns=['Price', 'Rate p/lot', 'Total Comm'])
                  
res = list(map(tuple, np.argwhere(np.logical_or.reduce(\
      [df.values.astype('<U3') == i for i in np.array(['BAM', 'NAD'])]))))
"""

"""

res = list(map(tuple, np.argwhere(np.logical_or.reduce(\
      [ds.values == i for i in np.array(['intro', 'verse1'])]))))

"""


# pick up & append into the first element
intro_index = ds.loc[ds['trait'] == 'intro'].index[0]


# pick the verse 1

# A1 or A2 by uniform
group = random.choice(['A1','A2']) # 1:1
sub_df = ds[(ds['complicated'] == group) & (ds['trait'] == 'verse1')]

# drum or beat
drum_state = np.random.choice(['beat','drum'], p=[0.8, 0.2])
sub_df = sub_df[sub_df['drum'] == drum_state ]

# which piano
piano = random.choice(np.unique(sub_df['piano']).tolist())
sub_df = sub_df[sub_df['piano'] == piano ]

# after choosing piano, choose the complexity of tracks

complexite_level = 0 # previous complexity
li = sorted(sub_df['complexite'].tolist()) # current state of complexity


# check the closest level in the current set
complexite_level = pick_order(li, complexite_level) # 60% chance

# Jump to higher complexity composition set
higher_choice = rest_choice(li, complexite_level) # 40% chance
random_choice = random.choice(li)
complexity = np.random.choice([complexite_level, higher_choice, random_choice], p=[0.5, 0.4, 0.1])

# transform back to index position to call the song & append
verse1 = sub_df[sub_df['complexite']==complexity].index[0]



# pick the verse 2

sub_df = ds[(ds['complicated'] == group) &
            (ds['trait'] == 'verse2') &
            (ds['drum'] == drum_state) &
            (ds['piano'] == piano)]

complexite_level = complexity # previous complexity
li = sorted(sub_df['complexite'].tolist()) # current state of complexity

complexite_level = pick_order(li, complexite_level) # 60% chance
higher_choice = rest_choice(li, complexite_level) # 40% chance
random_choice = random.choice(li)
complexity = np.random.choice([complexite_level, higher_choice, random_choice], p=[0.5, 0.4, 0.1])

verse2 = sub_df[sub_df['complexite']==complexity].index[0]

# Outro
outro_index = ds.loc[ds['trait'] == 'outro'].index[0]

# book-keeping for the next iteration

history = []
section_length = 0
index = [intro_index, verse1, verse2, outro_index]
for ind in index:
    section_length += songs[ind]['length']

history.append({'group': group,
            'drum': drum_state,
            'piano': piano,
            'complexity': complexity,
            'length': section_length,
           })


# ds.loc[ds['trait'] == 'outro']
# https://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas

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


def First_Loop(ds):
    try:
        intro_index = ds[ds['trait'] == 'intro'].index[0]
        group = random.choice(['A1','A2']) # 1:1
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
        if piano not in sub_df['piano']:
            piano = random.choice(sub_df['piano'].tolist())
            sub_df = sub_df[sub_df['piano'] == piano]
        else:
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
        print(sys.exc_info()[0], "occured.")
        print(sub_df)
        print([group,drum_state,piano,complexity])




def Loop(ds, last):
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
        if piano not in sub_df['piano']:
            piano = random.choice(sub_df['piano'].tolist())
            sub_df = sub_df[sub_df['piano'] == piano]
        else:
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
        print(sys.exc_info()[0], "occured.")
        print(sub_df)
        print([group,drum_state,piano,complexity])


def machine(ds):
    k = First_Loop(ds)
    number = 0
    PL = []
    PL += k[0]
    while number < 500:
        ite = Loop(ds, k)
        PL += ite[0]
        number += ite[1]['length']
        k = ite
    return PL

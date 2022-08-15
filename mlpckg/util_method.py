import pandas as pd
from tqdm import tqdm 
from haversine import haversine

def latlontogps(frame):
    frame.Latitude = frame.Latitude.astype(float)
    frame.Longitude = frame.Longitude.astype(float)

    frame_gps = []
    for i in tqdm(range(len(frame))):
        frame_gps.append( (frame.Latitude[i], frame.Longitude[i]) )
        
    frame['gps'] = frame_gps

    return frame



def remove_sp(frame):
    sp_idx = []
    for i in range(len(frame)):
        if 'sp.' in frame.Species[i]:
            sp_idx.append(i)
    frame= frame.drop(sp_idx).reset_index(drop=True)

    under_30 = []
    for i in range(len(frame.Species.value_counts())):
        if frame.Species.value_counts()[i]<30:
            under_30.append(frame.Species.value_counts().index[i])
            
    drop_30 = []
    for i in tqdm(range(len(frame.Species))):
        for j in under_30:
            if frame.Species[i] == j:
                drop_30.append(i)        
    frame= frame.drop(drop_30).reset_index(drop=True)            
                
    one_letter = []
    for i in frame.Species.value_counts().index:
        if len(i.split(' ')) == 1:
            one_letter.append(i)    
            
    drop_one = []
    for i in tqdm(range(len(frame.Species))):
        for j in one_letter:
            if frame.Species[i] == j:
                drop_one.append(i)        
    frame = frame.drop(drop_one).reset_index(drop=True)

    print("final species length:",len(frame.Species.unique()))

    return frame


def dropdup(frame):
    print("frame length:", len(frame))
    frame = frame[frame.public_positional_accuracy<=1000].reset_index(drop=True)
    frame = frame[(frame.Latitude!=0.0)&(frame.Longitude!=0.0)].reset_index(drop=True)
    frame = frame[['Source','State','Year','Species','Latitude','Longitude','public_positional_accuracy']].drop_duplicates(['Year','Species','Latitude','Longitude'],keep='first').reset_index(drop=True)
    print("frame length after eda:", len(frame))

    return frame






def select_key(num:int):
    no = num

    if no == 1:
        target_species = 'Coccinella novemnotata'
        key = 'novem'

    elif no == 2:
        target_species = 'Coccinella transversoguttata'
        key = 'trans'

    elif no == 3:
        target_species = 'Adalia bipunctata'
        key = 'bipun'

    elif no == 4:
        target_species = 'Hippodamia parenthesis'
        key = 'paren'

    return target_species,key
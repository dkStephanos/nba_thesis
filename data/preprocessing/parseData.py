import pandas as pd	
import numpy as np	
import sys

import matplotlib.pyplot as plt	
import seaborn as sns	

from IPython.display import IFrame	
import easygui

from utilities.GraphUtil import GraphUtil
from utilities.FeatureUtil import FeatureUtil
from utilities.DataUtil import DataUtil

# Load game with GUI
#game_path = easygui.fileopenbox(default="C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/", title="Select a game file")
#game_df = DataUtil.load_game_df(game_path)

#easygui.msgbox("Next select corresponding annotation file")
#annotation_path = easygui.fileopenbox(default="C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/", title="Select an annotation file")
#annotation_df = DataUtil.load_annotation_df(annotation_path)

game_df = DataUtil.load_game_df(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\static\data\game_raw_data\12.11.2015.GSW.at.BOS\0021500336.json")

players_data = DataUtil.get_players_data(game_df)
print(players_data)

annotation_df = DataUtil.load_annotation_df(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\static\data\event_annotations\events-20151211GSWBOS.csv")

annotation_df = DataUtil.trim_annotation_rows(annotation_df)
annotation_df = FeatureUtil.determine_possession(annotation_df)
annotation_df = DataUtil.generate_event_ids(annotation_df)

annotation_df = DataUtil.trim_annotation_cols(annotation_df)
combined_event_df = DataUtil.combine_game_and_annotation_events(game_df, annotation_df)
#combined_event_df.to_csv("static/data/test/events.csv")

# Get direction for each play, and remove moments occuring on the other half of the court
combined_event_df = FeatureUtil.determine_directionality(combined_event_df)
combined_event_df = DataUtil.trim_moments_by_directionality(combined_event_df)

sample_event = DataUtil.load_combined_event_by_num(combined_event_df, 4)
print(sample_event)
moments_df = DataUtil.get_moments_from_event(sample_event)
#moments_df.to_csv("static/data/test/test.csv")
print(len(moments_df))
event_passes = FeatureUtil.get_passess_for_event(moments_df, sample_event["possession"], players_data)
print(event_passes)
dribble_handoff_candidates = FeatureUtil.get_dribble_handoff_candidates(combined_event_df, moments_df, event_passes)
print("Hand off candidates")
print(dribble_handoff_candidates)

# get ball movements for event and graph them
ball_df = moments_df[moments_df.player_id==-1]
GraphUtil.plot_player_movement(ball_df)
ball_df = moments_df[moments_df.player_id==2738]
GraphUtil.plot_player_movement(ball_df)

all_candidates = []
succesful = 0
failed = 0
for index, event in combined_event_df.iterrows():
    try:
        moments_df = DataUtil.get_moments_from_event(event)
        event_passes = FeatureUtil.get_passess_for_event(moments_df, event["possession"], players_data)
        dribble_handoff_candidates = FeatureUtil.get_dribble_handoff_candidates(combined_event_df, moments_df, event_passes)
        all_candidates += dribble_handoff_candidates
        succesful += 1
    except:
        print("Issue at index: " + str(event['EVENTNUM']), sys.exc_info()[0])
        failed += 1
    #break

all_candidates = [i for n, i in enumerate(all_candidates) if i not in all_candidates[n + 1:]]
print("Number of candidates parsed: " + str(len(all_candidates)) + "\nSuccessful events: " + str(succesful) + "\nFailed events: " + str(failed))

canidate_df = pd.DataFrame(all_candidates)
canidate_df.to_csv('static/data/test/candidates.csv')
import pandas as pd	
import numpy as np	

import matplotlib.pyplot as plt	
import seaborn as sns	

from IPython.display import IFrame	
import easygui

from utilities.VisualizationUtil import VisualizationUtil as VisUtil
from utilities.FeatureUtil import FeatureUtil
from utilities.DataUtil import DataUtil

# Load game with GUI
#game_path = easygui.fileopenbox(default="C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/game_raw_data/", title="Select a game file")
#game_df = DataUtil.load_game_df(game_path)

#easygui.msgbox("Next select corresponding annotation file")
#annotation_path = easygui.fileopenbox(default="C:/Users/Stephanos/Documents/Dev/NBAThesis/NBA_Thesis/static/data/event_annotations/", title="Select an annotation file")
#annotation_df = DataUtil.load_annotation_df(annotation_path)

game_df = DataUtil.load_game_df(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\static\data\game_raw_data\12.11.2015.GSW.at.BOS\0021500336.json")
print(game_df.head())
print(game_df.shape)

annotation_df = DataUtil.load_annotation_df(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\static\data\event_annotations\events-20151211GSWBOS.csv")

game_data = DataUtil.get_game_data(game_df, annotation_df)
print(game_data)

annotation_df = annotation_df.loc[annotation_df["EVENTMSGTYPE"].isin([1,2,5,6])]
print(annotation_df.shape)


curr_event = DataUtil.load_event_by_num(game_df, "196")	
moments_df = DataUtil.get_moments_from_event(curr_event)
#moments_df.to_csv("static/data/test/test.csv")

#players_dict = DataUtil.get_players_df(curr_event)
#print(players_dict)

#ball_distances = FeatureUtil.distance_between_ball_and_players(moments_df)
#print(ball_distances.head())
#ball_dist_df = DataUtil.convert_labled_series_to_df('player_id', 'ball_distances', ball_distances)
#min_dist_df = DataUtil.get_labled_mins_from_df(ball_dist_df, 'dist_from_ball')

#min_dist_df.loc[min_dist_df['dist_from_ball'] > 3.0, 'player_id'] = pd.NA

#print(min_dist_df.shape)
#print(min_dist_df)

#min_dist_df.to_csv('static/data/test/ball_handler.csv')
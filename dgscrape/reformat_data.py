import pandas as pd
import numpy as np
import os

players_dataframe = pd.read_csv('./dgscrape/DiscGolfRankings.csv')
players_dataframe['Effective Date'] = pd.to_datetime(players_dataframe['Effective Date'])
players_dataframe = players_dataframe.pivot_table(index='Effective Date', columns='player_name', values='Rating')
players_dataframe = players_dataframe.sort_values('Effective Date')
players_dataframe = players_dataframe.loc['1998-01-01':]
players_dataframe = players_dataframe.ffill().where(players_dataframe.bfill().notnull())
all_players_dataframe = players_dataframe.copy()
#Get Players in top 10

players_in_top_x = set([])
for index, row in players_dataframe.iterrows():
    print(f'Getting top x for date {index}')
    top_x = 10
    top_x_players = row.sort_values(ascending=False)[0:top_x].index
    [players_in_top_x.add(player) for player in top_x_players]
    final_top_x = top_x_players 
    #Set all values not in top 10 to Nan
    replace_val = np.nan
    players_dataframe.loc[index, players_dataframe.columns.difference(top_x_players)] = replace_val

#Drop all columns with players never in top 10
players_dataframe = players_dataframe.dropna(axis=1, how='all')

players_dataframe = players_dataframe.transpose()

final_top_x_dataframe = all_players_dataframe[list(final_top_x)].transpose()
all_players_dataframe = all_players_dataframe[list(players_in_top_x)].transpose()
final_top_x_dataframe.to_csv(f'./dgscrape/Last{top_x}WholeHist.csv')
all_players_dataframe.to_csv(f'./dgscrape/Top{top_x}WholeHist.csv')
players_dataframe.to_csv(f'./dgscrape/Top{top_x}Formatted.csv')




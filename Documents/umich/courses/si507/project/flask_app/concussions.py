import pandas as pd
#Documentation: https://networkx.org/, suggested by chatgpt and read up on it here
import networkx as nx
import matplotlib.pyplot as plt
import itertools
from flask import Flask, render_template, request, jsonify
from itertools import chain

concussions = pd.read_csv('ConcussionInjuries2012-2014.csv')
stats = pd.read_csv('team_stats_2003_2023.csv')

class Concussions:
	def __init__(self, concussions_df, stats_df):
		self.concussions = concussions_df
		self.stats = stats_df
		self.G = nx.Graph()

	def preprocess(self):
		#extract columns i want
		self.player_info = self.concussions[['Player', 'Team','Date', 'Position','Weeks Injured', 'Games Missed', 'Play Time After Injury', 'Average Playtime Before Injury']].copy()
		#extract numerical values from strings
		self.player_info['Play Time After Injury'] = self.player_info['Play Time After Injury'].str.extract(r'(\d+)').astype(float)
		self.player_info['Average Playtime Before Injury'] = self.player_info['Average Playtime Before Injury'].str.extract(r'(\d+)').astype(float)
		#calc number of concussions for each player, as number of times they appear 
		self.player_info['Concussions'] = 1
		self.player_info['Concussions'] = self.player_info.groupby('Player')['Concussions'].transform('count')
		#add all concussion dates as a list of each occurence for each player
		self.player_info['Year'] = pd.to_datetime(self.player_info['Date'], format='%d/%m/%Y').dt.year
		self.player_info['Concussion Years'] = self.player_info.groupby('Player')['Year'].transform(lambda x: list(x))
		#aggregate functions
		self.player_info = self.player_info.groupby(['Player','Position']).agg({
			'Concussions': 'first',
			'Team': lambda x: list(set(x)),
			'Date': 'first',
			'Weeks Injured': 'sum',
			'Games Missed': 'sum',
			'Play Time After Injury': 'mean',
			'Average Playtime Before Injury': 'mean',
			'Concussion Years': 'first'
		})
		self.player_info.reset_index(inplace=True)
		
		self.stats = self.stats[['year', 'team', 'wins', 'losses', 'win_loss_perc']].copy()
		

	#chatgpt helped, asked how to build network with nodes and edges, based on player positions and number of concussions
	def network(self):
		#https://stackoverflow.com/questions/13698352/storing-and-accessing-node-attributes-python-networkx
		for idx, data in self.player_info.iterrows():
			player = data['Player']
			teams = data['Team']
			self.G.add_node(player, team=data['Team'], position=data['Position'], concussions=data['Concussions'], years=data['Concussion Years'], weeks_injured=data['Weeks Injured'], games_missed=data['Games Missed'], play_after=data['Play Time After Injury'], play_before=data['Average Playtime Before Injury'], )
			for team in teams:
				players = self.player_info[self.player_info['Team'].apply(lambda x: team in x)]['Player'].tolist()
				for other in players:
					if other != player:
						self.G.add_edge(player, other)
		
		
		return self.G

	
	def visualize(self):
		pos = nx.spring_layout(self.G)
		nx.draw(self.G, pos, with_labels= True)
		plt.show()



def main():
	concussion_analyzer = Concussions(concussions, stats)
	concussion_analyzer.preprocess()
	network = concussion_analyzer.network()
	already_seen = []
	for node in network.nodes:
		team = network.nodes[node]['team'][0]
		if team not in already_seen:
			players = list(set(chain(*network.edges(node))))
			already_seen.append(team)
	print(concussion_analyzer.stats)
		
	

if __name__ == "__main__":
    main()


	
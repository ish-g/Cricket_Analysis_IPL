import pandas as pd
import numpy as np


class Myclass:
    def __init__(self):
        self.list1 = None
        self.df = pd.read_csv('all_season_summary.csv')
        self.df1 = pd.read_csv('all_season_details.csv', low_memory=False)
        self.batter_df = pd.read_csv('all_season_batting_card.csv')
        self.player_played_dict = {}

    def seasons(self):  # 1- all seasons list for drop down
        temp_df = self.df['season']
        return temp_df.unique().tolist()

    def season_detail(self, i):  # 2- dataframe contain details of that season
        temp_df = self.df[['season', 'home_team']]
        list1 = sorted(temp_df[temp_df['season'] == i]['home_team'].unique())
        list2 = ', '.join(list1)
        var1 = len(temp_df[temp_df['season'] == i])
        temp_df1 = pd.DataFrame({'teams_name_played this_season': [list2],
                                 'total_matches': [var1]}, index=[int(i)])
        return temp_df1

    def teams_name(self):  # 3- Give all teams name with short name dataframe
        teams = self.df['name'].value_counts().index.tolist()
        teams = [i.split(" v ") for i in teams]

        l1 = sorted(list(set([j for i in teams for j in i])))
        l1_remove = ['Delhi Daredevils', 'Kochi Tuskers Kerala', 'Rising Pune Supergiants']
        l1 = [i for i in l1 if i not in l1_remove]
        l2 = ['CSK', 'DC', 'DD', 'GL', 'GT', 'KXIP', 'KKR', 'LSG', 'MI', 'PWI', 'PBKS', 'RR', 'RPS', 'RCB', 'SRH']

        teams = {}
        for i in np.arange(15):
            teams[l1[i]] = l2[i]

        teams = pd.DataFrame(list(teams.items()), columns=['IPL Teams', 'Abb.']).set_index('IPL Teams')
        return teams

    def total_matches_played_teams(self):  # 4- Dataframe of teams total matches played till yet
        temp_df = self.df[['season', 'home_team', 'away_team']]
        temp_df = (temp_df.groupby('home_team')['season'].count() + temp_df.groupby('away_team')[
            'season'].count()).to_frame().transpose()
        temp_df.index = ['total_matches']
        return temp_df

    def win_pct(self):  # 5- bar chart tells wins pct of every team
        teams = self.df1.groupby('current_innings')
        t1_dic = teams.nunique()['match_id'].to_dict()
        dict1 = self.df.groupby('winner')['away_team'].count().to_dict()
        q2_d = {}
        for key in dict1:
            q2_d[key] = round(dict1[key] / (t1_dic[key] - dict1[key]), 1)
        q2 = pd.DataFrame(list(q2_d.items()), columns=['team', 'w/l_ratio']).sort_values(by='w/l_ratio',
                                                                                         ascending=False)
        return q2

    def avg_run_teams(self):  # 6- bar chart of avg runs of every team
        temp_df = self.df1[['current_innings', 'match_id', 'runs']]
        result = round(temp_df.groupby(['current_innings', 'match_id'])['runs'].sum().unstack().mean(axis=1),
                       1).reset_index().rename(columns={'current_innings': 'team', 0: 'avg_run'})
        result1 = round(temp_df.groupby(['current_innings', 'match_id'])['runs'].sum().unstack().mean(axis=1),
                        1).to_frame().transpose()
        result1.index = ['avg_runs']
        return result, result1

    def highest_run(self):  # 7- Highest Run scored by a team st.metrics
        temp_df = self.df1[['match_id', 'innings_id', 'runs']]
        temp_df1 = temp_df.groupby(['match_id', 'innings_id'])['runs'].sum().reset_index().sort_values(by='runs',
                                                                                                       ascending=False).head(
            1)
        q7 = self.df1.loc[(self.df1['match_id'] == temp_df1['match_id'].iloc[0]) & (
                self.df1['innings_id'] == temp_df1['innings_id'].iloc[0])].iloc[0, [1, 3, 4]]
        return temp_df1['runs'].iloc[0], q7['home_team'], q7['season']

    def players_list(self):  # 8- Return a list and a dict of all players who played in ipl
        temp_df = self.df1.groupby(['batsman1_name', 'current_innings']).size().reset_index(level=1).drop(
            columns=0).rename(columns={'current_innings': 'teams'})
        for i in list(set(temp_df.index.tolist())):
            self.player_played_dict[i] = [y for x in temp_df.loc[i].values.reshape(1, -1) for y in x]
        self.list1 = list(self.player_played_dict.keys())
        return self.list1

    def player_total_score(self, i):  # 9- player total score till yet
        temp_df1 = self.df1[(self.df1['isWide'] == False) & (self.df1['isNoball'] == False)].iloc[:, :19]
        temp_df2 = temp_df1.groupby(['batsman1_id', 'batsman1_name'])['runs'].sum().reset_index().sort_values(by='runs',
                                                                                                              ascending=False)
        return temp_df2.rename(columns={'runs': 'total_run'}).loc[temp_df2['batsman1_name'] == i][
            ['batsman1_name', 'total_run']].set_index('batsman1_name')['total_run']

    def player_played_in_teams(self, i):  # 10- player played in teams
        return self.player_played_dict[i]

    def runs_distribution(self):  # 11- distribution of runs in every inning
        temp_df = self.df1[['match_id', 'innings_id', 'runs']]
        temp_df = temp_df.groupby(['match_id', 'innings_id'])['runs'].sum().unstack()
        temp_df.columns.name = None
        return temp_df

    def boundary_run_pct(self):  # 12- pie chart of percentage of run come from boundaries in a match
        temp_df = self.df1[['isBoundary', 'runs']]
        total_run = temp_df['runs'].sum()
        boundaries_run = temp_df[temp_df['isBoundary'] == True]['runs'].sum()
        boundary_pct = round(boundaries_run / total_run * 100)
        return boundary_pct

    def batter_list(self):  # 13- return batsman name list
        temp_df = self.batter_df['fullName']
        return temp_df.sort_values().unique().tolist()

    def batter_info(self, i):  # 14- batsman matches played in every season
        df = self.batter_df[['fullName', 'match_id', 'season', 'runs', 'fours', 'sixes', 'ballsFaced']]
        matches_p_season = df[(df['fullName'] == i)].groupby('season')['match_id'].count().sort_index(
            ascending=False).rename('matches')
        runs_p_season = df[(df['fullName'] == i)].groupby('season')['runs'].sum().sort_index(
            ascending=False).astype('int')
        balls_faced = df[(df['fullName'] == i)].groupby('season')['ballsFaced'].sum().sort_index(
            ascending=False).astype('int')
        strike_rate = ((runs_p_season / balls_faced) * 100).rename('strike rate').astype(int)
        total_4 = df[(df['fullName'] == i)].groupby('season')['fours'].sum().sort_index(
            ascending=False).astype('int')
        total_6 = df[(df['fullName'] == i)].groupby('season')['sixes'].sum().sort_index(
            ascending=False).astype('int')
        return pd.concat([matches_p_season, runs_p_season, strike_rate, total_4, total_6], axis=1)

    def players_sr(self):  # 15- players strike rate
        df = self.batter_df[['fullName', 'runs', 'ballsFaced']]
        players_list = df.groupby('fullName')['runs'].sum().sort_values(ascending=False).iloc[:150].index.tolist()
        runs = df.groupby('fullName')['runs'].sum()
        balls = df.groupby('fullName')['ballsFaced'].sum()
        strike_rate = ((runs / balls) * 100).round().rename('strike rate').sort_values(ascending=False)
        return strike_rate.sort_values(ascending=False).loc[players_list]

    def players_sr(self):  # 16- plotly strike rate of batsman
        df = self.batter_df[['fullName', 'runs', 'ballsFaced']]
        players_list = df.groupby('fullName')['runs'].sum().sort_values(ascending=False).iloc[:150].index.tolist()
        runs = df.groupby('fullName')['runs'].sum()
        balls = df.groupby('fullName')['ballsFaced'].sum()
        strike_rate = ((runs / balls) * 100).round().rename('strike rate').sort_values(ascending=False)
        return strike_rate.loc[players_list].sort_index(ascending=True)

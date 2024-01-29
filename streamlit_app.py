import streamlit as st
import analysis as an
import matplotlib.pyplot as plt
obj1 = an.Myclass()

st.set_page_config(layout="wide")

def set_custom_theme():
    st.markdown("""
        <style>
            .stApp {
                background-color: #ffffff;
                color: #333333;
            }
            .stTextInput > div > div {
                background-color: #000000;
            }
        </style>
    """, unsafe_allow_html=True)

set_custom_theme()

options = ['About', 'Season Wise Stats', 'Team Performance', 'Player Statistics', 'Match Insights',
           'Batsman Performance', 'Bowler Performance']
st.sidebar.header('''
    Welcome to IPL Statistics DashBoard
    ''')
user_input = st.sidebar.radio('Select the Performance type', options, index=0)

if user_input == 'About':
    col51, col52 = st.columns(2)
    with col52:
        st.subheader("All Teams")
        st.table(obj1.teams_name())  # 3
    with col51:
        st.header('Introduction to the Indian Premier League (IPL) and Project Overview')
        '''The Indian Premier League (IPL) stands as a pinnacle in the world of cricket, blending sportsmanship, entertainment, and fervent competition into a thrilling extravaganza. Launched in 2008 by the Board of Control for Cricket in India (BCCI), the IPL revolutionized the landscape of cricket by introducing a franchise-based Twenty20 format, transcending geographical boundaries to unite players from across the globe.'''
        '''With its electrifying atmosphere, star-studded lineups, and nail-biting matches, the IPL has captured the hearts of millions worldwide, becoming one of the most-watched sporting events annually. Beyond the boundaries of the cricket field, the IPL has also become a platform for budding talents to showcase their skills, while seasoned veterans continue to dazzle audiences with their prowess.'''

    st.header('Project Overview: IPL Stats')
    st.write('''In the vast ocean of IPL's captivating moments and statistical milestones, Ishwar's project emerges as a beacon for cricket enthusiasts and data aficionados alike. This meticulously crafted project delves into the wealth of statistical data generated by IPL matches, offering insights, trends, and analyses that unravel the intricacies of the game.''')

    st.write('''Ishwar's project serves as a comprehensive repository, presenting a treasure trove of statistical information encompassing player performances, team dynamics, match outcomes, and historical trends. Through meticulous data collection and insightful visualization techniques, this project paints a vivid portrait of the IPL's evolution over the years, highlighting standout players, record-breaking feats, and the pulse-pounding drama that defines this cricketing spectacle.''')

    st.write('''From batting averages to bowling economy rates, from match-winning innings to game-changing spells, Ishwar's project leaves no statistical stone unturned, providing cricket enthusiasts with a deep dive into the numbers behind the IPL's glitz and glamour. Whether you're a die-hard fan seeking to relive iconic moments or a data enthusiast unraveling the patterns of success, this project promises to be an invaluable resource, encapsulating the essence of the IPL through the lens of statistical analysis.''')

if user_input == 'Season Wise Stats':
    season_input = st.selectbox('Select season', obj1.seasons())  # 1
    st.table(obj1.season_detail(season_input))  # 2

if user_input == 'Team Performance':

    st.header("Matches played by each team in IPL")
    st.table(obj1.total_matches_played_teams())  # 4

    st.header('Win-Loss Ratio')
    st.bar_chart(obj1.win_pct(), x='team', y='w/l_ratio')  # 5

    st.subheader('Average run per match')
    x, y = obj1.avg_run_teams()  # 6
    st.dataframe(y)
    st.bar_chart(x, x='team', y='avg_run')


if user_input == 'Player Statistics':
    players = obj1.players_list()  # 8
    i = st.selectbox("Select a player", [""] + players)

    if i:
        col31, col32 = st.columns(2)
        with col31:
            st.write('Total scored in all matches till yet!')
            st.write(obj1.player_total_score(i))  # 9

        with col32:
            formatted_list = "\n".join([f"- {item}" for item in obj1.player_played_in_teams(i)])  # 10
            st.markdown(f"Played in teams:\n{formatted_list}")
    else:
        pass

if user_input == 'Match Insights':
    col41, col42 = st.columns(2)
    with col41:
        st.caption('Highest scored match')
        x, y, z = obj1.highest_run()  # 7
        st.metric(label=y, value=x, delta=z)
    with col42:
        st.caption('Average of runs come from boundaries in percentage')
        sizes = [obj1.boundary_run_pct(), 100-obj1.boundary_run_pct()]  # 12
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.pie(sizes, labels=['% of runs by boundaries', '% of runs by not boundaries'], autopct='%0.1f%%')
        st.pyplot(fig)

    col21, col22 = st.columns(2)
    with col21:
        st.caption('Runs distribution in inning 1')
        data1 = obj1.runs_distribution()[1]  # 11
        fig1, ax1 = plt.subplots()
        ax1.hist(data1, bins=30, color="skyblue", edgecolor="black")
        plt.xlabel("Value")
        plt.ylabel("score")
        st.pyplot(fig1)

    with col22:
        st.caption('Runs distribution in inning 2')
        data2 = obj1.runs_distribution()[2]  # 11
        fig2, ax2 = plt.subplots()
        ax2.hist(data2, bins=30, color='red', edgecolor='black')
        plt.xlabel("Value")
        plt.ylabel("score")
        st.pyplot(fig2)

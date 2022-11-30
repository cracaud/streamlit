import pandas as pd
import streamlit as st

st.set_page_config(page_title="LNB Stats",
                   page_icon=":basketball:",
                   layout="wide"
)

#DATA
url = 'https://www.lnb.fr/elite/stats-engine/?option=player&season=2022&competition=266&type=total'
dfs = pd.read_html(url)
df = dfs[0]
df.columns.values[[1, 8, 11, 14]] = ['team', '2%', '3%', 'lf%']

#eFG%
df['efg'] = (((df['2r'] + df['3r']) + 0.5 * df['3r']) / (df['2t'] + df['3t'])) * 100
#TS%
df['ts'] = (df['pts'] / (2 * ((df['2t'] + df['3t']) + 0.44 * df['lt']))) * 100
#Points per shot
df['pps'] = df['pts'] / (df['2t'] + df['3t'])

df = df.fillna(0)

data = (df[['joueur', 'team', 'mj', 'pps', 'efg', 'ts', '2%', '3%', 'lf%', 'pts', '2r', '2t', '3r', '3t', 'lr', 'lt']])
data.columns.values[[0, 1, 2, 3, 4, 5]] = ['Player', 'Team', 'GP', 'PPS', 'eFG%', 'TS%']

#SIDEBAR
st.sidebar.header("Please Filter Here:")
team = st.sidebar.multiselect(
    "Select a team",
    options=data["Team"].unique(),
    default='Paris'
)

data_selection = data.query("Team == @team")
df_selection = (data_selection[['Player', 'Team', 'GP', 'PPS', 'eFG%', 'TS%', '2%', '3%', 'lf%']])

#Selected team average
team_average_pps = round ((data_selection['pts'].sum()) / ((data_selection['2t'].sum()) + (data_selection['3t'].sum())).mean(), 2)
team_average_efg = round ((((((data_selection['2r'].sum()) + (data_selection['3r'].sum())) + 0.5 * (data_selection['3r'].sum())) / ((data_selection['2t'].sum()) + (data_selection['3t'].sum()))) * 100).mean(), 2)
team_average_ts = round ((((data_selection['pts'].sum()) / (2 * (((data_selection['2t'].sum()) + (data_selection['3t'].sum())) + 0.44 * (data_selection['lt'].sum())))) * 100).mean(), 2)

#League average
league_average_pps = round ((data['pts'].sum()) / ((data['2t'].sum()) + (data['3t'].sum())).mean(), 2)
league_average_efg = round ((((((data['2r'].sum()) + (data['3r'].sum())) + 0.5 * (data['3r'].sum())) / ((data['2t'].sum()) + (data['3t'].sum()))) * 100).mean(), 2)
league_average_ts = round ((((data['pts'].sum()) / (2 * (((data['2t'].sum()) + (data['3t'].sum())) + 0.44 * (data['lt'].sum())))) * 100).mean(), 2)

#MAIN PAGE
st.title(":dart: Shooting")

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Points per shot : ")
    st.markdown(f"Team : {team_average_pps:,} PPS")
    st.markdown(f"League : {league_average_pps:,} PPS")
with middle_column:
    st.subheader("Effective Field Goal : ")
    st.markdown(f"Team : {team_average_efg:,} %")
    st.markdown(f"League : {league_average_efg:,} %")
with right_column:
    st.subheader("True Shooting : ")
    st.markdown(f"Team : {team_average_ts:,} %")
    st.markdown(f"League : {league_average_ts:,} %")
st.markdown("##")
st.dataframe(df_selection)
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st
import plotly.figure_factory as ff
import scipy
import helper
import preprocessor

df = pd.read_csv("data/athlete_events.csv")
region_df = pd.read_csv("data/noc_regions.csv")

df = preprocessor.preprocess(df,region_df)
st.sidebar.title("Olympics Analysis")
st.sidebar.image("https://img.olympics.com/images/image/private//f_auto/primary/o3eae7skxxu8gba2ctwp")
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal tally', 'overall Analysis', 'Country-wise Analysis','Athlete-wise Analysis')
)

if user_menu == 'Medal tally':
    st.sidebar.header('Medal tally')

    years , country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select year",years)
    selected_country = st.sidebar.selectbox("Select country",country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title('Medal Tally in ' + selected_country)
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in '+ str(selected_year))
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title('Medal Tally of '+ selected_country +' in '+ str(selected_year))

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    st.table(medal_tally)

if user_menu == 'overall Analysis':
    editions = df["Year"].nunique()-1
    Cities = df['City'].nunique()
    Events = df['Event'].nunique()
    Sports = df['Sport'].nunique()
    Athletes = df['Name'].nunique()
    Nations = df['region'].nunique()
    st.title("Top Statistics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(Cities)
    with col3:
        st.header('Sports')
        st.title(Sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(Events)
    with col2:
        st.header('Nations')
        st.title(Nations)
    with col3:
        st.header('Athletes')
        st.title(Athletes)

    nations_over_time = helper.data_over_time(df,'region')
    st.title("Participating Nations Over Time")
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.plotly_chart(fig)

    Events_over_time = helper.data_over_time(df, 'Event')
    st.title("Events Over Time")
    fig = px.line(Events_over_time, x='Edition', y='Event')
    st.plotly_chart(fig)

    Athletes_over_time = helper.data_over_time(df, 'Name')
    st.title("Athletes Over Time")
    fig = px.line(Athletes_over_time, x='Edition', y='Name')
    st.plotly_chart(fig)

    st.title('No. of Events over time(Every Sport)')
    fig,ax = plt.subplots(figsize = (20,20))
    x = df.drop_duplicates(['Year', 'Event', 'Sport'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    most_successful = helper.most_successful(df,selected_sport)
    st.table(most_successful)

if user_menu == 'Country-wise Analysis':
    st.header('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    st.sidebar.title("Country-Wise Medal Tally")
    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_wise_df = helper.countrywise_medal_tally(df,selected_country)
    st.title(selected_country +" Medal Tally over the Years")
    fig = px.line(country_wise_df, x='Year', y='Medal')
    st.plotly_chart(fig)

    st.title(selected_country + " excels in these sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig,ax = plt.subplots(figsize = (20,20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("Top 10 Athletes from "+ selected_country)
    top10df = helper.most_successful_countrywise_athletes(df,selected_country)
    st.table(top10df)

if user_menu == 'Athlete-wise Analysis':

    st.header('Athlete-wise Analysis')
    st.title('Probability distribution of Athletes based on Medals')
    athlete_df = df.drop_duplicates(['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4],['Age Distribution', 'Gold Medalists', 'Silver Medalists', 'Bronze Medalists'],
                             show_hist=False, show_rug=False)
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming', 'Badminton', 'Sailing',
                     'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey', 'Rowing',
                     'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis', 'Golf', 'Softball',
                     'Archery', 'Volleyball',
                     'Synchronized Swimming', 'Table Tennis', 'Baseball', 'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball',
                     'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    st.title('Distribution of Age w.r.t Sports (Gold Medalist)')
    st.plotly_chart(fig)

    athlete_df['Medal'].fillna('No Medal', inplace=True)
    fig,ax = plt.subplots(figsize = (12,10))
    st.title('Distribution of Gender in specific sport')
    selected_sport = st.selectbox('Select a Sport',famous_sports)
    new_df = helper.height_v_weight(df,selected_sport)
    ax = sns.scatterplot(new_df, y='Height', x='Weight', hue='Medal', style='Sex',s= 50)
    st.pyplot(fig)

    st.title('Men vs Women Participation over the Years')
    final_df = helper.men_v_women(df)
    fig = px.line(final_df, x='Year', y=['Male', 'Female'])
    st.plotly_chart(fig)

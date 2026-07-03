import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


df=pd.read_csv("D:\\Olypics Project\\athlete_events.csv")
region_df=pd.read_csv("D:\\Olypics Project\\noc_regions.csv")


df=preprocessor.preprocess(df,region_df)
st.sidebar.header('Olympics Analysis')
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
st.sidebar.header('Medal Tally')
user_menu=st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)


if user_menu=='Medal Tally':
    st.sidebar.header('Medal Tally')
    st.header("Medal Tally")
    years,country=helper.country_year_list(df)

    selected_years=st.sidebar.selectbox("Select year",years)
    selected_country=st.sidebar.selectbox("Select country",country)

    medal_tally=helper.fetch_medal_tally(df,selected_years,selected_country)
    if selected_years=='overall' and selected_country=='overall':
        st.title('Overall Tally')
    if selected_years!='overall' and selected_country=='overall':
        st.title('Medal Tally  '+ str(selected_years)+ '  Olympics')
    if selected_years=='overall' and selected_country!='overall':
        st.title(selected_country + '  Overall Performance')
    if selected_years!='overall' and selected_country!='overall':
        st.title(selected_country +'  performance  In  '+str(selected_years)+ ' Olympics')
    st.table(medal_tally)



if user_menu=='Overall Analysis':
    editions=df["Year"].unique().shape[0] - 1
    cities=df["City"].unique().shape[0]
    sports=df["Sport"].unique().shape[0]
    events=df["Event"].unique().shape[0]
    athletes=df["Name"].unique().shape[0]
    nations=df['region'].unique().shape[0]
    st.title('Top Statistics')
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)


    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col2:
        st.header('Athletes')
        st.title(athletes)


    nations_over_time=helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x='Year', y='region')
    st.title('Participating Nations Over The Time')
    st.plotly_chart(fig)

    events_over_time=helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x='Year', y="Event")
    st.title('Events Over The Years')
    st.plotly_chart(fig)

    events_over_time=helper.data_over_time(df,'Name')
    fig = px.line(events_over_time, x='Year', y="Name")
    st.title('Athletes Over The Years')
    st.plotly_chart(fig)



    st.title('No of Events over time(Every Sports)')
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(["Year", "Sport", "Event"])
    ax =sns.heatmap(x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype("int"),
                annot=True)
    st.pyplot(fig)


    st.title('Most successful Athletes')
    sports_list=df['Sport'].unique().tolist()
    x=helper.most_successful(df,'Overall')
    st.table(x)



if user_menu=='Country-wise Analysis':

    st.title('Country wise Performance')

    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox('Select country',country_list)

    country_df=helper.yearwise_medal_tally(df,selected_country)

    fig = px.line(country_df, x='Year', y="Medal")
    st.title(selected_country+'   Medal Tally Over The Years')
    st.plotly_chart(fig)

    pt = helper.country_event_heatmap(df, selected_country)

    if pt.empty:
        st.warning(f"No medal data available for {selected_country}")
    else:
        fig, ax = plt.subplots(figsize=(20, 20))
        sns.heatmap(pt, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax)
        st.pyplot(fig)

    st.title('Top 10 Athletes   '+ selected_country)
    top10_df=helper.most_successful(df,'Overall')
    st.table(top10_df)

if user_menu=='Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)


    st.title('Distribution of Age')
    st.plotly_chart(fig)


    x=[]
    name=[]
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

        fig = ff.create_distplot(x,name,
                                 show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=1000, height=600)


        st.title('Distribution of Age wrt Sports')
        st.plotly_chart(fig)


import numpy as np
import seaborn as sns


def fetch_medal_tally(df,years, country):
    medal_df = df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    flag = 0
    if years == "Overall" and country == "Overall":
        temp_df = medal_df.copy()

    if years == "Overall" and country != "Overall":
        flag = 1
        temp_df = medal_df[medal_df["region"] == country]

    if years != "Overall" and country == "Overall":
        temp_df = medal_df[medal_df["Year"] == int(years)]

    if years != "Overall" and country != "Overall":
        temp_df = medal_df[(medal_df["Year"] == int(years)) & (medal_df["region"] == country)]

    if flag == 1:
        x = temp_df.groupby("Year").sum()[["Gold", "Silver", "Bronze"]].sort_values("Year").reset_index()
    else:
        x = temp_df.groupby("region").sum()[["Gold", "Silver", "Bronze"]].sort_values("Gold",
                                                                                      ascending=False).reset_index()

    x["total"] = x["Gold"] + x["Silver"] + x["Bronze"]

    x['Gold']=x['Gold'].astype(int)
    x['Silver']=x['Silver'].astype(int)
    x['Bronze']=x['Bronze'].astype(int)
    x['total']=x['total'].astype(int)

    return x




def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    medal_tally=medal_tally.groupby("region").sum()[["Gold", "Silver", "Bronze"]].sort_values("Gold", ascending=False).reset_index()

    medal_tally["total"] = medal_tally["Gold"] + medal_tally["Silver"] + medal_tally["Bronze"]


    return medal_tally


def country_year_list(df):
    years = sorted(df["Year"].unique().tolist())
    years.insert(0, "Overall")

    country = np.unique(df["region"].dropna().values).tolist()
    country.sort()
    country.insert(0, "Overall")
    return years, country

def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index(
        name='count').sort_values("Year")
    nations_over_time.rename(columns={'count': col}, inplace=True)

    return nations_over_time


def most_successful(df,sport):
    temp_df=df.dropna(subset=["Medal"])

    if sport != "Overall":
        temp_df=temp_df[temp_df["Sport"]==sport]

    temp = temp_df["Name"].value_counts().reset_index(name="Medals")
    temp = temp.head(15)

    temp = temp.merge(df, on="Name", how="left")

    x=temp[["Name", "Medals", "Sport", "region"]].drop_duplicates()
    x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
    )

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(
        index='Sport',
        columns='Year',
        values='Medal',
        aggfunc='count',
        fill_value=0
    )

    return pt

def most_successful_countrywise(df,country):


    temp_df = df.dropna(subset=["Medal"])

    temp_df = temp_df[temp_df["region"] == country]

    temp = temp_df["Name"].value_counts().reset_index(name="Medals")
    temp = temp.head(10)

    temp = temp.merge(df, on="Name", how="left")

    x = temp[["Name", "Medals", "Sport"]].drop_duplicates()
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

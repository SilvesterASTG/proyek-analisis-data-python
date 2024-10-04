import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_season_df(day_df):
    season_df = day_df.groupby(["season", "yr"])["cnt"].sum().reset_index()
    return season_df

def create_monthly_df(day_df):
    monthly_df = day_df.groupby(["mnth", "yr"])["cnt"].sum().reset_index()
    return monthly_df   

all_df = pd.read_csv("https://raw.githubusercontent.com/Meazzaa/Proyek-Analisis-Data-Bike-Sharing-Dataset/main/Data/day.csv")

season_df = create_season_df(all_df)
monthly_df = create_monthly_df(all_df)

st.header(":sparkles: Dashboard :sparkles:")

# Create Sidebar
with st.sidebar:
    st.sidebar.header("About")
    st.sidebar.write("This dashboard is created to visualize the number of bike rented by season and month in 2012. The data is taken from the Bike Sharing Dataset. The dataset contains 731 rows and 16 columns. The columns include the date, season, year, month, holiday, weekday, workingday, weather, temperature, humidity, windspeed, and the number of bike rented. The dataset is taken from the UCI Machine Learning Repository.")
    st.sidebar.caption("Created by: Meazzaa")

# Visualization Bike Renters by Season in 2012
st.subheader("Number of Bike Renters by Season in 2012")
fig, ax = plt.subplots(figsize=(15, 10))
data_2012 = season_df[season_df["yr"]==1] 
ax = sns.barplot(
    y="cnt", 
    x="season",
    hue="season",
    data=data_2012,
    palette="viridis",
    legend="full",
    ax=ax
)
season_label = ["Spring", "Summer", "Fall", "Winter"]
ax.set_xticks(range(len(season_label)), labels=season_label)
ax.set_title("Bike Rented by Season in 2012", loc="center", fontsize=15)
ax.set_ylabel("Bike Rented")
ax.set_xlabel("Season")
ax.tick_params(axis="x", labelsize=10)
for p in ax.patches:
    ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')
st.pyplot(fig)

# Visualization Bike Renters by Month in 2012
st.subheader("Number of Bike Renters by Month in 2012")
fig, ax = plt.subplots(figsize=(15, 10))
data_2012 = monthly_df[monthly_df["yr"]==1] 
ax = sns.barplot(
    y="cnt", 
    x="mnth",
    hue="mnth",
    data=data_2012,
    palette="viridis",
    legend="full",
    ax=ax
)
month_label = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
ax.set_xticks(ticks=range(len(month_label)), labels=month_label)
ax.set_title("Bike Rented by Month in 2012", loc="center", fontsize=15)
ax.set_ylabel("Bike Rented")
ax.set_xlabel("Month")
ax.tick_params(axis="x", labelsize=10)
for index, value in enumerate(data_2012["cnt"]):
    plt.text(index, value + 10, str(value), ha='center', va='bottom', fontsize=10)
st.pyplot(fig)

st.subheader("Conclusion")
st.write("In 2012 bicycle rentals reached the most rentals in the fall with 641479 bicycles, and the least rentals in the spring with 321348 bicycles. In 2012 bicycle rentals reached the most rentals in September with 218573 bicycles, and the least rentals in January with 96744 bicycles.")

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

# Load dataset
all_df = pd.read_csv("https://raw.githubusercontent.com/SilvesterASTG/proyek-analisis-data-python/refs/heads/main/Data/day.csv")

season_df = create_season_df(all_df)
monthly_df = create_monthly_df(all_df)

# Streamlit Header
st.header(":sparkles: Dashboard :sparkles:")

# Create Sidebar with Filters
with st.sidebar:
    st.sidebar.header("Filter Data")
    year_filter = st.sidebar.selectbox("Select Year", options=all_df['yr'].unique(), index=0)
    month_filter = st.sidebar.multiselect("Select Month", options=all_df['mnth'].unique(), default=all_df['mnth'].unique())

    st.sidebar.header("About")
    st.sidebar.write("This dashboard visualizes the number of bike rentals by season and month. The dataset contains data about bike sharing in 2012. You can filter the data using the year and month filters for more specific insights.")
    st.sidebar.caption("Created by: Silvester")

# Filter data based on user input
filtered_season_df = season_df[(season_df['yr'] == year_filter)]
filtered_monthly_df = monthly_df[(monthly_df['yr'] == year_filter) & (monthly_df['mnth'].isin(month_filter))]

# Visualization: Bike Rentals by Season
st.subheader("Number of Bike Rentals by Season in Selected Year")
fig, ax = plt.subplots(figsize=(15, 10))
ax = sns.barplot(
    y="cnt", 
    x="season",
    hue="season",
    data=filtered_season_df,
    palette="viridis",
    legend="full",
    ax=ax
)
season_label = ["Spring", "Summer", "Fall", "Winter"]
ax.set_xticks(range(len(season_label)), labels=season_label)
ax.set_title(f"Bike Rentals by Season in {year_filter}", loc="center", fontsize=15)
ax.set_ylabel("Bike Rented")
ax.set_xlabel("Season")
ax.tick_params(axis="x", labelsize=10)
for p in ax.patches:
    ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')
st.pyplot(fig)

# Visualization: Bike Rentals by Month
st.subheader("Number of Bike Rentals by Month in Selected Year")
fig, ax = plt.subplots(figsize=(15, 10))
ax = sns.barplot(
    y="cnt", 
    x="mnth",
    hue="mnth",
    data=filtered_monthly_df,
    palette="viridis",
    legend="full",
    ax=ax
)
month_label = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
ax.set_xticks(ticks=range(len(month_label)), labels=month_label)
ax.set_title(f"Bike Rentals by Month in {year_filter}", loc="center", fontsize=15)
ax.set_ylabel("Bike Rented")
ax.set_xlabel("Month")
ax.tick_params(axis="x", labelsize=10)
for index, value in enumerate(filtered_monthly_df["cnt"]):
    plt.text(index, value + 10, str(value), ha='center', va='bottom', fontsize=10)
st.pyplot(fig)

# Conclusion Section
st.subheader("Conclusion")
most_rented_season = filtered_season_df.loc[filtered_season_df["cnt"].idxmax()]["season"]
least_rented_season = filtered_season_df.loc[filtered_season_df["cnt"].idxmin()]["season"]
most_rented_month = filtered_monthly_df.loc[filtered_monthly_df["cnt"].idxmax()]["mnth"]
least_rented_month = filtered_monthly_df.loc[filtered_monthly_df["cnt"].idxmin()]["mnth"]

st.write(f"In {year_filter}, the season with the most bike rentals was **{season_label[int(most_rented_season) - 1]}**, "
         f"while the season with the least rentals was **{season_label[int(least_rented_season) - 1]}**.")
st.write(f"During the same year, the month with the highest rentals was **{month_label[int(most_rented_month) - 1]}**, "
         f"and the month with the lowest rentals was **{month_label[int(least_rented_month) - 1]}**.")
         
# Insights and Recommendations
st.subheader("Insights & Recommendations")
st.write("""
1. **High Rental Periods**: The highest number of rentals occurs in **Fall** and during the month of **September**. This suggests a peak in demand during these periods, which could be linked to favorable weather or local events.
   
2. **Low Rental Periods**: The fewest rentals are seen in **Spring** and **January**, which could be attributed to colder temperatures or weather conditions unfavorable for biking. 

3. **Actionable Insight**: Bike rental companies could prepare for increased demand during the Fall by ensuring bike availability, conducting maintenance, and potentially increasing marketing efforts during peak months like September. Conversely, offering promotions or discounts during off-peak months like January may help boost rentals in those periods.
""")

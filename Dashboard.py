import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

@st.cache
def load_data():
    return pd.read_csv("Data/day.csv")

def create_season_df(day_df):
    season_df = day_df.groupby(["season", "yr"])["cnt"].sum().reset_index()
    return season_df

def create_monthly_df(day_df):
    day_df["mnth"] = pd.Categorical(day_df["mnth"], categories=range(1, 13), ordered=True)
    monthly_df = day_df.groupby(["mnth", "yr"])["cnt"].sum().reset_index()
    return monthly_df   

# Load dataset
all_df = load_data()
season_df = create_season_df(all_df)
monthly_df = create_monthly_df(all_df)

# Streamlit Header
st.header(":sparkles: Dashboard :sparkles:")

# Create Sidebar with Filters
with st.sidebar:
    st.sidebar.header("Filter Data")
    year_filter = st.sidebar.selectbox("Select Year", options=all_df['yr'].unique(), index=0)
    month_filter = st.sidebar.multiselect("Select Month", options=all_df['mnth'].unique(), default=all_df['mnth'].unique())
    if not month_filter:
        month_filter = all_df['mnth'].unique()

    st.sidebar.header("About")
    st.sidebar.write("This dashboard visualizes the number of bike rentals by season and month...")
    st.sidebar.caption("Created by: Silvester")

# Filter data based on user input
filtered_season_df = season_df[(season_df['yr'] == year_filter)]
filtered_monthly_df = monthly_df[(monthly_df['yr'] == year_filter) & (monthly_df['mnth'].isin(month_filter))]

# Visualization: Bike Rentals by Season
st.subheader("Number of Bike Rentals by Season in Selected Year")
fig, ax = plt.subplots(figsize=(15, 10))
sns.barplot(y="cnt", x="season", hue="season", data=filtered_season_df, palette="viridis", ax=ax)
season_label = ["Spring", "Summer", "Fall", "Winter"]
ax.set_xticks(range(len(season_label)), labels=season_label)
ax.set_title(f"Bike Rentals by Season in {year_filter}", fontsize=15)
ax.set_ylabel("Bike Rented")
ax.set_xlabel("Season")
for p in ax.patches:
    ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')
st.pyplot(fig)

# Visualization: Bike Rentals by Month
st.subheader("Number of Bike Rentals by Month in Selected Year")
fig, ax = plt.subplots(figsize=(15, 10))
sns.barplot(y="cnt", x="mnth", hue="mnth", data=filtered_monthly_df, palette="viridis", ax=ax)
month_label = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
ax.set_xticks(ticks=range(len(month_label)), labels=month_label)
ax.set_title(f"Bike Rentals by Month in {year_filter}", fontsize=15)
ax.set_ylabel("Bike Rented")
ax.set_xlabel("Month")
for index, value in enumerate(filtered_monthly_df["cnt"]):
    plt.text(index, value + 10, str(value), ha='center', va='bottom', fontsize=10)
st.pyplot(fig)

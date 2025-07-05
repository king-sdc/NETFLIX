import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("netflix_user_data.csv")
df['watch_date'] = pd.to_datetime(df['watch_date'])
df['watch_day'] = df['watch_date'].dt.day_name()
df['watch_hour'] = df['watch_date'].dt.hour
df['month'] = df['watch_date'].dt.month_name()
df['is_binge'] = df['watch_duration'] >= 90

# Title
st.title("🎬 Netflix User Behavior Dashboard")

# Sidebar filters
selected_genre = st.sidebar.multiselect("Filter by Genre", options=df['genre'].unique(), default=df['genre'].unique())
selected_user = st.sidebar.multiselect("Filter by User ID", options=df['user_id'].unique(), default=df['user_id'].unique())

# Filtered data
filtered_df = df[(df['genre'].isin(selected_genre)) & (df['user_id'].isin(selected_user))]

# Top Genres
st.subheader("Top Genres Watched")
top_genres = pd.Series(filtered_df['genre']).value_counts().head(10)
st.bar_chart(top_genres)

# Binge Rate by Hour
st.subheader("Binge Watching Rate by Hour")
binge_by_hour = filtered_df.groupby('watch_hour')['is_binge'].mean()
st.line_chart(binge_by_hour)

# Ratings by Genre
st.subheader("Average Rating by Genre")
avg_ratings = filtered_df.groupby('genre')['rating'].mean()
st.bar_chart(avg_ratings)

# Watch Hours per Day
st.subheader("Average Watch Duration by Day of Week")
watch_by_day = filtered_df.groupby('watch_day')['watch_duration'].mean().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)
st.bar_chart(watch_by_day)

# Footer
st.markdown("We Made It")

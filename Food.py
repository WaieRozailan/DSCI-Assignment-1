import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud

file_path = r"C:\Users\ASUS\OneDrive\Documents\.politeknik\DSCI\GitHub-Test\zomatodifieds2.csv"

zomato_df = pd.read_csv(file_path)

# Extract numeric part from 'rate' and convert to numeric
zomato_df['rate'] = zomato_df['rate'].str.extract('(\d+\.\d+)').astype(float)


# --- SIDEBAR ---
st.sidebar.header("Filter Here: City")
city = st.sidebar.selectbox(
    "Select The City:",
    options=zomato_df['location'].unique(),
    index=0  # Set a default value, e.g., the first city
)

cuisine_type = st.sidebar.multiselect(
    "Select The Cuisine Type:",
    options=zomato_df['cuisines'].unique(),
    default=zomato_df['cuisines'].unique(),
)

restaurant_type = st.sidebar.multiselect(
    "Select The Restaurant Type:",
    options=zomato_df['rest_type'].unique(),
    default=zomato_df['rest_type'].unique(),
)

# ---
df_selection = zomato_df.query(
    "location == @city & cuisines == @cuisine_type & rest_type == @restaurant_type"
)

# Display filtered data instead of the entire dataset
st.dataframe(df_selection)

# Handling NaN Values
if df_selection.isnull().values.any():
    st.warning("There are NaN values in the selected data. Please handle them as needed.")

# Calculate average rating only for the selected location
average_rating = round(df_selection['rate'].mean(), 2)

# Convert average votes to a string with comma for readability
average_votes_formatted = "{:,}".format(int(df_selection['votes'].sum()))

# Convert cuisines to strings, handle NaN values, and make them unique
selected_cuisines = ', '.join(set(df_selection['cuisines'].astype(str)))

# --- MAINPAGE ---
st.title(":")
st.markdown("##")

# TOP KPI's
location = df_selection['location'].iloc[0]  # Take the first location if there are multiple
average_votes = int(df_selection['votes'].sum())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Selected Location:")
    st.write(f"{location}")

with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} :star:")

    st.subheader("Selected Cuisines:")
    st.write(selected_cuisines)

with right_column:
    st.subheader("Customer Votes for the selected Location:")
    st.subheader(f"{average_votes_formatted} :thumbsup:")


# --- VISUALIZATION NUMBER 1 ---
# Average ratings by cuisine in selected location
fig = px.bar(df_selection, x='cuisines', y='rate', color='location', title='Average Ratings by Cuisine')
st.plotly_chart(fig)

# --- VISUALIZATION NUMBER 2 ---
# Bar Chart for Average Ratings by Location
fig1 = px.bar(df_selection, x='location', y='rate', title='Average Ratings by Location')
st.plotly_chart(fig1)

# --- VISUALIZATION NUMBER 3 ---
# Pie Chart for Cuisine Distribution
fig2 = px.pie(df_selection, names='cuisines', title='Cuisine Distribution') 
st.plotly_chart(fig2)


# --- VISUALIZATION NUMBER 4 ---
# Word Cloud for Dish Liked
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df_selection['dish_liked'].dropna()))

st.image(wordcloud.to_image())
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
#st.pyplot(plt)



# streamlit run c:/Users/ASUS/OneDrive/Documents/.politeknik/DSCI/GitHub-Test/Food.py


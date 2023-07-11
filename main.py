import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
import urllib.parse

# Read the data from CSV
data = pd.read_csv('archive.csv')

# Set the page configuration
st.set_page_config(page_title = "Project Python 2", page_icon = ":tada:", layout="wide")

# HEADER SECTION
with st.container():
    st.subheader("Hi:wave: we're from group 4 class Business IT2")
    st.title("What is there more to know about Nobel Prize Winners?")
    st.write("Apart from their achievements, join us today on this app to get to know the Laureates' Birth Countries and Average Lifespan!" ) 

# OUR DATASET
url = "https://www.kaggle.com/datasets/nobelfoundation/nobel-laureates?resource=download"
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column: st.header("Our dataset :sparkles:")
    st.markdown(f"[Click here to see the original dataset]({url})")
    st.write("##")
    st.write(
        """ Our refined data frame contains 4 main variables as follows:
        \n - *Category*: A factor with levels of Medicine, Physics, Peace, Literature, Chemistry, and Economics (Categories of the Nobel Prize)
        \n - *Number of Prizes*: A vector that counts the number of Prizes received
        \n - *Birth Country*: A factor that notes the birth countries of Nobel Laureates
        \n - *Age*: A vector that illustrates the age of Nobel Prize Winners using the subtraction of Death Year to Birth Year """)

st.divider()
st.header("Top Birth Countries and Life Span Chart")
st.write("Discover these two graphs below with us")


# Add Sidebar
st.sidebar.write('**:bulb: Reporting to Dr. Tan Duc Do**')
st.sidebar.write('**:bulb: Group 4 Business IT 2 Members:**')

# Add content to the main area
with st.sidebar:
    st.write('Ta Nguyen Minh Hang')
    st.write('Doan Minh Ngoc')
    st.write('Nguyen Hong Bao Ngoc')
    st.write('Pham Dan Thao')
    st.write('Nguyen Ai Nhi')


# Initial 2 tabs for each interactive graph
tab1, tab2 = st.tabs(["Bar Chart", "Boxplot Chart"])

# Get the current URL
url = st.experimental_get_query_params()
current_tab = url["tab"][0] if "tab" in url else "Bar Chart"

### TAB 1: BAR CHART
if current_tab == "Bar Chart":
# Calculate the value counts of Birth_Country
    df = data['Birth_Country'].value_counts()

# Set the initial value for the slider
value = 5

# Get the top N countries with the most prizes
df1 = df.nlargest(n=value, keep='all')

# Define color palette for the bars
color1 = ["#19376D", "#576CBC", "#A5D7E8", "#66347F", "#9E4784", "#D27685", "#D4ADFC", "#F2F7A1", "#FB2576", "#E94560"]

# Add the slider
value = tab1.slider("Number of Countries", min_value=1, max_value=10, step=1, value=value)

# Update the top N countries based on the slider value
df1 = df.nlargest(n=value, keep='all')
color1 = color1[:len(df1)]

# Update the title of the plot
tab1.subheader("Top {} Countries That Had The Most Nobel Prize Winners".format(value))

# Create the bar chart using Altair
bar_data = pd.DataFrame({"Country": df1.index, "Number of Prizes": df1.values, "Color": color1})
bars = alt.Chart(bar_data).mark_bar().encode(
    x=alt.X('Country', sort=None),
    y=alt.Y('Number of Prizes'),
    color=alt.Color('Color', scale=None),
    tooltip=['Country', 'Number of Prizes']
).properties(width=1400)

# Rotate x-axis labels for better readability
bars = bars.configure_axisX(labelAngle=0)

# Display the chart using Streamlit
tab1.altair_chart(bars, use_container_width=True)

### TAB 2: BOXPLOT CHART
if current_tab == "Boxplot Chart":    
  data[['Birth_Year', 'Birth_Month', 'Birth_Day']] = data.Birth_Date.str.split("-", expand=True)
  data[['Death_Day', 'Death_Month', 'Death_Year']] = data.Death_Date.str.split("/", expand=True)

data["Birth_Year"] = pd.to_numeric(data["Birth_Year"], errors='coerce')
data["Death_Year"] = pd.to_numeric(data["Death_Year"], errors='coerce')
data["Year"] = pd.to_numeric(data["Year"], errors='coerce')

data['Age'] = data['Death_Year'] - data['Birth_Year']


# Sort the data by Age in ascending order
data_sorted = data.sort_values(by='Age', ascending=True)

# Create a palette color for categories
category_colors = {
    'Physics': '#7DEFA1',
    'Chemistry': '#FF2B2B',
    'Medicine': '#A5D7E8',
    'Literature': '#0068C9',
    'Peace': '#D4ADFC',
    'Economic Sciences': '#29B09D'
}

# Add the title of the plot
tab2.subheader("Lifespan of Nobel Winners")


    # Create two columns for displaying the boxplots
    col1, col2 = st.columns(2)

    with col1:
        # Create a subset of data for Physics, Medicine, and Chemistry categories
        physics_med_chem = data_sorted[data_sorted['Category'].isin(['Chemistry', 'Physics', 'Medicine'])]
        fig1 = px.box(physics_med_chem, y="Age", x="Category", color="Category", color_discrete_map=category_colors)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # Create a subset of data for Literature, Peace, and Economics categories
        lit_peace_econ = data_sorted[data_sorted['Category'].isin(['Literature', 'Peace', 'Economics'])]
        fig2 = px.box(lit_peace_econ, y="Age", x="Category", color="Category", color_discrete_map=category_colors)
        st.plotly_chart(fig2, use_container_width=True)



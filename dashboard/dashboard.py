import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Bike Rentals Data Visualization")

st.subheader("Loading Dataset")

# path to my data
csv_file_path = "https://raw.githubusercontent.com/TimKahyo/RentalBikeDataVisualization/main/dashboard/merged.csv"


# load dataset
merged_df = pd.read_csv(csv_file_path)

# convert 'dteday' column to datetime format
merged_df["dteday"] = pd.to_datetime(merged_df["dteday"])

st.write("Merged dataset preview:")
st.dataframe(merged_df.head())

st.subheader("Exploratory Data Analysis")


def show_correlation_matrix():
    st.write("Correlation Matrix")
    # select only numeric columns for correlation calculation
    numeric_df = merged_df.select_dtypes(include="number")
    corr = numeric_df.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    st.pyplot(fig)


show_correlation_matrix()


def plot_total_rentals_over_time():
    # group by date and sum the daily rentals from 'cnt_y'
    daily_rentals = merged_df.groupby("dteday")["cnt_y"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(
        daily_rentals["dteday"],
        daily_rentals["cnt_y"],
        marker="o",
        label="Total Rentals",
    )
    ax.set_title("Total Rentals Over Time", fontsize=14)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Total Daily Rentals", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis="y")
    plt.legend()
    st.pyplot(fig)


def plot_total_rentals_by_hour():
    # group by hour and sum the hourly rentals from 'cnt_x'
    hourly_rentals = merged_df.groupby("hr")["cnt_x"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(hourly_rentals["hr"], hourly_rentals["cnt_x"])
    ax.set_title("Total Rentals by Hour", fontsize=14)
    ax.set_xlabel("Hour of Day", fontsize=12)
    ax.set_ylabel("Total Hourly Rentals", fontsize=12)
    plt.grid(axis="y")
    st.pyplot(fig)


def plot_total_rentals_by_season():
    # group by season and sum the total rentals by season using 'cnt_y' (daily total rentals)
    seasonal_rentals = merged_df.groupby("season")["cnt_y"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(seasonal_rentals["season"], seasonal_rentals["cnt_y"])
    ax.set_title("Total Rentals by Season", fontsize=14)
    ax.set_xlabel("Season", fontsize=12)
    ax.set_ylabel("Total Rentals (Daily)", fontsize=12)
    st.pyplot(fig)


# dropdown for selecting plot type
st.subheader("Data Visualizations")
plot_options = [
    "Total Rentals Over Time",
    "Total Rentals by Hour",
    "Total Rentals by Season",
]
selected_plot = st.selectbox("Select a plot to visualize:", plot_options)

# plot based on the selection
if selected_plot == "Total Rentals Over Time":
    plot_total_rentals_over_time()
elif selected_plot == "Total Rentals by Hour":
    plot_total_rentals_by_hour()
else:
    plot_total_rentals_by_season()

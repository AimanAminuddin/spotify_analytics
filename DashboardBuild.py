import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Package to generate data
# needed to build dashboard
from DataBuilder import (
    DataBuilder,
    load_spotify_credentials
)

class DashboardBuild:
    '''
    Class that preps all the 
    charts and figures required
    in dashboard
    '''

    def __init__(self,dashboard_data):
        self.dashboard_data = dashboard_data

    def plot_track_popularity(self):
        '''
        Plot the distribution of saved songs based on 
        Spotify Popularity metrics
        '''

        # Set style for Seaborn
        sns.set(style="whitegrid")

        # Track Popularity Distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(self.dashboard_data['popularity'], kde=True, color='skyblue', bins=30)
        plt.title("Distribution of Track Popularity")
        plt.xlabel("Popularity")
        plt.ylabel("Frequency")
        plt.show()

        return
    
    def plot_artist_count(self):
        '''
        Plot the total number of songs by 
        same artist in saved & liked songs
        '''
        # Extract Top 10 artist based on count
        top_artists = self.dashboard_data['artist_name'].value_counts().head(10)
        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_artists.index, y=top_artists.values, palette='Blues')

        # Configuration to make Visualizations
        # more eye appealing
        plt.title("Top 10 Most Frequent Artists")
        plt.xlabel("Artist")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        
        plt.show()
        return


if __name__ == '__main__':
    print('hello world')
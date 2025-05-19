import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from wordcloud import WordCloud

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

    def plot_top_album(self):
        '''
        Plot the total number of songs by same
        album in saved & liked songs
        '''

        top_albums = self.dashboard_data['album_name'].value_counts().head(10)
        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_albums.index, y=top_albums.values, palette='Blues')
        plt.title("Top 10 Albums by Track Count")
        plt.xlabel("Album")
        plt.ylabel("Track Count")
        plt.xticks(rotation=45)
        plt.show()
        
        return
    
    def plot_explicit_non_explicit(self):
        '''
        Plot the total number of songs that 
        are explicit against songs that are not
        '''

        explicit_counts = (
            self.dashboard_data['explicit']
                .value_counts()
                .rename({True: 'Explicit', False: 'Clean'})
        )

        plt.figure(figsize=(8, 8))
        sns.countplot(x='explicit', data= explicit_counts, palette='Blues')
        plt.title("Explicit vs Clean Tracks")
        plt.xlabel("Track Type")
        plt.ylabel("Count")
        plt.xticks([0, 1], ['Clean', 'Explicit'])
        plt.show()

        return

    def plot_track_distribution(self):
        '''
        Function that generates the distribution 
        of song durations in liked songs 
        '''

        # Track Duration Distribution
        self.dashboard_data['duration_min'] = np.round(self.dashboard_data['duration_ms']/60000,2)
        plt.figure(figsize=(10, 6))
        sns.histplot(self.dashboard_data['duration_min'], kde=True, color='skyblue', bins=30)
        plt.title("Track Duration Distribution")
        plt.xlabel("Duration (minutes)")
        plt.ylabel("Frequency")
        plt.show()

        return
    
    def plot_release_year_trend(self):
        '''
        Function that generaets line chart 
        showing number of track(s) based on 
        release year in saved playlist
        '''

        # Release Year Trend
        self.dashboard_data['release_date'] = pd.to_datetime(
            self.dashboard_data['release_date'], 
            format='mixed', 
            errors='coerce'
            )

        self.dashboard_data['release_year'] = self.dashboard_data['release_date'].dt.year
        yearly_counts = self.dashboard_data['release_year'].value_counts().sort_index()
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=yearly_counts.index, y=yearly_counts.values, marker='o', color='b')
        plt.title("Number of Tracks Released Over Years")
        plt.xlabel("Year")
        plt.ylabel("Number of Tracks")
        plt.show()

        return 
    
    def generate_word_cloud(self):
        '''
        Function that generaets world cloud 
        based on saved & like songs
        '''

        # Genre Distribution (if available and contains genres)
        if 'genres' in self.dashboard_data.columns and self.dashboard_data['genres'].notna().any():
            all_genres = ', '.join(self.dashboard_data['genres'].dropna())

            # Check if there's any genre to create a word cloud
            if all_genres.strip():  # Ensure there is at least one genre
                wordcloud = WordCloud(
                    width=800, height=400,
                    background_color='white'
                    ).generate(all_genres)

                plt.figure(figsize=(10, 5))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                plt.title("Genre Word Cloud")
                plt.show()

            else:
                print("No genres available to generate word cloud.")

        else:
            print("No 'genres' column or genres data is missing.")

        return


if __name__ == '__main__':
    print('hello world')
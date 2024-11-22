from functools import partial
from shiny.express import ui
from shiny import render
from shiny.ui import page_navbar
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from shinywidgets import render_widget 
import plotly.express as px
from textblob import TextBlob

ui.page_opts(
    title="Three Way Decisions in Disaster Management",  
    page_fn=partial(page_navbar, id="page"),  
)

with ui.nav_panel("Overview"):
    with ui.layout_columns():
        with ui.value_box():
            'Number of Papers'
            papers = pd.read_csv("paper.csv")
            len(papers)

        with ui.value_box():
            'Number of Unique Authors'
            papers = pd.read_csv("paper.csv")
            authors = papers['Authors'].dropna().str.split(',').explode().str.strip().unique()
            len(authors)
        
        with ui.value_box():
            'Number of Conferences'
            papers = pd.read_csv("paper.csv")
            conferences = papers['Journal/Conference'].dropna().unique()
            len(conferences)
    
    with ui.layout_columns():
        with ui.card():
            ui.card_header("Number of Papers per Year")
            @render_widget
            def plot_papers_per_year():
                papers = pd.read_csv("paper.csv")
                papers_filtered = papers.dropna(subset=['Publication Year'])

                # Filter out non-numeric 'Publication Year' values
                papers_filtered = papers_filtered[papers_filtered['Publication Year'].apply(lambda x: x.isnumeric())]

                # Convert 'Publication Year' to integer
                papers_filtered['Publication Year'] = papers_filtered['Publication Year'].astype(int)

                # Plot the distribution of papers over the years
                papers_per_year = papers_filtered['Publication Year'].value_counts().sort_index()
                fig = px.bar(x=papers_per_year.index, y=papers_per_year.values, labels={'x': 'Year', 'y': 'Number of Papers'})
                fig.update_layout(template='simple_white')
                return fig

        with ui.card():
            ui.card_header("Sentiment polarity of Abstracts")
            @render_widget
            def plot_papers_per_conference():
                def get_sentiment(text):
                    blob = TextBlob(text)
                    return blob.sentiment.polarity

                # Apply the function to the 'Abstract' column
                papers['Sentiment'] = papers['Abstract Summary'].dropna().apply(get_sentiment)

                # Plot the distribution of sentiment polarity
                fig = px.histogram(papers, x='Sentiment', nbins=20, labels={'x': 'Sentiment Polarity', 'y': 'Number of Papers'})
                fig.update_layout(template='simple_white')
                return fig
            
with ui.nav_panel("WordClouds"):
    with ui.layout_columns():  
        with ui.card():  
            ui.card_header("Wordcloud for Keywords")
            @render.plot
            def wordcloud_keyword():
                papers = pd.read_csv("paper.csv")
                
                # Combine all keywords into a single string
                keywords_text = ' '.join(papers['Keywords'].dropna())

                # Generate the word cloud
                wordcloud_keyword = WordCloud(width=800, height=400, background_color='white').generate(keywords_text)
                fig, ax = plt.subplots()
                ax.imshow(wordcloud_keyword, interpolation='bilinear')
                ax.axis('off')

                return fig

        with ui.card():  
            ui.card_header("Wordcloud for Future Work")
            @render.plot
            def wordcloud_future_work():
                papers = pd.read_csv("paper.csv")
                
                # Combine all keywords into a single string
                keywords_text = ' '.join(papers['Future Work Suggestions'].dropna())

                # Generate the word cloud
                wordcloud_future_work = WordCloud(width=800, height=400, background_color='white').generate(keywords_text)
                fig, ax = plt.subplots()
                ax.imshow(wordcloud_future_work, interpolation='bilinear')
                ax.axis('off')

                return fig  
    
with ui.nav_panel("C"):  
    "Page C content"



import streamlit as st
import pandas as pd
import subprocess
import os
from datetime import datetime

def display_csv(file_path):
    df = pd.read_csv(file_path)
    st.dataframe(df)

def run_spider(keywords, location, post_timing):
    command = f"scrapy crawl linkedin_jobs -a keywords='{keywords}' -a location='{location}' -a post_timing='{post_timing}'"
    subprocess.run(command, shell=True)
    
    # Generate the new file name
    current_date = datetime.now().strftime("%Y-%m-%d")
    new_file_name = f"{keywords.replace(' ', '_')}-{post_timing.replace(' ', '_')}-{current_date}.csv"
    
    # Find the most recent CSV file in the output directory
    csv_files = [file for file in os.listdir('output') if file.endswith('.csv')]
    if csv_files:
        most_recent_file = max(csv_files, key=lambda f: os.path.getmtime(os.path.join('output', f)))
        
        # Rename the file
        os.rename(os.path.join('output', most_recent_file), os.path.join('output', new_file_name))
    
    return new_file_name

st.title('Freelancer Challenge Scraper.App')
st.header('Customize Your Job Search')

keywords = st.text_input('Job Keywords', 'data analyst')
location = st.text_input('Location', 'India')
post_timing = st.selectbox('Post Timing', ['1 day', '1 week', '1 month'])

if st.button('Scrape Jobs'):
    new_file_name = run_spider(keywords, location, post_timing)
    st.success(f'Scraping job completed. File saved as {new_file_name}')

st.header('Scraped Job Data')
csv_files = [file for file in os.listdir('output') if file.endswith('.csv')]
selected_file = st.selectbox('Select CSV file to view', csv_files)

if selected_file:
    display_csv(f'output/{selected_file}')
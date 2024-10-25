from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd
from ExtractLinks import extract_links

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
client = OpenAI()

# Sample URLs (replace with actual URLs or the structure from your bookmarks)
file_path = 'server/data/papers_dataset.html'
urls = extract_links(file_path)

# Define the table structure
columns = [
    "Title", "Authors", "Publication Source", "Year", "Main Topic", 
    "Key Findings", "Methodology", "Applications/Use Cases", "Limitations", 
    "Future Research Directions"
]
papers_df = pd.DataFrame(columns=columns)

# Function to query ChatGPT
def get_paper_info(url):
    try:
        # Construct the prompt with the URL
        prompt = f"Extract the following details from the research paper at this URL: {url}. Provide:\n" \
                 "Title, Authors, Publication Source, Year, Main Topic, Key Findings, Methodology, " \
                 "Applications/Use Cases, Limitations, and Future Research Directions."

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that helps extract and structure research paper details for a table format."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract the structured content from the response
        content = response['choices'][0]['message']['content']
        
        # Parse the response into dictionary format
        paper_info = {col: None for col in columns}
        for line in content.splitlines():
            for col in columns:
                if line.startswith(col + ":"):
                    paper_info[col] = line.split(": ", 1)[1]  # Extract the content after ": "
        
        return paper_info

    except Exception as e:
        print(f"Error fetching details for {url}: {e}")
        return None

# Iterate over each URL and populate the table
for url in urls:
    paper_info = get_paper_info(url)
    if paper_info:
        papers_df = pd.concat([papers_df, pd.DataFrame([paper_info])], ignore_index=True)

# Display the table
print(papers_df)
from bs4 import BeautifulSoup

def extract_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    links = [(a['href'], a.get_text(strip=True)) for a in soup.find_all('a', href=True)]
    
    return links

if __name__ == "__main__":
    file_path = 'server\data\papers_dataset.html'
    links = extract_links(file_path)
    print(links, sep='\n')
from scholarly import scholarly
import json
from datetime import datetime
import os

def fetch_papers(scholar_id):
    # Get the author's data
    author = scholarly.search_author_id(scholar_id)
    scholarly.fill(author, sections=['publications'])
    
    papers = []
    for pub in author['publications']:
        scholarly.fill(pub)
        
        # Get year and ensure it's a valid number
        year = pub['bib'].get('pub_year', '')
        try:
            year = int(year)
        except (ValueError, TypeError):
            year = 0
        
        paper = {
            'title': pub['bib'].get('title', ''),
            'authors': pub['bib'].get('author', '').split(' and '),
            'year': year,
            'venue': pub['bib'].get('venue', ''),
            'url': pub.get('pub_url', ''),
            'citations': pub.get('num_citations', 0),
            'scholar_url': pub.get('scholar_url', '')
        }
        papers.append(paper)
    
    # Sort papers by year (newest first)
    papers.sort(key=lambda x: x['year'] or 0, reverse=True)
    
    # Group papers by year (skip papers with invalid years)
    papers_by_year = {}
    for paper in papers:
        year = paper['year']
        if year != 0:  # Only include papers with valid years
            if year not in papers_by_year:
                papers_by_year[year] = []
            papers_by_year[year].append(paper)
    
    # Save to JSON file
    with open('papers.json', 'w') as f:
        json.dump(papers_by_year, f, indent=2)

if __name__ == "__main__":
    # Replace with your Google Scholar ID
    SCHOLAR_ID = "svxVZpoAAAAJ"
    fetch_papers(SCHOLAR_ID) 
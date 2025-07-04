import requests
from bs4 import BeautifulSoup

def get_course_codes(search_term: str):
    url = f"https://programs-courses.uq.edu.au/search.html?keywords={search_term}&searchType=all&archived=true"
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all <a> tags with class "code"
    code_links = soup.find_all('a', class_='code')
    
    course_codes = [a.text.strip() for a in code_links]
    return course_codes

if __name__ == "__main__":
    search_term = input("Search term for courses: ").strip()
    if not search_term:
        search_term = "."
    codes = get_course_codes(search_term)
    
    print(f"Found {len(codes)} courses:")
    with open('course_codes.txt', 'w', encoding='utf-8') as f:
        for code in codes:
            print(code)
            f.write(code + '\n')

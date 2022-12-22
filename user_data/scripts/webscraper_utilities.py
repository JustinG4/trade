import requests
from bs4 import BeautifulSoup
import operator


# scrape team URLS
def scrapeTeamsURLS(URL):
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    # Find all of the team links
    team_links = soup.find_all("a", class_="AnchorLink")

    # Create an empty dictionary
    teams = {}

    # Loop through the team links and add the team name and URL to the dictionary
    for link in team_links:
        name = link.text
        url = link['href']
        teams[name] = url

    print(teams)


# get soccer stats (in terms of GPG/APG)
def getSoccerStats(url):
    # Send a request to the webpage and store the response
    response = requests.get(url)

    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the two tables on the page
    tables = soup.find_all('table')

    goals = tables[0]
    # Find all rows in the table (excluding the header row)
    rows = goals.find_all('tr')[1:]
    goals_dict = {}

    # Iterate over the rows
    for row in rows:
        # Find all cells in the row
        cells = row.find_all('td')
        # Extract the name and stats from the cells
        name = cells[1].text
        games_played = cells[2].text
        goals_scored = cells[3].text
        gpg = float(goals_scored) / float(games_played)
        stats = [gpg, games_played, goals_scored]
        goals_dict[name] = stats

    assists = tables[1]
    # Find all rows in the table (excluding the header row)
    rows = assists.find_all('tr')[1:]
    assists_dict = {}

    # Iterate over the rows
    for row in rows:
        # Find all cells in the row
        cells = row.find_all('td')
        # Extract the name and stats from the cells
        name = cells[1].text
        games_played = cells[2].text
        assists = cells[3].text
        apg = float(assists) / float(games_played)
        stats = [apg, games_played, assists]
        assists_dict[name] = stats

    # Sort the dictionary by value in descending order
    sorted_goals_data = dict(sorted(goals_dict.items(), key=operator.itemgetter(1), reverse=True))
    sorted_ass_data = dict(sorted(assists_dict.items(), key=operator.itemgetter(1), reverse=True))

    data = {
        'Goals': sorted_goals_data,
        'Assists': sorted_ass_data
    }

    return data
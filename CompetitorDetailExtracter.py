from bs4 import BeautifulSoup
import requests
import json
import pandas as pd


class CompetitorDetailExtracter():
    athlete_id=None
    page_content=None
    soup=None

    def __init__(self, competition_id, athlete_id):
        self.competition_id = competition_id
        self.athlete_id = athlete_id
    
    def request_home_page(self):
        athlete_comp_page_url = "https://www.bjjcompsystem.com/tournaments/" +str(self.competition_id) + "/tournament_days/by_competitor?competitor_id=" + str(self.athlete_id)
        athlete_comp_page = requests.get(athlete_comp_page_url)
        assert(athlete_comp_page.status_code==200)

        self.page_content = athlete_comp_page.content
    
    def soupify_content(self):
        self.soup = BeautifulSoup(self.page_content, 'html.parser')

    def get_name(self):
        self.name = self.soup.h1.get_text()
    

    def get_assigned_matches(self):
        matches = self.soup.find_all('li', class_='match--assigned')
        self.assigned_match_dict = self.extract_details(list(set(matches)))
        return self.assigned_match_dict 
    
    def get_upcoming_matches(self):
        matches = self.soup.find_all('li', class_='match--created')
        self.upcoming_match_dict = self.extract_details(list(set(matches)))
        return self.upcoming_match_dict

    def extract_details(self, matches):
        match_no = 0
        match_dict={}
        for match in matches:
            match_when = match.find(class_="search-match-header__when").get_text()
            match_where = match.find(class_="search-match-header__where").b.get_text()
            match_given_opponent = match.find_all(class_="match-card__competitor-name")
            match_possible_opponent = match.find_all(class_= 'match-card__child-where')

            opponent_name = 'Unknown'
            for opponent in match_given_opponent:
                if opponent.get_text() == self.name:
                    pass
                else:
                    opponent_name = opponent 
            
            possible_opponent = []
            for opponent in match_possible_opponent:
                if opponent.get_text()=='-':
                    pass
                else:
                    possible_opponent.append(opponent.get_text())
                
            
            detail_match_dict = {
                "opponent_name":opponent_name,
                "possible_opponent": possible_opponent,
                "match_when":match_when,
                "match_where":match_where
            }

            match_dict["match"+str(match_no)] = detail_match_dict

            match_no = match_no+1
        return match_dict
        

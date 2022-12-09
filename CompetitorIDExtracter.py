from bs4 import BeautifulSoup
import requests
import json
import pandas as pd


class CompetitorIDExtracter():
    competition_id=None
    page_content=None
    soup=None
    competitor_df=None

    def __init__(self, competition_id):
        self.competition_id = competition_id
    
    def request_home_page(self):
        home_comp_page_url = "https://www.bjjcompsystem.com/tournaments/" +str(self.competition_id) + "/tournament_days/2409"
        
        home_comp_page = requests.get(home_comp_page_url)
        assert(home_comp_page.status_code==200)

        self.page_content = home_comp_page.content
        return home_comp_page
    
    def soupify_content(self):
        self.soup = BeautifulSoup(self.page_content, 'html.parser')

    def create_competitor_df(self):
        soup_search_elements = self.soup.find_all(attrs={"data-react-class":"search_field/search_field"})
        raw_competitor_id = soup_search_elements[2]['data-react-props'] #We need the third search element
        raw_competitor_id_dict = json.loads(raw_competitor_id)

        self.competitor_df = pd.DataFrame(json.loads(raw_competitor_id_dict['competitors']))
    
    def get_id(self, name):
        #If there is no dataframe yet, then we create it. Else we return the id
        if self.competitor_df is None:
            self.request_home_page()
            self.soupify_content()
            self.create_competitor_df()
        
        competitor_id = self.competitor_df[self.competitor_df['name']==name]
        if competitor_id.shape[0]==0:
            Exception('Name Not Found')
        elif competitor_id.shape[0]>1:
            print("Multiple athletes are called: " + name)
        return int(competitor_id.id)

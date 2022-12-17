from CompetitorIDExtracter import CompetitorIDExtracter
from CompetitorDetailExtracter import CompetitorDetailExtracter

competition_id = 1922 #Competition ID for Worlds
competitionExtracter = CompetitorIDExtracter(competition_id)
print(competitionExtracter.get_id('Aaron Cole Ryan'))

athlete_1 = competitionExtracter.get_id('Adam Wardzinski')
athlete_2 = competitionExtracter.get_id('Aaron Cole Ryan')

print([athlete_1, athlete_2])

athlete_1_extractor = CompetitorDetailExtracter(competition_id, athlete_1)
athlete_1_extractor.request_home_page()
athlete_1_extractor.soupify_content()
athlete_1_extractor.get_name()
print(athlete_1_extractor.get_assigned_matches())
print(athlete_1_extractor.get_upcoming_matches())

#If I want to finish this, just iterate over the names that you want to scrape.
#Create a pretty print class. And stuff is done. 
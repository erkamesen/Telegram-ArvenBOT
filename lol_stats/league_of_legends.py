import requests
from bs4 import BeautifulSoup


class LOL:
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0"
    }

    def __init__(self, username, region="tr"):
        self.stats = {}
        self.username = username
        self.region = region.lower()
        self.URL = f"https://www.leagueofgraphs.com/summoner/{self.region}/{self.username}#championsData-all"
        self.response = requests.get(self.URL, headers=LOL.header)
        self.soup = BeautifulSoup(self.response.content, "html.parser")
        self.stats["username"] = self.username
        self.stats["region"] = self.region
        self.personal_ratings()

    def personal_ratings(self):
        soloqueue_tier = self.soup.find(
            "span", class_="leagueTier").text.strip()
        if soloqueue_tier == "Unranked":
            soloqueue_rank = None
            soloqueue_wins = None
            soloqueue_losses = None
            soloqueue_lp = None


        else:
            soloqueue_rank = self.soup.find(
                "span", class_="highlight").text.strip()
            soloqueue_wins = self.soup.find(
                "span", class_="wins").text.strip().split()[1]
            soloqueue_losses = self.soup.find(
                "span", class_="losses").text.strip().split()[1]
            soloqueue_lp = self.soup.find(
                "div", class_="league-points").text.strip().split()[1]

        if self.soup.find("div", class_="medium-24 columns queueName text-left show-for-light-only"):
            flex_control = self.soup.find("div", class_="other-league-content")
            flex_tier = flex_control.find(
                "div", class_="medium-14 columns leagueTier").text.strip()
            flex_rank = flex_control.find(
                "span", class_="highlight-dark-only").text.strip()
            flex_wins = flex_control.find(
                "span", class_="wins").text.strip().split()[1]
            flex_losses = flex_control.find(
                "span", class_="losses").text.strip().split()[1]
            flex_lp = flex_control.find(
                "div", class_="medium-8 small-4 columns text-right").text.strip().split()[1]
        else:
            flex_tier = "Unranked"
            flex_rank = None
            flex_wins = None
            flex_losses = None
            flex_lp = None

        average_enemies_rating = None
        if self.soup.find("div", class_="leagueTier no-margin-bottom"):
            average_enemies_rating = self.soup.find(
                "div", class_="leagueTier no-margin-bottom").text.strip()

        self.stats["stats"] = {"soloqueue": {"tier": soloqueue_tier, "rank": soloqueue_rank,
                                             "wins": soloqueue_wins, "losses": soloqueue_losses, "lp": soloqueue_lp},
                               "flex":     {"tier": flex_tier, "rank": flex_rank,
                                            "wins": flex_wins, "losses": flex_losses, "lp": flex_lp},
                               "average_enemies_rating": average_enemies_rating}
        return self.stats




if __name__ == "__main__":
    lol = LOL("MANTARIMA BASMA")

    print(lol.stats)
from earthquake.fetch_earthquake import earthquake_list, getDistanceBetweenPointsNew
from github.github import Follow
from standings.standing import standing_list
from currency.currency import currency_reply
from youtube.youtube import YT
from ramadan.iftar_sehri import Ramadan


class Response:

    def message_reply():
        ...

    def last_ten_earthquake(self):
        """
        commandHandler = /earthquake
        """
        reply = ""
        for count, earthquake in enumerate(earthquake_list):
            if count > 9:
                break
            else:
                reply += f"\nTarih: {earthquake.date}\nYer: {earthquake.location}\nSaat: {earthquake.time}\nDerinlik: {earthquake.depth}\n\
Enlem: {earthquake.latitude} - Boylam: {earthquake.longitude}\nŞiddet: {earthquake.MD} MD,  {earthquake.ML} ML\
,  {earthquake.MW} MW\nNitelik: {earthquake.control}\n{'-'*10}"
        return reply

    def standing(self):
        reply = "Club              W   D   L  GD"
        for team in standing_list:
            club_name = team[1]
            reply += "\n"+team[0]+"-"+club_name+(" "*(17-(len(club_name)+len(
                str(team[0])))))+team[5]+"   "+team[6]+"   "+team[7]+"    "+team[10]
        return reply

    def near_earthquakes(self, city_name):
        """
        messageHandler = -earthquake/<cityName>
        """
        reply = ""
        near_list = []
        for earthquake in earthquake_list:
            control = getDistanceBetweenPointsNew(
                latitude1=earthquake.latitude, longitude1=earthquake.longitude, city=city_name)
            if control:
                if control < 200:
                    near_list.append(earthquake)
            else:
                return "City not found !"

        if near_list:
            for earthquake in near_list[:10]:
                reply += f"\nTarih: {earthquake.date}\nYer: {earthquake.location}\nSaat: {earthquake.time}\nDerinlik: {earthquake.depth}\nEnlem: {earthquake.latitude} - Boylam: {earthquake.longitude}\nŞiddet: {earthquake.MD} MD,  {earthquake.ML} ML,  {earthquake.MW} MW\nNitelik: {earthquake.control}\n{'-'*10}"
            return reply
        else:
            return "Earthquake not found"

    def github_nonFollowers(self, username):
        """
        messageHandler = -github/<username>
        """
        tracker = Follow(username)
        response = tracker.non_followers()
        return response

    def currency(self):
        """
        commandHandler = /currency
        """
        return currency_reply

    def reply_video_datas(self, URL, chat_id):
        """
        messageHandler = -audio/<YouTubeLink>
        """
        yt = YT(URL=URL, chat_id=chat_id)
        datas = yt.video_context()
        reply = f"<b>Title</b>: {datas.get('title')}\n<b>Author</b>: {datas.get('author')}\n<b>Channel Url</b>: {datas.get('channel_url')}\n\
<b>Thumbnail</b>: {datas.get('img_url')}\n<b>Length</b>: {datas.get('length')}s\n<b>Description</b>:\n{datas.get('description')}"
        return reply, datas.get("title")
    
    def send_media(self, URL, chat_id, type):
        """
        messageHandler = -audio/<YouTubeLink>
                        ||
        messageHandler = -video/<YouTubeLink>              
        """
        yt = YT(URL=URL, chat_id=chat_id)
        if type == "video":
            yt.video_downloader()
        else:
            yt.audio_downloader()

    def send_ramadan_infos(self, city):
        """
        messageHandler = -ramadan/<cityName>
        """
        tracker = Ramadan(city=city)
        r = tracker.responses()
        return f"To iftar: {r['to_iftar']}\nTo sehri: {r['to_sehri']}"
    





if __name__ == "__main__":
    res = Response()
    print(res.standing())

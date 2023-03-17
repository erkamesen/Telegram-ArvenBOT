from pytube import YouTube
from pytube.exceptions import PytubeError
import os


class YT():

    def __init__(self, URL, chat_id):
        self.current_path = os.getcwd()
        self.URL = URL
        self.chat_id = chat_id
        self.title = self.get_title()

    def video_downloader(self):
        downloader = YouTube(self.URL)
        os.chdir(self.current_path)
        os.chdir(f"{self.current_path}/youtube/video")
        try:
            os.mkdir(str(self.chat_id))
        except FileExistsError:
            pass
        downloader.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(
            output_path=f"{self.current_path}/youtube/video/{str(self.chat_id)}", filename=f"{self.title}.mp4")

    def audio_downloader(self):
        downloader = YouTube(self.URL)
        os.chdir(self.current_path)
        os.chdir(f"{self.current_path}/youtube/audio")
        try:
            os.mkdir(str(self.chat_id))
        except FileExistsError:
            pass
        downloader.streams.filter(mime_type="audio/mp4").first().download(
            output_path=f"{self.current_path}/youtube/audio/{str(self.chat_id)}", filename=f"{self.title}.mp4")
    

    def video_context(self):
        datas = {}
        data = YouTube(self.URL)

        try:
            datas["length"] = data.length
        except PytubeError:
            datas["length"] = "Unknown"
        try:
            datas["author"] = data.author
        except PytubeError:
            datas["author"] = "Unknown"
        try:
            datas["title"] = data.title
        except PytubeError:
            datas["title"] = "Unknown"
        try:
            if len(data.description) > 200:
                datas["description"] = data.description[:400]+"..."
            else:
                datas["description"] = data.description
        except PytubeError:
            datas["description"] = "Unknown"
        try:
            datas["img_url"] = data.thumbnail_url
        except PytubeError:
            datas["img_url"] = "Unknown"
        try:
            datas["channel_url"] = data.channel_url
        except PytubeError:
            datas["channel_url"] = "Unknown"

        return datas
    
    def get_title(self):
        t = YouTube(self.URL)
        return t.title




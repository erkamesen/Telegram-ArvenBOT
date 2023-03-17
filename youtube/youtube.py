from pytube import YouTube

class YT():
    
    def __init__(self, URL):
        self.URL = URL

    def video_downloader(self):
        downloader = YouTube(self.URL)
        downloader.streams.filter(progressive=True, resolution="720p").first().download(output_path="/home/erkam/Files/Scraper/Telegram Bot/youtube/audio")

    def audio_downloader(self):
        downloader = YouTube(self.URL)
        t = downloader.streams.filter(only_audio=True).all()
        t[0].download()



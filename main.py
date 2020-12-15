import vlc
import pafy
import time
import random
import multiprocessing as mp
import json

import requests

import detector

VIDEO_URLS_URL = "https://raw.githubusercontent.com/Snarik/LabPeephole/main/video_urls.json"

def main():
    
    sub_process = mp.Process(target=detector.human_detector)
    sub_process.start() 

    while True: 
        video_urls= json.loads(requests.get(VIDEO_URLS_URL).text)
        video = pafy.new(random.choice(video_urls))

        best = video.getbest()
        media = vlc.MediaPlayer(best.url)
        print("created the media object: {}".format(media))
        media.set_fullscreen(True)

        media.play()
        print("attempted to play the media: {}".format(media.get_state()))
        while media.get_state() == vlc.State.Opening:
            time.sleep(5)
            
        while media.is_playing():
            time.sleep(10)
        media.stop()
if __name__ == "__main__":
    main()

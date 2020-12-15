import vlc
import pafy
import time
import random
import multiprocessing as mp

import detector

GOOD_VIDEOS=["https://www.youtube.com/watch?v=lM02vNMRRB0",
             "https://www.youtube.com/watch?v=7S7smPw9EiE",
             "https://www.youtube.com/watch?v=lM02vNMRRB0",
             "https://www.youtube.com/watch?v=HSsqzzuGTPo",
             "https://www.youtube.com/watch?v=IdejM6wCkxA",
             "https://www.youtube.com/watch?v=72kRM86V-dw",
             "https://www.youtube.com/watch?v=6qGiXY1SB68",
             "https://www.youtube.com/watch?v=QmEyLmioHJY",
             "https://www.youtube.com/watch?v=vHr4qSQ-5XU",
             "https://www.youtube.com/watch?v=1aqM14CYb4Y",
             "https://www.youtube.com/watch?v=4It9yQSjaGA",
             "https://www.youtube.com/watch?v=6XZOgg9WRhI",
             "https://www.youtube.com/watch?v=OKAYqzOfLjY",
             "https://www.youtube.com/watch?v=ftlvreFtA2A",
             "https://www.youtube.com/watch?v=rpeOOYpvEuo",
             "https://www.youtube.com/watch?v=8LKjoo6FRkg",
             "https://www.youtube.com/watch?v=0txBFbAuhLY",
             "https://www.youtube.com/watch?v=XKU17jsdH0U",
             "https://www.youtube.com/watch?v=kV9qndEs3Nk",
             "https://www.youtube.com/watch?v=XqrWHwQNtwk",   
        ]
def main():
    
    sub_process = mp.Process(target=detector.human_detector)
    sub_process.start() 

    while True: 
        video = pafy.new(random.choice(GOOD_VIDEOS))

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

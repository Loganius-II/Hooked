from pygame import mixer, time
from time import sleep
from threading import Thread
import random

mixer.pre_init(44100, -16, 2, 2048)
mixer.init()

def switch_song(next_song):
    mixer.music.set_volume(1)
    volume = 1

    for _ in range(10):
        volume -= 0.1
        sleep(0.1)
        mixer.music.set_volume(volume)
    
    mixer.music.stop()

    mixer.music.load(next_song)
    mixer.music.play()

    for _ in range(10):
        volume += 0.1
        sleep(0.1)
        mixer.music.set_volume(volume)


def play_theme():
    mixer.music.load('MusicAndSFX/Mambo Inn.ogg')
    mixer.music.set_volume(0.6)
    mixer.music.play(fade_ms=800)

def play_random_song():
    #mixer.music.fadeout(2000)
    
    paths = ['We the People.mp3','Giant Steps.mp3', 'Iroquois.mp3']
    Thread(target=switch_song, args=(f'MusicAndSFX/{random.choice(paths)}',)).start()

def enter_sea():
    #mixer.music.fadeout(2000)  # fade OUT current song over 2s
    Thread(target=switch_song, args=("MusicAndSFX/Li'l Darlin' 1994.mp3",)).start()



def badadadink():
    # misc sound effect
    # going to be used multiple times

    s = mixer.Sound('MusicAndSFX/badadadink.ogg')
    s.set_volume(0.6)
    s.play()

def menubum():
    # plays a bum sound
    # misc effect

    mixer.Sound('MusicAndSFX/menubum.mp3').play()

def buttonclicked():
    # plays when button is clicked

    mixer.Sound('MusicAndSFX/buttonclicked.mp3').play()

def pop():
    # plays when button is clicked

    mixer.Sound('MusicAndSFX/pop.mp3').play()

def whoosh():
    # plays random of two woosh sounds

    w = ['MusicAndSFX/whoosh1.mp3', 'MusicAndSFX/whoosh2.mp3']

    w = mixer.Sound(random.choice(w))
    w.set_volume(1.2)

    w.play()

def click():
    # plays little clicky sound
    s = mixer.Sound('MusicAndSFX/click.mp3')
    s.set_volume(10)
    s.play()

def play_man_talking():
    rand_path = random.choice(['talking1.mp3', 'eblanizhe.wav', 'blydon.wav', 'davalka.wav'])

    s = mixer.Sound(f'MusicAndSFX/{rand_path}')
    s.set_volume(1.3)
    s.play()

def play_woman_talking():
    s = mixer.Sound(f'MusicAndSFX/germanwoman.wav')
    s.set_volume(1.3)
    s.play()

def woman_yes():
    s = mixer.Sound(f'MusicAndSFX/yes.mp3')
    s.set_volume(1.3)
    s.play()

def woman_rejected():
    s = mixer.Sound(f'MusicAndSFX/rejected.wav')
    s.set_volume(1.3)
    s.play()

def reel():
    # plays the reely sound
    # returns the sound object to stop it when you exit the ui

    s = mixer.Sound('MusicAndSFX/reel.mp3')
    s.play()

    return s

def error():
    mixer.Sound('MusicAndSFX/error.mp3')
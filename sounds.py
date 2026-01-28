from pygame import mixer, time
from time import sleep
from threading import Thread
import random

mixer.pre_init(44100, -16, 2, 2048)
mixer.init()

def play_theme():
    mixer.music.load('MusicAndSFX/Mambo Inn.ogg')
    mixer.music.set_volume(0.6)
    mixer.music.play(fade_ms=800)

def enter_sea():
    mixer.music.fadeout(2000)  # fade OUT current song over 2s
    sleep(2)    # wait for fade to finish

    mixer.music.load("MusicAndSFX/Li'l Darlin' 1994.mp3")
    mixer.music.play(fade_ms=2000)  # fade IN new song


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

def reel():
    # plays the reely sound
    # returns the sound object to stop it when you exit the ui

    s = mixer.Sound('MusicAndSFX/reel.mp3')
    s.play()

    return s

def error():
    mixer.Sound('MusicAndSFX/error.mp3')
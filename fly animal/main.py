from engine import introscreen
from engine import gameplay

def main():
    isGameQuit = introscreen()
    if not isGameQuit:
        gameplay()

main()
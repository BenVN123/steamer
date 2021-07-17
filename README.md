# steamer

**steamer** is a tool written in python for gamers to find Steam games that were made for them.

**[Steam](https://store.steampowered.com/)** is a popular distributing platform by Valve Corporation mainly used for video games.

## Why?

"Why would I use this if I just have the official Steam store?", you may ask. Well, there isn't a real reason. I just thought it'd be fun to do this little project.

## Installation
```
git clone https://github.com/BenVN123/steamer.git
cd steamer
pip install -r requirements.txt
```

## Usage
```
py -m steamer -h
usage: steamer.py [-h] [-s S] [-p P] [-g G] [-q Q] [-t T] [-v]

steamer - Find steam games meant for you | v0.0.0

optional arguments:
  -h, --help  show this help message and exit
  -s S        Specify minimum discount percentage [Default : 0]
  -p P        Specify maximum game price [Default : infinite]
  -g G        Search term(s) seperated by ", " [Default : None]
  -q Q        Maximum number of search results [Default : 50]
  -t T        Specify timeout [Default : 20]
  -v          Prints version
```

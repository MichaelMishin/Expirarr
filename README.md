# last-call-posters

*Project inspired by *[Maintainerr Overlay Helperr](https://github.com/gssariev/maintainerr-overlay-helperr) recreated in Python 

A Python app to automatically update Plex posters with a "Leaving Soon" badge for shows about to be removed based on [Maintainerr](https://github.com/jorenn92/Maintainerr).

## Features
- Sync with Plex using `plexapi`
- Download current posters
- Overlay a "Leaving Soon" banner
- Upload updated posters back to Plex

## Setup
```bash
git clone https://github.com/yourname/LastCallPosters.git
cd LastCallPosters
cp .env.example .env
# Fill in your .env with Plex details
pip install -r requirements.txt
python -m lastcallposters.main
```

## Environment Variables
```
PLEX_URL=http://your-plex-ip:32400
PLEX_TOKEN=your-plex-token
LIBRARY_NAME=TV Shows
TEST_MODE=true  # Set to false to enable Plex uploads
```

## Docker
```bash
docker build -t lastcallposters .
docker run --env-file .env lastcallposters
```

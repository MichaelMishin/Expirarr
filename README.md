# Expirarr

*Project inspired by [Maintainerr Overlay Helperr](https://github.com/gssariev/maintainerr-overlay-helperr) recreated in Python*

A Python app to automatically update Plex posters with a "Leaving Soon" badge for shows about to be removed based on [Maintainerr](https://github.com/jorenn92/Maintainerr).

## Features
- Sync with Plex using `plexapi`
- detects last date from Maintainerr collections "deleteAfterDays" 
- Download current posters
- Overlay a "Leaving >>DATE<<" banner
- Upload updated posters back to Plex
- Configurable schedule and "run on start" option
- Docker and Docker Compose support

## Setup (Manual)
```bash
git clone https://github.com/MichaelMishin/Expirarr.git
cd Expirarr
pip install -r requirements.txt
cp config/config.example.yaml config/config.yaml
# Edit config/config.yaml with your Plex and Maintainerr details
python -m expirarr.main
```

## Configuration

Edit `config/config.yaml` with your details. Example:
```yaml
plex:
  url: http://your-plex-ip:32400
  token: your-plex-token

maintainerr:
  url: http://your-maintainerr-ip:6246
  api_key: your-maintainerr-api-key

# Optional settings
test_mode: false         # Set to true to run without applying changes to Plex
run_on_start: true       # Run the task immediately on container/app start
cron_schedule: "0 0 * * *"  # Cron schedule (default: every day at midnight)

badge_customization:
  text_scale: 0.04
  padding_scale: 0.02
  corner_radius_scale: 0.02

text_positioning:
  horizontal_align: left
  vertical_align: bottom
  horizontal_offset_scale: 0.015
  vertical_offset_scale: 0.015
```
- `plex.url` and `maintainerr.url` must be valid URLs.
- `plex.token` and `maintainerr.api_key` must not be left as placeholders.

## Docker

Build and run with Docker:
```bash
docker build -t expirarr .
docker run -v $(pwd)/config:/app/config -v $(pwd)/data:/app/data expirarr
```

## Docker Compose

Example `docker-compose.yml`:
```yaml
version: '3.8'
services:
  expirarr:
    image: michaelmishin/expirarr:latest
    container_name: expirarr
    working_dir: /app
    volumes:
      - /mnt/SpeedVault/Apps/dockerApps/expirarr/config:/app/config
      - /mnt/SpeedVault/Apps/dockerApps/expirarr/data:/app/data
    command: ["python", "-u", "-m", "expirarr.main"]
```

### Using Docker Compose

1. Place your `docker-compose.yml` in your desired directory.
2. Make sure the `config` directory contains your `config.yaml` (or let the container auto-create it from the example on first run).
3. Start the service:
   ```bash
   docker compose up -d
   ```
4. View logs:
   ```bash
   docker logs expirarr
   ```

## Notes

- The container will copy a default `config.yaml` if one does not exist in your mounted config directory.
- All print/log output is unbuffered and visible in Docker logs.
- Fonts used for badge overlays are included in the image (`fonts/` directory).

## Troubleshooting

- Ensure your `config.yaml` is filled out and not using placeholder values.
- Check Docker logs for validation errors or missing configuration.
- For immediate task execution on container start, set `run_on_start: true` in your config.

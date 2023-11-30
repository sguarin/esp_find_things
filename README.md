# Introduction

Gets SSID/Password and BSSID from ESP* firmware binary files.

# Usage

Optional if you want to run it in a container environment:

```bash
podman run -ti --rm --volume $(pwd):/src:Z --workdir /src library/python:3.11 /bin/bash
```

```bash
pip install -r requirements.txt
python3 esp_find_things.py <firmware.bin>
```

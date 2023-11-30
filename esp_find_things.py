import sys
import os
import re
import binascii
import mac_vendor_lookup
import requests

FILENAME = sys.argv[1]
#FILENAME = "lamp-nvs.bin"

GOOGLE_API_TOKEN = os.getenv("GOOGLE_API_TOKEN")

def get_geo_by_bssid(bssid, token):
    ret = ""
    try:
        bssid2 = ':'.join(re.findall('.{2}', bssid))
        url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={token}"
        json = {
            "considerIp": "false",
            "wifiAccessPoints": [
                {"macAddress": bssid2},
                {"macAddress": "00:25:9c:cf:1c:ad"}
            ]
        }
        response = requests.post(url, json = json)
        if (response.status_code == 200):
            json_response = response.json()
            ret = f"https://www.google.com/maps/search/?api=1&query={json_response['location']['lat']},{json_response['location']['lng']}"
    except:
        print("Warning, google appi returnet error", file=sys.stderr)
        #raise

    return ret

file = open(FILENAME, "rb")
content = file.read()

r_ssid = re.compile(rb"([a-zA-Z0-9]{4,})(\x00+)")
r_password = re.compile(rb"([a-zA-Z0-9]{8,})(\x00+)")
pos = 0
while (result := r_ssid.search(content[pos:])):
    pos = pos + result.end(0)
    if len(result.group(0)) == 32:
        ssid = result.group(1)
        if (result2 := r_password.search(content[pos:pos+64])) and len(result2.group(0)) == 64:
            password = result2.group(1)
            print(f"SSID={str(ssid, encoding='utf-8')} PASSWORD={str(password, encoding='utf-8')}")
            break

#r_mac = re.compile(rb"(.{6})(\x03\|\x0B|\x0F)")
r_mac = re.compile(rb"(.{6})(\x0B|\x0F)")
macs = set()
pos = 0
while (result := r_mac.search(content[pos:])):
    pos = pos + result.start(0) + 1
    bssid = result.group(1)
    macs.add(str(binascii.b2a_hex(bssid), encoding='utf-8'))

mac = mac_vendor_lookup.MacLookup()
mac.update_vendors()
for x in macs:
    try:
        vendor = mac.lookup(x)
    except mac_vendor_lookup.VendorNotFoundError:
        vendor = ""
    geo = get_geo_by_bssid(x, GOOGLE_API_TOKEN)
    print(f"BSSID={x} VENDOR={vendor} GEO={geo}")

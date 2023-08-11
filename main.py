import yaml

import m3u_parser
import epg_parser

# http://epg.51zmt.top:8000/e.xml
# https://live.fanmingming.com/e.xml

with open("./manifest.yaml") as f:
    manifest = yaml.safe_load(f)
    playlist = m3u_parser.load_from_url(manifest['m3u'])
    epg = epg_parser.load_from_url(manifest['epg'])
    channels = {}
    for track in playlist['tracks']:
        channels[track['name']] = track
    
    for channel in manifest['playlist']:
        id = channel['id']
        name = channel['name']
        tvgId = channel['tvg-id']
        tvgName = channel['tvg-name']
        location = channels[name]['location']
        programme = epg[id]
        print(tvgId, tvgName, location)
        for x in programme['programmes']:
            print(x)

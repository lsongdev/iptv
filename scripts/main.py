import m3u_parser
import epg_parser

# http://epg.51zmt.top:8000/e.xml
# https://live.fanmingming.com/e.xml

result = m3u_parser.load_from_url("https://live.fanmingming.com/tv/m3u/global.m3u")
epg = epg_parser.load_from_url(result['metadata']['x-tvg-url'])

for track in result['tracks']:
    id = track["name"]
    if 'tvg-id' in track['attrs']:
        id = track['attrs']['tvg-id']
    print(track['name'], id in epg)
import requests
import xml.etree.ElementTree as xml


def parse_epg(data):
    root = xml.fromstring(data)
    channels = {}
    for channel in root.findall("channel"):
        channel_id = channel.get("id")
        display_name = channel.find("display-name")
        channels[channel_id] = {
            "id": channel_id,
            "name": display_name.text,
            "programmes": [],
        }

    for programme in root.findall("programme"):
        channel_id = programme.get("channel")
        start_time = programme.get("start")
        stop_time = programme.get("stop")
        title = programme.find("title")
        desc = programme.find("desc")
        programme_data = {
            "start_time": start_time,
            "stop_time": stop_time,
            "title": title.text,
            "desc": desc.text if desc is not None else "",
        }
        channels[channel_id]["programmes"].append(programme_data)

    return channels

def load_from_url(url):
    resp = requests.get(url)
    return parse_epg(resp.content.decode("utf8"))

import requests
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement

def parse_epg(data):
    root = ElementTree.fromstring(data)
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
        title = programme.find("title")
        desc = programme.find("desc")
        programme_data = {
            "start": programme.get("start"),
            "stop": programme.get("stop"),
            "title": title.text,
            "desc": desc.text if desc is not None else "",
        }
        channels[channel_id]["programmes"].append(programme_data)

    return channels


def load_from_url(url):
    resp = requests.get(url)
    return parse_epg(resp.content.decode("utf8"))


def generate_epg(data):    
    root = Element("tv")
    for id, channel in data.items():
        name = channel["name"]
        channel_element = SubElement(root, "channel", {"id": id })
        SubElement(channel_element, "display-name", {"lang": "zh"}).text = name
        for programme in channel["programmes"]:
            programme_element = SubElement(root, "programme",
                {
                    "channel": id,
                    "start": programme["start"],
                    "stop": programme["stop"],
                },
            )
            SubElement(programme_element, "title", {"lang": "zh"}).text = programme["title"]
            if programme["desc"]:
                SubElement(programme_element, "desc", {"lang": "zh"}).text = programme["desc"]
    xml_str = ElementTree.tostring(root, encoding='utf-8')
    prettified_xml_str = minidom.parseString(xml_str).toprettyxml(indent="  ")
    return prettified_xml_str

def write_epg(filename, data):
    with open(filename, 'w') as f:
        f.write(generate_epg(data))
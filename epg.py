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


def generate_epg(data):
    lang = "zh"
    root = Element("tv")
    for channel in data:
        id = channel["id"]
        name = channel["name"]
        channel_element = SubElement(root, "channel", {"id": id})
        SubElement(channel_element, "display-name", {"lang": lang}).text = name
        for programme in channel["programmes"]:
            programme_element = SubElement(
                root,
                "programme",
                {
                    "channel": id,
                    "start": programme["start"],
                    "stop": programme["stop"],
                },
            )
            SubElement(programme_element, "title", {"lang": lang}).text = programme[
                "title"
            ]
            if programme["desc"]:
                SubElement(programme_element, "desc", {"lang": lang}).text = programme[
                    "desc"
                ]

    xml_str = ElementTree.tostring(root, encoding="utf-8")
    prettified_xml_str = minidom.parseString(xml_str).toprettyxml(indent="  ")
    return prettified_xml_str


def write_epg(filename, data):
    with open(filename, "w") as f:
        f.write(generate_epg(data))


def load_from_url(url):
    resp = requests.get(url)
    return parse_epg(resp.content.decode("utf8"))

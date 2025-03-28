import re, requests


def parse_attributes(data):
    attrs = {}
    regex = re.compile(r'([\w-]+)="(.*?)"')
    matches = regex.findall(data)
    for key, value in matches:
        attrs[key] = value.replace('"', "")
    return attrs


def parse_extinf(data):
    track = {}
    regex = re.compile(r"^(-?\d+)(\s.+)?,(\s?.*)$")
    match = regex.match(data)
    if match:
        duration, extra_attrs, channel_name = match.groups()
        track["name"] = channel_name
        track["duration"] = int(duration)
        track["attrs"] = parse_attributes(extra_attrs or "")
    return track


def parse_m3u(m3u_data):
    tracks = []
    metadata = {}
    lines = m3u_data.strip().split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("#EXTM3U"):
            metadata.update(parse_attributes(line[len("#EXTM3U ") :]))
        elif line.startswith("#EXTINF"):
            track = parse_extinf(line[len("#EXTINF ") :])
        elif line.startswith("#EXTGRP"):
            track["group"] = line[len("#EXTGRP ") :]
        elif line and not line.startswith("#"):
            track["location"] = line
            tracks.append(track)
            track = {}
    return {"metadata": metadata, "tracks": tracks}


def load_from_url(url):
    resp = requests.get(url)
    return parse_m3u(resp.text)


def generate_m3u(data):
    output = "#EXTM3U " + " ".join(
        [f'{key}="{value}"' for key, value in data["metadata"].items()]
    )
    output += "\n"
    for track in data["tracks"]:
        duration = track.get("duration", -1)
        attrs_str = " ".join(
            [f'{key}="{value}"' for key, value in track["attrs"].items()]
        )
        output += f"#EXTINF:{duration} {attrs_str},{track['name']}\n"
        output += f"{track['location']}\n"
    return output


def write_m3u(filename, data):
    with open(filename, "w") as f:
        f.write(generate_m3u(data))

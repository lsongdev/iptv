#!/usr/bin/env python3

import yaml
import m3u
import epg


def load_configuration(filename="./manifest.yaml"):
    with open(filename) as f:
        return yaml.safe_load(f)


def build_channel_data(m, e, manifest):
    m3u_data = {"metadata": {}, "tracks": []}

    epg_data = {}
    channels = {track["name"]: track for track in m["tracks"]}
    for channel in manifest["playlist"]:
        tvgId = channel["tvg-id"]
        tvgName = channel["tvg-name"]
        name = channel["m3u-filter"]
        location = channels[name]["location"]
        c = e[channel["epg-filter"]]
        c["name"] = tvgName
        epg_data[tvgId] = c
        m3u_data["tracks"].append(
            {
                "name": tvgName,
                "location": location,
                "attrs": {"tvg-id": tvgId, "tvg-name": tvgName, "group-title": "央视"},
            }
        )

    return m3u_data, epg_data


def main():
    manifest = load_configuration()
    m = m3u.load_from_url(manifest["m3u"])
    e = epg.load_from_url(manifest["epg"])
    m3u_data, epg_data = build_channel_data(m, e, manifest)
    m3u.write_m3u("tv.m3u", m3u_data)
    epg.write_epg("epg.xml", epg_data)


if __name__ == "__main__":
    main()

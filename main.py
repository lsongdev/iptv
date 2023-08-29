#!/usr/bin/env python3

import yaml
import m3u
import epg

def main():
    m = m3u.load_from_url("https://live.fanmingming.com/tv/m3u/global.m3u")
    for x in m["tracks"]:
        print(x["name"], x["location"])
    

if __name__ == "__main__":
    main()

import epg
import m3u
import yaml


def load_manifest(manifest_file):
    with open(manifest_file, "r") as f:
        return yaml.safe_load(f)


def filter_and_customize_tracks(m3u_tracks, epg_data, playlist_config):
    output_m3u = []
    output_epg = []

    for config in playlist_config:
        filter_name = config["filter"]
        selected_track = m3u_tracks.get(filter_name)

        if not selected_track:
            print(f"Warning: No track found for filter: {filter_name}")
            continue

        # Customize the track and program based on the config
        customized_track = {
            "name": config["tvg-name"],
            "location": selected_track["location"],
            "attrs": {
                "tvg-id": config["tvg-id"],
                "tvg-name": config["tvg-name"],
                "tvg-logo": f"logo/{config['tvg-id']}.png",
                "group-title": config["group-title"],
            },
        }
        output_m3u.append(customized_track)

        if "tvg-id" in selected_track["attrs"]:
            id = selected_track["attrs"]["tvg-id"]
            program = epg_data.get(id)
            if not program:
                print(f"Warning: No EPG data found for ID: {id}")
            customized_program = program.copy()
            customized_program["id"] = config["tvg-id"]
            customized_program["name"] = config["tvg-name"]
            output_epg.append(customized_program)
        else:
            print(f"Warning: No tvg-id found for track: {filter_name}")
    
    return output_m3u, output_epg


def main():
    manifest = load_manifest("./manifest.yaml")
    m3u_data = m3u.load_from_url(manifest["m3u"])
    epg_data = epg.load_from_url(manifest["epg"])
    m3u_tracks = {track["name"]: track for track in m3u_data["tracks"]}
    output_m3u, output_epg = filter_and_customize_tracks(
        m3u_tracks, epg_data, manifest["playlists"]
    )
    # Convert output_m3u to the expected format for write_m3u
    output_m3u_data = {
        "metadata": {
            "x-tvg-url": "https://lsong.org/iptv/epg.xml",
        },
        "tracks": output_m3u,
    }
    # Save output_m3u to a new M3U file
    m3u.write_m3u("tv.m3u", output_m3u_data)
    epg.write_epg("epg.xml", output_epg)


if __name__ == "__main__":
    main()

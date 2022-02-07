
# set -x

check() {
  jq -r '.location' | while read link; do
    if curl -sL --connect-timeout 3 --max-time 3 "$link" | grep "#EXTM3U" &> /dev/null; then
      echo "$link"
    fi
  done
}

[[ -f tmp/cn.json ]] || curl -sL https://github.com/iptv-org/iptv/raw/master/channels/cn.m3u | m3u-parser > tmp/cn.json
cat templates/cctv.m3u | m3u-parser | jq -r '.items[].tvg.id' | while read tvgId; do
  echo "tvgId: $tvgId"
  cat tmp/cn.json | jq -r ".items[] | select(.tvg.id == \"$tvgId\")" | check > "tmp/$tvgId.links"
done

find tmp -name "*.links" -type f -size 0 -delete

echo "#EXTM3U" > channels/cn/cctv.m3u
ls tmp/*.links | while read f; do
  tvgId=$(basename $f .links);
  echo "tvgId: $tvgId"
  grep "tvg-id=\"$tvgId\"" templates/cctv.m3u >> channels/cn/cctv.m3u
  head -n1 "$f" >> channels/cn/cctv.m3u
done

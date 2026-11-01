import csv
import hashlib
import os
import sys
import time
from datetime import date
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests

RAW = "data/raw"
MANIFEST = "data/manifest.csv"
HEADERS = {
    "User-Agent": "ExamateStudentProject/1.0 (learning project)"
}
DELAY = 2
robots = {}


def allowed(url):
    root = "{0.scheme}://{0.netloc}".format(urlparse(url))

    if root not in robots:
        robots_url = root + "/robots.txt"
        rp = RobotFileParser()

        try:
            response = requests.get(
                robots_url,
                headers=HEADERS,
                timeout=10,
            )

            if response.status_code != 200:
                robots[root] = None
            else:
                rp.set_url(robots_url)
                rp.parse(response.text.splitlines())
                robots[root] = rp

        except requests.RequestException:
            robots[root] = None

    rp = robots[root]

    if rp is None:
        return False

    return rp.can_fetch(HEADERS["User-Agent"], url)


def name_for(url):
    name = os.path.basename(urlparse(url).path) or "index.html"
    return name.replace(" ", "_")


def main(list_file):
    os.makedirs(RAW, exist_ok=True)
    new_manifest = not os.path.exists(MANIFEST)

    with open(MANIFEST, "a", newline="") as mf:
        log = csv.writer(mf)

        if new_manifest:
            log.writerow(
                ["file", "source_url", "downloaded_on", "bytes", "sha256"]
            )

        with open(list_file) as fh:
            urls = [u.strip() for u in fh]

        for url in urls:
            if not url or url.startswith("#"):
                continue

            path = os.path.join(RAW, name_for(url))

            if os.path.exists(path):
                print("skip (already have)", path)
                continue

            if not allowed(url):
                print("BLOCKED by robots.txt, not downloading:", url)
                continue

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=30,
            )

            if response.status_code != 200:
                print("failed", response.status_code, url)
                continue

            with open(path, "wb") as file:
                file.write(response.content)

            digest = hashlib.sha256(response.content).hexdigest()[:16]

            log.writerow(
                [
                    path,
                    url,
                    date.today().isoformat(),
                    len(response.content),
                    digest,
                ]
            )

            print("saved", path, len(response.content), "bytes")
            time.sleep(DELAY)


if __name__ == "__main__":
    main(sys.argv[1])

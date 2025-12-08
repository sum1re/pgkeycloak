import requests
import os
import re

BASE_URL = "https://quay.io/api/v1/repository/keycloak/keycloak/tag/"
DOCKER_IMAGE_NAME = "sum1re/pgkeycloak"

def get_all_tags():
    tags = []
    page = 1
    while True:
        resp = requests.get(f"{BASE_URL}?page={page}")
        resp.raise_for_status()
        data = resp.json()
        ts = data.get("tags", [])
        if not ts:
            break
        tags.extend(ts)
        if len(ts) < data.get("page_size", len(ts)):
            break
        page += 1
    return tags

def find_tags_by_digest(target_tag):
    """Finds all tags sharing the same manifest digest as the target tag."""
    tags = get_all_tags()
    target_digest = None
    for t in tags:
        if t["name"] == target_tag:
            target_digest = t["manifest_digest"]
            break

    if not target_digest:
        raise ValueError(f"Tag {target_tag} not found")

    same_tags = [t["name"] for t in tags if t["manifest_digest"] == target_digest]
    return same_tags, target_digest

def set_github_output(target_tag="latest"):
    """
    Finds associated tags, formats them for Docker, and sets GitHub Actions outputs.
    """
    try:
        raw_tags, target_digest = find_tags_by_digest(target_tag)
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    formatted_tags = ",".join(f"{DOCKER_IMAGE_NAME}:{tag}" for tag in raw_tags)

    xyz_versions = [tag for tag in raw_tags if re.fullmatch(r'\d+\.\d+\.\d+$', tag)]

    main_version = sorted(xyz_versions, key=lambda v: [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', v)])[-1] if xyz_versions else ""

    if not main_version:
        print(f"::error::Could not find an X.Y.Z version tag in the raw tags: {raw_tags}")
        return 1

    output_file = os.environ.get('GITHUB_OUTPUT')
    if output_file:
        with open(output_file, 'a') as f:
            f.write(f"formatted_tags={formatted_tags}\n")
            f.write(f"main_version={main_version}\n")
            f.write(f"raw_tags_string={','.join(raw_tags)}\n")
            f.write(f"current_digest={target_digest}\n")

    print(f"Successfully detected tags: {formatted_tags}")
    print(f"Main version for ARG: {main_version}")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(set_github_output("latest"))
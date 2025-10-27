#!/usr/bin/env python3
import argparse
import os
import re
import sys
import time
from typing import Dict, List

import requests


FIGMA_API_BASE = "https://api.figma.com/v1"


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\-_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-") or "node"


def fetch_file_json(file_key: str, token: str) -> Dict:
    resp = requests.get(
        f"{FIGMA_API_BASE}/files/{file_key}",
        headers={"X-Figma-Token": token},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def collect_node_ids(node: Dict, collected: List[str], names: Dict[str, str]):
    node_type = node.get("type")
    node_id = node.get("id")
    node_name = node.get("name", "node")

    # Export common visual containers by default
    exportable_types = {
        "FRAME",
        "COMPONENT",
        "COMPONENT_SET",
        "GROUP",
        "INSTANCE",
        "RECTANGLE",
        "ELLIPSE",
        "VECTOR",
    }

    if node_id and node_type in exportable_types:
        collected.append(node_id)
        names[node_id] = node_name

    for child in node.get("children", []) or []:
        collect_node_ids(child, collected, names)


def export_images(file_key: str, token: str, node_ids: List[str], scale: float, out_dir: str, names: Dict[str, str]):
    os.makedirs(out_dir, exist_ok=True)

    # Figma images endpoint supports batching ids via comma-separated list
    batch_size = 75
    for i in range(0, len(node_ids), batch_size):
        batch = node_ids[i : i + batch_size]
        ids_param = ",".join(batch)
        params = {
            "ids": ids_param,
            "format": "png",
            "scale": str(scale),
        }
        resp = requests.get(
            f"{FIGMA_API_BASE}/images/{file_key}",
            headers={"X-Figma-Token": token},
            params=params,
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        images_map = data.get("images", {})

        for node_id, url in images_map.items():
            if not url:
                continue
            # Rate-limit a bit to be kind
            time.sleep(0.05)
            img_resp = requests.get(url, timeout=120)
            img_resp.raise_for_status()
            name_slug = slugify(names.get(node_id, node_id))
            out_path = os.path.join(out_dir, f"{name_slug}-{node_id}.png")
            with open(out_path, "wb") as f:
                f.write(img_resp.content)
            print(f"Saved {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Export images from a Figma file")
    parser.add_argument("--file-key", default="ycfU0or3PHCjVukujL4haE", help="Figma file key (from URL)")
    parser.add_argument("--token", default=os.getenv("FIGMA_TOKEN"), help="Figma personal access token")
    parser.add_argument("--scale", type=float, default=2.0, help="Export scale (1, 2, 3, ...)")
    parser.add_argument(
        "--out-dir",
        default=os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "farhan-rafat.github.io",
            "bashar-s-portfolio",
            "assets",
            "images",
            "figma",
        ),
        help="Output directory for exported images",
    )

    args = parser.parse_args()
    if not args.token:
        print("Error: Provide a Figma token via --token or FIGMA_TOKEN env var.", file=sys.stderr)
        sys.exit(1)

    print("Fetching Figma file structure...")
    file_json = fetch_file_json(args.file_key, args.token)
    document = file_json.get("document", {})

    node_ids: List[str] = []
    names: Dict[str, str] = {}
    collect_node_ids(document, node_ids, names)

    if not node_ids:
        print("No exportable nodes found.")
        return

    print(f"Exporting {len(node_ids)} nodes to {args.out_dir} at scale {args.scale}...")
    export_images(args.file_key, args.token, node_ids, args.scale, args.out_dir, names)
    print("Done.")


if __name__ == "__main__":
    main()


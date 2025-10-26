#!/usr/bin/env python3
"""
Script to check the availability of tool and room images for the Leiter firetruck.
This script analyzes the firetruck configuration and checks if the corresponding
image files exist in the assets directory.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Tuple


def tool_name_2image_name(tool_name: str) -> str:
    """
    Convert tool name to image filename convention.
    Same function as used in the main application.
    """
    return (
        tool_name.lower()
        .replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
        .replace('"', "")
        .replace("/", "")
        .replace(".", "")
    )


def remove_tool_tags(tool_name: str) -> str:
    """Remove image tags from tool name."""
    return tool_name.split("<Bild:")[0].split("<Raumbild:")[0].strip()


def isolate_tag_value(tool_name: str, tag: str) -> str:
    """Extract tag value and convert to proper file path."""
    if tag in tool_name:
        start = tool_name.index(tag) + len(tag)
        end = tool_name.index(">", start)
        tool_image_file_str = tool_name[start:end]
        return os.path.join(".", "assets", *tool_image_file_str.split("/")) + ".jpg"
    return ""


def load_firetruck_data(yaml_file: str) -> Dict:
    """Load firetruck data from YAML file."""
    with open(yaml_file, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def check_image_exists(image_path: str, base_dir: str) -> bool:
    """Check if image file exists."""
    full_path = os.path.join(base_dir, image_path.replace("./app/assets", ""))
    return os.path.exists(full_path)


def analyze_leiter_images(base_dir: str = "app") -> None:
    """
    Analyze Leiter firetruck configuration and check image availability.
    """
    # Paths
    yaml_file = os.path.join(base_dir, "content", "firetruck_tools_hallein.yaml")
    assets_dir = os.path.join(base_dir, "assets")

    # Load data
    # print("Loading firetruck configuration...")
    data = load_firetruck_data(yaml_file)

    if "Leiter" not in data:
        print("Error: Leiter firetruck not found in configuration!")
        return

    leiter_data = data["Leiter"]["Tools"]

    # print(f"\n{'='*80}")
    # print(f"IMAGE AVAILABILITY CHECK FOR LEITER FIRETRUCK")
    # print(f"{'='*80}")

    missing_tool_images = []
    missing_room_images = []
    found_tool_images = []
    found_room_images = []

    total_tools = 0

    # Analyze each room and its tools
    for room_key, tools in leiter_data.items():
        # print(f"\n📂 Room: {room_key}")
        # print("-" * 50)

        for tool in tools:
            total_tools += 1
            clean_tool_name = remove_tool_tags(tool)

            # print(f"\n🔧 Tool: {clean_tool_name}")

            # Check tool image
            tool_image_tag = isolate_tag_value(tool, "<Bild:")
            if tool_image_tag:
                tool_image_path = tool_image_tag
                # print(f"   📷 Tool image (from tag): {tool_image_path}")
            else:
                tool_image_name = tool_name_2image_name(clean_tool_name) + ".jpg"
                tool_image_path = f"./assets/tools/{tool_image_name}"
                # print(f"   📷 Tool image (auto): {tool_image_path}")

            # Check if tool image exists
            if check_image_exists(tool_image_path, base_dir):
                # print(f"   ✅ Tool image: FOUND")
                found_tool_images.append((clean_tool_name, tool_image_path))
            else:
                # print(f"   ❌ Tool image: MISSING")
                missing_tool_images.append((clean_tool_name, tool_image_path))

            # Check room image
            room_image_tag = isolate_tag_value(tool, "<Raumbild:")
            if room_image_tag:
                room_image_path = room_image_tag
                # print(f"   🏠 Room image (from tag): {room_image_path}")
            else:
                room_name = room_key.lower()
                if " / " in room_name:
                    room_name = "_".join(room_name.split(" / "))
                room_image_path = f"./assets/hallein_leiter/{room_name.lower()}.jpg"
                # print(f"   🏠 Room image (auto): {room_image_path}")

            # Check if room image exists
            if check_image_exists(room_image_path, base_dir):
                # print(f"   ✅ Room image: FOUND")
                found_room_images.append((clean_tool_name, room_image_path))
            else:
                # print(f"   ❌ Room image: MISSING")
                missing_room_images.append((clean_tool_name, room_image_path))

    # Summary
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"Total tools analyzed: {total_tools}")
    print(f"Tool images found: {len(found_tool_images)}")
    print(f"Tool images missing: {len(missing_tool_images)}")
    print(f"Room images found: {len(found_room_images)}")
    print(f"Room images missing: {len(missing_room_images)}")

    # Missing tool images details
    if missing_tool_images:
        print(f"\n❌ MISSING TOOL IMAGES ({len(missing_tool_images)}):")
        print("-" * 50)
        for tool_name, image_path in missing_tool_images:
            print(f"   • {tool_name}")
            print(f"     Expected: {image_path}")

    # Missing room images details
    if missing_room_images:
        print(f"\n❌ MISSING ROOM IMAGES ({len(missing_room_images)}):")
        print("-" * 50)
        for tool_name, image_path in missing_room_images:
            print(f"   • {tool_name}")
            print(f"     Expected: {image_path}")

    # Calculate percentages
    tool_percentage = (
        (len(found_tool_images) / total_tools) * 100 if total_tools > 0 else 0
    )
    room_percentage = (
        (len(found_room_images) / total_tools) * 100 if total_tools > 0 else 0
    )

    print(f"\n📊 COMPLETION RATES:")
    print(f"   Tool images: {tool_percentage:.1f}%")
    print(f"   Room images: {room_percentage:.1f}%")

    # # Create missing images report
    # report_file = "leiter_missing_images_report.txt"
    # with open(report_file, "w", encoding="utf-8") as f:
    #     f.write("LEITER FIRETRUCK - MISSING IMAGES REPORT\n")
    #     f.write("=" * 50 + "\n\n")

    #     f.write(f"Total tools: {total_tools}\n")
    #     f.write(f"Missing tool images: {len(missing_tool_images)}\n")
    #     f.write(f"Missing room images: {len(missing_room_images)}\n\n")

    #     if missing_tool_images:
    #         f.write("MISSING TOOL IMAGES:\n")
    #         f.write("-" * 30 + "\n")
    #         for tool_name, image_path in missing_tool_images:
    #             f.write(f"{tool_name}: {image_path}\n")
    #         f.write("\n")

    #     if missing_room_images:
    #         f.write("MISSING ROOM IMAGES:\n")
    #         f.write("-" * 30 + "\n")
    #         for tool_name, image_path in missing_room_images:
    #             f.write(f"{tool_name}: {image_path}\n")

    # print(f"\n📝 Report saved to: {report_file}")


def list_available_images():
    """List all available images in the assets directories."""
    print(f"\n{'='*80}")
    print(f"AVAILABLE IMAGES IN ASSETS")
    print(f"{'='*80}")

    # List tools images
    tools_dir = "app/assets/tools"
    if os.path.exists(tools_dir):
        print(f"\n📂 Tools directory ({tools_dir}):")
        tools_images = [f for f in os.listdir(tools_dir) if f.endswith(".jpg")]
        tools_images.sort()
        for img in tools_images:
            print(f"   • {img}")
        print(f"   Total: {len(tools_images)} images")

    # List hallein_leiter images
    leiter_dir = "app/assets/hallein_leiter"
    if os.path.exists(leiter_dir):
        print(f"\n📂 Hallein Leiter directory ({leiter_dir}):")
        leiter_images = [f for f in os.listdir(leiter_dir) if f.endswith(".jpg")]
        leiter_images.sort()
        for img in leiter_images:
            print(f"   • {img}")
        print(f"   Total: {len(leiter_images)} images")


if __name__ == "__main__":
    print("🚒 Leiter Firetruck Image Checker")
    # print("=" * 50)

    # Check if we're in the right directory
    if not os.path.exists("app"):
        print("❌ Error: Please run this script from the feuerwehr_app root directory")
        exit(1)

    # Run analysis
    analyze_leiter_images()

    # List available images
    # list_available_images()

    print("\n✅ Analysis complete!")

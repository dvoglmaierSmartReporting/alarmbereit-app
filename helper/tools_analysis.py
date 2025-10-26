from collections import defaultdict
import yaml
from pprint import pprint

# Load the YAML content to process
file_path = "./app/content/firetruck_tools.yaml"

# Loading the YAML file
with open(file_path, "r", encoding="utf-8") as file:
    data = yaml.safe_load(file)


# # Normalize function: To handle common differences (case, whitespace, hyphens)
# def normalize_string(s):
#     return (
#         s.lower()
#         .replace(" ", "")
#         .replace("-", "")
#         .replace("ü", "u")
#         .replace("ä", "a")
#         .replace("ö", "o")
#         .replace("ß", "ss")
#     )


def remove_tool_tags(tool_name: str) -> str:
    return tool_name.split("<Bild:")[0].split("<Raumbild:")[0].strip()


# Dictionary to store normalized names with their original strings
items_dict = defaultdict(list)
item_list = list()


# Traverse YAML data recursively to collect item names
def collect_items(data, items_dict):
    if isinstance(data, dict):
        for value in data.values():
            collect_items(value, items_dict)
    elif isinstance(data, list):
        for item in data:
            # normalized = normalize_string(item)
            # items_dict[normalized].append(item)

            item_clean = remove_tool_tags(item)
            if item_clean not in item_list:
                item_list.append(item_clean)


# Run the function on the loaded data
# collect_items(data, items_dict)
collect_items(data, item_list)

# Find items with different descriptions by checking if there are multiple original strings for a normalized string
# inconsistent_items = {key: set(val) for key, val in items_dict.items() if len(val) > 1}
# inconsistent_items = {key: set(val) for key, val in items_dict.items()}

# pprint(inconsistent_items, width=100)
item_list.sort()

# pprint(item_list, width=100)

for item in item_list:
    print(item)

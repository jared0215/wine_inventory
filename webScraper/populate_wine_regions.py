import json
import requests
from bs4 import BeautifulSoup

# Define the URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_wine-producing_regions"

# Send a GET request to the URL
response = requests.get(url)

# Parse the content with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Define a dictionary to store the hierarchy
wine_regions = {}

# Function to recursively process the list items


def process_list_items(ul_element):
    regions_dict = {}
    for li in ul_element.find_all('li', recursive=False):
        # Safely get the region or subregion name
        a_tag = li.find('a')
        if a_tag:
            region_name = a_tag.text.strip()
        else:
            continue  # Skip this li if it doesn't contain an a tag

        # Check if there is a nested list of subregions
        subregion_ul = li.find('ul')
        if subregion_ul:
            regions_dict[region_name] = process_list_items(subregion_ul)
        else:
            regions_dict[region_name] = []
    return regions_dict


# Find all the main regions/countries
main_regions = soup.find_all('h3')

for main_region in main_regions:
    country_name = main_region.text.strip()
    print(f"Processing {country_name}...")

    # Look for the nearest ul element, even if multiple elements down
    next_ul = main_region.find_next('ul')

    if next_ul:
        wine_regions[country_name] = process_list_items(next_ul)
    else:
        print(f"Warning: No regions list found for {country_name}")

# Display the hierarchical data
for country, regions in wine_regions.items():
    print(f"{country}:")
    for region, subregions in regions.items():
        print(f"  {region}:")
        if isinstance(subregions, dict):
            for subregion, microregions in subregions.items():
                print(f"    {subregion}:")
                if microregions:
                    for microregion in microregions:
                        print(f"      {microregion}")

# Assuming 'wine_regions' is your data structure
with open('wine_regions.json', 'w', encoding='utf-8') as f:
    json.dump(wine_regions, f, ensure_ascii=False, indent=4)

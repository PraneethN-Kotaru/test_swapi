from urllib.parse import urlparse

def get_species_id(species_url):
    # Parse the URL and split it to get the ID (last part)
    parsed_url = urlparse(species_url)
    # The ID is the last part of the URL path
    species_id = parsed_url.path.strip('/').split('/')[-1]
    return species_id
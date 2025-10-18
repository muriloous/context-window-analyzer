from nltk.data import find
from nltk.downloader import download

nltk_resources = [
    "punkt",
    "punkt_tab",
    "floresta"
]

def check_and_download(resource_list):
    for resource in resource_list:
      download(resource)

if __name__ == "__main__":
    check_and_download(nltk_resources)
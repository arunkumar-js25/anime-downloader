import requests
from bs4 import BeautifulSoup
from gogoanimelink import *
from Downloader import *

#MAIN
def main():
    searchInput = input("Enter Anime Name/URL : ")
    anime_search_results = GogoAnimeScraper.searchInGogoAnime(searchInput)
    [print(f'\t {i+1}) {anime_search_results[i][0]}') for i in range(len(anime_search_results))]

    selected_index = int(input('\nSelect your option: ')) - 1
    anime_scraper = GogoAnimeScraper(anime_search_results[selected_index][1])
    print("\nFOUND:", anime_scraper.episode_count, " Episodes in TOTAL!")

    start_ep = int(input("\nStart From Episode: "))
    end_ep = int(input("End At Episode: "))
    anime_scraper.scrapeEpisodes(start=start_ep, end=end_ep)

    print("\n-------------------- DOWNLOAD STARTED !!! --------------------")
    downloader = Downloader(anime_scraper.dataDict)
    downloader.downloadAnime()
    print("\n-------------------- DOWNLOAD COMPLETED !!! ------------------")

if __name__ == '__main__':
    main()

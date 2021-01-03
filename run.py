from gogoanimelink import *
from Downloader import *

def main():
    searchInput = input("\n>> Enter Anime Name/URL : ")
    anime_search_results = AnimeScraper.searchAnime(searchInput)
    [print(f'\t {i+1}) {anime_search_results[i][0]}') for i in range(len(anime_search_results))]

    selected_index = int(input('\n>> Select your option: ')) - 1
    anime_scraper = AnimeScraper(anime_search_results[selected_index][1])
    print("FOUND:", anime_scraper.episode_count, " Episodes in TOTAL!")
    print("="*40)
    start_ep = int(input(">> Start From Episode: "))
    end_ep = int(input(">> End At Episode: "))
    print("=" * 40)
    anime_scraper.scrapeEpisodes(start=start_ep, end=end_ep)
    print("=" * 40)

    print("DOWNLOAD STARTED !!! ------------------>")
    downloader = Downloader(anime_scraper.dataDict)
    #downloader.downloadAnime()
    print("DOWNLOAD COMPLETED !!! ---------------->")
    print("=" * 40)

if __name__ == '__main__':
    isconfig_done = "DONE"
    #islog_done = "DONE"

    try:
        configsetting('config.ini')
    except:
        isconfig_done = "FAILED"

    print("""\t"""+("="*33)
          +"""\n\t|\t|----------------------|\t|\n\t|\t|   ANIME Downloader   |\t|\n\t|\t|----------------------|\t|\n\t|\t Creator : """
          +str(config['about']['creator']).ljust(11,' ')+"""\t\t|\n\t|\t Version : """
          +str(config['about']['version']).ljust(11,' ')+"""\t\t|\t\n\t"""
          +("=" * 33)
          + """\n\t|\t[Configuration] => """+isconfig_done.ljust(9,' ')
          #+"""|\n\t|\t[Log Setup]     => """+islog_done.ljust(9,' ')
          +"""|\n\t"""+("=" * 33))

    main()

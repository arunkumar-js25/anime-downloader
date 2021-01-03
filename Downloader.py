import requests,os,glob
from bs4 import BeautifulSoup
import re as RegExp

my_headers = {}
my_headers['user-agent'] = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

class Downloader:
    def __init__(self, anime_dictionary):
        if os.path.isfile('failed.txt'):
            os.remove('failed.txt')
        self.anime_dict = anime_dictionary

    def downloadAnime(self):
        for episodeDict in self.anime_dict['scraped-episodes']:
            download_link = get_available_download_link(episodeDict)
            if download_link == 'unavailable':
                continue
            extension = '.mp4'
            if '.m3u8' in download_link:
                extension = '.m3u8'
            self.__downloadEpisode(filename=episodeDict['episode-title']+extension, download_link=download_link)
        self.__retryFailedDownloads()

    def __downloadEpisode(self, filename='episode.mp4', download_link='download-url'):
        print(" DOWNLOADING EPISODE:", filename)
        options = f'-x 10 --max-tries=5 --retry-wait=10 --check-certificate=false -d downloaded -o "{filename}"'
        cmd = f'aria2c {download_link} {options}'
        if os.path.isfile(f'downloaded/{filename}') and not os.path.isfile(f'downloaded/{filename}.aria2'):
            return

        while True:
            try:
                os.system(cmd)
                break
            except KeyboardInterrupt: input("\nDownloader is paused. PRESS [ENTER] TO CONTINUE...")

        if os.path.isfile("downloaded/" + filename + ".aria2"):
            open('failed.txt', 'a').write(cmd + '\n')

    def __retryFailedDownloads(self):
        if not os.path.isfile('failed.txt'):
            return
        print('- Retrying failed downloads')
        commands = open('failed.txt', 'r').read().strip().split('\n')
        for command in commands:
            while True:
                try:
                    os.system(command)
                    break
                except KeyboardInterrupt: input('\nDownloader is paused. PRESS [ENTER] TO CONTINUE...')

    def __del__(self):
        if len(glob.glob('downloaded/*.aria2')) != 0:
            return
        os.rename('downloaded', self.anime_dict['anime-title'])
        if os.path.isfile('failed.txt'):
            os.remove('failed.txt')

def get_available_download_link(episode_dict):
    if 'mp4' in episode_dict['embed-servers'].keys():
        return get_mp4upload_download_link(episode_dict['embed-servers']['mp4'])
    if 'vidcdn' in episode_dict['embed-servers'].keys():
        return get_vidcdn_download_link(episode_dict['embed-servers']['vidcdn'])
    return 'unavailable'

def get_vidcdn_download_link(embed_url):
    soup = BeautifulSoup(requests.get(embed_url, headers=my_headers).text, 'html.parser')
    js_text = str(soup.find('div', class_='videocontent'))
    download_link = RegExp.findall('file: \'(.+?)\'', js_text)[0]
    return download_link

def get_mp4upload_download_link(embed_url):
    scripts = BeautifulSoup(requests.get(embed_url, headers=my_headers).text, 'html.parser').find_all('script', type="text/javascript")
    evalText = [str(script) for script in scripts if "|embed|" in str(script)][0]
    #evalText = scripts[len(scripts)-1].text
    evalItems = evalText.split('|')
    del evalItems[:evalItems.index('mp4upload')+1]
    videoID = [a for a in evalItems if len(a)>30][0]
    evalItems = evalText.split('|')
    w3strPossiblesList = [s for s in evalItems if RegExp.match('s\d+$', s) or RegExp.match('www\d+$', s)]
    w3str = "www"
    if len(w3strPossiblesList) != 0:
        w3str = max(w3strPossiblesList, key=len)
    return 'https://{}.mp4upload.com:{}/d/{}/video.mp4'.format(w3str, evalItems[evalItems.index(videoID)+1], videoID)

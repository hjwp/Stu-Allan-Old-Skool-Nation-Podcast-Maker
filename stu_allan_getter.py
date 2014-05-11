import requests
from lxml import html
from django.contrib import syndication


MIXCLOUD_ROOT = 'http://www.mixcloud.com'

def get_episode_pages():
    contents_page = requests.get(MIXCLOUD_ROOT + '/stuallandj/').content
    contents = html.fromstring(contents_page)

    episodes = contents.cssselect('h3.card-cloudcast-title a')
    episode_urls = [
        a.get('href') for a in episodes
        if a.text_content().startswith('(#')
    ]
    return episode_urls


def find_mp3_link(episode_url):
    episode_html = requests.get(MIXCLOUD_ROOT + episode_url).content
    episode = html.fromstring(episode_html)
    all_links = episode.cssselect('a.mx-link')
    for a in all_links:
        link = a.get('href')
        if link and 'stuallan.com' in link and 'mp3' in link:
            return link

def main():
    for episode_url in get_episode_pages():
        print(episode_url)
        mp3_url = find_mp3_link(episode_url)
        print(mp3_url)
        if mp3_url:
            filename = mp3_url.split('/')[-1]
            print(filename)

#TODO: /usr/local/lib/python2.7/dist-packages/django/utils/feedgenerator.py

if __name__ == '__main__':
    main()

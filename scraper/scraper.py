import urllib2
import codecs
from bs4 import BeautifulSoup

# NOTE: Not all rap data is scraped.  Some high-profile artists have custom web pages

base_url = "http://ohhla.com/"

base_html = urllib2.urlopen(base_url + "all.html").read()
base_soup = BeautifulSoup(base_html)

def scrape_song(song_url, album_url, artist_url):
    song_html = urllib2.urlopen(base_url + artist_url + album_url + song_url).read()
    song_soup = BeautifulSoup(song_html)
    print "\t\t" + song_url
    lyrics = ""
    try:
        lyrics = song_soup.pre.prettify()
    except AttributeError:
        lyrics = song_soup.prettify()
    song_file = codecs.open("songs/" + song_url, 'w', 'utf-8')
    song_file.write(lyrics)


def scrape_album(album_url, artist_url):
    #print base_url + artist_url + album_url
    album_html = urllib2.urlopen(base_url + artist_url + album_url).read()
    album_soup = BeautifulSoup(album_html)
    song_links = album_soup.find_all("a", href=True)
    print "\t" + album_url
    for i in range(1, len(song_links)):
        link = song_links[i]
        song_url = link['href']
        scrape_song(song_url, album_url, artist_url)

def scrape_artist(artist_url):
    artist_html = urllib2.urlopen(base_url + artist_url).read()
    artist_soup = BeautifulSoup(artist_html)
    album_links = artist_soup.find_all("a", href=True)
    print artist_url
    for i in range(1, len(album_links)):
        link = album_links[i]
        album_url = link['href']
        scrape_album(album_url, artist_url)

pre_html = base_soup.pre

artist_links = pre_html.find_all("a", href=True)

for link in artist_links:
    artist_url = link['href']
    if "YFA" not in artist_url:
        scrape_artist(artist_url)

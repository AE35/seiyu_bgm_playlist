# -*- coding: utf-8 -*-
from datetime import date
import json

from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.util import prompt_for_user_token

from conf import (
    USERNAME,
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
)


TARGET_URL = 'https://www.seiyu.co.jp/campaign/bgm/'
SCOPE = 'playlist-modify-public'
SPOTIPY_REDIRECT_URI = 'http://localhost/'
PLAYLIST_JSON_PATH = 'out/playlist.json'


class PlayList(object):
    """プレイリストオジェクト
    """
    def __init__(self, title, tracks=[]):
        self.title = title
        self.tracks = tracks

    def add_track(self, artist, title):
        self.tracks.append({
            'artist': artist,
            'title': title,
        })

    def to_dict(self):
        return {
            'title': self.title,
            'tracks': self.tracks,
        }

    @classmethod
    def from_dict(cls, playlist_dict):
        return cls(title=playlist_dict['title'], tracks=playlist_dict['tracks'])

    def __repr__(self):
        return '{}({}曲)'.format(self.title, len(self.tracks))


def get_old_playlist():
    """過去のプレイリスト情報を復帰
    """
    try:
        with open(PLAYLIST_JSON_PATH, 'r') as f:
            data = f.read()
        playlist_dict = json.loads(data)
        return PlayList.from_dict(playlist_dict)
    except (FileNotFoundError, json.decoder.JSONDecodeError, KeyError):
        return

def get_playlist():
    """プレイリスト情報を取得
    """
    res = requests.get(TARGET_URL)
    soup = BeautifulSoup(res.content, 'lxml')

    # プレイリストタイトル取得
    try:
        playlist_title = soup.find('h2', attrs={'class': 'bgm_song_title'}).text
    except AttributeError:
        playlist_title = '放送曲名リスト'
    playlist = PlayList(playlist_title)

    # 各曲情報を取得
    for item in soup.find_all('p', attrs={'class': 'bgm_item_inner'}):
        title = item.next.strip().lower()
        artist = item.next.next.next.lstrip('by ').strip().lower()
        playlist.add_track(artist, title)

    # プレイリスト情報を保存
    with open(PLAYLIST_JSON_PATH, 'w') as f:
        f.write(json.dumps(playlist.to_dict()))

    print(playlist)
    return playlist

def search_all_tracks(token, playlist):
    """Spotifyから指定プレイリスト全曲の曲情報を取得
    """
    sp = spotipy.Spotify(auth=token)

    track_ids = []
    for i, track_dict in enumerate(playlist.tracks, 1):
        artist = track_dict['artist']
        song = track_dict['title']

        # 検索
        results = sp.search(q='artist:{} track:{}'.format(artist, song), limit=1)
        items = results['tracks']['items']
        item = None
        if len(items) > 0:
            item = items[0]

        if item is None:
            continue
        track_ids.append(item['id'])
        print('{}. {} by {}'.format(i, song, artist))
        print('   {} ({})'.format(item['external_urls']['spotify'], item['id']))

    return track_ids

def create_playklist(token, track_ids):
    sp = spotipy.Spotify(auth=token)
    user = sp.current_user()

    # プレイリスト取得
    playlist_title = '西友{}'.format(date.today().strftime('%Y%m'))
    results = sp.current_user_playlists()
    for playlist in results['items']:
        if playlist['name'] == playlist_title:
            # 作成済なら終了
            print('プレイリストは既に作成済です')
            return

    # 無ければ作成
    playlist = sp.user_playlist_create(user['id'], playlist_title)
    playlist_id = playlist['id']

    # 曲追加
    sp.user_playlist_add_tracks(user['id'], playlist_id, track_ids)

def main():
    # 直前取得データを復帰
    old_playlist = get_old_playlist()

    token = prompt_for_user_token(
        USERNAME, SCOPE,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
    )
    if not token:
        print("Can't get token for {}".format(USERNAME))
        return

    # 最新情報取得
    playlist = get_playlist()

    if old_playlist is not None and old_playlist.title == playlist.title:
        # 更新していなければ終了
        print('更新なし')
        return

    # Spotify問い合わせ
    track_ids = search_all_tracks(token, playlist)
    create_playklist(token, track_ids)

if __name__ == '__main__':
    main()

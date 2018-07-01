# Seiyu BGM Playlist

`Seiyu BGM Playlist` makes Spotify playlist from Seiyu BGM page.

- 認証した Spotify アカウント上に、プレイリストを作成します
- 直前の取得内容と変更が無い場合は作成しません
- 既に同名プレイリストがある場合は作成しません

## 開発環境におけるバージョン

- python: 3.6.4
- beautifulsoup4: 4.6.0
- lxml: 4.2.2
- requests: 2.19.1
- spotipy: 2.4.4

## 事前準備

1. [Spotify for Developpers](https://developer.spotify.com/dashboard/applications) にて、アプリケーションを作成
2. 作成したアプリケーションの `Client ID` と `Client Secret` を conf.py の `SPOTIPY_CLIENT_ID` と `SPOTIPY_CLIENT_SECRET` に控える
3. 作成したアプリケーションの `Edit Settings` から `Redirect URIs` を `http://localhost` を追加
4. プレイリストを追加したいSpotipyアカウント名を conf.py の USERNAME に指定

## 環境構築

    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirement.txt

## 実行

    $ python3 ./seiyu_bgm
    2018年6月15日からの放送曲名リスト(11曲)
    1. young adult friction by the pains of being pure at heart
       https://open.spotify.com/track/6Q1bS2CQiCLUFAuoRyl2gU (6Q1bS2CQiCLUFAuoRyl2gU)
    2. emmylou by first aid kit
       https://open.spotify.com/track/2e2Z8FeqqvUClWqc23nuX1 (2e2Z8FeqqvUClWqc23nuX1)
    3. talking backwards by real estate
       https://open.spotify.com/track/0ZwlxoHAnvkCRjsOrHAleU (0ZwlxoHAnvkCRjsOrHAleU)
    4. drive by the cars
       https://open.spotify.com/track/3wfujdbamR3Z46F4xav7LM (3wfujdbamR3Z46F4xav7LM)
    7. for what it's worth by the cardigans
       https://open.spotify.com/track/5JLYUKmpTS5KywAFJHmrA5 (5JLYUKmpTS5KywAFJHmrA5)
    8. let's start by haley reinhart
       https://open.spotify.com/track/196QUVJnVFL5yZ1uWjY3mB (196QUVJnVFL5yZ1uWjY3mB)
    9. age of consent by new order
       https://open.spotify.com/track/2EEinN4Zk8MUv4OQuLsTBj (2EEinN4Zk8MUv4OQuLsTBj)
    10. passenger by lisa hannigan
       https://open.spotify.com/track/1cdMp3YVnv5nBMsZJFTz7R (1cdMp3YVnv5nBMsZJFTz7R)
    11. everything now by arcade fire
       https://open.spotify.com/track/7KsZHCfOitA5V9oQYVdltG (7KsZHCfOitA5V9oQYVdltG)

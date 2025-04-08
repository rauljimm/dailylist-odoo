# 🎵 Dailylist Odoo

![Dailylist Odoo Logo](https://github.com/rauljimm/dailylist-odoo/blob/main/static/description/icon.png)

Welcome to Dailylist Odoo, an Odoo application that integrates with Spotify and Genius to provide an enriched musical experience.

## 📋 Description

Dailylist Odoo allows users to search for artists, explore albums, and get song lyrics directly from Odoo. It uses the Spotify API to search and retrieve music information and the Genius API to fetch song lyrics.

## 🚀 Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/rauljimm/dailylist-odoo.git
    ```
2. Navigate to the project directory:
    ```bash
    cd dailylist-odoo
    ```
3. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 🔧 Configuration

To make the Spotify integration work, you will need to configure your Spotify API credentials in the `spotipy_connector.py` file.

1. Open the `spotipy_connector.py` file located in the `util` directory.
2. Replace `'INSERT-HERE-YOUR-CLIENT-ID'` and `'INSERT-HERE-YOUR-CLIENT-SECRET'` with your Spotify credentials:

    ```python
    self.client_credentials_manager = SpotifyClientCredentials(
        client_id='INSERT-HERE-YOUR-CLIENT-ID',
        client_secret='INSERT-HERE-YOUR-CLIENT-SECRET'
    )
    ```

## 🌟 Features

- **Artist Search:** Search for artists by name on Spotify.
- **Album Exploration:** Get a list of an artist's albums on Spotify.
- **Track Listing:** Fetch the songs of a specific album on Spotify.
- **Track URLs:** Get the URL of a song on Spotify.
- **Song Lyrics:** Fetch song lyrics using the Genius API.

## 📄 Usage

### Artist Search

You can search for an artist by name and get a list of matching artists from Spotify.

```python
connector = SpotipyConnector()
artists = connector.search_artist('Artist Name')
```

### Get Artist Albums

Retrieve a list of albums by a specific artist using the artist's Spotify ID.

```python
albums = connector.get_artist_albums('Artist ID')
```

### Get Album Tracks

Fetch a list of tracks in a specific album using the album's Spotify ID.

```python
tracks = connector.get_album_tracks('Album ID')
```

### Get Track URL

Obtain the Spotify URL for a specific track using the track's Spotify ID.

```python
track_url = connector.get_track_url('Spotify ID')
```

### Get Song Lyrics

Retrieve the lyrics of a song using the artist's name and the song's name through the Genius API.

```python
lyrics = connector.get_song_lyrics('Artist Name', 'Song Name')
```

## 🤝 Contributions

Contributions are welcome! Please open an issue or submit a pull request to improve this project.

## 📧 Contact

If you have any questions or suggestions, feel free to contact [Raúl Jiménez](https://github.com/rauljimm).

Thank you for using Dailylist Odoo! 🎶

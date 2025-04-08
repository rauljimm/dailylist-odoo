import time
import spotipy
import lyricsgenius

from spotipy.oauth2 import SpotifyClientCredentials


class SpotipyConnector:

    # Constructor del conector de Spotipy
    def __init__(self):
        self.client_credentials_manager = SpotifyClientCredentials(
            client_id='INSERT-HERE-YOUR-CLIENT-ID',
            client_secret='INSERT-HERE-YOUR-CLIENT-SECRET'
        )
        self.genius = lyricsgenius.Genius("CxJPwGvew_lGUMaOSRXKisb6NwG7g0Zy-YGMjXI16XGMQLduHGfLvdeY5k5Bljb_")
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
        

    # Método usado para prevenir el sobrepaso de rate/request limit impuesto por la API de Spotify
    def safe_request(self, func, *args, **kwargs):
        """Realiza solicitudes seguras con reintentos en caso de límites de tasa."""
        retries = 3  # Número de intentos antes de fallar
        delay = 10  # Tiempo de espera en segundos entre reintentos

        # Por cada intento que tenemos
        for attempt in range(retries):
            try:
                # Lanzamos la función
                return func(*args, **kwargs)
            except spotipy.exceptions.SpotifyException as e:
                # Si salta excepción aplicamos una espera
                if "rate limit" in str(e).lower():
                    time.sleep(delay)  # Espera antes de volver a intentar
                else:
                    raise  # Propaga otros errores
            except Exception as e:
                raise Exception(f"Error inesperado: {e}")
        raise Exception("Rate limit alcanzado. Intentos fallidos.")

    # Método para retornar artista por nombre en Spotify
    def search_artist(self, artist_name):
        results = self.sp.search(q=artist_name, type='artist')
        return results['artists']['items']

    # Método para retornar los álbums de un artista en Spotify
    def get_artist_albums(self, artist_id):
        albums = self.sp.artist_albums(artist_id, album_type='album')
        return albums['items']
    
    # Método para retornar las canciones de un álbum en Spotify
    def get_album_tracks(self, album_id):
        tracks = self.sp.album_tracks(album_id)
        return tracks['items'] 
    
    # Método para retornar el URL de una canción en Spotify
    def get_track_url(self, spotify_id):
        track = self.sp.track(spotify_id)
        return track['external_urls']['spotify']
    
    def get_song_lyrics(self, artist_name, song_name):
        song = self.genius.search_song(song_name, artist_name)
        return song.lyrics

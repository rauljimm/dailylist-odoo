from odoo import models, fields, api
from ..util.spotipy_connector import SpotipyConnector
from datetime import datetime
from requests.exceptions import ConnectionError, Timeout

import base64
import requests
import time
import logging

_logger = logging.getLogger(__name__)  # Logger configurado

class Artist(models.Model):

    # Nombre y descripción del modelo
    _name = 'dailylist.artist'
    _description = 'Artista'

    # Campos del modelo
    name = fields.Char(string='Nombre', required=True)
    genres_spotify = fields.Char(string='Géneros de Spotify', default="")

    # Relaciones
    album_ids = fields.One2many('dailylist.album', 'artist_id', string='Álbumes', ondelete='cascade')
    genre = fields.Many2one('dailylist.genre', string="Género")

    @api.model
    def create(self, vals):
        sp = SpotipyConnector()

        # Creamos el artista
        artist = super().create(vals)

        try:
            artist_data = sp.safe_request(sp.search_artist, artist.name)

            if artist_data:
                spotify_artist = artist_data[0]

                # Comparamos de forma insensible al caso y eliminar espacios adicionales
                if artist.name.strip().lower() != spotify_artist.get('name', '').strip().lower():
                    return artist  # Si no coincide con un artista de Spotify, no añadimos datos adicionales

                # Si el nombre coincide, actualizamos los datos del artista
                artist_id = spotify_artist.get('id')

                genres_spotify = spotify_artist.get('genres', [])
                if genres_spotify:
                    artist.genres_spotify = ', '.join(genres_spotify)

                # Obtener los álbumes del artista
                albums = sp.safe_request(sp.get_artist_albums, artist_id)
                for album_data in albums:
                    time.sleep(1)  # Retardo entre solicitudes

                    release_date = album_data.get('release_date', '')
                    if len(release_date) == 4:
                        release_date = f"{release_date}-01-01"
                    try:
                        formatted_date = datetime.strptime(release_date, "%Y-%m-%d").date()
                    except ValueError:
                        formatted_date = None

                    #Buscamos la portada y sacamos la URL mediante requests
                    try:
                        portada = album_data.get('images')[0]['url']
                        response = requests.get(portada, timeout=10)
                        response.raise_for_status()
                        portada_base64 = base64.b64encode(response.content).decode('utf-8')
                    except(ConnectionError, Timeout) as e:
                        portada_base64 = None

                    except requests.exceptions.RequestException as e:
                        portada_base64 = None    

                    # Creamos el álbum
                    album = self.env['dailylist.album'].create({
                        'name': album_data.get('name'),
                        'artist_id': artist.id,
                        'fecha_publicacion': formatted_date,
                        'portada': portada_base64
                    })

                    # Procesamos las canciones del álbum
                    tracks = sp.safe_request(sp.get_album_tracks, album_data.get('id'))
                    if tracks:
                        time.sleep(1)  # Retardo adicional entre solicitudes
                        self.env['dailylist.song'].create([{
                            'name': track.get('name'),
                            'duration': track.get('duration_ms') // 1000,
                            'album_id': album.id,
                            'spotify_id': track.get('id')
                        } for track in tracks])

        except Exception as e:
            _logger.warning(f"Error processing artist '{artist.name}': {e}")

        return artist

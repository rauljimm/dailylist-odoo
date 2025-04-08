from odoo import models, fields, api
from ..util.spotipy_connector import SpotipyConnector

class Song(models.Model):

    # Nombre y descripción del modelo   
    _name = 'dailylist.song'
    _description = 'Canción'

    # Campos del modelo
    name = fields.Char(string='Nombre', required=True)
    duration = fields.Integer(string='Duración en segundos', required=True)
    lyrics = fields.Text(string="Lyrics")
    spotify_id = fields.Char(string='ID de Spotify')
    spotify_url = fields.Char(string='Enlace a Spotify')

    # Relaciones
    album_id = fields.Many2one('dailylist.album', string='Álbum', ondelete='cascade')
    artist_id = fields.Many2one(related='album_id.artist_id', string='Artista', store=True, readonly=True, ondelete='cascade')
    playlist_ids = fields.Many2many('dailylist.playlist', string='Listas de reproducción')

    # Campos computados
    duration_display = fields.Char(string='Duración', compute='_compute_duration_display', store=False)
    lyrics_status = fields.Char(string="Lyrics", compute="_compute_lyrics_status")

    # Función para crear el campo computado de duración transformándolo en minutos y segundos
    @api.depends('duration')
    def _compute_duration_display(self):
        for record in self:
            minutes = record.duration // 60
            seconds = record.duration % 60
            record.duration_display = f'{minutes}m {seconds}s'

    # Cálculo campo computado que comprueba si hay lyrics en una canción o no
    def _compute_lyrics_status(self):
        for record in self:
            record.lyrics_status = "Lyrics disponibles" if record.lyrics else "No hay lyrics disponibles"

    # Método para cuando se cree una canción se genere el URL en Spotify
    @api.model
    def create(self, vals):
        if vals.get('spotify_id'):
            sp = SpotipyConnector()
            spotify_url = sp.get_track_url(vals['spotify_id'])
            if spotify_url:
                vals['spotify_url'] = spotify_url
        return super(Song, self).create(vals)

    # Método para hacer clickable el URL de Spotify de la canción
    def open_spotify(self):
        for record in self:
            if record.spotify_url:
                return {
                    'type': 'ir.actions.act_url',
                    'url': record.spotify_url,
                    'target': 'new',
                }

    # Método para obtener las letras de la canción
    def get_lyrics(self):
        for record in self:
            if record.name and record.artist_id:
                sp = SpotipyConnector()
                try:
                    lyrics = sp.get_song_lyrics(record.artist_id.name, record.name)
                    if lyrics:
                        record.lyrics = lyrics
                    else:
                        record.lyrics = "No se encontraron letras para esta canción."
                except Exception as e:
                    record.lyrics = f"Error al obtener las letras: {e}"

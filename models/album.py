# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Album(models.Model):

    # Nombre y descripción del modelo
    _name = 'dailylist.album'
    _description = 'Albumes'

    # Campos del modelo
    name = fields.Char(string='Título', required=True)
    fecha_publicacion = fields.Date(string='Fecha de Publicación')
    portada = fields.Image(max_width=200, max_height=200)
    
    # Relaciones
    artist_id = fields.Many2one('dailylist.artist', string='Artista', ondelete='cascade')
    songs_ids = fields.One2many('dailylist.song', 'album_id', string='Canciones', ondelete='cascade') 

    # Campo computado duración total de todas las canciones del Álbum que es el que se mostrará en la vista
    total_duration = fields.Char(
        string='Duración total', 
        compute='_compute_total_duration',
        store=True
    )

    # Función para el cálculo del tiempo total formateado de las canciones del Álbum
    @api.depends('songs_ids.duration')
    def _compute_total_duration(self):
        for album in self:
            # Recogemos la duración de cada una de las canciones y las sumamos
            total_seconds = sum(song.duration for song in album.songs_ids if song.duration)
            
            # Convertimos a horas, minutos y segundos
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            
            # Formateamos el tiempo a hh:mm:ss, que será lo que se mostrará
            album.total_duration = f"{hours:02}:{minutes:02}:{seconds:02}"
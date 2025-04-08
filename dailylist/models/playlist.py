# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Playlist(models.Model):

    # Nombre y descripción del modelo
    _name = 'dailylist.playlist'
    _description = 'Lista de reproducción'

    # Campos del modelo
    name = fields.Char(string='Nombre de la lista', required=True)
    description = fields.Char(string='Descripción', required=True)

    # Relaciones
    songs_ids = fields.Many2many('dailylist.song', string='Canciones')
    
    # Campo computado de la duración total de la playlist que es el que se mostrará en la vista
    total_duration = fields.Char(
        string='Duración total', 
        compute='_compute_total_duration',
        store=True
    )

    # Método para calcular el campo computado formateado de la duración total de la playlist
    @api.depends('songs_ids.duration')
    def _compute_total_duration(self):
        for playlist in self:
            total_seconds = sum(song.duration for song in playlist.songs_ids if song.duration)
            
            # Convertimos a horas, minutos y segundos
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            
            # Formateamos a hh:mm:ss
            playlist.total_duration = f"{hours:02}:{minutes:02}:{seconds:02}"

    
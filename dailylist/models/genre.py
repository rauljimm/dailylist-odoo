# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Genre(models.Model):

    # Nombre y descripción del modelo
    _name = 'dailylist.genre'
    _description = 'Géneros'

    # Campos del modelo
    name = fields.Char(string='Nombre', required=True)
    
    # Relaciones
    artist_ids = fields.One2many('dailylist.artist', 'genre', string='Artistas')


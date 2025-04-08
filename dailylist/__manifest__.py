# -*- coding: utf-8 -*-
{
    'name': "dailylist",
    'summary': "Gestión de listas de reproducción musicales",
    'description': """
        Módulo para gestionar artistas, álbumes, canciones y listas de reproducción con conexión a distintos recursos en línea automatizados
    """,
    'author': "rauljimm",
    'category': 'Uncategorized',
    'website': "https://www.mywebsite.com",
    'version': '0.1',
    'depends': ['base'],
    'images': ['static/description/icon.png'],
    'data': [
        'security/ir.model.access.csv',
        'views/artist_views.xml',
        'views/album_views.xml',
        'views/playlist_views.xml',
        'views/song_views.xml',
        'views/genre.xml',
        'views/menus.xml',
    ],
    'application': True,
    'installable': True,
}
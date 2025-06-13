{
    'name': 'Checkpoints GPS de Seguridad',
    'version': '1.0',
    'summary': 'Gestión de puntos de control GPS con QR y registros de visitas.',
    'description': 'Este módulo permite registrar checkpoints con códigos QR',
    'author': 'Tecno Servicios Artavia',
    'license': 'LGPL-3',
    'depends': ['base', 'web', 'website', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/checkpoint_views.xml',
        'views/checkpoint_actions.xml',
        'views/generar_qr_wizard_view.xml',
        'views/visita_views.xml',
        'views/qr_scan_template.xml',
        'data/qr_sequence.xml'
    ],
    'installable': True,
    'application': True,
}
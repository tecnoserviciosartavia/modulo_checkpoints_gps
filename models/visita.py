from odoo import models, fields, api

class VisitaSeguridad(models.Model):
    _name = 'visita.seguridad'
    _description = 'Registro de Visita de Seguridad'

    checkpoint_id = fields.Many2one('checkpoint.seguridad', string='Checkpoint', required=True)
    #ubicacion_checkpoint = fields.Char(string='Ubicación del Checkpoint', related='checkpoint_id.ubicacion', store=True, readonly=True)
    ubicacion_checkpoint = fields.Char(string='Puesto de Seguridad', related='checkpoint_id.puesto_id.name', store=True, readonly=True)
    oficial_id = fields.Many2one('res.users', string='Oficial', required=True, default=lambda self: self.env.user)
    fecha_visita = fields.Datetime(string='Fecha de la Visita', required=True, default=fields.Datetime.now)
    ubicacion_gps = fields.Char(string='Ubicación GPS')
    observaciones = fields.Text(string='Observaciones')
    mapa_html = fields.Html(string='Mapa', compute='_compute_mapa_html', sanitize=False)

    @api.depends('ubicacion_gps')
    def _compute_mapa_html(self):
        for rec in self:
            if rec.ubicacion_gps and ',' in rec.ubicacion_gps:
                lat, lng = rec.ubicacion_gps.split(',')
                url = (
                    f"https://www.google.com/maps?q={lat.strip()},{lng.strip()}&z=16&output=embed"
                )
                rec.mapa_html = (
                    f'<iframe width="150" height="100" frameborder="0" style="border:0" '
                    f'src="{url}" allowfullscreen></iframe>'
                )
            else:
                rec.mapa_html = ''


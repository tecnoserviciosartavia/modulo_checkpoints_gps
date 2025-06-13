from odoo import models, fields, api

class VisitaSeguridad(models.Model):
    _name = 'visita.seguridad'
    _description = 'Registro de Visita de Seguridad'

    checkpoint_id = fields.Many2one('checkpoint.seguridad', string='Checkpoint', required=True)
    oficial_id = fields.Many2one('res.users', string='Oficial', required=True, default=lambda self: self.env.user)
    fecha_visita = fields.Datetime(string='Fecha de la Visita', required=True, default=fields.Datetime.now)
    ubicacion_gps = fields.Char(string='Ubicación GPS')
    observaciones = fields.Text(string='Observaciones')
    mapa_html = fields.Html(string="Mapa", compute='_compute_mapa_html')

    @api.depends('ubicacion_gps')
    def _compute_mapa_html(self):
        for rec in self:
            if rec.ubicacion_gps and ',' in rec.ubicacion_gps:
                lat, lng = rec.ubicacion_gps.split(',')
                # Calcula un bbox pequeño alrededor del punto
                delta = 0.01
                bbox = f"{float(lng)-delta},{float(lat)-delta},{float(lng)+delta},{float(lat)+delta}"
                rec.mapa_html = (
                    f'<iframe width="300" height="200" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" '
                    f'src="https://www.openstreetmap.org/export/embed.html?bbox={bbox}&amp;layer=mapnik&amp;marker={lat},{lng}" '
                    f'style="border: 1px solid black"></iframe>'
                    f'<br/><small><a href="https://www.openstreetmap.org/#map=16/{lat}/{lng}" target="_blank">Ver mapa más grande</a></small>'
                )
            else:
                rec.mapa_html = ''
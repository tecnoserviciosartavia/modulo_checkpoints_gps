from odoo import models, fields, api
import qrcode
from io import BytesIO
from base64 import b64encode

class Checkpoint(models.Model):
    _name = 'checkpoint.seguridad'
    _description = 'Checkpoint de Seguridad'
    _sql_constraints = [
        ('checkpoint_name_unique', 'unique(name)', 'El nombre del checkpoint debe ser único.'),
    ]

    name = fields.Char('Checkpoint', required=True)  # <--- elimina unique=True
    gps_latitude = fields.Float('Latitud GPS', digits=(10, 6))
    gps_longitude = fields.Float('Longitud GPS', digits=(10, 6))
    mapa_html = fields.Html(string='Mapa', compute='_compute_mapa_html', sanitize=False)
    qr_image = fields.Binary('Imagen QR', readonly=True)

    @api.depends('gps_latitude', 'gps_longitude')
    def _compute_mapa_html(self):
        for rec in self:
            if rec.gps_latitude and rec.gps_longitude:
                url = (
                    f"https://www.google.com/maps?q={rec.gps_latitude},{rec.gps_longitude}&z=16&output=embed"
                )
                rec.mapa_html = (
                    f'<iframe width="250" height="150" frameborder="0" style="border:0" '
                    f'src="{url}" allowfullscreen></iframe>'
                )
            else:
                rec.mapa_html = ''

    descripcion = fields.Text(string='Descripción')
    ubicacion = fields.Char(string='Ubicación del Checkpoint')
    codigo_qr = fields.Char(
        string='Código QR',
        required=True,
        copy=False,
        readonly=True,
        default='Nuevo'
    )
    imagen_qr = fields.Binary(string="QR Code", compute="_generar_imagen_qr")
    visita_ids = fields.One2many('visita.seguridad', 'checkpoint_id', string='Visitas')
    fecha_hora = fields.Datetime(string='Fecha y Hora', default=fields.Datetime.now)

    @api.model
    def create(self, vals):
        if vals.get('codigo_qr', 'Nuevo') == 'Nuevo':
            vals['codigo_qr'] = self.env['ir.sequence'].next_by_code('checkpoint.seguridad.qr') or 'Nuevo'
        return super().create(vals)

    def _generate_qr_code(self):
        return self.env['ir.sequence'].next_by_code('checkpoint.seguridad.qr') or 'Nuevo'

    @api.depends('codigo_qr')
    def _generar_imagen_qr(self):
        for record in self:
            if record.codigo_qr:
                qr = qrcode.QRCode(version=1, box_size=3, border=4)
                qr.add_data(record.codigo_qr)
                img = qr.make_image(fill_color="black", back_color="white")
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                record.imagen_qr = b64encode(buffered.getvalue())
            else:
                record.imagen_qr = False
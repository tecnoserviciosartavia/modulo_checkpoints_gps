from odoo import models, fields, api
import base64
import io
import qrcode

class GenerarQRWizard(models.TransientModel):
    _name = 'generar.qr.wizard'
    _description = 'Generar QR para Checkpoint'

    checkpoint_id = fields.Many2one('checkpoint.seguridad', string='Checkpoint', required=True)
    qr_image = fields.Binary('QR Generado', readonly=True)

    def generar_qr(self):
        self.ensure_one()
        qr_data = self.checkpoint_id.name
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        qr_image = base64.b64encode(buffer.getvalue())
        self.qr_image = qr_image
        # Actualiza el checkpoint con el QR generado
        self.checkpoint_id.qr_image = qr_image
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'generar.qr.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
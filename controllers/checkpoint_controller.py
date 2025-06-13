from odoo import http
from odoo.http import request
from datetime import datetime

class CheckpointController(http.Controller):

    @http.route('/registrar_visita/<string:codigo_qr>', type='http', auth='public', website=True)
    def registrar_visita(self, codigo_qr, **kwargs):
        checkpoint = request.env['checkpoint.seguridad'].sudo().search([('codigo_qr', '=', codigo_qr)], limit=1)
        if checkpoint:
            oficial = request.env.user
            ubicacion_gps = kwargs.get('ubicacion_gps', '')
            observaciones = kwargs.get('observaciones', '')
            visita = request.env['visita.seguridad'].create({
                'checkpoint_id': checkpoint.id,
                'oficial_id': oficial.id,
                'fecha_visita': datetime.now(),
                'ubicacion_gps': ubicacion_gps,
                'observaciones': observaciones
            })
            return """
                <h2>✅ Visita registrada</h2>
                <p>Checkpoint: %s</p>
                <p>Oficial: %s</p>
                <p>Hora: %s</p>
                <p>Ubicación GPS: %s</p>
                <p>Observaciones: %s</p>
                <p>Redirigiendo al escaneo...</p>
                <script>
                    setTimeout(function() {
                        window.location.href = '/qr_scan';
                    }, 2000);
                </script>
            """ % (checkpoint.name, oficial.name, visita.fecha_visita, ubicacion_gps, observaciones)
        else:
            return """
                <h2>❌ Código QR no válido</h2>
                <p>Redirigiendo al escaneo...</p>
                <script>
                    setTimeout(function() {
                        window.location.href = '/qr_scan';
                    }, 2000);
                </script>
            """
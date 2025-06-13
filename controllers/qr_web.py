from odoo import http
from odoo.http import request
from datetime import datetime

class QrWebController(http.Controller):

    @http.route('/qr_scan', type='http', auth='user', website=True)
    def qr_scan_page(self, **kw):
        return request.render('modulo_checkpoints_gps.qr_scan_template', {})

    @http.route('/qr_scan/submit', type='json', auth='user')
    def qr_scan_submit(self, qr_code, **kw):
        # Buscar el checkpoint por el código QR
        checkpoint = request.env['checkpoint.seguridad'].sudo().search([('codigo_qr', '=', qr_code)], limit=1)
        if not checkpoint:
            return {'status': 'error', 'msg': 'Checkpoint no encontrado'}
        # Crear la visita
        visita = request.env['visita.seguridad'].sudo().create({
            'checkpoint_id': checkpoint.id,
            'oficial_id': request.env.user.id,
            'fecha_visita': datetime.now(),
            'ubicacion_gps': '',  # Puedes obtenerla del frontend si lo deseas
            'observaciones': 'Visita registrada automáticamente desde QR'
        })
        return {
            'status': 'ok',
            'msg': f'Visita registrada en {checkpoint.name}',
            'checkpoint': checkpoint.name,
            'fecha': str(visita.fecha_visita)
        }

class CheckpointController(http.Controller):

    @http.route('/registrar_visita/<string:codigo_qr>', type='http', auth='public', website=True)
    def registrar_visita(self, codigo_qr, **kwargs):
        checkpoint = request.env['checkpoint.seguridad'].sudo().search([('codigo_qr', '=', codigo_qr)], limit=1)
        if checkpoint:
            oficial = request.env.user
            ubicacion_gps = kwargs.get('ubicacion_gps', '')
            visita = request.env['visita.seguridad'].create({
                'checkpoint_id': checkpoint.id,
                'oficial_id': oficial.id,
                'fecha_visita': datetime.now(),
                'observaciones': f'Ubicación GPS: {ubicacion_gps}'
            })
            # Página con redirección automática
            return """
                <h2>✅ Visita registrada</h2>
                <p>Checkpoint: %s</p>
                <p>Oficial: %s</p>
                <p>Hora: %s</p>
                <p>Ubicación GPS: %s</p>
                <p>Redirigiendo al escaneo...</p>
                <script>
                    setTimeout(function() {
                        window.location.href = '/qr_scan';
                    }, 2000);
                </script>
            """ % (checkpoint.name, oficial.name, visita.fecha_visita, ubicacion_gps)
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
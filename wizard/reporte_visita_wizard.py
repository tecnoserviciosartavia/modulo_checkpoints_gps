from odoo import models, fields, api

class ReporteVisitaWizard(models.TransientModel):
    _name = 'reporte.visita.wizard'
    _description = 'Asistente para Generar Reporte de Visitas'

    fecha_inicio = fields.Datetime(string='Desde', required=True)
    fecha_fin = fields.Datetime(string='Hasta', required=True)
    ubicacion_gps = fields.Char(string='Ubicación GPS', required=True)

    def generar_reporte(self):
        data = {
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'ubicacion_gps': self.ubicacion_gps,
        }
        return self.env.ref('modulo_checkpoints_gps.action_reporte_visita_xlsx').report_action(self, data=data)
from odoo import models
from datetime import datetime

class ReporteVisitaExcel(models.AbstractModel):
    _name = 'report.modulo_checkpoints_gps.reporte_visita_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        visitas = self.env['visita.seguridad'].search([
            ('fecha_visita', '>=', data['fecha_inicio']),
            ('fecha_visita', '<=', data['fecha_fin']),
        ])

        sheet = workbook.add_worksheet('Visitas')
        bold = workbook.add_format({'bold': True})

        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 30)
        sheet.set_column('C:C', 30)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 30)  # Columna para ubicación GPS

        sheet.write(0, 0, 'Checkpoint', bold)
        sheet.write(0, 1, 'Oficial', bold)
        sheet.write(0, 2, 'Fecha y Hora', bold)
        sheet.write(0, 3, 'Observaciones', bold)
        sheet.write(0, 4, 'Ubicación GPS', bold)  # Encabezado para ubicación GPS

        row = 1
        for visita in visitas:
            sheet.write(row, 0, visita.checkpoint_id.name)
            sheet.write(row, 1, visita.oficial_id.name)
            sheet.write(row, 2, str(visita.fecha_visita))
            sheet.write(row, 3, visita.observaciones or '')
            sheet.write(row, 4, visita.checkpoint_id.ubicacion or '')  # Ubicación GPS
            row += 1
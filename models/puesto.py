from odoo import models, fields

class PuestoSeguridad(models.Model):
    _name = 'puesto.seguridad'
    _description = 'Puesto de Seguridad'

    name = fields.Char('Nombre del Puesto', required=True)
    descripcion = fields.Text('Descripción')
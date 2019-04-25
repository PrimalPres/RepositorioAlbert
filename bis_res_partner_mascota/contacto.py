#	-*-	coding:	utf-8	-*-
from openerp import models, fields, api
class Contacto(models.Model):
    _name = 'contacto'
    _inherit = ['res.partner']
    hacer = fields.Boolean("Lo sé hacer o no")

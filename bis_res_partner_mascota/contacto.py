#	-*-	coding:	utf-8	-*-
from openerp import models, fields, api
class Contacto(models.Model):
    _inherit = ['res.partner']
    hacer = fields.Boolean(string='Lo sé hacer o no')

#	-*-	coding:	utf-8	-*-
from	openerp	import	models,	fields,	api
class	TodoTask(models.Model):
	def do_toggle_done(self):
		self.is_done = not self.is_done
		return True

	_name	=	'todo.task'
	name	=	fields.Char('Description',	required=True)
	is_done	=	fields.Boolean('Done?')
	active	=	fields.Boolean('Active?',	default=True)
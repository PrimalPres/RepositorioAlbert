#	-*-	coding:	utf-8	-*-
from	.	import	todo_task
class TodoTask(models.Model):
	@api.one
	def do_toggle_done(self):
		if self.user_id != self.env.user:
			raise Exception('Only	the	responsible	can	do	this!')
		else:
			return super(TodoTask, self).do_toggle_done()

	@api.multi
	def do_clear_done(self):
		domain = [('is_done', '=', True),
				  '|', ('user_id', '=', self.env.uid),
				  ('user_id', '=', False)]
		done_recs = self.search(domain)
		done_recs.write({'active': False})

	_name = 'todo.task'
	_inherit = ['todo.task', 'mail.thread']
	user_id	=	fields.Many2one('res.users', 'Responsible')
	date_deadline	=	fields.Date('Deadline')
    name = fields.Char(help="What needs to be done")

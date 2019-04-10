#	-*-	coding:	utf-8	-*-
from	openerp	import	models,	fields,	api
from	openerp.addons.base.res	import	res_request
from openerp.Exceptions import ValidationError


def	referencable_models(self):
	return	res_request.referencable_models(
        self,	self.env.cr,	self.env.uid,	context=self.env.context)

class	Tag(models.Model):
    class Tags(models.Model):
        _name = 'todo.task.tag'
        _parent_store = True
        #	_parent_name	=	'parent_id'
        name = fields.Char('Name')
        parent_id = fields.Many2one(
            'todo.task.tag', 'Parent	Tag', ondelete='restrict')
        parent_left = fields.Integer('Parent	Left', index=True)
        parent_right = fields.Integer('Parent	Right', index=True)

class	Stage(models.Model):
    _name = 'todo.task.stage'
    _order = 'sequence,name'
    #	String	fields:
    name = fields.Char('Name', 40)
    desc = fields.Text('Description')
    state = fields.Selection(
        [('draft', 'New'), ('open', 'Started'), ('done', 'Closed')],
        'State')
    docs = fields.Html('Documentation')
    #	Numeric	fields:
    sequence = fields.Integer('Sequence')
    perc_complete = fields.Float('%	Complete', (3, 2))
    #	Date	fields:
    date_effective = fields.Date('Effective	Date')
    date_changed = fields.Datetime('Last	Changed')
    #	Other	fields:
    fold = fields.Boolean('Folded?')
    image = fields.Binary('Image')
    #	Stage	class	relation	with	Tasks:
    tasks = fields.One2many('todo.task','stage_id', 'Tasks	in	this	stage')
    # related	model   # field	for	"this"	on	related	model

class TodoTask(models.Model):
    @api.one
    @api.constrains('name')
    def _check_name_size(self):
        if len(self.name) < 5:
            raise ValidationError('Must	have	5	chars!')

    @api.one     # para
    @api.depends('stage_id.fold') # se escribe el nombre de la funcion
    def _compute_stage_fold(self):
        self.stage_fold = self.stage_id.fold

    def _search_stage_fold(self, operator, value):
        return [('stage_id.fold', operator, value)]

    def _write_stage_fold(self):
        self.stage_id.fold = self.stage_fold

    _inherit	=	'todo.task'
    stage_id	=	fields.Many2one('todo.task.stage',	'Stage')
    #	TodoTask	class:	Task	<->	Tag	relation	(long	form):
    tag_ids = fields.Many2many(
    comodel_name='todo.task.tag',  # related	model
    relation='todo_task_tag_rel',  # relation	table	name
    column1='task_id',  # field	for	"this"	record
    column2='tag_id',  # field	for	"other"	record
    string='Tasks')
    stage_fold	=	fields.Boolean(
     'Stage	Folded?',
     compute='_compute_stage_fold',
     # store=False)  # the default
     search='_search_stage_fold',
     inverse='_write_stage_fold'
     )
    refers_to = fields.Reference(
        # [('res.user', 'User'), ('res.partner', 'Partner')],      Antiguamente
        # 'Refers	to')
        referencable_models, 'Refers	to'
    )
    stage_state = fields.Selection(
        related='stage_id.state',
        string='Stage	State')


    _sql_constraints	=	[
    ('todo_task_name_uniq',
    'UNIQUE	(name,	user_id,	active)',
     'Task	title	must	be	unique!')]
# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    # added fields
    project_id = fields.Many2one('project.project', string="Project")
    project_task_id = fields.Many2one('project.task', string="Task",
                                      domain="[('project_id','!=',False), "
                                             "('project_id','=',project_id), "
                                             "('is_closed','=',False)]")
    description = fields.Text(string="Description")

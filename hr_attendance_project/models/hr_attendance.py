# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    """ ODOO BEST PRACTICES
      The code uses model inheritance (_inherit) to extend the
     functionality of existing models (hr.attendance).
     This is a recommended approach in Odoo for adding custom fields and
     methods while keeping the original functionality intact.
     Custom fields like project_id, project_task_id, and description are added to
     the HrAttendance model to associate attendance records with projects and tasks.
     These fields provide more context about the attendance, which is helpful for
     reporting and analysis. """

    project_id = fields.Many2one('project.project', string="Project")
    project_task_id = fields.Many2one('project.task', string="Task",
                                      domain="[('project_id','!=',False), "
                                             "('project_id','=',project_id), "
                                             "('is_closed','=',False)]")
    description = fields.Text(string="Description")

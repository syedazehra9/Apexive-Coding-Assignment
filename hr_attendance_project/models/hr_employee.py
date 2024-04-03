# -*- coding: utf-8 -*-
from odoo import api, fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    """ ODOO BEST PRACTICES
    inherited model hr.employee
    Computed fields (attendance_project_id, attendance_project_task_id,
    and attendance_description) in the HrEmployee model are used to dynamically
    compute values based on the employee's last attendance record. Computed fields
    ensure data consistency and accuracy by automatically updating based on specified
    conditions.
    Security groups (groups attribute) are applied to computed fields to control visibility
    and access rights. This ensures that only authorized users can view and modify
    attendance-related information.
    Decorators like @api.depends and @api.model are used to define dependencies and
    expose methods to the Odoo API. These decorators ensure that computed fields
    are recalculated when their dependencies change and that methods are accessible
    from external sources.
    The get_attendance_projects method retrieves relevant project
    and task information based on specified domain criteria. This function
    prepares data for use in the user interface, such as dropdown lists
    for project and task selection.
    The _attendance_action_change method handles context variables related to project, task,
    and description changes during attendance actions. It updates the corresponding
    fields in the model based on the provided context. """

    """ USE OF DRY PRINCIPLE FOR A SERVER ACTION OR COMPUTABLE FIELD
     The DRY (Don't Repeat Yourself) principle is a software development principle that
     encourages developers to avoid duplicating code. It promotes code reusability,
     maintainability, and reduces the risk of errors.
    
     1. Computed Fields (attendance_project_id, attendance_project_task_id, attendance_description):
     These computed fields are used to dynamically compute values based on the employee's last attendance record.
     The computation logic for these fields is defined in a single method _compute_attendance_project(), which is decorated with @api.depends.
     By defining the computation logic in a single method, the code avoids duplicating the logic
     across multiple places. This adheres to the DRY principle by keeping the computation logic
     centralized and reusable.
    
     2. Helper Function (_compute_attendance_project()):
     This method computes the values of attendance_project_id, attendance_project_task_id, and attendance_description fields based on the employee's last attendance record.
     Instead of repeating the computation logic wherever these fields are used, the logic is centralized within this method.
     Other parts of the code that require these computed values can simply depend on these fields, rather than duplicating the computation logic.
    
     3. Context Handling (_attendance_action_change()):
     This method handles context variables related to project, task, and description changes during attendance actions.
     It updates the corresponding fields in the model based on the provided context.
     By centralizing the handling of context variables in this method, the code avoids duplicating context handling logic across multiple places.
     
     4. Code Modularity:
     The code is structured into logical units (methods and fields) that perform specific tasks.
     Each method and field serves a specific purpose and can be reused in other parts of the code or extended with additional functionality.
     Modularity promotes code reuse and reduces the need for duplicating code.
    """

    attendance_project_id = fields.Many2one('project.project',
                                            string="Attendance Project", compute='_compute_attendance_project',
                                            groups="hr_attendance.group_hr_attendance_kiosk,hr_attendance.group_hr_attendance,hr.group_hr_user")
    attendance_project_task_id = fields.Many2one('project.task',
                                                 string="Attendance Project Task",
                                                 compute='_compute_attendance_project',
                                                 groups="hr_attendance.group_hr_attendance_kiosk,hr_attendance.group_hr_attendance,hr.group_hr_user")
    attendance_description = fields.Text(string="Attendance Descriptions", compute='_compute_attendance_project',
                                         groups="hr_attendance.group_hr_attendance_kiosk,hr_attendance.group_hr_attendance,hr.group_hr_user")

    @api.depends('last_attendance_id.check_in', 'last_attendance_id.check_out', 'last_attendance_id')
    def _compute_attendance_project(self):
        for employee in self:
            att = employee.last_attendance_id.sudo()
            attendance_state = att and not att.check_out and 'checked_in' or 'checked_out'
            if attendance_state == 'checked_in':
                employee.attendance_project_id = att.project_id
                employee.attendance_project_task_id = att.project_task_id
                employee.attendance_description = att.description
            else:
                employee.attendance_project_id = False
                employee.attendance_project_task_id = False
                employee.attendance_description = False

    @api.model
    def get_attendance_projects(self, domain):
        projects = self.env['project.project'].search([])
        tasks = projects.mapped('task_ids')
        emp_id = self.search(domain, limit=1)
        return {
            'project_ids': [{'id': x.id, 'name': x.display_name} for x in projects if len(x.task_ids) > 0],
            'project_task_ids': [{'id': x.id, 'name': x.display_name, 'project_id': x.project_id.id} for x in tasks],
            'current_project_id': {'id': emp_id.attendance_project_id.id,
                                   'name': emp_id.attendance_project_id.display_name} if emp_id.attendance_project_id and emp_id.attendance_project_id.id in projects.ids else False,
            'current_project_task_id': {'id': emp_id.attendance_project_task_id.id,
                                        'name': emp_id.attendance_project_task_id.display_name} if emp_id.attendance_project_task_id and emp_id.attendance_project_task_id.id in tasks.ids else False,
            'current_description': emp_id.attendance_description or False,
        }

    def _attendance_action_change(self):
        res = super(HrEmployee, self)._attendance_action_change()
        project_id = self.env.context.get('project_id', False)
        project_task_id = self.env.context.get('project_task_id', False)
        attend_description = self.env.context.get('attend_description', False)
        val = {
            'project_id': int(project_id) if project_id else False,
            'project_task_id': int(project_task_id) if project_task_id else False,
            'description': str(attend_description) if attend_description else False
        }
        res.update(val)
        return res
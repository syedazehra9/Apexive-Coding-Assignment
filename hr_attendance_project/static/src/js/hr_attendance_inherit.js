odoo.define('hr_attendance_project.inherit_attendance', function (require) {
    "use strict";

    var MyAttendances = require('hr_attendance.my_attendances');
    var session = require('web.session');

    MyAttendances.include({
        events: Object.assign({}, MyAttendances.prototype.events, {
            'change select[id="projectSelect"]': '_onChangeProjectSelect',
        }),
        // When change the project, It will set project task with this project
        _onChangeProjectSelect: function (ev) {
            if (this.$("#projectSelect")[0]) {
                const projectID = this.$("select[name='project_id']").val();
                var selectHtml = '<select class="col-7" name="project_task_id" id="projectTaskSelect">';
                selectHtml += '<option selected="selected" value=""></option>';
                for (const tId of this.projects.project_task_ids) {
                    if (tId.project_id == projectID) {
                        selectHtml += "<option value='" + tId.id + "'" + ">" + tId.name + "</option>";
                    }
                }
                selectHtml += "</select>";
                this.$("#projectTaskSelect").replaceWith(selectHtml);
            }
        },
        // When it start Attendance, collection current attendances data with project, project task and description from backend
        willStart: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                return self._rpc({
                    model: 'hr.employee',
                    method: 'get_attendance_projects',
                    args: [[['user_id', '=', self.getSession().uid]]],
                    context: session.user_context,
                }).then(function (p) {
                    self.projects = p;
                });
            });
        },
        // Function overrided
        update_attendance: function () {
            var self = this;
            var context = session.user_context;
            var project_id = this.$("select[name='project_id']").val();
            var project_task_id = this.$("select[name='project_task_id']").val();
            var attend_description = this.$("textarea[id='attend_description']").val();

            // Check if project task and description are not entered
            if (!project_id || !project_task_id || !attend_description) {
                // Display a notification to the user indicating missing information
                self.displayNotification({ title: "Please enter project, project task and description.", type: 'danger' });
                return; // Do not proceed further
            }

            context['project_id'] = project_id;
            context['project_task_id'] = project_task_id;
            context['attend_description'] = attend_description;
            this._rpc({
                model: 'hr.employee',
                method: 'attendance_manual',
                args: [[self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances'],
                context: context,
            })
                .then(function (result) {
                    if (result.action) {
                        self.do_action(result.action);
                    } else if (result.warning) {
                        self.displayNotification({ title: result.warning, type: 'danger' });
                    }
                });
        },
    });
    return MyAttendances;
});
odoo.define('hr_attendance_project.inherit_attendance', function (require) {
    "use strict";

    /* JS CODE FOLLOWS BEST PRACTICES OF ODOO TO IMPLEMENT FRONTEND-SIDE ACTION
    1. Modularization: The code is organized as an Odoo module and utilizes the odoo.define
    method to define a new module named 'hr_attendance_project.inherit_attendance'.
    This follows Odoo's recommended approach for structuring JavaScript code within modules.
    2. Inheritance: The MyAttendances.include({}) method is used to extend the behavior
    of the existing hr_attendance.my_attendances module. This allows the code to override
    or add functionality to the existing frontend actions while keeping the original
     functionality intact.
     3. Events Handling: The code attaches event handlers to DOM elements using the events object.
      This approach is recommended in Odoo for handling user interactions and updating the UI
       dynamically.
     4. RPC Calls: Remote Procedure Calls (RPCs) are used to communicate with the Odoo backend.
      The _rpc method is employed to invoke server-side methods (get_attendance_projects and
       attendance_manual) asynchronously, ensuring smooth interaction between the frontend and backend.
     5. Error Handling: The code includes error handling logic to handle cases where required
     information (project, project task, and description) is not provided by the user. It
     displays a notification to the user indicating the missing information, which enhances
     the user experience and helps prevent data inconsistencies.
     6. Context Management: Context variables such as project_id, project_task_id, and
     attend_description are passed along with RPC calls to provide additional information
     to server-side methods. This allows the backend to perform actions based on the context
      provided by the frontend.
      7. Asynchronous Operations: Asynchronous programming techniques, such as using promises
       (then()), are utilized to ensure that certain operations (e.g., fetching attendance projects)
        do not block the UI thread, thereby maintaining a responsive user interface.
     8. Variable Scoping: The code uses proper variable scoping to prevent conflicts and
     ensure the correct context for variables like self, context, etc. This improves code
     readability and maintainability.
     */
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
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.tasks import export_user_quiz_history, export_all_user_performance
from app.models import User
from app.utils.auth import role_required

class UserQuizExportAPI(Resource):
    @jwt_required()
    def post(self):
        """Triggers an async job for the current user's quiz history."""
        current_user_id = get_jwt_identity()
        export_user_quiz_history.delay(current_user_id)
        return {
            'message': 'Your export has started. You will receive an email with the file shortly.'
        }, 202

class AdminUserExportAPI(Resource):
    @role_required('admin')
    def post(self):
        """
        Triggers an async job to export performance data for all users.
        This is an admin-only endpoint.
        """
        admin_id = get_jwt_identity()
        admin_user = User.query.get(admin_id)

        # Security check: Ensure the user triggering this is an admin
        if not admin_user or admin_user.role != 'admin':
            return {'message': 'Unauthorized access'}, 403

        # Pass the admin's email to the task so they receive the notification
        export_all_user_performance.delay(admin_user.email)
        
        return {
            'message': 'The all-user performance export has started. You will receive an email with the download link shortly.'
        }, 202

# This function registers all job-related routes
def register_job_routes(api):
    api.add_resource(UserQuizExportAPI, '/api/jobs/export/my-history')
    # Add the new admin-only endpoint
    api.add_resource(AdminUserExportAPI, '/api/jobs/export/all-users')

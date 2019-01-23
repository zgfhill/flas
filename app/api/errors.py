from flask import jsonify
from app.exceptions import ValidationError
from . import api

@main.app_erorhandler(404)
def page_not_found(e):
	if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
		response = jsonify({'error': 'not found'})
		response.status_code = 404
		return response
	return render_template('404.html'), 404

def forbidden(message):
	response = jsonify({'error': 'forbidden', 'message': message})
	response.status_code = 403
	return response

@api.errorhander(ValidationError)
def validation_error(e):
	return bad_request(e.args[0])


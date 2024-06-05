# Importing required functions 
from flask import Flask, jsonify

# Flask constructor 
app = Flask(__name__)

# Root endpoint 
@app.route('/hello', methods=['GET'])

def welcome():
	return jsonify({'msg':'Hello Flask World'})
	# # Define Plot Data 
	# labels = [
	# 	'January',
	# 	'February',
	# 	'March',
	# 	'April',
	# 	'May',
	# 	'June',
	# ]

	# data = [0, 10, 15, 8, 22, 18, 25]

	# # Return the components to the HTML template 
	# return render_template(
	# 	template_name_or_list='chartjs-example.html',
	# 	data=data,
	# 	labels=labels,
	# )


# Main Driver Function 
if __name__ == '__main__':
	# Run the application on the local development server ##
	app.run(debug=True)

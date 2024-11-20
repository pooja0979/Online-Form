from flask import Flask, render_template, request

app = Flask(__name__)

# Route to display the form
@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    
    if request.method == 'POST':
        # Get data from the form
        name = request.form.get('name')
        topics = request.form.getlist('topics')  # Checkbox values
        comments = request.form.get('comments', '')

        # Check if the user has already submitted
        try:
            with open('submitted_users.txt', 'r') as user_file:
                submitted_users = user_file.read().splitlines()
        except FileNotFoundError:
            submitted_users = []

        if name in submitted_users:
            # If the user already submitted, display a message and don't save the response
            message = "You have already submitted your response."
        else:
            # Save feedback to a file only if it's the first submission
            with open('feedback.txt', 'a') as feedback_file:
                feedback_file.write(f"Name: {name}\n")
                feedback_file.write(f"Topics: {', '.join(topics)}\n")
                feedback_file.write(f"Comments: {comments}\n")
                feedback_file.write("-" * 40 + "\n")

            # Log the user as having submitted feedback
            with open('submitted_users.txt', 'a') as user_file:
                user_file.write(f"{name}\n")

            message = "Thank you for your feedback!"

    return render_template('index.html', message=message)

# Route to view feedback
@app.route('/view-feedback')
def view_feedback():
    try:
        # Read the feedback from the file
        with open('feedback.txt', 'r') as f:
            feedback = f.readlines()
    except FileNotFoundError:
        feedback = ["No feedback available yet."]

    # Format feedback into a simple webpage
    formatted_feedback = "<br>".join(feedback)
    return f"<h1>Feedback</h1><p>{formatted_feedback}</p>"

# Route to clear all responses (delete the feedback and submitted users)
@app.route('/clear-responses')
def clear_responses():
    # Clear feedback file
    open('feedback.txt', 'w').close()  # This will empty the file
    
    # Clear submitted users file
    open('submitted_users.txt', 'w').close()  # This will empty the file

    return "All responses have been cleared."

if __name__ == '__main__':
    app.run(debug=True)

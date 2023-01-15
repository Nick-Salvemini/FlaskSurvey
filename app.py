from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chickens'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses = []

questions = []
choices =[]
for q in satisfaction_survey.questions:
    questions.append(q.question)
    choices.append(q.choices)


@app.route('/')
def home():
    print(responses, questions, choices)
    return render_template('home.html', title=satisfaction_survey.title, inst=satisfaction_survey.instructions)

@app.route('/questions/<int:q_num>')
def ask_questions(q_num):
    return render_template('questions.html', question=questions[q_num], choices=choices[q_num], q_id=q_num)

@app.route('/answers/<int:q_id>', methods=['POST'])
def add_answers(q_id):
    answer = request.form['response']
    responses.append(answer)
    if q_id < len(questions):
        id = q_id + 1
        return redirect('/questions/<int:id>')
    else:
        return render_template('/thanks.html')
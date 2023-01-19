from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chickens'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# responses = []

# questions = []
# choices =[]
# for q in satisfaction_survey.questions:
#     questions.append(q.question)
#     choices.append(q.choices)


# @app.route('/')
# def home():
#     if len(responses) == len(questions):
#         return render_template('/thanks.html')
#     return render_template('home.html', title=satisfaction_survey.title, inst=satisfaction_survey.instructions, index=len(responses))

# @app.route('/questions/<int:q_num>')
# def ask_questions(q_num):

#     re_len = len(responses)

#     if re_len == 0 and q_num != 0:
#         flash('Please do not attempt to access questions out of order. Thank you.')
#         return redirect ('/questions/0')
#     elif re_len > 0 and q_num != re_len:
#         flash('Please do not attempt to access questions out of order. Thank you.')
#         return redirect (f'/questions/<re_len>')
#     else:
#         return render_template('questions.html', question=questions[q_num], choices=choices[q_num], q_id=q_num)

# @app.route('/answers/<int:q_id>', methods=['POST'])
# def add_answers(q_id):

#     answer = request.form['response']
#     responses.append(answer)
#     id = q_id + 1

#     if id < len(questions):
#         return redirect(f'/questions/<int:id>')
#     else:
#         return render_template('/thanks.html')



questions = []
choices =[]
for q in satisfaction_survey.questions:
    questions.append(q.question)
    choices.append(q.choices)

@app.route('/')
def home():
    # if len(responses) == len(questions):
    #     return render_template('/thanks.html')
    if session.get('responses') == None:
        session['responses'] = []
        return render_template('home.html', title=satisfaction_survey.title, inst=satisfaction_survey.instructions, index=len(session['responses']))
    
    elif len(session['responses']) == len(choices):
        return render_template('/thanks.html')

    return render_template('home.html', title=satisfaction_survey.title, inst=satisfaction_survey.instructions, index=len(session['responses']))

@app.route('/start-session', methods=['POST'])
def start_session():
    index=len(session['responses'])
    return redirect(f'/questions/{index}') 
    # return redirect(f'/questions/'+str(index)) 

@app.route('/questions/<int:q_num>')
def ask_questions(q_num):

    re_len = len(session['responses'])

    print('**********************************')
    print(re_len)
    print(q_num)
    print(re_len == 0)
    print(q_num != 0)


    if re_len == 0 and q_num != 0:

        flash('Please do not attempt to access questions out of order. Thank you.')
        return redirect ('/questions/0')
    elif re_len > 0 and q_num != re_len:

        flash('Please do not attempt to access questions out of order. Thank you.')
        return redirect (f'/questions/{re_len}')
    else:
        return render_template('questions.html', question=questions[q_num], choices=choices[q_num], q_id=q_num)

@app.route('/answers/<int:q_id>', methods=['POST'])
def add_answers(q_id):

    answer = request.form['response']

    updated_response = session['responses']
    updated_response.append(answer)
    session['responses'] = updated_response

    id = q_id + 1

    if id < len(questions):
        return redirect(f'/questions/{id}')
    else:
        return render_template('/thanks.html')
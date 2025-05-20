# app.py
from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'secretkey123'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        low = int(request.form['start'])
        high = int(request.form['end'])
        session['low'] = low
        session['high'] = high
        session['attempts'] = 0
        return redirect(url_for('guess'))

    return render_template('index.html')

@app.route('/guess', methods=['GET', 'POST'])
def guess():
    if 'low' not in session or 'high' not in session:
        return redirect(url_for('index'))

    low = session['low']
    high = session['high']
    guess = (low + high) // 2
    session['guess'] = guess
    session['attempts'] += 1

    return render_template('guess.html', guess=guess, attempts=session['attempts'])

@app.route('/feedback/<action>')
def feedback(action):
    low = session['low']
    high = session['high']
    guess = session['guess']

    if action == 'higher':
        session['low'] = guess + 1
    elif action == 'lower':
        session['high'] = guess - 1
    elif action == 'correct':
        return render_template('success.html', guess=guess, attempts=session['attempts'])

    if session['low'] > session['high']:
        return render_template('error.html')

    return redirect(url_for('guess'))

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

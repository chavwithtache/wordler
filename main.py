from flask import Flask, request, redirect
from flask import render_template
from _wordler import Wordler

app = Flask(__name__)
app.secret_key = 'fdslkfgjslgj'


@app.route('/')
def index():
    return 'Under Construction'


@app.route('/wordler')
@app.route('/wordler/')
def new_game():
    w = Wordler()
    w.reset_all()
    pin = w.pin
    return redirect(f'{request.url_root}wordler/{pin}')


@app.route('/wordler/<pin>', methods=['GET', 'POST'])
def start(pin):
    w = Wordler()
    if pin=='':
        return redirect(f'{request.url_root}wordler')
    if request.query_string:
        new_pin=request.query_string.decode().split('=')[1]
        return redirect(f'{request.url_root}wordler/{new_pin}')
    url = f'{request.url_root}wordler/{pin}'
    message = ''
    top_row = '9999999999'
    second_row = '999999999'
    third_row = '9999999'
    if request.method == 'GET':
        w.reset_all()
        words_and_scores = {}
        w.reset_from_pin(pin)
        words_left=w.words_left

    else:
        guess_word = request.form['guess'].lower()
        words_str = request.form['words']
        words = [] if words_str == '' else words_str.split(',')
        pin = request.form['pin']
        words_and_scores = w.set_and_return_words_and_scores(pin=pin, words=words)
        wl=w.words_left
        if guess_word == 'help':
            message = f'There are {len(wl)} possible words remaining {wl if len(wl) < 10 else str(wl[:10])[:-1] + ", ...]"}'
        elif guess_word not in w.allowed_words:
            message = f'Invalid word "{guess_word}"'
        else:
            result = w.guess(guess_word)
            words_and_scores[guess_word.upper()] = result
            wl=w.words_left
            if result == '22222':
                message= f'Congratulations! you did it in {len(words_and_scores)} goes.'
            else:
                message = f'There are {len(wl)} possible words remaining.'

    top_row=w.get_letters('QWERTYUIOP')
    second_row = w.get_letters('ASDFGHJKL')
    third_row = w.get_letters('ZXCVBNM')



    return render_template('wordler.html',
                           url=url,
                           words_and_scores=words_and_scores,
                           words=','.join(list(words_and_scores.keys())),
                           pin=pin,
                           message=message,
                           top_row=top_row,
                           second_row=second_row,
                           third_row=third_row,
                           zip=zip)




app.run(host='0.0.0.0', port=81)


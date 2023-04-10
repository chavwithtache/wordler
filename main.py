from flask import Flask, request, redirect
from flask import render_template
from _wordler import Wordler
from get_definition import get_word_definition
app = Flask(__name__)
app.secret_key = 'fdslkfgjslgj'


@app.route('/')
def index():
    return redirect(f'{request.url_root}wordler/5')

@app.route('/wordler')
def root():
    return redirect(f'{request.url_root}wordler/5')

@app.route('/wordlerTest/<letters_in_word>/<result_word>')
def test_result_word(letters_in_word,result_word):
    w = Wordler()
    message=''
    try:
        w.reset_all(letters_in_word,result_word)
    except ValueError as e:
        message=str(e)
        w.reset_all(letters_in_word)
    pin = w.pin
    return start(letters_in_word,str(pin),message)

@app.route('/wordler/<letters_in_word>')
def new_game(letters_in_word):
    if len(letters_in_word)>1:
        return redirect(f'{request.url_root}wordler/5')
    w = Wordler()
    w.reset_all(letters_in_word)
    pin = w.pin
    return redirect(f'{request.url_root}wordler/{letters_in_word}/{pin}')


@app.route('/wordler/<letters_in_word>/<pin>', methods=['GET', 'POST'])
def start(letters_in_word, pin, message:str = None):
    letters_in_word=int(letters_in_word)
    w = Wordler()
    show_definition=True
    if pin=='':
        return redirect(f'{request.url_root}wordler')
    if request.query_string:
        qs_args = {a.split('=')[0]:a.split('=')[1] for a in request.query_string.decode().split('&')}
        new_pin=qs_args['pin']
        if len(new_pin)==5:
            letters_in_word=7
        elif len(new_pin) == 3:
            letters_in_word = 3
        elif len(new_pin)==4:
            letters_in_word=5
        else:
            letters_in_word = qs_args.get('letters_in_word', 5)
        if new_pin=='':
            return redirect(f'{request.url_root}wordler/{letters_in_word}')
        else:
            return redirect(f'{request.url_root}wordler/{letters_in_word}/{new_pin}')
    url = f'{request.url_root}wordler/{letters_in_word}/{pin}'
    message = [] if message is None else [message]
    # top_row = '9999999999'
    # second_row = '999999999'
    # third_row = '9999999'
    if request.method == 'GET':
        w.reset_all()
        words_and_scores = {}
        w.reset_from_pin(pin)
        # words_left=w.words_left

    else:
        guess_word = request.form['guess'].lower().strip()
        words_str = request.form['words']
        words = [] if words_str == '' else words_str.split(',')
        pin = request.form['pin']
        words_and_scores = w.set_and_return_words_and_scores(pin=pin, words=words)
        wl=w.words_left
        if guess_word == 'help':
            message = [f'There are {len(wl)} possible words remaining {wl if len(wl) < 10 else str(wl[:10])[:-1] + ", ...]"}']
        elif len(guess_word) != letters_in_word:
            message = [f'Word must have {letters_in_word} letters']
        elif guess_word not in w.allowed_words:
            message = [f'Invalid word "{guess_word}"']
        else:
            result = w.guess(guess_word)
            words_and_scores[guess_word.upper()] = result
            wl=w.words_left
            if result == '2'* letters_in_word:
                message= [f'Congratulations! you did it in {len(words_and_scores)} goes.']
            else:
                if len(wl) == 1:
                    message = ['There is just 1 possible word remaining.']
                else:
                    message = [f'There are {len(wl)} possible words remaining.']
            if show_definition:
                if show_definition is True:
                    message = get_word_definition(guess_word) + message
    top_row=w.get_letters('QWERTYUIOP')
    second_row = w.get_letters('ASDFGHJKL')
    third_row = w.get_letters('ZXCVBNM')



    return render_template('wordler.html',
                           url=url,
                           words_and_scores=words_and_scores,
                           words=','.join(list(words_and_scores.keys())),
                           pin=pin,
                           letters_in_word=letters_in_word,
                           message=message,
                           top_row=top_row,
                           second_row=second_row,
                           third_row=third_row,
                           zip=zip)


app.run(host='0.0.0.0', port=81)


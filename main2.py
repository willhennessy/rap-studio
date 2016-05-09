from flask import Flask, render_template, request
from rhyme_analyzer import sort_by_rhyme
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
	if request.method == 'GET':
		return render_template('main.html')
	else:
		start = time.time()
		user_verse = request.form['input_lyric']
		lyrics_db = open('generated_lines.txt').read().splitlines()
		phonetics_db = open('generated_lines_phonetics.txt').read().splitlines()
		output_lyrics = sort_by_rhyme(user_verse, lyrics_db, phonetics_db)
		print "Load Time: %s seconds" % (time.time() - start)
		return render_template('main.html', input_lyric=user_verse, output_lyrics=output_lyrics)

if __name__ == '__main__':
	app.debug = True
	app.run(host='127.0.0.1', port=5001)

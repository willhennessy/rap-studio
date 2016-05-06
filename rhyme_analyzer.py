import subprocess
from difflib import SequenceMatcher

'''
How to test in python console:

from rhyme_analyzer import *
import rhyme_analyzer
sort_by_rhyme("I want a banana", ["I want an apple","I want a banana","I want a cherry","I want dominos"])


reload(rhyme_analyzer)  to update changes
'''

def sort_by_rhyme(user_verse, gen_verses):
    '''
    input:  user_verse - string provided by the user
            gen_verses - list of verses to be sorted
    output: sorted list of verses from best rhyme score to worst
    '''
    return sorted(gen_verses, key=lambda verse: rhyme_score(user_verse, verse), reverse = True)


def rhyme_score(verse1, verse2):
    '''
    input:  two musical verses (string)
    output: score of how well the verses rhyme together
    Returns a high score if the last word of the two verses are phonetically similar
    '''
    phonemes1 = translate_to_phonemes(last_word(verse1))
    phonemes2 = translate_to_phonemes(last_word(verse2))

    # TODO - define a better similarity function
    # consider removing consonants and focus only on vowels=rhymes
    score = SequenceMatcher(None, phonemes1, phonemes2).ratio()

    print verse1, '=>', phonemes1, verse2, '=>', phonemes2, 'Score:', score
    print '----'
    return score


def translate_to_phonemes(verse):
    ''' NOTE: the shell=True parameter is a security hazard.
                maybe shouldn't use it for web form input '''
    command = u'espeak -xq -v%s %s' % ('en-us', verse)
    return subprocess.check_output(command, shell=True)


def last_word(verse):
    return verse.rsplit(None, 1)[-1]

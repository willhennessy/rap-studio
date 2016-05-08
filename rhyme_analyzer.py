import subprocess
import re
from difflib import SequenceMatcher
import time

'''
How to test in python console:

from rhyme_analyzer import *
import rhyme_analyzer
sort_by_rhyme("Who cut other people open like cantaloupes", ["Who cut other people open like cantaloupes", "But if we can hump dead animals and antelopes","Then there's no reason that a man and another man can't elope","But if you feel like I feel, I got the antidote","Women wave your pantyhose, sing the chorus and it goes"])


reload(rhyme_analyzer)  to update changes
'''

END_RHYME_LEN = 3

THREE_CHAR_PHONEMES = ['aI@', 'aU@']
TWO_CHAR_PHONEMES = ['l^','n^','3:','@L','@2','@5','aa','a#','A:','A@','e@','I2','i:','i@','u:','U@','O:','O@','o@','aI','eI','OI','aU','oU']
ONE_CHAR_PHONEMES = ['@','3','a','E','I','i','0','V','U']


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
    start = time.time()
    phonemes1 = separate_phonemes(translate_to_phonemes(verse1))
    phonemes2 = separate_phonemes(translate_to_phonemes(verse2))

    score = 0
    length = min(END_RHYME_LEN, len(phonemes1), len(phonemes2))
    for back_idx in range(1, length+1):
        score += phoneme_match(phonemes1[-back_idx], phonemes2[-back_idx])

    print "%s seconds" % (time.time() - start)

    # print verse1, '=>', phonemes1
    # print verse2, '=>', phonemes2
    # print 'Score:', score
    # print '----'
    return score


def phoneme_match(one, two):
    '''
    input:  two phonemes
    output: a score [0.0,1.0] of how well they rhyme

    List of all phonemes:  http://espeak.sourceforge.net/phonemes.html
    '''
    uh = {'@','a#','@2', 'V'}
    i = {'I','I2'}
    ee = {'i','i:'}
    orr = {'O@', 'o@'}
    aa = {'a', 'aa'}

    if one == two:
        return 1.0
    elif one in uh and two in uh:
        return 0.9
    elif one in i and two in i:
        return 0.9
    elif one in orr and two in orr:
        return 0.9
    elif one in ee and two in ee:
        return 0.7
    elif one in aa and two in aa:
        return 0.4
    else:
        return 0.0


def translate_to_phonemes(verse):
    ''' NOTE: the shell=True parameter is a security hazard.
                maybe shouldn't use it for web form input '''
    clean_verse = re.sub("['\"]", '', verse)
    command = u"espeak -xq -v%s '%s'" % ('en-us', clean_verse)
    phonetics = subprocess.check_output(command, shell=True)
    return re.sub("[',\s+$]", '', phonetics)


def last_word(verse):
    return verse.rsplit(None, 1)[-1]


def separate_phonemes(phonemes):
    '''
    input: phonetic string like ba#nan@
    output: array of phonemes like ['b', 'a#', 'n', 'a', 'n', '@']
    '''
    result = []
    idx = 0
    while idx < len(phonemes):
        three = phonemes[idx:idx+3]
        two = phonemes[idx:idx+2]
        one = phonemes[idx]

        if three in THREE_CHAR_PHONEMES:
            result.append(three)
            idx += 3
        elif two in TWO_CHAR_PHONEMES:
            result.append(two)
            idx += 2
        elif one in ONE_CHAR_PHONEMES:
            result.append(one)
            idx += 1
        else:
            # skip over consonant sounds and other characters
            idx += 1
    return result

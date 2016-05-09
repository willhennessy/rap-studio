import subprocess
import re
from difflib import SequenceMatcher
import time

END_RHYME_LEN = 3

THREE_CHAR_PHONEMES = ['aI@', 'aU@']
TWO_CHAR_PHONEMES = ['l^','n^','3:','@L','@2','@5','aa','a#','A:','A@','e@','I2','i:','i@','u:','U@','O:','O@','o@','aI','eI','OI','aU','oU']
ONE_CHAR_PHONEMES = ['@','3','a','E','I','i','0','V','U']

uh = {'@','a#','@2', 'V'}
i = {'I','I2'}
ee = {'i','i:'}
orr = {'O@', 'o@'}
aa = {'a', 'aa'}


def sort_by_rhyme(user_verse, gen_verses, phonetics_db):
    '''
    input:  user_verse - string provided by the user
            gen_verses - list of verses to be sorted
            phonetics_db - list of verses in phonetic representation
    output: sorted list of verses from best rhyme score to worst
    '''
    user_verse_phonemes = separate_phonemes(translate_to_phonemes(slice_end(user_verse)))

    top_indices = sorted(range(len(phonetics_db)), key=lambda verse_idx:
        rhyme_score(user_verse_phonemes, separate_phonemes(phonetics_db[verse_idx])), reverse = True)[:10]

    return [gen_verses[idx] for idx in top_indices]


def rhyme_score(phonemes1, phonemes2):
    '''
    input:  two musical verses (string)
    output: score of how well the verses rhyme together
    Returns a high score if the last word of the two verses are phonetically similar
    '''
    score = 0
    length = min(END_RHYME_LEN, len(phonemes1), len(phonemes2))
    for back_idx in range(1, length+1):
        score += phoneme_match(phonemes1[-back_idx], phonemes2[-back_idx])

    #print phonemes1, phonemes2, score
    return score


def phoneme_match(one, two):
    '''
    input:  two phonemes
    output: a score [0.0,1.0] of how well they rhyme

    List of all phonemes:  http://espeak.sourceforge.net/phonemes.html
    '''
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
    command = u"espeak -xq -v%s \"%s\"" % ('en-us', verse)
    phonetics = subprocess.check_output(command, shell=True)
    return re.sub("[',\s+$]", '', phonetics)


def convert_db_to_phonetics():
    ''' static method to convert the text file to phonetics '''
    lyrics_db = open('generated_lines.txt').read().splitlines()
    file_out = open('generated_lines_phonetics.txt', 'w')
    for verse in lyrics_db:
        phonemes = translate_to_phonemes(slice_end(verse))
        file_out.write("%s\n" % phonemes)


def slice_end(verse):
    return ' '.join(verse.rsplit(None, 3)[-3:])


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

from nltk.probability import FreqDist
import re

def is_boundary_marker(token):
    BOUNDARY_MARKERS = {'.', '?', '!', ';', '...', '<b>'}

    return token in BOUNDARY_MARKERS

def boundary_marker_to_tag(token, TAG = '<b>'):
    return TAG if is_boundary_marker(token) else token

def get_lower_words(tokens: list[str]) -> list[str]:
    '''
    Returns a sanitized word list based on the provided tokens list

    '''
    return [token.lower() for token in tokens if re.match(r"^\w+", token)]

def get_lower_tokens(tokens: list[str]) -> list[str]:
    '''
    Returns a lowered version of the provided tokens list

    '''
    return [token.lower() for token in tokens]

def get_most_common_words(tokens: list[str], num: int, remove_boundary_markers = False) -> list[str]:
    '''
    Use FreqDist to identify most common tokens/words and return them

    '''
    if remove_boundary_markers:
        tokens = [token for token in tokens if not is_boundary_marker(token)]
    
    word_freq = FreqDist(tokens)

    common_words: list[tuple[str, int]] = word_freq.most_common(num)

    return [word.lower() for word, _ in common_words]
    
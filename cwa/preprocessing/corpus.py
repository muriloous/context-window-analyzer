from pylangacq import Reader

def prepare_corpus(corpus: str | list[str]):
    if isinstance(corpus, str): 
        from nltk.tokenize import word_tokenize
        return word_tokenize(corpus)
    else: return corpus

def get_childes_reader() -> Reader:
    import pylangacq
    import os, logging

    BASE_PATH = os.path.join(os.getcwd(), 'corpora', 'CHILDES')
    CORPORA = ['AlegreLong', 'AlegreX']

    reader: Reader = pylangacq.Reader()

    for corpus in CORPORA:
        corpus_reader = pylangacq.read_chat(os.path.join(BASE_PATH, corpus + '.zip'))
        reader.append(corpus_reader)

    logging.info(
        "Processed CHILDES files: " +
        str(reader.n_files())   
    )

    return reader

def load_childes(childes_reader: Reader|None = None) -> tuple[list[str], list[tuple[str, str]]]:
    from pylangacq.objects import Token

    if not childes_reader:
        childes_reader = get_childes_reader()
    
    tokens: list[str] = []
    tagged_data: list[tuple[str, str]] = []

    UTTERANCE_BOUNDARIES = ['.', '?', '!', '...', '+...', '+..?', '+!?', '+//.', '+//?', '++.',]
    INTERMEDIATE_PUNCTUATION = [',', '+.', '+,', '+/?', '+/.', '+=.', '+"', '+^', '+"/.', '+".',  '+<', '++']

    utterance: list[Token]
    for utterance in childes_reader.tokens(by_utterances=True, exclude="CHI"):
        utt_len = len(utterance)
        for idx, token in enumerate(utterance):
            ignore_token = False
            if not token.mor:
                if token.word in UTTERANCE_BOUNDARIES:
                    token.word = "<br>"
                    token.pos = "punct" 
                elif token.pos in INTERMEDIATE_PUNCTUATION or not token.word.isalnum():
                    ignore_token = True
                else:
                    # logging.debug("Untagged word:", token)
                    ignore_token = True
            if token.word == 'POSTCLITIC':
                ignore_token = True

            if not ignore_token:
                tokens.append(token.word)
                tagged_data.append((token.word, token.pos,))

            if idx == utt_len - 1 and token.word != "<br>" and token.pos not in INTERMEDIATE_PUNCTUATION and token.word not in INTERMEDIATE_PUNCTUATION:
                tokens.append("<br>")
                tagged_data.append((token.word, token.pos,))
    
    return tokens, tagged_data

def load_floresta() -> tuple[list[str], list[tuple[str, str]]]:
  from nltk.corpus import floresta
  tokens = floresta.words()
  tagged_data = floresta.tagged_words()

  return tokens, tagged_data

def load_corpus(corpus: str = "childes") -> tuple[list[str], list[tuple[str, str]]]:
    match corpus:
        case "childes":
            return load_childes()
        case "floresta":
            return load_floresta()
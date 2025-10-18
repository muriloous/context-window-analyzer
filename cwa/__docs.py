import logging
logging.basicConfig(level=logging.DEBUG, force=True, format='%(message)s')

def get_example_for_pseudocode():
  from processing import (
    build_contingency_dicts_from_context_window,
    build_contingency_dicts_from_sentences
  )

  raw_text = "No meio do caminho tinha uma pedra\ntinha uma pedra no meio do caminho\ntinha uma pedra\nno meio do caminho tinha uma pedra"
  raw_text = raw_text.lower()
  raw_text = raw_text.replace("\n", " <b> ")
  tokens = raw_text.split()
  logging.debug("\nTokens\n" + repr(tokens))
  
  from_ctx_window = build_contingency_dicts_from_context_window(tokens, 3, 3)
  logging.debug('\nFrom context window\n' + repr(from_ctx_window))
  
  from_sentence = build_contingency_dicts_from_sentences(tokens, 3, 3)
  logging.debug('\nFrom sentence\n' + repr(from_sentence))

  return from_ctx_window, from_sentence

def get_statistics_for_pseudocode():
  from metrics import evaluate

  from_ctx_window, _ = get_example_for_pseudocode()
  tagged_data = [('tinha', 'verb'), ('uma', 'det'), ('pedra', 'noun')]
  logging.debug('\nTagged data\n' + repr(tagged_data))

  evaluate(from_ctx_window, tagged_data)

import logging
from config import Config
from .options import OPTIONS

def help():
    print('Usage: python cwa [... options]')
    print('\nOPTIONS:')

    for option in OPTIONS.values():
        tags = [f'-{tag}' if len(tag) == 1 else f'--{tag}' for tag in list(option['tag'])]
        print(', '.join(tags))
        print(option['description'])
        if 'example' in option: print('How to use:', option['example'])
        if option['require_arguments']: print("Argument is required")
        print()

def get_current_config(config):
    logging.info(repr(config) + '\n')

def parse_args(args):
    from re import match

    COMPLETE_PARAM_TAG_REGEX = '^--[a-zA-Z\\-]*'
    SIMPLIFIED_PARAM_TAG_REGEX = '^-[a-zA-Z]{1}\\d*$'

    parsed_args = []
    for idx, arg in enumerate(args):
        is_option_tag = False
        tag, argument = None, None

        if match(COMPLETE_PARAM_TAG_REGEX, arg) and (is_option_tag := True): 
            parsed = arg.replace('--', '').split('=')
            tag = parsed[0]
            argument = parsed[1] if (len(parsed)) > 1 else None
        
        if match(SIMPLIFIED_PARAM_TAG_REGEX, arg) and (is_option_tag := True):
            tag = arg.replace('-', '')
            if len(tag) > 1: argument = tag[1:]; tag = tag[0]

        if is_option_tag:
            for option in OPTIONS.values():
                if tag in option['tag']:
                    if option['require_arguments'] and not argument:
                        try:
                            argument = args[idx + 1]
                        except IndexError:
                            raise Exception(f"No argument given for {tag}")
                    
                    parsed_args.append((tag, argument))

    return parsed_args

def set_incoming_args(incoming_args: list[str], config: Config):
  from helpers import is_integer

  for option, argument in parse_args(incoming_args):
    # Help
    if option in OPTIONS['help']['tag']:
        help()
        exit()

    # Data setter
    if option in OPTIONS['corpus']['tag']:
        config.corpus = argument
    
    if option in OPTIONS['sample_from']['tag']:
        samples = argument.split(',')
        for sample in samples:
            if sample in OPTIONS['sample_from']['arguments']['context_window']:
                config.sample_from_context_window = True
            elif sample in OPTIONS['sample_from']['arguments']['sentences']:
                config.sample_from_sentences = True
            elif sample in OPTIONS['sample_from']['arguments']['context_window_with_boundaries']:
                config.sample_from_context_window_with_boundaries = True
            else:
                raise Exception(f"\
                    Invalid argument: \"{argument}\". \"sample-from\" option requires one of the following values:\n\
                    {list(OPTIONS['sample_from']['arguments']['sentences']) \
                    + list(OPTIONS['sample_from']['arguments']['context_window']) \
                    + list(OPTIONS['sample_from']['arguments']['context_window_with_boundaries'])}\
                ")
            continue

    # Parameters setters
    if option in OPTIONS['num_context_words']['tag']:
        if not (is_integer(argument)): raise Exception(f"Invalid argument: \"{argument}\". \"context-words\" option requires an integer")
        config.num_context_words = int(argument)
        continue
    
    if option in OPTIONS['num_target_words']['tag']:
        if not (is_integer(argument)): raise Exception(f"Invalid argument: \"{argument}\". \"target-words\" option requires an integer")
        config.num_target_words = int(argument)
        continue

    if option in OPTIONS['window_or_max_window_length']['tag']:
        exception = Exception(f"Invalid argument: \"{argument}\". \"target-words\" option requires an integer or a list of integers")
        if not (is_integer(argument)):
            if not (argument.startswith('[') and argument.endswith(']')):
                raise exception
            else:
                import ast
                try: argument = ast.literal_eval(argument)
                except ValueError: raise exception
        else:
            argument = int(argument)
        config.window_or_max_window_length = argument
        continue

    # Export method setters
    if option in OPTIONS['plot_graph']['tag']:
        config.plot_graph = True
        continue

    if option in OPTIONS['no_plot_graph']['tag']:
        config.plot_graph = False
        continue

    if option in OPTIONS['plot_dendrogram']['tag']:
        config.plot_dendrogram = True
        continue

    if option in OPTIONS['export_comparative_table']['tag']:
        config.export_comparative_table = True
        continue

    if option in OPTIONS['export_contingency_table']['tag']:
        config.export_contingency_table = True
        continue

    if option in OPTIONS['print_evaluation_results']['tag']:
        config.print_evaluation_results = True
        continue

    # Log level setters
    if option in OPTIONS['verbose']['tag']:
        config.log_level = 'info'
        logging.basicConfig(level=logging.INFO, force=True, format='%(message)s',)
        continue

    if option in OPTIONS['debug']['tag']:
        config.log_level = 'debug'
        logging.basicConfig(level=logging.DEBUG, force=True, format='%(message)s')
        continue

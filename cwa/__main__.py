def main():
  import sys
  from config import Config
  from interface_adapters.cli import (
    set_incoming_args,
    get_current_config,
    run_model
  )

  config = Config(30, 20, 2)

  incoming_args = sys.argv[1:]

  if 'pseudocode' in incoming_args:
    from __docs import get_statistics_for_pseudocode
    get_statistics_for_pseudocode()
    exit()

  if incoming_args: set_incoming_args(incoming_args, config)
  
  get_current_config(config)
  
  run_model(config)

if __name__ == '__main__':
  main()

#------------------------------------------------------------------------------
# File: main.py
# Desc: The main file for GeneticMusic
# Auth: Cezary Wojcik
# Date: September 17, 2016
# Opts: -d, --debug : show debug messages
#------------------------------------------------------------------------------

# ---- [ imports ] ------------------------------------------------------------

import getopt, sys

# ---- [ globals ] ------------------------------------------------------------

debug = False

# ---- [ utility functions ] --------------------------------------------------

def handle_error(message):
  print("Error: {0}".format(message))
  sys.exit(2)

def debug_message(message):
  global debug
  if debug:
    print(message)

def enable_debug():
  global debug
  debug = True

# ---- [ main ] ---------------------------------------------------------------

def main(argv):

  try:
    options, arguments = getopt.getopt(
      sys.argv[1:],
      "d",
      ["debug"])
  except getopt.GetoptError as error:
    handle_error(str(error))

  for option, argument in options:
    if option in ["-d", "--debug"]:
      enable_debug()
      debug_message("Debug mode enabled.")
    else:
      handle_error("unhandled option '{0}' detected".format(o))

  # TODO: do something!

if __name__ == "__main__":
    main(sys.argv[1:])

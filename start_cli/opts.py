OPT_FILE = (['file'], {'help': "path to the scenario config file"})
OPT_TIMEOUT = \
    (['--timeout'],
     {'help': 'the number of seconds that may pass without success until a mission is considered a failure.',
     'type': int,
     'default': 300})
OPT_SPEEDUP = \
    (['--speedup'],
     {'help': 'the speed-up factor that should be applied to the simulation clock.',
      'type': int,
      'default': 30})
OPT_LIVENESS = \
    (['--timeout-liveness'],
     {'help': 'the number of seconds that may pass without communication with the rover until the mission is aborted.',
      'type': int,
      'default': 30})

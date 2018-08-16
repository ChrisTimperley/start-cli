OPT_FILE = (['file'], {'help': "path to the scenario config file"})
OPT_TIMEOUT = \
    (['--time-limit'],
     {'help': 'the number of seconds that may pass without success until a mission is considered a failure.',
     'type': int,
     'default': 300})
OPT_TIMEOUT_CONNECTION = \
    (['--timeout-connection'],
     {'help': 'the number of seconds to wait when connecting to the SITL before aborting.',
     'type': int,
     'default': 5})
OPT_CHECK_WAYPOINTS = \
    (['--check-wps'],
     {'help': 'enable checking of number of visited waypoints.',
      'action': 'store_true'})
OPT_SITL_PREFIX = None
OPT_SPEEDUP = \
    (['--speedup'],
     {'help': 'the speed-up factor that should be applied to the simulation clock.',
      'type': int,
      'default': 10})
OPT_LIVENESS = \
    (['--liveness-timeout'],
     {'help': 'the number of seconds that may pass without communication with the rover until the mission is aborted.',
      'type': int,
      'default': 1})

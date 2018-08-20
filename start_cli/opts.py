OPT_FILE = (['file'], {'help': "path to the scenario config file"})
OPT_TIMEOUT = \
    (['--time-limit'],
     {'help': 'the number of seconds that may pass without success until a mission is considered a failure.',
     'type': int,
     'dest': 'timeout',
     'default': 300})
OPT_TIMEOUT_CONNECTION = \
    (['--timeout-connection'],
     {'help': 'the number of seconds to wait when connecting to the SITL before aborting.',
     'type': int,
     'default': 5})
OPT_WORKAROUND = \
    (['--no-workaround'],
     {'help': 'disables a workaround that causes the oracle to ignore all commands beyond a known non-terminating command.',
      'dest': 'use_workaround',
      'action': 'store_false'})
OPT_CHECK_WAYPOINTS = \
    (['--check-wps'],
     {'help': 'enable checking of number of visited waypoints.',
      'action': 'store_true'})
OPT_SITL_PREFIX = None
OPT_ATTACK = \
    (['--attack'],
     {'help': 'enables the attack during the mission execution.',
      'action': 'store_true'})
OPT_SPEEDUP = \
    (['--speedup'],
     {'help': 'the speed-up factor that should be applied to the simulation clock.',
      'type': int,
      'default': 10})
OPT_LIVENESS = \
    (['--liveness-timeout'],
     {'help': 'the number of seconds that may pass without communication with the rover until the mission is aborted.',
      'type': int,
      'dest': 'timeout_liveness',
      'default': 1})

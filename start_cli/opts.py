OPT_FILE = (['file'], {'help': "path to the scenario config file"})
OPT_COVERAGE_FILE = \
    (['file'], {'help': 'path to a JSON-encoded coverage report.'})
OPT_ARCHIVE = \
    (['--archive'],
     {'help': 'path to a compressed Docker image.',
      'dest': 'fn_archive',
      'type': str})
OPT_LOCALIZATION = \
    (['--localization'],
     {'help': 'loads fault localization information from a given file.',
      'type': str})
OPT_TRANSFORMATIONS = \
    (['--transformations'],
     {'help': 'load transformations from a specified transformation database file.',
      'type': str})
OPT_TIMEOUT_REPAIR = \
    (['--timeout-repair'],
     {'help': 'maximum number of minutes to wait before terminating the search.',
      'type': int,
      'default': 60})
OPT_LIMIT_CANDIDATES = \
    (['--candidate-limit'],
     {'help': 'maximum number of candidate patches that may be evaluated.',
      'dest': 'limit_candidates',
      'type': int})
OPT_NUM_THREADS = \
    (['--threads'],
     {'help': 'number of threads to use.',
      'type': int,
      'default': 1})
OPT_SNIPPETS = \
    (['--snippets'],
     {'help': 'loads snippets from a specified snippet database file.',
      'type': str})
OPT_COVERAGE = \
    (['--coverage'],
     {'help': 'path to a JSON-encoded line coverage report.',
      'type': str})
OPT_ANALYSIS = \
    (['--analysis'],
     {'help': 'path to a JSON-encoded static analysis report.',
      'type': str})
OPT_TIMEOUT = \
    (['--time-limit'],
     {'help': 'the number of seconds that may pass without success until a mission is considered a failure.',
     'type': int,
     'dest': 'timeout_mission',
     'default': 300})
OPT_TIMEOUT_CONNECTION = \
    (['--timeout-connection'],
     {'help': 'the number of seconds to wait when connecting to the SITL before aborting.',
     'type': int,
     'default': 10})
OPT_WORKAROUND = \
    (['--no-workaround'],
     {'help': 'disables a workaround that causes the oracle to ignore all commands beyond a known non-terminating command.',
      'dest': 'use_workaround',
      'action': 'store_false'})
OPT_CHECK_WAYPOINTS = \
    (['--no-check-wps'],
     {'help': 'disables checking of number of visited waypoints.',
      'dest': 'check_waypoints',
      'action': 'store_false'})
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
    (['--timeout-liveness'],
     {'help': 'the number of seconds that may pass without communication with the rover until the mission is aborted.',
      'type': int,
      'dest': 'timeout_liveness',
      'default': 1})

OPT_DOCKER_CLIENT = \
    (['--docker-client'],
     {'help': 'the version of the Docker Client API that should be used to communicate with the Docker server.',
      'type': str})

OPT_SEED = \
    (['--seed'],
     {'help': 'specifies a seed for the random number generator.',
      'type': int,
      'default': 0})
OPT_NO_TERMINATE_EARLY = \
    (['--no-terminate-early'],
     {'help': 'the search will produce as many patches as possible within the allotted time window.',
      'dest': 'no_terminate_early',
      'action': 'store_true'})
OPT_CHECK_SCOPE = \
    (['--check-scope'],
     {'help': 'prevents transformations with out-of-scope variables.',
      'dest': 'check_scope',
      'action': 'store_true'})
OPT_CHECK_SYNTAX = \
    (['--check-syntax-scope'],
     {'help': 'prevents transformations with out-of-scope keywords..',
      'dest': 'check_syntax_scope',
      'action': 'store_true'})
OPT_IGNORE_DEAD_CODE = \
    (['--ignore-dead-code'],
     {'help': 'prevents insertion of known dead-code.',
      'dest': 'ignore_dead_code',
      'action': 'store_true'})
OPT_IGNORE_UNTYPED_RETURNS = \
    (['--ignore-untyped-returns'],
     {'help': 'do not insert "return" if types mismatch.',
      'dest': 'ignore_untyped_returns',
      'action': 'store_true'})
OPT_IGNORE_EQUIV_PREPENDS = \
    (['--ignore-equiv-prepends'],
     {'help': 'prevents equivalent prepend transformations.',
      'dest': 'ignore_equiv_prepends',
      'action': 'store_true'})
OPT_IGNORE_STRING_EQUIV_SNIPPETS = \
    (['--ignore-string-equiv-snippets'],
     {'help': 'ignores duplicate string-equivalent snippets.',
      'dest': 'ignore_string_equiv_snippets',
      'action': 'store_true'})
OPT_IGNORE_DECLS = \
    (['--ignore-decls'],
     {'help': 'prevents declrations from being transformed or inserted.',
      'dest': 'ignore_decls',
      'action': 'store_true'})
OPT_ONLY_INSERT_EXECUTED = \
    (['--only-insert-executed'],
     {'help': 'restricts transformations to those that involve executed code.',
      'dest': 'only_insert_executed',
      'action': 'store_true'})
OPT_NO_ORDERING = \
    (['--no-ordering'],
     {'help': 'disables ordering of transformations',
      'dest': 'ordered',
      'action': 'store_false'})

OPTS_REPAIR = [
    OPT_NO_TERMINATE_EARLY,
    OPT_SEED,
    OPT_CHECK_SCOPE,
    OPT_CHECK_SYNTAX,
    OPT_IGNORE_DEAD_CODE,
    OPT_IGNORE_UNTYPED_RETURNS,
    OPT_IGNORE_STRING_EQUIV_SNIPPETS,
    OPT_IGNORE_EQUIV_PREPENDS,
    OPT_IGNORE_DECLS,
    OPT_ONLY_INSERT_EXECUTED,
    OPT_NO_ORDERING
]

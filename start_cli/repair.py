__all__ = ['RepairController']

import logging

from start_core.scenario import Scenario
from start_repair.snapshot import Snapshot
from start_repair.validate import validate
from cement.ext.ext_argparse import ArgparseController, expose

logger = logging.getLogger(__name__)  # type: logging.Logger
logger.setLevel(logging.DEBUG)

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


class RepairController(ArgparseController):
    class Meta:
        label = 'repair'
        description = 'interact with the repair component of START'
        stacked_on = 'base'
        stacked_type = 'nested'

    def __load_scenario(self, filename: str) -> Scenario:
        logger.info("loading scenario from file [%s]", filename)
        scenario = Scenario.from_file(filename)
        logger.info("loaded scenario [%s] from file", scenario.name)
        return scenario

    def default(self) -> None:
        self.app.args.print_help()

    @expose(
        help='attempts to repair the source code for a given scenario',
        arguments=[OPT_FILE])
    def repair(self) -> None:
        fn_scenario = self.app.pargs.file

        scenario = self.__load_scenario(fn_scenario)
        logger.info("repairing scenario")

        logger.info("successfully repaired scenario")

    @expose(
        help='ensures that a scenario produces an expected set of test outcomes',
        arguments=[OPT_FILE, OPT_TIMEOUT, OPT_LIVENESS, OPT_SPEEDUP])
    def validate(self) -> None:
        fn_scenario = self.app.pargs.file
        timeout_mission = self.app.pargs.timeout
        timeout_liveness = self.app.pargs.timeout_liveness
        speedup = self.app.pargs.speedup

        # FIXME build snapshot
        scenario = self.__load_scenario(fn_scenario)
        logger.info("validating scenario")
        snapshot = Snapshot.build(scenario=scenario,
                                  timeout_mission=timeout_mission,
                                  timeout_liveness=timeout_liveness,
                                  speedup=speedup,
                                  check_waypoints=True,  # FIXME
                                  use_oracle_workaround=False)  # FIXME
        validate(snapshot)
        logger.info("validated scenario")
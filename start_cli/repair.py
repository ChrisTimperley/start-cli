__all__ = ['RepairController']

import logging

from start_core.scenario import Scenario
from start_repair.snapshot import Snapshot
from start_repair.validate import validate
from cement.ext.ext_argparse import ArgparseController, expose

from .opts import *

logger = logging.getLogger(__name__)  # type: logging.Logger
logger.setLevel(logging.DEBUG)


class RepairController(ArgparseController):
    class Meta:
        label = 'repair'
        description = 'interact with the repair component of START'
        stacked_on = 'base'
        stacked_type = 'nested'

    def __load_scenario(self, filename):
        # type: (str) -> Scenario
        logger.info("loading scenario from file [%s]", filename)
        scenario = Scenario.from_file(filename)
        logger.info("loaded scenario [%s] from file", scenario.name)
        return scenario

    def default(self):
        # type: () -> None
        self.app.args.print_help()

    @expose(
        help='attempts to repair the source code for a given scenario',
        arguments=[OPT_FILE,
                   OPT_TIMEOUT,
                   OPT_LIVENESS,
                   OPT_SPEEDUP,
                   OPT_WORKAROUND])
    def repair(self):
        # type: () -> None
        fn_scenario = self.app.pargs.file

        scenario = self.__load_scenario(fn_scenario)
        logger.info("repairing scenario")

        logger.info("successfully repaired scenario")

    @expose(
        help='performs static analysis of a given scenario.',
        arguments=[OPT_FILE])
    def analyze(self):
        # type: () -> None
        fn_scenario = self.app.pargs.file
        scenario = self.__load_scenario(fn_scenario)

        logger.info("performing static analyis of scenario")

        fn_out = "analysis.json"

        logger.info("saved static analysis to disk: %s", fn_out)

    @expose(
        help='performs fault localization for a given scenario.',
        arguments=[OPT_FILE,
                   OPT_TIMEOUT,
                   OPT_LIVENESS,
                   OPT_SPEEDUP,
                   OPT_WORKAROUND])
    def localize(self):
        # type: () -> None
        fn_scenario = self.app.pargs.file
        scenario = self.__load_scenario(fn_scenario)

        logger.info("performing fault localization for scenario")

        fn_out = "coverage.json"

        logger.info("saved fault localization to disk: %s", fn_out)

    @expose(
        help='ensures that a scenario produces an expected set of test outcomes',
        arguments=[OPT_FILE,
                   OPT_TIMEOUT,
                   OPT_LIVENESS,
                   OPT_SPEEDUP,
                   OPT_WORKAROUND])
    def validate(self):
        # type: () -> None
        fn_scenario = self.app.pargs.file
        timeout_mission = self.app.pargs.timeout
        timeout_liveness = self.app.pargs.timeout_liveness
        speedup = self.app.pargs.speedup
        use_workaround = self.app.pargs.use_workaround

        scenario = self.__load_scenario(fn_scenario)
        logger.info("validating scenario")
        snapshot = Snapshot.build(scenario=scenario,
                                  timeout_mission=timeout_mission,
                                  timeout_liveness=timeout_liveness,
                                  speedup=speedup,
                                  check_waypoints=True,  # FIXME
                                  use_oracle_workaround=use_workaround)
        validate(snapshot)
        logger.info("validated scenario")

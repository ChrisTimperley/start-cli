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

    def __build_snapshot(self,
                         fn_scenario,           # type: str
                         timeout_mission,       # type: int
                         timeout_liveness,      # type: int
                         timeout_connection,    # type: int
                         speedup,               # type: int
                         check_waypoints,       # type: bool
                         use_workaround         # type: bool
                         ):                     # type: (...) -> None
        # type: (str) -> Snapshot
        scenario = self.__load_scenario(fn_scenario)
        logger.debug("building snapshot")
        snapshot = Snapshot.build(scenario=scenario,
                                  timeout_mission=timeout_mission,
                                  timeout_liveness=timeout_liveness,
                                  timeout_connection=timeout_connection,
                                  speedup=speedup,
                                  check_waypoints=True,  # FIXME
                                  use_oracle_workaround=use_workaround)
        logger.debug("built snapshot: %s", snapshot)
        return snapshot

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
                   OPT_TIMEOUT_CONNECTION,
                   OPT_LIVENESS,
                   OPT_SPEEDUP,
                   OPT_CHECK_WAYPOINTS,
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
                   OPT_TIMEOUT_CONNECTION,
                   OPT_LIVENESS,
                   OPT_SPEEDUP,
                   OPT_CHECK_WAYPOINTS,
                   OPT_WORKAROUND])
    def validate(self):
        # type: () -> None
        fn_scenario = self.app.pargs.file
        timeout_mission = self.app.pargs.timeout_mission
        timeout_liveness = self.app.pargs.timeout_liveness
        timeout_connection = self.app.pargs.timeout_connection
        speedup = self.app.pargs.speedup
        use_workaround = self.app.pargs.use_workaround
        check_waypoints = self.app.pargs.check_waypoints
        snapshot = self.__build_snapshot(fn_scenario,
                                         timeout_mission,
                                         timeout_liveness,
                                         timeout_connection,
                                         speedup,
                                         check_waypoints,
                                         use_workaround)
        logger.info("validating scenario")
        validate(snapshot, verbose=self.app.pargs.verbose)
        logger.info("validated scenario")

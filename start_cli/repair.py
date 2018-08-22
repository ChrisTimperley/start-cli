__all__ = ['RepairController']

import logging

from bugzoo.core.coverage import TestSuiteCoverage
from start_core.scenario import Scenario
from start_repair.snapshot import Snapshot
from start_repair.validate import validate
from start_repair.localize import coverage, localize
from start_repair.analyze import analyze
from cement.ext.ext_argparse import ArgparseController, expose

from .opts import *

logger = logging.getLogger(__name__)  # type: logging.Logger
logger.setLevel(logging.DEBUG)


class RepairController(ArgparseController):
    class Meta:
        label = 'repair'
        description = 'interact with the repair component of START'
        stacked_on = 'base'
        stacked_type = 'embedded'

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
                                  check_waypoints=check_waypoints,
                                  use_oracle_workaround=use_workaround)
        logger.debug("built snapshot: %s", snapshot)
        return snapshot

    def __placeholder_snapshot(self, fn_scenario):
        # type: (str) -> Snapshot
        return self.__build_snapshot(fn_scenario,
                                     timeout_mission=1,
                                     timeout_liveness=1,
                                     timeout_connection=1,
                                     speedup=1,
                                     check_waypoints=True,
                                     use_workaround=True)


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
        help='precomputes the set of transformations for a given scenario.',
        arguments=[OPT_FILE])
    def transformations(self):
        # type: () -> None
        fn_scenario = self.app.pargs.file
        fn_out = "transformations.json"

        logger.info("precomputing transformations for scenario")

        snapshot = self.__placeholder_snapshot(fn_scenario)

        logger.info("saved precomputed transformations to disk: %s", fn_out)

    @expose(
        help='performs static analysis of a given scenario.',
        arguments=[OPT_FILE])
    def analyze(self):
        # type: () -> None
        fn_scenario = self.app.pargs.file

        logger.info("performing static analyis of scenario")
        fn_out = "analysis.json"

        # NOTE since we never interact with the test suite, we can use
        #   placeholder values to build the snapshot.
        snapshot = self.__build_snapshot(fn_scenario,
                                         timeout_mission=1,
                                         timeout_liveness=1,
                                         timeout_connection=1,
                                         speedup=1,
                                         check_waypoints=True,
                                         use_workaround=True)

        analysis = analyze(snapshot)
        analysis.to_file(fn_out, snapshot)
        logger.info("saved static analysis to disk: %s", fn_out)

    @expose(
        help='computes fault localization from a line coverage report.',
        arguments=[OPT_COVERAGE_FILE]
    )
    def localize(self):
        # type: () -> None
        fn_coverage = self.app.pargs.file
        logger.info("computing fault localization")
        logger.info("using line coverage report: %s", fn_coverage)
        coverage = TestSuiteCoverage.from_file(fn_coverage)
        localization = localize(coverage)
        print(localization)

    @expose(
        help='computes line coverage for a given scenario.',
        arguments=[OPT_FILE,
                   OPT_TIMEOUT,
                   OPT_TIMEOUT_CONNECTION,
                   OPT_LIVENESS,
                   OPT_SPEEDUP,
                   OPT_CHECK_WAYPOINTS,
                   OPT_WORKAROUND])
    def coverage(self):
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

        logger.info("performing fault localization for scenario")
        fn_out = "coverage.json"
        cov = coverage(snapshot, fn_out)
        logger.info("Coverage:\n%s", cov)
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

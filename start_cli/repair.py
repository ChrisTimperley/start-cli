__all__ = ['RepairController']

import logging
import json

from kaskara.analysis import Analysis
from darjeeling.localization import Localization
from darjeeling.transformation import Transformation
from darjeeling.snippet import SnippetDatabase
from bugzoo.util import indent
from bugzoo.core.coverage import TestSuiteCoverage
from start_core.scenario import Scenario
from start_repair.snapshot import Snapshot
from start_repair.validate import validate
from start_repair.localize import compute_coverage, localize
from start_repair.analyze import analyze
from start_repair.repair import repair
from start_repair.repair import transformations as find_transformations
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

    def obtain_snapshot(self):
        # type: () -> None
        return self.__build_snapshot(self.app.pargs.file,
                                     self.app.pargs.timeout_mission,
                                     self.app.pargs.timeout_liveness,
                                     self.app.pargs.timeout_connection,
                                     self.app.pargs.speedup,
                                     self.app.pargs.check_waypoints,
                                     self.app.pargs.use_workaround)

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
                   OPT_LIMIT_CANDIDATES,
                   OPT_NUM_THREADS,
                   OPT_LOCALIZATION,
                   OPT_COVERAGE,
                   OPT_SNIPPETS,
                   OPT_TRANSFORMATIONS,
                   OPT_ANALYSIS,
                   OPT_TIMEOUT,
                   OPT_TIMEOUT_REPAIR,
                   OPT_TIMEOUT_CONNECTION,
                   OPT_LIVENESS,
                   OPT_SPEEDUP,
                   OPT_CHECK_WAYPOINTS,
                   OPT_WORKAROUND])
    def repair(self):
        # type: () -> None
        logger.info("performing repair")
        candidate_limit = self.app.pargs.limit_candidates
        time_limit_mins = self.app.pargs.timeout_repair
        threads = self.app.pargs.threads
        snapshot = self.obtain_snapshot()
        analysis = self.obtain_analysis(snapshot)
        coverage = self.obtain_coverage(snapshot)
        snippets = self.obtain_snippets(snapshot)
        localization = self.obtain_localization(coverage)
        #transformations = self.obtain_transformations(snapshot,
        #                                              coverage,
        #                                              snippets,
        #                                              analysis)

        logger.info("ready to perform repair")

        # # perform repair
        # searcher = \
        #     repair(snapshot, localization, coverage, analysis, transformations,
        #            threads, candidate_limit, time_limit_mins)
        # # FIXME

    def obtain_localization(self, coverage):
        # type: (TestSuiteCoverage) -> Localization
        fn = self.app.pargs.localization
        if not fn:
            logger.info("no localization file provided")
            logger.info("computing fault localization")
            localization = localize(coverage)
            logger.info("computed fault localization:\n%s",
                        indent(repr(localization), 2))
        else:
            logger.info("loading localization from file: %s", fn)
            localization = Localization.from_file(fn)
            logger.info("loaded localization from file:\n%s",
                        indent(repr(localization), 2))
        return localization

    def obtain_transformations(self,
                               snapshot,    # type: Snapshot
                               coverage,    # type: TestSuiteCoverage
                               snippets,    # type: SnippetDatabase
                               analysis     # type: Analysis
                               ):           # type: (...) -> List[Transformation]
        fn = self.app.pargs.transformations
        if not fn:
            logger.info("no transformation database provided")
            logger.info("generating transformation database")
            transformations = find_transformations(snapshot,
                                                   coverage,
                                                   snippets,
                                                   analysis)
            logger.info("generated transformation database")
        else:
            logger.info("loading transformation database: %s", fn)
            # FIXME implement transformation database
            with open(fn, 'r') as f:
                jsn = json.load(f)
            transformations = [Transformation.from_dict(d) for d in jsn]
            logger.info("loaded transformation database (%d transformations)",
                        len(transformations))
        return transformations

    def obtain_coverage(self, snapshot):
        # type: (Snapshot) -> TestSuiteCoverage
        fn = self.app.pargs.coverage
        if not fn:
            logger.info("no line coverage report provided")
            logger.info("generating line coverage report")
            coverage = compute_coverage(snapshot)
            logger.info("generated line coverage report")
        else:
            logger.info("loading line coverage report: %s", fn)
            coverage = TestSuiteCoverage.from_file(fn)
            logger.info("loaded line coverage report")
        return coverage

    def obtain_snippets(self, snapshot):
        # type: (Snapshot) -> SnippetDatabase
        fn = self.app.pargs.snippets
        if not fn:
            logger.info("no snippet database provided")
            logger.info("generating snippet database")
            raise NotImplementedError  # FIXME
            logger.info("generated snippet database: %d snippets",
                        len(snippets))
        else:
            logger.info("loading provided snippet database: %s", fn)
            snippets = SnippetDatabase.from_file(fn)
            logger.info("loaded snippet database: %d snippets", len(snippets))
        return snippets

    def obtain_analysis(self, snapshot):
        # type: (Snapshot) -> Analysis
        fn = self.app.pargs.analysis
        if not fn:
            logger.info("no static analysis provided")
            logger.info("performing static analysis")
            raise NotImplementedError  # FIXME
            logger.info("performed static analysis")
        else:
            logger.info("loading provided static analysis: %s", fn)
            analysis = Analysis.from_file(fn, snapshot)
            logger.info("loaded static analysis")
        return analysis

    @expose(
        help='precomputes the set of transformations for a given scenario.',
        arguments=[OPT_FILE,
                   OPT_COVERAGE,
                   OPT_SNIPPETS,
                   OPT_ANALYSIS,
                   OPT_TIMEOUT,
                   OPT_TIMEOUT_CONNECTION,
                   OPT_LIVENESS,
                   OPT_SPEEDUP,
                   OPT_CHECK_WAYPOINTS,
                   OPT_WORKAROUND])
    def transformations(self):
        # type: () -> None
        fn_out = "transformations.json"

        snapshot = self.obtain_snapshot()
        coverage = self.obtain_coverage(snapshot)
        snippets = self.obtain_snippets(snapshot)
        analysis = self.obtain_analysis(snapshot)

        logger.info("precomputing transformations for scenario")
        transformations = find_transformations(snapshot,
                                               coverage,
                                               snippets,
                                               analysis)
        logger.info("finished precomputing transformations")

        logger.info("writing precomputed transformations to disk: %s", fn_out)
        try:
            jsn = [t.to_dict() for t in transformations]
            with open(fn_out, 'w') as f:
                json.dump(jsn, f)
        except Exception:
            logger.exception("failed to save precomputed transformations to disk")
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
        cov = compute_coverage(snapshot)

        logger.info("saving coverage to disk: %s", fn_out)
        jsn = cov.to_dict()
        with open(fn_out, 'w') as f:
            json.dump(jsn, f)
        logger.info("saved coverage to disk: %s", fn_out)

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

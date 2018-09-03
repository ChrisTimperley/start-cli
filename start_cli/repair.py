__all__ = ['RepairController']

from typing import List
import logging
import json

import start_repair
from start_repair import compute_coverage, Snapshot
from kaskara.analysis import Analysis
from darjeeling.localization import Localization
from darjeeling.transformation import Transformation
from darjeeling.snippet import SnippetDatabase
from darjeeling.candidate import Candidate
from bugzoo.util import indent
from bugzoo.core.coverage import TestSuiteCoverage
from start_core.scenario import Scenario
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
        coverage = self.obtain_coverage(snapshot)
        localization = self.obtain_localization(coverage)
        analysis = self.obtain_analysis(snapshot, localization.files)
        snippets = self.obtain_snippets(snapshot, analysis)
        transformations = self.obtain_transformations(snapshot,
                                                      coverage,
                                                      localization,
                                                      snippets,
                                                      analysis)

        logger.info("ready to perform repair")
        searcher = start_repair.search(snapshot,
                                       localization=localization,
                                       coverage=coverage,
                                       analysis=analysis,
                                       transformations=transformations,
                                       threads=threads,
                                       candidate_limit=candidate_limit,
                                       time_limit_mins=time_limit_mins)

        # FIXME obtain desired number of patches
        logger.info("beginning search process")
        patches = []  # type: List[Candidate]
        try:
            patches.append(next(searcher))
        except StopIteration:
            logger.info("failed to find a patch")

        # report stats
        num_test_evals = searcher.num_test_evals
        num_candidate_evals = searcher.num_candidate_evals
        time_running_mins = searcher.time_running.seconds / 60

        logger.info("found %d plausible patches", len(patches))
        logger.info("time taken: %.2f minutes", time_running_mins)
        logger.info("# test evaluations: %d", searcher.num_test_evals)
        logger.info("# candidate evaluations: %d", searcher.num_candidate_evals)

        # FIXME write patches to disk?

    def obtain_localization(self, coverage):
        # type: (TestSuiteCoverage) -> Localization
        fn = self.app.pargs.localization
        if not fn:
            logger.info("no localization file provided")
            logger.info("computing fault localization")
            localization = start_repair.localize(coverage)
            logger.info("computed fault localization:\n%s",
                        indent(repr(localization), 2))
        else:
            logger.info("loading localization from file: %s", fn)
            localization = Localization.from_file(fn)
            logger.info("loaded localization from file:\n%s",
                        indent(repr(localization), 2))
        return localization

    def obtain_transformations(self,
                               snapshot,        # type: Snapshot
                               coverage,        # type: TestSuiteCoverage
                               localization,    # type: Localization
                               snippets,        # type: SnippetDatabase
                               analysis         # type: Analysis
                               ):               # type: (...) -> List[Transformation]
        fn = self.app.pargs.transformations
        if not fn:
            logger.info("no transformation database provided")
            logger.info("generating transformation database")
            transformations = start_repair.transformations(snapshot,
                                                           coverage,
                                                           localization,
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

    def obtain_snippets(self, snapshot, analysis):
        # type: (Snapshot, Analysis) -> SnippetDatabase
        fn = self.app.pargs.snippets
        if not fn:
            logger.info("no snippet database provided")
            logger.info("generating snippet database")
            snippets = SnippetDatabase.from_statements(analysis.statements)
            logger.info("generated snippet database: %d snippets",
                        len(snippets))
        else:
            logger.info("loading provided snippet database: %s", fn)
            snippets = SnippetDatabase.from_file(fn)
            logger.info("loaded snippet database: %d snippets", len(snippets))
        return snippets

    def obtain_analysis(self, snapshot, files):
        # type: (Snapshot, List[str]) -> Analysis
        fn = self.app.pargs.analysis
        if not fn:
            logger.info("no static analysis provided")
            logger.info("performing static analysis")
            analysis = start_repair.analyze(snapshot, files)
            logger.info("performed static analysis")
        else:
            logger.info("loading provided static analysis: %s", fn)
            analysis = Analysis.from_file(fn, snapshot)
            logger.info("loaded static analysis")
        return analysis

    @expose(
        help='builds the snippet database for a given scenario.',
        arguments=[OPT_FILE,
                   OPT_COVERAGE,
                   OPT_LOCALIZATION,
                   OPT_SNIPPETS,
                   OPT_ANALYSIS,
                   OPT_TIMEOUT,
                   OPT_TIMEOUT_CONNECTION,
                   OPT_LIVENESS,
                   OPT_SPEEDUP,
                   OPT_CHECK_WAYPOINTS,
                   OPT_WORKAROUND,
                   (['--output'],
                     {'help': 'output file for snippet database',
                      'default': 'snippets.json',
                      'type': str})
                   ])
    def snippets(self):
        # type: () -> None
        fn_out = self.app.pargs.output

        snapshot = self.obtain_snapshot()
        coverage = self.obtain_coverage(snapshot)
        localization = self.obtain_localization(coverage)
        analysis = self.obtain_analysis(snapshot, localization.files)

        logger.info("building snippet database for a given scenario")
        snippets = SnippetDatabase.from_statements(analysis.statements)
        logger.info("built snippet database for a given scenario")

        logger.info("saving snippet database to file: %s", fn_out)
        try:
            snippets.to_file(fn_out)
        except Exception:
            logger.exception("failed to save snippet database file: %s", fn_out)  # noqa: pycodestyle
            raise
        logger.info("saved snippet database to file: %s", fn_out)

    @expose(
        help='precomputes the set of transformations for a given scenario.',
        arguments=[OPT_FILE,
                   OPT_COVERAGE,
                   OPT_LOCALIZATION,
                   OPT_SNIPPETS,
                   OPT_ANALYSIS,
                   OPT_TIMEOUT,
                   OPT_TIMEOUT_CONNECTION,
                   OPT_LIVENESS,
                   OPT_SPEEDUP,
                   OPT_CHECK_WAYPOINTS,
                   OPT_WORKAROUND,
                   (['--output'],
                     {'help': 'output file for transformation database',
                      'default': 'transformations.json',
                      'type': str})
                   ])
    def transformations(self):
        # type: () -> None
        fn_out = self.app.pargs.output

        snapshot = self.obtain_snapshot()
        coverage = self.obtain_coverage(snapshot)
        localization = self.obtain_localization(coverage)
        analysis = self.obtain_analysis(snapshot, localization.files)
        snippets = self.obtain_snippets(snapshot, analysis)

        logger.info("precomputing transformations for scenario")
        transformations = start_repair.transformations(snapshot,
                                                       coverage,
                                                       localization,
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
        arguments=[OPT_FILE,
                   OPT_COVERAGE,
                   OPT_LOCALIZATION,
                   OPT_SNIPPETS,
                   OPT_ANALYSIS,
                   OPT_TIMEOUT,
                   OPT_TIMEOUT_CONNECTION,
                   OPT_LIVENESS,
                   OPT_SPEEDUP,
                   OPT_CHECK_WAYPOINTS,
                   OPT_WORKAROUND,
                   (['--output'],
                     {'help': 'output file for static analysis',
                      'default': 'analysis.json',
                      'type': str})
                   ])
    def analyze(self):
        # type: () -> None
        fn_scenario = self.app.pargs.file
        fn_out = self.app.pargs.output
        logger.info("performing static analyis of scenario")

        snapshot = self.obtain_snapshot()
        coverage = self.obtain_coverage(snapshot)
        localization = self.obtain_localization(coverage)
        analysis = start_repair.analyze(snapshot, localization.files)
        analysis.to_file(fn_out, snapshot)
        logger.info("saved static analysis to disk: %s", fn_out)

    @expose(
        help='computes fault localization from a line coverage report.',
        arguments=[OPT_FILE,
                   OPT_COVERAGE,
                   OPT_TIMEOUT,
                   OPT_TIMEOUT_CONNECTION,
                   OPT_LIVENESS,
                   OPT_SPEEDUP,
                   OPT_CHECK_WAYPOINTS,
                   OPT_WORKAROUND,
                   (['--output'],
                     {'help': 'output file to write results to.',
                      'default': 'localization.json',
                      'type': str})
                   ])
    def localize(self):
        # type: () -> None
        fn_coverage = self.app.pargs.file
        fn_out = self.app.pargs.output
        snapshot = self.obtain_snapshot()
        coverage = self.obtain_coverage(snapshot)

        logger.info("computing fault localization")
        localization = start_repair.localize(coverage)
        print(localization)
        logger.info('writing line coverage report to file: %s', fn_out)
        localization.to_file(fn_out)
        logger.info('wrote line coverage report to file: %s', fn_out)

    @expose(
        help='computes line coverage for a given scenario.',
        arguments=[OPT_FILE,
                   OPT_TIMEOUT,
                   OPT_TIMEOUT_CONNECTION,
                   OPT_LIVENESS,
                   OPT_SPEEDUP,
                   OPT_CHECK_WAYPOINTS,
                   OPT_WORKAROUND,
                   (['--output'],
                     {'help': 'output file to coverage report',
                      'default': 'coverage.json',
                      'type': str})
                   ])
    def coverage(self):
        # type: () -> None
        fn_scenario = self.app.pargs.file
        fn_out = self.app.pargs.output
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
        start_repair.validate(snapshot, verbose=self.app.pargs.verbose)
        logger.info("validated scenario")

__all__ = ['TestController']

import logging

from start_core.scenario import Scenario
from start_repair.snapshot import Snapshot
from start_repair.validate import validate
from cement.ext.ext_argparse import ArgparseController, expose

from .opts import *

logger = logging.getLogger(__name__)  # type: logging.Logger
logger.setLevel(logging.DEBUG)


class TestController(ArgparseController):
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
        arguments=[
            OPT_FILE,
            OPT_SPEEDUP,
            OPT_LIVENESS,
            OPT_TIMEOUT,
            OPT_TIMEOUT_CONNECTION,
            OPT_CHECK_WAYPOINTS
        ])
    def execute(self) -> None:
        fn_scenario = self.app.pargs.file

        scenario = self.__load_scenario(fn_scenario)
        logger.info("repairing scenario")

        logger.info("successfully repaired scenario")



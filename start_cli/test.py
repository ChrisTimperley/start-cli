__all__ = ['TestController']

import sys
import logging

from start_core.test import execute as execute_test
from start_core.scenario import Scenario
from cement.ext.ext_argparse import ArgparseController, expose

from .opts import *

logger = logging.getLogger(__name__)  # type: logging.Logger
logger.setLevel(logging.DEBUG)


class TestController(ArgparseController):
    class Meta:
        label = 'test'
        description = 'execute missions using a given ArduPilot binary'
        stacked_on = 'base'
        stacked_type = 'embedded'

    @expose(
        help='executes a given mission on an ArduPilot binary',
        arguments=[
            OPT_FILE,
            OPT_SPEEDUP,
            OPT_LIVENESS,
            OPT_TIMEOUT,
            OPT_TIMEOUT_CONNECTION,
            OPT_ATTACK,
            OPT_CHECK_WAYPOINTS
        ])
    def execute(self):
        # type: () -> None
        fn_scenario = self.app.pargs.file
        timeout_mission = self.app.pargs.timeout_mission
        timeout_liveness = self.app.pargs.timeout_liveness
        timeout_connection = self.app.pargs.timeout_connection
        check_waypoints = self.app.pargs.check_waypoints
        speedup = self.app.pargs.speedup
        scenario = Scenario.from_file(fn_scenario)
        attack = scenario.attack if self.app.pargs.attack else None
        (passed, reason) = execute_test(sitl=scenario.sitl,
                                        mission=scenario.mission,
                                        attack=attack,
                                        speedup=speedup,
                                        timeout_mission=timeout_mission,
                                        timeout_liveness=timeout_liveness,
                                        timeout_connection=timeout_connection,
                                        check_wps=check_waypoints)
        if passed:
            logger.info("mission was successfully completed.")
            sys.exit(0)
        else:
            logger.info("mission failed: %s", reason)
            sys.exit(1)

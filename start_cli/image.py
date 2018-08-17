__all__ = ['ImageController']

import sys
import logging

from start_image.build import build_scenario_image
from start_core.scenario import Scenario
from cement.ext.ext_argparse import ArgparseController, expose

from .opts import *

logger = logging.getLogger(__name__)  # type: logging.Logger
logger.setLevel(logging.DEBUG)


class ImageController(ArgparseController):
    class Meta:
        label = 'image'
        description = 'manages the Docker images for scenarios'
        stacked_on = 'base'
        stacked_type = 'embedded'

    @expose(
        help='builds the Docker image for a given scenario',
        arguments=[OPT_FILE])
    def build(self) -> None:
        fn_scenario = self.app.pargs.file
        logger.info("loading scenario from file [%s]", args.filename)
        scenario = Scenario.from_file(fn_scenario)
        logger.info("loaded scenario")
        image = image_name(scenario)
        logger.info("building image [%s] for scenario [%s]",
                    image, scenario.name)
        build_scenario_image(scenario)
        logger.info("built image [%s] for scenario [%s]",
                    image, scenario.name)

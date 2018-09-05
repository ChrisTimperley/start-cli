__all__ = ['ImageController']

import sys
import logging

from start_image.name import name as image_name
from start_image.build import build_scenario_image
from start_image import install_from_archive, save_to_archive
from start_core.scenario import Scenario
from cement.ext.ext_argparse import ArgparseController, expose
from docker import DockerClient

from .opts import *

logger = logging.getLogger(__name__)  # type: logging.Logger
logger.setLevel(logging.DEBUG)


class ImageController(ArgparseController):
    class Meta:
        label = 'image'
        description = 'manages the Docker images for scenarios'
        stacked_on = 'base'
        stacked_type = 'embedded'

    def obtain_docker(self):
        # type: () -> DockerClient
        return DockerClient(version=self.app.pargs.docker_client)

    @expose(
        help='builds the Docker image for a given scenario',
        arguments=[OPT_FILE, OPT_DOCKER_CLIENT])
    def build(self):
        # type: () -> None
        fn_scenario = self.app.pargs.file
        dkr = self.obtain_docker()

        logger.info("loading scenario from file [%s]", fn_scenario)
        scenario = Scenario.from_file(fn_scenario)
        logger.info("loaded scenario")
        name_image = image_name(scenario)
        logger.info("building image [%s] for scenario [%s]",
                    name_image, scenario.name)
        build_scenario_image(dkr, scenario)
        logger.info("built image [%s] for scenario [%s]",
                    name_image, scenario.name)

    @expose(
        help='installs the Docker image for a scenario from an archive',
        arguments=[OPT_FILE,
                   OPT_ARCHIVE,
                   OPT_DOCKER_CLIENT])
    def install(self):
        # type: () -> None
        fn_scenario = self.app.pargs.file
        fn_archive = self.app.pargs.fn_archive
        dkr = self.obtain_docker()

        logger.info("loading scenario from file [%s]", fn_scenario)
        scenario = Scenario.from_file(fn_scenario)
        logger.info("loaded scenario")
        image = image_name(scenario)

        logger.info("installing Docker image [%s] for scenario [%s] from archive: %s",
                    image, scenario.name, fn_archive)
        try:
            install_from_archive(dkr, scenario, fn_archive)
        except Exception:
            logger.exception("failed to install image from archive")
            raise
        logger.info("installed Docker image [%s] for scenario [%s] from archive: %s",
                    image, scenario.name, fn_archive)

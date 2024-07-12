import glob
import os
from importlib.util import spec_from_file_location, module_from_spec

from aiohttp import web

from schedulr.logger import log_info
from schedulr.routes import Routes


def load_route_modules(base_path: str = "schedulr/routes") -> None:
    for file_path in glob.glob(os.path.join(base_path, "*.py")):
        module_name = os.path.basename(file_path)[:-3]
        if module_name not in ["app"]:
            spec = spec_from_file_location(module_name, file_path)
            if spec is None:
                continue
            module = module_from_spec(spec)
            if module is None or spec.loader is None:
                continue
            spec.loader.exec_module(module)


class Schedulr:
    def __init__(self) -> None:
        log_info("Initializing Schedulr")
        self.app: web.Application = web.Application()

    def run(self) -> web.Application:
        log_info("Running Schedulr")
        load_route_modules()
        Routes(self.app).activate()
        return self.app


async def start_app() -> web.Application:
    schedulr = Schedulr()
    return schedulr.run()

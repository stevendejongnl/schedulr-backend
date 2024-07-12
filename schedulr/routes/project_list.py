from aiohttp import web
from aiohttp.web_request import Request

from schedulr.modules.project.project_list import ProjectList
from schedulr.routes import Routes


class ProjectListRoutes:
    @staticmethod
    @Routes.register("/project_list", "GET")
    async def overview(request: Request) -> web.Response:
        project_list = ProjectList()
        return web.json_response({"project_list": project_list.get_projects()})

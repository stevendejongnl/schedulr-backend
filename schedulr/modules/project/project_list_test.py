from schedulr.modules.project.project_list import Project, ProjectList, ProjectType
from datetime import datetime


def test_add_project() -> None:
    project_list = ProjectList()
    project = Project(
        name="Get a life",
        project_type=ProjectType.SUPER_SPECIAL,
        description="Do something with your life",
        start_date=datetime(2024, 7, 1),
        end_date=datetime(2024, 12, 31),
    )
    project_list.add_project(project)

    assert len(project_list.get_projects()) == 1
    assert project_list.get_projects()[0].name == "Get a life"
    assert project_list.get_projects()[0].project_type == ProjectType.SUPER_SPECIAL
    assert project_list.get_projects()[0].description == "Do something with your life"
    assert project_list.get_projects()[0].start_date == datetime(2024, 7, 1)
    assert project_list.get_projects()[0].end_date == datetime(2024, 12, 31)

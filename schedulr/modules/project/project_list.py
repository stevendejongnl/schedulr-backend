from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ProjectType(Enum):
    BASIC = "Basic"
    SPECIAL = "Special"
    SUPER_SPECIAL = "Super Special"


@dataclass(frozen=True)
class Project:
    name: str
    project_type: ProjectType
    description: str
    start_date: datetime
    end_date: datetime


class ProjectList:
    def __init__(self) -> None:
        self.list: list[Project] = []

    def add_project(self, project: Project) -> None:
        self.list.append(project)

    def get_projects(self) -> list[Project]:
        return self.list

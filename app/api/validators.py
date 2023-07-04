from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.services.investing import close_investment


async def check_name_duplicate(
    project_name: str, session: AsyncSession
) -> None:
    """Проверка названия проекта на уникальность"""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """Проверка на существование проекта"""
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(status_code=404, detail='Проект не был найден!')
    return project


def check_charity_project_closed(
    project: CharityProject,
):
    """Проверка, закрыт ли проект."""
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    return project


def check_if_full_amount_enough(
    project: CharityProject, full_amount: int
) -> CharityProject:
    """Проверка: закрыть и обновить проект"""
    if full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя установить требуемую сумму меньше вложенной'
        )
    if full_amount == project.invested_amount:
        close_investment(project)
    return project


def check_charity_project_invested(
    charity_project: CharityProject,
) -> None:
    """Проверка на внесенные средства в проект"""
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )

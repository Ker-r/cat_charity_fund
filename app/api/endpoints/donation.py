from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationMyDB
from app.services.investing import investment

router = APIRouter()


@router.post(
    '/', response_model=DonationMyDB, response_model_exclude_none=True,
)
async def create_donation(
    reservation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Create donation."""
    new_donation = await donation_crud.create(reservation, session, user)
    await investment(new_donation, charity_project_crud, session)
    return new_donation


@router.get(
    '/',
    response_model=List[DonationDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Получить список всех донатов (для суперюзеров)"""
    return await donation_crud.get_multi(session)


@router.get('/my', response_model=List[DonationMyDB])
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Получить список донатов текущего пользователя"""
    return await donation_crud.get_by_user(session=session, user=user)

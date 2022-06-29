from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse


from app.services.database.dao.trasaction_dao import TransactionDAO
from app.services.database.dao.user_dao import UserDAO, NegativeBalanceEXC
from app.services.security.jwt import get_current_user_check_jwt
from app.services.database.base import get_dao
from app.schemas.user_schemas import UserScheme


router = APIRouter(
    prefix="/api/v1/account",
    tags=["account/user"]
)


@router.post('/cachein')
async def cache_in(
        amount: int,
        user: UserScheme = Depends(get_current_user_check_jwt),
        transaction_dao: TransactionDAO = Depends(get_dao(TransactionDAO)),
        user_dao: UserDAO = Depends(get_dao(UserDAO))
):
    await user_dao.update_user_balance(user_id=user.id, amount=amount, operation='+')
    is_declined = False
    response = JSONResponse(status_code=200, content={'message': 'операция одобрена'})
    await transaction_dao.create_transaction(user_id=user.id, amount=amount, operation='+', is_declined=is_declined)
    return response


@router.post('/cacheout')
async def cache_out(
        amount: int,
        user: UserScheme = Depends(get_current_user_check_jwt),
        transaction_dao: TransactionDAO = Depends(get_dao(TransactionDAO)),
        user_dao: UserDAO = Depends(get_dao(UserDAO))
):
    try:
        await user_dao.update_user_balance(user_id=user.id, amount=amount, operation='-')
        is_declined = False
        response = JSONResponse(status_code=200, content={'message': 'операция одобрена'})
    except NegativeBalanceEXC:
        is_declined = True
        response = JSONResponse(status_code=200, content={'message': 'операция отклонена'})
    await transaction_dao.create_transaction(user_id=user.id, amount=amount, operation='-', is_declined=is_declined)
    return response

from fastapi import APIRouter, Depends, Body, HTTPException, status

from app.core.jwt import create_access_token
from app.db.firebase import FireBase, get_token
from app.db.mongodb import AsyncIOMotorClient, get_mongodb
from app.models.user import UserInLogin, UserInCreate, UserInLoginViaEmail
from app.crud.user import check_free_username_and_email, get_user, create_user, get_user_by_email

router = APIRouter()


@router.post(
    '/auth/login',
    response_model=UserInLogin,
    tags=['authentication'],
)
async def login(
    firebase: FireBase,
    db: AsyncIOMotorClient = Depends(get_mongodb),
):
    firebase_user_data = get_token(token=firebase.firebase_token)
    token = create_access_token(
        data={'firebase_id': firebase_user_data['user_id']}
    )
    auth_provider = firebase_user_data['firebase']['sign_in_provider']
    user_in_db = await get_user(db, firebase_id=firebase_user_data['user_id'])
    if not user_in_db:
        if auth_provider == 'phone':
            await create_user(
                db,
                user=UserInCreate(
                    firebase_id=firebase_user_data['user_id'],
                    phone_number=firebase_user_data['phone_number'],
                    sign_in_provider=auth_provider,
                )
            )
        elif auth_provider == 'facebook.com':
            await create_user(
                db,
                user=UserInCreate(
                    firebase_id=firebase_user_data['user_id'],
                    sign_in_provider=auth_provider,
                )
            )

    return UserInLogin(**firebase_user_data, access_token=token)


@router.post(
    '/auth/login_via_email',
    response_model=UserInLogin,
    tags=['authentication']
)
async def login_via_email(
    user: UserInLoginViaEmail = Body(..., embed=True),
    db: AsyncIOMotorClient = Depends(get_mongodb)
):
    dbuser = await get_user_by_email(db, user.email)
    if not dbuser or not dbuser.check_password(user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Incorrect email or password'
        )

    token = create_access_token(
        data={'email': dbuser.email}
    )
    return UserInLogin(access_token=token)


@router.post(
    '/auth/create',
    response_model=UserInLogin,
    tags=['authentication']
)
async def add_user_by_email(
    user: UserInCreate = Body(..., embed=True),
    db: AsyncIOMotorClient = Depends(get_mongodb)
):
    if not user.email or not user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email or password'
        )

    await check_free_username_and_email(db, user.username, user.email)

    async with await db.start_session() as s:
        async with s.start_transaction():
            dbuser = await create_user(db, user)
            token = create_access_token(
                data={'email': dbuser.email}
            )

            return UserInLogin(access_token=token)

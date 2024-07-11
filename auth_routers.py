import datetime
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_
from database import SesionLocal, engine
from schemas import SignupModel, LoginModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT

session = SesionLocal(bind=engine)
auth_router = APIRouter(
    prefix="/auth"
)


@auth_router.get("/")
async def auth_(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": "Hello auth"}


@auth_router.get("/")
async def auth_():
    return {"message": "Hello auth"}


@auth_router.post('/signup', status_code=201)
async def signup(user: SignupModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        return {'message': 'Email already exists', 'status_code': status.HTTP_400_BAD_REQUEST}
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        return {'message': 'Username already exists', 'status_code': status.HTTP_400_BAD_REQUEST}
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )
    session.add(new_user)
    session.commit()
    user_data = {

        'username': user.username,
        'email': user.email,
        'is_active': user.is_active,
        'is_staff': user.is_staff,
    }
    return {'message': 'User created successfully', 'new_user': user_data, 'status': status.HTTP_201_CREATED}


@auth_router.post('/login', status_code=200)
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    db_user = session.query(User).filter(
        or_(
            User.username == user.username_or_email, User.email == user.username_or_email
        )).first()
    if db_user and check_password_hash(db_user.password, user.password):
        access_lifetime = datetime.timedelta(minutes=60)
        refresh_lifetime = datetime.timedelta(days=3)
        access_token = Authorize.create_access_token(subject=db_user.username,
                                                     expires_time=access_lifetime)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username,
                                                       expires_time=refresh_lifetime)
        token = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        response_data = {
            'status': status.HTTP_200_OK,
            'message': "Successfully logged in",
            'token': token
        }
        return response_data
    raise HTTPException(status=status.HTTP_400_BAD_REQUEST,
                        detail='Invalid username, email or password')

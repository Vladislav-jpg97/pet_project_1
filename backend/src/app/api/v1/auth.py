from fastapi import APIRouter,status

from app.dependencies.auth import UserServiceDep
from app.schemas.user import UserRegister, UserResponse, UserLogin, Token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserRegister,
    user_service: UserServiceDep
):
    return await user_service.create_user(user_in)

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(
        user_in: UserLogin,
        user_service: UserServiceDep
):
    return await user_service.login_user(user_in)
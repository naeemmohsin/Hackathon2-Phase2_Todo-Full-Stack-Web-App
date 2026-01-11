"""Authentication API endpoints."""

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from ..api.deps import DbSession, CurrentUser
from ..models.user import User
from ..schemas.user import RegisterRequest, LoginRequest, UserResponse, AuthResponse
from ..services.auth import hash_password, verify_password, create_access_token

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: DbSession) -> AuthResponse:
    """
    Register a new user.

    - Validates email uniqueness
    - Hashes password with bcrypt
    - Returns user data and JWT token
    """
    # Check if email already exists
    statement = select(User).where(User.email == request.email)
    existing_user = db.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create new user with hashed password
    user = User(
        email=request.email,
        password_hash=hash_password(request.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate JWT token
    token = create_access_token(user_id=user.id, email=user.email)

    return AuthResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at,
        ),
        token=token,
    )


@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest, db: DbSession) -> AuthResponse:
    """
    Authenticate user and return JWT token.

    - Validates email exists
    - Verifies password against stored hash
    - Returns user data and JWT token
    """
    # Find user by email
    statement = select(User).where(User.email == request.email)
    user = db.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Generate JWT token
    token = create_access_token(user_id=user.id, email=user.email)

    return AuthResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at,
        ),
        token=token,
    )


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(current_user: CurrentUser) -> dict:
    """
    Logout user.

    Note: With JWT, logout is typically handled client-side by removing the token.
    This endpoint exists for API completeness and can be extended for token blacklisting.
    """
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: CurrentUser) -> UserResponse:
    """
    Get current authenticated user information.

    Returns the user data associated with the JWT token.
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        created_at=current_user.created_at,
    )

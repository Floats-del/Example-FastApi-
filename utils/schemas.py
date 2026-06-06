from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, Literal

# =====================================================================
# --- INCOMING REQUEST PAYLOAD SCHEMAS (Data sent BY User to API) ---
# =====================================================================

class PostCreateSchema(BaseModel):
    """
    Used in: routers/posts.py
    Routes: 
      - POST /posts/  (Creating a brand new post)
      - PUT  /posts/{id} (Updating an existing post's details)
    """
    title: str = Field(..., description="Title of the post", max_length=200)
    content: str = Field(..., description="Content of the post", max_length=5000)
    published: bool = Field(True, description="Public visibility status")


class UserRegisterSchema(BaseModel):
    """
    Used in: routers/users.py
    Route:  POST /users/ (Registering/creating a brand new account)
    """
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel): 
    """
    Used in: routers/auth.py
    Route:  POST /login (Standard data validation if OAuth2Form isn't used)
    """
    email: EmailStr
    password: str


class LikeSchema(BaseModel):
    """
    Used in: routers/likes.py
    Route:  POST /likes/ (Liking or unliking a specific post)
    """
    post_id: int
    dir: Literal[0, 1]  # Strict enforcement: 1 for liking, 0 for removing a like


# =====================================================================
# --- OUTGOING RESPONSE PAYLOAD SCHEMAS (Data sent BY API back to User) ---
# =====================================================================

class UserResponseSchema(BaseModel):
    """
    Used in: routers/users.py
    Routes: 
      - POST /users/  (Returns newly created user profile info minus the password)
      - GET  /users/  (Returns a list of user profiles)
      - GET  /users/{id} (Returns a single user profile)
    Also Nested Inside: PostResponseSchema as the "owner" object.
    """
    email: EmailStr
    user_id: int 
    created_at: datetime
    
    model_config = {"from_attributes": True}


class PostResponseSchema(PostCreateSchema):
    """
    Used in: routers/posts.py
    Routes:
      - POST /posts/ (Returns the newly created post with ID, user_id, and owner info)
      - PUT  /posts/{id} (Returns the freshly updated post object data)
    """
    post_id: int 
    user_id: int 
    owner: UserResponseSchema # Nests the user details who authored it
    
    model_config = {"from_attributes": True} 


class TokenSchema(BaseModel): 
    """
    Used in: routers/auth.py
    Route:  POST /login (Returns the bearer token structure string to clients)
    """
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel): 
    """
    Used in: Oauth2.py
    Function: verify_access_token & get_user_jwt_payload
    Purpose: Internal verification schema to hold decrypted token payloads (the user_id).
    """
    user_id: Optional[int] = None


class PostLikesOutSchema(BaseModel):
    """
    Used in: routers/posts.py
    Routes:
      - GET /posts/    (The main social media feed displaying posts + like counts)
      - GET /posts/{id} (Fetching a specific post to see its single layout + like count)
    """
    post: PostResponseSchema # Nests the entire post layout and its user owner
    likes: int               # Packs the aggregate database count number alongside it
    
    model_config = {"from_attributes": True}
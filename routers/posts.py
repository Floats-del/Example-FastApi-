from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func
from db_tables.tables import PostTable, LikeTable
from db import get_db
from typing import List, Optional
from utils.schemas import PostLikesOutSchema, PostResponseSchema, PostCreateSchema
from Oauth2 import get_user_jwt_payload
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get("/", response_model=List[PostLikesOutSchema])
def get_all_posts(
    db: Session = Depends(get_db),
    user_payload = Depends(get_user_jwt_payload),
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = None
):
    # Alias structural names to circumvent internal naming dict parsing validation issues
    post_alias = aliased(PostTable, name="post") 

    # Build relational aggregate projection query
    query = db.query(
        post_alias, 
        func.count(LikeTable.post_id).label("likes")
    ).join(
        LikeTable, 
        LikeTable.post_id == post_alias.post_id, 
        isouter=True
    ).group_by(post_alias.post_id)

    if search:
        query = query.filter(post_alias.title.contains(search))

    results = query.offset(offset).limit(limit).all()
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponseSchema) 
def create_post(
    new_post: PostCreateSchema, 
    user_payload = Depends(get_user_jwt_payload),
    db: Session = Depends(get_db)
):
    jwt_payload = user_payload.model_dump()
    post = PostTable(user_id=jwt_payload["user_id"], **new_post.model_dump())    

    try:
        db.add(post)
        db.commit()
        db.refresh(post)
    except SQLAlchemyError:
        db.rollback() 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database operational failure. Verify data formats and sizes."
        )
    return post 


@router.get("/{id}", response_model=PostLikesOutSchema)  
def get_post_by_id(
    id: int, 
    user_payload = Depends(get_user_jwt_payload),
    db: Session = Depends(get_db)
):  
    post_alias = aliased(PostTable, name="post") 
    
    results = db.query(
        post_alias, 
        func.count(LikeTable.post_id).label("likes")
    ).join(
        LikeTable, 
        LikeTable.post_id == post_alias.post_id, 
        isouter=True
    ).filter(
        post_alias.post_id == id
    ).group_by(post_alias.post_id).first()
    
    if not results:
        raise HTTPException(status_code=404, detail="Post Not Found!")
        
    return results


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_post_by_id(
    id: int, 
    user_payload = Depends(get_user_jwt_payload),
    db: Session = Depends(get_db)
):
    current_user = user_payload.model_dump()
    post = db.query(PostTable).filter(PostTable.post_id == id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post Not Found!")
    
    if post.user_id != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to delete this post!")

    db.delete(post)
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT)  


@router.put("/{id}", response_model=PostResponseSchema)
def update_by_id(
    id: int, 
    post_data: PostCreateSchema, 
    user_payload = Depends(get_user_jwt_payload),
    db: Session = Depends(get_db)
):
    current_user = user_payload.model_dump()
    new_data = post_data.model_dump()
    fetched_post = db.query(PostTable).filter(PostTable.post_id == id).first()
    
    if not fetched_post:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} was not found!")
    
    if fetched_post.user_id != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to Update this post")
    
    for key, value in new_data.items():
        setattr(fetched_post, key, value)

    db.commit()
    db.refresh(fetched_post)
    return fetched_post
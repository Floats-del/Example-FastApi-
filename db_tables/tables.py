from db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class PostTable(Base): 
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")) 
    
    user_id = Column(
        Integer, 
        ForeignKey("users.user_id", ondelete="CASCADE", onupdate="SET_DEFAULT"), 
        nullable=False
    )
    
    # Relationships
    owner = relationship("UserTable", back_populates="posts")
    likers = relationship("UserTable", secondary="likes", back_populates="liked_posts")


class UserTable(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")) 
    
    # Relationships
    posts = relationship("PostTable", back_populates="owner")
    liked_posts = relationship("PostTable", secondary="likes", back_populates="likers")


class LikeTable(Base):
    __tablename__ = "likes"
    
    # Composite key setup to restrict a single user to one like per post
    user_id = Column(
        Integer, 
        ForeignKey("users.user_id", ondelete="CASCADE"), 
        primary_key=True
    )
    post_id = Column(
        Integer, 
        ForeignKey("posts.post_id", ondelete="CASCADE"), 
        primary_key=True
    )
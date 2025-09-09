"""
Sample FastAPI application for testing the guidance template.
"""

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import uvicorn

app = FastAPI(title="User Management API", version="1.0.0")

# Pydantic models
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: Optional[int] = None

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None

# Mock database
users_db = [
    User(id=1, name="John Doe", email="john@example.com", age=30),
    User(id=2, name="Jane Smith", email="jane@example.com", age=25),
    User(id=3, name="Bob Johnson", email="bob@example.com", age=35)
]

def get_db():
    """Mock database dependency"""
    return users_db

def get_user_by_id(user_id: int, db: List[User] = Depends(get_db)) -> User:
    """Get user by ID with dependency injection"""
    user = next((u for u in db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# API endpoints
@app.get("/", summary="Root endpoint")
async def root():
    """Root endpoint for health check"""
    return {"message": "User Management API", "version": "1.0.0"}

@app.get("/users", response_model=List[User], summary="Get all users")
async def get_users(db: List[User] = Depends(get_db)):
    """Get all users"""
    return db

@app.get("/users/{user_id}", response_model=User, summary="Get user by ID")
async def get_user(user: User = Depends(get_user_by_id)):
    """Get a specific user by ID"""
    return user

@app.post("/users", response_model=User, status_code=201, summary="Create new user")
async def create_user(user: UserCreate, db: List[User] = Depends(get_db)):
    """Create a new user"""
    new_id = max(u.id for u in db) + 1
    new_user = User(id=new_id, **user.dict())
    db.append(new_user)
    return new_user

@app.put("/users/{user_id}", response_model=User, summary="Update user")
async def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    db: List[User] = Depends(get_db)
):
    """Update an existing user"""
    user = next((u for u in db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields if provided
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    return user

@app.delete("/users/{user_id}", status_code=204, summary="Delete user")
async def delete_user(user_id: int, db: List[User] = Depends(get_db)):
    """Delete a user"""
    user = next((u for u in db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.remove(user)
    return None

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"detail": "Resource not found"}

@app.exception_handler(422)
async def validation_error_handler(request, exc):
    return {"detail": "Validation error", "errors": exc.errors()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

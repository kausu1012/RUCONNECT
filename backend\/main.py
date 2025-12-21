from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
from auth import hash_password, verify_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Login & Signup API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ SIGNUP API
@app.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.SignupSchema, db: Session = Depends(get_db)):
    
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        customer_type=user.customer_type.lower()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# ✅ LOGIN API
@app.post("/login")
def login(data: schemas.LoginSchema, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "Login successful",
        "user_id": user.id,
        "name": user.name,
        "customer_type": user.customer_type
    }

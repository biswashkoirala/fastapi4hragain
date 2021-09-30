from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.param_functions import Body
from sqlalchemy import schema
from sqlalchemy.orm import Session
from starlette.responses import Response
from . import schemas, models
from blog.database import engine, SessionLocal



app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get('/', tags=['test'])
def index():
    return ({'Hello World':'Cool'})

@app.get('/blogs', tags=['blogs'])
def all(db: Session =Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs



@app.get('/blog/{id}', tags=['blogs'])
def show(id, db: Session =Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog




@app.get('/blog/{id}/comments', tags=['test'])
def comments(id):
    return ({'comments': {'comments':'list'}})



@app.post('/blog', tags=['blogs'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body= request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
    

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).update({'title': request.title, 'body': request.body})
    db.commit()
    return {'message':f'blog with id {id} updated'}

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delete(id, db:Session =Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    #return {'message': f'Blog with id {id} deleted'}


@app.post('/user', response_model=schemas.ShowUser, tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db) ):
    new_user = models.User(name= request.name, email = request.email, password = request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}',response_model=schemas.ShowUser, tags=['users'])
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f'User with id {id} is not available')
    return user
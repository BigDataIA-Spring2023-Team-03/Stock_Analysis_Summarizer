from fastapi import FastAPI, Depends, status, HTTPException, Response
from Util import db_util

import os
import schemas
from Authentication import auth, auth_bearer

app = FastAPI()

########################################################################################################################

@app.get("/user_info", tags=['user'])
async def read_main(token):
    return auth.get_user_data(token)

@app.post('/user/register', tags=['user'])
def register(user: schemas.UserRegisterSchema):
    if not db_util.check_user_exists(user.email):
        db_util.insert_user(user.email, auth.get_password_hash(user.password), user.service_plan, user.admin_flag)
        return auth.signJWT(user.email)
    else:
        raise HTTPException(status_code=400, detail="User with that email already exists")
    return auth.signJWT(user.email)


@app.post('/user/login', tags=['user'])
def login(user: schemas.UserLoginSchema):
    if db_util.check_user(user.email, user.password):
        return auth.signJWT(user.email)
    else:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')

@app.post('/update_plan', tags=['user'], status_code=status.HTTP_200_OK, dependencies=[Depends(auth_bearer.JWTBearer())])
def update_serviceplan(user: schemas.ServicePlan):
    if user:
        return db_util.update_serviceplan(user.service_plan, user.email)
    else:
        raise HTTPException(status_code=401, detail='Error while updating the service plan')

@app.get("/user_data", tags=['user'])
async def read_main(email: str):
    if email and not email == '':
        return db_util.get_user_data(email)

@app.post('/update_api_calls', tags=['user'], status_code=status.HTTP_200_OK, dependencies=[Depends(auth_bearer.JWTBearer())])
def update_api_calls(user: schemas.ApiCalls):
    if user.email and not user.email == '':
        return db_util.update_api_calls(user.email)
    else:
        raise HTTPException(status_code=401, detail='Error while updating the service plan')

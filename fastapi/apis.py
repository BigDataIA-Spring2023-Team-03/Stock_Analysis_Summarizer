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
    else:
        raise HTTPException(status_code=400, detail="User with that email already exists")
    return auth.signJWT(user.email)


@app.post('/user/login', tags=['user'])
def login(user: schemas.UserLoginSchema):
    if db_util.check_user(user.email, user.password):
        return auth.signJWT(user.email)
    else:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')

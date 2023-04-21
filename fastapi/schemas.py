from pydantic import BaseModel, EmailStr

class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    service_plan: str
    admin_flag: bool = False


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class ServicePlan(BaseModel):
    service_plan: str
    email: str

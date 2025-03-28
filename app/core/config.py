from pydantic_settings import BaseSettings


class ENV(BaseSettings):

    DATABASE_HOST : str = "localhost"
    DATABASE_USERNAME : str 
    DATABASE_PASSWORD : str 
    DATABASE_PORT : str 
    DATABASE_NAME : str 
    SECRET_KEY : str = "DO NOT USE THIS STRING AS SECRET KEY THIS IS ONLY FOR DEV PURPOSES "
    ALGORITHM : str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 4300
    HASH_ROUND : int = 100

    class Config:
        env_file = ".env"


Evariable=ENV()
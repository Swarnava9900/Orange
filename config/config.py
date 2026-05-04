class Config:
    SECRET_KEY = "bsga&367bi4e6eiariulg@lrs367hhrs5647hlbl64bi67547"
    JWT_SECRET_KEY = "o58bw8y9t5v03y9wybu8p98yvgwgou5vw93y9o"
    JWT_TOKEN_LOCATION = ["headers"]

    SQLALCHEMY_DATABASE_URI = "sqlite:///orange.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
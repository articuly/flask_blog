class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"  ## ///为相对路经，////为绝对路经
    ALLOW_UPLOAD_TYPE = ['image/jpeg', 'image/png', 'image/gif']
    SECRET_KEY = "123654"


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

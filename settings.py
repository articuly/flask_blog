class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"  ## ///为相对路经，////为绝对路经
    ALLOW_UPLOAD_TYPE = ['image/jpeg', 'image/png', 'image/gif']
    SECRET_KEY = "123654"
    # CKEDITOR配置
    CKEDITOR_WIDTH = "\"100%\""
    CKEDITOR_HEIGHT = "600"
    CKEDITOR_FILE_UPLOADER = "upload_app.ckeditor_upload"
    CKEDITOR_FILE_BROWSER = "upload_app.ckeditor_browser"


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

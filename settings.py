class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"  ## ///为相对路经，////为绝对路经
    ALLOW_UPLOAD_TYPE = ['image/jpeg', 'image/png', 'image/gif']
    SECRET_KEY = "123654"

    # CKEDITOR配置
    CKEDITOR_WIDTH = "\"100%\""
    CKEDITOR_HEIGHT = "600"
    CKEDITOR_LANGUAGE = 'zh-cn'
    CKEDITOR_FILE_UPLOADER = "upload_app.ckeditor_upload"
    CKEDITOR_FILE_BROWSER = "upload_app.ckeditor_browser"

    # Dropzone配置
    DROPZONE_MAX_FILE_SIZE = 10
    DROPZONE_MAX_FILE = 10
    # DROPZONE_ALLOWED_FILE_TYPE="image"
    DROPZONE_ALLOWED_FILE_CUSTOM = True
    DROPZONE_ALLOWED_FILE_TYPE = "image/*, .ico, .webp"
    DROPZONE_ENABLE_CSRF = True
    DROPZONE_INPUT_NAME = "upload"
    DROPZONE_DEFAULT_MESSAGE = '点击或拖拽文件到这里上传'


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

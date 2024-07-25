


def InitRestxConfig(app):
    pass
    """
    RESTX_JSON = {
        'sort_keys': bool-True 是否自动排序
        'ensure_ascii': bool-True 是否将非ASCII字符转换为Unicode
        'indent': int JSON缩进空格数
        'spearators': (',', ':') 接受一个元组，项之间和键值对之间的分隔符
        'default': function 指定一个函数，当遇到JSON无法序列化时，调用次函数来处理
    }
    ERROR_404_HELP: 控制当API找不到时是否显示帮助信息。通常接受布尔值1。
    HTTP_BASIC_AUTH_REALM: 指定基本认证的领域（realm），通常是对被访问系统的描述。接受字符串类型的数据1。
    SWAGGER_VALIDATOR_URL: 设置自定义的Swagger验证器的URL。接受字符串格式的URL1。
    SWAGGER_UI_DOC_EXPANSION: 控制Swagger UI文档的初始展开状态。接受字符串，有效值为'none', 'list', 或 'full'1。
    SWAGGER_UI_OPERATION_ID: 用于控制Swagger UI中操作的ID。接受布尔值1。
    SWAGGER_UI_REQUEST_DURATION: 显示在Swagger UI中发起请求的持续时间。接受布尔值1。
    SWAGGER_UI_OAUTH_APP_NAME: 设置OAuth应用的名称，用于Swagger UI中。接受字符串类型的数据1。
    SWAGGER_UI_OAUTH_CLIENT_ID: 设置OAuth客户端ID，用于Swagger UI中的OAuth2流程。接受字符串类型的数据1。
    SWAGGER_UI_OAUTH_REALM: 指定OAuth的领域（realm），添加为授权URL和令牌URL的查询参数。接受字符串类型的数据1。
    SWAGGER_SUPPORTED_SUBMIT_METHODS: 控制Swagger UI中哪些方法显示“Try it Out”按钮。接受字符串数组，有效方法如['get', 'post', 'put', 'delete']等1。
    """

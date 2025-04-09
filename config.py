#configurando a aplicação anterior
SECRET_KEY = 'mysecretkey'
CACHE_TYPE = 'simple'
SWAGGER = {
    'title': 'Catalogo de Receitas API',
    'uiversion': 3
}
SQLALCHEMY_DATABASE_URI = 'sqlite:///recipes.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = 'myjwtsecretkey'





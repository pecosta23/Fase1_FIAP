from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)

app = Flask (__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
jwt = JWTManager(app)
swagger = Swagger(app)

class User (db.Model):
    id = db.Column (db.Integer, primary_key = True)
    username = db.Column (db.String(80), unique = True, nullable = False)
    password = db.Column (db.String(120), nullable = False)

class Recipe (db.Model):
    id = db.Column (db.Integer, primary_key = True)
    tittle = db.Column (db.String (120), nullable = False)
    ingredients = db.Column (db.Text, nullable = False)
    time_minutes = db.Column (db.Integer, nullable = False)

#helou flask
@app.route('/')
def home():
    return "Hello, Flask"

#adicionando um novo usuario
@app. route('/register', methods = ['POST'])
def register_user():
    """
    Registra um novo usuario.
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
         type: object
         properties:
           username:
             type: string
             password:
             type: string
    responses:
      201:
        description: Usuario criado com sucesso
      400:
        description: Usuario ja exxiste
    """
    data = request.get_json()
    if User.query.filter_by(username = data['username']).first():
        return jsonify({"error": "User already exists"}), 400
    new_user = User(username = data['username'], password = data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User created"}), 201


#capturando dados
@app.route('/login', methods = ['POST'])
def login():
    """
    Faz login do usuario e retorna um JWT
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
         type: object
         properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login realizado com sucesso, retorno JWT
      401:
        description: Credenciais invalidas
    """
    data = request.get_json()
    user = User.query.filter_by(username = data['username']).first()
    if user and user.password == data['password']:
        #convertendo ID para string
        token = create_access_token(identity = str(user.id))
        return jsonify({"access_token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401

#rota simples para testar o JWT
@app.route('/protected', methods = ['GET'])
@jwt_required()
def protected():
    """
    Rota protegida que retorna o ID do usuario logado
    ---
    responses:
      200:
        description: Retorna o ID do usuario logado
    """
    current_user_id = get_jwt_identity()
    return jsonify({"msg": f"Usuario com ID {current_user_id} acessou a rota protegida"}), 200

#rota post de receitas
@app.route('/recipes', methods = ['POST'])
@jwt_required()
def create_recipe():
    """
    Cria uma nova receita
    ---
    security:
      - BearerAtuh: []
    parameters:
      - in body:
        name: body
        schema:
          type: object
          properties:
            title:
              type: string
            ingredients:
              type: string
            time_minutes:
              type: integer
    responses:
      201:
        description: Receita criada com sucesso
      401:
        description: Token nao fornecido ou invalido
    """
    data = request.get_json()
    new_recipe = Recipe(
        tittle = data['tittle'],
        ingredients = data['ingredients'],
        time_minutes = data['time_minutes']
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({"msg": "Recipe created successfully"}), 201

#pegando as receitas
@app.route('/recipes', methods = ['GET'])
def get_recipes():
  """
    Lista receitas com filtros opcionais
    ---
    parameters:
      - in: query
        name: ingredient
        type: string
        required: false
        description: Filtra por ingredientes
      - in: query
        name: max_time
        type: integer
        required: false
        description: Tempo maximo de preparo
    responses:
        200:
          description: Lista de receitas filtradas
          schema:
            type: array
            items:
              type: object
              properties:
                id:
                  type: integer
                tittle:
                  type: string
                time_minutes:
                  type integer
    """
  ingredient = request.args.get('ingredient')
  max_time = request.args.get('max_time')

  query = Recipe.query
  if ingredient:
      query = query.filter(Recipe.ingredients.ilike(f'%{ingredient}'))
  if max_time:
      query = query.filter(Recipe.time_minutes <= max_time)
    
  recipes = query.all()
  return jsonify([
      {
          "id": r.id,
          "tittle": r.tittle,
          "ingredients": r.ingredients,
          "time_minutes": r.time_minutes
      }
      for r in recipes
  ])

#criando o put para atualizar receitas
@app.route('/recipes/<int:recipe_id>', methods = ['PUT'])
@jwt_required()
def update_recipe(recipe_id):
    """
    Atualiza uma receita existente
    ---
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: recipe_id
        type: integer
        required: true
      - in body:
        name: body
        schema:
          type: object
          properties:
            title:
              type: string
            ingredients:
              type: string
            time_minutes:
              type: integer
    responses:
        200:
          description: Receita atualizada com sucesso
        404:
          description: Receita nao encontrada
        401:
          description: token nao fornecido ou invalido
    """
    data = request.get_json()
    recipe = Recipe.query.get_or_404(recipe_id)
    if 'title' in data:
        recipe.title = data['title']
    if 'ingredients' in data:
        recipe.ingredients = data['ingredients']
    if 'time_minutes' in data:
        recipe.time_minutes = data['time_minutes']

    db.session.commit()
    return jsonify({"msg": "Recipe updated successfully"}), 200




#chamando app run
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Banco de dados criado com sucesso!")
        app.run(debug=True)

#print(app.config['SECRET_KEY'])
#print(app.config['SQLALCHEMY_DATABASE_URI'])
#print(app.config['SWAGGER'])
#print(app.config['CACHE_TYPE'])


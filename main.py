from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

app = FastAPI(
    title="My FastAPI Application",
    version="1.0.0",
    description="Sample FastAPI application",
)

# banco de dados em memória para para autenticacao
users = {
    "user1": "password1",
    "user2": "password2",
}

# lista de itens em memoria para simular um banco de dados
items = []  # Armazena como dict


class Item(BaseModel):
    name: str  # Nome do item
    description: str = None  # Descrição do item
    price: float = None  # Preço do item
    quantity: int = None  # Quantidade do item


# captura items
@app.get("/items")
async def get_items():
    return items


# inserir items
@app.post("/items")
async def create_item(item: Item):
    items.append(item.dict())
    return item


# rota de put para atualizar os itens
app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if 0 <= item_id < len(items):
        items[item_id] = item.dict()
        return items[item_id]
    raise HTTPException(status_code=404, detail="Item not found")


# rota do delete para excluir o item
app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if 0 <= item_id < len(items):
        removed_item = items.pop(item_id)
        return removed_item
    raise HTTPException(status_code=404, detail="Item not found")


security = HTTPBasic()

#Rota de autenticação básica
@app.get("/hello")
def verify_password(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    if username in users and users[username] == password:
        return username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        details="Invalid Credentials",
        headers={"WWW-Authenticate": "Basic"},
    )


@app.get("/")
async def home():
    return "FastAPI  build"

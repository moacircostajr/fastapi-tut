from typing import Union, List, Set, Dict
from fastapi import FastAPI, Query, Path, Body, Cookie, Header, status
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl, EmailStr


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    # Field... = informação extra para proposito de documentação.
    name: str = Field(example="Foo")  # obrigatorio
    description: Union[str, None] = Field(
        default=None, example="A very nice Item")  # facultativo
    price: float = Field(example=35.4)
    tax: Union[float, None] = Field(default=None, example=3.2)


class Image(BaseModel):
    url: HttpUrl
    name: str


class ItemBaseModel(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(
        gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None
    tags: List[str] = []
    unique_string_list: Set[str] = set()
    image: Union[Image, None] = None
    images: Union[List[Image], None] = None


class Offer(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    items: List[ItemBaseModel]


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]


app = FastAPI()


# @ app.get("/", status_code=HTTPStatus.OK.value)
@ app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello World"}


@ app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": '/' + file_path}


@ app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@ app.get("/items/")  # rotas fixas devem estar no inicio do script
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]  # retorno paginado


@ app.get("/manyItems/")
async def read_items(q: List[str] = Query(default=None)):
    results = {"items": q}
    return results


@ app.get("/items/")
async def read_items(q: list = Query(default=[])):  # não valida conteudo da lista
    query_items = {"q": q}
    return query_items


@ app.get("/items/")
async def read_items(q: Union[List[str], None] = Query(default="fixedquery", min_length=3, max_length=50, regex="^fixedquery$")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bau"}]}
    if q:
        results.update({"q": q})
    return results


@ app.get("/items/")
async def read_items(
    q: Union[str, None] = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@ app.get("/items/")
async def read_items(q: Union[str, None] = Query(default=None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@ app.get("/items/")
async def read_items(
    q: Union[str, None] = Query(
        default=None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@ app.get("/items/{item_id}")
# q e short são parâmetros de consulta opcionais -> http://127.0.0.1:8000/items/2?short=True
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@ app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    # o parametro de consulta short é obrigatório
    user_id: int, item_id: str, short: bool, q: Union[str, None] = None
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@ app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: Union[str, None] = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@ app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: Union[str, None] = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@ app.get("/items/{item_id}")
async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@ app.get("/items/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@ app.get("/items/{item_id}")
async def read_items(
    *, item_id: int = Path(title="The ID of the item to get", ge=1), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@ app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: int = Path(title="The ID of the item to get", gt=0, le=1000),
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@ app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: str,
    size: float = Query(gt=0, lt=10.5)
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/")
async def read_items(ads_id: Union[str, None] = Cookie(default=None)):
    return {"ads_id": ads_id}


@app.get("/items/")
async def read_items(user_agent: Union[str, None] = Header(default=None, convert_underscores=False)):
    return {"User-Agent": user_agent}


@app.get("/items/")
async def read_items(x_token: Union[List[str], None] = Header(default=None)):
    return {"X-Token values": x_token}


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    for image in images:
        print(image.url)
    return images


@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights


@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user


@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}


@ app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


@ app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: Union[str, None] = None,
    item: Union[Item, None] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


@ app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     },
#     "user": {
#         "username": "dave",
#         "full_name": "Dave Grohl"
#     }
# }


@ app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User, importance: int = Body()):
    results = {"item_id": item_id, "item": item,
               "user": user, "importance": importance}
    return results
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     },
#     "user": {
#         "username": "dave",
#         "full_name": "Dave Grohl"
#     },
#     "importance": 5
# }


@ app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(gt=0),
    q: Union[str, None] = None
):
    results = {"item_id": item_id, "item": item,
               "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results


@ app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     }
# }


@ app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: ItemBaseModel = Body(
        embed=True,
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    )
):
    results = {"item_id": item_id, "item": item}
    return results


@ app.put("/items/{item_id}")
async def update_item(item_id: int, item: ItemBaseModel):
    results = {"item_id": item_id, "item": item}
    return results
# {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2,
#     "tags": [
#         "rock",
#         "metal",
#         "bar"
#     ],
#     "unique_string_list": [
#         "rock",
#         "metal",
#         "bar"
#     ],
#     "images": [
#         {
#             "url": "http://example.com/baz.jpg",
#             "name": "The Foo live"
#         },
#         {
#             "url": "http://example.com/dave.jpg",
#             "name": "The Baz"
#         }
#     ]
# }


# TIPOS DE DADOS:
    #  https: // fastapi.tiangolo.com/pt/tutorial/extra-data-types/
    # int
    # float
    # str
    # bool
    # UUID
    # datetime.datetime
    # datetime.date
    # datetime.time
    # datetime.timedelta
    # frozenset
    # bytes
    # Decimal
    # https://pydantic-docs.helpmanual.io/usage/types/

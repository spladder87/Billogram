from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import string
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

discount = {}

def discountNameGenerator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()

    for item  in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return  listOfKeys

def generateDiscountCodes(amount):
    while amount > 0:
        code = discountNameGenerator()
        discount[code] = "Unassigned"
        amount -= 1

def getDiscountCode(discount, userId):
    for key in discount:
        if(discount[key] == "Unassigned"):
            discount[key] = userId
            return

@app.get("/brand/", response_class=HTMLResponse)
async def admin_brand(request: Request):
    return templates.TemplateResponse("brand.html", {"request": request, "discount": discount})

@app.post("/brand/")
async def brandGenerateCodes(request: Request, num: int = Form(...)):
    generateDiscountCodes(num)
    return templates.TemplateResponse("brand.html", {"request": request, "discount": discount})

@app.get("/users/{user_id}", response_class=HTMLResponse)
async def read_user(request: Request, user_id: int):
    user_discount = []
    user_discount = getKeysByValue(discount, user_id)
    return templates.TemplateResponse("user.html", {"request": request, "id": user_id, "discount": user_discount})

@app.post("/users/{user_id}")
async def getUserDiscount(request: Request, user_id: int):
    getDiscountCode(discount,user_id)
    user_discount = []
    user_discount = (getKeysByValue(discount, user_id))
    if (user_discount):
        return templates.TemplateResponse("user.html", {"request": request, "id": user_id, "discount": user_discount})
    else:
        errmsg = "No available discount codes"
        return templates.TemplateResponse("user.html", {"request": request, "id": user_id, "error": errmsg})
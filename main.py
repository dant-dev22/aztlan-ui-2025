from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from mangum import Mangum
import httpx

app = FastAPI()
handler = Mangum(app)

templates = Jinja2Templates(directory="templates")

API_URL = "https://vjfpbq4jbiz5uyarfu7z7ahlhi0xbhmi.lambda-url.us-east-1.on.aws/participants"

# 🔹 Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {"request": request}
    )


@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
            "form_data": {},
            "errors": {},
            "message": None,
            "aztlan_id": ""
        }
    )


@app.post("/register")
async def submit_form(
    name: str = Form(...),
    birth_date: str = Form(...),
    weight: float = Form(...),
    academy: str = Form(...),
    experience: int = Form(...),
    email: str = Form(...),
    belt: str | None = Form("white"),
    torneo: str = Form(...),
):
    payload = { "name": name, "birth_date": birth_date, "weight": weight,
                "academy": academy, "experience": experience, "email": email,
                "belt": belt, "torneo": torneo }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            aztlan_id = data.get("aztlan_id", "")
            return JSONResponse({"success": True, "aztlan_id": aztlan_id, 
                                 "message": f"Participant registered! ID: {aztlan_id}"})
    except httpx.HTTPStatusError as exc:
        return JSONResponse({"success": False, "errors": exc.response.json()})
    except Exception as e:
        return JSONResponse({"success": False, "errors": str(e)})


@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request
        }
    )

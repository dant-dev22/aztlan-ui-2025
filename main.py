from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from mangum import Mangum
import httpx

app = FastAPI()
handler = Mangum(app)

templates = Jinja2Templates(directory="templates")

API_URL = "https://vjfpbq4jbiz5uyarfu7z7ahlhi0xbhmi.lambda-url.us-east-1.on.aws/participants"


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
            "message": None
        }
    )


@app.post("/register", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    name: str = Form(...),
    birth_date: str = Form(...),
    weight: float = Form(...),
    academy: str = Form(...),
    experience: int = Form(...),
    email: str = Form(...),
    belt: str | None = Form("white"),
    torneo: str = Form(...),
):
    payload = {
        "name": name,
        "birth_date": birth_date,
        "weight": weight,
        "academy": academy,
        "experience": experience,
        "email": email,
        "belt": belt,
        "torneo": torneo
    }

    message = None
    errors = {}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            message = f"Participant registered! ID: {data.get('aztlan_id', 'N/A')}"

    except httpx.HTTPStatusError as exc:
        detail = exc.response.json().get("detail", {})
        if isinstance(detail, dict) and "field" in detail and "message" in detail:
            errors[detail["field"]] = detail["message"]
        else:
            errors["general"] = str(detail)

    except Exception as e:
        errors["general"] = str(e)

    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
            "message": message,
            "errors": errors,
            "form_data": payload
        }
    )

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request
        }
    )
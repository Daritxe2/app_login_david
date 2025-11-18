from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import mysql.connector

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Página de inicio con formulario
@app.get("/")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Procesar login
@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = mysql.connector.connect(
        host="db",
        user="testuser",
        password="testpass",
        database="testdb"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return templates.TemplateResponse("coches.html", {"request": request})
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Credenciales incorrectas"})

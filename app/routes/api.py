from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from jinja2 import Template
from app.services.mail import send_registration_email
import sqlite3

router = APIRouter()

@router.get("/products", response_class=HTMLResponse)
async def product_list():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    with open("app/templates/product_list.html") as f:
        template = Template(f.read())
    
    return template.render(products=[{'id': p[0], 'name': p[1], 'price': p[2]} for p in products])


# SQL Injection Vulnerable Route
@router.get("/product/detail", response_class=HTMLResponse)
async def product_detail(request: Request):
    product_id = request.query_params.get('id', '')
    
    # Vulnerable SQL query
    query = f"SELECT * FROM products WHERE id = {product_id}"
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query)  # SQL Injection vulnerability
    product = cursor.fetchone()
    conn.close()

    if product:
        return f"<h2>Product Found: {product[1]}</h2><p>Price: ${product[2]}</p>"
    else:
        return "<h2>No product found!</h2>"

# XSS Vulnerable Route
@router.get("/xss", response_class=HTMLResponse)
async def xss_form():
    with open("app/templates/xss.html") as f:
        return HTMLResponse(content=f.read())

@router.get("/xss_demo", response_class=HTMLResponse)
async def xss_demo(request: Request):
    user_input = request.query_params.get('input', '')
    
    # Reflecting user input into the page without sanitization (XSS vulnerability)
    return f"<h2>You entered: {user_input}</h2>"

# Registration Form Route
@router.get("/register", response_class=HTMLResponse)
async def register_form():
    with open("app/templates/register.html") as f:
        return HTMLResponse(content=f.read())

# Register and send email (HTML Injection Vulnerability)
@router.post("/register", response_class=HTMLResponse)
async def register(fullname: str = Form(...), email: str = Form(...)):
    # Load HTML template
    with open("app/templates/email_confirmation.html") as f:
        template_content = f.read()
    
    # Render template with user details (Vulnerable to HTML Injection)
    template = Template(template_content)
    rendered_html = template.render(fullname=fullname, email=email)
    
    # Send registration email
    await send_registration_email(fullname, email)
    
    return HTMLResponse(content=rendered_html)

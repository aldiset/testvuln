import sqlite3
from jinja2 import Template
from passlib.hash import bcrypt
from fastapi.responses import HTMLResponse
from starlette.status import HTTP_302_FOUND
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Form, Request, HTTPException


from app.services.mail import send_registration_email

router = APIRouter()

def get_db():
    conn = sqlite3.connect('database.db')
    return conn, conn.cursor()

@router.get("/", response_class=HTMLResponse)
async def home():
    with open("app/templates/index.html") as f:
        return HTMLResponse(content=f.read())


@router.get("/products", response_class=HTMLResponse)
async def product_list(request: Request):
    search_query = request.query_params.get('s', '')

    conn, cursor = get_db()

    if search_query:
        cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT * FROM products")
    
    products = cursor.fetchall()
    conn.close()

    with open("app/templates/products.html") as f:
        template = Template(f.read())

    return template.render(products=[{'id': p[0], 'name': p[1], 'price': p[2]} for p in products], search_query=search_query)


@router.get("/product", response_class=HTMLResponse)
async def product_detail(request: Request):
    product_id = request.query_params.get('id', '')

    # Vulnerable query: directly concatenate the user input (product_id) into the SQL query
    conn, cursor = get_db()
    query = f"SELECT * FROM products WHERE id = {product_id}"
    cursor.execute(query)  # Vulnerable to SQL Injection
    product = cursor.fetchone()
    conn.close()

    if not product:
        return HTMLResponse(content="<h2>Product not found</h2>", status_code=404)

    # Load the template for the product detail page
    with open("app/templates/product_detail.html") as f:
        template = Template(f.read())

    # Render the template with product details
    product_data = {'name': product[1], 'price': product[2], 'description': product[3]}
    return template.render(product=product_data)


@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return RedirectResponse(url="/login", status_code=HTTP_302_FOUND)

    # Fetch the user's details from the database based on the user_id stored in the session
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return HTMLResponse(content="<h2>User not found</h2>", status_code=404)

    # Load the template for the profile page
    with open("app/templates/profile.html") as f:
        template = Template(f.read())

    # Render the template with user details
    user_data = {'fullname': user[1], 'username': user[2], 'email': user[3]}
    print(user_data)
    return template.render(fullname=user_data["fullname"])

@router.get("/logout", response_class=RedirectResponse)
async def logout(request: Request):
    request.session.clear()  # Clear the session to log the user out
    return RedirectResponse(url="/login", status_code=HTTP_302_FOUND)

@router.get("/login", response_class=HTMLResponse)
async def login_form():
    # Render the login form (no error by default)
    with open("app/templates/login.html") as f:
        template = Template(f.read())
    return template.render(error_message=None)

@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    conn, cursor = get_db()

    # Unsafe query: directly concatenate user inputs into the SQL query (vulnerable to SQL Injection)
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    conn.close()

    print(user[4])
    # Skip password verification for demonstration, or keep it vulnerable by avoiding password hash verification.
    if not user or not bcrypt.verify(password, user[4]):
        # Render the login form again with an error message if login fails
        with open("app/templates/login.html") as f:
            template = Template(f.read())
        return template.render(error_message="Invalid username or password. Please try again.")
    
    # Store the user's ID in the session on successful login
    request.session['user_id'] = user[0]
    return RedirectResponse(url="/profile", status_code=HTTP_302_FOUND)

@router.get("/register", response_class=HTMLResponse)
async def register_form():
    with open("app/templates/register.html") as f:
        return HTMLResponse(content=f.read())

@router.post("/register", response_class=HTMLResponse)
async def register(fullname: str = Form(...), username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # Hash the password using bcrypt
    hashed_password = bcrypt.hash(password)
    
    conn, cursor = get_db()

    # Check for duplicate username or email
    cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
    existing_user = cursor.fetchone()
    
    if existing_user:
        conn.close()
        raise HTTPException(status_code=400, detail="Username or email already exists.")
    
    # Insert the user data into the database
    cursor.execute('''
        INSERT INTO users (fullname, username, email, password)
        VALUES (?, ?, ?, ?)
    ''', (fullname, username, email, hashed_password))
    conn.commit()
    conn.close()

    # Render the confirmation page after successful registration
    with open("app/templates/success.html") as f:
        template_content = f.read()
    
    template = Template(template_content)
    rendered_html = template.render(fullname=fullname, email=email)
    
    await send_registration_email(fullname, email)  # Simulated email sending
    return RedirectResponse(url="/login", status_code=HTTP_302_FOUND)

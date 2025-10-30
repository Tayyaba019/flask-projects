# 📝 Notes API  

This API allows users to register, log in, and manage their personal notes securely using JWT authentication.  

The API is live at:  
👉 **[https://tayyabaparveen.pythonanywhere.com/](https://tayyabaparveen.pythonanywhere.com/)**  

---

## ⚙️ Endpoints  

### 🧍 User Registration  

**POST** `/register`  

Registers a new user.

**Request Body (JSON):**
```json
{
  "username": "tayyaba",
  "password": "mypassword123"
}

Response Example:

{
  "message": "User registered successfully!"
}

🔐 User Login

POST /login

Authenticates a user and returns a JWT token.

Request Body (JSON):

{
  "email": "tayyaba@example.com",
  "password": "mypassword123"
}


Response Example:

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5..."
}

📋 Get All Notes

GET /notes

Returns all notes belonging to the authenticated user.
Requires authentication.

Headers:

Authorization: Bearer <YOUR TOKEN>


Response Example:

[
  {
    "id": 1,
    "title": "My First Note",
    "content": "This is my first note",
    "date_created": "2025-10-27T12:00:00"
  },
  {
    "id": 2,
    "title": "Flask API Plan",
    "content": "Complete Notes API by Monday",
    "date_created": "2025-10-27T14:30:00"
  }
]

➕ Create a Note

POST /notes

Creates a new note for the logged-in user.
Requires authentication.

Headers:

Authorization: Bearer <YOUR TOKEN>


Request Body (JSON):

{
  "title": "New Note",
  "content": "Learning Flask JWT Authentication"
}


Response Example:

{
  "message": "Note created successfully!"
}

✏️ Update a Note

PUT /notes/<id>

Updates an existing note by ID.
Requires authentication.

Headers:

Authorization: Bearer <YOUR TOKEN>


Request Body (JSON):

{
  "title": "Updated Note Title",
  "content": "Updated note content"
}


Response Example:

{
  "message": "Note updated successfully!"
}

❌ Delete a Note

DELETE /notes/<id>

Deletes a note by its ID.
Requires authentication.

Headers:

Authorization: Bearer <YOUR TOKEN>


Response Example:

{
  "message": "Note deleted successfully!"
}

🔑 API Authentication

All /notes routes require a valid JWT token.
You must first log in via /login to get your token.

Include the token in every request header as:

Authorization: Bearer <YOUR TOKEN>

⚙️ Local Setup

Follow these steps to run the project locally on your computer:

1️⃣ Clone the Repository
git clone https://github.com/Tayyaba019/flask-notes-api.git
cd flask-notes-api

2️⃣ Create a Virtual Environment
python -m venv venv

3️⃣ Activate the Environment

Windows:

venv\Scripts\activate


macOS/Linux:

source venv/bin/activate

4️⃣ Install Dependencies
pip install -r requirements.txt

5️⃣ Set Environment Variables

Create a .env file in your project folder and add:

SECRET_KEY=your_flask_secret_key
JWT_SECRET_KEY=your_jwt_secret_key

6️⃣ Run the Application
python run.py


The app will be available at http://127.0.0.1:5000/

👩‍💻 Author

Tayyaba Parveen
📍 Live Demo: tayyabaparveen.pythonanywhere.com

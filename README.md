# Resume-web-page
Webpage made in Python and Angular for create and download a personal Resume

# 📌 Interactive Resume

This project is a **full-stack web application** that allows you to create and display an interactive resume.  
It is built with **Angular** for the frontend and **FastAPI (Python)** for the backend.

---

## 🚀 Features

- 📄 Interactive and dynamic resume builder  
- 🎨 Frontend built with **Angular 20** (TypeScript, SCSS)  
- ⚡ Backend powered by **FastAPI** and **Uvicorn**  
- 🔗 REST API for communication between frontend and backend  
- 🐍 Python virtual environment for dependencies  
- 📦 Easy setup with `npm` (frontend) and `pip` (backend)  

---

## 📂 Project structure



resume-interactivo/
├── backend/ # FastAPI backend
│ ├── main.py # Entry point for API
│ ├── requirements.txt
│ └── ...
├── frontend/ # Angular frontend
│ ├── src/
│ ├── package.json
│ └── ...
├── .venv/ # Python virtual environment (ignored in git)
├── README.md
└── .gitignore


---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/resume-interactivo.git
cd resume-interactivo

2. Backend (FastAPI)

Create a virtual environment:

python -m venv .venv


Activate the virtual environment:

Windows:

.venv\Scripts\activate


Linux/Mac:

source .venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Run the backend:

uvicorn main:app --reload


By default, the backend will run on http://127.0.0.1:8000

3. Frontend (Angular)

Install dependencies:

npm install


Run the Angular app in development mode:

npm start


By default, the frontend will run on http://localhost:4200

🛠️ Technologies Used

Frontend

Angular 20

TypeScript

SCSS

Backend

Python 3.10+

FastAPI

Uvicorn

Others

Node.js 20+

NPM

Virtual environments for Python

(Optional) Docker for containerization

📜 Environment Variables

Create a .env file in the root folder to manage sensitive configuration. Example:

DATABASE_URL=sqlite:///./database.db
SECRET_KEY=your_secret_key

🧪 Running Tests
Backend (pytest)
pytest

Frontend (Angular tests)
ng test

📦 Build
Frontend
ng build --prod

Backend

Backend does not require building; just deploy with Uvicorn or Docker.

🚀 Deployment

You can deploy both services using Docker or separately on platforms like Heroku, Vercel, or AWS.
A docker-compose.yml file can be added for running frontend and backend together.

🤝 Contributing

Fork the repo

Create your feature branch (git checkout -b feature/my-feature)

Commit changes (git commit -m "Add new feature")

Push to the branch (git push origin feature/my-feature)

Open a Pull Request

📄 License

This project is licensed under the MIT License.
You are free to use, modify, and distribute this software.


---

👉 Te lo dejé **completo y formal en inglés**: incluye instalación, estructura, tests, env vars y contribución.  
¿Querés que también te lo prepare en una **versión resumida estilo startup** (más corto, tipo landing) para que quede más “moderno” en GitHub?

You said:
necesito que me lo hagas para copiar y pegar en un .md o en un txt que luego convierta a md
ChatGPT said:

Genial 🙌, te lo dejo listo para copiar y pegar directo en un .md o .txt sin explicaciones extra.

# 📌 Interactive Resume

This project is a **full-stack web application** that allows you to create and display an interactive resume.  
It is built with **Angular** for the frontend and **FastAPI (Python)** for the backend.

---

## 🚀 Features

- 📄 Interactive and dynamic resume builder  
- 🎨 Frontend built with **Angular 20** (TypeScript, SCSS)  
- ⚡ Backend powered by **FastAPI** and **Uvicorn**  
- 🔗 REST API for communication between frontend and backend  
- 🐍 Python virtual environment for dependencies  
- 📦 Easy setup with `npm` (frontend) and `pip` (backend)  

---

## 📂 Project structure



resume-interactivo/
├── backend/ # FastAPI backend
│ ├── main.py # Entry point for API
│ ├── requirements.txt
│ └── ...
├── frontend/ # Angular frontend
│ ├── src/
│ ├── package.json
│ └── ...
├── .venv/ # Python virtual environment (ignored in git)
├── README.md
└── .gitignore


---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/resume-interactivo.git
cd resume-interactivo

2. Backend (FastAPI)

Create a virtual environment:

python -m venv .venv


Activate the virtual environment:

Windows:

.venv\Scripts\activate


Linux/Mac:

source .venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Run the backend:

uvicorn main:app --reload


Default URL: http://127.0.0.1:8000

3. Frontend (Angular)

Install dependencies:

npm install


Run the Angular app in development mode:

npm start


Default URL: http://localhost:4200

🛠️ Technologies Used

Frontend

Angular 20

TypeScript

SCSS

Backend

Python 3.10+

FastAPI

Uvicorn

Others

Node.js 20+

NPM

Virtual environments for Python

(Optional) Docker for containerization

📜 Environment Variables

Create a .env file in the root folder to manage sensitive configuration. Example:

DATABASE_URL=sqlite:///./database.db
SECRET_KEY=your_secret_key

🧪 Running Tests
Backend (pytest)
pytest

Frontend (Angular tests)
ng test

📦 Build
Frontend
ng build --prod

Backend

Backend does not require building; just deploy with Uvicorn or Docker.

🚀 Deployment

You can deploy both services using Docker or separately on platforms like Heroku, Vercel, or AWS.
A docker-compose.yml file can be added for running frontend and backend together.

🤝 Contributing

Fork the repo

Create your feature branch (git checkout -b feature/my-feature)

Commit changes (git commit -m "Add new feature")

Push to the branch (git push origin feature/my-feature)

Open a Pull Request

📄 License

This project is licensed under the MIT License.
You are free to use, modify, and distribute this software.


---

¿Querés que también te arme el **docker-compose.yml** para correr backend y frontend juntos con un solo comando (`docker-compose up`)?

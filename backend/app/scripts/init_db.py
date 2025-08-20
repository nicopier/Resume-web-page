from app.db.session import engine
from app.db.models import Base

#execute me in that way:
#cd "C:\Users\Nicolas y Sofia\OneDrive\Escritorio\resume-interactivo\backend
# ..\.\.venv\Scripts\activate.bat
# python -m app.scripts.init_db

def main():
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas creadas")

if __name__ == "__main__":
    main()
    
    
    

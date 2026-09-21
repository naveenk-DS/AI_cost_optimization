from .connection import engine, Base
# IMPORTANT: We MUST import our models here, otherwise SQLAlchemy's Base 
# will not know they exist and will not create the tables!
from .models import InferenceLog 

def init_db():
    print("Initializing Database Connection to Brother PC...")
    try:
        # Base.metadata.create_all() looks at all imported classes inheriting from Base
        # and issues SQL `CREATE TABLE IF NOT EXISTS` commands to PostgreSQL.
        Base.metadata.create_all(bind=engine)
        print("Success! Created 'inference_logs' table securely.")
    except Exception as e:
        print(f"Failed to reach database: {str(e)}")

if __name__ == "__main__":
    init_db()

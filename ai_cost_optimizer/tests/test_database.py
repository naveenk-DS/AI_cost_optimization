from src.ai_cost_optimizer.database.connection import SessionLocal, engine
from src.ai_cost_optimizer.database.models import InferenceLog
from src.ai_cost_optimizer.database.init_db import init_db

def test_database_flow():
    print("1. Connecting to PostgreSQL and Verifying...")
    try:
        # Pings the DB by attempting a fast connection over LAN
        with engine.connect() as conn:
            print("   -> Connection successfully verified over LAN!")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    print("\n2. Creating Table (IF NOT EXISTS)...")
    init_db()

    print("\n3. Inserting one test inference record...")
    # Open a dedicated database session instance
    db = SessionLocal()
    try:
        # Create an ORM Object purely in python memory
        new_log = InferenceLog(
            provider="local_test",
            model="unit-test-model",
            input_tokens=10,
            output_tokens=20,
            total_tokens=30,
            latency_ms=120.5,
            estimated_cost=0.00015
        )
        
        # Add to session and flush transaction to DB!
        db.add(new_log)
        db.commit()
        
        # Refresh syncs the Python object with Database-generated fields (like IDs or Timestamp defaults)
        db.refresh(new_log)
        print(f"   -> Inserted Successfully! Generated ID: {new_log.id}")
        
        print("\n4. Reading record back from database...")
        # Fire a robust SQL SELECT query using the exact ID we just generated
        saved_record = db.query(InferenceLog).filter(InferenceLog.id == new_log.id).first()
        
        print("\n5. Output of Database Record:")
        print(f"   ID: {saved_record.id}")
        print(f"   Timestamp: {saved_record.timestamp}") # Will show as UTC timezone!
        print(f"   Model: {saved_record.model}")
        print(f"   Cost: ${saved_record.estimated_cost}")
        print(f"   Status: {saved_record.status}")
        
    finally:
        # GUARANTEE closure so we don't bleed our 5-connection pool dry if the test fails
        db.close()
        print("\nTest completed cleanly.")

if __name__ == "__main__":
    test_database_flow()

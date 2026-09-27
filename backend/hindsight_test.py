import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_API_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

bank_id = os.getenv("HINDSIGHT_BANK_ID")

print("Connecting to Hindsight...")

# Store an incident in memory
client.retain(
    bank_id=bank_id,
    content="""
    Incident INC-1001:
    Payment API experienced database connection timeouts.
    Root cause was PostgreSQL connection pool exhaustion.
    The engineering team increased the database connection pool limit
    and restarted the affected services.
    This successfully restored the Payment API.
    """,
    context="production incident"
)

print("Memory retained successfully!")

# Search the memory
response = client.recall(
    bank_id=bank_id,
    query="How was the previous Payment API database connection timeout resolved?"
)

print("\n========== HINDSIGHT RECALL ==========\n")

if response.results:
    for result in response.results:
        print(result.text)
else:
    print("No memories found.")

print("\n=======================================\n")
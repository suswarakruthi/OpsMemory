import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_API_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

BANK_ID = os.getenv("HINDSIGHT_BANK_ID")

incidents = [
    {
        "id": "INC-2001",
        "title": "Payment API database connection pool exhaustion",
        "content": """
Incident INC-2001:
The Payment API started returning 500 errors during peak traffic.
Database connection requests were timing out because the PostgreSQL
connection pool was exhausted.

Root cause:
The connection pool limit was too low for the increased request volume.

Successful resolution:
The engineering team increased the PostgreSQL connection pool limit
and restarted the affected payment services.

Outcome:
Payment API traffic recovered and database connection timeouts stopped.

Lesson:
For Payment API database timeout incidents, check PostgreSQL connection
pool utilization and compare it with the configured pool limit.
"""
    },
    {
        "id": "INC-2002",
        "title": "Checkout service slow database queries",
        "content": """
Incident INC-2002:
The Checkout service experienced high latency and request timeouts.
Database CPU usage increased significantly during peak traffic.

Root cause:
A frequently executed checkout query performed a full table scan.

Successful resolution:
The engineering team identified the slow query, added an appropriate
database index, and verified the query execution plan.

Outcome:
Checkout query latency decreased and timeout rates returned to normal.

Lesson:
When checkout latency increases together with database CPU usage,
inspect slow queries and execution plans before scaling application servers.
"""
    },
    {
        "id": "INC-2003",
        "title": "Redis cache connection failures",
        "content": """
Incident INC-2003:
The Order service reported intermittent Redis connection timeouts.
Application logs showed repeated failures while establishing Redis
connections.

Root cause:
The Redis client connection timeout was too aggressive during a
temporary network latency spike.

Successful resolution:
The team increased the Redis connection timeout and restarted the
affected workers.

Outcome:
Redis connection failures stopped and order processing recovered.

Lesson:
For intermittent Redis connection failures, inspect network latency
and client timeout configuration before replacing the cache service.
"""
    },
    {
        "id": "INC-2004",
        "title": "Duplicate payment webhook events",
        "content": """
Incident INC-2004:
The payment processing service received duplicate webhook events for
the same transaction.

Root cause:
Webhook delivery could be retried by the payment provider, while the
application did not enforce idempotency for already processed events.

Successful resolution:
The engineering team introduced idempotency keys and stored processed
webhook event identifiers before applying payment state changes.

Outcome:
Repeated webhook deliveries no longer created duplicate payment actions.

Lesson:
Payment webhook handlers must be idempotent because external providers
may retry event delivery.
"""
    },
    {
        "id": "INC-2005",
        "title": "Deployment caused elevated API error rate",
        "content": """
Incident INC-2005:
A new backend deployment caused the API error rate to increase shortly
after release.

Root cause:
A configuration change introduced an invalid environment value used by
the application at startup.

Successful resolution:
The team compared the deployment configuration with the previous
working release, corrected the environment value, rolled back the
deployment, and then redeployed the corrected configuration.

Outcome:
API error rates returned to normal.

Lesson:
When errors begin immediately after deployment, compare configuration
changes with the last known-good release before investigating unrelated
infrastructure causes.
"""
    }
]

print(f"Seeding {len(incidents)} incidents into bank: {BANK_ID}")
print()

for incident in incidents:
    content = f"""
Production Incident: {incident["id"]}
Title: {incident["title"]}

{incident["content"]}
"""

    client.retain(
        bank_id=BANK_ID,
        content=content,
        context="historical production incident and successful resolution"
    )

    print(f"✓ Stored {incident['id']} - {incident['title']}")

print()
print("======================================")
print("DEMO MEMORY SEEDING COMPLETE")
print("======================================")
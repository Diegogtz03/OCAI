# Scraper OCI Docs --> Clean --> Format --> Store in Vector Database, shared with API (AI Service)

from pymilvus import connections, db
from dotenv import load_dotenv
import os

load_dotenv()
conn = connections.connect(host=os.getenv('VDB_HOST'), port=os.getenv('VDB_PORT'), db_name=os.getenv('VDB_NAME'), token=os.getenv('VDB_TOKEN'))
print(db.list_database())
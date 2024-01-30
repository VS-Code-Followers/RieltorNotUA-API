**RietorNotUA API**

**For connect to DB at localhost:**

```docker run --name postgresql -e POSTGRES_PASSWORD=PASSWORD -e POSTGRES_USER=USER-e POSTGRES_DB=DB_NAME -p 4308:4308 -d postgres:13.4-alpine```

**For start API**
````python main.py``
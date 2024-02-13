**RietorNotUA API**

**For connect to DB at localhost:**

```docker run --name postgresql -e POSTGRES_PASSWORD=password -e POSTGRES_USER=user -e POSTGRES_DB=db_name -p 5432:5432 -d postgres:13.4-alpine```

**For start API**
```python main.py```

**All env variables, like POSTGRES_PASSWORD, etc., you can use from example.env, BUT only for TEST!**
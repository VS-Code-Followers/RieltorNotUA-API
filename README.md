**RietorNotUA API**

**For connect to DB at localhost:**

```bash
docker run --name postgresql -e POSTGRES_PASSWORD=password -e POSTGRES_USER=user -e POSTGRES_DB=db_name -p 5432:5432 -d postgres:16.2-alpine
```

**Rename example.env to .env, or set ENV_FILE to example.env. You can do it with this command:**

```bash
export ENV_FILE=example.env
```

**For start API**

```bash
python main.py
```

**Also you can use ```gen_data.py``` for generating data in DataBase**
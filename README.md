**Steps, to run API at localhost**

**1. Clone this repository**

```bash
git clone https://github.com/CBoYXD/RietorNotUA-API.git
```

**2. Create ```venv``` (if not created yet)**

1) **Check, if you install ```virtualenv``` package. If not, install it with:**

```bash
python -m pip install virtualenv
```

2) **Create .venv folder**

```bash
python -m venv .venv
```


**3. Install project requirements**

1) With **pip**:

```bash
python -m pip install -r requirements.txt
```

2) With **poetry**:

```bash
python -m poetry install --no-root
```

**If after command above you see these error: ```No module named 'packaging'```, you need to install ```packaging``` package:**

```bash
python -m pip install packaging
```

**4) Rename example.env to .env, or set ENV_FILE to example.env. You can do it with this command:**

1) For **Linix**:
   
```bash
export ENV_FILE="example.env"
```

2) For **Windows**:

```powershell
$Env:ENV_FILE="example.env"
```

**5) Connect to DB at localhost with docker:**

```bash
docker run --name postgresql -e POSTGRES_PASSWORD=password -e POSTGRES_USER=user -e POSTGRES_DB=db_name -p 5432:5432 -d postgres:16.2-alpine
```

**6) Start API**

```bash
python main.py
```

**Also you can use ```gen_data.py``` for generating data in DataBase**
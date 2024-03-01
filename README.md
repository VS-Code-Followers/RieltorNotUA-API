**Steps, to run API at localhost**

**1. Clone this repository**

```bash
git clone https://github.com/CBoYXD/RietorNotUA-API.git
```

**2. Start project with [docker compose](https://docs.docker.com/compose/)**

1) [Install Docker](https://docs.docker.com/engine/install/) (if not already installed)

2) Start Docker

3) Run project
   
```bash
docker compose up
```

**3. Link to API**

You need to use [this link](http://127.0.0.1:8000), for access to API.


**Also you can use ```gen_data.py``` for generating data in DataBase**


**For run tests you needs:**

**1. Create venv**

```bash
python -m venv .venv
```

**2. Install Dependencies**

```bash
python -m poetry install --with test --no-root
```

**3. Set environment variables:**
1) Rename example.env file to .env
2) Put all need data in this file
3) Set path to file:

For **Windows**:

```powershell
$Env:ENV_FILE=".env"
```
   
For **Linux**:

```bash
export ENV_FILE=".env"
```

4) Run tests

```bash
python -m pytest .
```


**Good luck! 😁**
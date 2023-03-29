# wetherbot
![image](https://img.shields.io/pypi/v/poetry)

This bot is made to find out the weather in any period of time. This facilitates travel planning and minimizes the risk of being hit by bad weather.
___

## Getting started

- To start working with this project you need to install poetry

```
pip install poetry
poetry install
```


- Command for start 
```commandline
poetry run python main.py
```
## Initial Configuration

- In order to start you need to assign a unique token
```commandline
API_TOKEN = os.environ.get("Your TOKEN")

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
```


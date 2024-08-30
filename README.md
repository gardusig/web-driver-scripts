## download:

Remember to keep the same matching version **X**
- chromium version X
- chromedriver version X

## install:

```bash
$ python3 -m venv env/
$ source env/bin/activate
$ python3 -m pip install -r requirements.txt
```

## add this at ifood-gift-card/resources/sheet_data.json

```json
[
    {
        "link": "https://loja.smash.gifts/resgatar/0LLluqMIZcLdZwwUoZ6U",
        "password": "588285"
    },
    {
        "link": "https://loja.smash.gifts/resgatar/0ayzLvwmuhdHhsmbiADz",
        "password": "792534"
    }
]
```

## run this when finished:

```bash
$ deactivate
```

## run

```bash
$ python3 ifood_gift_card.py
```

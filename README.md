# Getting Started

In order to get the project running, make sure you have python installed and install the required packages:

```bash
$ pip install -r requirements.txt
```

Create a `.env` file from `.env.example` and add your `OPENAI_API_KEY`:

```
$ cp .env.example .env
```

Secondly, run the development server:

```bash
$ fastapi dev main.py
```

Happy hacking!

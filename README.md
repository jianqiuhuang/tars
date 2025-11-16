Reference https://medium.com/@hmbarotov/configuring-a-django-project-with-uv-548f15ccbc63
```
uv init --python 3.12  # init project
uv add Django  # add dependencies
uv add --group dev django-debug-toolbar  # add dev group dependencies
uv add --group prod gunicorn  # add prod group dependencies

uv sync  # reslve dependencies
uv run manager.py runserver

```
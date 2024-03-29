# FastApi template

================

## Description

My project description

## Template Stack

- [FastApi](https://fastapi.tiangolo.com/)

## Project Setup

- Install [Poetry](https://python-poetry.org/docs/)

- Set config for venv in local

  ```sh
  poetry config virtualenvs.in-project true
  poetry env use 3.11
  poetry shell                # Launch terminal with dependencies
  poetry install
  ```

- Apply migrations

  ```sh
  alembic upgrade head        # Ensure your database is running, and SQLALCHEMY_DATABASE_URI env variable is correctly setup
  ```

### Run locally

```sh
# WITHOUT DOCKER (Guess ADC from env)
uvicorn app.main:app --reload          # Or from VSCode launcher

# OR

# WITH DOCKER
Use the launch.json configuration to build and run the container

# (Running the launch is an equivalent to):
docker build -t <image>:<tag> -f Dockerfile .
docker run --name fastapi_template -p 8000:8000 -p 5678:5678 -v "$HOME/.config/gcloud/application_default_credentials.json":/gcp/creds.json --env GOOGLE_APPLICATION_CREDENTIALS=/gcp/creds.json --env GCLOUD_PROJECT=<gcp_project_id> <image>:<tag>


```

## Tests

```sh
poetry run pytest --cov=app --cov-report=term     # Uses SQLALCHEMY_DATABASE_URI in pyproject.toml
```

## Api docs

- [Swagger](http://localhost:8000/api/docs)

### Maintainers

Digital Lab

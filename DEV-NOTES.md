# Development Notes

## Database

```bash
docker run -d -p 5432:5432 --name postgresql -e POSTGRESQL_PASSWORD=password -e POSTGRESQL_DATABASE=jobs_for_teens bitnami/postgresql:latest
```


## Python Backend
```bash
pipenv shell
pipenv install
python app.py
```

## Frontend
```bash
cd frontend
npm install
npm run dev
```

## Caddy
```bash
cd caddy-server
caddy run
```

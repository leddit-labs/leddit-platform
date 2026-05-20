# Community Service

This service uses alembic to migrate database changes.

Replace USER and PASS in the below command to see the currently applied migration.

```bash
DATABASE_URL=postgresql://USER:PASS@localhost:5433/community uv run alembic current
```

To upgrade:

```bash
DATABASE_URL=postgresql://USER:PASS@localhost:5433/community uv run alembic upgrade head
```

To autogenerate a new migration file:

```bash
DATABASE_URL=postgresql://USER:PASS@localhost:5433/community uv run alembic revision --autogenerate -m "describe the change"
```

OBS: This service DB uses localhost port 5433

# Python Backend Boilerplate

## Development

Install pre-commit hooks:

```bash
make install-hooks
```

Setup env with [direnv](https://direnv.net/) using `.envrc.example`.

```bash

Run dev infrastructure:

```bash
make dev-up
```

Read [Migrations](#migrations) section in this file and apply migrations for development database:

```bash
make apply-migrations
```

Run tests for checking:

```bash
make run-tests
```

Run dev server:

```bash
make run-web
```

## Migrations

Install [Atlas](https://atlasgo.io/community-edition).

Read guide about SQLAlchemy [here](https://atlasgo.io/guides/orms/sqlalchemy).

In this template we use custom command to print models ddl for Atlas.

Generate migrations:

```bash
make migrations-generate
```

Check migrations status:

```bash
make migrations-status url=postgresql://user:password@localhost:5432/dbname
```

Apply migrations:

```bash
make apply-migrations url=postgresql://user:password@localhost:5432/dbname
```

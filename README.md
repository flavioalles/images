# images

A simple image uploading application.

### Stack

- Python: `3.12.4`
- [Poetry](https://python-poetry.org/): `1.8.2`
- PostgreSQL: `15.7`.
    - Minor version `7` is the latest available of major `15`.
    - PostgreSQL `15` major is the [latest fully tested for SQLAlchemy](https://docs.sqlalchemy.org/en/20/dialects/index.html#support-levels-for-included-dialects) ~`2.0`.
    - SQLAlchemy ~`2.0` is the ORM of choice for this project.

### Workflow

#### Requirements

- `git-lfs` is required - as it was used to track **JPEG** and **PNG** files - see [`.gitattributes`](.gitattributes).
- `make` is the interface to every (or, at least, most) tools used in the project - including the ones mentioned here.
    - Run `make help` if curious.
- `docker` & `docker-compose` are the packaging tools used in the workflow described here.

#### Run App

1. **Build backend app. image.**

```fish
$ TAG=<tag> make build-image
```

2. **Run services (i.e. backend app & DB).**

```fish
$ POSTGRES_PASSWORD=<password> TAG=<tag> make compose-up
```

3. **Explore and test.**

    Application will be running at host's port `8000` and the interactive API docs at [`/docs`](http://0.0.0.0:8000/docs) can be used to test it.

    Example images are available at [`examples/`](examples/).

4. **Stop (and remove) services.**

```fish
$ TAG=<tag> make compose-down
```

Make sure `TAG` is the same throughout every step.

### Future Work

- Implement serving of image file.
- Verify caching opportunities.
- Document dev. workflow.
- Automate creation of DB used by `pytest`.
- Automate dir. used by FastAPI app within `pytest`.
- Handle `warnings` - e.g. `pydantic` deprecations.
- Complete test cases to cover all scenarios.
- Setup CI - i.e. tests run, style and type checks.
- Fix type checker (i.e. `mypy` issue) - as seen on `make check-typing`.
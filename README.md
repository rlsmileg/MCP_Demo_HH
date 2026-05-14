# DatasauRus API

This project publishes `myDatasauRus.csv` as static JSON files that can be hosted on GitHub Pages.

GitHub Pages cannot run a live API server, but it can host static API endpoints. For this dataset, the endpoint pattern is:

```text
api/datasets/<dataset-name>.json
```

## Endpoints

```text
GET api/datasets.json
```

Lists available datasets.

```text
GET api/datasets/dino.json
```

Returns all `x` and `y` values for the `dino` dataset.

Available dataset names:

- `away`
- `bullseye`
- `dino`
- `star`

## Build

Run this whenever `myDatasauRus.csv` changes:

```bash
node scripts/build-api.mjs
```

Then commit the generated `api/` files and enable GitHub Pages for the repository.

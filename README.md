# Ngulia Website

Standalone Vue website for the Ngulia project, deployed to GitHub Pages.

## Repository layout

- `src/`: Vue app code.
- `scripts/preprocess.py`: builds website resources from the Zenodo dataset.
- `data/zenodo/`: complete local dataset copy, ignored by Git.
- `data/reference/birdlife_ranges/`: local source range assets, ignored by Git.
- `public/generated/`: committed dashboard, recovery, migration, and species-range resources.
- `public/species-photos/`, `public/history-archive/`, `public/partner-logos/`: website assets.

## Local development

```bash
npm install
uv sync
npm run dev
```

Set `VITE_MAPBOX_TOKEN` in `.env.local`. Python uses the project's Python 3.12 environment through `uv`; preprocessing itself uses only the standard library.

## Data source

Copy `.env.pipeline.example` to `.env.pipeline.local` and set the published Zenodo record ID:

```bash
NGULIA_ZENODO_RECORD_ID=<published-record-id>
```

Each preprocessing run resolves the latest published version and downloads the five CSVs and two documentation files into `data/zenodo/`. `source.json` records the resolved record ID, DOI, and URL. This folder gives you a complete copy of the Zenodo output; the full ringing dataset is not bundled into the public website.

No live Zenodo record is configured yet. Until publication, use the dataset repository's export:

```bash
npm run preprocess -- --source-dir /absolute/path/to/ngulia-dataset/exports/zenodo
```

Alternatively set `NGULIA_ZENODO_SOURCE_DIR` in `.env.pipeline.local`. A configured local source takes precedence; remove it when switching to Zenodo. There is no dependency on research workbooks or an R website exporter.

## Preprocessing

```bash
npm run preprocess
```

The Python pipeline reads:

- `taxonomy.csv`: names, classification, external identifiers, and project codes, joined by `avibase_id`.
- `daily_counts.csv`: annual totals, species totals, and seasonal phenology.
- `recoveries.csv`: recovery records and migration prototype densities.

It produces `dashboard.json`, `recoveries.json`, `migration-probabilities.json`, and `species-ranges-index.json` in `public/generated/`. The dashboard totals use daily counts; capture and daily-count totals in taxonomy describe separate sources and are not added together. Phenology uses the existing non-leap calendar; `effortYears` counts seasons with a positive record for that calendar day.

Recovery distances are great-circle distances from the published coordinates to Ngulia. Durations are calculated only when both dates have day precision; partial and interval dates retain their published precision. Recovery IDs are website identifiers based on row order in the downloaded file. Encounter types come from Zenodo; internal encounter methods and curation status are not present in the public dataset.

Species photos are matched by Avibase filename. Curated range GeoJSON files remain in `public/generated/species-ranges/`; their static metadata is kept in `scripts/species_ranges.json` and used to rebuild the species-range index. Publications and other static assets remain in this repository. Migration grids preserve the existing prototype's coarse land mask, smoothing parameters, and 500 km exclusion band; they are illustrations, not estimated migration distributions.

## Build and deployment

Build from the committed resources:

```bash
npm run build
```

Download or copy the dataset, regenerate resources, and build:

```bash
npm run build:full
```

For GitHub Pages, set the repository Actions variable `NGULIA_ZENODO_RECORD_ID` once the dataset is published. The deployment workflow will then regenerate resources from the latest version before building. Until that variable is set, deployment uses the committed resources.

`scripts/geocode_recovery_sites.py` is a separate manual maintenance tool for historical source evidence. Its research data path and Google Maps key are not needed for preprocessing or deployment.

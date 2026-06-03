# Ngulia Website

Standalone GitHub Pages repository for the core Ngulia website.

## What is in this repo

- `src/`: Vue app code
- `public/generated/`: committed processed website data
- `public/history-archive/`: curated historical images used by the site
- `public/partner-logos/`: partner assets used by the site
- `scripts/`: sync and helper scripts for the website repo

## What is not in this repo

Raw research inputs and the website data pipeline stay outside the repo. In particular, the large ringing spreadsheets, recovery workbook, BirdLife geodatabase, source photo archive, and the R export script are not part of this website repository.

## Environment split

Public website config goes in `.env.local`:

```bash
VITE_MAPBOX_TOKEN=...
```

Private pipeline config goes in `.env.pipeline.local`:

```bash
NGULIA_PROJECT_DATA_DIR=/absolute/path/to/Ngulia/data
GOOGLE_MAPS_API_KEY=...
```

Only the `VITE_` token is used by the frontend build. The Google key is only used by `scripts/geocode_recovery_sites.py`.
`NGULIA_PROJECT_DATA_DIR` should point to the research workspace `data/` directory so `scripts/preprocess.py` can copy the prepared website export from `derived/website/`.

## Local development

```bash
npm install
npm run dev
```

## Build

Build the website from the committed processed data:

```bash
npm run build
```

Regenerate processed data first, then build:

```bash
Rscript /absolute/path/to/Ngulia/scripts/07_build_curated_recoveries.R
Rscript /absolute/path/to/Ngulia/scripts/08_build_website_data.R
npm run preprocess
npm run build
```

Or in one step:

```bash
npm run build:full
```

## Preprocessing notes

The website no longer builds its data payload from raw research inputs.

The research workspace now prepares website data in two steps:

```bash
Rscript /absolute/path/to/Ngulia/scripts/07_build_curated_recoveries.R
Rscript /absolute/path/to/Ngulia/scripts/08_build_website_data.R
```

The website export step reads only:

- `data/curated/daily_counts.csv`
- `data/curated/recoveries.csv`
- taxonomy files in `data/staging/website/config/`, `data/staging/ring_events/config/`, and `data/reference/taxonomy/`

It writes the website-ready files to:

- `NGULIA_PROJECT_DATA_DIR/derived/website/`

Then this repo only copies that directory into:

- `public/generated/`

The sync script expects these paths to exist in `derived/website/`:

- `dashboard.json`
- `recoveries.json`
- `migration-probabilities.json`
- `species-ranges-index.json`

Static publications data and species photos now live in this repo and are not part of the generated data sync.

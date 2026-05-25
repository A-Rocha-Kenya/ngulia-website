# Ngulia Website

Standalone GitHub Pages repository for the core Ngulia website.

## What is in this repo

- `src/`: Vue app code
- `public/generated/`: committed processed website data
- `public/history-archive/`: curated historical images used by the site
- `public/partner-logos/`: partner assets used by the site
- `scripts/`: optional preprocessing scripts for regenerating `public/generated/`
- `data/`: small curated metadata used by the preprocessing scripts

## What is not in this repo

Raw research inputs stay outside the repo. In particular, the large ringing spreadsheets, recovery workbook, BirdLife geodatabase, and source photo archive are not part of this website repository.

## Environment split

Public website config goes in `.env.local`:

```bash
VITE_MAPBOX_TOKEN=...
```

Private pipeline config goes in `.env.pipeline.local`:

```bash
NGULIA_SOURCE_DATA_DIR=/absolute/path/to/raw/data
GOOGLE_MAPS_API_KEY=...
```

Only the `VITE_` token is used by the frontend build. The Google key is only used by `scripts/geocode_recovery_sites.py`.

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
npm run preprocess
npm run build
```

Or in one step:

```bash
npm run build:full
```

## Preprocessing notes

`scripts/preprocess.py` expects the external raw data directory to contain the same relative structure currently used in the research workspace, including:

- `1991-2023 Ngulia Ringing Data MASTER.xlsx`
- `Data - management and analysis/05 Recoveries/0709 Ngulia Recoveries and Controls.xls`
- `Ngulia_DJP/From DJP 2017/Selected birds/`
- `birdlife/BOTW.gdb`

The repo keeps only the curated metadata required by the pipeline:

- `data/ngulia_taxonomy_crosswalk.csv`
- `data/references.bib`

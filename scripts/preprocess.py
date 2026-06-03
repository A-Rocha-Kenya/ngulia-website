from __future__ import annotations

import os
import json
import shutil
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
PIPELINE_ENV_PATH = ROOT_DIR / ".env.pipeline.local"
OUTPUT_DIR = ROOT_DIR / "public" / "generated"
DYNAMIC_EXPORT_FILES = [
    "dashboard.json",
    "recoveries.json",
    "migration-probabilities.json",
]


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if not text or text.startswith("#") or "=" not in text:
            continue
        key, value = text.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key and key not in os.environ:
            os.environ[key] = value


def resolve_project_data_dir() -> Path:
    configured = os.getenv("NGULIA_PROJECT_DATA_DIR") or os.getenv("NGULIA_SOURCE_DATA_DIR")
    if configured:
        return Path(configured).expanduser()

    legacy_path = ROOT_DIR.parent / "data"
    if legacy_path.exists():
        return legacy_path

    raise RuntimeError(
        f"Missing NGULIA_PROJECT_DATA_DIR. Set it in {PIPELINE_ENV_PATH} to the research workspace data directory."
    )


def main() -> None:
    load_env_file(PIPELINE_ENV_PATH)

    source_dir = resolve_project_data_dir() / "derived" / "website"
    if not source_dir.exists():
        raise RuntimeError(
            f"Missing website export directory: {source_dir}. "
            "Run scripts/08_build_website_data.R in the research workspace first."
        )

    required_paths = [source_dir / name for name in DYNAMIC_EXPORT_FILES]
    missing_paths = [path for path in required_paths if not path.exists()]
    if missing_paths:
        missing_text = "\n".join(f"- {path}" for path in missing_paths)
        raise RuntimeError(
            "Website export directory is incomplete. Missing:\n"
            f"{missing_text}\n"
            "Re-run scripts/08_build_website_data.R in the research workspace."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for name in DYNAMIC_EXPORT_FILES:
        shutil.copy2(source_dir / name, OUTPUT_DIR / name)

    generated_ranges_index_path = source_dir / "species-ranges-index.json"
    static_ranges_index_path = OUTPUT_DIR / "species-ranges-index.json"
    static_ranges_dir = OUTPUT_DIR / "species-ranges"

    if generated_ranges_index_path.exists():
        generated_ranges_index = json.loads(generated_ranges_index_path.read_text(encoding="utf-8"))
        static_ranges_index = {}
        if static_ranges_index_path.exists():
            static_ranges_index = json.loads(static_ranges_index_path.read_text(encoding="utf-8"))

        static_species = static_ranges_index.get("species", {})
        merged_species = {}
        available_species = 0

        for species_id, species_meta in generated_ranges_index.get("species", {}).items():
            merged_meta = dict(species_meta)
            static_meta = static_species.get(species_id, {})
            static_path = static_meta.get("path")
            static_geojson_exists = (
                bool(static_path)
                and (OUTPUT_DIR / static_path).exists()
                and static_meta.get("available") is True
            )
            if static_geojson_exists:
                merged_meta.update(
                    {
                        "available": True,
                        "birdlifeScientificName": static_meta.get("birdlifeScientificName", ""),
                        "birdlifeCommonName": static_meta.get("birdlifeCommonName", ""),
                        "path": static_path,
                        "rangeTypes": static_meta.get("rangeTypes", []),
                        "featureCount": static_meta.get("featureCount", 0),
                    }
                )
                merged_meta.pop("missingReason", None)
                available_species += 1
            merged_species[species_id] = merged_meta

        generated_ranges_index["metadata"] = {
            **generated_ranges_index.get("metadata", {}),
            **{k: v for k, v in static_ranges_index.get("metadata", {}).items() if k != "source"},
            "source": static_ranges_index.get("metadata", {}).get(
                "source", generated_ranges_index.get("metadata", {}).get("source")
            ),
        }
        generated_ranges_index["summary"] = {
            "totalSpecies": len(merged_species),
            "matchedSpecies": available_species,
            "availableSpecies": available_species,
        }
        generated_ranges_index["species"] = merged_species
        static_ranges_index_path.write_text(
            json.dumps(generated_ranges_index, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    print(
        "Copied website data from "
        f"{source_dir} to {OUTPUT_DIR}"
    )


if __name__ == "__main__":
    main()

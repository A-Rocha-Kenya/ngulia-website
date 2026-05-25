# Website Agent Notes

This website is in active development. Optimize for clean iteration, not backward compatibility or premature optimization.

## Development priorities

- Keep routes simple and current.
- Remove obsolete routes instead of redirecting them unless explicitly requested.
- Remove temporary debug code, test content, placeholders, and scaffold text once a real feature is in place.
- Prefer explicit, readable code over abstraction-heavy solutions.
- Build the data pipeline first; optimize later.
- Keep frontend components easy to inspect and modify during development.

## Architecture bias

- The preprocessing pipeline is the source of truth for website-ready data.
- Keep data cleaning, joins, reshaping, and aggregation in preprocessing scripts rather than in Vue views.
- Prefer one clear implementation for each feature. If two pages or components duplicate the same behavior, consolidate instead of maintaining both.
- Do not add backward-compatibility redirects, migration shims, or legacy route support unless explicitly requested.

## Cleanup rule

When removing or replacing a feature:

- delete the old route or component
- remove stale links and copy
- remove related debug or temporary code
- leave the website in a clean, working state without legacy fallbacks

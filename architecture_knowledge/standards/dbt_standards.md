# dbt Modeling Standards

## Layering
- staging: source-aligned, minimal logic
- intermediate: joins, deduplication
- marts: business-ready entities

## Testing
- Every model must have:
  - not_null
  - unique (on primary key)
  - relationships where applicable

## Anti-patterns
- CASE logic in marts
- Hard-coded values
- Mixed grain joins

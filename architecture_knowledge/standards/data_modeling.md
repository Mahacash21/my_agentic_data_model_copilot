# Data Modeling Standards

## General Principles
- Separate **identity** from **events**
- Use **surrogate keys** internally
- Preserve **source identifiers**
- Prefer **Type 2 SCD** for attributes with historical meaning

## Grain Rules
- Every table must declare its grain explicitly
- Facts must not contain mutable descriptive attributes
- Dimensions must not contain aggregations

## Naming
- snake_case
- Singular entity names
- _sk suffix for surrogate keys

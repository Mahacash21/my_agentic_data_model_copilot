# Canonical Member Model

## Member (Golden Record)
Grain: One row per unique individual

Attributes:
- member_sk (surrogate key)
- mdm_id
- source_member_ids (array)
- first_name
- last_name
- dob
- gender_code
- status
- created_ts
- updated_ts

Source of Truth:
- MDM system

Notes:
- No enrollment or coverage data here


## Member Enrollment
Grain: One row per member per coverage period

Attributes:
- enrollment_sk
- member_sk
- product_sk
- group_sk
- coverage_start_date
- coverage_end_date
- enrollment_status


## Member Address (SCD2)
Grain: One row per member per address version

Attributes:
- address_sk
- member_sk
- address_line1
- city
- state
- zip
- effective_start_date
- effective_end_date
- is_current

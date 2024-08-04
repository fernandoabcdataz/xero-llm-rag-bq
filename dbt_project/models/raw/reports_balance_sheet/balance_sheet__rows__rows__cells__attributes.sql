{{ config(
    materialized="view",
    schema="raw"
) }}

SELECT
  report_date
  , report_id
  , report_name
  , report_type
  , updated_date_utc
  , rows_row_type
  , rows_title
  , rows_rows_row_type
  , rows_rows_cells_value
  , rows_rows_cells_attributes.Id AS rows_rows_cells_attributes_id
  , rows_rows_cells_attributes.Value AS rows_rows_cells_attributes_value
FROM
  {{ ref('balance_sheet__rows__rows__cells') }},
  UNNEST(rows_rows_cells_attributes) AS rows_rows_cells_attributes
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
  , rows_rows_cells.Value AS rows_rows_cells_value
  , rows_rows_cells.Attributes AS rows_rows_cells_attributes
FROM
  {{ ref('balance_sheet__rows__rows') }},
  UNNEST(rows_rows_cells) AS rows_rows_cells
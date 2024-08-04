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
  , rows_rows.Cells AS rows_rows_cells
  , rows_rows.RowType AS rows_rows_row_type
FROM
  {{ ref('balance_sheet__rows') }},
  UNNEST(rows_rows) AS rows_rows
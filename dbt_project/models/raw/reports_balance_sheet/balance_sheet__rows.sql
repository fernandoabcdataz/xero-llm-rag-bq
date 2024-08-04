{{ config(
    materialized="view",
    schema="raw"
) }}

SELECT
  ReportDate AS report_date
  , ReportID AS report_id
  , ReportName AS report_name
  , ReportType AS report_type
  , UpdatedDateUTC AS updated_date_utc
  , rows_.RowType AS rows_row_type
  , rows_.Title AS rows_title
  , rows_.Cells AS rows_cells
  , rows_.Rows AS rows_rows
FROM
  {{ source('landing', 'reports__balance_sheet')}},
  UNNEST(`Rows`) AS rows_
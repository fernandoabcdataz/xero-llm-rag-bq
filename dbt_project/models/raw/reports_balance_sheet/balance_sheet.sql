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
FROM
  {{ source('landing', 'reports__balance_sheet')}}

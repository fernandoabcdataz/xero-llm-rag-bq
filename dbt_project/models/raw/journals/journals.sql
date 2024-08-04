{{ config(
    materialized="view",
    schema="raw"
) }}

SELECT
  CreatedDateUTC AS created_date_utc
  , JournalDate AS journal_date
  , JournalID AS journal_id
  , JournalNumber AS journal_number
  , Reference AS reference
  , SourceID AS source_id
  , SourceType AS source_type
FROM 
  {{ source('landing', 'journals')}}

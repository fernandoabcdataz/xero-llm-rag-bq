{{ config(
    materialized="table",
    schema="raw"
) }}

SELECT
  JournalID AS journal_id
  , JournalLines.JournalLineID AS journal_line_id
  , TrackingCategories.Name AS tracking_categories__name
  , TrackingCategories.Options AS tracking_categories__options
  , TrackingCategories.TrackingCategoryID AS tracking_categories__tracking_category_id
  , TrackingCategories.TrackingOptionID AS tracking_categories__tracking_option_id
FROM 
  {{ source('landing', 'journals')}},
  UNNEST(JournalLines) AS JournalLines,
  UNNEST(JournalLines.TrackingCategories) AS TrackingCategories

{{ config(
    materialized="view",
    schema="raw"
) }}

SELECT DISTINCT
  JournalID AS journal_id
  , JournalLines.AccountCode AS account_code
  , JournalLines.AccountID AS account_id
  , JournalLines.AccountName AS account_name
  , JournalLines.AccountType AS account_type
  , JournalLines.Description AS description
  , JournalLines.GrossAmount AS gross_amount
  , JournalLines.JournalLineID AS journal_line_id
  , JournalLines.NetAmount AS net_amount
  , JournalLines.TaxAmount AS tax_amount
  , JournalLines.TaxName AS tax_name
  , JournalLines.TaxType AS tax_type
FROM 
  {{ source('landing', 'journals')}},
  UNNEST(JournalLines) AS JournalLines
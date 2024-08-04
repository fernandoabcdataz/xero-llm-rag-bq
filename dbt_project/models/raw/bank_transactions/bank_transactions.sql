{{ config(
    materialized="view",
    schema="raw"
) }}

SELECT
  BankTransactionID AS bank_transaction_id
  , CurrencyCode AS currency_code
  , Date AS date
  , DateString AS date_string
  , ExternalLinkProviderName AS external_link_provider_name
  , HasAttachments AS has_attachments
  , IsReconciled AS is_reconciled
  , LineAmountTypes AS line_amount_types
  , Reference AS reference
  , Status AS status
  , SubTotal AS sub_total
  , Total AS total
  , TotalTax AS total_tax
  , Type AS type
  , UpdatedDateUTC AS updated_date_utc
  , Url AS url
FROM {{ source('landing', 'bank_transactions')}}

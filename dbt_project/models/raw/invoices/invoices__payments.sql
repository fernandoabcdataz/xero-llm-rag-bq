{{ config(
    materialized="table",
    schema="raw"
) }}

SELECT
  InvoiceID AS invoice_id
  , Payments.Amount AS amount
  , Payments.CurrencyRate AS currency_rate
  , Payments.Date AS date
  , Payments.HasAccount AS has_account
  , Payments.HasValidationErrors AS has_validation_errors
  , Payments.PaymentID AS payment_id
  , Payments.Reference AS reference
FROM 
  {{ source('landing', 'invoices')}},
  UNNEST(Payments) AS Payments

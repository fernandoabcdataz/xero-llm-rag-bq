{{ config(
    materialized="table",
    schema="refined"
) }}

SELECT 
  InvoiceID
  , InvoiceNumber
  , Status
  , Date
  , DueDate
  , Total
  , SubTotal
  , TotalTax
  , AmountDue
  , AmountPaid
  , LineAmountTypes
  , Type
  , Reference
  , CurrencyCode
  , CurrencyRate
  , Url
FROM abcdataz.demo.invoices
{{ config(
    materialized="view",
    schema="raw"
) }}

SELECT
  ContactID AS contact_id
  , BatchPayments.BankAccountName AS bank_account_name
  , BatchPayments.BankAccountNumber AS bank_account_number
  , BatchPayments.Code AS code
  , BatchPayments.Details AS details
  , BatchPayments.Reference AS reference
FROM 
  {{ source('landing', 'contacts')}}
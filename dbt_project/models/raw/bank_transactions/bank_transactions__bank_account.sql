{{ config(
    materialized="table",
    schema="raw"
) }}

SELECT
  BankTransactionID AS bank_transaction_id
  , BankAccount.AccountID AS account_id
  , BankAccount.Code AS code
  , BankAccount.Name AS name
FROM 
  {{ source('landing', 'bank_transactions')}}

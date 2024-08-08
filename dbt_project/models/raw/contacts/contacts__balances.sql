{{ config(
    materialized="table",
    schema="raw"
) }}

SELECT
  ContactID AS contact_id
  , Balances.AccountsPayable.Outstanding AS accounts_payable__outstanding 
  , Balances.AccountsPayable.Overdue AS accounts_payable__overdue
  , Balances.AccountsReceivable.Outstanding AS accounts_receivable__outstanding 
  , Balances.AccountsReceivable.Overdue AS accounts_receivable__overdue
FROM 
  {{ source('landing', 'contacts')}}

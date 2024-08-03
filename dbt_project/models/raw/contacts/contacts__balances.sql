{{ config(
    materialized="view",
    schema="raw"
) }}

/*
SELECT
  ContactID
  , balance__accounts_payable.overdue AS AccountsPayableOverdue
  , balance__accounts_payable.outstanding AS AccountsPayableOutstanding
  , balance__accounts_receivable.overdue AS AccountsReceivableOverdue
  , balance__accounts_receivable.outstanding AS AccountsReceivableOutstanding
FROM 
  {{ ref('contacts') }},
  UNNEST(Balances.AccountsPayable) AS balance_accounts_payable,
  UNNEST(Balances.AccountsReceivable) AS balance_accounts_receivable
*/
SELECT
  ContactID,
  Balances.AccountsPayable.overdue AS AccountsPayableOverdue,
  Balances.AccountsPayable.outstanding AS AccountsPayableOutstanding,
  Balances.AccountsReceivable.overdue AS AccountsReceivableOverdue,
  Balances.AccountsReceivable.outstanding AS AccountsReceivableOutstanding
FROM 
  {{ ref('contacts') }}
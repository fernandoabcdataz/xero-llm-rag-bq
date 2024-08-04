{{ config(
    materialized="view",
    schema="raw"
) }}

SELECT
  BankTransactionID AS bank_transaction_id
  , Contact.Addresses AS addresses
  , Contact.ContactGroups AS contact_groups
  , Contact.ContactID AS contact_id
  , Contact.ContactPersons AS contact_persons
  , Contact.HasValidationErrors AS has_validation_errors
  , Contact.Name AS name
  , Contact.Phones AS phones
FROM {{ source('landing', 'bank_transactions')}}

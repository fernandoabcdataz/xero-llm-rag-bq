{{ config(
    materialized="view",
    schema="raw"
) }}

SELECT
  InvoiceID AS invoice_id
  , contact.Addresses AS addresses
  , contact.ContactGroups AS contact_groups
  , Contact.ContactID AS contact_id
  , Contact.ContactNumber AS contact_number
  , contact.ContactPersons AS contact_persons
  , Contact.HasValidationErrors AS has_validation_errors
  , Contact.Name AS name
  , contact.Phones AS phones
FROM 
  {{ source('landing', 'invoices')}}

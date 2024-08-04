{{ config(
    materialized="view",
    schema="raw"
) }}

SELECT
  AccountsPayableTaxType AS accounts_payable_tax_type
  , AccountsReceivableTaxType AS accounts_receivable_tax_type
  , BankAccountDetails AS bank_account_details
  , ContactID AS contact_id
  , ContactNumber AS contact_number
  , ContactStatus AS contact_status
  , DefaultCurrency AS default_currency
  , EmailAddress AS email_address
  , FirstName AS first_name
  , HasAttachments AS has_attachments
  , HasValidationErrors AS has_validation_errors
  , IsCustomer AS is_customer
  , IsSupplier AS is_supplier
  , LastName AS last_name
  , Name AS name
  , TaxNumber AS tax_number
  , UpdatedDateUTC AS updated_date_utc
FROM {{ source('landing', 'contacts')}}

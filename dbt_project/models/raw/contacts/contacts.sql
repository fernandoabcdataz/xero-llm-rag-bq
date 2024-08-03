{{ config(
    materialized="view",
    schema="raw"
) }}

SELECT
  ContactID
  , ContactStatus
  , Name
  , FirstName
  , LastName
  , EmailAddress
  , IsSupplier
  , IsCustomer
FROM {{ ref('contacts')}}

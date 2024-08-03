{{ config(
    materialized="table",
    schema="refined"
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

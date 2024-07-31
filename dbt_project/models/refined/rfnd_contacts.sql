{{ config(
    materialized="table",
    schema="refined"
) }}

SELECT
  ContactID
  , Name
  , FirstName
  , LastName
  , ContactStatus
  , EmailAddress
FROM {{ ref('contacts')}}
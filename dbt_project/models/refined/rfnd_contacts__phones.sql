{{ config(
    materialized="table",
    schema="refined"
) }}

SELECT
  ContactID
  , phone.PhoneCountryCode
  , phone.PhoneAreaCode
  , phone.PhoneNumber
  , phone.PhoneType
FROM 
  {{ ref('contacts')}},
  UNNEST(Phones) AS phone
WHERE
  phone.PhoneNumber IS NOT NULL
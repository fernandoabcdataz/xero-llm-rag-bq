{{ config(
    materialized="table",
    schema="raw"
) }}

SELECT
  ContactID AS contact_id
  , Phones.PhoneAreaCode AS phone_area_code
  , Phones.PhoneCountryCode AS phone_country_code
  , Phones.PhoneNumber AS phone_number
  , Phones.PhoneType AS phone_type
FROM 
  {{ source('landing', 'contacts')}},
  UNNEST(Phones) AS Phones

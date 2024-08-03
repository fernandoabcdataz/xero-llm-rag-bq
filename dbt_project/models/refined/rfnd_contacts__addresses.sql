{{ config(
    materialized="table",
    schema="refined"
) }}

SELECT
  ContactID
  , address.AddressType
  , address.AddressLine1
  , address.AddressLine2
  , address.AddressLine3
  , address.AddressLine4
  , address.PostalCode
  , address.City
  , address.Region
  , address.Country
  , address.AttentionTo
FROM 
  {{ ref('contacts')}},
  UNNEST(Addresses) AS address
WHERE 
  LENGTH(address.AddressLine1) > 0 OR
  LENGTH(address.AddressLine2) > 0 OR
  LENGTH(address.AddressLine3) > 0 OR
  LENGTH(address.AddressLine4) > 0
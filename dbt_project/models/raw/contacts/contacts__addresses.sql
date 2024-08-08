{{ config(
    materialized="table",
    schema="raw"
) }}

SELECT
  ContactID AS contact_id
  , Addresses.AddressLine1 AS address_line_1
  , Addresses.AddressLine2 AS address_line_2
  , Addresses.AddressLine3 AS address_line_3
  , Addresses.AddressLine4 AS address_line_4
  , Addresses.AddressType AS address_type
  , Addresses.AttentionTo AS attention_to
  , Addresses.City AS city
  , Addresses.Country AS country
  , Addresses.PostalCode AS postal_code
  , Addresses.Region AS region
FROM 
  {{ source('landing', 'contacts')}},
  UNNEST(Addresses) AS Addresses

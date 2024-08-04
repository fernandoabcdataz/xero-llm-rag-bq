{{ config(
    materialized="view",
    schema="raw"
) }}

SELECT
  ContactID AS contact_id
  , BrandingTheme.BrandingThemeID AS branding_theme_id
  , BrandingTheme.Name AS name
FROM 
  {{ source('landing', 'contacts')}}

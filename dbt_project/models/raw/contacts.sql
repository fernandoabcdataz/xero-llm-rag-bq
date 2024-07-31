{{ config(
    materialized="view",
    schema="raw"
) }}

SELECT
  *
FROM {{ source('landing', 'contacts')}}
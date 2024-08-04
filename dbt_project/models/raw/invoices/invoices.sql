{{ config(
    materialized="view",
    schema="raw"
) }}

SELECT
  AmountCredited AS amount_credited
  , AmountDue AS amount_due
  , AmountPaid AS amount_paid
  , BrandingThemeID AS branding_theme_id
  , CurrencyCode AS currency_code
  , CurrencyRate AS currency_rate
  , Date AS date
  , DateString AS date_string
  , DueDate AS due_date
  , DueDateString AS due_date_string
  , FullyPaidOnDate AS fully_paid_on_date
  , HasAttachments AS has_attachments
  , HasErrors AS has_errors
  , InvoiceID AS invoice_id
  , InvoiceNumber AS invoice_number
  , IsDiscounted AS is_discounted
  , LineAmountTypes AS line_amount_types
  , Reference AS reference
  , RepeatingInvoiceID AS repeating_invoice_id
  , SentToContact AS sent_to_contact
  , Status AS status
  , SubTotal AS sub_total
  , Total AS total
  , TotalTax AS total_tax
  , Type AS type
  , UpdatedDateUTC AS updated_date_utc
  , Url AS url
FROM {{ source('landing', 'invoices')}}

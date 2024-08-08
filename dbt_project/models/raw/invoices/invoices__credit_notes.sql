{{ config(
    materialized="table",
    schema="raw"
) }}

SELECT
  InvoiceID AS invoice_id
  , CreditNotes.AppliedAmount AS applied_amount
  , CreditNotes.CreditNoteID AS credit_note_id
  , CreditNotes.CreditNoteNumber AS credit_note_number
  , CreditNotes.Date AS date
  , CreditNotes.DateString AS date_string
  , CreditNotes.HasErrors AS has_errors
  , CreditNotes.ID AS id
  , CreditNotes.LineItems AS line_items
  , CreditNotes.Total AS total
FROM 
  {{ source('landing', 'invoices')}},
  UNNEST(CreditNotes) AS CreditNotes

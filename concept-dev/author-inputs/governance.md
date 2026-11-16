## Authors thoughts on governance

- each type of governance documents should each have a purpose
  - if content does not fit that purpose then we should engage with the developer on either adding to the purpose or creating a new document type for the purpose
  - Governance changelog or amendment notes or both.
    - QUESTION:  Do we need to have a changelog and a amendment notes files or can this all just be changelog which also contains the amendment notes.
    - governance documents may be amended.  However, the documents should be updated in place.  If we want to maintain amendment notes, then these should be in an `amendment` directory with an amendment file for each orginal file being updated.  For example adrs/ADR-001.md ammendment notes should not be documented in adrs/ADR-001.md.  Rather adrs/ADR-001.md should be updated in place.  Amendment notes should be maintained in amendment/adrs/ADR-001-amendment.md
    - Follow the same approach for specs and other governance documents (i.e. amendment/specs/SPEC-005-amendment.md)
    - What other types of records clutter up our prime governance documents?
\c metascience;

INSERT INTO authorships (researcher_uuid, publication_uuid, position)
  SELECT
    r.uuid,
    p.uuid,
    array_position(p.authors, r.overlapping_ranges[1])
  FROM publication p
    JOIN LATERAL (
      SELECT r.names AS overlapping_ranges, r.current_alias, r.uuid
      FROM   researchers as r
      WHERE  r.names && p.authors
    ) r ON overlapping_ranges IS NOT NULL;


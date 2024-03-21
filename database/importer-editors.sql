\c metascience;

INSERT INTO editors (researcher_uuid, publication_group_uuid, position)
  SELECT
    r.uuid,
    p.uuid,
    array_position(p.editors, r.overlapping_ranges[1])
  FROM publication_groups p
    JOIN LATERAL (
      SELECT r.names AS overlapping_ranges, r.current_alias, r.uuid
      FROM   researchers as r
      WHERE  r.names && p.editors
    ) r ON overlapping_ranges IS NOT NULL;


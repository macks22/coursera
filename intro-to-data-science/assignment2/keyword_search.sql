CREATE VIEW IF NOT EXISTS query AS
  SELECT * FROM frequency
  UNION
  SELECT 'q' as docid, 'washington' as term, 1 as count
  UNION
  SELECT 'q' as docid, 'taxes' as term, 1 as count
  UNION
  SELECT 'q' as docid, 'treasury' as term, 1 as count;

SELECT max(similarity)
  FROM (
    SELECT c1.docid, c2.docid, sum(c1.count * c2.count) AS similarity
      FROM query AS c1, Frequency AS c2
      WHERE c1.docid='q' AND c1.term = c2.term
      GROUP BY c1.docid, c2.docid
);

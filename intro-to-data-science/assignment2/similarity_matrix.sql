SELECT similarity
  FROM (
  SELECT f1.docid, f2.docid, sum(f1.count * f2.count) AS similarity
    FROM Frequency AS f1, Frequency as f2
  WHERE f1.docid < f2.docid AND f1.term=f2.term
    AND f1.docid="10080_txt_crude"
    AND f2.docid="17035_txt_earn"
  GROUP BY f1.docid, f2.docid);

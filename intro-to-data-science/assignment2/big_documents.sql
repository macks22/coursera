SELECT count(docid)
    FROM (
        SELECT docid, sum(count) AS num_terms
            FROM Frequency
            GROUP BY docid)
    WHERE num_terms > 300;

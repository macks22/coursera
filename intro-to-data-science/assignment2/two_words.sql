SELECT count(docid)
    FROM (
        SELECT docid, count(term) AS qualifier
        FROM Frequency
        WHERE term="transactions" OR term="world"
        GROUP BY docid)
    WHERE qualifier=2;

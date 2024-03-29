SELECT value
  FROM (
    SELECT A.row_num AS row_num, B.col_num AS col_num, sum(A.value * B.value) AS value
      FROM A, B
    WHERE A.col_num = B.row_num
    GROUP BY row_num, col_num)
  WHERE row_num=2 AND col_num=3;

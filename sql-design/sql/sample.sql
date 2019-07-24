SELECT
  *
FROM
  hoge AS a
INNER JOIN
  huga AS b
ON
  a.id = b.id
WHERE
  a.row_num = 1
ORDER BY
  a.id ASC
;

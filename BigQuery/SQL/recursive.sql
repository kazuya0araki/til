WITH RECURSIVE
raw_data AS (
  SELECT 1 AS id, null AS parent_id, 1 AS cnt, 10 AS value
  UNION ALL
  SELECT 2 AS id, 1 AS parent_id, -1 AS cnt, -10 AS value
  UNION ALL
  SELECT 3 AS id, 1 AS parent_id, 0 AS cnt, 5 AS value
  UNION ALL
  SELECT 4 AS id, null AS parent_id, 1 AS cnt, 10 AS value
  UNION ALL
  SELECT 5 AS id, 4 AS parent_id, -1 AS cnt, -10 AS value
),

offset_records AS (
  SELECT
    *,
    ROW_NUMBER() OVER(PARTITION BY parent_id ORDER BY id) AS sequential_number  -- 再帰処理のシーケンス番号
  FROM
    raw_data
  WHERE
    parent_id IS NOT NULL
),

recursive_process AS (
  SELECT
    *,
    cnt AS offset_cnt,
    value AS offset_value,
    1 AS sequential_number  -- 相殺レコードとシーケンス番号を合わせてJOIN可能とするため
  FROM
    raw_data
  UNION ALL
  (
    SELECT
      aaa.id,
      aaa.parent_id,
      aaa.cnt,
      aaa.value,
      aaa.offset_cnt + COALESCE(bbb.cnt, 0) AS offset_cnt,
      aaa.offset_value + COALESCE(bbb.value, 0) AS offset_value,
      aaa.sequential_number + 1 AS sequential_number  -- ここでイテレーション
    FROM
      recursive_process AS aaa
    LEFT JOIN
      offset_records AS bbb
    ON
      aaa.id = bbb.parent_id
      AND aaa.sequential_number = bbb.sequential_number
    LEFT JOIN
      offset_records AS ccc
    ON
      aaa.id = ccc.id
      AND aaa.sequential_number = ccc.sequential_number
    WHERE
      bbb.id IS NOT NULL  -- offset_recordsの結果のレコードが0にならないと再帰処理がループしてしまうので必要。
  )
),

final AS (
  SELECT
    *
  FROM
    recursive_process
  QUALIFY
    ROW_NUMBER() OVER(PARTITION BY id ORDER BY sequential_number DESC) = 1  -- 再帰CTEの仕様でUNION ALLで積み上がってしまうので、最新のシーケンス番号を取得することで積み上げを回避
)

SELECT
  aaa.id,
  aaa.parent_id,
  aaa.cnt,
  aaa.value,
  aaa.offset_cnt - COALESCE(bbb.cnt, 0) AS offset_cnt,
  aaa.offset_value - COALESCE(bbb.value, 0) AS offset_value
FROM
  final AS aaa
LEFT JOIN
  offset_records AS bbb  -- 相殺レコードをリセットする
ON
  aaa.id = bbb.id
ORDER BY aaa.id

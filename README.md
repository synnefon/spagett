# Spagett Query Language
Welcome to Spagett — the query language so noodly, it tangles up your data and serves it piping hot.

Spagett is a Lisp-inspired functional query language designed for combining, filtering, and aggregating structured data from multiple sources.

It runs on Python, eats .🍝 files for breakfast, and prints out clean tables.

## 🚀 Quick Start
1️⃣ Install Python

2️⃣ Clone the Spagett repo.

3️⃣ Write a .🍝 file (see examples below).

4️⃣ Run:
```bash
python spagett_it.py your_query_file.🍝
```

> note that Spagett is currently under development, so it only supports fake queries on a local file.

## 🛠️ Supported Operators (with Examples)

### 🧱 Core Expressions
| **Operator** | **Args**                        | **Example**                             | **What It Does**                          |
| ------------ | ------------------------------- | --------------------------------------- | ----------------------------------------- |
| `get`        | `table`                         | `(get users)`                           | Fetches the entire table.                 |
| `join`       | `condition`, `left`, `right`    | `(join (== user_id id) (get users) (get roleplays))` | Joins two tables on a condition.      |
| `map`        | `sub-expression`, `format`      | `(map (get users) (list user_id name))` | Applies a format to each record.         |
| `filter`      | `condition`, `sub-expression` | `(filter (> age 25) (get users))` | filters the sub expression by the condition, returning a subset of the sub expression's data|
| `ascending`   | `field(s)`, `sub-expression`        | `(ascending (list age name) (get users))`            | Sorts the result of the sub-expression in ascending order by given field(s). |
| `descending`  | `field(s)`, `sub-expression`        | `(descending (list age name) (get users))`           | Sorts the result of the sub-expression in descending order by given field(s). |
| `limit`       | `max-rows`, `sub-expression`        | `(limit 10 (get users))`                             | Limits the number of returned results from the sub-expression to max-rows.   |

### 🧱 Formatters
| **Operator** | **Args**                        | **Example**                             | **What It Does**                          |
| ------------ | ------------------------------- | --------------------------------------- | ----------------------------------------- |
| `list`       | `field1`, `field2`, ..., or `*` | `(list user_id completed)`  | Selects specific fields. Use `*` for all. |

### 📊 Aggregations
| **Operator** | **Args**                      | **Example**                                     | **What It Does**                 |
| ------------ | ----------------------------- | ----------------------------------------------- | -------------------------------- |
| `sum`        | `group-by`, `group-on`, `sub-expression` | `(sum (list email roleplay_id) duration_seconds (join ...))` | Sums group-on field for each distinct group-by field(s). |
| `max`        | `group-on`, `group-on`, `sub-expression` | `(max name duration_seconds (join ...))`        | Finds max value of group-on field for each distinct group-by field(s).       |
| `min`        | `group-by`, `group-on`, `sub-expression` | `(min name duration_seconds (join ...))`        | Finds min value of group-on field for each distinct group-by field(s).       |
| `avg`        | `group-by`, `group-on`, `sub-expression` | `(avg name duration_seconds (join ...))`        | Finds average value of group-on field for each distinct group-by field(s).       |
| `count`       | `group-by`, `sub-expression`        | `(count email (get users))`                          | Counts the number of records for each distinct value of the group-by field(s). |

### 🧮 Expressions
| **Operator**         | **Args**              | **Example**                            | **What It Does**             |
| -------------------- | --------------------- | -------------------------------------- | ---------------------------- |
| `==`, `!=`           | `left`, `right`       | `(== user_id id)`                      | Equality / inequality check. |
| `<`, `>`, `<=`, `>=` | `left`, `right`       | `(> age 25)`                           | Comparison operators.        |
| `+`, `-`, `*`, `/`   | `left`, `right`       | `(+ duration_seconds 10)`              | Basic math.                  |
| `and`, `or`          | `expr1`, `expr2`, ... | `(and (> age 25) (== true completed))` | Logical operators.           |


## 🍝 Example Queries

#### Get & Map
```lisp
(map (get users) (list id name))
```
→ Get users table, and pull out just the id and name fields.

#### Sum by Group
```lisp
(sum user_id duration_seconds (get roleplays))
```
→ Sum up duration_seconds grouped by user_id in the roleplays table.

#### Max Value
```lisp
(max user_id score (get scores))
```
→ Find the max score per user_id.

#### Join Tables
```lisp
(min
  (list name roleplay_id)
  performance
  (join
    (== oid roleplay_id)
    (join
      (== user_id id)
      (map
        (get users)
        (list name id)
      )
      (get roleplays)
    )
    (map
      (get ratings)
      (list performance roleplay_id)
    )
  )
)
```
→ get the min performance rating from users table joined with roleplays table, for each name and roleplay pair

## 🏗️ Contributing
Want to help shape the most noodly query language on Earth?
Open a PR, suggest a feature, or just yell into the void:

“Somebody toucha my Spagett!”

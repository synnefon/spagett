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

| **Operator**        | **Args**                                                                  | **Example**                                                                                         | **Explanation**                                                                                                                                                                                                                                     |
|---------------------|---------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `get`              | `source` [, `sub-expression`]                                             | `(get users)`                                                                                       | Gets the full `users` table; can optionally pass a sub-expression.                                                                                                                                                                                  |
| `list`             | `field1`, `field2`, ... or `*`                                            | `(list user_id completed)`                                                                          | Pulls only the `user_id` and `completed` fields from a record. `(list *)` would pull all fields.                                                                                                                                                   |
| `map`             | `sub-expression`                                                          | `(map (list user_id completed))`                                                                    | Maps each record in the list to just the `user_id` and `completed` fields.                                                                                                                                                                         |
| `join`             | `condition`, `left`, `right`                                              | `(join (== user_id id) (get users) (get roleplays))`                                                | Joins `users` and `roleplays` where `user_id` matches `id`.                                                                                                                                                                                       |
| `sum`              | `group_by_field`, `sum_field`, `sub-expression`                                   | `(sum name duration_seconds (join ...))`                                                            | Sums `duration_seconds` grouped by `name` across joined data.                                                                                                                                                                                      |
| `max`              | `group_by_field`, `max_field`, `sub-expression`                                   | `(max name duration_seconds (join ...))`                                                            | Finds the max `duration_seconds` per `name` across joined data.                                                                                                                                                                                    |
| `min`              | `group_by_field`, `min_field`, `sub-expression`                                   | `(min name duration_seconds (join ...))`                                                            | Finds the min `duration_seconds` per `name` across joined data.                                                                                                                                                                                    |
| `if`               | `condition`, `then_expr` [, `else_expr`]                                 | `(if (> age 25) (list *))`                                                                          | If `age` is over 25, return all fields.                                                                                                                                                                                                           |
|                   |                                                                           | `(if (< age 30) (list *) (list name id))`                                                           | If `age` is under 30, return all fields; else, just return `name` and `id`.                                                                                                                                                                       |
| `==`, `!=`         | `left`, `right`                                                          | `(== user_id id)`                                                                                   | Checks if `user_id` equals `id`.                                                                                                                                                                                                                  |
| `<`, `>`, `<=`, `>=` | `left`, `right`                                                          | `(> age 25)`                                                                                         | Checks if `age` is greater than 25.                                                                                                                                                                                                               |
| `+`, `-`, `*`, `/`, `//`, `**` | `left`, `right`                                                          | `(+ duration_seconds 10)`                                                                           | Adds 10 to `duration_seconds`.                                                                                                                                                                                                                    |
| `and`, `or`        | `expr1`, `expr2`, ...                                                    | `(and (> age 25) (== completed true) (< 4 id))`                                                     | Returns true if `age > 25`, `completed == true`, **and** `id < 4`.                                                                                                                                                                                |


## 🍝 Example Queries

#### Get & Map
```lisp
(get users (map (list id name)))
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
(max
  name
  duration_seconds
  (join
    (== user_id id)
    (get users
      (map
        (if
          (> age 25)
          (list *)
        )
      )
    )
    (get roleplays 
      (map 
        (list user_id completed duration_seconds)
      )
    )
  )
)
```
→ get the max duration_seconds from users table joined with roleplays table

## 🏗️ Contributing
Want to help shape the most noodly query language on Earth?
Open a PR, suggest a feature, or just yell into the void:

“Somebody toucha my Spagett!”

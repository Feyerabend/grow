;; Exercise F.2: two branches to one block, one carrying an i32, the
;; other an i64. Validation must refuse it.
(module
  (func (export "main") (result i32)
    (block (result i32)
      (br_if 0 (i32.const 1) (i32.const 0))   ;; carries an i32
      (drop)
      (br 0 (i64.const 2)))))                 ;; carries an i64

;; Exercise F.3: a test that catches the seventh breakage, an i32.add
;; that adds one more when its first operand is 0x12345678.
(module
  (func (export "add") (param i32 i32) (result i32)
    (i32.add (local.get 0) (local.get 1))))

(assert_return
  (invoke "add" (i32.const 0x12345678) (i32.const 0))
  (i32.const 0x12345678))

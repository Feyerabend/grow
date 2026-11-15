;; Exercise F.4: the five sign-extension instructions. Each takes the
;; low 8, 16 or 32 bits of its operand as a signed number.
(module
  (func (export "i32.extend8_s") (param i32) (result i32) (i32.extend8_s (local.get 0)))
  (func (export "i32.extend16_s") (param i32) (result i32) (i32.extend16_s (local.get 0)))
  (func (export "i64.extend8_s") (param i64) (result i64) (i64.extend8_s (local.get 0)))
  (func (export "i64.extend16_s") (param i64) (result i64) (i64.extend16_s (local.get 0)))
  (func (export "i64.extend32_s") (param i64) (result i64) (i64.extend32_s (local.get 0))))

(assert_return (invoke "i32.extend8_s" (i32.const 0x7f)) (i32.const 127))
(assert_return (invoke "i32.extend8_s" (i32.const 0x80)) (i32.const -128))
(assert_return (invoke "i32.extend8_s" (i32.const 0x12345680)) (i32.const -128))
(assert_return (invoke "i32.extend16_s" (i32.const 0x7fff)) (i32.const 32767))
(assert_return (invoke "i32.extend16_s" (i32.const 0x8000)) (i32.const -32768))
(assert_return (invoke "i32.extend16_s" (i32.const 0xffff1234)) (i32.const 0x1234))
(assert_return (invoke "i64.extend8_s" (i64.const 0xff)) (i64.const -1))
(assert_return (invoke "i64.extend8_s" (i64.const 0x0123456789abcd7f)) (i64.const 127))
(assert_return (invoke "i64.extend16_s" (i64.const 0x8000)) (i64.const -32768))
(assert_return (invoke "i64.extend32_s" (i64.const 0x7fffffff)) (i64.const 2147483647))
(assert_return (invoke "i64.extend32_s" (i64.const 0x80000000)) (i64.const -2147483648))
(assert_return (invoke "i64.extend32_s" (i64.const 0xffffffff00000001)) (i64.const 1))

;; The operand's type is checked: an i64 where i32.extend8_s needs an i32.
(assert_invalid
  (module (func (result i32) (i32.extend8_s (i64.const 0))))
  "type mismatch")

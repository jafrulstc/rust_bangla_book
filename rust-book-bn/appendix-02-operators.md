## Appendix B: Operators এবং Symbols

এই appendix-এ Rust-এর syntax-এর একটি glossary দেওয়া আছে, যার মধ্যে রয়েছে operator এবং অন্যান্য symbol—যেগুলো একা বা path, generic, trait bound, macro, attribute, comment, tuple এবং bracket-এর context-এ দেখা যায়।

### Operators

Table B-1-এ Rust-এর operator গুলো দেওয়া আছে—কোনো context-এ operator-টি কীভাবে দেখাবে তার একটি উদাহরণ, একটি সংক্ষিপ্ত ব্যাখ্যা, এবং সেই operator-টি overloadable কিনা। কোনো operator overloadable হলে, সেই operator overload করতে ব্যবহৃত relevant trait তালিকাভুক্ত করা হয়েছে।

<span class="caption">Table B-1: Operators</span>

| Operator                  | Example                                                 | Explanation                                                           | Overloadable?  |
| ------------------------- | ------------------------------------------------------- | --------------------------------------------------------------------- | -------------- |
| `!`                       | `ident!(...)`, `ident!{...}`, `ident![...]`             | Macro expansion                                                       |                |
| `!`                       | `!expr`                                                 | Bitwise বা logical complement                                         | `Not`          |
| `!=`                      | `expr != expr`                                          | Nonequality comparison                                                | `PartialEq`    |
| `%`                       | `expr % expr`                                           | Arithmetic remainder                                                  | `Rem`          |
| `%=`                      | `var %= expr`                                           | Arithmetic remainder ও assignment                                     | `RemAssign`    |
| `&`                       | `&expr`, `&mut expr`                                    | Borrow                                                                |                |
| `&`                       | `&type`, `&mut type`, `&'a type`, `&'a mut type`        | Borrowed pointer type                                                 |                |
| `&`                       | `expr & expr`                                           | Bitwise AND                                                           | `BitAnd`       |
| `&=`                      | `var &= expr`                                           | Bitwise AND ও assignment                                              | `BitAndAssign` |
| `&&`                      | `expr && expr`                                          | Short-circuiting logical AND                                          |                |
| `*`                       | `expr * expr`                                           | Arithmetic multiplication                                             | `Mul`          |
| `*=`                      | `var *= expr`                                           | Arithmetic multiplication ও assignment                                | `MulAssign`    |
| `*`                       | `*expr`                                                 | Dereference                                                           | `Deref`        |
| `*`                       | `*const type`, `*mut type`                              | Raw pointer                                                           |                |
| `+`                       | `trait + trait`, `'a + trait`                           | Compound type constraint                                              |                |
| `+`                       | `expr + expr`                                           | Arithmetic addition                                                   | `Add`          |
| `+=`                      | `var += expr`                                           | Arithmetic addition ও assignment                                      | `AddAssign`    |
| `,`                       | `expr, expr`                                            | Argument ও element separator                                          |                |
| `-`                       | `- expr`                                                | Arithmetic negation                                                   | `Neg`          |
| `-`                       | `expr - expr`                                           | Arithmetic subtraction                                                | `Sub`          |
| `-=`                      | `var -= expr`                                           | Arithmetic subtraction ও assignment                                   | `SubAssign`    |
| `->`                      | `fn(...) -> type`, <code>&vert;...&vert; -> type</code> | Function ও closure return type                                        |                |
| `.`                       | `expr.ident`                                            | Field access                                                          |                |
| `.`                       | `expr.ident(expr, ...)`                                 | Method call                                                           |                |
| `.`                       | `expr.0`, `expr.1`, ইত্যাদি                              | Tuple indexing                                                        |                |
| `..`                      | `..`, `expr..`, `..expr`, `expr..expr`                  | Right-exclusive range literal                                         | `PartialOrd`   |
| `..=`                     | `..=expr`, `expr..=expr`                                | Right-inclusive range literal                                         | `PartialOrd`   |
| `..`                      | `..expr`                                                | Struct literal update syntax                                          |                |
| `..`                      | `variant(x, ..)`, `struct_type { x, .. }`               | “And the rest” pattern binding                                        |                |
| `...`                     | `expr...expr`                                           | (Deprecated, `..=` ব্যবহার করো) Pattern-এ: inclusive range pattern    |                |
| `/`                       | `expr / expr`                                           | Arithmetic division                                                   | `Div`          |
| `/=`                      | `var /= expr`                                           | Arithmetic division ও assignment                                      | `DivAssign`    |
| `:`                       | `pat: type`, `ident: type`                              | Constraints                                                           |                |
| `:`                       | `ident: expr`                                           | Struct field initializer                                              |                |
| `:`                       | `'a: loop {...}`                                        | Loop label                                                            |                |
| `;`                       | `expr;`                                                 | Statement ও item terminator                                           |                |
| `;`                       | `[...; len]`                                            | Fixed-size array syntax-এর অংশ                                        |                |
| `<<`                      | `expr << expr`                                          | Left-shift                                                            | `Shl`          |
| `<<=`                     | `var <<= expr`                                          | Left-shift ও assignment                                               | `ShlAssign`    |
| `<`                       | `expr < expr`                                           | Less than comparison                                                  | `PartialOrd`   |
| `<=`                      | `expr <= expr`                                          | Less than or equal to comparison                                      | `PartialOrd`   |
| `=`                       | `var = expr`, `ident = type`                            | Assignment/equivalence                                                |                |
| `==`                      | `expr == expr`                                          | Equality comparison                                                   | `PartialEq`    |
| `=>`                      | `pat => expr`                                           | Match arm syntax-এর অংশ                                               |                |
| `>`                       | `expr > expr`                                           | Greater than comparison                                               | `PartialOrd`   |
| `>=`                      | `expr >= expr`                                          | Greater than or equal to comparison                                   | `PartialOrd`   |
| `>>`                      | `expr >> expr`                                          | Right-shift                                                           | `Shr`          |
| `>>=`                     | `var >>= expr`                                          | Right-shift ও assignment                                              | `ShrAssign`    |
| `@`                       | `ident @ pat`                                           | Pattern binding                                                       |                |
| `^`                       | `expr ^ expr`                                           | Bitwise exclusive OR                                                  | `BitXor`       |
| `^=`                      | `var ^= expr`                                           | Bitwise exclusive OR ও assignment                                     | `BitXorAssign` |
| <code>&vert;</code>       | <code>pat &vert; pat</code>                             | Pattern alternatives                                                  |                |
| <code>&vert;</code>       | <code>expr &vert; expr</code>                           | Bitwise OR                                                            | `BitOr`        |
| <code>&vert;=</code>      | <code>var &vert;= expr</code>                           | Bitwise OR ও assignment                                               | `BitOrAssign`  |
| <code>&vert;&vert;</code> | <code>expr &vert;&vert; expr</code>                     | Short-circuiting logical OR                                           |                |
| `?`                       | `expr?`                                                 | Error propagation                                                     |                |

### Non-operator Symbols

নিচের টেবিলগুলোতে এমন সব symbol রয়েছে যেগুলো operator হিসেবে কাজ করে না; অর্থাৎ এগুলো function বা method call-এর মতো আচরণ করে না।

Table B-2-তে এমন symbol দেখানো হয়েছে যেগুলো নিজে নিজেই আসে এবং বিভিন্ন জায়গায় valid।

<span class="caption">Table B-2: Stand-alone Syntax</span>

| Symbol                                                                 | Explanation                                                            |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `'ident`                                                               | Named lifetime বা loop label                                           |
| Digit-এর ঠিক পরে `u8`, `i32`, `f64`, `usize`, ইত্যাদি                  | নির্দিষ্ট type-এর numeric literal                                      |
| `"..."`                                                                | String literal                                                         |
| `r"..."`, `r#"..."#`, `r##"..."##`, ইত্যাদি                            | Raw string literal; escape character process করা হয় না               |
| `b"..."`                                                               | Byte string literal; string-এর পরিবর্তে byte-এর array তৈরি করে        |
| `br"..."`, `br#"..."#`, `br##"..."##`, ইত্যাদি                         | Raw byte string literal; raw ও byte string literal-এর সমন্বয়         |
| `'...'`                                                                | Character literal                                                      |
| `b'...'`                                                               | ASCII byte literal                                                     |
| <code>&vert;...&vert; expr</code>                                      | Closure                                                                |
| `!`                                                                    | Diverging function-এর জন্য সর্বদা-empty bottom type                    |
| `_`                                                                    | “Ignored” pattern binding; integer literal পড়তে সহজ করতেও ব্যবহৃত হয় |

Table B-3-তে এমন symbol দেখানো হয়েছে যেগুলো module hierarchy ধরে কোনো item-এ path হিসেবে ব্যবহৃত হয়।

<span class="caption">Table B-3: Path-Related Syntax</span>

| Symbol                                  | Explanation                                                                                                  |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------|
| `ident::ident`                          | Namespace path                                                                                               |
| `::path`                                | Crate root-এর সাপেক্ষে path (অর্থাৎ explicitly absolute path)                                              |
| `self::path`                            | বর্তমান module-এর সাপেক্ষে path (অর্থাৎ explicitly relative path)                                          |
| `super::path`                           | বর্তমান module-এর parent-এর সাপেক্ষে path                                                                   |
| `type::ident`, `<type as trait>::ident` | Associated constant, function ও type                                                                         |
| `<type>::...`                           | এমন type-এর associated item যা সরাসরি নাম দেওয়া যায় না (যেমন `<&T>::...`, `<[T]>::...`, ইত্যাদি)            |
| `trait::method(...)`                    | যে trait method-টি define করে তার নাম উল্লেখ করে method call disambiguate করা                                |
| `type::method(...)`                     | যে type-এর জন্য method define করা তার নাম উল্লেখ করে method call disambiguate করা                            |
| `<type as trait>::method(...)`          | Trait ও type-এর নাম উল্লেখ করে method call disambiguate করা                                                  |

Table B-4-তে দেখানো হয়েছে সেইসব symbol যা generic type parameter ব্যবহারের context-ে আসে।

<span class="caption">Table B-4: Generics</span>

| Symbol                         | Explanation                                                                                                                                         |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `path<...>`                    | কোনো type-এ generic type-এর parameter উল্লেখ করে (যেমন `Vec<u8>`)                                                                                  |
| `path::<...>`, `method::<...>` | expression-এ generic type, function বা method-এর parameter উল্লেখ করে; প্রায়ই _turbofish_ নামে পরিচিত (যেমন `"42".parse::<i32>()`)                  |
| `fn ident<...> ...`            | Generic function define করে                                                                                                                         |
| `struct ident<...> ...`        | Generic structure define করে                                                                                                                        |
| `enum ident<...> ...`          | Generic enumeration define করে                                                                                                                      |
| `impl<...> ...`                | Generic implementation define করে                                                                                                                   |
| `for<...> type`                | Higher ranked lifetime bound                                                                                                                        |
| `type<ident=type>`             | এমন একটি generic type যেখানে এক বা একাধিক associated type-এর নির্দিষ্ট assignment রয়েছে (যেমন `Iterator<Item=T>`)                                    |

Table B-5-তে দেখানো হয়েছে সেইসব symbol যা generic type parameter-কে trait bound দিয়ে constrain করার context-ে আসে।

<span class="caption">Table B-5: Trait Bound Constraints</span>

| Symbol                        | Explanation                                                                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `T: U`                        | Generic parameter `T` শুধুমাত্র `U` implement করে এমন type-এ constrain করা                                                                |
| `T: 'a`                       | Generic type `T`-কে অবশ্যই lifetime `'a`-এর চেয়ে বেশি সময় বাঁচতে হবে (অর্থাৎ type transitively `'a`-এর চেয়ে ছোট lifetime-এর কোনো reference ধারণ করবে না) |
| `T: 'static`                  | Generic type `T`-তে `'static` ছাড়া আর কোনো borrowed reference নেই                                                                         |
| `'b: 'a`                      | Generic lifetime `'b`-কে অবশ্যই lifetime `'a`-এর চেয়ে বেশি সময় বাঁচতে হবে                                                                 |
| `T: ?Sized`                   | Generic type parameter-কে dynamically sized type হতে দেওয়া হয়                                                                            |
| `'a + trait`, `trait + trait` | Compound type constraint                                                                                                                   |

Table B-6-তে দেখানো হয়েছে সেইসব symbol যা macro call বা define করার এবং কোনো item-এ attribute উল্লেখ করার context-ে আসে।

<span class="caption">Table B-6: Macros and Attributes</span>

| Symbol                                      | Explanation        |
| ------------------------------------------- | ------------------ |
| `#[meta]`                                   | Outer attribute    |
| `#![meta]`                                  | Inner attribute    |
| `$ident`                                    | Macro substitution |
| `$ident:kind`                               | Macro metavariable |
| `$(...)...`                                 | Macro repetition   |
| `ident!(...)`, `ident!{...}`, `ident![...]` | Macro invocation   |

Table B-7-তে দেখানো হয়েছে comment তৈরির symbol গুলো।

<span class="caption">Table B-7: Comments</span>

| Symbol     | Explanation             |
| ---------- | ----------------------- |
| `//`       | Line comment            |
| `//!`      | Inner line doc comment  |
| `///`      | Outer line doc comment  |
| `/*...*/`  | Block comment           |
| `/*!...*/` | Inner block doc comment |
| `/**...*/` | Outer block doc comment |

Table B-8-তে দেখানো হয়েছে যেসব context-এ parenthesis ব্যবহৃত হয়।

<span class="caption">Table B-8: Parentheses</span>

| Symbol                   | Explanation                                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------------- |
| `()`                     | Empty tuple (অর্থাৎ unit), literal ও type উভয়ই                                            |
| `(expr)`                 | Parenthesized expression                                                                    |
| `(expr,)`                | Single-element tuple expression                                                             |
| `(type,)`                | Single-element tuple type                                                                   |
| `(expr, ...)`            | Tuple expression                                                                            |
| `(type, ...)`            | Tuple type                                                                                  |
| `expr(expr, ...)`        | Function call expression; tuple `struct` ও tuple `enum` variant initialize করতেও ব্যবহৃত হয় |

Table B-9-তে দেখানো হয়েছে যেসব context-ে curly bracket ব্যবহৃত হয়।

<span class="caption">Table B-9: Curly Brackets</span>

| Context      | Explanation      |
| ------------ | ---------------- |
| `{...}`      | Block expression |
| `Type {...}` | Struct literal   |

Table B-10-তে দেখানো হয়েছে যেসব context-এ square bracket ব্যবহৃত হয়।

<span class="caption">Table B-10: Square Brackets</span>

| Context                                            | Explanation                                                                                                                   |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `[...]`                                            | Array literal                                                                                                                 |
| `[expr; len]`                                      | `expr`-এর `len` কপি বিশিষ্ট array literal                                                                                     |
| `[type; len]`                                      | `type`-এর `len` সংখ্যক instance বিশিষ্ট array type                                                                            |
| `expr[expr]`                                       | Collection indexing; overloadable (`Index`, `IndexMut`)                                                                       |
| `expr[..]`, `expr[a..]`, `expr[..b]`, `expr[a..b]` | Collection indexing যা collection slicing-এর মতো আচরণ করে, “index” হিসেবে `Range`, `RangeFrom`, `RangeTo`, বা `RangeFull` ব্যবহার করে |

## Refutability: একটি Pattern Match এ ব্যর্থ হতে পারে কি না

Pattern দুটি রূপে আসে: refutable এবং irrefutable। যে pattern গুলো pass করা যেকোনো possible value-এর সাথে match করবে সেগুলো হলো _irrefutable_। উদাহরণস্বরূপ, `let x = 5;` statement-এ `x` একটি irrefutable pattern, কারণ `x` যেকোনো কিছুর সাথে match করে এবং তাই match এ ব্যর্থ হতেই পারে না। যে pattern গুলো কোনো possible value-এর সাথে match এ ব্যর্থ হতে পারে সেগুলো হলো _refutable_। উদাহরণস্বরূপ, `if let Some(x) = a_value` expression-এ `Some(x)` একটি refutable pattern, কারণ `a_value` variable-এর value যদি `Some` না হয়ে `None` হয়, তাহলে `Some(x)` pattern match করবে না।

Function parameter, `let` statement, এবং `for` loop শুধু irrefutable pattern গ্রহণ করতে পারে, কারণ value গুলো match না করলে program মানে কিছুই করতে পারে না। `if let` এবং `while let` expression এবং `let...else` statement refutable ও irrefutable উভয় প্রকার pattern-ই গ্রহণ করে, কিন্তু compiler irrefutable pattern-এর ক্ষেত্রে warning দেয়, কারণ সংজ্ঞানুযায়ী এগুলো possible failure handle করার জন্যই তৈরি: একটি conditional-এর মূল কার্যকারিতা হলো success বা failure অনুযায়ী ভিন্নভাবে কাজ করা।

সাধারণভাবে, তোমাকে refutable ও irrefutable pattern-এর পার্থক্য নিয়ে চিন্তা করতে হবে না; তবে refutability নামের concept-টির সাথে তোমার পরিচিত থাকা প্রয়োজন, যাতে কোনো error message-এ তা দেখলে তুমি প্রতিক্রিয়া দেখাতে পারো। সেই ক্ষেত্রে code-এর intended behavior অনুযায়ী তোমাকে হয় pattern পরিবর্তন করতে হবে, নয়তো যে construct-এর সাথে pattern ব্যবহার করছ সেটি পরিবর্তন করতে হবে।

চলো একটি উদাহরণ দেখি—কী হয় যখন আমরা এমন জায়গায় যেখানে Rust-এর irrefutable pattern দরকার, সেখানে একটি refutable pattern ব্যবহার করার চেষ্টা করি, এবং এর উল্টোটাও। Listing 19-8-তে একটি `let` statement দেখানো হয়েছে, কিন্তু pattern হিসেবে আমরা `Some(x)`—একটি refutable pattern—নির্দিষ্ট করেছি। যেমনটা তুমি আশা করতে পারো, এই code compile হবে না।

<Listing number="19-8" caption="Attempting to use a refutable pattern with `let`">

```rust,ignore,does_not_compile
    let Some(x) = some_option_value;
```

</Listing>

`some_option_value` যদি একটি `None` value হত, তাহলে সেটি `Some(x)` pattern-এর সাথে match করতে ব্যর্থ হত, অর্থাৎ pattern-টি refutable। কিন্তু `let` statement শুধু একটি irrefutable pattern গ্রহণ করতে পারে, কারণ একটি `None` value নিয়ে code-এর valid কিছু করার উপায় নেই। Compile করার সময় Rust এই অভিযোগ করবে যে আমরা এমন জায়গায় refutable pattern ব্যবহার করার চেষ্টা করেছি যেখানে irrefutable pattern প্রয়োজন:

```console
$ cargo run
   Compiling patterns v0.1.0 (file:///projects/patterns)
error[E0005]: refutable pattern in local binding
 --> src/main.rs:3:9
  |
3 |     let Some(x) = some_option_value;
  |         ^^^^^^^ pattern `None` not covered
  |
  = note: `let` bindings require an "irrefutable pattern", like a `struct` or an `enum` with only one variant
  = note: for more information, visit https://doc.rust-lang.org/book/ch19-02-refutability.html
  = note: the matched value is of type `Option<i32>`
help: you might want to use `let...else` to handle the variant that isn't matched
  |
3 |     let Some(x) = some_option_value else { todo!() };
  |                                     ++++++++++++++++

For more information about this error, try `rustc --explain E0005`.
error: could not compile `patterns` (bin "patterns") due to 1 previous error
```

যেহেতু আমরা `Some(x)` pattern দিয়ে প্রতিটি valid value cover করতে পারিনি (এবং পারার উপায়ও নেই!), Rust যথার্থভাবে একটি compiler error produce করে।

যদি এমন জায়গায় যেখানে irrefutable pattern দরকার, সেখানে আমাদের কাছে refutable pattern থাকে, তাহলে আমরা pattern ব্যবহার করা code টি পরিবর্তন করে সেটি fix করতে পারি: `let` ব্যবহারের বদলে আমরা `let...else` ব্যবহার করতে পারি। তাহলে, pattern match না করলে curly bracket-এর ভেতরের code টি value টিকে handle করবে। Listing 19-9 দেখায় কীভাবে Listing 19-8-এর code টি fix করা যায়।

<Listing number="19-9" caption="Using `let...else` and a block with refutable patterns instead of `let`">

```rust
    let Some(x) = some_option_value else {
        return;
    };
```

</Listing>

আমরা code-টিকে একটি বিকল্প পথ দিয়েছি! এই code টি সম্পূর্ণ valid, যদিও এর মানে হলো আমরা warning ছাড়া irrefutable pattern ব্যবহার করতে পারব না। আমরা যদি `let...else`-কে এমন কোনো pattern দিয়ে ব্যবহার করি যেটি সব সময় match করবে—যেমন `x`—Listing 19-10-এ দেখানো হয়েছে, তাহলে compiler একটি warning দেবে।

<Listing number="19-10" caption="Attempting to use an irrefutable pattern with `let...else`">

```rust
    let x = 5 else {
        return;
    };
```

</Listing>

Rust অভিযোগ করে যে `let...else`-এর সাথে irrefutable pattern ব্যবহার করার কোনো মানে নেই, কারণ `else` block-এ কখনো পৌঁছানো যাবে না:

```console
$ cargo run
   Compiling patterns v0.1.0 (file:///projects/patterns)
warning: unreachable `else` clause
 --> src/main.rs:2:15
  |
2 |     let x = 5 else {
  |     --------- ^^^^
  |     |
  |     assigning to binding pattern will always succeed
  |
  = note: this pattern always matches, so the else clause is unreachable
  = note: `#[warn(irrefutable_let_patterns)]` on by default

warning: `patterns` (bin "patterns") generated 1 warning
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.39s
     Running `target/debug/patterns`
```

এই কারণে, match arm গুলোতে অবশ্যই refutable pattern ব্যবহার করতে হবে—শুধু শেষ arm ছাড়া, যেটির উচিত একটি irrefutable pattern দিয়ে বাকি সব value match করা। Rust আমাদের শুধু একটি arm বিশিষ্ট একটি `match`-এ irrefutable pattern ব্যবহার করতে দেয়, কিন্তু এই syntax টি বিশেষ কাজের নয় এবং একটি সরল `let` statement দিয়ে replace করা যেতে পারে।

এখন যেহেতু তুমি জানো pattern কোথায় ব্যবহার করতে হয় এবং refutable ও irrefutable pattern-এর মধ্যে পার্থক্য কী, চলো দেখি pattern তৈরি করতে আমরা কোন কোন syntax ব্যবহার করতে পারি।

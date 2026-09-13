## Variables এবং Mutability

[“Storing Values with Variables”][storing-values-with-variables]<!-- ignore -->
section-এ যেমন বলা হয়েছে, default হিসেবে variable গুলো immutable হয়। Rust যে safety ও easy concurrency দেয়, তার সুবিধা নিয়ে কোড লেখার জন্য এটি Rust-এর অনেক ধরনের ইঙ্গিতের মধ্যে একটি। তবে তোমার variable-গুলোকে mutable করার সুযোগও আছে। চলো দেখি Rust কেন immutability-কে গুরুত্ব দিতে উৎসাহিত করে এবং কখন তুমি সেটি এড়িয়ে যেতে চাইতে পারো।

যখন একটি variable immutable থাকে, তখন একবার কোনো value একটি নামের সাথে bind হয়ে গেলে সেই value আর পরিবর্তন করতে পারবে না। এটা দেখানোর জন্য `cargo new variables` ব্যবহার করে তোমার _projects_ directory-তে _variables_ নামে একটি নতুন project তৈরি করো।

তারপর নতুন _variables_ directory-তে _src/main.rs_ খুলে সেখানকার code নিচের code দিয়ে পরিবর্তন করো, যেটা এখনও compile হবে না:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
fn main() {
    let x = 5;
    println!("The value of x is: {x}");
    x = 6;
    println!("The value of x is: {x}");
}
```

`cargo run` দিয়ে program-টি save করে run করো। তোমার একটি immutability error সম্পর্কিত error message দেখতে পাওয়া উচিত, যেমন এই output-এ দেখানো হয়েছে:

```console
$ cargo run
   Compiling variables v0.1.0 (file:///projects/variables)
error[E0384]: cannot assign twice to immutable variable `x`
 --> src/main.rs:4:5
  |
2 |     let x = 5;
  |         - first assignment to `x`
3 |     println!("The value of x is: {x}");
4 |     x = 6;
  |     ^^^^^ cannot assign twice to immutable variable
  |
help: consider making this binding mutable
  |
2 |     let mut x = 5;
  |         +++

For more information about this error, try `rustc --explain E0384`.
error: could not compile `variables` (bin "variables") due to 1 previous error
```

এই উদাহরণটি দেখায় compiler কীভাবে তোমার program-এর error খুঁজে পেতে সাহায্য করে। Compiler error বিরক্তিকর হতে পারে, কিন্তু আসলে এগুলো শুধু এটাই বোঝায় যে তোমার program এখনও নিরাপদে সেটা করছে না যেটা তুমি করতে চাইছো; এগুলো এটা _বোঝায় না_ যে তুমি ভালো programmer নও! অভিজ্ঞ Rustacean-রাও compiler error পান।

তুমি `` cannot assign twice to immutable variable `x` `` error message টি পেয়েছ কারণ তুমি immutable `x` variable-কে দ্বিতীয় একটি value assign করার চেষ্টা করেছিলে।

যখন আমরা কোনো value কে immutable হিসেবে চিহ্নিত করা অবস্থায় পরিবর্তন করার চেষ্টা করি, তখন compile-time error পাওয়াটা জরুরি, কারণ এই পরিস্থিতিটি bug-এর জন্ম দিতে পারে। যদি আমাদের code-এর একাংশ এই অনুমানে কাজ করে যে কোনো value কখনো পরিবর্তিত হবে না, এবং code-এর অন্য অংশ সেই value পরিবর্তন করে দেয়, তাহলে সম্ভব হয় যে code-এর প্রথম অংশটি যেটা করার জন্য ডিজাইন করা হয়েছিল সেটা করবে না। এই ধরনের bug-এর কারণ পরে খুঁজে বের করা কঠিন হতে পারে, বিশেষ করে যদি দ্বিতীয় code টুকরোটি value পরিবর্তন করে শুধু _মাঝে মাঝে_। Rust compiler গ্যারান্টি দেয় যে যখন তুমি বলবে কোনো value পরিবর্তিত হবে না, তখন সেটা সত্যিই পরিবর্তিত হবে না, ফলে তোমাকে নিজে সেটা ট্র্যাক করে রাখতে হবে না। এতে তোমার code বোঝা সহজ হয়।

তবে mutability অনেক সময় খুব কাজের হতে পারে এবং code লেখা সহজ করে দিতে পারে। যদিও variable গুলো default হিসেবে immutable থাকে, তুমি [Chapter 2][storing-values-with-variables]<!-- ignore -->-তে করেছিলে তেমনভাবে variable-এর নামের আগে `mut` যোগ করে সেগুলোকে mutable করতে পারো। `mut` যোগ করা code-এর ভবিষ্যৎ পাঠকদের কাছে এও বুঝিয়ে দেয় যে code-এর অন্যান্য অংশ এই variable-এর value পরিবর্তন করবে।

উদাহরণস্বরূপ, _src/main.rs_-কে নিচের মতো পরিবর্তন করি:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let mut x = 5;
    println!("The value of x is: {x}");
    x = 6;
    println!("The value of x is: {x}");
}
```

এখন আমরা যখন program-টি run করব, তখন এটা পাব:

```console
$ cargo run
   Compiling variables v0.1.0 (file:///projects/variables)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.30s
     Running `target/debug/variables`
The value of x is: 5
The value of x is: 6
```

`mut` ব্যবহার করলে আমরা `x`-এর সাথে bind করা value `5` থেকে `6`-এ পরিবর্তন করতে পারি। সবশেষে, mutability ব্যবহার করবে কি না সেটা তোমার ওপর নির্ভর করে এবং সেই নির্দিষ্ট পরিস্থিতিতে কোনটা সবচেয়ে পরিষ্কার মনে হয় তার ওপর।

<!-- Old headings. Do not remove or links may break. -->
<a id="constants"></a>

### Declaring Constants

Immutable variable-গুলোর মতোই, _constant_-গুলো এমন value যেগুলো একটি নামের সাথে bind থাকে এবং পরিবর্তন করতে দেয় না, কিন্তু constant আর variable-এর মধ্যে কিছু পার্থক্য আছে।

প্রথমত, constant-এর সাথে তুমি `mut` ব্যবহার করতে পারবে না। Constant গুলো শুধু default হিসেবে immutable নয়—এরা সবসময় immutable। তুমি `let` keyword-এর বদলে `const` keyword ব্যবহার করে constant declare করো, এবং value-এর type _অবশ্যই_ annotate করতে হবে। আমরা type ও type annotation নিয়ে পরের section [“Data Types”][data-types]<!-- ignore -->-এ আলোচনা করব, তাই এখন বিস্তারিত নিয়ে চিন্তা করো না। শুধু এটুকু জেনে রাখো যে সবসময় type annotate করতে হবে।

Constant যেকোনো scope-এ declare করা যায়, যার মধ্যে global scope-ও আছে, যা code-এর অনেক অংশের জানা দরকার এমন value-গুলোর জন্য এদের কার্যকর করে তোলে।

শেষ পার্থক্য হলো constant-কে শুধুমাত্র constant expression-এ set করা যায়, runtime-এ হিসাব করা সম্ভব এমন কোনো value-এর result-এ নয়।

একটি constant declaration-এর উদাহরণ দেখো:

```rust
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```

Constant-টির নাম `THREE_HOURS_IN_SECONDS`, এবং এর value set করা হয়েছে 60 (এক মিনিটে সেকেন্ড সংখ্যা) কে 60 (এক ঘণ্টায় মিনিট সংখ্যা) দিয়ে এবং তার ফলকে 3 (এই program-এ আমরা যত ঘণ্টা গণনা করতে চাই) দিয়ে গুণ করার ফল হিসেবে। Constant-এর জন্য Rust-এর naming convention হলো সব অক্ষর uppercase এবং শব্দের মাঝে underscore ব্যবহার করা। Compile time-এ সীমিত কিছু operation evaluator দিয়ে হিসাব করতে পারে, যা আমাদের এই value-টিকে 10,800 লেখার বদলে এমনভাবে লিখতে দেয় যা বোঝা ও যাচাই করা সহজ। Constant declare করার সময় কোন কোন operation ব্যবহার করা যায় সে সম্পর্কে আরও তথ্যের জন্য [Rust Reference-এর constant evaluation section][const-eval] দেখো।

Constant-গুলো একটি program চলার সময়, যেই scope-এ declare করা হয়েছিল সেখানে পুরো সময় জন্য valid থাকে। এই বৈশিষ্ট্যের কারণে constant-গুলো application domain-এর সেইসব value-গুলোর জন্য কার্যকর যেগুলো program-এর একাধিক অংশ জানতে প্রয়োজন, যেমন কোনো game-এ যেকোনো খেলোয়াড় সর্বোচ্চ যত পয়েন্ট অর্জন করতে পারে, বা আলোর গতি।

পুরো program জুড়ে ব্যবহৃত hardcoded value-গুলোকে constant হিসেবে নাম দেওয়া সেই value-এর অর্থ code-এর ভবিষ্যৎ maintainer-দের কাছে পৌঁছে দিতে সাহায্য করে। এটাও সাহায্য করে যে ভবিষ্যতে সেই hardcoded value আপডেট করতে হলে code-এ শুধু এক জায়গাতেই পরিবর্তন আনতে হবে।

### Shadowing

[Chapter 2][comparing-the-guess-to-the-secret-number]<!-- ignore -->-এর guessing game tutorial-তে যেমন দেখেছ, তুমি একটি নতুন variable আগের একটি variable-এর একই নামে declare করতে পারো। Rustacean-রা বলেন যে প্রথম variable-টি দ্বিতীয়টি দ্বারা _shadowed_ হয়েছে, যার মানে হলো তুমি variable-টির নাম ব্যবহার করলে compiler দ্বিতীয় variable-টিকে দেখবে। কার্যত, দ্বিতীয় variable-টি প্রথমটিকে overshadow করে, variable-নামটির যাবতীয় ব্যবহার নিজের দিকে নিয়ে নেয়—যতক্ষণ না সে নিজে shadowed হয় অথবা scope শেষ হয়। আমরা একই variable-এর নাম ব্যবহার করে এবং `let` keyword পুনরায় ব্যবহার করে একটি variable-কে shadow করতে পারি, এভাবে:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let x = 5;

    let x = x + 1;

    {
        let x = x * 2;
        println!("The value of x in the inner scope is: {x}");
    }

    println!("The value of x is: {x}");
}
```

এই program প্রথমে `x`-কে `5` value-এর সাথে bind করে। তারপর, সে `let x =` পুনরায় ব্যবহার করে একটি নতুন variable `x` তৈরি করে, আগের value নিয়ে তাতে `1` যোগ করে যাতে `x`-এর value `6` হয়। তারপর, curly brackets দিয়ে তৈরি একটি inner scope-এর ভেতরে তৃতীয় `let` statement-টিও `x`-কে shadow করে এবং একটি নতুন variable তৈরি করে, আগের value-কে `2` দিয়ে গুণ করে যাতে `x`-এর value `12` হয়ে যায়। সেই scope শেষ হলে inner shadowing-ও শেষ হয় এবং `x` আবার `6` হয়ে যায়। এই program-টি run করলে নিচের output পাওয়া যাবে:

```console
$ cargo run
   Compiling variables v0.1.0 (file:///projects/variables)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.31s
     Running `target/debug/variables`
The value of x in the inner scope is: 12
The value of x is: 6
```

Shadowing আর variable-কে `mut` হিসেবে চিহ্নিত করা এক নয়, কারণ `let` keyword ব্যবহার না করে আমরা ভুলে এই variable-কে পুনরায় assign করার চেষ্টা করলে আমরা একটি compile-time error পাব। `let` ব্যবহার করে, আমরা একটি value-এর ওপর কিছু transformation করতে পারি কিন্তু সেই transformation শেষ হলে variable-টিকে immutable রাখতে পারি।

`mut` আর shadowing-এর আরেকটি পার্থক্য হলো, যেহেতু আমরা `let` keyword আবার ব্যবহার করলে কার্যত একটি নতুন variable তৈরি করছি, আমরা value-এর type পরিবর্তন করতে পারি কিন্তু একই নাম পুনরায় ব্যবহার করতে পারি। যেমন, ধরো আমাদের program একজন ব্যবহারকারীকে বলে কিছু text-এর মাঝে কতগুলো space তারা চায় সেটা space character input করে দেখাতে, এবং তারপর আমরা সেই input-কে একটি number হিসেবে store করতে চাই:

```rust
    let spaces = "   ";
    let spaces = spaces.len();
```

প্রথম `spaces` variable-টি string type-এর, আর দ্বিতীয় `spaces` variable-টি number type-এর। Shadowing এভাবে আমাদের `spaces_str` আর `spaces_num`-এর মতো আলাদা নাম ভাবার ঝামেলা থেকে রেহাই দেয়; এর বদলে আমরা সহজ `spaces` নামটি পুনরায় ব্যবহার করতে পারি। তবে আমরা যদি এর জন্য `mut` ব্যবহার করতে চেষ্টা করি, যেমন এখানে দেখানো হয়েছে, তাহলে আমরা একটি compile-time error পাব:

```rust,ignore,does_not_compile
    let mut spaces = "   ";
    spaces = spaces.len();
```

Error-এ বলা হয় আমরা কোনো variable-এর type mutate করতে পারি না:

```console
$ cargo run
   Compiling variables v0.1.0 (file:///projects/variables)
error[E0308]: mismatched types
 --> src/main.rs:3:14
  |
2 |     let mut spaces = "   ";
  |                      ----- expected due to this value
3 |     spaces = spaces.len();
  |              ^^^^^^^^^^^^ expected `&str`, found `usize`

For more information about this error, try `rustc --explain E0308`.
error: could not compile `variables` (bin "variables") due to 1 previous error
```

এখন আমরা variable গুলো কীভাবে কাজ করে তা দেখেছি, চলো দেখি সেগুলোর আরও কী কী data type হতে পারে।

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[data-types]: ch03-02-data-types.html#data-types
[storing-values-with-variables]: ch02-00-guessing-game-tutorial.html#storing-values-with-variables
[const-eval]: ../reference/const_eval.html

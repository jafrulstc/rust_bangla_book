## Functions

Function গুলো Rust code-এ সর্বত্র বিদ্যমান। তুমি ইতিমধ্যেই language-টির সবচেয়ে গুরুত্বপূর্ণ function-গুলোর একটি দেখেছ: `main` function, যা অনেক program-এর entry point। তুমি `fn` keyword-ও দেখেছ, যা তোমাকে নতুন function declare করতে দেয়।

Rust code function ও variable-এর নামের জন্য conventional style হিসেবে _snake case_ ব্যবহার করে, যেখানে সব অক্ষর lowercase এবং শব্দের মাঝে underscore থাকে। এখানে এমন একটি program দেওয়া হলো যাতে একটি example function definition আছে:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    println!("Hello, world!");

    another_function();
}

fn another_function() {
    println!("Another function.");
}
```

আমরা Rust-এ `fn` এবং তারপর একটি function নাম ও parentheses-এর একটি set লিখে একটি function define করি। Curly brackets compiler-কে বলে দেয় function body কোথায় শুরু আর কোথায় শেষ।

আমরা যেকোনো function-এর নাম এবং তারপর parentheses-এর একটি set লিখে আমরা define করা যেকোনো function call করতে পারি। যেহেতু `another_function` এই program-এ define করা আছে, এটিকে `main` function-এর ভেতর থেকে call করা যেতে পারে। মনে রাখবে আমরা source code-তে `another_function`-কে `main` function-এর _পরে_ define করেছি; আমরা চাইলে এটিকে আগেও define করতে পারতাম। Rust এটা নিয়ে চিন্তিত নয় যে তুমি কোথায় function define করছ, শুধু সেটি caller-এর দেখা পাওয়া একটি scope-এ defined থাকলেই হলো।

Function নিয়ে আরও বিস্তারিত জানতে চলো _functions_ নামে একটি নতুন binary project শুরু করি। `another_function` উদাহরণটি _src/main.rs_-এ রেখে এটি run করো। তোমার নিচের output দেখা উচিত:

```console
$ cargo run
   Compiling functions v0.1.0 (file:///projects/functions)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.28s
     Running `target/debug/functions`
Hello, world!
Another function.
```

line-গুলো সেই ক্রমানুসারে execute হয় যেভাবে সেগুলো `main` function-এ দেখা যায়। প্রথমে “Hello, world!” message print হয়, এবং তারপর `another_function` call হয় এবং তার message print হয়।

### Parameters

আমরা function-গুলোকে _parameter_ সহ define করতে পারি, যেগুলো হলো বিশেষ variable যা একটি function-এর signature-এর অংশ। যখন একটি function-এর parameter থাকে, তুমি সেই parameter-গুলোর জন্য নির্দিষ্ট value দিতে পারো। Technically, নির্দিষ্ট value-গুলোকে _argument_ বলা হয়, কিন্তু casual conversation-এ মানুষ _parameter_ এবং _argument_ শব্দ দুটো একে অপরের বদলে ব্যবহার করে—function-এর definition-এর variable-গুলো বোঝাতেও আবার function call করার সময় passed নির্দিষ্ট value গুলো বোঝাতেও।

এই version-এর `another_function`-এ আমরা একটি parameter যোগ করেছি:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    another_function(5);
}

fn another_function(x: i32) {
    println!("The value of x is: {x}");
}
```

এই program-টি run করে দেখো; তোমার নিচের output পাওয়া উচিত:

```console
$ cargo run
   Compiling functions v0.1.0 (file:///projects/functions)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 1.21s
     Running `target/debug/functions`
The value of x is: 5
```

`another_function`-এর declaration-এ `x` নামের একটি parameter আছে। `x`-এর type `i32` হিসেবে specify করা হয়েছে। আমরা যখন `another_function`-এ `5` pass করি, `println!` macro format string-এ `x` ধারণ করা curly brackets-এর জায়গায় `5` বসিয়ে দেয়।

Function signature-এ তোমার প্রতিটি parameter-এর type _অবশ্যই_ declare করতে হবে। এটি Rust design-এর একটি ইচ্ছাকৃত সিদ্ধান্ত: function definition-এ type annotation require করার অর্থ হলো compiler-কে প্রায় কখনোই code-এর অন্য কোথাও তোমার কোন type বোঝানোর জন্য সেগুলো ব্যবহার করতে হয় না। Compiler function কোন type expect করছে তা জানলে আরও সহায়ক error message দিতে পারে।

একাধিক parameter define করার সময়, parameter declaration-গুলো কমা দিয়ে আলাদা করো, এভাবে:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    print_labeled_measurement(5, 'h');
}

fn print_labeled_measurement(value: i32, unit_label: char) {
    println!("The measurement is: {value}{unit_label}");
}
```

এই উদাহরণটি `print_labeled_measurement` নামে একটি function তৈরি করে যার দুটি parameter আছে। প্রথম parameter-এর নাম `value` এবং এটি একটি `i32`। দ্বিতীয়টির নাম `unit_label` এবং এর type `char`। Function-টি তারপর `value` এবং `unit_label` দুটোই ধারণ করে text print করে।

চলো এই code টি run করে দেখি। তোমার _functions_ project-এর _src/main.rs_ file-এ বর্তমানে যে program আছে সেটি উপরের উদাহরণ দিয়ে পরিবর্তন করো এবং `cargo run` দিয়ে run করো:

```console
$ cargo run
   Compiling functions v0.1.0 (file:///projects/functions)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.31s
     Running `target/debug/functions`
The measurement is: 5h
```

যেহেতু আমরা function-টিকে `value`-এর জন্য `5` এবং `unit_label`-এর জন্য `'h'` value দিয়ে call করেছি, program-এর output সেই value-গুলো ধারণ করে।

### Statements এবং Expressions

Function body গুলো কিছু statement-এর একটি ধারা দিয়ে গঠিত, optional ভাবে শেষে একটি expression-এ শেষ হয়। এ পর্যন্ত আমরা যে function-গুলো দেখেছি সেগুলোর কোনো শেষের expression ছিল না, কিন্তু তুমি একটি statement-এর অংশ হিসেবে expression দেখেছ। যেহেতু Rust একটি expression-based language, এটি বোঝা একটি গুরুত্বপূর্ণ পার্থক্য। অন্যান্য language-এ একই রকম পার্থক্য নেই, তাই চলো দেখি statement আর expression কী এবং সেগুলোর পার্থক্য function-এর body-কে কীভাবে প্রভাবিত করে।

- _Statement_-গুলো হলো এমন instruction যা কিছু action সম্পন্ন করে এবং কোনো value return করে না।
- _Expression_-গুলো একটি result value-তে evaluate হয়।

কিছু উদাহরণ দেখি।

আমরা আসলে ইতিমধ্যেই statement এবং expression ব্যবহার করেছি। `let` keyword দিয়ে একটি variable তৈরি করে তাকে কোনো value assign করা একটি statement। Listing 3-1-তে, `let y = 6;` একটি statement।

<Listing number="3-1" file-name="src/main.rs" caption="A `main` function declaration containing one statement">

```rust
fn main() {
    let y = 6;
}
```

</Listing>

Function definition-গুলোও statement; পুরো উপরের উদাহরণটি নিজেই একটি statement। (যেমন আমরা শীঘ্রই দেখব, function call করা একটি statement নয়।)

Statement গুলো value return করে না। সুতরাং, তুমি একটি `let` statement-কে অন্য কোনো variable-এ assign করতে পারবে না, যেমন নিচের code চেষ্টা করে; তুমি একটি error পাবে:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
fn main() {
    let x = (let y = 6);
}
```

এই program-টি run করলে তুমি যে error পাবে সেটা দেখতে এরকম:

```console
$ cargo run
   Compiling functions v0.1.0 (file:///projects/functions)
error: expected expression, found `let` statement
 --> src/main.rs:2:14
  |
2 |     let x = (let y = 6);
  |              ^^^
  |
  = note: only supported directly in conditions of `if` and `while` expressions

warning: unnecessary parentheses around assigned value
 --> src/main.rs:2:13
  |
2 |     let x = (let y = 6);
  |             ^         ^
  |
  = note: `#[warn(unused_parens)]` (part of `#[warn(unused)]`) on by default
help: remove these parentheses
  |
2 -     let x = (let y = 6);
2 +     let x = let y = 6;
  |

warning: `functions` (bin "functions") generated 1 warning
error: could not compile `functions` (bin "functions") due to 1 previous error; 1 warning emitted
```

`let y = 6` statement টি কোনো value return করে না, তাই `x`-এর bind করার মতো কিছুই নেই। এটি C বা Ruby-র মতো অন্যান্য language-এ যা হয় তার থেকে আলাদা, যেখানে assignment তার value return করে। সেই সব language-এ তুমি `x = y = 6` লিখতে পারো এবং `x` এবং `y` দুটোরই value `6` হতে পারে; Rust-এ সেটা হয় না।

Expression গুলো একটি value-তে evaluate হয় এবং Rust-এ তুমি যে বাকি code লিখবে তার বেশিরভাগই এগুলো দিয়ে গঠিত। একটি গাণিতিক operation কল্পনা করো, যেমন `5 + 6`, যা একটি expression যা `11` value-তে evaluate হয়। Expression গুলো statement-এর অংশ হতে পারে: Listing 3-1-তে, `let y = 6;` statement-এর `6` টি একটি expression যা `6` value-তে evaluate হয়। কোনো function call করা একটি expression। কোনো macro call করা একটি expression। Curly brackets দিয়ে তৈরি একটি নতুন scope block একটি expression, যেমন:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let y = {
        let x = 3;
        x + 1
    };

    println!("The value of y is: {y}");
}
```

এই expression:

```rust,ignore
{
    let x = 3;
    x + 1
}
```

এমন একটি block যা এই ক্ষেত্রে `4`-এ evaluate হয়। সেই value-টি `let` statement-এর অংশ হিসেবে `y`-এর সাথে bind হয়। লক্ষ্য করো শেষে কোনো semicolon ছাড়া `x + 1` line-টি, যা তুমি এ পর্যন্ত দেখেছ এমন বেশিরভাগ line-এর মতো নয়। Expression গুলো শেষের semicolon ধারণ করে না। যদি তুমি একটি expression-এর শেষে semicolon যোগ করো, তুমি সেটিকে একটি statement-এ পরিণত করবে, এবং তখন সেটি কোনো value return করবে না। function return value এবং expression নিয়ে পরে যখন explore করবে তখন এটি মনে রাখবে।

### Functions with Return Values

Function গুলো তাদেরকে call করা code-এ value return করতে পারে। আমরা return value-গুলোর নাম দিই না, কিন্তু একটি arrow (`->`) এর পরে সেগুলোর type declare করতে হয়। Rust-এ, function-টির return value হলো function-এর body block-এর শেষ expression-এর value-এর সমার্থক। তুমি `return` keyword এবং একটি value specify করে function থেকে আগেই return করতে পারো, কিন্তু বেশিরভাগ function শেষ expression-টিকে implicitly return করে। এখানে এমন একটি function-এর উদাহরণ দেওয়া হলো যা একটি value return করে:

<span class="filename">Filename: src/main.rs</span>

```rust
fn five() -> i32 {
    5
}

fn main() {
    let x = five();

    println!("The value of x is: {x}");
}
```

`five` function-এ কোনো function call, macro, এমনকি `let` statement-ও নেই—শুধু একা `5` number-টি আছে। এটি Rust-এ সম্পূর্ণ একটি valid function। লক্ষ্য করো function-এর return type-ও specify করা আছে, `-> i32` হিসেবে। এই code টি run করে দেখো; output দেখতে এমন হওয়া উচিত:

```console
$ cargo run
   Compiling functions v0.1.0 (file:///projects/functions)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.30s
     Running `target/debug/functions`
The value of x is: 5
```

`five`-এর ভেতরের `5` টি হলো function-টির return value, এই জন্যই return type `i32`। চলো এটি আরও বিস্তারিত দেখি। দুটি গুরুত্বপূর্ণ জিনিস আছে: প্রথমত, `let x = five();` line-টি দেখায় যে আমরা একটি function-এর return value দিয়ে একটি variable initialize করছি। যেহেতু `five` function-টি `5` return করে, সেই line-টি নিচের line-এর সমান:

```rust
let x = 5;
```

দ্বিতীয়ত, `five` function-টির কোনো parameter নেই এবং এটি return value-এর type define করে, কিন্তু function-টির body হলো কোনো semicolon ছাড়া একা একটি `5`, কারণ এটি একটি expression যার value আমরা return করতে চাই।

চলো আরেকটি উদাহরণ দেখি:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let x = plus_one(5);

    println!("The value of x is: {x}");
}

fn plus_one(x: i32) -> i32 {
    x + 1
}
```

এই code টি run করলে `The value of x is: 6` print হবে। কিন্তু কী হবে যদি আমরা `x + 1` ধারণ করা line-টির শেষে একটি semicolon বসাই, সেটিকে একটি expression থেকে একটি statement-এ পরিণত করে?

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
fn main() {
    let x = plus_one(5);

    println!("The value of x is: {x}");
}

fn plus_one(x: i32) -> i32 {
    x + 1;
}
```

এই code compile করলে একটি error তৈরি হবে, নিচের মতো:

```console
$ cargo run
   Compiling functions v0.1.0 (file:///projects/functions)
error[E0308]: mismatched types
 --> src/main.rs:7:24
  |
7 | fn plus_one(x: i32) -> i32 {
  |    --------            ^^^ expected `i32`, found `()`
  |    |
  |    implicitly returns `()` as its body has no tail or `return` expression
8 |     x + 1;
  |          - help: remove this semicolon to return this value

For more information about this error, try `rustc --explain E0308`.
error: could not compile `functions` (bin "functions") due to 1 previous error
```

প্রধান error message-টি, `mismatched types`, এই code-এর মূল সমস্যাটি প্রকাশ করে। `plus_one` function-টির definition বলছে যে এটি একটি `i32` return করবে, কিন্তু statement গুলো কোনো value-তে evaluate হয় না, যা `()` unit type দ্বারা প্রকাশ করা হয়েছে। সুতরাং, কিছুই return হয় না, যা function definition-এর সাথে বিরোধ করে এবং একটি error-এ পরিণত হয়। এই output-এ Rust একটি message দেয় যা সম্ভবত এই সমস্যাটি সমাধানে সাহায্য করবে: এটি semicolon-টি remove করার পরামর্শ দেয়, যা error টি ঠিক করে দেবে।

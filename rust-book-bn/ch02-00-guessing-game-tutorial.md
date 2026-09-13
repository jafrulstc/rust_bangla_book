# একটি Guessing Game প্রোগ্রামিং

চলো, একটি hands-on project একসাথে করে Rust-এ ঝাঁপ দিই! এই chapter-টি তোমাকে কিছু সাধারণ Rust concept-এর সাথে পরিচয় করিয়ে দেবে, সেগুলো একটি বাস্তব প্রোগ্রামে কীভাবে ব্যবহার করতে হয় তা দেখিয়ে। তুমি `let`, `match`, method, associated function, external crate এবং আরও অনেক কিছু সম্পর্কে জানতে পারবে! পরবর্তী chapter-গুলোতে আমরা এই ধারণাগুলো আরও বিস্তারিত আলোচনা করব। এই chapter-এ তুমি শুধু মৌলিক বিষয়গুলো অনুশীলন করবে।

আমরা একটি ক্লাসিক শিক্ষানবিশ প্রোগ্রামিং সমস্যা implement করব: একটি guessing game। এটি যেভাবে কাজ করবে: প্রোগ্রামটি ১ থেকে ১০০-এর মধ্যে একটি random integer তৈরি করবে। তারপর এটি খেলোয়াড়কে একটি অনুমান লেখার জন্য prompt করবে। একটি অনুমান লেখার পর, প্রোগ্রামটি নির্দেশ করবে অনুমানটি খুব কম নাকি খুব বেশি। যদি অনুমানটি সঠিক হয়, তবে খেলাটি একটি অভিনন্দন বার্তা দেখাবে এবং বন্ধ হবে।

## একটি নতুন Project সেট আপ করা

নতুন project সেট আপ করতে, Chapter 1-এ তুমি যে _projects_ directory তৈরি করেছিলে সেখানে যাও এবং Cargo ব্যবহার করে একটি নতুন project বানাও, এভাবে:

```console
$ cargo new guessing_game
$ cd guessing_game
```

প্রথম command-টি, `cargo new`, project-এর নাম (`guessing_game`) কে প্রথম argument হিসেবে নেয়। দ্বিতীয় command-টি নতুন project-এর directory-তে পরিবর্তন করে।

তৈরি করা _Cargo.toml_ file-টি দেখো:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial
rm -rf no-listing-01-cargo-new
cargo new no-listing-01-cargo-new --name guessing_game
cd no-listing-01-cargo-new
cargo run > output.txt 2>&1
cd ../../..
-->

<span class="filename">Filename: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
version = "0.1.0"
edition = "2024"

[dependencies]
```

Chapter 1-এ যেমন দেখেছিলে, `cargo new` তোমার জন্য একটি “Hello, world!” প্রোগ্রাম তৈরি করে দেয়। _src/main.rs_ file-টি দেখে নাও:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    println!("Hello, world!");
}
```

এখন `cargo run` command ব্যবহার করে এই “Hello, world!” প্রোগ্রামটি compile করো এবং একই step-এ run করো:

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.08s
     Running `target/debug/guessing_game`
Hello, world!
```

যখন তোমাকে একটি project-এ দ্রুত iterate করতে হবে, তখন `run` command খুব কাজে লাগে — যেমন এই খেলায় আমরা করব, পরবর্তী iteration-এ যাওয়ার আগে প্রতিটি iteration দ্রুত test করে দেখব।

_src/main.rs_ file-টি আবার খোলো। তুমি সব কোড এই file-টিতেই লিখবে।

## একটি অনুমান প্রসেস করা

Guessing game প্রোগ্রামের প্রথম অংশটি user input চাইবে, সেই input প্রসেস করবে এবং যাচাই করবে যে input প্রত্যাশিত রূপে আছে কি না। শুরু করতে, আমরা খেলোয়াড়কে একটি অনুমান লেখার সুযোগ দেব। Listing 2-1-এর কোডটি _src/main.rs_-এ লেখো।

<Listing number="2-1" file-name="src/main.rs" caption="Code that gets a guess from the user and prints it">

```rust,ignore
use std::io;

fn main() {
    println!("Guess the number!");

    println!("Please input your guess.");

    let mut guess = String::new();

    io::stdin()
        .read_line(&mut guess)
        .expect("Failed to read line");

    println!("You guessed: {guess}");
}
```

</Listing>

এই কোডে অনেক তথ্য আছে, তাই চলো এটি লাইন বাই লাইন বুঝে নিই। User input নিতে এবং তারপর সেই input-কে output হিসেবে print করতে, আমাদের `io` input/output library-কে scope-এ আনতে হবে। `io` library-টি standard library থেকে আসে, যাকে `std` বলা হয়:

```rust,ignore
use std::io;
```

ডিফল্টভাবে, Rust-এর standard library-তে কিছু item define করা থাকে যেগুলো সে প্রতিটি প্রোগ্রামের scope-এ নিয়ে আসে। এই সেটটিকে _prelude_ বলা হয়, এবং এর সবকিছু তুমি [standard library documentation-এ][prelude] দেখতে পারো।

যদি তুমি যে type-টি ব্যবহার করতে চাও সেটি prelude-তে না থাকে, তবে তোমাকে সেই type-টিকে একটি `use` statement দিয়ে explicitly scope-এ আনতে হবে। `std::io` library ব্যবহার করলে তুমি অনেক useful feature পাবে, যার মধ্যে user input গ্রহণ করার ক্ষমতাও আছে।

Chapter 1-এ যেমন শিখেছিলে, `main` function-টি হল প্রোগ্রামের entry point:

```rust,ignore
fn main() {
```

`fn` syntax একটি নতুন function declare করে; parentheses, `()`, নির্দেশ করে কোনো parameter নেই; এবং curly bracket, `{`, function-এর body শুরু করে।

Chapter 1-এ যেমন শিখেছিলে, `println!` হল একটি macro যা screen-এ একটি string print করে:

```rust,ignore
    println!("Guess the number!");

    println!("Please input your guess.");
```

এই কোডটি একটি prompt print করছে যা বলছে খেলাটি কী এবং user-এর কাছ থেকে input চাইছে।

### Variable-এর সাথে Value সংরক্ষণ করা

এরপর, আমরা user input সংরক্ষণ করার জন্য একটি _variable_ তৈরি করব, এভাবে:

```rust,ignore
    let mut guess = String::new();
```

এখন প্রোগ্রামটি আকর্ষণীয় হতে শুরু করেছে! এই ছোট লাইনে অনেক কিছু ঘটছে। আমরা `let` statement ব্যবহার করে variable তৈরি করি। আরেকটি উদাহরণ দেখো:

```rust,ignore
let apples = 5;
```

এই লাইনটি `apples` নামের একটি নতুন variable তৈরি করে এবং সেটিকে `5` value-এর সাথে bind করে। Rust-এ variable ডিফল্টভাবে immutable থাকে, অর্থাৎ একবার variable-এ একটি value দিলে সেই value বদলাবে না। আমরা এই concept সম্পর্কে Chapter 3-এর [“Variables এবং Mutability”][variables-and-mutability]<!-- ignore --> section-এ বিস্তারিত আলোচনা করব। একটি variable-কে mutable করতে, আমরা variable-এর নামের আগে `mut` যোগ করি:

```rust,ignore
let apples = 5; // immutable
let mut bananas = 5; // mutable
```

> Note: `//` syntax একটি comment শুরু করে যা লাইনের শেষ পর্যন্ত চলে। Rust comment-এর ভেতরের সবকিছু ignore করে। আমরা comment সম্পর্কে [Chapter 3][comments]<!-- ignore -->-এ আরও বিস্তারিত আলোচনা করব।

Guessing game প্রোগ্রামে ফিরে এসে, তুমি এখন জানো যে `let mut guess` একটি mutable variable যার নাম `guess` introduce করবে। সমান চিহ্ন (`=`) Rust-কে বলে যে আমরা এখন variable-এর সাথে কিছু bind করতে চাই। সমান চিহ্নের ডানপাশে হল সেই value যার সাথে `guess` bind হবে, যা হল `String::new` call করার ফল — একটি function যা `String`-এর একটি নতুন instance ফেরত দেয়। [`String`][string]<!-- ignore --> হল standard library-র দেওয়া একটি string type যা growable, UTF-8 encoded text-এর একটি অংশ।

`::new` লাইনের `::` syntax নির্দেশ করে যে `new` হল `String` type-এর একটি associated function। _Associated function_ হল এমন একটি function যা একটি type-এ implement করা থাকে, এই ক্ষেত্রে `String`। এই `new` function একটি নতুন, খালি string তৈরি করে। তুমি অনেক type-এ `new` function খুঁজে পাবে, কারণ এটি সাধারণত সেই নাম হিসেবে ব্যবহৃত হয় যা কোনো একটি kind-এর নতুন value বানায়।

পুরো কথায়, `let mut guess = String::new();` লাইনটি একটি mutable variable তৈরি করেছে যা বর্তমানে একটি নতুন, খালি `String` instance-এর সাথে bind আছে। ফু!

### User Input গ্রহণ করা

মনে করো আমরা প্রোগ্রামের প্রথম লাইনে `use std::io;` দিয়ে standard library থেকে input/output functionality include করেছিলাম। এখন আমরা `io` module থেকে `stdin` function call করব, যা আমাদের user input handle করতে দেবে:

```rust,ignore
    io::stdin()
        .read_line(&mut guess)
```

যদি আমরা প্রোগ্রামের শুরুতে `use std::io;` দিয়ে `io` module import না করতাম, তবুও আমরা সেই function-টি ব্যবহার করতে পারতাম এই function call-টিকে `std::io::stdin` হিসেবে লিখে। `stdin` function [`std::io::Stdin`][iostdin]<!-- ignore -->-এর একটি instance ফেরত দেয়, যা এমন একটি type যা তোমার terminal-এর standard input-এর একটি handle নির্দেশ করে।

এরপর, `.read_line(&mut guess)` লাইনটি standard input handle-এর উপর [`read_line`][read_line]<!-- ignore --> method call করে user-এর কাছ থেকে input নিতে। আমরা `read_line`-এ argument হিসেবে `&mut guess` pass করছি যাতে সে জানে কোন string-এ user input সংরক্ষণ করবে। `read_line`-এর পুরো কাজ হল user যা standard input-এ লেখে তা নিয়ে একটি string-এ append করা (তার আগের content overwrite না করে), তাই আমরা সেই string-টিকে argument হিসেবে pass করি। String argument-টি mutable হতে হবে যাতে method-টি string-এর content পরিবর্তন করতে পারে।

`&` নির্দেশ করে যে এই argument-টি একটি _reference_, যা তোমার code-এর একাধিক অংশকে একটি data-এ access দেওয়ার একটি উপায় কড়িয়ে দেয়, সেই data একাধিকবার memory-তে copy না করেই। Reference একটি জটিল feature, এবং Rust-এর অন্যতম প্রধান সুবিধা হল reference কতটা নিরাপদ এবং ব্যবহার করা সহজ। এই প্রোগ্রামটি শেষ করতে তোমাকে এসব বিস্তারিত জানতে হবে না। আপাতত, তোমার যা জানা দরকার তা হল — variable-এর মতো reference-ও ডিফল্টভাবে immutable থাকে। তাই, এটিকে mutable করতে তোমাকে `&guess` না লিখে `&mut guess` লিখতে হবে। (Chapter 4-এ reference সম্পর্কে আরও বিস্তারিত আলোচনা করা হবে।)

<!-- Old headings. Do not remove or links may break. -->

<a id="handling-potential-failure-with-the-result-type"></a>

### `Result` দিয়ে সম্ভাব্য Failure Handle করা

আমরা এখনও এই কোড line-টিতেই কাজ করছি। আমরা এখন টেক্সটের তৃতীয় লাইন নিয়ে আলোচনা করছি, কিন্তু মনে রাখবে এটি একটি single logical line of code-এর অংশ। পরবর্তী অংশটি হল এই method-টি:

```rust,ignore
        .expect("Failed to read line");
```

আমরা এই কোডটিকে এভাবেও লিখতে পারতাম:

```rust,ignore
io::stdin().read_line(&mut guess).expect("Failed to read line");
```

তবে একটি দীর্ঘ লাইন পড়তে কঠিন, তাই এটিকে ভাগ করা ভাল। `.method_name()` syntax দিয়ে method call করার সময় long line ভাগ করতে newline এবং অন্যান্য whitespace যোগ করা প্রায়ই বুদ্ধিমানের কাজ। এখন চলো আলোচনা করি এই লাইনটি কী করে।

আগে যেমন বলা হয়েছিল, `read_line` user যা লেখে তা আমরা যে string-টি pass করি সেখানে রাখে, কিন্তু এটি একটি `Result` value-ও ফেরত দেয়। [`Result`][result]<!-- ignore --> হল একটি [_enumeration_][enums]<!-- ignore -->, যাকে প্রায়ই _enum_ বলা হয়, যা এমন একটি type যা একাধিক সম্ভাব্য state-এর একটিতে থাকতে পারে। আমরা প্রতিটি সম্ভাব্য state-কে _variant_ বলি।

[Chapter 6][enums]<!-- ignore -->-এ enum সম্পর্কে আরও বিস্তারিত আলোচনা করা হবে। এই `Result` type-গুলোর উদ্দেশ্য হল error-handling সংক্রান্ত তথ্য encode করা।

`Result`-এর variant-গুলো হল `Ok` এবং `Err`। `Ok` variant নির্দেশ করে যে operation সফল হয়েছে, এবং এটি সফলভাবে তৈরি করা value ধারণ করে। `Err` variant মানে operation ব্যর্থ হয়েছে, এবং এটি কীভাবে বা কেন operation ব্যর্থ হয়েছে তার তথ্য ধারণ করে।

`Result` type-এর value-গুলোর, যেকোনো type-এর value-এর মতো, তাদের উপর method define করা থাকে। `Result`-এর একটি instance-এর একটি [`expect` method][expect]<!-- ignore --> আছে যা তুমি call করতে পারো। যদি এই `Result` instance-টি একটি `Err` value হয়, `expect` প্রোগ্রামটিকে crash করবে এবং তুমি `expect`-এ argument হিসেবে যে message দিয়েছিলে তা দেখাবে। যদি `read_line` method একটি `Err` ফেরত দেয়, তবে সম্ভবত এটি underlying operating system থেকে আসা কোনো error-এর ফল।

যদি এই `Result` instance-টি একটি `Ok` value হয়, `expect` সেই return value নেবে যা `Ok` ধারণ করছে এবং শুধু সেই value-টি তোমাকে ফেরত দেবে যাতে তুমি তা ব্যবহার করতে পারো। এই ক্ষেত্রে, সেই value হল user-এর input-এ থাকা byte-এর সংখ্যা।

যদি তুমি `expect` call না করো, প্রোগ্রামটি compile হবে, কিন্তু তুমি একটি warning পাবে:

```console
$ cargo build
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
warning: unused `Result` that must be used
  --> src/main.rs:10:5
   |
10 |     io::stdin().read_line(&mut guess);
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   |
   = note: this `Result` may be an `Err` variant, which should be handled
   = note: `#[warn(unused_must_use)]` (part of `#[warn(unused)]`) on by default
help: use `let _ = ...` to ignore the resulting value
   |
10 |     let _ = io::stdin().read_line(&mut guess);
   |     +++++++

warning: `guessing_game` (bin "guessing_game") generated 1 warning
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.59s
```

Rust warning দেয় যে তুমি `read_line` থেকে ফেরত আসা `Result` value ব্যবহার করোনি, নির্দেশ করে যে প্রোগ্রামটি একটি সম্ভাব্য error handle করেনি।

Warning দূর করার সঠিক উপায় হল আসলে error-handling কোড লেখা, কিন্তু আমাদের ক্ষেত্রে আমরা শুধু চাই সমস্যা হলে প্রোগ্রামটি crash করুক, তাই আমরা `expect` ব্যবহার করতে পারি। error থেকে পুনরুদ্ধার সম্পর্কে তুমি [Chapter 9][recover]<!-- ignore -->-এ শিখবে।

### `println!` Placeholder দিয়ে Value Print করা

closing curly bracket ছাড়া, এখন পর্যন্ত কোডে আলোচনা করার মতো আর মাত্র একটি লাইন বাকি:

```rust,ignore
    println!("You guessed: {guess}");
```

এই লাইনটি সেই string-টি print করে যাতে এখন user-এর input আছে। `{}` কার্লি ব্র্যাকেট জোড়া হল একটি placeholder: `{}`-কে ছোট crab pincer হিসেবে ভাবো যা একটি value-কে জায়গায় ধরে রাখে। একটি variable-এর value print করার সময়, variable-এর নাম কার্লি ব্র্যাকেটের ভেতরে থাকতে পারে। একটি expression evaluate করার ফল print করার সময়, format string-এ খালি কার্লি ব্র্যাকেট রাখো, তারপর format string-এর পরে একটি comma-separated list দাও যাতে প্রতিটি খালি কার্লি ব্র্যাকেট placeholder-এ সেই একই ক্রমে expression-গুলো print হয়। একটি variable এবং একটি expression-এর ফল একটি `println!` call-এ print করা এমন দেখাবে:

```rust
let x = 5;
let y = 10;

println!("x = {x} and y + 2 = {}", y + 2);
```

এই কোডটি `x = 5 and y + 2 = 12` print করবে।

### প্রথম অংশটি Test করা

চলো guessing game-এর প্রথম অংশটি test করি। `cargo run` দিয়ে এটি চালাও:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-01/
cargo clean
cargo run
input 6 -->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 6.44s
     Running `target/debug/guessing_game`
Guess the number!
Please input your guess.
6
You guessed: 6
```

এই মুহূর্তে, খেলার প্রথম অংশটি শেষ: আমরা keyboard থেকে input নিচ্ছি এবং তা print করছি।

## একটি Secret Number তৈরি করা

এরপর, আমাদের এমন একটি secret number তৈরি করতে হবে যা user অনুমান করার চেষ্টা করবে। Secret number প্রতিবার আলাদা হওয়া উচিত যাতে খেলাটি একাধিকবার খেলতে মজাদার হয়। আমরা ১ থেকে ১০০-এর মধ্যে একটি random number ব্যবহার করব যাতে খেলাটি খুব কঠিন না হয়। Rust-এর standard library-তে এখনও random number functionality অন্তর্ভুক্ত নেই। তবে Rust team [`rand` crate][randcrate] নামে একটি crate সরবরাহ করে যাতে এই functionality আছে।

<!-- Old headings. Do not remove or links may break. -->
<a id="using-a-crate-to-get-more-functionality"></a>

### একটি Crate দিয়ে Functionality বাড়ানো

মনে রাখবে crate হল Rust source code file-গুলোর একটি সংগ্রহ। আমরা যে project বানাচ্ছি সেটি একটি binary crate, যা একটি executable। `rand` crate-টি একটি library crate, যার ভেতরের কোড অন্যান্য প্রোগ্রামে ব্যবহারের জন্য তৈরি এবং এটি নিজে থেকে execute করা যায় না।

External crate-গুলোর coordination করাটাই Cargo-র সবচেয়ে চমকপ্রদ দিক। `rand` ব্যবহার করে এমন কোড লেখার আগে, আমাদের _Cargo.toml_ file-টি পরিবর্তন করে `rand` crate-কে একটি dependency হিসেবে যোগ করতে হবে। সেই file-টি এখন খোলো এবং নিচের লাইনটি Cargo তোমার জন্য তৈরি করা `[dependencies]` section header-এর নিচে bottom-এ যোগ করো। নিশ্চিত করো যে তুমি `rand`-কে ঠিক এখানে যেমন আছে তেমনভাবেই specify করেছ, এই version number সহ, নাহলে এই tutorial-এর কোড example-গুলো কাজ নাও করতে পারে:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
* ch14-03-cargo-workspaces.md
-->

<span class="filename">Filename: Cargo.toml</span>

```toml
[dependencies]
rand = "0.10.1"
```

_Cargo.toml_ file-এ, একটি header-এর পরে আসা সবকিছু সেই section-এর অংশ, যা অন্য একটি section শুরু না হওয়া পর্যন্ত চলে। `[dependencies]`-এ তুমি Cargo-কে বলো তোমার project কোন external crate-গুলোর উপর depend করে এবং তুমি সেই crate-গুলোর কোন version চাও। এই ক্ষেত্রে, আমরা `rand` crate-কে semantic version specifier `0.10.1` দিয়ে specify করি। Cargo [Semantic Versioning][semver]<!-- ignore --> বোঝে (যাকে কখনো _SemVer_ বলা হয়), যা version number লেখার একটি standard। Specifier `0.10.1` আসলে `^0.10.1`-এর shorthand, যার অর্থ যেকোনো version যা অন্তত 0.10.1 কিন্তু 0.11.0-এর নিচে।

Cargo মনে করে এই version-গুলোর public API version 0.10.1-এর সাথে compatible, এবং এই specification নিশ্চিত করে যে তুমি সর্বশেষ patch release পাবে যা এই chapter-এর কোডের সাথে এখনও compile হবে। যেকোনো version 0.11.0 বা তার বেশি-এর নিশ্চয়তা নেই যে নিচের example-গুলো যে API ব্যবহার করে তার সমান হবে।

এখন, কোনো কোড পরিবর্তন না করেই, চলো project-টি build করি, যেমন Listing 2-2-তে দেখানো হয়েছে।

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
rm Cargo.lock
cargo clean
cargo build -->

<Listing number="2-2" caption="The output from running `cargo build` after adding the `rand` crate as a dependency">

```console
$ cargo build
    Updating crates.io index
     Locking 8 packages to latest Rust 1.96.0 compatible versions
  Downloaded rand_core v0.10.1
  Downloaded chacha20 v0.10.1
  Downloaded rand v0.10.1
  Downloaded 3 crates (162.9KiB) in 0.59s
   Compiling libc v0.2.186
   Compiling rand_core v0.10.1
   Compiling getrandom v0.4.3
   Compiling cfg-if v1.0.4
   Compiling chacha20 v0.10.1
   Compiling rand v0.10.1
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 2.03s
```

</Listing>

তুমি ভিন্ন version number দেখতে পারো (কিন্তু সবগুলো কোডের সাথে compatible হবে, SemVer-এর জন্য ধন্যবাদ!) এবং ভিন্ন লাইন (operating system-এর উপর নির্ভর করে), এবং লাইনগুলো ভিন্ন ক্রমেও থাকতে পারে।

যখন আমরা একটি external dependency অন্তর্ভুক্ত করি, Cargo _registry_ থেকে সেই dependency-র প্রয়োজনীয় সবকিছুর সর্বশেষ version গুলো fetch করে, যেটি [Crates.io][cratesio] থেকে আসা data-এর একটি copy। Crates.io হল সেই জায়গা যেখানে Rust ecosystem-এর মানুষজন তাদের open source Rust project post করে অন্যদের ব্যবহারের জন্য।

Registry update করার পর, Cargo `[dependencies]` section check করে এবং যেসব crate ইতিমধ্যে download করা নেই সেগুলো download করে। এই ক্ষেত্রে, যদিও আমরা শুধু `rand`-কে dependency হিসেবে list করেছি, Cargo আরও কিছু crate download করেছে যার উপর `rand` কাজ করার জন্য depend করে। Crate-গুলো download করার পর, Rust সেগুলো compile করে এবং তারপর dependency available থাকা অবস্থায় project compile করে।

যদি তুমি কোনো পরিবর্তন না করেই সাথে সাথে আবার `cargo build` run করো, তুমি `Finished` লাইন ছাড়া আর কোনো output পাবে না। Cargo জানে সে ইতিমধ্যে dependency-গুলো download এবং compile করেছে, এবং তুমি তোমার _Cargo.toml_ file-এ সেগুলো সম্পর্কে কিছু পরিবর্তন করোনি। Cargo আরও জানে যে তুমি তোমার কোড সম্পর্কে কিছু পরিবর্তন করোনি, তাই সেটিও recompile করে না। করার কিছু না থাকায় সে শুধু exit করে।

যদি তুমি _src/main.rs_ file-টি খোলো, একটি তুচ্ছ পরিবর্তন করো, এবং তারপর save করে আবার build করো, তুমি শুধু দুটি লাইন output দেখবে:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
touch src/main.rs
cargo build -->

```console
$ cargo build
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
```

এই লাইনগুলো দেখায় যে Cargo শুধু _src/main.rs_ file-এ তোমার ছোট পরিবর্তনের সাথে build update করেছে। তোমার dependency-গুলো পরিবর্তিত হয়নি, তাই Cargo জানে সে যা আগে download এবং compile করেছে তা reuse করতে পারে।

<!-- Old headings. Do not remove or links may break. -->
<a id="ensuring-reproducible-builds-with-the-cargo-lock-file"></a>

#### Reproducible Build নিশ্চিত করা

Cargo-র এমন একটি mechanism আছে যা নিশ্চিত করে যে তুমি বা অন্য কেউ তোমার কোড build করলে প্রতিবার একই artifact rebuild করতে পারবে: Cargo শুধু তোমার specify করা dependency-গুলোর version ব্যবহার করবে যতক্ষণ না তুমি অন্যরূপে নির্দেশ করো। উদাহরণস্বরূপ, ধরো আগামী সপ্তাহে `rand` crate-এর version 0.10.2 বের হল, এবং সেই version-এ একটি গুরুত্বপূর্ণ bug fix আছে, কিন্তু এতে একটি regression-ও আছে যা তোমার কোড ভেঙে দেবে। এটি handle করার জন্য, Rust প্রথমবার তুমি `cargo build` run করার সময় _Cargo.lock_ file তৈরি করে, তাই এখন _guessing_game_ directory-তে আমাদের এই file আছে।

যখন তুমি প্রথমবার একটি project build করো, Cargo সব dependency-গুলোর version খুঁজে বের করে যা criteria পূরণ করে এবং সেগুলো _Cargo.lock_ file-এ লেখে। ভবিষ্যতে তুমি যখন তোমার project build করবে, Cargo দেখবে _Cargo.lock_ file-টি আছে এবং আবার version খুঁজে বের করার সমস্ত কাজ না করে সেখানে specify করা version ব্যবহার করবে। এর ফলে তোমার একটি reproducible build স্বয়ংক্রিয়ভাবে থাকে। অন্য কথায়, _Cargo.lock_ file-এর জন্য তোমার project ততক্ষণ 0.10.1-এই থাকবে যতক্ষণ না তুমি explicitly upgrade করো। যেহেতু _Cargo.lock_ file reproducible build-এর জন্য গুরুত্বপূর্ণ, এটি প্রায়ই project-এর বাকি কোডের সাথে source control-এ check করা হয়।

#### নতুন Version পেতে একটি Crate Update করা

যখন তুমি একটি crate update করতে চাও, Cargo `update` command সরবরাহ করে, যা _Cargo.lock_ file ignore করে এবং তোমার _Cargo.toml_-এর specification মেনে চলা সর্বশেষ version গুলো খুঁজে বের করে। তারপর Cargo সেই version-গুলো _Cargo.lock_ file-এ লেখে। অন্যথায়, ডিফল্টভাবে, Cargo শুধু 0.10.1-এর বেশি এবং 0.11.0-এর কম version খুঁজবে। যদি `rand` crate দুটি নতুন version 0.10.2 এবং 0.999.0 release করে থাকে, তুমি যদি `cargo update` run করো তবে নিচেরটা দেখবে:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
cargo update
assuming there is a new version of rand; otherwise use another update
as a guide to creating the hypothetical output shown here -->

```console
$ cargo update
    Updating crates.io index
     Locking 1 package to latest Rust 1.96.0 compatible version
    Updating rand v0.10.1 -> v0.10.2 (available: v0.999.0)
```

Cargo 0.999.0 release ignore করে। এই মুহূর্তে, তুমি তোমার _Cargo.lock_ file-এও একটি পরিবর্তন লক্ষ্য করবে যা জানায় যে তুমি এখন `rand` crate-এর যে version ব্যবহার করছ তা 0.10.2। `rand` version 0.999.0 অথবা 0.999._x_ series-এর যেকোনো version ব্যবহার করতে, তোমাকে _Cargo.toml_ file-টিকে নিচের মতো করে update করতে হবে (এই পরিবর্তনটি আসলে করবে না কারণ নিচের example-গুলো ধরে নেয় তুমি `rand` 0.10 ব্যবহার করছ):

```toml
[dependencies]
rand = "0.999.0"
```

পরবর্তীবার তুমি `cargo build` run করলে, Cargo available crate-গুলোর registry update করবে এবং তোমার specify করা নতুন version অনুযায়ী তোমার `rand` requirement পুনরায় evaluate করবে।

[Cargo][doccargo]<!-- ignore --> এবং [এর ecosystem][doccratesio]<!-- ignore --> সম্পর্কে আরও অনেক কিছু বলার আছে, যা আমরা Chapter 14-এ আলোচনা করব, কিন্তু আপাতত, তোমার যতটুকু জানা দরকার ততটুকুই। Cargo library reuse করা খুব সহজ করে দেয়, তাই Rustacean-রা ছোট ছোট project লিখতে পারে যা অনেকগুলো package থেকে assemble করা হয়।

### একটি Random Number তৈরি করা

চলো অনুমান করার জন্য একটি number তৈরি করতে `rand` ব্যবহার শুরু করি। পরবর্তী step হল _src/main.rs_ update করা, যেমন Listing 2-3-তে দেখানো হয়েছে।

<Listing number="2-3" file-name="src/main.rs" caption="Adding code to generate a random number">

```rust,ignore
use std::io;

use rand::prelude::*;

fn main() {
    println!("Guess the number!");

    let secret_number = rand::rng().random_range(1..=100);

    println!("The secret number is: {secret_number}");

    println!("Please input your guess.");

    let mut guess = String::new();

    io::stdin()
        .read_line(&mut guess)
        .expect("Failed to read line");

    println!("You guessed: {guess}");
}
```

</Listing>

প্রথমে, আমরা `use rand::prelude::*;` লাইনটি যোগ করি। `prelude` module-এ `rand` crate-এর সবচেয়ে বেশি ব্যবহৃত অংশগুলো থাকে, এবং `use` সেই item-গুলোকে আমাদের প্রোগ্রামের scope-এ available করে তোলে।

এরপর, আমরা মাঝখানে দুটি লাইন যোগ করছি। প্রথম লাইনে, আমরা `rand::rng` function call করি যা আমাদের সেই নির্দিষ্ট random number generator দেয় যা আমরা ব্যবহার করব: একটি যা current thread of execution-এ local এবং operating system দ্বারা seeded। তারপর, আমরা random number generator-এ `random_range` method call করি। এই method-টি `RngExt` trait দ্বারা define করা যা `rand::prelude` module-এর অংশ, যাকে আমরা `use rand::prelude::*;` statement দিয়ে scope-এ এনেছি। `random_range` method একটি range expression argument হিসেবে নেয় এবং সেই range-এ একটি random number তৈরি করে। আমরা এখানে যে ধরনের range expression ব্যবহার করছি তা `start..=end` রূপ নেয় এবং lower এবং upper bound-এ inclusive, তাই আমাদের ১ থেকে ১০০-এর মধ্যে একটি number চাইতে `1..=100` specify করতে হবে।

> Note: তুমি শুধু এমনিই জানবে না কোন crate থেকে কী scope-এ আনতে হবে এবং কোন method ও function call করতে হবে, তাই প্রতিটি crate-এর documentation থাকে এটি ব্যবহারের instruction সহ। Cargo-র আরেকটি চমৎকার feature হল `cargo doc --open` command run করলে তোমার সব dependency দ্বারা সরবরাহিত documentation স্থানীয়ভাবে build করে তোমার browser-এ খুলে দেবে। যদি তুমি উদাহরণস্বরূপ `rand` crate-এর অন্যান্য functionality-তে আগ্রহী হও, `cargo doc --open` run করো এবং বাম পাশের sidebar-এ `rand`-এ click করো।

দ্বিতীয় নতুন লাইনটি secret number print করে। প্রোগ্রামটি develop করার সময় এটি test করতে কাজে লাগে, কিন্তু আমরা এটি চূড়ান্ত version থেকে delete করব। প্রোগ্রাম শুরু হওয়ার সাথে সাথে যদি উত্তর print করে দেয় তবে তা খেলা হিসেবে বেশি কিছু নয়!

প্রোগ্রামটি কয়েকবার run করে দেখো:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-03/
cargo run
4
cargo run
5
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 7
Please input your guess.
4
You guessed: 4

$ cargo run
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 83
Please input your guess.
5
You guessed: 5
```

তোমার ভিন্ন random number আসা উচিত, এবং সবগুলো ১ থেকে ১০০-এর মধ্যে হওয়া উচিত। যদি তুমি warning পাও, সেগুলো ignore করতে নিরাপদ। যদি তুমি error পাও, অনুগ্রহ করে check করো তোমার *Cargo.toml*-এ `rand = "0.10.1"` আছে কি না, কারণ `rand`-এর ভবিষ্যৎ version-এ ভিন্ন API থাকতে পারে, কিন্তু `0.10` series-এর যেকোনো version এই chapter-এর কোডের সাথে কাজ করবে।

## অনুমানকে Secret Number-এর সাথে Compare করা

যেহেতু এখন আমাদের user input এবং একটি random number আছে, আমরা সেগুলোকে compare করতে পারি। সেই step-টি Listing 2-4-তে দেখানো হয়েছে। মনে রাখবে এই কোডটি এখনও compile হবে না, যেমন আমরা ব্যাখ্যা করব।

<Listing number="2-4" file-name="src/main.rs" caption="Handling the possible return values of comparing two numbers">

```rust,ignore,does_not_compile
use std::cmp::Ordering;
use std::io;

use rand::prelude::*;

fn main() {
    // --snip--

    println!("You guessed: {guess}");

    match guess.cmp(&secret_number) {
        Ordering::Less => println!("Too small!"),
        Ordering::Greater => println!("Too big!"),
        Ordering::Equal => println!("You win!"),
    }
}
```

</Listing>

প্রথমে, আমরা আরেকটি `use` statement যোগ করি, যা standard library থেকে `std::cmp::Ordering` নামের একটি type scope-এ আনে। `Ordering` type আরেকটি enum এবং এর variant হল `Less`, `Greater`, এবং `Equal`। এগুলো হল তিনটি সম্ভাব্য outcome যা তুমি দুটি value compare করলে ঘটতে পারে।

তারপর, আমরা bottom-এ পাঁচটি নতুন লাইন যোগ করি যা `Ordering` type ব্যবহার করে। `cmp` method দুটি value compare করে এবং যেকোনো comparable জিনিসের উপর call করা যেতে পারে। এটি তুমি যার সাথে compare করতে চাও তার একটি reference নেয়: এখানে, এটি `guess`-কে `secret_number`-এর সাথে compare করছে। তারপর, এটি `use` statement দিয়ে scope-এ আনা `Ordering` enum-এর একটি variant ফেরত দেয়। আমরা একটি [`match`][match]<!-- ignore --> expression ব্যবহার করি সিদ্ধান্ত নিতে যে `guess` এবং `secret_number` value দিয়ে `cmp` call করার ফলে কোন `Ordering` variant ফেরত এসেছে তার উপর ভিত্তি করে এরপর কী করতে হবে।

একটি `match` expression _arm_-গুলো দিয়ে তৈরি। একটি arm গঠিত একটি _pattern_ দিয়ে যার সাথে match করানো হয়, এবং সেই code যা `match`-কে দেওয়া value যদি সেই arm-এর pattern-এ fit হয় তবে run করা উচিত। Rust `match`-কে দেওয়া value নেয় এবং প্রতিটি arm-এর pattern পর্যায়ক্রমে check করে। Pattern এবং `match` construct Rust-এর শক্তিশালী feature: এগুলো তোমাকে বিভিন্ন পরিস্থিতি প্রকাশ করতে দেয় যা তোমার কোড encounter করতে পারে, এবং নিশ্চিত করে যে তুমি সবগুলো handle করেছ। এই feature-গুলো সম্পর্কে যথাক্রমে Chapter 6 এবং Chapter 19-এ বিস্তারিত আলোচনা করা হবে।

চলো আমরা এখানে যে `match` expression ব্যবহার করি তার একটি উদাহরণ দিয়ে হাঁটি। ধরো user ৫০ অনুমান করেছে এবং এবার randomly তৈরি হওয়া secret number হল ৩৮।

যখন কোড ৫০-কে ৩৮-এর সাথে compare করে, `cmp` method `Ordering::Greater` ফেরত দেবে কারণ ৫০, ৩৮-এর চেয়ে বড়। `match` expression `Ordering::Greater` value পায় এবং প্রতিটি arm-এর pattern check করা শুরু করে। এটি প্রথম arm-এর pattern `Ordering::Less` দেখে এবং বুঝতে পারে যে value `Ordering::Greater`, `Ordering::Less`-এর সাথে match করে না, তাই সেই arm-এর কোড ignore করে পরবর্তী arm-এ যায়। পরবর্তী arm-এর pattern হল `Ordering::Greater`, যা `Ordering::Greater`-এর সাথে match করে! সেই arm-এর associated কোড execute হবে এবং screen-এ `Too big!` print করবে। `match` expression প্রথম successful match-এর পর শেষ হয়ে যায়, তাই এই পরিস্থিতিতে এটি শেষ arm-টি দেখবে না।

তবে, Listing 2-4-এর কোড এখনও compile হবে না। চলো চেষ্টা করি:

<!--
The error numbers in this output should be that of the code **WITHOUT** the
anchor or snip comments
-->

```console
$ cargo build
   Compiling libc v0.2.186
   Compiling rand_core v0.10.1
   Compiling cfg-if v1.0.0
   Compiling getrandom v0.4.3
   Compiling chacha20 v0.10.1
   Compiling rand v0.10.1
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
error[E0308]: mismatched types
  --> src/main.rs:23:21
   |
23 |     match guess.cmp(&secret_number) {
   |                 --- ^^^^^^^^^^^^^^ expected `&String`, found `&{integer}`
   |                 |
   |                 arguments to this method are incorrect
   |
   = note: expected reference `&String`
              found reference `&{integer}`
note: method defined here
  --> /rustc/88d9e12ae178fab0fb5cc050a94da85685d449ea/library/core/src/cmp.rs:1000:7

For more information about this error, try `rustc --explain E0308`.
error: could not compile `guessing_game` (bin "guessing_game") due to 1 previous error
```

Error-টির core বলছে যে _mismatched types_ আছে। Rust-এর একটি শক্তিশালী, static type system আছে। তবে এর type inference-ও আছে। যখন আমরা `let mut guess = String::new()` লিখেছিলাম, Rust infer করতে পেরেছিল যে `guess` একটি `String` হওয়া উচিত এবং আমাদের type লেখাতে বাধ্য করেনি। অন্যদিকে, `secret_number` হল একটি number type। Rust-ের কিছু number type ১ থেকে ১০০-এর মধ্যে value নিতে পারে: `i32`, একটি 32-bit number; `u32`, একটি unsigned 32-bit number; `i64`, একটি 64-bit number; এবং অন্যান্য। অন্যরূপে specify না করা হলে, Rust ডিফল্টভাবে `i32` নেয়, যা `secret_number`-এর type, যদি না তুমি অন্য কোথাও type তথ্য যোগ করো যার ফলে Rust অন্য একটি numerical type infer করে। Error-এর কারণ হল Rust একটি string এবং একটি number type-এর মধ্যে compare করতে পারে না।

পরিশেষে, আমরা চাই প্রোগ্রামটি যে `String` input হিসেবে পড়ে তাকে একটি number type-এ convert করতে, যাতে আমরা এটিকে secret number-এর সাথে numerical ভাবে compare করতে পারি। আমরা তা করি `main` function-এর body-তে এই লাইনটি যোগ করে:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore
    // --snip--

    let mut guess = String::new();

    io::stdin()
        .read_line(&mut guess)
        .expect("Failed to read line");

    let guess: u32 = guess.trim().parse().expect("Please type a number!");

    println!("You guessed: {guess}");

    match guess.cmp(&secret_number) {
        Ordering::Less => println!("Too small!"),
        Ordering::Greater => println!("Too big!"),
        Ordering::Equal => println!("You win!"),
    }
```

লাইনটি হল:

```rust,ignore
let guess: u32 = guess.trim().parse().expect("Please type a number!");
```

আমরা `guess` নামের একটি variable তৈরি করি। কিন্তু দাঁড়াও, প্রোগ্রামের কি ইতিমধ্যেই `guess` নামের একটি variable নেই? আছে, কিন্তু Rust সহায়তার সাথে আমাদের `guess`-এর আগের value-কে একটি নতুন value দিয়ে shadow করতে দেয়। _Shadowing_ আমাদেরকে `guess` variable-এর নাম reuse করতে দেয়, এমন দুটি আলাদা variable তৈরি করতে বাধ্য না করে, যেমন `guess_str` এবং `guess`। আমরা এ সম্পর্কে [Chapter 3][shadowing]<!-- ignore -->-এ আরও বিস্তারিত আলোচনা করব, কিন্তু আপাতত জেনে রাখো যে এই feature প্রায়ই ব্যবহৃত হয় যখন তুমি একটি value-কে এক type থেকে অন্য type-ে convert করতে চাও।

আমরা এই নতুন variable-কে `guess.trim().parse()` expression-এর সাথে bind করি। Expression-টিতে `guess` বলতে সেই আসল `guess` variable-কে বোঝায় যা input-কে string হিসেবে ধারণ করেছিল। একটি `String` instance-এর `trim` method শুরু এবং শেষের কোনো whitespace সরিয়ে দেবে, যা আমাদের করতেই হবে string-কে `u32`-এ convert করার আগে, যা শুধুমাত্র numerical data ধারণ করতে পারে। User-কে অবশ্যই <kbd>enter</kbd> চাপতে হবে `read_line` satisfy করতে এবং তাদের অনুমান input করতে, যা string-এ একটি newline character যোগ করে। উদাহরণস্বরূপ, যদি user <kbd>5</kbd> লেখে এবং <kbd>enter</kbd> চাপে, `guess` এমন দেখায়: `5\n`। `\n` মানে “newline।” (Windows-এ, <kbd>enter</kbd> চাপলে একটি carriage return এবং একটি newline আসে, `\r\n`।) `trim` method `\n` বা `\r\n` সরিয়ে দেয়, ফলে শুধু `5` থাকে।

String-এর [`parse` method][parse]<!-- ignore --> একটি string-কে অন্য type-এ convert করে। এখানে, আমরা এটি ব্যবহার করি string থেকে number-এ convert করতে। আমাদের Rust-কে বলতে হবে আমরা ঠিক কোন number type চাই `let guess: u32` ব্যবহার করে। `guess`-এর পরে colon (`:`) Rust-কে বলে যে আমরা variable-এর type annotate করব। Rust-এ কিছু built-in number type আছে; এখানে দেখা `u32` হল একটি unsigned, 32-bit integer। ছোট positive number-এর জন্য এটি একটি ভাল ডিফল্ট পছন্দ। অন্যান্য number type সম্পর্কে তুমি [Chapter 3][integers]<!-- ignore -->-এ শিখবে।

তাছাড়া, এই example প্রোগ্রামে `u32` annotation এবং `secret_number`-এর সাথে comparison-এর অর্থ হল Rust infer করবে যে `secret_number`-ও একটি `u32` হওয়া উচিত। তাই, এখন comparison একই type-এর দুটি value-এর মধ্যে হবে!

`parse` method শুধুমাত্র সেই character-গুলোর উপর কাজ করবে যা logically number-এ convert করা যায়, তাই এটি সহজেই error ঘটাতে পারে। যদি উদাহরণস্বরূপ string-টিতে `A👍%` থাকে, তবে তাকে number-এ convert করার কোনো উপায় নেই। যেহেতু এটি ব্যর্থ হতে পারে, `parse` method একটি `Result` type ফেরত দেয়, ঠিক যেমন `read_line` method করে (আগে [“`Result` দিয়ে সম্ভাব্য Failure Handle করা”](#handling-potential-failure-with-result)<!-- ignore -->-এ আলোচনা করা হয়েছে)। আমরা এই `Result`-কেও একইভাবে treat করব আবার `expect` method ব্যবহার করে। যদি `parse` string থেকে number তৈরি করতে না পেরে একটি `Err` `Result` variant ফেরত দেয়, `expect` call খেলাটিকে crash করবে এবং আমরা যে message দিয়েছি তা print করবে। যদি `parse` সফলভাবে string-কে number-এ convert করতে পারে, এটি `Result`-এর `Ok` variant ফেরত দেবে, এবং `expect` সেই `Ok` value থেকে আমরা যে number চাই তা ফেরত দেবে।

চলো এখন প্রোগ্রামটি run করি:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/
touch src/main.rs
cargo run
  76
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.26s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 58
Please input your guess.
  76
You guessed: 76
Too big!
```

দারুণ! অনুমানের আগে spaces যোগ করা সত্ত্বেও প্রোগ্রাম বুঝতে পেরেছে যে user ৭৬ অনুমান করেছে। প্রোগ্রামটি কয়েকবার run করে বিভিন্ন ধরনের input-এ ভিন্ন আচরণ verify করো: সঠিক number অনুমান করো, এমন একটি number অনুমান করো যা খুব বড়, এবং এমন একটি number অনুমান করো যা খুব ছোট।

এখন খেলার বেশিরভাগ অংশ কাজ করছে, কিন্তু user শুধু একবারই অনুমান করতে পারে। চলো একটি loop যোগ করে এটি পরিবর্তন করি!

## Loop দিয়ে একাধিক অনুমানের সুযোগ দেওয়া

`loop` keyword একটি infinite loop তৈরি করে। আমরা user-দের number অনুমান করার আরও সুযোগ দিতে একটি loop যোগ করব:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore
    // --snip--

    println!("The secret number is: {secret_number}");

    loop {
        println!("Please input your guess.");

        // --snip--

        match guess.cmp(&secret_number) {
            Ordering::Less => println!("Too small!"),
            Ordering::Greater => println!("Too big!"),
            Ordering::Equal => println!("You win!"),
        }
    }
}
```

যেমন দেখতে পাচ্ছ, আমরা guess input prompt থেকে শুরু করে সবকিছু একটি loop-এ নিয়ে এসেছি। নিশ্চিত করো যে loop-এর ভেতরের লাইনগুলো আরও চারটি space করে indent করেছ এবং প্রোগ্রামটি আবার run করো। প্রোগ্রামটি এখন চিরকাল আরেকটি অনুমান চাইবে, যা আসলে একটি নতুন সমস্যা তৈরি করে। মনে হচ্ছে না user quit করতে পারবে!

User সবসময় keyboard shortcut <kbd>ctrl</kbd>-<kbd>C</kbd> ব্যবহার করে প্রোগ্রামটিকে interrupt করতে পারে। কিন্তু এই অন্তহীন monster থেকে বাঁচার আরেকটি উপায় আছে, যেমন [“অনুমানকে Secret Number-এর সাথে Compare করা”](#comparing-the-guess-to-the-secret-number)<!-- ignore -->-এ `parse` আলোচনায় উল্লেখ করা হয়েছে: যদি user এমন একটি উত্তর লেখে যা number নয়, প্রোগ্রামটি crash করবে। আমরা এর সুযোগ নিতে পারি user-কে quit করার অনুমতি দিতে, যেমন এখানে দেখানো হয়েছে:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-04-looping/
touch src/main.rs
cargo run
(too small guess)
(too big guess)
(correct guess)
quit
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.23s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 59
Please input your guess.
45
You guessed: 45
Too small!
Please input your guess.
60
You guessed: 60
Too big!
Please input your guess.
59
You guessed: 59
You win!
Please input your guess.
quit

thread 'main' (6694925) panicked at src/main.rs:28:47:
Please type a number!: ParseIntError { kind: InvalidDigit }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

`quit` লেখলে খেলা ছেড়ে দেবে, কিন্তু তুমি যেমন লক্ষ্য করবে, অন্য কোনো non-number input লিখলেও তা হবে। এটি কমপক্ষে বলা যায় যে এটি suboptimal; আমরা চাই সঠিক number অনুমান করা হলেও খেলাটি থেমে যাক।

### সঠিক অনুমানের পর Quit করা

চলো একটি `break` statement যোগ করে user win করলে খেলা ছেড়ে দেওয়ার প্রোগ্রাম করি:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore
        // --snip--

        match guess.cmp(&secret_number) {
            Ordering::Less => println!("Too small!"),
            Ordering::Greater => println!("Too big!"),
            Ordering::Equal => {
                println!("You win!");
                break;
            }
        }
    }
}
```

`You win!`-এর পরে `break` লাইন যোগ করায় user সঠিকভাবে secret number অনুমান করলে প্রোগ্রামটি loop থেকে বেরিয়ে যায়। Loop থেকে বেরিয়ে যাওয়া মানে প্রোগ্রাম থেকেও বেরিয়ে যাওয়া, কারণ loop-টি `main`-এর শেষ অংশ।

### অবৈধ Input Handle করা

খেলার আচরণ আরও নিখুঁত করতে, user non-number input লেখার সময় প্রোগ্রাম crash করার বদলে, চলো খেলাটিকে এমন করি যে non-number-কে ignore করে যাতে user আবার অনুমান করতে পারে। আমরা তা করতে পারি সেই লাইনটি পরিবর্তন করে যেখানে `guess`-কে `String` থেকে `u32`-এ convert করা হয়, যেমন Listing 2-5-তে দেখানো হয়েছে।

<Listing number="2-5" file-name="src/main.rs" caption="Ignoring a non-number guess and asking for another guess instead of crashing the program">

```rust,ignore
        // --snip--

        io::stdin()
            .read_line(&mut guess)
            .expect("Failed to read line");

        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };

        println!("You guessed: {guess}");

        // --snip--

        match guess.cmp(&secret_number) {
            Ordering::Less => println!("Too small!"),
            Ordering::Greater => println!("Too big!"),
            Ordering::Equal => {
                println!("You win!");
                break;
            }
        }
    }
}
```

</Listing>

আমরা `expect` call থেকে `match` expression-এ পরিবর্তন করে error-এ crash করা থেকে error handle করায় চলে এসেছি। মনে রাখবে `parse` একটি `Result` type ফেরত দেয় এবং `Result` হল একটি enum যার variant `Ok` এবং `Err`। আমরা এখানে একটি `match` expression ব্যবহার করছি, ঠিক যেমন `cmp` method-এর `Ordering` result-এর সাথে করেছিলাম।

যদি `parse` সফলভাবে string-কে number-এ পরিণত করতে পারে, এটি একটি `Ok` value ফেরত দেবে যা resultant number ধারণ করে। সেই `Ok` value প্রথম arm-এর pattern-ের সাথে match করবে, এবং `match` expression শুধু সেই `num` value ফেরত দেবে যা `parse` তৈরি করেছে এবং `Ok` value-এর ভেতরে রেখেছে। সেই number ঠিক সেই জায়গায় গিয়ে শেষ হবে যেখানে আমরা চাই — আমরা যে নতুন `guess` variable তৈরি করছি তার ভেতরে।

যদি `parse` string-কে number-এ পরিণত করতে না পারে, এটি একটি `Err` value ফেরত দেবে যা error সম্পর্কে আরও তথ্য ধারণ করে। `Err` value প্রথম `match` arm-এর `Ok(num)` pattern-ের সাথে match করে না, কিন্তু এটি দ্বিতীয় arm-ের `Err(_)` pattern-ের সাথে match করে। Underscore, `_`, হল একটি catch-all value; এই example-এ, আমরা বলছি যে আমরা সব `Err` value match করতে চাই, ভেতরে যা তথ্যই থাকুক না কেন। তাই, প্রোগ্রামটি দ্বিতীয় arm-ের কোড, `continue`, execute করবে, যা প্রোগ্রামকে বলে `loop`-এর পরবর্তী iteration-এ যেতে এবং আরেকটি অনুমান চাইতে। তাই, কার্যত প্রোগ্রামটি সেই সব error ignore করে যা `parse` encounter করতে পারে!

এখন প্রোগ্রামের সবকিছু প্রত্যাশা অনুযায়ী কাজ করা উচিত। চলো চেষ্টা করি:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-05/
cargo run
(too small guess)
(too big guess)
foo
(correct guess)
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 61
Please input your guess.
10
You guessed: 10
Too small!
Please input your guess.
99
You guessed: 99
Too big!
Please input your guess.
foo
Please input your guess.
61
You guessed: 61
You win!
```

দারুণ! আরেকটি ছোট final tweak দিলেই আমরা guessing game শেষ করব। মনে করো প্রোগ্রামটি এখনও secret number print করছে। এটি test করার জন্য ভাল কাজ করেছিল, কিন্তু এটি খেলাটি নষ্ট করে দেয়। চলো secret number output করা `println!` টি delete করি। Listing 2-6-তে চূড়ান্ত কোড দেখানো হয়েছে।

<Listing number="2-6" file-name="src/main.rs" caption="Complete guessing game code">

```rust,ignore
use std::cmp::Ordering;
use std::io;

use rand::prelude::*;

fn main() {
    println!("Guess the number!");

    let secret_number = rand::rng().random_range(1..=100);

    loop {
        println!("Please input your guess.");

        let mut guess = String::new();

        io::stdin()
            .read_line(&mut guess)
            .expect("Failed to read line");

        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };

        println!("You guessed: {guess}");

        match guess.cmp(&secret_number) {
            Ordering::Less => println!("Too small!"),
            Ordering::Greater => println!("Too big!"),
            Ordering::Equal => {
                println!("You win!");
                break;
            }
        }
    }
}
```

</Listing>

এই মুহূর্তে, তুমি সফলভাবে guessing game তৈরি করেছ। অভিনন্দন!

## Summary

এই project তোমাকে অনেক নতুন Rust concept-ের সাথে পরিচয় করানোর একটি hands-on উপায় ছিল: `let`, `match`, function, external crate ব্যবহার এবং আরও অনেক কিছু। পরবর্তী কয়েকটি chapter-এ তুমি এই concept-গুলো সম্পর্কে আরও বিস্তারিত শিখবে। Chapter 3 covers concept যা বেশিরভাগ programming language-এ থাকে, যেমন variable, data type এবং function, এবং দেখায় কীভাবে সেগুলো Rust-এ ব্যবহার করতে হয়। Chapter 4 explores ownership, এমন একটি feature যা Rust-কে অন্যান্য language থেকে আলাদা করে। Chapter 5-এ struct এবং method syntax আলোচনা করা হয়েছে, এবং Chapter 6 ব্যাখ্যা করে কীভাবে enum কাজ করে।

[prelude]: ../std/prelude/index.html
[variables-and-mutability]: ch03-01-variables-and-mutability.html#variables-and-mutability
[comments]: ch03-04-comments.html
[string]: ../std/string/struct.String.html
[iostdin]: ../std/io/struct.Stdin.html
[read_line]: ../std/io/struct.Stdin.html#method.read_line
[result]: ../std/result/enum.Result.html
[enums]: ch06-00-enums.html
[expect]: ../std/result/enum.Result.html#method.expect
[recover]: ch09-02-recoverable-errors-with-result.html
[randcrate]: https://crates.io/crates/rand
[semver]: http://semver.org
[cratesio]: https://crates.io/
[doccargo]: https://doc.rust-lang.org/cargo/
[doccratesio]: https://doc.rust-lang.org/cargo/reference/publishing.html
[match]: ch06-02-match.html
[shadowing]: ch03-01-variables-and-mutability.html#shadowing
[parse]: ../std/primitive.str.html#method.parse
[integers]: ch03-02-data-types.html#integer-types

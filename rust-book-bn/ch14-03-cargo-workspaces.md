## Cargo Workspaces

Chapter 12-তে আমরা এমন একটি package build করেছিলাম যাতে একটি binary crate এবং একটি library crate ছিল। তোমার project যখন বড় হতে থাকবে, তুমি দেখতে পাবে library crate আরও বড় হচ্ছে এবং তুমি তোমার package কে আরও একাধিক library crate-এ ভাগ করতে চাইবে। Cargo _workspaces_ নামের একটি feature দেয় যা একসাথে develop হওয়া একাধিক সম্পর্কিত package manage করতে সাহায্য করে।

### একটি Workspace তৈরি করা

একটি _workspace_ হলো এমন কিছু package-এর সমষ্টি যারা একই _Cargo.lock_ এবং output directory share করে। চলো একটি workspace ব্যবহার করে একটি project বানাই — আমরা ছোট ছোট trivial code ব্যবহার করব যাতে আমরা workspace-এর structure-এ মনোযোগ দিতে পারি। Workspace structure করার একাধিক উপায় আছে, তাই আমরা শুধু একটি সাধারণ উপায় দেখাবো। আমাদের workspace-এ থাকবে একটি binary এবং দুটি library। যে binary-টি main functionality দেবে সেটি এই দুটি library-র উপর নির্ভর করবে। একটি library একটি `add_one` function দেবে এবং অন্য library একটি `add_two` function দেবে। এই তিনটি crate একই workspace-এর অংশ হবে। আমরা প্রথমে workspace-এর জন্য একটি নতুন directory তৈরি করব:

```console
$ mkdir add
$ cd add
```

এরপর, _add_ directory-তে আমরা _Cargo.toml_ file তৈরি করব যা পুরো workspace configure করবে। এই file-এ কোনো `[package]` section থাকবে না। এর বদলে, এতে একটি `[workspace]` section দিয়ে শুরু হবে যা আমাদের workspace-এ member যোগ করতে দেবে। আমরা এটাও নিশ্চিত করব যে আমাদের workspace-এ Cargo-র resolver algorithm-এর সর্বশেষ ও সেরা version ব্যবহার করতে `resolver` value টি `"3"` তে সেট করব:

<span class="filename">Filename: Cargo.toml</span>

```toml
[workspace]
resolver = "3"
```

এরপর, আমরা _add_ directory-র ভেতরে `cargo new` run করে `adder` binary crate তৈরি করব:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-01-adder-crate/add
remove `members = ["adder"]` from Cargo.toml
rm -rf adder
cargo new adder
copy output below
-->

```console
$ cargo new adder
     Created binary (application) `adder` package
      Adding `adder` as member of workspace at `file:///projects/add`
```

Workspace-এর ভেতরে `cargo new` run করলে নতুন তৈরি হওয়া package-টি workspace-এর _Cargo.toml_-এ `[workspace]` definition-এর `members` key-তে স্বয়ংক্রিয়ভাবে যোগ হয়ে যায়, এভাবে:

```toml
[workspace]
resolver = "3"
members = ["adder"]
```

এই মুহূর্তে, আমরা `cargo build` run করে workspace build করতে পারি। তোমার _add_ directory-র file গুলো দেখতে এমন হওয়া উচিত:

```text
├── Cargo.lock
├── Cargo.toml
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

Workspace-এ top level-এ একটি _target_ directory আছে যেখানে compile হওয়া artifact গুলো রাখা হবে; `adder` package-এর নিজের কোনো _target_ directory নেই। যদি আমরা _adder_ directory থেকেও `cargo build` run করি, compile হওয়া artifact গুলো _add/adder/target_-এর বদলে _add/target_-এই গিয়ে পড়বে। Cargo workspace-এ _target_ directory-কে এভাবে structure করে কারণ একটি workspace-এর crate গুলো একে অপরের উপর নির্ভর করার জন্যই তৈরি। যদি প্রতিটি crate-এর নিজস্ব _target_ directory থাকত, তবে প্রতিটি crate-কে তার নিজস্ব _target_ directory-তে artifact রাখার জন্য workspace-এর অন্য সব crate আলাদাভাবে recompile করতে হতো। একটি _target_ directory share করে crate গুলো অপ্রয়োজনীয় rebuilding এড়াতে পারে।

### Workspace-এ দ্বিতীয় Package তৈরি করা

এরপর, চলো workspace-এ আরেকটি member package তৈরি করি যার নাম দেব `add_one`। `add_one` নামের একটি নতুন library crate generate করো:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-02-add-one/add
remove `"add_one"` from `members` list in Cargo.toml
rm -rf add_one
cargo new add_one --lib
copy output below
-->

```console
$ cargo new add_one --lib
     Created library `add_one` package
      Adding `add_one` as member of workspace at `file:///projects/add`
```

Top-level _Cargo.toml_-এ এখন `members` list-এ _add_one_ path যোগ হবে:

<span class="filename">Filename: Cargo.toml</span>

```toml
[workspace]
resolver = "3"
members = ["adder", "add_one"]
```

তোমার _add_ directory-তে এখন এই directory এবং file গুলো থাকা উচিত:

```text
├── Cargo.lock
├── Cargo.toml
├── add_one
│   ├── Cargo.toml
│   └── src
│       └── lib.rs
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

_add_one/src/lib.rs_ file-এ, চলো একটি `add_one` function যোগ করি:

<span class="filename">Filename: add_one/src/lib.rs</span>

```rust,noplayground
pub fn add_one(x: i32) -> i32 {
    x + 1
}
```

এখন আমরা আমাদের binary সহ `adder` package কে আমাদের library সহ `add_one` package-এর উপর নির্ভর করাতে পারি। প্রথমে, _adder/Cargo.toml_-এ `add_one`-এর একটি path dependency যোগ করতে হবে।

<span class="filename">Filename: adder/Cargo.toml</span>

```toml
[dependencies]
add_one = { path = "../add_one" }
```

Cargo ধরে নেয় না যে একটি workspace-এর crate গুলো একে অপরের উপর নির্ভর করবে, তাই dependency relationship গুলো আমাদের স্পষ্টভাবে উল্লেখ করতে হবে।

এরপর, চলো `adder` crate-এ `add_one` function (`add_one` crate থেকে) ব্যবহার করি। _adder/src/main.rs_ file খোলো এবং `main` function-কে পরিবর্তন করে `add_one` function call করো, যেমন Listing 14-7-তে।

<Listing number="14-7" file-name="adder/src/main.rs" caption="Using the `add_one` library crate from the `adder` crate">

```rust,ignore
fn main() {
    let num = 10;
    println!("Hello, world! {num} plus one is {}!", add_one::add_one(num));
}
```

</Listing>

চলো top-level _add_ directory-তে `cargo build` run করে workspace build করি!

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.22s
```

_add_ directory থেকে binary crate run করতে, আমরা `cargo run`-এর সাথে `-p` argument এবং package নাম ব্যবহার করে workspace-এর কোন package টি run করতে চাই তা specify করতে পারি:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo run -p adder
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo run -p adder
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running `target/debug/adder`
Hello, world! 10 plus one is 11!
```

এটি _adder/src/main.rs_-এর code run করে, যা `add_one` crate-এর উপর নির্ভর করে।

<!-- Old headings. Do not remove or links may break. -->

<a id="depending-on-an-external-package-in-a-workspace"></a>

### একটি External Package-এর উপর নির্ভর করা

খেয়াল করো যে workspace-এ top level-এ শুধু একটিই _Cargo.lock_ file আছে, প্রতিটি crate-এর directory-তে আলাদা _Cargo.lock_ নেই। এটি নিশ্চিত করে যে সব crate সব dependency-এর একই version ব্যবহার করছে। যদি আমরা `rand` package কে _adder/Cargo.toml_ এবং _add_one/Cargo.toml_ file দুটিতে যোগ করি, Cargo সে দুটিকেই `rand`-এর একটি version-এ resolve করবে এবং সেটি একটিমাত্র _Cargo.lock_-এ record করবে। Workspace-এর সব crate কে একই dependency ব্যবহার করানোর অর্থ হলো crate গুলো সবসময় একে অপরের সাথে compatible থাকবে। চলো _add_one/Cargo.toml_ file-এর `[dependencies]` section-এ `rand` crate যোগ করি যাতে আমরা `add_one` crate-এ `rand` crate ব্যবহার করতে পারি:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
-->

<span class="filename">Filename: add_one/Cargo.toml</span>

```toml
[dependencies]
rand = "0.10.1"
```

আমরা এখন _add_one/src/lib.rs_ file-এ `use rand;` যোগ করতে পারি, এবং _add_ directory-তে `cargo build` run করে পুরো workspace build করলে `rand` crate টি আসবে ও compile হবে। আমরা একটি warning পাব কারণ আমরা scope-এ আনা `rand` কে refer করছি না:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
    Updating crates.io index
  Downloaded rand v0.10.1
   --snip--
   Compiling rand v0.10.1
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
warning: unused import: `rand`
 --> add_one/src/lib.rs:1:5
  |
1 | use rand;
  |     ^^^^
  |
  = note: `#[warn(unused_imports)]` (part of `#[warn(unused)]`) on by default

warning: `add_one` (lib) generated 1 warning (run `cargo fix --lib -p add_one` to apply 1 suggestion)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.95s
```

Top-level _Cargo.lock_-এ এখন `add_one`-এর `rand`-এর উপর নির্ভরতা সম্পর্কিত তথ্য আছে। তবে, যদিও `rand` workspace-এর কোথাও ব্যবহৃত হয়েছে, আমরা workspace-এর অন্য crate-এ এটি ব্যবহার করতে পারব না যদি না তাদের _Cargo.toml_ file-এও `rand` যোগ করি। উদাহরণস্বরূপ, যদি আমরা `adder` package-এর জন্য _adder/src/main.rs_ file-এ `use rand;` যোগ করি, তবে আমরা একটি error পাব:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-03-use-rand/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
  --snip--
   Compiling adder v0.1.0 (file:///projects/add/adder)
error[E0432]: unresolved import `rand`
 --> adder/src/main.rs:2:5
  |
2 | use rand;
  |     ^^^^ no external crate `rand`
```

এটি fix করতে, `adder` package-এর _Cargo.toml_ file সম্পাদনা করো এবং উল্লেখ করো যে `rand` এর জন্যও একটি dependency। `adder` package build করলে _Cargo.lock_-এ `adder`-এর dependency list-এ `rand` যোগ হবে, কিন্তু `rand`-এর কোনো অতিরিক্ত copy download হবে না। যতক্ষণ workspace-এর প্রতিটি package-এর প্রতিটি crate `rand` package-এর compatible version specify করবে, ততক্ষণ Cargo নিশ্চিত করবে যে `rand` package ব্যবহার করা প্রতিটি crate একই version ব্যবহার করবে, যা আমাদের জায়গা বাঁচায় এবং workspace-এর crate গুলো একে অপরের সাথে compatible হবে তা নিশ্চিত করে।

যদি workspace-এর crate গুলো একই dependency-এর incompatible version specify করে, Cargo সে সবগুলোকে resolve করবে কিন্তু সম্ভব হলে যত কম version পারা যায় ততটাই resolve করার চেষ্টা করবে।

### একটি Workspace-এ Test যোগ করা

আরেকটি enhancement হিসেবে, চলো `add_one` crate-এর ভেতরে `add_one::add_one` function-এর একটি test যোগ করি:

<span class="filename">Filename: add_one/src/lib.rs</span>

```rust,noplayground
pub fn add_one(x: i32) -> i32 {
    x + 1
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(3, add_one(2));
    }
}
```

এখন top-level _add_ directory-তে `cargo test` run করো। এমন workspace-এ `cargo test` run করলে workspace-এর সব crate-এর test গুলো run হবে:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test
copy output below; the output updating script doesn't handle subdirectories in
paths properly
-->

```console
$ cargo test
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.20s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/debug/deps/adder-3a47283c568d2b6a)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

output-এর প্রথম section দেখায় যে `add_one` crate-এর `it_works` test pass করেছে। পরের section দেখায় যে `adder` crate-এ কোনো test পাওয়া যায়নি, এবং তারপরের শেষ section দেখায় যে `add_one` crate-এ কোনো documentation test পাওয়া যায়নি।

আমরা top-level directory থেকে `-p` flag ব্যবহার করে এবং যে crate টি test করতে চাই তার নাম specify করে একটি workspace-এর কোনো নির্দিষ্ট crate-এর test ও run করতে পারি:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test -p add_one
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo test -p add_one
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

এই output দেখায় যে `cargo test` শুধু `add_one` crate-এর test গুলো run করেছে এবং `adder` crate-এর test গুলো run করেনি।

তুমি workspace-এর crate গুলো [crates.io](https://crates.io/)<!-- ignore -->-তে publish করলে, workspace-এর প্রতিটি crate আলাদাভাবে publish করতে হবে। `cargo test`-এর মতো, আমরা `-p` flag ব্যবহার করে এবং যে crate টি publish করতে চাই তার নাম specify করে আমাদের workspace-এর কোনো নির্দিষ্ট crate publish করতে পারি।

অতিরিক্ত অনুশীলনের জন্য, `add_one` crate-এর মতো একইভাবে এই workspace-এ একটি `add_two` crate যোগ করো!

তোমার project যখন বড় হবে, workspace ব্যবহার করা বিবেচনা করো: এটি তোমাকে এক বিশাল কোডের ব্লবের বদলে ছোট, বোঝার সহজ component নিয়ে কাজ করতে দেয়। তাছাড়া, workspace-এ crate গুলো একসাথে রাখলে যদি সেগুলো প্রায়ই একই সময়ে পরিবর্তিত হয় তবে crate-গুলোর মধ্যে সমন্বয় সহজ হতে পারে।

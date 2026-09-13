## Test Organization

Chapter-এর শুরুতে যেমনটা বলা হয়েছিল, testing একটি জটিল শাস্ত্র, এবং ভিন্ন ভিন্ন মানুষ ভিন্ন ভিন্ন terminology ও organization ব্যবহার করে। Rust community test-কে দুটি প্রধান category-তে ভাবে: unit test এবং integration test। _Unit test_ ছোট ও বেশি focused, একসময়ে একটি module-কে বিচ্ছিন্নভাবে test করে, এবং private interface test করতে পারে। _Integration test_ সম্পূর্ণভাবে তোমার library-র বাইরে থাকে এবং তোমার code-কে এমনভাবে ব্যবহার করে যেমনভাবে অন্য কোনো external code ব্যবহার করত — শুধুমাত্র public interface ব্যবহার করে এবং সম্ভবত প্রতি test-এ একাধিক module-কে exercise করে।

তোমার library-র অংশগুলো আলাদাভাবে এবং একসাথে তোমার প্রত্যাশা অনুযায়ী কাজ করছে কিনা তা নিশ্চিত করতে উভয় ধরনের test লেখা গুরুত্বপূর্ণ।

### Unit Test

Unit test-গুলোর উদ্দেশ্য হলো code-এর প্রতিটি ইউনিটকে বাকি code থেকে বিচ্ছিন্নভাবে test করা, যাতে দ্রুত শনাক্ত করা যায় কোন কোন code প্রত্যাশা অনুযায়ী কাজ করছে এবং কোনটি করছে না। তুমি unit test-গুলো _src_ ডিরেক্টরিতে প্রতিটি file-এ রাখবে যেই file-এর code তারা test করছে। প্রতিটি file-এ `tests` নামে একটি module তৈরি করা convention, যেখানে test function-গুলো থাকবে এবং module-টিকে `cfg(test)` দিয়ে annotate করা হবে।

#### `tests` Module এবং `#[cfg(test)]`

`tests` module-এর ওপর `#[cfg(test)]` annotation Rust-কে বলে যে test code-টি শুধু তখনই compile ও run করতে হবে যখন তুমি `cargo test` চালাও, `cargo build` চালানোর সময় নয়। এটি তখন compile time বাঁচায় যখন তুমি শুধু library build করতে চাও এবং ফলস্বরূপ compiled artifact-এ জায়গা বাঁায় কারণ test-গুলো সেখানে অন্তর্ভুক্ত থাকে না। তুমি দেখবে যেহেতু integration test-গুলো ভিন্ন ডিরেক্টরিতে যায়, সেগুলোর `#[cfg(test)]` annotation-এর প্রয়োজন হয় না। তবে যেহেতু unit test-গুলো code-এর সাথে একই file-এ থাকে, তাই তুমি `#[cfg(test)]` ব্যবহার করে নির্দিষ্ট করবে যে সেগুলো যেন compiled ফলাফলে অন্তর্ভুক্ত না হয়।

মনে করো যে এই chapter-এর প্রথম section-এ আমরা যখন নতুন `adder` project তৈরি করেছিলাম, তখন Cargo আমাদের জন্য এই code তৈরি করেছিল:

<span class="filename">Filename: src/lib.rs</span>

```rust,noplayground
pub fn add(left: u64, right: u64) -> u64 {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
```

স্বয়ংক্রিয়ভাবে তৈরি হওয়া `tests` module-এ, `cfg` attribute-টির অর্থ _configuration_ এবং এটি Rust-কে বলে যে নিচের item-টি শুধুমাত্র একটি নির্দিষ্ট configuration option থাকলে অন্তর্ভুক্ত করতে হবে। এই ক্ষেত্রে configuration option-টি হলো `test`, যা Rust test compile ও run করার জন্য সরবরাহ করে। `cfg` attribute ব্যবহার করে, Cargo আমাদের test code শুধুমাত্র তখনই compile করে যখন আমরা `cargo test` দিয়ে সক্রিয়ভাবে test চালাই। এতে এই module-এ থাকা যেকোনো helper function অন্তর্ভুক্ত হয়, `#[test]` দিয়ে annotated function-গুলোর পাশাপাশি।

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-private-functions"></a>

#### Private Function Test

Testing community-তে এ নিয়ে বিতর্ক আছে যে private function-গুলো সরাসরি test করা উচিত কিনা, এবং অন্যান্য ভাষায় private function test করা কঠিন বা অসম্ভব। তুমি যেই testing ideology মেনে চলো না কেন, Rust-এর privacy rule তোমাকে private function test করতে দেয়। Listing 11-12-তে থাকা code-টি বিবেচনা করো, যেখানে `internal_adder` নামে একটি private function আছে।

<Listing number="11-12" file-name="src/lib.rs" caption="Testing a private function">

```rust,noplayground
pub fn add_two(a: u64) -> u64 {
    internal_adder(a, 2)
}

fn internal_adder(left: u64, right: u64) -> u64 {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn internal() {
        let result = internal_adder(2, 2);
        assert_eq!(result, 4);
    }
}
```

</Listing>

খেয়াল করো যে `internal_adder` function-টিকে `pub` হিসেবে চিহ্নিত করা হয়নি। Test-গুলো শুধু Rust code, এবং `tests` module আরেকটি মাত্র module। যেমনটা আমরা ["Paths for Referring to an Item in the Module Tree"][paths]<!-- ignore -->-এ আলোচনা করেছি, child module-গুলোর item-গুলো তাদের ancestor module-এর item ব্যবহার করতে পারে। এই test-এ আমরা `tests` module-এর parent-এর সব item `use super::*` দিয়ে scope-এ আনি, এবং তারপর test-টি `internal_adder`-কে call করতে পারে। তুমি যদি মনে করো private function test করা উচিত নয়, তবে Rust-এ এমন কিছু নেই যা তোমাকে সেটি করতে বাধ্য করবে।

### Integration Test

Rust-এ integration test সম্পূর্ণভাবে তোমার library-র বাইরে থাকে। এগুলো তোমার library ব্যবহার করে ঠিক সেভাবে যেভাবে অন্য যেকোনো code ব্যবহার করত, যার মানে হলো এগুলো শুধুমাত্র সেই সব function call করতে পারে যেগুলো তোমার library-র public API-এর অংশ। এদের উদ্দেশ্য হলো test করা যে তোমার library-র অনেকগুলো অংশ একসাথে সঠিকভাবে কাজ করে কিনা। যে সব code ইউনিট নিজে নিজে সঠিকভাবে কাজ করে তারা integrate হওয়ার সময় সমস্যা তৈরি করতে পারে, তাই integrated code-এর test coverage-ও গুরুত্বপূর্ণ। Integration test তৈরি করতে তোমার প্রথমে একটি _tests_ ডিরেক্টরি দরকার।

#### _tests_ ডিরেক্টরি

আমরা আমাদের project ডিরেক্টরির top level-এ, _src_-এর পাশে একটি _tests_ ডিরেক্টরি তৈরি করি। Cargo জানে এই ডিরেক্টরিতে integration test file খুঁজতে হবে। এরপর আমরা যত খুশি test file বানাতে পারি, এবং Cargo প্রতিটি file-কে একটি আলাদা crate হিসেবে compile করবে।

চলো একটি integration test তৈরি করি। Listing 11-12-এর code _src/lib.rs_ file-এ রেখে, একটি _tests_ ডিরেক্টরি বানাও, এবং _tests/integration_test.rs_ নামে একটি নতুন file তৈরি করো। তোমার ডিরেক্টরি structure এমন হওয়া উচিত:

```text
adder
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    └── integration_test.rs
```

_tests/integration_test.rs_ file-এ Listing 11-13-এর code লেখো।

<Listing number="11-13" file-name="tests/integration_test.rs" caption="An integration test of a function in the `adder` crate">

```rust,ignore
use adder::add_two;

#[test]
fn it_adds_two() {
    let result = add_two(2);
    assert_eq!(result, 4);
}
```

</Listing>

_tests_ ডিরেক্টরির প্রতিটি file একটি আলাদা crate, তাই আমাদের প্রতিটি test crate-এর scope-এ আমাদের library-কে আনতে হবে। সেই কারণে আমরা code-এর শীর্ষে `use adder::add_two;` যোগ করি, যা unit test-গুলোর ক্ষেত্রে আমাদের দরকার হয়নি।

_tests/integration_test.rs_-এ আমাদের কোনো code-কে `#[cfg(test)]` দিয়ে annotate করতে হয় না। Cargo _tests_ ডিরেক্টরিকে বিশেষভাবে গণ্য করে এবং এই ডিরেক্টরির file-গুলো শুধু তখনই compile করে যখন আমরা `cargo test` চালাই। এখন `cargo test` চালাও:

```console
$ cargo test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 1.31s
     Running unittests src/lib.rs (target/debug/deps/adder-1082c4b063a8fbe6)

running 1 test
test tests::internal ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running tests/integration_test.rs (target/debug/deps/integration_test-1082c4b063a8fbe6)

running 1 test
test it_adds_two ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests adder

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

Output-এর তিনটি section হলো unit test, integration test, এবং doc test। খেয়াল করো যে কোনো একটি section-এ কোনো test fail করলে পরের section-গুলো চলবে না। উদাহরণস্বরূপ, যদি কোনো unit test fail করে, তবে integration ও doc test-এর কোনো output থাকবে না, কারণ সেই test-গুলো তখনই চলবে যখন সব unit test pass করবে।

Unit test-গুলোর জন্য প্রথম section-টি সেরকমই যেমনটা আমরা দেখে আসছি: প্রতিটি unit test-এর জন্য একটি করে লাইন (Listing 11-12-তে আমরা যে `internal` নামেরটি যোগ করেছি) এবং তারপর unit test-গুলোর জন্য একটি সারসংক্ষেপ লাইন।

Integration test section `Running tests/integration_test.rs` লাইন দিয়ে শুরু হয়। এরপর ওই integration test-এর প্রতিটি test function-এর জন্য একটি করে লাইন থাকে এবং `Doc-tests adder` section শুরু হওয়ার ঠিক আগে integration test-এর ফলাফলের জন্য একটি সারসংক্ষেপ লাইন থাকে।

প্রতিটি integration test file-এর নিজস্ব section থাকে, তাই আমরা যদি _tests_ ডিরেক্টরিতে আরও file যোগ করি, তবে আরও integration test section থাকবে।

আমরা এখনো `cargo test`-কে argument হিসেবে test function-এর নাম উল্লেখ করে একটি নির্দিষ্ট integration test function চালাতে পারি। একটি নির্দিষ্ট integration test file-এর সব test চালাতে, `cargo test`-এর `--test` argument ব্যবহার করো এবং তারপর file-টির নাম লেখো:

```console
$ cargo test --test integration_test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.64s
     Running tests/integration_test.rs (target/debug/deps/integration_test-82e7799c1bc62298)

running 1 test
test it_adds_two ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

এই command শুধু _tests/integration_test.rs_ file-এর test-গুলো চালায়।

#### Integration Test-এ Submodule

তুমি যখন আরও integration test যোগ করবে, তখন সেগুলো সাজাতে _tests_ ডিরেক্টরিতে আরও file বানাতে চাইতে পারো; উদাহরণস্বরূপ, তুমি test function-গুলোকে সেগুলো যা test করছে তার functionality অনুযায়ী group করতে পারো। আগেই বলা হয়েছে, _tests_ ডিরেক্টরির প্রতিটি file তার নিজস্ব আলাদা crate হিসেবে compile হয়, যা আলাদা scope তৈরি করতে সহায়ক — যাতে end user তোমার crate যেভাবে ব্যবহার করবে তাকে আরও কাছাকাছি অনুকরণ করা যায়। তবে এর মানে হলো _tests_ ডিরেক্টরির file-গুলো _src_-এর file-গুলোর মতো একই আচরণ করে না, যেমনটা তুমি Chapter 7-এ code-কে module ও file-এ ভাগ করা শিখেছ।

_tests_ ডিরেক্টরির file-গুলোর ভিন্ন আচরণ সবচেয়ে লক্ষণীয় হয় যখন তোমার কাছে এমন কিছু helper function থাকে যেগুলো একাধিক integration test file-এ ব্যবহার করতে চাও, এবং তুমি Chapter 7-এর ["Separating Modules into Different Files"][separating-modules-into-files]<!-- ignore --> section-এর ধাপ অনুসরণ করে সেগুলোকে একটি common module-এ extract করার চেষ্টা করো। উদাহরণস্বরূপ, যদি আমরা _tests/common.rs_ তৈরি করি এবং এতে `setup` নামে একটি function রাখি, তাহলে আমরা `setup`-এ এমন কিছু code যোগ করতে পারি যেটি আমরা একাধিক test file-এর একাধিক test function থেকে call করতে চাই:

<span class="filename">Filename: tests/common.rs</span>

```rust,noplayground
pub fn setup() {
    // setup code specific to your library's tests would go here
}
```

যখন আমরা আবার test চালাব, আমরা test output-এ _common.rs_ file-এর জন্য একটি নতুন section দেখতে পাব, যদিও এই file-টিতে কোনো test function নেই এবং আমরা কোথাও থেকে `setup` function-কে call করিনি:

```console
$ cargo test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.89s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 1 test
test tests::internal ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running tests/common.rs (target/debug/deps/common-92948b65e88960b4)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running tests/integration_test.rs (target/debug/deps/integration_test-92948b65e88960b4)

running 1 test
test it_adds_two ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests adder

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

`common` test result-এ উপস্থিত হওয়া এবং তার জন্য `running 0 tests` প্রদর্শিত হওয়াটা আমাদের কাঙ্ক্ষিত ছিল না। আমরা শুধু অন্যান্য integration test file-গুলোর সাথে কিছু code share করতে চেয়েছিলাম। `common`-কে test output-এ উপস্থিত হওয়া থেকে রক্ষা করতে, _tests/common.rs_ তৈরি করার বদলে আমরা _tests/common/mod.rs_ তৈরি করব। Project ডিরেক্টরি এখন এমন দেখায়:

```text
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    ├── common
    │   └── mod.rs
    └── integration_test.rs
```

এটি Rust-এর সেই পুরোনো naming convention যা Rust বোঝে এবং যা আমরা Chapter 7-এর ["Alternate File Paths"][alt-paths]<!-- ignore --> section-এ উল্লেখ করেছি। File-টিকে এভাবে নামকরণ করলে Rust বোঝে যে `common` module-কে integration test file হিসেবে গণ্য করা উচিত নয়। যখন আমরা `setup` function-এর code _tests/common/mod.rs_-এ সরিয়ে দিই এবং _tests/common.rs_ file-টি মুছে ফেলি, তখন test output-এর সেই section আর উপস্থিত হবে না। _tests_ ডিরেক্টরির subdirectory-তে থাকা file-গুলো আলাদা crate হিসেবে compile হয় না বা test output-এ কোনো section থাকে না।

_tests/common/mod.rs_ তৈরি করার পর, আমরা যেকোনো integration test file থেকে এটিকে একটি module হিসেবে ব্যবহার করতে পারি। _tests/integration_test.rs_-এর `it_adds_two` test থেকে `setup` function-কে call করার একটি উদাহরণ নিচে দেওয়া হলো:

<span class="filename">Filename: tests/integration_test.rs</span>

```rust,ignore
use adder::add_two;

mod common;

#[test]
fn it_adds_two() {
    common::setup();

    let result = add_two(2);
    assert_eq!(result, 4);
}
```

খেয়াল করো যে `mod common;` declaration-টি Listing 7-21-তে আমরা যে module declaration দেখিয়েছিলাম তার মতোই। তারপর test function-এ আমরা `common::setup()` function-কে call করতে পারি।

#### Binary Crate-এর জন্য Integration Test

আমাদের project যদি এমন একটি binary crate হয় যাতে শুধু _src/main.rs_ file আছে এবং কোনো _src/lib.rs_ file নেই, তাহলে আমরা _tests_ ডিরেক্টরিতে integration test তৈরি করতে পারব না এবং _src/main.rs_ file-এ define করা function-গুলোকে `use` statement দিয়ে scope-এ আনতে পারব না। শুধুমাত্র library crate এমন function expose করে যা অন্যান্য crate ব্যবহার করতে পারে; binary crate নিজে নিজে চালানোর জন্য তৈরি।

Rust project-গুলো যেগুলো একটি binary সরবরাহ করে সেগুলোর একটি straightforward _src/main.rs_ file থাকে যা _src/lib.rs_ file-এ থাকা logic-কে call করে — এটি তার একটি কারণ। সেই structure ব্যবহার করলে, integration test গুরুত্বপূর্ণ functionality উপলব্ধ করতে `use` দিয়ে library crate-কে test করতে _পারে_। গুরুত্বপূর্ণ functionality কাজ করলে, _src/main.rs_ file-এর সামান্য code-টিও কাজ করবে, এবং সেই সামান্য code-টিকে test করার দরকার নেই।

## Summary

Rust-এর testing feature code কীভাবে কাজ করা উচিত তা নির্দিষ্ট করার একটি উপায় দেয় যাতে তুমি পরিবর্তন আনলেও code আশা অনুযায়ী কাজ করতে থাকে। Unit test একটি library-র বিভিন্ন অংশ আলাদাভাবে exercise করে এবং private implementation detail test করতে পারে। Integration test যাচাই করে যে library-র অনেকগুলো অংশ একসাথে সঠিকভাবে কাজ করে, এবং সেগুলো external code যেভাবে ব্যবহার করবে সেভাবে library-র public API ব্যবহার করে code test করে। যদিও Rust-এর type system ও ownership rule কিছু ধরনের bug প্রতিরোধে সাহায্য করে, তবুও তোমার code-এর প্রত্যাশিত আচরণ সম্পর্কিত logic bug কমাতে test-গুলো গুরুত্বপূর্ণ।

চলো এই chapter-এ এবং পূর্ববর্তী chapter-গুলোতে তুমি যা শিখেছ তা একত্রিত করে একটি project নিয়ে কাজ করি!

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
[separating-modules-into-files]: ch07-05-separating-modules-into-different-files.html
[alt-paths]: ch07-05-separating-modules-into-different-files.html#alternate-file-paths

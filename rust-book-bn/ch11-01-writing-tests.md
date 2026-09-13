## How to Write Tests

_Test_ হলো Rust function যেগুলো যাচাই করে যে non-test code-টি প্রত্যাশিতভাবে কাজ করছে। Test function-গুলোর body সাধারণত এই তিনটি কাজ করে:

- প্রয়োজনীয় data বা state সেট আপ করা।
- যেই code টেস্ট করতে চাও সেটি চালানো।
- ফলাফল প্রত্যাশিত কিনা তা assert করা।

চলো দেখি Rust এই কাজগুলো করার জন্য test লেখার ক্ষেত্রে ঠিক কী সুবিধা দেয় — যার মধ্যে আছে `test` attribute, কয়েকটি macro, এবং `should_panic` attribute।

<!-- Old headings. Do not remove or links may break. -->

<a id="the-anatomy-of-a-test-function"></a>

### Test Function-গুলোর গঠন

সবচেয়ে সহজভাবে বলতে গেলে, Rust-এ একটি test হলো এমন একটি function যাতে `test` attribute যুক্ত করা থাকে। Attribute হলো Rust code-এর অংশগুলো সম্পর্কে metadata; এর একটি উদাহরণ হলো `derive` attribute, যা আমরা Chapter 5-এ struct-এর সাথে ব্যবহার করেছি। একটি function-কে test function-এ পরিণত করতে `fn`-এর আগের লাইনে `#[test]` যোগ করো। যখন তুমি `cargo test` command দিয়ে তোমার test-গুলো চালাও, Rust একটি test runner binary তৈরি করে যেটি annotated function-গুলো চালায় এবং প্রতিটি test function pass করেছে নাকি fail করেছে তা রিপোর্ট করে।

Cargo দিয়ে নতুন library project তৈরি করলে আমাদের জন্য স্বয়ংক্রিয়ভাবে একটি test module তৈরি হয়ে যায় যার ভেতরে একটি test function থাকে। এই module তোমাকে test লেখার একটি template দেয়, যাতে প্রতিবার নতুন project শুরু করার সময় তোমাকে সঠিক structure ও syntax খুঁজে বের করতে না হয়। তুমি যত খুশি অতিরিক্ত test function এবং test module যোগ করতে পারো!

প্রথমে আমরা template test-টিকে নিয়ে পরীক্ষা-নিরীক্ষা করে দেখব কীভাবে test কাজ করে, এরপর আসল code টেস্ট করব। তারপর আমরা কিছু বাস্তব test লিখব যেগুলো আমাদের লেখা কোনো code-কে call করবে এবং তার আচরণ সঠিক কিনা তা assert করবে।

চলো `adder` নামে একটি নতুন library project তৈরি করি যেটি দুটি সংখ্যা যোগ করবে:

```console
$ cargo new adder --lib
     Created library `adder` project
$ cd adder
```

তোমার `adder` library-এর _src/lib.rs_ file-এর content Listing 11-1-এর মতো দেখাবে।

<Listing number="11-1" file-name="src/lib.rs" caption="The code generated automatically by `cargo new`">

<!-- manual-regeneration
cd listings/ch11-writing-automated-tests
rm -rf listing-11-01
cargo new listing-11-01 --lib --name adder
cd listing-11-01
echo "$ cargo test" > output.txt
RUSTFLAGS="-A unused_variables -A dead_code" RUST_TEST_THREADS=1 cargo test >> output.txt 2>&1
git diff output.txt # commit any relevant changes; discard irrelevant ones
cd ../../..
-->

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

</Listing>

File-টি একটি উদাহরণ `add` function দিয়ে শুরু হয়েছে যাতে আমাদের টেস্ট করার মতো কিছু থাকে।

আপাতত চলো শুধু `it_works` function-টির দিকে মনোযোগ দিই। `#[test]` annotation-টি খেয়াল করো: এই attribute নির্দেশ করে যে এটি একটি test function, তাই test runner জানবে এই function-টিকে test হিসেবে গণ্য করতে হবে। `tests` module-এ আমাদের non-test function-ও থাকতে পারে যেগুলো সাধারণ scenario সেট আপ করতে বা সাধারণ কাজ করতে সাহায্য করে, তাই কোন কোন function test সেটা আমাদের সবসময় নির্দেশ করতে হবে।

উদাহরণের function body-তে `assert_eq!` macro ব্যবহার করা হয়েছে যাতে assert করা যায় যে `result` — যেটিতে `add`-কে 2 ও 2 দিয়ে call করার ফল রয়েছে — সেটি 4-এর সমান। এই assertion একটি সাধারণ test-এর ফরম্যাটের উদাহরণ হিসেবে কাজ করে। চলো এটি চালাই দেখি এই test-টি pass করে কিনা।

`cargo test` command আমাদের project-এর সব test চালায়, যেমনটা Listing 11-2-তে দেখানো হয়েছে।

<Listing number="11-2" caption="The output from running the automatically generated test">

```console
$ cargo test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.57s
     Running unittests src/lib.rs (target/debug/deps/adder-01ad14159ff659ab)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests adder

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

</Listing>

Cargo test-টি compile ও চালিয়েছে। আমরা `running 1 test` লাইনটি দেখতে পাচ্ছি। পরের লাইনে তৈরি হওয়া test function-এর নাম — `tests::it_works` — দেখানো হয়েছে, এবং ওই test-টি চালানোর ফল `ok`। সামগ্রিক সারসংক্ষেপ `test result: ok.` মানে হলো সব test pass করেছে, এবং যে অংশটি `1 passed; 0 failed` লেখা, সেটি pass বা fail হওয়া test-এর সংখ্যা জোড়ে বোঝায়।

একটি test-কে ignored হিসেবে চিহ্নিত করা সম্ভব যাতে সেটি কোনো নির্দিষ্ট ক্ষেত্রে না চলে; এই chapter-এ পরে আমরা সেটি ["Ignoring Tests Unless Specifically Requested"][ignoring]<!-- ignore --> section-এ নিয়ে আলোচনা করব। যেহেতু আমরা এখানে সেটি করিনি, সারসংক্ষেপে `0 ignored` দেখাচ্ছে। আমরা `cargo test` command-কে এমন একটি argument-ও পাস করতে পারি যাতে শুধু সেই সব test চলে যাদের নাম কোনো string-এর সাথে মেলে; একে _filtering_ বলা হয় এবং আমরা এ সম্পর্কে ["Running a Subset of Tests by Name"][subset]<!-- ignore --> section-এ আলোচনা করব। এখানে আমরা চলমান test-গুলোকে filter করিনি, তাই সারসংক্ষেপের শেষে `0 filtered out` দেখাচ্ছে।

`0 measured` পরিসংখ্যানটি performance পরিমাপ করে এমন benchmark test-এর জন্য। এই লেখা পর্যন্ত অবধি benchmark test শুধুমাত্র nightly Rust-এ পাওয়া যায়। আরও জানতে [the documentation about benchmark tests][bench] দেখো।

`Doc-tests adder` থেকে শুরু হওয়া test output-এর পরের অংশটি documentation test-গুলোর ফলাফলের জন্য। আমাদের এখনো কোনো documentation test নেই, তবে Rust আমাদের API documentation-এ থাকা যেকোনো code উদাহরণ compile করতে পারে। এই সুবিধাটি তোমার docs ও code-কে sync রাখতে সাহায্য করে! Documentation test কীভাবে লিখতে হয় তা আমরা Chapter 14-এর ["Documentation Comments as Tests"][doc-comments]<!-- ignore --> section-এ আলোচনা করব। আপাতত, আমরা `Doc-tests` output-টি উপেক্ষা করব।

চলো এবার test-টিকে আমাদের নিজস্ব প্রয়োজন অনুযায়ী customize করা শুরু করি। প্রথমে `it_works` function-টির নাম অন্য নামে পরিবর্তন করো, যেমন `exploration`, এভাবে:

<span class="filename">Filename: src/lib.rs</span>

```rust,noplayground
pub fn add(left: u64, right: u64) -> u64 {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn exploration() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
```

এরপর আবার `cargo test` চালাও। এবার output-এ `it_works`-এর বদলে `exploration` দেখাবে:

```console
$ cargo test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.59s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 1 test
test tests::exploration ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests adder

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

এখন আমরা আরেকটি test যোগ করব, কিন্তু এবার এমন একটি test যেটি fail করবে! Test function-এর ভেতরে কিছু panic করলে test fail করে। প্রতিটি test একটি নতুন thread-এ চলে, এবং যখন main thread দেখে যে একটি test thread মারা গেছে, তখন সেই test-টিকে failed হিসেবে চিহ্নিত করা হয়। Chapter 9-এ আমরা আলোচনা করেছি যে panic করার সবচেয়ে সহজ উপায় হলো `panic!` macro-কে call করা। নতুন test-টি `another` নামের একটি function হিসেবে লেখো, যাতে তোমার _src/lib.rs_ file-টি Listing 11-3-এর মতো দেখায়।

<Listing number="11-3" file-name="src/lib.rs" caption="Adding a second test that will fail because we call the `panic!` macro">

```rust,panics,noplayground
pub fn add(left: u64, right: u64) -> u64 {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn exploration() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }

    #[test]
    fn another() {
        panic!("Make this test fail");
    }
}
```

</Listing>

আবার `cargo test` দিয়ে test-গুলো চালাও। Output Listing 11-4-এর মতো হওয়া উচিত, যেখানে দেখা যাচ্ছে যে আমাদের `exploration` test pass করেছে এবং `another` fail করেছে।

<Listing number="11-4" caption="Test results when one test passes and one test fails">

```console
$ cargo test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.72s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 2 tests
test tests::another ... FAILED
test tests::exploration ... ok

failures:

---- tests::another stdout ----

thread 'tests::another' (6019162) panicked at src/lib.rs:17:9:
Make this test fail
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    tests::another

test result: FAILED. 1 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

</Listing>

<!-- manual-regeneration
rg panicked listings/ch11-writing-automated-tests/listing-11-03/output.txt
check the line number of the panic matches the line number in the following paragraph
 -->

`ok`-এর বদলে `test tests::another` লাইনে `FAILED` দেখাচ্ছে। পৃথক test-এর ফল ও সারসংক্ষেপের মাঝে দুটি নতুন section উপস্থিত হয়েছে: প্রথমটিতে প্রতিটি test failure-এর বিস্তারিত কারণ দেখানো হয়। এই ক্ষেত্রে, আমরা বিস্তারিত পাই যে `tests::another` কেন fail করেছে — কারণ এটি _src/lib.rs_ file-এর 17 নম্বর লাইনে `Make this test fail` মেসেজ দিয়ে panic করেছে। পরের section-টিতে শুধু সব fail হওয়া test-গুলোর নাম তালিকাভুক্ত করা হয়, যা তখন কাজে দেয় যখন অনেক test থাকে এবং fail হওয়া test-এর বিস্তারিত output অনেক বড় হয়। আমরা fail হওয়া কোনো test-এর নাম ব্যবহার করে শুধু সেই test-টি চালাতে পারি যাতে সহজে debug করা যায়; test চালানোর আরও উপায় নিয়ে আমরা ["Controlling How Tests Are Run"][controlling-how-tests-are-run]<!-- ignore --> section-ে আরও কথা বলব।

সারসংক্ষেপের লাইনটি শেষে দেখা যায়: সামগ্রিকভাবে, আমাদের test result `FAILED`। আমাদের একটি test pass করেছে এবং একটি fail করেছে।

যেহেতু এখন তুমি বিভিন্ন পরিস্থিতিতে test result কেমন দেখায় তা দেখেছ, চলো `panic!` ছাড়াও test-এ কাজে লাগে এমন আরও কিছু macro দেখি।

<!-- Old headings. Do not remove or links may break. -->

<a id="checking-results-with-the-assert-macro"></a>

### `assert!` দিয়ে Result যাচাই করা

Standard library থেকে পাওয়া `assert!` macro তখন কাজে লাগে যখন তুমি নিশ্চিত করতে চাও যে কোনো test-এর কোনো condition `true` হিসেবে মূল্যায়িত হয়েছে। আমরা `assert!` macro-কে এমন একটি argument দিই যা একটি Boolean-এ মূল্যায়িত হয়। যদি value-টি `true` হয়, কিছুই ঘটে না এবং test pass করে। যদি value-টি `false` হয়, তাহলে `assert!` macro `panic!`-কে call করে যাতে test fail করে। `assert!` macro ব্যবহার করা আমাদের code-টি আমাদের ইচ্ছামতো কাজ করছে কিনা তা যাচাই করতে সাহায্য করে।

Chapter 5-এর Listing 5-15-এ আমরা একটি `Rectangle` struct এবং একটি `can_hold` method ব্যবহার করেছিলাম, যেগুলো এখানে Listing 11-5-এ আবার দেওয়া হলো। চলো এই code-টিকে _src/lib.rs_ file-এ রাখি, তারপর `assert!` macro ব্যবহার করে এর জন্য কিছু test লিখি।

<Listing number="11-5" file-name="src/lib.rs" caption="The `Rectangle` struct and its `can_hold` method from Chapter 5">

```rust,noplayground
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }
}
```

</Listing>

`can_hold` method একটি Boolean ফেরত দেয়, যার মানে হলো এটি `assert!` macro-এর জন্য একটি নিখুঁত use case। Listing 11-6-তে আমরা এমন একটি test লিখি যেটি `can_hold` method-টিকে ব্যবহার করে — 8 প্রস্থ ও 7 উচ্চতার একটি `Rectangle` instance তৈরি করে এবং assert করে যে এটি 5 প্রস্থ ও 1 উচ্চতার অন্য একটি `Rectangle` instance-কে ধারণ করতে পারে।

<Listing number="11-6" file-name="src/lib.rs" caption="A test for `can_hold` that checks whether a larger rectangle can indeed hold a smaller rectangle">

```rust,noplayground
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn larger_can_hold_smaller() {
        let larger = Rectangle {
            width: 8,
            height: 7,
        };
        let smaller = Rectangle {
            width: 5,
            height: 1,
        };

        assert!(larger.can_hold(&smaller));
    }
}
```

</Listing>

`tests` module-এর ভেতরে `use super::*;` লাইনটি খেয়াল করো। `tests` module একটি সাধারণ module, যা Chapter 7-এর ["Paths for Referring to an Item in the Module Tree"][paths-for-referring-to-an-item-in-the-module-tree]<!-- ignore --> section-এ আলোচিত স্বাভাবিক visibility নিয়ম মেনে চলে। যেহেতু `tests` module একটি inner module, আমাদের outer module-এ থাকা test করার উদ্দেশ্যে code-টিকে inner module-এর scope-এ নিয়ে আসতে হবে। আমরা এখানে একটি glob ব্যবহার করেছি, তাই outer module-এ আমরা যা কিছু define করেছি তা এই `tests` module-এ পাওয়া যায়।

আমরা আমাদের test-এর নাম `larger_can_hold_smaller` দিয়েছি এবং আমাদের দরকারি দুটি `Rectangle` instance তৈরি করেছি। তারপর আমরা `assert!` macro-কে call করে এতে `larger.can_hold(&smaller)` call করার ফল পাস করেছি। এই expression-টি `true` ফেরত দেওয়ার কথা, তাই আমাদের test pass করা উচিত। চলো দেখি হয় কিনা!

```console
$ cargo test
   Compiling rectangle v0.1.0 (file:///projects/rectangle)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.66s
     Running unittests src/lib.rs (target/debug/deps/rectangle-6584c4561e48942e)

running 1 test
test tests::larger_can_hold_smaller ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests rectangle

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

হ্যাঁ, এটি pass করেছে! চলো আরেকটি test যোগ করি, এবার assert করি যে একটি ছোট rectangle একটি বড় rectangle-কে ধারণ করতে পারে না:

<span class="filename">Filename: src/lib.rs</span>

```rust,noplayground
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn larger_can_hold_smaller() {
        // --snip--
    }

    #[test]
    fn smaller_cannot_hold_larger() {
        let larger = Rectangle {
            width: 8,
            height: 7,
        };
        let smaller = Rectangle {
            width: 5,
            height: 1,
        };

        assert!(!smaller.can_hold(&larger));
    }
}
```

যেহেতু এই ক্ষেত্রে `can_hold` function-এর সঠিক ফল `false`, আমাদের এই ফলটিকে `assert!` macro-তে পাস করার আগে negate করতে হবে। ফলস্বরূপ, `can_hold` যদি `false` ফেরত দেয় তাহলে আমাদের test pass করবে:

```console
$ cargo test
   Compiling rectangle v0.1.0 (file:///projects/rectangle)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.66s
     Running unittests src/lib.rs (target/debug/deps/rectangle-6584c4561e48942e)

running 2 tests
test tests::larger_can_hold_smaller ... ok
test tests::smaller_cannot_hold_larger ... ok

test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests rectangle

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

দুটি test pass করেছে! এখন দেখি আমাদের code-এ একটি bug ঢুকিয়ে দিলে test result-এ কী হয়। আমরা `can_hold` method-এর implementation পরিবর্তন করব width তুলনা করার সময় greater-than চিহ্ন (`>`) কে less-than চিহ্ন (`<`) দিয়ে প্রতিস্থাপন করে:

```rust,not_desired_behavior,noplayground
// --snip--
impl Rectangle {
    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width < other.width && self.height > other.height
    }
}
```

এখন test চালালে নিচের ফল পাওয়া যায়:

```console
$ cargo test
   Compiling rectangle v0.1.0 (file:///projects/rectangle)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.66s
     Running unittests src/lib.rs (target/debug/deps/rectangle-6584c4561e48942e)

running 2 tests
test tests::larger_can_hold_smaller ... FAILED
test tests::smaller_cannot_hold_larger ... ok

failures:

---- tests::larger_can_hold_smaller stdout ----

thread 'tests::larger_can_hold_smaller' (6020788) panicked at src/lib.rs:28:9:
assertion failed: larger.can_hold(&smaller)
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    tests::larger_can_hold_smaller

test result: FAILED. 1 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

আমাদের test-গুলো bug ধরে ফেলেছে! যেহেতু `larger.width` হলো `8` এবং `smaller.width` হলো `5`, `can_hold`-এ width তুলনা এখন `false` ফেরত দেয়: 8 কখনো 5-এর কম নয়।

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-equality-with-the-assert_eq-and-assert_ne-macros"></a>

### `assert_eq!` এবং `assert_ne!` Macro দিয়ে Equality যাচাই করা

কার্যকারিতা যাচাই করার একটি সাধারণ উপায় হলো টেস্ট করা যে code-এর ফল ও code-টি যা ফেরত দেওয়ার কথা তার মধ্যে equality আছে কিনা। তুমি এটি `assert!` macro ব্যবহার করে করতে পারো এবং এতে `==` operator ব্যবহার করে একটি expression পাস করতে পারো। তবে এটি এত সাধারণ একটি test যে standard library এই test সুবিধার জন্য macro-গুলোর একটি জোড়া সরবরাহ করে — `assert_eq!` এবং `assert_ne!`। এই macro-গুলো যথাক্রমে দুটি argument-এর equality বা inequality যাচাই করে। এগুলো assertion fail হলে দুটি value-ই print করে, যার ফলে বোঝা সহজ হয় কেন test fail করেছে; অন্যদিকে `assert!` macro শুধু নির্দেশ করে যে `==` expression-এর জন্য সে একটি `false` value পেয়েছে, কিন্তু যে value-গুলো এই `false` ফল এনে দিয়েছে সেগুলো print করে না।

Listing 11-7-তে আমরা `add_two` নামে একটি function লিখি যেটি তার parameter-এর সাথে `2` যোগ করে, এবং তারপর আমরা এই function-টিকে `assert_eq!` macro ব্যবহার করে test করি।

<Listing number="11-7" file-name="src/lib.rs" caption="Testing the function `add_two` using the `assert_eq!` macro">

```rust,noplayground
pub fn add_two(a: u64) -> u64 {
    a + 2
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_adds_two() {
        let result = add_two(2);
        assert_eq!(result, 4);
    }
}
```

</Listing>

চলো দেখি এটি pass করে কিনা!

```console
$ cargo test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.58s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 1 test
test tests::it_adds_two ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests adder

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

আমরা `result` নামে একটি variable তৈরি করি যেটিতে `add_two(2)` call করার ফল থাকে। তারপর আমরা `result` এবং `4` কে `assert_eq!` macro-তে argument হিসেবে পাস করি। এই test-এর output লাইনটি হলো `test tests::it_adds_two ... ok`, এবং `ok` text-টি নির্দেশ করে যে আমাদের test pass করেছে!

চলো আমাদের code-এ একটি bug ঢুকিয়ে দেখি `assert_eq!` fail করলে কেমন দেখায়। `add_two` function-এর implementation পরিবর্তন করে এমনভাবে করো যাতে সেটি বরং `3` যোগ করে:

```rust,not_desired_behavior,noplayground
pub fn add_two(a: u64) -> u64 {
    a + 3
}
```

আবার test চালাও:

```console
$ cargo test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.61s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 1 test
test tests::it_adds_two ... FAILED

failures:

---- tests::it_adds_two stdout ----

thread 'tests::it_adds_two' (6020955) panicked at src/lib.rs:12:9:
assertion `left == right` failed
  left: 5
 right: 4
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    tests::it_adds_two

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

আমাদের test বাগ ধরে ফেলেছে! `tests::it_adds_two` test-টি fail করেছে এবং বার্তাটি আমাদের জানায় যে যে assertion-টি fail করেছে সেটি হলো `left == right` এবং `left` ও `right` value-গুলো কী কী। এই বার্তাটি আমাদের debug করা শুরু করতে সাহায্য করে: `left` argument — যেখানে `add_two(2)` call করার ফল ছিল — ছিল `5`, কিন্তু `right` argument ছিল `4`। তুমি কল্পনা করতে পারো যে যখন অনেকগুলো test একসাথে চলছে, তখন এটি বিশেষভাবে সাহায্যকারী হবে।

খেয়াল করো যে কিছু ভাষা ও test framework-এ equality assertion function-গুলোর parameter-গুলোকে `expected` ও `actual` বলা হয়, এবং আমরা argument যে ক্রমে উল্লেখ করি সেটি গুরুত্বপূর্ণ। কিন্তু Rust-এ সেগুলোকে `left` এবং `right` বলা হয়, এবং আমরা যে value আশা করি এবং code যে value তৈরি করে সেগুলো যে ক্রমে উল্লেখ করি তা গুরুত্বপূর্ণ নয়। আমরা এই test-এর assertion-টিকে `assert_eq!(4, result)` হিসেবে লিখতে পারতাম, যার ফলে একই failure বার্তা আসত যেটি `` assertion `left == right` failed `` প্রদর্শন করে।

`assert_ne!` macro পাস করবে যদি আমরা যে দুটি value দিই সেগুলো সমান না হয়, এবং fail করবে যদি সেগুলো সমান হয়। এই macro সবচেয়ে বেশি কাজে লাগে এমন ক্ষেত্রে যখন আমরা নিশ্চিত নই যে একটি value ঠিক কী _হবে_, কিন্তু আমরা জানি যে সেই value-টি নিশ্চিতভাবে কী _হওয়া উচিত নয়_। উদাহরণস্বরূপ, যদি আমরা এমন একটি function test করি যেটি তার input কোনো না কোনোভাবে পরিবর্তন করার গ্যারান্টি দেয়, কিন্তু input যেভাবে পরিবর্তিত হবে তা নির্ভর করে আমরা কোন সপ্তাহের দিনে test চালাই তার ওপর, তাহলে সবচেয়ে ভালো assert করার বিষয় হতে পারে যে function-এর output তার input-এর সমান নয়।

ভেতরের দিকে `assert_eq!` এবং `assert_ne!` macro যথাক্রমে `==` এবং `!=` operator ব্যবহার করে। যখন assertion-গুলো fail করে, এই macro-গুলো debug formatting ব্যবহার করে তাদের argument print করে, যার মানে তুলনা করা value-গুলোকে অবশ্যই `PartialEq` এবং `Debug` trait implement করতে হবে। সব primitive type এবং standard library-র বেশিরভাগ type এই trait-গুলো implement করে। তোমার নিজের define করা struct এবং enum-এর জন্য তুমি এই ধরনের type-এর equality assert করতে `PartialEq` implement করতে হবে। assertion fail করলে value-গুলো print করার জন্য তোমাকে `Debug`-ও implement করতে হবে। যেহেতু দুটি trait-ই derivable trait, যেমনটা Chapter 5-এর Listing 5-12-তে উল্লেখ করা হয়েছে, তাই সাধারণত এটি তোমার struct বা enum definition-এ `#[derive(PartialEq, Debug)]` annotation যোগ করার মতোই সহজ। এই এবং অন্যান্য derivable trait সম্পর্কে আরও বিস্তারিত জানতে Appendix C-এর ["Derivable Traits,"][derivable-traits]<!-- ignore --> দেখো।

### Custom Failure Message যোগ করা

তুমি `assert!`, `assert_eq!`, এবং `assert_ne!` macro-গুলোতে optional argument হিসেবে একটি custom message যোগ করতে পারো যেটি failure বার্তার সাথে print হবে। প্রয়োজনীয় argument-গুলোর পরে উল্লেখ করা যেকোনো argument `format!` macro-তে পাস করা হয় (Chapter 8-এর [`+` বা `format!` দিয়ে Concatenating][concatenating]<!-- ignore --> section-এ আলোচনা করা হয়েছে), তাই তুমি `{}` placeholder যুক্ত একটি format string এবং সেই placeholder-গুলোতে বসানোর মতো value পাস করতে পারো। Custom message একটি assertion-এর অর্থ নথিভুক্ত করতে কাজে লাগে; যখন একটি test fail করে, তখন তোমার কাছে code-এ সমস্যাটি কী সে সম্পর্কে একটি ভালো ধারণা থাকবে।

উদাহরণস্বরূপ, ধরো আমাদের এমন একটি function আছে যেটি নাম ধরে মানুষকে অভিবাদন জানায় এবং আমরা test করতে চাই যে function-এ যে নামটি পাস করা হয়েছে সেটি output-এ দেখা যাচ্ছে কিনা:

<span class="filename">Filename: src/lib.rs</span>

```rust,noplayground
pub fn greeting(name: &str) -> String {
    format!("Hello {name}!")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn greeting_contains_name() {
        let result = greeting("Carol");
        assert!(result.contains("Carol"));
    }
}
```

এই program-টির requirement-গুলো এখনো চূড়ান্ত হয়নি, এবং আমরা বেশ নিশ্চিত যে greeting-এর শুরুতে থাকা `Hello` text-টি পরিবর্তিত হবে। আমরা সিদ্ধান্ত নিলাম যে প্রয়োজন পরিবর্তিত হলে আমরা test আপডেট করতে চাই না, তাই `greeting` function থেকে ফেরত আসা value-র সাথে সম্পূর্ণ equality যাচাই করার বদলে আমরা শুধু assert করব যে output-এ input parameter-এর text আছে।

এখন চলো এই code-এ একটি bug ঢুকিয়ে দেই `greeting` থেকে `name` বাদ দিয়ে, দেখি default test failure কেমন দেখায়:

```rust,not_desired_behavior,noplayground
pub fn greeting(name: &str) -> String {
    String::from("Hello!")
}
```

এই test চালালে নিচের ফল পাওয়া যায়:

```console
$ cargo test
   Compiling greeter v0.1.0 (file:///projects/greeter)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.91s
     Running unittests src/lib.rs (target/debug/deps/greeter-170b942eb5bf5e3a)

running 1 test
test tests::greeting_contains_name ... FAILED

failures:

---- tests::greeting_contains_name stdout ----

thread 'tests::greeting_contains_name' (6021143) panicked at src/lib.rs:12:9:
assertion failed: result.contains("Carol")
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    tests::greeting_contains_name

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

এই ফল শুধু নির্দেশ করে যে assertion fail করেছে এবং assertion-টি কোন লাইনে আছে। একটি বেশি কার্যকর failure বার্তা `greeting` function থেকে পাওয়া value print করবে। চলো একটি custom failure message যোগ করি — একটি format string যার ভেতরে একটি placeholder থাকবে যেটি `greeting` function থেকে প্রকৃতপক্ষে পাওয়া value দিয়ে পূরণ হবে:

```rust,ignore
    #[test]
    fn greeting_contains_name() {
        let result = greeting("Carol");
        assert!(
            result.contains("Carol"),
            "Greeting did not contain name, value was `{result}`"
        );
    }
```

এখন যখন আমরা test চালাব, আমরা একটি অধিক তথ্যপূর্ণ error বার্তা পাব:

```console
$ cargo test
   Compiling greeter v0.1.0 (file:///projects/greeter)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.93s
     Running unittests src/lib.rs (target/debug/deps/greeter-170b942eb5bf5e3a)

running 1 test
test tests::greeting_contains_name ... FAILED

failures:

---- tests::greeting_contains_name stdout ----

thread 'tests::greeting_contains_name' (6021333) panicked at src/lib.rs:12:9:
Greeting did not contain name, value was `Hello!`
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    tests::greeting_contains_name

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

আমরা test output-এ প্রকৃতপক্ষে যে value পেয়েছি তা দেখতে পাচ্ছি, যা আমাদের কী ঘটেছিল তা debug করতে সাহায্য করবে — যেখানে আমরা আশা করছিলাম অন্য কিছু ঘটবে।

### `should_panic` দিয়ে Panic যাচাই করা

return value যাচাই করার পাশাপাশি, এটাও গুরুত্বপূর্ণ যাচাই করা যে আমাদের code error condition-গুলো আমাদের প্রত্যাশা অনুযায়ী handle করে। উদাহরণস্বরূপ, Chapter 9-এর Listing 9-13-এ আমরা যে `Guess` type তৈরি করেছিলাম সেটা বিবেচনা করো। `Guess` ব্যবহার করে এমন অন্যান্য code নির্ভর করে এই গ্যারান্টির ওপর যে `Guess` instance-গুলো শুধুমাত্র 1 থেকে 100-এর মধ্যে value ধারণ করবে। আমরা এমন একটি test লিখতে পারি যেটা নিশ্চিত করে যে সেই range-এর বাইরের কোনো value দিয়ে `Guess` instance তৈরি করার চেষ্টা করলে panic হয়।

আমরা এটি করি আমাদের test function-এ `should_panic` attribute যোগ করে। function-টির ভেতরের code panic করলে test pass করে; function-টির ভেতরের code panic না করলে test fail করে।

Listing 11-8-তে এমন একটি test দেখানো হয়েছে যেটি যাচাই করে যে `Guess::new`-এর error condition-গুলো আমাদের প্রত্যাশিত সময়ে ঘটে।

<Listing number="11-8" file-name="src/lib.rs" caption="Testing that a condition will cause a `panic!`">

```rust,noplayground
pub struct Guess {
    value: i32,
}

impl Guess {
    pub fn new(value: i32) -> Guess {
        if value < 1 || value > 100 {
            panic!("Guess value must be between 1 and 100, got {value}.");
        }

        Guess { value }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[should_panic]
    fn greater_than_100() {
        Guess::new(200);
    }
}
```

</Listing>

আমরা `#[should_panic]` attribute-টিকে `#[test]` attribute-এর পরে এবং যে test function-এ এটি প্রযোজ্য সেটির আগে রাখি। চলো দেখি এই test pass করলে ফল কেমন হয়:

```console
$ cargo test
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.58s
     Running unittests src/lib.rs (target/debug/deps/guessing_game-57d70c3acb738f4d)

running 1 test
test tests::greater_than_100 - should panic ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests guessing_game

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

বেশ ভালো! এখন চলো আমাদের code-এ একটি bug ঢুকিয়ে দেই value 100-এর বেশি হলে `new` function যে panic করবে সেই শর্তটি সরিয়ে:

```rust,not_desired_behavior,noplayground
// --snip--
impl Guess {
    pub fn new(value: i32) -> Guess {
        if value < 1 {
            panic!("Guess value must be between 1 and 100, got {value}.");
        }

        Guess { value }
    }
}
```

যখন আমরা Listing 11-8-এর test-টি চালাব, এটি fail করবে:

```console
$ cargo test
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.62s
     Running unittests src/lib.rs (target/debug/deps/guessing_game-57d70c3acb738f4d)

running 1 test
test tests::greater_than_100 - should panic ... FAILED

failures:

---- tests::greater_than_100 stdout ----
note: test did not panic as expected at src/lib.rs:21:8

failures:
    tests::greater_than_100

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

এই ক্ষেত্রে আমরা খুব সহায়ক বার্তা পাই না, কিন্তু test function-টির দিকে তাকালে আমরা দেখি এটি `#[should_panic]` দিয়ে annotated। আমরা যে failure পেয়েছি তার মানে হলো test function-এর code কোনো panic ঘটায়নি।

`should_panic` ব্যবহার করে এমন test অসুনির্দিষ্ট হতে পারে। একটি `should_panic` test তখনও pass করবে যদি test আমাদের প্রত্যাশিত কারণ ছাড়া অন্য কোনো কারণে panic করে। `should_panic` test-গুলোকে আরও সুনির্দিষ্ট করতে আমরা `should_panic` attribute-এ একটি optional `expected` parameter যোগ করতে পারি। test harness নিশ্চিত করবে যে failure বার্তাটি প্রদত্ত text ধারণ করছে। উদাহরণস্বরূপ, Listing 11-9-তে `Guess`-এর পরিবর্তিত code বিবেচনা করো যেখানে `new` function value খুব ছোট নাকি খুব বড় তার ওপর ভিত্তি করে আলাদা বার্তা দিয়ে panic করে।

<Listing number="11-9" file-name="src/lib.rs" caption="Testing for a `panic!` with a panic message containing a specified substring">

```rust,noplayground
// --snip--

impl Guess {
    pub fn new(value: i32) -> Guess {
        if value < 1 {
            panic!(
                "Guess value must be greater than or equal to 1, got {value}."
            );
        } else if value > 100 {
            panic!(
                "Guess value must be less than or equal to 100, got {value}."
            );
        }

        Guess { value }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[should_panic(expected = "less than or equal to 100")]
    fn greater_than_100() {
        Guess::new(200);
    }
}
```

</Listing>

এই test-টি pass করবে কারণ আমরা `should_panic` attribute-এর `expected` parameter-এ যে value দিয়েছি তা `Guess::new` function যে বার্তা দিয়ে panic করে তার একটি অংশ। আমরা প্রত্যাশিত সম্পূর্ণ panic বার্তাটিও উল্লেখ করতে পারতাম, যা এই ক্ষেত্রে হতো `Guess value must be less than or equal to 100, got 200`। তুমি কী উল্লেখ করবে তা নির্ভর করে কতটা unique বা dynamic panic বার্তাটি এবং তোমার test কতটা সুনির্দিষ্ট হবে তার ওপর। এই ক্ষেত্রে, panic বার্তার একটি অংশ test function-এর code যে `else if value > 100` case execute করে তা নিশ্চিত করতে যথেষ্ট।

`expected` বার্তা যুক্ত একটি `should_panic` test fail করলে কী হয় দেখতে, চলো আবার আমাদের code-এ একটি bug ঢুকিয়ে দিই `if value < 1` এবং `else if value > 100` block-গুলোর body অদলবদল করে:

```rust,ignore,not_desired_behavior
        if value < 1 {
            panic!(
                "Guess value must be less than or equal to 100, got {value}."
            );
        } else if value > 100 {
            panic!(
                "Guess value must be greater than or equal to 1, got {value}."
            );
        }
```

এবার যখন আমরা `should_panic` test চালাব, এটি fail করবে:

```console
$ cargo test
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.66s
     Running unittests src/lib.rs (target/debug/deps/guessing_game-57d70c3acb738f4d)

running 1 test
test tests::greater_than_100 - should panic ... FAILED

failures:

---- tests::greater_than_100 stdout ----

thread 'tests::greater_than_100' (6021675) panicked at src/lib.rs:12:13:
Guess value must be greater than or equal to 1, got 200.
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
note: panic did not contain expected string
      panic message: "Guess value must be greater than or equal to 1, got 200."
 expected substring: "less than or equal to 100"

failures:
    tests::greater_than_100

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

Failure বার্তাটি নির্দেশ করে যে এই test সত্যিই আমাদের প্রত্যাশা অনুযায়ী panic করেছে, কিন্তু panic বার্তাটি প্রত্যাশিত string `less than or equal to 100` ধারণ করছে না। এই ক্ষেত্রে আমরা যে panic বার্তা পেয়েছি তা হলো `Guess value must be greater than or equal to 1, got 200`। এখন আমরা বুঝতে পারছি আমাদের bug কোথায়!

### Test-এ `Result<T, E>` ব্যবহার করা

এ পর্যন্ত আমাদের সব test fail হলে panic করে। আমরা এমন test-ও লিখতে পারি যেগুলো `Result<T, E>` ব্যবহার করে! নিচে Listing 11-1-এর test-টিকে এমনভাবে পুনরায় লেখা হলো যাতে সেটি `Result<T, E>` ব্যবহার করে এবং panic করার বদলে একটি `Err` ফেরত দেয়:

```rust,noplayground
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() -> Result<(), String> {
        let result = add(2, 2);

        if result == 4 {
            Ok(())
        } else {
            Err(String::from("two plus two does not equal four"))
        }
    }
}
```

`it_works` function-টিতে এখন `Result<(), String>` return type আছে। function-টির body-তে, `assert_eq!` macro call করার বদলে, আমরা test pass করলে `Ok(())` ফেরত দিই এবং test fail করলে ভেতরে একটি `String` নিয়ে একটি `Err` ফেরত দিই।

Test-গুলোকে এমনভাবে লিখলে যে তারা `Result<T, E>` ফেরত দেয়, তুমি test-এর body-তে question mark operator ব্যবহার করতে পারো, যা এমন test লেখার একটি সুবিধাজনক উপায় যেগুলোর ভেতরের কোনো operation `Err` variant ফেরত দিলে fail করা উচিত।

`Result<T, E>` ব্যবহার করে এমন test-এ তুমি `#[should_panic]` annotation ব্যবহার করতে পারবে না। কোনো operation `Err` variant ফেরত দেয় তা assert করতে, `Result<T, E>` value-তে question mark operator ব্যবহার করো _না_। তার বদলে, `assert!(value.is_err())` ব্যবহার করো।

যেহেতু এখন তুমি test লেখার কয়েকটি উপায় জানো, চলো দেখি আমরা যখন আমাদের test-গুলো চালাই তখন কী ঘটছে এবং `cargo test`-এর সাথে কী কী বিভিন্ন option ব্যবহার করতে পারি।

[concatenating]: ch08-02-strings.html#concatenating-with--or-format
[bench]: ../unstable-book/library-features/test.html
[ignoring]: ch11-02-running-tests.html#ignoring-tests-unless-specifically-requested
[subset]: ch11-02-running-tests.html#running-a-subset-of-tests-by-name
[controlling-how-tests-are-run]: ch11-02-running-tests.html#controlling-how-tests-are-run
[derivable-traits]: appendix-03-derivable-traits.html
[doc-comments]: ch14-02-publishing-to-crates-io.html#documentation-comments-as-tests
[paths-for-referring-to-an-item-in-the-module-tree]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html

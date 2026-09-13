## Test চালানোর উপায় নিয়ন্ত্রণ করা

যেমন `cargo run` তোমার code compile করে এবং তারপর ফলস্বরূপ binary-টি চালায়, তেমনি `cargo test` তোমার code-টিকে test mode-এ compile করে এবং ফলস্বরূপ test binary-টি চালায়। `cargo test` থেকে তৈরি হওয়া binary-টির default আচরণ হলো সব test parallel-ভাবে চালানো এবং test চলার সময় তৈরি হওয়া output capture করা, যাতে সেই output প্রদর্শিত না হয় এবং test result সম্পর্কিত output পড়া সহজ হয়। তবে তুমি command line option উল্লেখ করে এই default আচরণ পরিবর্তন করতে পারো।

কিছু command line option `cargo test`-কে দেওয়া হয়, আর কিছু ফলস্বরূপ test binary-কে দেওয়া হয়। এই দুই ধরনের argument আলাদা করতে, তুমি `cargo test`-কে দেওয়া argument-গুলো উল্লেখ করো, তারপর separator `--` দাও, এবং তারপর test binary-কে দেওয়া argument-গুলো উল্লেখ করো। `cargo test --help` চালালে `cargo test`-এর সাথে ব্যবহারযোগ্য option-গুলো দেখায়, আর `cargo test -- --help` চালালে separator-এর পরে ব্যবহারযোগ্য option-গুলো দেখায়। এই option-গুলো সম্পর্কে [_The `rustc` Book_-এর "Tests" section][tests]-এও নথিভুক্ত করা আছে।

[tests]: https://doc.rust-lang.org/rustc/tests/index.html

### Test Parallel-ভাবে বা পরপর চালানো

তুমি একাধিক test চালানোর সময়, সেগুলো default-ভাবে thread ব্যবহার করে parallel-ভাবে চলে, যার মানে সেগুলো দ্রুত শেষ হয় এবং তুমি তাড়াতাড়ি feedback পাও। যেহেতু test-গুলো একই সময়ে চলে, তোমাকে অবশ্যই নিশ্চিত করতে হবে যে তোমার test-গুলো একে অপরের ওপর বা কোনো shared state-এর ওপর — shared environment সহ, যেমন বর্তমান কর্ম ডিরেক্টরি বা environment variable — নির্ভর করে না।

উদাহরণস্বরূপ, ধরো তোমার প্রতিটি test এমন কিছু code চালায় যা ডিস্কে _test-output.txt_ নামে একটি file তৈরি করে এবং সেই file-এ কিছু data লেখে। তারপর প্রতিটি test সেই file-এর data পড়ে এবং assert করে যে file-টি একটি নির্দিষ্ট value ধারণ করছে, যা প্রতিটি test-এ আলাদা। যেহেতু test-গুলো একই সময়ে চলে, একটি test হয়তো আরেকটি test file-টিতে write করার পর এবং read করার আগের সময়ের মাঝেই file-টিকে overwrite করে ফেলতে পারে। তখন দ্বিতীয় test-টি fail করবে, code ভুল বলে নয় বরং কারণ test-গুলো parallel-ভাবে চলার সময় একে অপরের সাথে হস্তক্ষেপ করেছে। একটি সমাধান হলো নিশ্চিত করা যে প্রতিটি test ভিন্ন একটি file-এ লেখে; আরেকটি সমাধান হলো test-গুলো একবারে একটি করে চালানো।

তুমি যদি test-গুলো parallel-ভাবে না চালাতে চাও বা ব্যবহৃত thread সংখ্যার ওপর আরও fine-grained নিয়ন্ত্রণ চাও, তাহলে তুমি test binary-কে `--test-threads` flag এবং তুমি যে সংখ্যক thread ব্যবহার করতে চাও তা পাস করতে পারো। নিচের উদাহরণটি দেখো:

```console
$ cargo test -- --test-threads=1
```

আমরা test thread সংখ্যা `1`-এ সেট করেছি, যা program-কে বলে কোনো parallelism ব্যবহার করতে না। একটি thread ব্যবহার করে test চালালে parallel-এ চালানোর চেয়ে বেশি সময় লাগবে, কিন্তু test-গুলো যদি state share করে তবুও এরা একে অপরের সাথে হস্তক্ষেপ করবে না।

### Function Output প্রদর্শন করা

Default-ভাবে, যদি কোনো test pass করে, তাহলে Rust-এর test library standard output-এ প্রিন্ট করা সবকিছু capture করে। উদাহরণস্বরূপ, যদি আমরা কোনো test-এ `println!` call করি এবং test-টি pass করে, তাহলে আমরা terminal-এ `println!` output দেখতে পাব না; শুধু সেই লাইনটি দেখতে পাব যা নির্দেশ করে যে test pass করেছে। যদি কোনো test fail করে, তাহলে আমরা failure বার্তার বাকি অংশের সাথে standard output-এ যা প্রিন্ট করা হয়েছিল তা দেখতে পাব।

উদাহরণস্বরূপ, Listing 11-10-তে এমন একটি সাধারণ function আছে যা তার parameter-এর value print করে এবং 10 ফেরত দেয়, সেই সাথে একটি pass করা ও একটি fail করা test আছে।

<Listing number="11-10" file-name="src/lib.rs" caption="Tests for a function that calls `println!`">

```rust,panics,noplayground
fn prints_and_returns_10(a: i32) -> i32 {
    println!("I got the value {a}");
    10
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn this_test_will_pass() {
        let value = prints_and_returns_10(4);
        assert_eq!(value, 10);
    }

    #[test]
    fn this_test_will_fail() {
        let value = prints_and_returns_10(8);
        assert_eq!(value, 5);
    }
}
```

</Listing>

যখন আমরা এই test-গুলোকে `cargo test` দিয়ে চালাব, আমরা নিচের output দেখতে পাব:

```console
$ cargo test
   Compiling silly-function v0.1.0 (file:///projects/silly-function)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.58s
     Running unittests src/lib.rs (target/debug/deps/silly_function-160869f38cff9166)

running 2 tests
test tests::this_test_will_fail ... FAILED
test tests::this_test_will_pass ... ok

failures:

---- tests::this_test_will_fail stdout ----
I got the value 8

thread 'tests::this_test_will_fail' (6019863) panicked at src/lib.rs:19:9:
assertion `left == right` failed
  left: 10
 right: 5
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    tests::this_test_will_fail

test result: FAILED. 1 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

খেয়াল করো যে এই output-এ কোথাও `I got the value 4` দেখা যাচ্ছে না, যা pass করা test চলার সময় প্রিন্ট হয়। সেই output capture করা হয়েছে। Fail করা test থেকে পাওয়া output, `I got the value 8`, test সারসংক্ষেপ output-এর section-এ দেখা যায়, যা test failure-এর কারণও দেখায়।

আমরা যদি pass করা test-এর জন্যও প্রিন্ট করা value দেখতে চাই, তাহলে আমরা Rust-কে `--show-output` দিয়ে নির্দেশ দিতে পারি যে সফল test-গুলোর output-ও দেখাবে:

```console
$ cargo test -- --show-output
```

যখন আমরা Listing 11-10-এর test-গুলো `--show-output` flag সহ আবার চালাব, আমরা নিচের output দেখতে পাব:

```console
$ cargo test -- --show-output
   Compiling silly-function v0.1.0 (file:///projects/silly-function)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.60s
     Running unittests src/lib.rs (target/debug/deps/silly_function-160869f38cff9166)

running 2 tests
test tests::this_test_will_fail ... FAILED
test tests::this_test_will_pass ... ok

successes:

---- tests::this_test_will_pass stdout ----
I got the value 4


successes:
    tests::this_test_will_pass

failures:

---- tests::this_test_will_fail stdout ----
I got the value 8

thread 'tests::this_test_will_fail' (6022313) panicked at src/lib.rs:19:9:
assertion `left == right` failed
  left: 10
 right: 5
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    tests::this_test_will_fail

test result: FAILED. 1 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

### নাম দিয়ে Test-এর একটি Subset চালানো

সম্পূর্ণ test suite চালাতে মাঝে মাঝে অনেক সময় লাগতে পারে। তুমি যদি কোনো নির্দিষ্ট অংশের code নিয়ে কাজ করো, তাহলে হয়তো শুধু সেই code-এর সাথে সম্পর্কিত test-গুলো চালাতে চাইবে। তুমি `cargo test`-কে argument হিসেবে যেই test (গুলো) চালাতে চাও তার নাম পাস করে যে কোন কোন test চালাবে তা বেছে নিতে পারো।

কীভাবে test-এর একটি subset চালাতে হয় তা প্রদর্শন করতে, আমরা প্রথমে আমাদের `add_two` function-এর জন্য তিনটি test তৈরি করব, যেমন Listing 11-11-তে দেখানো হয়েছে, এবং যে কোন কোনটি চালাবে তা বেছে নেব।

<Listing number="11-11" file-name="src/lib.rs" caption="Three tests with three different names">

```rust,noplayground
pub fn add_two(a: u64) -> u64 {
    a + 2
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn add_two_and_two() {
        let result = add_two(2);
        assert_eq!(result, 4);
    }

    #[test]
    fn add_three_and_two() {
        let result = add_two(3);
        assert_eq!(result, 5);
    }

    #[test]
    fn one_hundred() {
        let result = add_two(100);
        assert_eq!(result, 102);
    }
}
```

</Listing>

আমরা যদি কোনো argument পাস না করে test চালাই, যেমনটা আগে দেখেছি, তবে সব test parallel-ভাবে চলবে:

```console
$ cargo test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.62s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 3 tests
test tests::add_three_and_two ... ok
test tests::add_two_and_two ... ok
test tests::one_hundred ... ok

test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests adder

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

#### Single Test চালানো

আমরা যেকোনো test function-এর নাম `cargo test`-কে পাস করতে পারি শুধু সেই test-টি চালানোর জন্য:

```console
$ cargo test one_hundred
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.69s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 1 test
test tests::one_hundred ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 2 filtered out; finished in 0.00s
```

শুধু `one_hundred` নামের test-টি চলেছে; অন্য দুটি test সেই নামের সাথে মেলেনি। Test output আমাদের জানায় যে আমাদের আরও test ছিল যেগুলো চলেনি, শেষে `2 filtered out` প্রদর্শন করে।

আমরা এভাবে একাধিক test-এর নাম উল্লেখ করতে পারি না; `cargo test`-কে দেওয়া প্রথম value-টিই ব্যবহৃত হবে। কিন্তু একাধিক test চালানোর একটি উপায় আছে।

#### একাধিক Test চালাতে Filtering

আমরা কোনো test নামের অংশ উল্লেখ করতে পারি, এবং যেকোনো test যার নাম সেই value-এর সাথে মেলে সেটি চলবে। উদাহরণস্বরূপ, যেহেতু আমাদের দুটি test-এর নামে `add` আছে, আমরা `cargo test add` চালিয়ে সেই দুটিকে চালাতে পারি:

```console
$ cargo test add
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.61s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 2 tests
test tests::add_three_and_two ... ok
test tests::add_two_and_two ... ok

test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 1 filtered out; finished in 0.00s
```

এই command-টি নামে `add` থাকা সব test চালিয়েছে এবং `one_hundred` নামের test-টিকে filter করে বাদ দিয়েছে। এটাও খেয়াল করো যে কোনো test যেই module-এ আছে সেটি তার নামের অংশে পরিণত হয়, তাই আমরা একটি module-এর নাম filter করে সেই module-এর সব test চালাতে পারি।

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-some-tests-unless-specifically-requested"></a>

### বিশেষভাবে না চাওয়া পর্যন্ত Test Ignore করা

মাঝে মাঝে কয়েকটি নির্দিষ্ট test execute করতে অনেক সময় লাগতে পারে, তাই তুমি হয়তো `cargo test`-এর বেশিরভাগ চলার সময় সেগুলো বাদ দিতে চাইবে। তুমি যে সব test চালাতে চাও তাদের সবগুলোকে argument হিসেবে তালিকাভুক্ত করার বদলে, তুমি সময়সাপেক্ষ test-গুলোকে `ignore` attribute দিয়ে annotate করে বাদ দিতে পারো, যেমনটা এখানে দেখানো হয়েছে:

<span class="filename">Filename: src/lib.rs</span>

```rust,noplayground
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }

    #[test]
    #[ignore]
    fn expensive_test() {
        // code that takes an hour to run
    }
}
```

`#[test]`-এর পর, আমরা যেই test-টিকে বাদ দিতে চাই তার কাছে `#[ignore]` লাইন যোগ করি। এখন আমরা যখন আমাদের test চালাব, `it_works` চলবে, কিন্তু `expensive_test` চলবে না:

```console
$ cargo test
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.60s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 2 tests
test tests::expensive_test ... ignored
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests adder

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

`expensive_test` function-টিকে `ignored` হিসেবে তালিকাভুক্ত করা হয়েছে। আমরা যদি শুধু ignored test-গুলো চালাতে চাই, আমরা `cargo test -- --ignored` ব্যবহার করতে পারি:

```console
$ cargo test -- --ignored
   Compiling adder v0.1.0 (file:///projects/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.61s
     Running unittests src/lib.rs (target/debug/deps/adder-92948b65e88960b4)

running 1 test
test tests::expensive_test ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 1 filtered out; finished in 0.00s

   Doc-tests adder

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

কোন কোন test চলবে তা নিয়ন্ত্রণ করে, তুমি নিশ্চিত করতে পারো যে তোমার `cargo test`-এর ফল দ্রুত ফিরে আসবে। যখন তুমি এমন একটি পর্যায়ে পৌঁছাবে যখন `ignored` test-গুলোর ফল যাচাই করা প্রাসঙ্গিক এবং ফলের জন্য অপেক্ষা করার সময় তোমার কাছে আছে, তখন তুমি `cargo test -- --ignored` চালাতে পারো। তুমি যদি সব test চালাতে চাও — সেগুলো ignored কিনা তা বিবেচ্য নয় — তাহলে তুমি `cargo test -- --include-ignored` চালাতে পারো।

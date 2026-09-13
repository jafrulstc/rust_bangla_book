## `Result` দিয়ে Recoverable Error

বেশিরভাগ error এত গুরুতর নয় যে program সম্পূর্ণভাবে থামিয়ে দিতে হবে। মাঝে মাঝে একটি function ব্যর্থ হলে, এর কারণ এমন হতে পারে যা তুমি সহজেই বুঝতে পারো এবং সাড়া দিতে পারো। যেমন, তুমি যদি একটি file খোলার চেষ্টা করো এবং সেই কাজটি ব্যর্থ হয় কারণ file-টি নেই, তবে তুমি হয়তো process বন্ধ না করে সেই file-টি তৈরি করতে চাইবে।

Chapter 2-এর [“Handling Potential Failure with `Result`”][handle_failure]<!-- ignore --> section-এ মনে করো, `Result` enum-কে দুটি variant সহ define করা হয়েছে—`Ok` এবং `Err`, এভাবে:

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

`T` এবং `E` হল generic type parameter: Chapter 10-এ আমরা generics নিয়ে আরও বিস্তারিত আলোচনা করব। এখন তোমার যা জানা প্রয়োজন তা হলো `T` সেই value-এর type উপস্থাপন করে যা success-এর ক্ষেত্রে `Ok` variant-এর ভেতরে return হবে, এবং `E` সেই error-এর type উপস্থাপন করে যা failure-এর ক্ষেত্রে `Err` variant-এর ভেতরে return হবে। যেহেতু `Result`-এ এই generic type parameter গুলো আছে, আমরা অনেক ভিন্ন ভিন্ন পরিস্থিতিতে `Result` type এবং এর উপর define করা function ব্যবহার করতে পারি যেখানে আমরা যে success value ও error value return করতে চাই তা ভিন্ন হতে পারে।

চলো এমন একটি function call করি যা একটি `Result` value return করে, কারণ function-টি ব্যর্থ হতে পারে। Listing 9-3-তে আমরা একটি file খোলার চেষ্টা করি।

<Listing number="9-3" file-name="src/main.rs" caption="Opening a file">

```rust
use std::fs::File;

fn main() {
    let greeting_file_result = File::open("hello.txt");
}
```

</Listing>

`File::open`-এর return type হলো একটি `Result<T, E>`। Generic parameter `T`-কে `File::open`-এর implementation-এ success value-এর type দিয়ে পূরণ করা হয়েছে—`std::fs::File`, যা একটি file handle। Error value-তে ব্যবহৃত `E`-এর type হলো `std::io::Error`। এই return type-এর অর্থ হলো `File::open`-এ করা call সফল হতে পারে এবং এমন একটি file handle return করতে পারে যা থেকে আমরা পড়তে বা লিখতে পারব। Function call-টি ব্যর্থও হতে পারে: যেমন, file-টি নাও থাকতে পারে, অথবা আমাদের file-টি অ্যাক্সেস করার permission নাও থাকতে পারে। `File::open` function-এর এমন উপায় থাকা দরকার যাতে সে আমাদের জানাতে পারে সে সফল হয়েছে না ব্যর্থ, এবং একই সাথে আমাদের file handle অথবা error সংক্রান্ত তথ্য দিতে পারে। এই তথ্যটিই `Result` enum প্রকাশ করে।

`File::open` সফল হলে, `greeting_file_result` variable-এর value হবে `Ok`-এর একটি instance যা একটি file handle ধারণ করে। ব্যর্থ হলে, `greeting_file_result`-এর value হবে `Err`-এর একটি instance যা ঘটে যাওয়া error-এর ধরন সম্পর্কে আরও তথ্য ধারণ করে।

`File::open` যে value return করে তার উপর ভিত্তি করে ভিন্ন ভিন্ন পদক্ষেপ নিতে আমাদের Listing 9-3-এর code-এ আরও কিছু যোগ করতে হবে। Listing 9-4 একটি সাধারণ টুল—Chapter 6-এ আলোচিত `match` expression—ব্যবহার করে `Result` handle করার একটি উপায় দেখায়।

<Listing number="9-4" file-name="src/main.rs" caption="Using a `match` expression to handle the `Result` variants that might be returned">

```rust,should_panic
use std::fs::File;

fn main() {
    let greeting_file_result = File::open("hello.txt");

    let greeting_file = match greeting_file_result {
        Ok(file) => file,
        Err(error) => panic!("Problem opening the file: {error:?}"),
    };
}
```

</Listing>

লক্ষ্য করো যে, `Option` enum-এর মতো `Result` enum এবং এর variant গুলো prelude দ্বারা scope-এ নিয়ে আসা হয়েছে, তাই `match` arm-এ `Ok` এবং `Err` variant-এর আগে `Result::` উল্লেখ করার প্রয়োজন নেই।

যখন result হয় `Ok`, এই code `Ok` variant-এর ভেতরের `file` value-কে বের করে return করবে, এবং আমরা সেই file handle value-কে `greeting_file` variable-এ assign করব। `match`-এর পরে, আমরা পড়ার বা লেখার জন্য সেই file handle ব্যবহার করতে পারি।

`match`-এর অন্য arm-টি সেই ক্ষেত্রে handle করে যেখানে আমরা `File::open` থেকে একটি `Err` value পাই। এই উদাহরণে, আমরা `panic!` macro call করার সিদ্ধান্ত নিয়েছি। যদি আমাদের current directory-তে _hello.txt_ নামে কোনো file না থাকে এবং আমরা এই code run করি, তবে আমরা `panic!` macro থেকে নিম্নলিখিত output দেখতে পাব:

```console
$ cargo run
   Compiling error-handling v0.1.0 (file:///projects/error-handling)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.73s
     Running `target/debug/error-handling`

thread 'main' (6018048) panicked at src/main.rs:8:23:
Problem opening the file: Os { code: 2, kind: NotFound, message: "No such file or directory" }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

স্বাভাবিকভাবেই, এই output আমাদের ঠিক কী ভুল হয়েছে তা জানায়।

### ভিন্ন ভিন্ন Error-এর উপর Match করা

`File::open` যে কারণেই ব্যর্থ হোক না কেন, Listing 9-4-এর code `panic!` করবে। তবে আমরা ভিন্ন ভিন্ন ব্যর্থতার কারণের জন্য ভিন্ন ভিন্ন পদক্ষেপ নিতে চাই। যদি `File::open` ব্যর্থ হয় কারণ file-টি নেই, আমরা file-টি তৈরি করে নতুন file-এর handle return করতে চাই। কিন্তু অন্য যেকোনো কারণে `File::open` ব্যর্থ হলে—যেমন file-টি খোলার permission না থাকলে—আমরা এখনও চাই code যেন Listing 9-4-এর মতোই `panic!` করে। এর জন্য, আমরা একটি inner `match` expression যোগ করি, যা Listing 9-5-তে দেখানো হয়েছে।

<Listing number="9-5" file-name="src/main.rs" caption="Handling different kinds of errors in different ways">

<!-- ignore this test because otherwise it creates hello.txt which causes other
tests to fail lol -->

```rust,ignore
use std::fs::File;
use std::io::ErrorKind;

fn main() {
    let greeting_file_result = File::open("hello.txt");

    let greeting_file = match greeting_file_result {
        Ok(file) => file,
        Err(error) => match error.kind() {
            ErrorKind::NotFound => match File::create("hello.txt") {
                Ok(fc) => fc,
                Err(e) => panic!("Problem creating the file: {e:?}"),
            },
            _ => {
                panic!("Problem opening the file: {error:?}");
            }
        },
    };
}
```

</Listing>

`File::open` যে value `Err` variant-এর ভেতরে return করে তার type হলো `io::Error`, যা standard library দ্বারা সরবরাহ করা একটি struct। এই struct-এ একটি method আছে—`kind`—যা call করলে আমরা একটি `io::ErrorKind` value পাই। `io::ErrorKind` enum standard library দ্বারা সরবরাহ করা হয় এবং এর variant গুলো একটি `io` operation থেকে সৃষ্ট বিভিন্ন ধরনের error উপস্থাপন করে। আমরা যে variant ব্যবহার করতে চাই তা হলো `ErrorKind::NotFound`, যা নির্দেশ করে যে আমরা যে file-টি খোলার চেষ্টা করছি সেটি এখনও নেই। সুতরাং, আমরা `greeting_file_result`-এর উপর match করি, কিন্তু `error.kind()`-এর উপরেও একটি inner match রয়েছে।

inner match-এ আমরা যে শর্তটি যাচাই করতে চাই তা হলো `error.kind()` থেকে return হওয়া value `ErrorKind` enum-এর `NotFound` variant কি না। যদি তাই হয়, আমরা `File::create` দিয়ে file তৈরি করার চেষ্টা করি। কিন্তু যেহেতু `File::create`-ও ব্যর্থ হতে পারে, আমাদের inner `match` expression-এ দ্বিতীয় একটি arm দরকার। যখন file তৈরি করা যায় না, তখন একটি ভিন্ন error message প্রিন্ট করা হয়। বাইরের `match`-এর দ্বিতীয় arm-টি অপরিবর্তিত থাকে, তাই program missing file error ছাড়া অন্য যেকোনো error-এ panic করে।

> #### `Result<T, E>`-এর সাথে `match` ব্যবহারের বিকল্প
>
> বেশ কিছু `match`! `match` expression খুবই কার্যকর, কিন্তু এটি অনেকটাই একটি primitive টুল। Chapter 13-তে তুমি closure সম্পর্কে শিখবে, যা `Result<T, E>`-এর উপর define করা অনেক method-এর সাথে ব্যবহৃত হয়। `Result<T, E>` value handle করার ক্ষেত্রে `match` ব্যবহারের চেয়ে এই method গুলো আরও সংক্ষিপ্ত হতে পারে।
>
> যেমন, এখানে Listing 9-5-এ দেখানো একই logic লেখার আরেকটি উপায় দেওয়া হলো, এবার closure এবং `unwrap_or_else` method ব্যবহার করে:
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore
> use std::fs::File;
> use std::io::ErrorKind;
>
> fn main() {
>     let greeting_file = File::open("hello.txt").unwrap_or_else(|error| {
>         if error.kind() == ErrorKind::NotFound {
>             File::create("hello.txt").unwrap_or_else(|error| {
>                 panic!("Problem creating the file: {error:?}");
>             })
>         } else {
>             panic!("Problem opening the file: {error:?}");
>         }
>     });
> }
> ```
>
> যদিও এই code-এর behavior Listing 9-5-এর মতোই, এতে কোনো `match` expression নেই এবং পড়তেও পরিষ্কার। Chapter 13 পড়ার পর এই উদাহরণে ফিরে এসো এবং standard library documentation-এ `unwrap_or_else` method খুঁজে দেখো। error নিয়ে কাজ করার সময় বড় বড় nested `match` expression পরিষ্কার করতে এই ধরনের আরও অনেক method কাজে লাগে।

<!-- Old headings. Do not remove or links may break. -->

<a id="shortcuts-for-panic-on-error-unwrap-and-expect"></a>

#### Error হলে Panic-এর Shortcut

`match` ব্যবহার করা যথেষ্ট কাজ করে, কিন্তু এটি কিছুটা verbose হতে পারে এবং সবসময় intent ভালোভাবে প্রকাশ করে না। `Result<T, E>` type-এ বিভিন্ন আরও নির্দিষ্ট কাজের জন্য অনেক helper method define করা আছে। `unwrap` method হলো এমন একটি shortcut যা ঠিক Listing 9-4-এ আমরা যে `match` expression লিখেছিলাম তার মতোই implement করা। যদি `Result` value `Ok` variant হয়, `unwrap` `Ok`-এর ভেতরের value return করবে। যদি `Result` `Err` variant হয়, `unwrap` আমাদের হয়ে `panic!` macro call করবে। এখানে `unwrap`-এর কাজ করার একটি উদাহরণ দেওয়া হলো:

<Listing file-name="src/main.rs">

```rust,should_panic
use std::fs::File;

fn main() {
    let greeting_file = File::open("hello.txt").unwrap();
}
```

</Listing>

আমরা যদি এই code _hello.txt_ file ছাড়া run করি, তবে `unwrap` method-টি যে `panic!` call করে সেখান থেকে একটি error message দেখতে পাব:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-04-unwrap
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:4:49:
called `Result::unwrap()` on an `Err` value: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

একইভাবে, `expect` method আমাদের `panic!` error message বেছে নেওয়ার সুযোগ দেয়। `unwrap`-এর বদলে `expect` ব্যবহার করে এবং ভালো error message দিলে তোমার intent প্রকাশ পায় এবং একটি panic-এর উৎস খুঁজে বের করা সহজ হয়। `expect`-এর syntax দেখতে এমন:

<Listing file-name="src/main.rs">

```rust,should_panic
use std::fs::File;

fn main() {
    let greeting_file = File::open("hello.txt")
        .expect("hello.txt should be included in this project");
}
```

</Listing>

আমরা `unwrap`-এর মতো একইভাবে `expect` ব্যবহার করি: file handle return করতে অথবা `panic!` macro call করতে। `expect` যে error message তার `panic!` call-এ ব্যবহার করে সেটি হবে সেই parameter যা আমরা `expect`-কে পাস করি, `unwrap` যে ডিফল্ট `panic!` message ব্যবহার করে তা নয়। এটি দেখতে এমন:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-05-expect
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:5:10:
hello.txt should be included in this project: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

production-quality code-এ, বেশিরভাগ Rustacean `unwrap`-এর বদলে `expect` বেছে নেয় এবং কেন এই operation সবসময় সফল হবে বলে আশা করা হচ্ছে তা সম্পর্কে আরও context দেয়। এভাবে, তোমার assumption কখনো ভুল প্রমাণিত হলে, debugging-এ ব্যবহারের জন্য তোমার হাতে আরও তথ্য থাকে।

### Propagating Error

যখন কোনো function-এর implementation এমন কিছু call করে যা ব্যর্থ হতে পারে, তখন function-এর ভেতরেই error handle করার বদলে তুমি error-টিকে calling code-এ return করতে পারো যাতে সে সিদ্ধান্ত নিতে পারে কী করতে হবে। একে error _propagate_ করা বলা হয় এবং এটি calling code-কে আরও বেশি নিয়ন্ত্রণ দেয়, কারণ সেখানে সম্ভবত তোমার code-এর context-এ থাকা তথ্য বা logic-এর চেয়ে বেশি তথ্য বা এমন logic থাকতে পারে যা নির্দেশ করে error কীভাবে handle করা উচিত।

যেমন, Listing 9-6 এমন একটি function দেখায় যা একটি file থেকে username পড়ে। যদি file-টি না থাকে বা পড়া না যায়, এই function সেই error গুলো function-টিকে call করা code-এ return করবে।

<Listing number="9-6" file-name="src/main.rs" caption="A function that returns errors to the calling code using `match`">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
use std::fs::File;
use std::io::{self, Read};

fn read_username_from_file() -> Result<String, io::Error> {
    let username_file_result = File::open("hello.txt");

    let mut username_file = match username_file_result {
        Ok(file) => file,
        Err(e) => return Err(e),
    };

    let mut username = String::new();

    match username_file.read_to_string(&mut username) {
        Ok(_) => Ok(username),
        Err(e) => Err(e),
    }
}
```

</Listing>

এই function-টিকে আরও ছোট করে লেখা যেত, কিন্তু আমরা প্রথমে error handling বোঝার জন্য অনেকটা নিজে হাতে করব; শেষে, আমরা ছোট উপায়টি দেখাব। চলো প্রথমে function-টির return type-টি দেখি: `Result<String, io::Error>`। এর অর্থ হলো function-টি `Result<T, E>` type-এর একটি value return করছে, যেখানে generic parameter `T` কংক্রিট type `String` দিয়ে পূরণ করা হয়েছে এবং generic type `E` কংক্রিট type `io::Error` দিয়ে পূরণ করা হয়েছে।

যদি এই function-টি কোনো সমস্যা ছাড়া সফল হয়, এই function-টিকে call করা code একটি `Ok` value পাবে যা একটি `String` ধারণ করবে—সেই `username` যা এই function file থেকে পড়েছে। যদি এই function কোনো সমস্যার মুখোমুখি হয়, calling code একটি `Err` value পাবে যা `io::Error`-এর একটি instance ধারণ করবে যাতে সমস্যা সম্পর্কে আরও তথ্য থাকবে। আমরা এই function-এর return type হিসেবে `io::Error` বেছেছি কারণ এটি ঘটনাক্রমে এই function-এর body-তে call করা দুটি operation-ই যা ব্যর্থ হতে পারে—`File::open` function এবং `read_to_string` method—তাদের return করা error value-এর type ও একই।

Function-টির body শুরু হয় `File::open` function call করার মাধ্যমে। তারপর, আমরা `Result` value-টি Listing 9-4-এর `match`-এর মতো একটি `match` দিয়ে handle করি। যদি `File::open` সফল হয়, pattern variable `file`-এ থাকা file handle mutable variable `username_file`-এর value হয়ে যায় এবং function চলতে থাকে। `Err` case-এ, `panic!` call করার বদলে, আমরা `return` keyword ব্যবহার করে function থেকে সম্পূর্ণভাবে আগেই ফিরে যাই এবং `File::open` থেকে আসা error value-টিকে, এখন pattern variable `e`-তে, এই function-এর error value হিসেবে calling code-এ পাঠাই।

সুতরাং, যদি `username_file`-এ একটি file handle থাকে, তবে function-টি `username` variable-এ একটি নতুন `String` তৈরি করে এবং `username_file`-এ থাকা file handle-এর উপর `read_to_string` method call করে file-এর content `username`-এ পড়ে। `read_to_string` method-ও একটি `Result` return করে কারণ এটিও ব্যর্থ হতে পারে, যদিও `File::open` সফল হয়েছে। সুতরাং, আমাদের সেই `Result` handle করার জন্য আরেকটি `match` দরকার: যদি `read_to_string` সফল হয়, তবে আমাদের function সফল হয়েছে, এবং আমরা `username`-এ এখন যে file থেকে পড়া username আছে তা একটি `Ok`-এ মুড়ে return করি। যদি `read_to_string` ব্যর্থ হয়, আমরা `File::open`-এর return value handle করা `match`-এ যেভাবে error value return করেছিলাম সেভাবেই error value return করি। তবে, স্পষ্টভাবে `return` বলার দরকার নেই, কারণ এটি function-টির শেষ expression।

এই code-টিকে call করা code তারপর একটি `Ok` value যা username ধারণ করে অথবা একটি `Err` value যা `io::Error` ধারণ করে—পাওয়ার পর handle করবে। এই value গুলো দিয়ে কী করা হবে তা calling code-এর উপর নির্ভর করে। Calling code যদি একটি `Err` value পায়, সে `panic!` call করে program crash করতে পারে, একটি ডিফল্ট username ব্যবহার করতে পারে, অথবা file ছাড়া অন্য কোথাও থেকে username খুঁজে নিতে পারে। আমাদের কাছে calling code-টি আসলে কী করার চেষ্টা করছে তা নিয়ে যথেষ্ট তথ্য নেই, তাই আমরা সমস্ত success বা error তথ্য উপরের দিকে propagate করি যাতে সে যথাযথভাবে handle করতে পারে।

Rust-এ error propagate করার এই pattern এতই সাধারণ যে Rust এটিকে সহজ করার জন্য `?` (প্রশ্নবোধক চিহ্ন) operator সরবরাহ করে।

<!-- Old headings. Do not remove or links may break. -->

<a id="a-shortcut-for-propagating-errors-the--operator"></a>

#### `?` Operator Shortcut

Listing 9-7 `read_username_from_file`-এর এমন একটি implementation দেখায় যার কার্যকারিতা Listing 9-6-এর মতোই, কিন্তু এই implementation `?` operator ব্যবহার করে।

<Listing number="9-7" file-name="src/main.rs" caption="A function that returns errors to the calling code using the `?` operator">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
use std::fs::File;
use std::io::{self, Read};

fn read_username_from_file() -> Result<String, io::Error> {
    let mut username_file = File::open("hello.txt")?;
    let mut username = String::new();
    username_file.read_to_string(&mut username)?;
    Ok(username)
}
```

</Listing>

একটি `Result` value-এর পরে বসানো `?` ঠিক সেভাবেই কাজ করে যেভাবে আমরা Listing 9-6-এ `Result` value handle করার জন্য define করা `match` expression গুলো করেছি। যদি `Result`-এর value একটি `Ok` হয়, `Ok`-এর ভেতরের value এই expression থেকে return হবে, এবং program চলতে থাকবে। যদি value একটি `Err` হয়, পুরো function থেকে সেই `Err` return হবে ঠিক যেমন আমরা `return` keyword ব্যবহার করেছি, যাতে error value calling code-এ propagate হয়।

Listing 9-6-এর `match` expression যা করে এবং `?` operator যা করে তার মধ্যে একটি পার্থক্য আছে: যে error value-এর উপর `?` operator call করা হয় সেগুলো `from` function দিয়ে যায়, যা standard library-এর `From` trait-এ define করা এবং যা এক ধরনের value অন্য ধরনে রূপান্তর করতে ব্যবহৃত হয়। যখন `?` operator `from` function call করে, যে error type পাওয়া গেছে সেটি current function-এর return type-এ define করা error type-এ রূপান্তরিত হয়। এটি তখন কার্যকর যখন একটি function একটি error type return করে একটি function-এর ব্যর্থ হওয়ার সব উপায় উপস্থাপন করতে, যদিও কিছু অংশ অনেক ভিন্ন কারণে ব্যর্থ হতে পারে।

যেমন, আমরা Listing 9-7-এর `read_username_from_file` function-টিকে এমন একটি custom error type `OurError` return করতে পরিবর্তন করতে পারি যা আমরা define করি। যদি আমরা একটি `io::Error` থেকে `OurError`-এর একটি instance তৈরি করতে `impl From<io::Error> for OurError`-ও define করি, তবে `read_username_from_file`-এর body-তে `?` operator call গুলো `from` call করবে এবং function-এ আর কোনো অতিরিক্ত code ছাড়াই error type রূপান্তর করবে।

Listing 9-7-এর context-এ, `File::open` call-এর শেষের `?` একটি `Ok`-এর ভেতরের value-কে `username_file` variable-এ return করবে। যদি কোনো error ঘটে, `?` operator পুরো function থেকে আগেই return করবে এবং যেকোনো `Err` value calling code-কে দেবে। `read_to_string` call-এর শেষের `?`-এর ক্ষেত্রেও একই কথা প্রযোজ্য।

`?` operator অনেক boilerplate দূর করে এবং এই function-এর implementation আরও সহজ করে। আমরা `?`-এর ঠিক পরেই method call chain করে এই code আরও ছোট করতে পারি, যেমন Listing 9-8-তে দেখানো হয়েছে।

<Listing number="9-8" file-name="src/main.rs" caption="Chaining method calls after the `?` operator">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
use std::fs::File;
use std::io::{self, Read};

fn read_username_from_file() -> Result<String, io::Error> {
    let mut username = String::new();

    File::open("hello.txt")?.read_to_string(&mut username)?;

    Ok(username)
}
```

</Listing>

আমরা নতুন `String` তৈরি করাটা `username`-এ function-টির শুরুতে সরিয়ে নিয়েছি; সেই অংশের কোনো পরিবর্তন নেই। `username_file` নামে একটি variable তৈরি করার বদলে, আমরা `read_to_string` call-টিকে সরাসরি `File::open("hello.txt")?`-এর result-এর সাথে chain করেছি। `read_to_string` call-এর শেষে এখনও একটি `?` আছে, এবং আমরা এখনও একটি `Ok` value return করি যা `username` ধারণ করে যখন `File::open` এবং `read_to_string` উভয়ই সফল হয়, error return করার বদলে। কার্যকারিতা আবারও Listing 9-6 এবং Listing 9-7-এর মতোই; এটি শুধু লেখার একটি ভিন্ন, আরও ergonomic উপায়।

Listing 9-9 `fs::read_to_string` ব্যবহার করে এটিকে আরও ছোট করার একটি উপায় দেখায়।

<Listing number="9-9" file-name="src/main.rs" caption="Using `fs::read_to_string` instead of opening and then reading the file">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
use std::fs;
use std::io;

fn read_username_from_file() -> Result<String, io::Error> {
    fs::read_to_string("hello.txt")
}
```

</Listing>

একটি file থেকে string-এ পড়া বেশ সাধারণ একটি operation, তাই standard library সুবিধাজনক `fs::read_to_string` function সরবরাহ করে যা file খোলে, একটি নতুন `String` তৈরি করে, file-এর content পড়ে, সেই content সেই `String`-এ রাখে, এবং তা return করে। অবশ্যই, `fs::read_to_string` ব্যবহার করলে আমাদের সমস্ত error handling বোঝানোর সুযোগ থাকে না, তাই আমরা আগে দীর্ঘ উপায়ে করেছি।

<!-- Old headings. Do not remove or links may break. -->

<a id="where-the--operator-can-be-used"></a>

#### `?` Operator কোথায় ব্যবহার করা যায়

`?` operator শুধুমাত্র সেসব function-এ ব্যবহার করা যায় যাদের return type `?` যে value-এর উপর ব্যবহার করা হচ্ছে তার সাথে compatible। এর কারণ হলো `?` operator-কে এমনভাবে define করা হয়েছে যাতে সে Listing 9-6-এ আমরা যে `match` expression define করেছিলাম তার মতো একইভাবে function থেকে একটি value early return করে। Listing 9-6-তে, `match`-টি একটি `Result` value ব্যবহার করছিল, এবং early return arm একটি `Err(e)` value return করেছিল। Function-এর return type-টি অবশ্যই একটি `Result` হতে হবে যাতে এই `return`-এর সাথে এটি compatible হয়।

Listing 9-10-তে, চলো দেখি যদি আমরা এমন একটি `main` function-এ `?` operator ব্যবহার করি যার return type আমরা `?` যে value-এর উপর ব্যবহার করছি তার type-এর সাথে compatible নয়, তবে কী error পাব।

<Listing number="9-10" file-name="src/main.rs" caption="Attempting to use the `?` in the `main` function that returns `()` won’t compile.">

```rust,ignore,does_not_compile
use std::fs::File;

fn main() {
    let greeting_file = File::open("hello.txt")?;
}
```

</Listing>

এই code একটি file খোলে, যা ব্যর্থ হতে পারে। `?` operator `File::open` থেকে return হওয়া `Result` value-কে অনুসরণ করে, কিন্তু এই `main` function-এর return type হলো `()`, `Result` নয়। যখন আমরা এই code compile করি, আমরা নিম্নলিখিত error message পাই:

```console
$ cargo run
   Compiling error-handling v0.1.0 (file:///projects/error-handling)
error[E0277]: the `?` operator can only be used in a function that returns `Result` or `Option` (or another type that implements `FromResidual`)
 --> src/main.rs:4:48
  |
3 | fn main() {
  | --------- this function should return `Result` or `Option` to accept `?`
4 |     let greeting_file = File::open("hello.txt")?;
  |                                                ^ cannot use the `?` operator in a function that returns `()`
  |
help: consider adding return type
  |
3 ~ fn main() -> Result<(), Box<dyn std::error::Error>> {
4 |     let greeting_file = File::open("hello.txt")?;
5 +     Ok(())
  |

For more information about this error, try `rustc --explain E0277`.
error: could not compile `error-handling` (bin "error-handling") due to 1 previous error
```

এই error-টি নির্দেশ করে যে আমরা শুধুমাত্র এমন একটি function-এ `?` operator ব্যবহার করতে পারি যা `Result`, `Option`, অথবা `FromResidual` implement করে এমন অন্য কোনো type return করে।

error-টি ঠিক করতে তোমার কাছে দুটি পছন্দ আছে। একটি পছন্দ হলো তোমার function-এর return type-কে এমনভাবে পরিবর্তন করা যাতে সেটি তুমি `?` operator যে value-এর উপর ব্যবহার করছ তার সাথে compatible হয়, যদি কোনো বাধা না থাকে। অন্য পছন্দটি হলো একটি `match` অথবা `Result<T, E>`-এর কোনো একটি method ব্যবহার করে `Result<T, E>`-কে যথাযথভাবে handle করা।

error message-টিতে আরও উল্লেখ করা হয়েছে যে `?` কে `Option<T>` value-এর সাথেও ব্যবহার করা যায়। `Result`-এর উপর `?` ব্যবহারের মতোই, তুমি শুধুমাত্র এমন একটি function-ে `Option`-এর উপর `?` ব্যবহার করতে পারো যা একটি `Option` return করে। `Option<T>`-এর উপর call করা হলে `?` operator-এর behavior `Result<T, E>`-এর উপর call করার মতোই: যদি value `None` হয়, সেই মুহূর্তে function থেকে `None` early return হবে। যদি value `Some` হয়, `Some`-এর ভেতরের value হবে সেই expression-এর resultant value, এবং function চলতে থাকবে। Listing 9-11-তে এমন একটি function-এর উদাহরণ আছে যা প্রদত্ত text-এর প্রথম লাইনের শেষ character খুঁজে বের করে।

<Listing number="9-11" caption="Using the `?` operator on an `Option<T>` value">

```rust
fn last_char_of_first_line(text: &str) -> Option<char> {
    text.lines().next()?.chars().last()
}
```

</Listing>

এই function-টি `Option<char>` return করে কারণ সম্ভব যে সেখানে একটি character থাকতে পারে, কিন্তু সম্ভব যে কিছুই নাও থাকতে পারে। এই code `text` string slice argument নেয় এবং তার উপর `lines` method call করে, যা string-এর লাইন গুলোর উপর একটি iterator return করে। যেহেতু এই function প্রথম লাইনটি পরীক্ষা করতে চায়, সে iterator-এর উপর `next` call করে iterator থেকে প্রথম value পায়। যদি `text` একটি ফাঁকা string হয়, `next`-এ করা এই call `None` return করবে, যে ক্ষেত্রে আমরা `?` ব্যবহার করে `last_char_of_first_line` থেকে থামিয়ে `None` return করি। যদি `text` ফাঁকা string না হয়, `next` একটি `Some` value return করবে যা `text`-এর প্রথম লাইনের একটি string slice ধারণ করে।

`?` সেই string slice-টিকে বের করে, এবং আমরা সেই string slice-এর উপর `chars` call করে তার character-গুলোর একটি iterator পেতে পারি। আমরা এই প্রথম লাইনের শেষ character-টিতে আগ্রহী, তাই আমরা iterator-এর শেষ item return করতে `last` call করি। এটি একটি `Option` কারণ সম্ভব যে প্রথম লাইনটি ফাঁকা string; যেমন, যদি `text` একটি ফাঁকা লাইন দিয়ে শুরু হয় কিন্তু অন্য লাইনে character থাকে, যেমন `"\nhi"`। তবে, যদি প্রথম লাইনে একটি শেষ character থাকে, তবে তা `Some` variant-এ return হবে। মাঝখানের `?` operator আমাদের এই logic প্রকাশ করার একটি সংক্ষিপ্ত উপায় দেয়, যার ফলে আমরা function-টি এক লাইনেই implement করতে পারি। যদি আমরা `Option`-এর উপর `?` operator ব্যবহার করতে না পারতাম, তবে আমাদের আরও বেশি method call অথবা একটি `match` expression ব্যবহার করে এই logic implement করতে হতো।

মনে রাখবে যে তুমি এমন একটি function-এ যা `Result` return করে `Result`-এর উপর `?` operator ব্যবহার করতে পারো, এবং এমন একটি function-ে যা `Option` return করে `Option`-এর উপর `?` operator ব্যবহার করতে পারো, কিন্তু দুটো মিলিয়ে ব্যবহার করতে পারবে না। `?` operator স্বয়ংক্রিয়ভাবে একটি `Result`-কে `Option`-এ বা এর উল্টোটি রূপান্তর করবে না; সেই ক্ষেত্রে তুমি `Result`-এর উপর `ok` method অথবা `Option`-এর উপর `ok_or` method-এর মতো method ব্যবহার করে স্পষ্টভাবে রূপান্তর করতে পারো।

এ পর্যন্ত, আমরা যেসব `main` function ব্যবহার করেছি সবগুলো `()` return করে। `main` function-টি বিশেষ কারণ এটি একটি executable program-এর entry point এবং exit point, এবং program-টি যাতে প্রত্যাশিত আচরণ করে তার জন্য এর return type কী হতে পারে তার উপর কিছু restriction আছে।

ভাগ্যক্রমে, `main` একটি `Result<(), E>`-ও return করতে পারে। Listing 9-12-তে Listing 9-10-এর code আছে, কিন্তু আমরা `main`-এর return type পরিবর্তন করে `Result<(), Box<dyn Error>>` করেছি এবং শেষে একটি return value `Ok(())` যোগ করেছি। এখন এই code compile হবে।

<Listing number="9-12" file-name="src/main.rs" caption="Changing `main` to return `Result<(), E>` allows the use of the `?` operator on `Result` values.">

```rust,ignore
use std::error::Error;
use std::fs::File;

fn main() -> Result<(), Box<dyn Error>> {
    let greeting_file = File::open("hello.txt")?;

    Ok(())
}
```

</Listing>

`Box<dyn Error>` type হলো একটি trait object, যা সম্পর্কে Chapter 18-এর [“Using
Trait Objects to Abstract over Shared Behavior”][trait-objects]<!-- ignore --> section-এ আলোচনা করব। আপাতত, তুমি `Box<dyn Error>`-কে “যেকোনো ধরনের error” হিসেবে পড়তে পারো। `Box<dyn Error>` error type সহ একটি `main` function-এ একটি `Result` value-এর উপর `?` ব্যবহার করা allowed, কারণ এটি যেকোনো `Err` value-কে early return করতে দেয়। যদিও এই `main` function-এর body শুধু `std::io::Error` type-এর error-ই return করবে, `Box<dyn Error>` উল্লেখ করায় এই signature এমনকি `main`-এর body-তে অন্য error return করে এমন আরও code যোগ করা হলেও সঠিক থাকবে।

যখন একটি `main` function `Result<(), E>` return করে, executable-টি `main` যদি `Ok(())` return করে তবে `0` value দিয়ে এবং `main` যদি একটি `Err` value return করে তবে nonzero value দিয়ে exit করবে। C-তে লেখা executable যখন exit করে তখন integer return করে: সফলভাবে exit করা program `0` integer return করে, এবং error করা program `0` ছাড়া অন্য কোনো integer return করে। Rust-ও এই convention-এর সাথে compatible হতে executable থেকে integer return করে।

`main` function এমন যেকোনো type return করতে পারে যা [the
`std::process::Termination` trait][termination]<!-- ignore --> implement করে, যেখানে একটি `report` function আছে যা একটি `ExitCode` return করে। তোমার নিজের type-এর জন্য `Termination` trait implement করা সম্পর্কে আরও তথ্যের জন্য standard library documentation দেখো।

এখন আমরা `panic!` call করা বা `Result` return করার বিস্তারিত আলোচনা করেছি, চলো কোন ক্ষেত্রে কোনটি ব্যবহার করা উপযুক্ত সেই বিষয়ে ফিরে যাই।

[handle_failure]: ch02-00-guessing-game-tutorial.html#handling-potential-failure-with-result
[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[termination]: ../std/process/trait.Termination.html

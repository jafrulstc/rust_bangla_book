## Shared-State Concurrency

message passing হলো concurrency handle করার একটা ভালো পদ্ধতি, কিন্তু একমাত্র পদ্ধতি নয়। আরেকটা পদ্ধতি হলো একাধিক thread-কে একই shared data-এ access করতে দেওয়া। Go language documentation-এর slogan-এর সেই অংশটা আবার ভাবো: “Do not communicate by sharing memory.”

memory share করে communicate করা দেখতে কেমন হবে? আর কেন message-passing enthusiast রা memory sharing ব্যবহার না করতে সতর্ক করবে?

একটা অর্থে, যেকোনো programming language-এর channel গুলো single ownership-এর মতো, কারণ একবার তুমি channel-এ একটা value transfer করলে, সেই value আর ব্যবহার করা উচিত নয়। Shared-memory concurrency হলো multiple ownership-এর মতো: একাধিক thread একই সময়ে একই memory location-এ access পেতে পারে। যেমন Chapter 15-এ দেখেছিলে যে smart pointer multiple ownership সম্ভব করেছে, multiple ownership complexity বাড়িয়ে দেয় কারণ এই ভিন্ন ভিন্ন owner দের manage করতে হয়। Rust-এর type system আর ownership rule এই management সঠিকভাবে করতে অনেক সাহায্য করে। একটা example হিসেবে চলো mutex দেখি, যা shared memory-র জন্য অন্যতম সাধারণ concurrency primitive।

<!-- Old headings. Do not remove or links may break. -->

<a id="using-mutexes-to-allow-access-to-data-from-one-thread-at-a-time"></a>

### Mutex দিয়ে Access নিয়ন্ত্রণ করা

_Mutex_ হলো _mutual exclusion_-এর abbreviation, অর্থাৎ একটা mutex যেকোনো সময়ে শুধু একটা thread-কে কোনো data-এ access করতে দেয়। একটা mutex-এ থাকা data-এ access পেতে একটা thread-কে প্রথমে mutex-এর lock acquire করার অনুরোধ করে signal দিতে হয় যে সে access চায়। _Lock_ হলো এমন একটা data structure যা mutex-এর অংশ আর যা track রাখে বর্তমানে কার data-এ exclusive access আছে। সুতরাং, mutex-কে বলা হয় সে locking system-এর মাধ্যমে যে data সে ধরে রাখে তাকে _guard_ করে।

Mutex-এর difficult-to-use খ্যাতি আছে কারণ তোমাকে দুটো rule মনে রাখতে হয়:

1. তোমাকে data ব্যবহার করার আগে lock acquire করার চেষ্টা করতেই হবে।
2. যখন mutex-এর guard করা data দিয়ে তোমার কাজ শেষ, তখন তোমাকে data unlock করতে হবে যাতে অন্য thread গুলো lock acquire করতে পারে।

mutex-এর একটা real-world metaphor হিসেবে কল্পনা করো একটা conference-এর panel discussion, যেখানে শুধু একটা microphone আছে। একজন panelist কথা বলার আগে তাকে microphone ব্যবহার করতে চাইলে signal দিতে বা অনুরোধ করতে হয়। যখন সে microphone পায়, তখন সে তার ইচ্ছেমতো কথা বলতে পারে আর তারপর পরের panelist কে দিতে পারে যে কথা বলতে চায়। যদি একজন panelist কথা শেষ হলে microphone দিতে ভুলে যায়, তবে আর কেউই কথা বলতে পারবে না। যদি shared microphone-এর management ভুল হয়, তবে panel পরিকল্পনা অনুযায়ী কাজ করবে না!

mutex-এর management ঠিকভাবে করা বেশ কঠিন হতে পারে, তাই অনেকে channel-এ উৎসাহী। কিন্তু Rust-এর type system আর ownership rule-এর জন্য তুমি locking আর unlocking ভুল করতে পারবে না।

#### `Mutex<T>`-এর API

mutex ব্যবহারের একটা example হিসেবে, চলো Listing 16-12-তে দেখানো অনুযায়ী single-threaded context-এ একটা mutex ব্যবহার করা শুরু করি।

<Listing number="16-12" file-name="src/main.rs" caption="Exploring the API of `Mutex<T>` in a single-threaded context for simplicity">

```rust
use std::sync::Mutex;

fn main() {
    let m = Mutex::new(5);

    {
        let mut num = m.lock().unwrap();
        *num = 6;
    }

    println!("m = {m:?}");
}
```

</Listing>

অনেক type-এর মতো, আমরা `Mutex<T>` তৈরি করি associated function `new` ব্যবহার করে। mutex-এর ভেতরের data-এ access পেতে আমরা `lock` method ব্যবহার করে lock acquire করি। এই call বর্তমান thread-কে block করবে যাতে আমাদের lock পাওয়ার পালা না আসা পর্যন্ত সে কোনো কাজ করতে না পারে।

`lock`-এর call ব্যর্থ হবে যদি lock ধরে রাখা অন্য কোনো thread panic করে। সেক্ষেত্রে, কেউই আর lock পাবে না, তাই আমরা `unwrap` choose করেছি যাতে এই পরিস্থিতিতে এই thread-টা panic করে।

lock acquire করার পর, আমরা return value কে — এই ক্ষেত্রে `num` নাম দেওয়া — ভেতরের data-এর একটা mutable reference হিসেবে treat করতে পারি। type system নিশ্চিত করে যে আমরা `m`-এর value ব্যবহার করার আগে একটা lock acquire করি। `m`-এর type হলো `Mutex<i32>`, `i32` নয়, তাই আমরা `i32` value ব্যবহার করতে চাইলে _অবশ্যই_ `lock` call করতে হবে। আমরা ভুলে যেতে পারি না; type system আমাদের ভেতরের `i32`-এ অন্যভাবে access করতে দেবে না।

`lock`-এর call `MutexGuard` নামের একটা type return করে, যা `LockResult`-এ wrap করা থাকে, যেটা আমরা `unwrap` call দিয়ে handle করেছি। `MutexGuard` type `Deref` implement করে যাতে সে আমাদের ভেতরের data-কে point করে; এই type-এর একটা `Drop` implementation আছে যা একটা `MutexGuard` scope থেকে বেরিয়ে গেলে — যা এই inner scope-এর শেষে ঘটে — lock automatically release করে। ফলে, আমরা lock release করতে ভুলে যাওয়ার আর ঝুঁকিতে নেই, কারণ lock release স্বয়ংক্রিয়ভাবে ঘটে।

lock drop করার পর, আমরা mutex-এর value print করতে পারি আর দেখতে পারি যে আমরা ভেতরের `i32` কে `6`-এ পরিবর্তন করতে পেরেছি।

<!-- Old headings. Do not remove or links may break. -->

<a id="sharing-a-mutext-between-multiple-threads"></a>

#### `Mutex<T>`-এ Shared Access

এবার চলো `Mutex<T>` ব্যবহার করে একাধিক thread-এর মধ্যে একটা value share করার চেষ্টা করি। আমরা ১০টা thread তৈরি করব আর প্রত্যেককে একটা counter value ১ করে increment করতে বলব, যাতে counter ০ থেকে ১০-এ যায়। Listing 16-13-এর example-এ একটা compiler error হবে, আর আমরা সেই error কাজে লাগিয়ে `Mutex<T>` ব্যবহার সম্পর্কে আরও জানব আর কীভাবে Rust আমাদের সেটা সঠিকভাবে ব্যবহার করতে সাহায্য করে তা বুঝব।

<Listing number="16-13" file-name="src/main.rs" caption="Ten threads, each incrementing a counter guarded by a `Mutex<T>`">

```rust,ignore,does_not_compile
use std::sync::Mutex;
use std::thread;

fn main() {
    let counter = Mutex::new(0);
    let mut handles = vec![];

    for _ in 0..10 {
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();

            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Result: {}", *counter.lock().unwrap());
}
```

</Listing>

আমরা Listing 16-12-এর মতো করে একটা `i32` কে `Mutex<T>`-এর ভেতর রেখে একটা `counter` variable তৈরি করি। এরপর আমরা এক range number-এর উপর iterate করে ১০টা thread তৈরি করি। আমরা `thread::spawn` ব্যবহার করি আর সব thread-কে একই closure দিই: এমন একটা যা counter কে thread-এ move করে, `lock` method call করে `Mutex<T>`-এ একটা lock acquire করে, আর তারপর mutex-এর value-এর সাথে ১ যোগ করে। যখন একটা thread তার closure run করা শেষ করে, `num` scope থেকে বেরিয়ে যাবে আর lock release করবে যাতে অন্য thread সেটা acquire করতে পারে।

main thread-এ আমরা সব join handle সংগ্রহ করি। তারপর, Listing 16-2-এর মতো, আমরা প্রতিটি handle-এ `join` call করি যাতে সব thread শেষ হয় তা নিশ্চিত করি। সেই মুহূর্তে, main thread lock acquire করবে আর এই program-এর result print করবে।

আমরা ইঙ্গিত দিয়েছিলাম যে এই example compile হবে না। এবার দেখি কেন!

```console
$ cargo run
   Compiling shared-state v0.1.0 (file:///projects/shared-state)
error[E0382]: borrow of moved value: `counter`
  --> src/main.rs:21:29
   |
 5 |     let counter = Mutex::new(0);
   |         ------- move occurs because `counter` has type `std::sync::Mutex<i32>`, which does not implement the `Copy` trait
...
 8 |     for _ in 0..10 {
   |     -------------- inside of this loop
 9 |         let handle = thread::spawn(move || {
   |                                    ------- value moved into closure here, in previous iteration of loop
...
21 |     println!("Result: {}", *counter.lock().unwrap());
   |                             ^^^^^^^ value borrowed here after move

For more information about this error, try `rustc --explain E0382`.
error: could not compile `shared-state` (bin "shared-state") due to 1 previous error
```

error message বলছে যে `counter` value টা loop-এর previous iteration-এ move হয়েছে। Rust আমাদের বলছে যে আমরা `counter` lock-এর ownership একাধিক thread-এ move করতে পারি না। চলো Chapter 15-এ আলোচিত multiple-ownership method দিয়ে compiler error ঠিক করি।

#### একাধিক Thread-এর সাথে Multiple Ownership

Chapter 15-এ আমরা smart pointer `Rc<T>` ব্যবহার করে একটা value কে একাধিক owner-এ দিয়েছিলাম, যাতে একটা reference-counted value তৈরি হয়। চলো এখানেও একই করি আর দেখি কী হয়। Listing 16-14-তে আমরা `Mutex<T>`-কে `Rc<T>`-এ wrap করব আর thread-এ ownership move করার আগে `Rc<T>` কে clone করব।

<Listing number="16-14" file-name="src/main.rs" caption="Attempting to use `Rc<T>` to allow multiple threads to own the `Mutex<T>`">

```rust,ignore,does_not_compile
use std::rc::Rc;
use std::sync::Mutex;
use std::thread;

fn main() {
    let counter = Rc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Rc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();

            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Result: {}", *counter.lock().unwrap());
}
```

</Listing>

আবারও compile করলে... ভিন্ন error পাই! Compiler আমাদের অনেক কিছু শেখাচ্ছে:

```console
$ cargo run
   Compiling shared-state v0.1.0 (file:///projects/shared-state)
error[E0277]: `Rc<std::sync::Mutex<i32>>` cannot be sent between threads safely
  --> src/main.rs:11:36
   |
11 |           let handle = thread::spawn(move || {
   |                        ------------- ^------
   |                        |             |
   |  ______________________|_____________within this `{closure@src/main.rs:11:36: 11:43}`
   | |                      |
   | |                      required by a bound introduced by this call
12 | |             let mut num = counter.lock().unwrap();
13 | |
14 | |             *num += 1;
15 | |         });
   | |_________^ `Rc<std::sync::Mutex<i32>>` cannot be sent between threads safely
   |
   = help: within `{closure@src/main.rs:11:36: 11:43}`, the trait `Send` is not implemented for `Rc<std::sync::Mutex<i32>>`
note: required because it's used within this closure
  --> src/main.rs:11:36
   |
11 |         let handle = thread::spawn(move || {
   |                                    ^^^^^^^
note: required by a bound in `spawn`
  --> /rustc/88d9e12ae178fab0fb5cc050a94da85685d449ea/library/std/src/thread/functions.rs:125:0

For more information about this error, try `rustc --explain E0277`.
error: could not compile `shared-state` (bin "shared-state") due to 1 previous error
```

ওহ, error message-টা বেশ বড়! যে অংশে মনোযোগ দিতে হবে তা হলো: `` `Rc<Mutex<i32>>` cannot be sent between threads safely ``। Compiler আমাকে কারণও বলছে: `` the trait `Send` is not implemented for `Rc<Mutex<i32>>` ``। আমরা পরের section-এ `Send` নিয়ে কথা বলব: এটি এমন এক trait যা নিশ্চিত করে যে thread-এর সাথে আমরা যে type গুলো ব্যবহার করি সেগুলো concurrent পরিস্থিতিতে ব্যবহারের জন্যই তৈরি।

দুর্ভাগ্যবশত, `Rc<T>` thread-এর মধ্যে share করা safe নয়। যখন `Rc<T>` reference count manage করে, তখন সে প্রতিটি `clone` call-এ count-এ যোগ করে আর প্রতিটি clone drop হলে count থেকে বিয়োগ করে। কিন্তু সে কোনো concurrency primitive ব্যবহার করে না যাতে count-এ পরিবর্তন অন্য thread দ্বারা interrupt না হয়। এতে wrong count হতে পারে—subtle bug যা আবার memory leak বা আমরা কাজ শেষ করার আগেই value drop হয়ে যাওয়ার কারণ হতে পারে। আমাদের দরকার এমন একটা type যা ঠিক `Rc<T>`-এর মতো, কিন্তু যা thread-safe ভাবে reference count-এ পরিবর্তন করে।

#### `Arc<T>` দিয়ে Atomic Reference Counting

সৌভাগ্যক্রমে, `Arc<T>` _হলো_ `Rc<T>`-এর মতো এমন এক type যা concurrent পরিস্থিতিতে ব্যবহার করা safe। _a_ দাঁড়িয়েছে _atomic_-এর জন্য, যার মানে এটি একটি _atomically reference-counted_ type। Atomic হলো আরেক ধরনের concurrency primitive যা আমরা এখানে বিস্তারিত cover করব না: আরও বিস্তারিত জানতে standard library documentation-এর [`std::sync::atomic`][atomic]<!-- ignore --> দেখো। এই মুহূর্তে, তোমার শুধু এটুকু জানা দরকার যে atomic গুলো primitive type-এর মতো কাজ করে কিন্তু thread-এর মধ্যে share করা safe।

তুমি ভাবতে পারো কেন সব primitive type atomic নয় আর কেন standard library type গুলো default-ভাবে `Arc<T>` ব্যবহার করতে বানানো নয়। কারণ হলো thread safety এর সাথে একটা performance penalty আসে যা তুমি শুধু সত্যিই দরকার হলেই pay করতে চাইবে। যদি তুমি শুধু single thread-এ value-এর উপর operation করো, তবে তোমার code দ্রুত run করতে পারে যদি সে atomic-এর guarantee enforce করতে না হয়।

চলো আমাদের example-এ ফিরে যাই: `Arc<T>` আর `Rc<T>`-এর API একই, তাই আমরা `use` line, `new` call আর `clone` call পরিবর্তন করে আমাদের program ঠিক করি। Listing 16-15-এর code অবশেষে compile হবে আর run করবে।

<Listing number="16-15" file-name="src/main.rs" caption="Using an `Arc<T>` to wrap the `Mutex<T>` to be able to share ownership across multiple threads">

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();

            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Result: {}", *counter.lock().unwrap());
}
```

</Listing>

এই code নিচের মতো print করবে:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Result: 10
```

আমরা পেরেছি! আমরা ০ থেকে ১০ পর্যন্ত count করেছি, যেটা খুব চমৎকার মনে নাও হতে পারে, কিন্তু এটা `Mutex<T>` আর thread safety সম্পর্কে অনেক কিছু শিখিয়েছে। তুমি এই program-এর structure কাজে লাগিয়ে শুধু counter increment করার চেয়ে আরও জটিল operation ও করতে পারো। এই কৌশল ব্যবহার করে তুমি একটা calculation-কে স্বাধীন অংশে ভাগ করতে পারো, সেই অংশ গুলো thread-এ ভাগ করতে পারো, আর তারপর একটা `Mutex<T>` ব্যবহার করে প্রতিটি thread-কে তার অংশ দিয়ে final result update করতে পারো।

খেয়াল করো, তুমি যদি simple numerical operation করো, তবে standard library-র [`std::sync::atomic` module][atomic]<!-- ignore -->-এ `Mutex<T>`-এর চেয়ে সরল কিছু type দেওয়া আছে। এই type গুলো primitive type-এ safe, concurrent, atomic access দেয়। আমরা এই example-এ primitive type-এর সাথে `Mutex<T>` choose করেছি যাতে আমরা `Mutex<T>` কীভাবে কাজ করে সেদিকে মনোযোগ দিতে পারি।

<!-- Old headings. Do not remove or links may break. -->

<a id="similarities-between-refcelltrct-and-mutextarct"></a>

### `RefCell<T>`/`Rc<T>` এবং `Mutex<T>`/`Arc<T>` তুলনা

তুমি খেয়াল করে থাকতে পারো যে `counter` immutable কিন্তু আমরা তার ভেতরের value-এর একটা mutable reference পেয়েছি; এর মানে `Mutex<T>` interior mutability provide করে, যেমন `Cell` family করে। Chapter 15-এ আমরা যেভাবে `Rc<T>`-এর ভেতরের content mutate করার জন্য `RefCell<T>` ব্যবহার করেছিলাম, একইভাবে আমরা `Arc<T>`-এর ভেতরের content mutate করার জন্য `Mutex<T>` ব্যবহার করি।

আরেকটা বিস্তার খেয়াল করার মতো — তুমি `Mutex<T>` ব্যবহার করলে Rust তোমাকে সব ধরনের logic error থেকে রক্ষা করতে পারে না। Chapter 15 থেকে মনে করো যে `Rc<T>` ব্যবহার করলে reference cycle তৈরির ঝুঁকি ছিল, যেখানে দুটো `Rc<T>` value একে অপরকে refer করে, ফলে memory leak হয়। একইভাবে, `Mutex<T>` এর সাথে _deadlock_ তৈরির ঝুঁকি আছে। এগুলো ঘটে যখন একটা operation-কে দুটো resource lock করতে হয় আর দুটো thread প্রত্যেকে একটা করে lock acquire করে রেখেছে, ফলে তারা চিরকাল একে অপরের জন্য অপেক্ষা করে। তুমি যদি deadlock-এ আগ্রহী হও, একটা Rust program তৈরি করো যাতে deadlock থাকে; তারপর যেকোনো language-এর mutex-এর জন্য deadlock mitigation strategy নিয়ে research করো আর সেগুলো Rust-এ implement করার চেষ্টা করো। `Mutex<T>` আর `MutexGuard`-এর standard library API documentation useful তথ্য দেয়।

আমরা এই chapter `Send` আর `Sync` trait নিয়ে আলোচনা করে শেষ করব আর দেখব কীভাবে সেগুলো custom type-এর সাথে ব্যবহার করতে পারি।

[atomic]: ../std/sync/atomic/index.html

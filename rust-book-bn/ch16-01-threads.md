## Thread ব্যবহার করে একই সময়ে Code Run করা

বর্তমান বেশিরভাগ operating system-এ, একটা executed program-এর code একটা _process_-এ run হয়, আর operating system একসাথে একাধিক process পরিচালনা করে। একটা program-এর ভেতরেও তুমি এমন স্বাধীন অংশ রাখতে পারো যা একই সময়ে run করে। এই স্বাধীন অংশগুলোকে run করানো feature-কে _thread_ বলা যায়। যেমন, একটা web server-এ একাধিক thread থাকতে পারে যাতে একই সময়ে একাধিক request-এ সাড়া দিতে পারে।

তোমার program-এর computation-কে একাধিক thread-এ ভাগ করে একই সময়ে একাধিক task run করলে performance বাড়তে পারে, কিন্তু সাথে complexity-ও বাড়ে। কারণ thread গুলো একই সময়ে run হতে পারে, তাই ভিন্ন ভিন্ন thread-এ থাকা তোমার code-এর অংশগুলো কোন ক্রমে run হবে সে ব্যাপারে কোনো inherent guarantee নেই। এতে নিচের মতো সমস্যা হতে পারে:

- Race condition, যেখানে thread গুলো অসামঞ্জস্যপূর্ণ ক্রমে data বা resource access করে
- Deadlock, যেখানে দুটো thread একে অপরের জন্য অপেক্ষা করে, ফলে দুটোই এগোতে পারে না
- এমন bug যা শুধু নির্দিষ্ট কিছু পরিস্থিতিতে ঘটে আর reliably reproduce করে ঠিক করা কঠিন

thread ব্যবহারের নেতিবাচক প্রভাব কমানোর চেষ্টা Rust করে, কিন্তু multithreaded context-এ programming করতে এখনও সতর্ক চিন্তা দরকার আর single thread-এ চলা program থেকে ভিন্ন এক ধরনের code structure প্রয়োজন।

Programming language গুলো কয়েকভাবে thread implement করে, আর অনেক operating system এমন একটা API দেয় যা language নতুন thread তৈরির জন্য call করতে পারে। Rust standard library thread implementation-এর _1:1_ model ব্যবহার করে, অর্থাৎ একটা language thread-এর জন্য একটা operating system thread। এমন crate আছে যা 1:1 model থেকে ভিন্ন trade-off সহ আরও কিছু threading model implement করে। (পরের chapter-এ দেখা যাবে এমন Rust-এর async system, যা concurrency-এর আরেকটা পদ্ধতি দেয়।)

### `spawn` দিয়ে নতুন Thread তৈরি করা

নতুন thread তৈরি করতে আমরা `thread::spawn` function কে call করি আর একে একটা closure পাস করি (Chapter 13-এ closure নিয়ে আলোচনা করেছিলাম) যেটায় নতুন thread-এ run করার মতো code থাকে। Listing 16-1-এর example একটা main thread থেকে কিছু text আর আরেকটা নতুন thread থেকে অন্য text print করে।

<Listing number="16-1" file-name="src/main.rs" caption="Creating a new thread to print one thing while the main thread prints something else">

```rust
use std::thread;
use std::time::Duration;

fn main() {
    thread::spawn(|| {
        for i in 1..10 {
            println!("hi number {i} from the spawned thread!");
            thread::sleep(Duration::from_millis(1));
        }
    });

    for i in 1..5 {
        println!("hi number {i} from the main thread!");
        thread::sleep(Duration::from_millis(1));
    }
}
```

</Listing>

খেয়াল করো, যখন একটা Rust program-এর main thread শেষ হয়, তখন সব spawned thread shut down হয়ে যায়, তারা কাজ শেষ করেছে কি না তা বিবেচ্য নয়। এই program-এর output প্রতিবার একটু ভিন্ন হতে পারে, কিন্তু নিচের মতো দেখাবে:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the main thread!
hi number 1 from the spawned thread!
hi number 2 from the main thread!
hi number 2 from the spawned thread!
hi number 3 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the main thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
```

`thread::sleep`-এর call একটা thread-কে সাময়িকভাবে তার execution থামিয়ে দেয়, ফলে অন্য একটা thread run করতে পারে। thread গুলো সম্ভবত পালা করে চলবে, কিন্তু সেটাই হবে এমন কোনো guarantee নেই: এটা নির্ভর করে তোমার operating system কীভাবে thread schedule করে তার উপর। এই run-এ, main thread আগে print করেছে, যদিও spawned thread-এর print statement code-এ আগে আছে। আর যদিও আমরা spawned thread-কে `i` `9` হওয়া পর্যন্ত print করতে বলেছি, সে শুধু `5` পর্যন্ত পৌঁছেছে মূল thread shut down হওয়ার আগে।

তুমি যদি এই code run করো আর শুধু main thread-এর output দেখো, বা কোনো overlap না দেখো, range-এর সংখ্যা বাড়িয়ে দেখো — তাহলে operating system-এর জন্য thread গুলোর মধ্যে switch করার সুযোগ বাড়বে।

<!-- Old headings. Do not remove or links may break. -->

<a id="waiting-for-all-threads-to-finish-using-join-handles"></a>

### সব Thread-এর শেষ হওয়া পর্যন্ত অপেক্ষা করা

Listing 16-1-এর code বেশিরভাগ সময় main thread শেষ হয়ে যাওয়ার কারণে spawned thread-কে সময়ের আগেই থামিয়ে দেয়, কিন্তু যেহেতু thread গুলো কোন ক্রমে run হবে তার কোনো guarantee নেই, তাই আমরা এটাও guarantee দিতে পারি না যে spawned thread আদৌ run হবে কি না!

spawned thread না চলা বা সময়ের আগে শেষ হয়ে যাওয়ার সমস্যা আমরা ঠিক করতে পারি `thread::spawn`-এর return value একটা variable-এ সংরক্ষণ করে। `thread::spawn`-এর return type হলো `JoinHandle<T>`। `JoinHandle<T>` একটা owned value, যার উপর আমরা `join` method call করলে সে তার thread শেষ হওয়া পর্যন্ত অপেক্ষা করে। Listing 16-2 দেখায় কীভাবে Listing 16-1-এ তৈরি করা thread-এর `JoinHandle<T>` ব্যবহার করব আর `join` call করব যাতে নিশ্চিত হই spawned thread `main` exit করার আগে শেষ হয়েছে।

<Listing number="16-2" file-name="src/main.rs" caption="Saving a `JoinHandle<T>` from `thread::spawn` to guarantee the thread is run to completion">

```rust
use std::thread;
use std::time::Duration;

fn main() {
    let handle = thread::spawn(|| {
        for i in 1..10 {
            println!("hi number {i} from the spawned thread!");
            thread::sleep(Duration::from_millis(1));
        }
    });

    for i in 1..5 {
        println!("hi number {i} from the main thread!");
        thread::sleep(Duration::from_millis(1));
    }

    handle.join().unwrap();
}
```

</Listing>

handle-এর উপর `join` call করলে বর্তমানে চলা thread block হয়ে যায় যতক্ষণ না handle-এর দ্বারা প্রতিনিধিত্ব করা thread terminate হয়। কোনো thread-কে _block_ করা মানে সেই thread-কে কোনো কাজ করতে বা exit করতে বাধা দেওয়া। যেহেতু আমরা `join`-এর call main thread-এর `for` loop-এর পরে রেখেছি, তাই Listing 16-2 run করলে নিচের মতো output আসবে:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 1 from the spawned thread!
hi number 3 from the main thread!
hi number 2 from the spawned thread!
hi number 4 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
```

দুটো thread পালাক্রমে চলতেই থাকে, কিন্তু `handle.join()` call-এর কারণে main thread অপেক্ষা করে আর spawned thread শেষ না হলে শেষ হয় না।

কিন্তু দেখি কী হয় যদি আমরা `handle.join()`-কে `main`-এর `for` loop-এর আগে নিয়ে যাই, এভাবে:

<Listing file-name="src/main.rs">

```rust
use std::thread;
use std::time::Duration;

fn main() {
    let handle = thread::spawn(|| {
        for i in 1..10 {
            println!("hi number {i} from the spawned thread!");
            thread::sleep(Duration::from_millis(1));
        }
    });

    handle.join().unwrap();

    for i in 1..5 {
        println!("hi number {i} from the main thread!");
        thread::sleep(Duration::from_millis(1));
    }
}
```

</Listing>

main thread spawned thread শেষ হওয়া পর্যন্ত অপেক্ষা করবে আর তারপর নিজের `for` loop run করবে, তাই output আর interleave হবে না, যেমনটা এখানে দেখানো হলো:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the spawned thread!
hi number 2 from the spawned thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 3 from the main thread!
hi number 4 from the main thread!
```

এমন ছোট বিস্তার, যেমন `join` কোথায় call করা হয়েছে, তা প্রভাব ফেলতে পারে তোমার thread গুলো একই সময়ে চলবে কি না।

### Thread-এর সাথে `move` Closure ব্যবহার করা

আমরা প্রায়ই `thread::spawn`-এ পাস করা closure-এর সাথে `move` keyword ব্যবহার করব, কারণ তাতে closure তার environment থেকে যে value গুলো ব্যবহার করে সেগুলোর ownership নিয়ে নেবে, ফলে সেই value গুলোর ownership এক thread থেকে অন্য thread-এ transfer হয়। Chapter 13-এর [“Capturing References or Moving Ownership”][capture]<!-- ignore
--> section-এ আমরা closure-এর context-এ `move` নিয়ে আলোচনা করেছি। এখন আমরা `move` আর `thread::spawn`-এর interaction-এর উপর বেশি মনোযোগ দেব।

খেয়াল করো Listing 16-1-এ, আমরা `thread::spawn`-কে যে closure পাস করেছি সেটার কোনো argument নেই: আমরা spawned thread-এর code-এ main thread-এর কোনো data ব্যবহার করছি না। main thread-এর কোনো data spawned thread-এ ব্যবহার করতে হলে, spawned thread-এর closure-কে তার দরকারি value capture করতে হবে। Listing 16-3-এ main thread-এ একটা vector তৈরি করে সেটা spawned thread-এ ব্যবহার করার চেষ্টা দেখানো হলো। কিন্তু এটা এখনও কাজ করবে না, যেমন একটু পরেই দেখা যাবে।

<Listing number="16-3" file-name="src/main.rs" caption="Attempting to use a vector created by the main thread in another thread">

```rust,ignore,does_not_compile
use std::thread;

fn main() {
    let v = vec![1, 2, 3];

    let handle = thread::spawn(|| {
        println!("Here's a vector: {v:?}");
    });

    handle.join().unwrap();
}
```

</Listing>

closure টা `v` ব্যবহার করে, তাই সে `v`-কে capture করবে আর তাকে closure-এর environment-এর অংশ করে নেবে। যেহেতু `thread::spawn` এই closure টা নতুন একটা thread-এ run করে, আমাদের সেই নতুন thread-এর ভেতরে `v`-তে access পাওয়ার কথা। কিন্তু এই example compile করালে আমরা নিচের error পাই:

```console
$ cargo run
   Compiling threads v0.1.0 (file:///projects/threads)
error[E0373]: closure may outlive the current function, but it borrows `v`, which is owned by the current function
 --> src/main.rs:6:32
  |
6 |     let handle = thread::spawn(|| {
  |                                ^^ may outlive borrowed value `v`
7 |         println!("Here's a vector: {v:?}");
  |                                     - `v` is borrowed here
  |
note: function requires argument type to outlive `'static`
 --> src/main.rs:6:18
  |
6 |       let handle = thread::spawn(|| {
  |  __________________^
7 | |         println!("Here's a vector: {v:?}");
8 | |     });
  | |______^
help: to force the closure to take ownership of `v` (and any other referenced variables), use the `move` keyword
  |
6 |     let handle = thread::spawn(move || {
  |                                ++++

For more information about this error, try `rustc --explain E0373`.
error: could not compile `threads` (bin "threads") due to 1 previous error
```

Rust `v`-কে কীভাবে capture করবে তা _infer_ করে, আর যেহেতু `println!`-এর শুধু `v`-এর একটা reference দরকার, তাই closure চেষ্টা করে `v`-কে borrow করতে। কিন্তু এতে একটা সমস্যা আছে: Rust বুঝতে পারে না spawned thread কতক্ষণ run করবে, তাই সে জানে না `v`-এর reference সব সময় valid থাকবে কি না।

Listing 16-4 এমন একটা পরিস্থিতি দেখায় যেখানে `v`-এর এমন একটা reference থাকার সম্ভাবনা বেশি যেটা valid থাকবে না।

<Listing number="16-4" file-name="src/main.rs" caption="A thread with a closure that attempts to capture a reference to `v` from a main thread that drops `v`">

```rust,ignore,does_not_compile
use std::thread;

fn main() {
    let v = vec![1, 2, 3];

    let handle = thread::spawn(|| {
        println!("Here's a vector: {v:?}");
    });

    drop(v); // oh no!

    handle.join().unwrap();
}
```

</Listing>

যদি Rust আমাদের এই code run করতে দিত, তাহলে এমন সম্ভাবনা থাকত যে spawned thread একেবারে background-এ চলে যাবে আর আদৌ run হবে না। spawned thread-এর ভেতরে `v`-এর একটা reference আছে, কিন্তু main thread সাথে সাথে Chapter 15-এ আলোচিত `drop` function দিয়ে `v`-কে drop করে দেয়। তারপর যখন spawned thread execute হতে শুরু করে, `v` আর valid থাকে না, তাই তার reference-টাও invalid। ওহ না!

Listing 16-3-এর compiler error ঠিক করতে আমরা error message-এর পরামর্শ ব্যবহার করতে পারি:

<!-- manual-regeneration
after automatic regeneration, look at listings/ch16-fearless-concurrency/listing-16-03/output.txt and copy the relevant part
-->

```text
help: to force the closure to take ownership of `v` (and any other referenced variables), use the `move` keyword
  |
6 |     let handle = thread::spawn(move || {
  |                                ++++
```

closure-এর আগে `move` keyword যোগ করে আমরা closure-কে বাধ্য করি যে সে যে value গুলো ব্যবহার করছে সেগুলোর ownership নিয়ে নেবে, Rust-কে সেগুলো borrow করার inference করতে দেবে না। Listing 16-3-এর এই পরিবর্তন, যা Listing 16-5-এ দেখানো হয়েছে, compile হবে আর আমরা যা চাই তেমনভাবে run করবে।

<Listing number="16-5" file-name="src/main.rs" caption="Using the `move` keyword to force a closure to take ownership of the values it uses">

```rust
use std::thread;

fn main() {
    let v = vec![1, 2, 3];

    let handle = thread::spawn(move || {
        println!("Here's a vector: {v:?}");
    });

    handle.join().unwrap();
}
```

</Listing>

আমাদের মনে হতে পারে যে Listing 16-4-এর code-এ, যেখানে main thread `drop` call করেছে, সেটা ঠিক করতেও একই `move` closure ব্যবহার করা যাবে। কিন্তু এই fix কাজ করবে না, কারণ Listing 16-4 যা করতে চায় সেটা অন্য কারণে disallow। যদি আমরা closure-এ `move` যোগ করতাম, তাহলে `v`-কে closure-এর environment-এ move করে নিতাম, আর main thread-এ তার উপর আর `drop` call করতে পারতাম না। তখন আমরা এই compiler error পেতাম:

```console
$ cargo run
   Compiling threads v0.1.0 (file:///projects/threads)
error[E0382]: use of moved value: `v`
  --> src/main.rs:10:10
   |
 4 |     let v = vec![1, 2, 3];
   |         - move occurs because `v` has type `Vec<i32>`, which does not implement the `Copy` trait
 5 |
 6 |     let handle = thread::spawn(move || {
   |                                ------- value moved into closure here
 7 |         println!("Here's a vector: {v:?}");
   |                                     - variable moved due to use in closure
...
10 |     drop(v); // oh no!
   |          ^ value used here after move
   |
help: consider cloning the value before moving it into the closure
   |
 6 ~     let value = v.clone();
 7 ~     let handle = thread::spawn(move || {
 8 ~         println!("Here's a vector: {value:?}");
   |

For more information about this error, try `rustc --explain E0382`.
error: could not compile `threads` (bin "threads") due to 1 previous error
```

Rust-এর ownership rule আবারও আমাদের বাঁচিয়েছে! Listing 16-3-এর code থেকে আমরা error পেয়েছিলাম কারণ Rust conservative ছিল আর thread-এর জন্য `v`-কে শুধু borrow করছিল, যার মানে main thread theoretically ভাবে spawned thread-এর reference invalid করে দিতে পারত। Rust-কে `v`-এর ownership spawned thread-এ move করতে বলে আমরা Rust-কে guarantee দিচ্ছি যে main thread আর `v` ব্যবহার করবে না। যদি আমরা Listing 16-4-এও একইভাবে পরিবর্তন করি, তাহলে main thread-এ `v` ব্যবহার করার চেষ্টা করলে আমরা ownership rule ভাঙছি। `move` keyword, Rust-এর borrow করার conservative default-কে override করে; এটা ownership rule ভাঙতে দেয় না।

এখন যেহেতু আমরা thread কী আর thread API যেসব method দেয় সেটা cover করেছি, চলো দেখি এমন কিছু পরিস্থিতি যেখানে আমরা thread ব্যবহার করতে পারি।

[capture]: ch13-01-closures.html#capturing-references-or-moving-ownership

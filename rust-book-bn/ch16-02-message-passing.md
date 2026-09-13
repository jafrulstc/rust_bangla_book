<!-- Old headings. Do not remove or links may break. -->

<a id="using-message-passing-to-transfer-data-between-threads"></a>

## Message Passing দিয়ে Thread-এর মধ্যে Data Transfer করা

safe concurrency নিশ্চিত করার একটা ক্রমশ জনপ্রিয় পদ্ধতি হলো message passing, যেখানে thread বা actor গুলো একে অপরের সাথে data-সহ message পাঠিয়ে communicate করে। এই ভাবনাটি [Go language documentation](https://golang.org/doc/effective_go.html#concurrency)-এর একটা slogan-এ আছে: “Do not communicate by sharing memory; instead, share memory by communicating.”

message-sending concurrency করতে Rust-এর standard library channel-এর একটা implementation দেয়। _Channel_ হলো একটা সাধারণ programming concept যার মাধ্যমে এক thread থেকে অন্য thread-এ data পাঠানো হয়।

programming-এর channel-কে তুমি এমন একটা directional water channel হিসেবে কল্পনা করতে পারো, যেমন একটা stream বা নদী। তুমি যদি একটা rubber duck-এর মতো কিছু নদীতে ছেড়ে দাও, সেটা downstream-এ ভেসে যাবে আর waterway-এর শেষে পৌঁছাবে।

channel-এর দুটো অংশ থাকে: একটা transmitter আর একটা receiver। transmitter অংশটি হলো upstream-এর সেই স্থান যেখানে তুমি rubber duck-টা নদীতে ছাড়ো, আর receiver অংশটি হলো সেই জায়গা যেখানে rubber duck-টা downstream-এ গিয়ে পৌঁছায়। তোমার code-এর এক অংশ transmitter-এর উপর method call করে যে data পাঠাতে চায় পাঠায়, আর অন্য অংশ receiving-এর দিকে আসা message-এর জন্য check করে। যদি transmitter বা receiver কোনো অংশ drop হয়ে যায়, তবে বলা হয় channel _closed_ হয়ে গেছে।

এখানে আমরা এমন একটা program তৈরি করব যার একটা thread value গুলো generate করে সেগুলো channel-এ পাঠাবে, আর আরেকটা thread সেই value গুলো receive করে print করবে। আমরা channel ব্যবহার করে thread-এর মধ্যে simple value পাঠাব, যাতে feature-টা বোঝানো যায়। এই technique-এর সাথে পরিচিত হলে তুমি যেকোনো thread-এর মধ্যে communicate করার জন্য channel ব্যবহার করতে পারবে, যেমন একটা chat system বা এমন একটা system যেখানে অনেক thread এক calculation-এর কিছু অংশ করে সেই অংশ গুলো একটা thread-এ পাঠায় যেটা result aggregate করে।

প্রথমে, Listing 16-6-তে আমরা একটা channel তৈরি করব কিন্তু সাথে সাথে কিছু করব না। খেয়াল করো এটা এখনও compile হবে না কারণ Rust বুঝতে পারে না আমরা channel-এ কোন type-এর value পাঠাতে চাই।

<Listing number="16-6" file-name="src/main.rs" caption="Creating a channel and assigning the two halves to `tx` and `rx`">

```rust,ignore,does_not_compile
use std::sync::mpsc;

fn main() {
    let (tx, rx) = mpsc::channel();
}
```

</Listing>

আমরা `mpsc::channel` function দিয়ে নতুন channel তৈরি করি; `mpsc` হলো _multiple producer, single consumer_-এর সংক্ষিপ্ত রূপ। সংক্ষেপে, Rust-এর standard library যেভাবে channel implement করে তার মানে হলো একটা channel-এ একাধিক _sending_ end থাকতে পারে যা value produce করে, কিন্তু শুধু একটাই _receiving_ end থাকে যা সেই value গুলো consume করে। কল্পনা করো একাধিক stream একসাথে একটা বড় নদীতে মিলিত হচ্ছে: যেকোনো stream-এ যা পাঠানো হবে শেষে সেই এক নদীতেই গিয়ে পৌঁছাবে। আপাতত আমরা একটা single producer দিয়ে শুরু করব, কিন্তু এই example কাজ করার পর আমরা একাধিক producer যোগ করব।

`mpsc::channel` function একটা tuple return করে, যার প্রথম element হলো sending end—transmitter—আর দ্বিতীয় element হলো receiving end—receiver। `tx` আর `rx` abbreviation টা অনেক field-এ প্রচলিতভাবে _transmitter_ আর _receiver_-এর জন্য ব্যবহৃত হয়, তাই আমরা আমাদের variable-গুলোর নাম সেভাবে রেখে প্রতিটি end নির্দেশ করছি। আমরা একটা `let` statement ব্যবহার করছি এমন এক pattern সহ যা tuple-কে destructure করে; `let` statement-এ pattern-এর ব্যবহার আর destructuring নিয়ে আমরা Chapter 19-এ আলোচনা করব। আপাতত, এটুকু জেনো যে এভাবে `let` statement ব্যবহার করা `mpsc::channel` থেকে return হওয়া tuple-এর অংশগুলো বের করার একটা সুবিধাজনক পদ্ধতি।

চলো transmitting end-টা spawned thread-এ move করি আর সেটাকে একটা string পাঠাতে বলি, যাতে spawned thread-টা main thread-এর সাথে communicate করে, যেমন Listing 16-7-তে দেখানো হয়েছে। এটা ঠিক উপরের দিকে নদীতে rubber duck ছাড়ার মতো বা এক thread থেকে অন্য thread-এ chat message পাঠানোর মতো।

<Listing number="16-7" file-name="src/main.rs" caption='Moving `tx` to a spawned thread and sending `"hi"`'>

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let val = String::from("hi");
        tx.send(val).unwrap();
    });
}
```

</Listing>

আবারও, আমরা `thread::spawn` ব্যবহার করে নতুন thread তৈরি করছি আর তারপর `move` ব্যবহার করে `tx`-কে closure-এ move করছি যাতে spawned thread `tx`-এর ownership পায়। spawned thread-কে channel-এর মাধ্যমে message পাঠাতে হলে transmitter-এর ownership থাকা দরকার।

transmitter-এ একটা `send` method আছে যেটা আমরা যে value পাঠাতে চাই সেটা নেয়। `send` method একটা `Result<T, E>` type return করে, তাই যদি receiver ইতিমধ্যে drop হয়ে যায় আর value পাঠানোর কোনো জায়গা না থাকে, তবে send operation একটা error return করবে। এই example-এ আমরা error হলে panic করার জন্য `unwrap` call করছি। কিন্তু একটা real application-এ আমরা সেটা সঠিকভাবে handle করতাম: proper error handling strategy-র জন্য Chapter 9-এ ফিরে যাও।

Listing 16-8-তে আমরা main thread-এ receiver থেকে value পাব। এটা নদীর শেষে জল থেকে rubber duck তুলে নেওয়ার মতো বা এক chat message receive করার মতো।

<Listing number="16-8" file-name="src/main.rs" caption='Receiving the value `"hi"` in the main thread and printing it'>

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let val = String::from("hi");
        tx.send(val).unwrap();
    });

    let received = rx.recv().unwrap();
    println!("Got: {received}");
}
```

</Listing>

receiver-এর দুটো useful method আছে: `recv` আর `try_recv`। আমরা `recv` ব্যবহার করছি, _receive_-এর সংক্ষিপ্ত রূপ, যেটা main thread-এর execution block করে আর channel-এ একটা value পাঠানো পর্যন্ত অপেক্ষা করে। একবার কোনো value পাঠানো হলে, `recv` সেটাকে একটা `Result<T, E>`-এ return করে। যখন transmitter close হয়ে যায়, `recv` একটা error return করে যাতে বোঝানো হয় যে আর কোনো value আসবে না।

`try_recv` method block করে না, বরং সাথে সাথে একটা `Result<T, E>` return করে: কোনো message available থাকলে তাকে ধরে একটা `Ok` value, আর এবারে কোনো message না থাকলে একটা `Err` value। যদি এই thread-এর message-এর জন্য অপেক্ষা করার সময় অন্য কাজ থাকে, তবে `try_recv` কাজে লাগে: আমরা এমন একটা loop লিখতে পারি যা মাঝে মাঝে `try_recv` call করে, কোনো message available থাকলে সেটা handle করে, আর না থাকলে কিছুক্ষণ অন্য কাজ করে আবার check করে।

এই example-এ সরলতার জন্য আমরা `recv` ব্যবহার করেছি; message-এর জন্য অপেক্ষা করা ছাড়া main thread-এর করার অন্য কোনো কাজ নেই, তাই main thread-কে block করাটাই মানানসই।

Listing 16-8-এর code run করলে, আমরা main thread থেকে value টা print হতে দেখব:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
```

দারুণ!

<!-- Old headings. Do not remove or links may break. -->

<a id="channels-and-ownership-transference"></a>

### Channel-এর মাধ্যমে Ownership Transfer করা

message sending-এ ownership rule অত্যন্ত গুরুত্বপূর্ণ ভূমিকা পালন করে, কারণ এগুলো তোমাকে safe, concurrent code লিখতে সাহায্য করে। concurrent programming-এ error প্রতিরোধ করাই হলো তোমার সম্পূর্ণ Rust program জুড়ে ownership নিয়ে ভাবার সুবিধা। চলো এমন একটা experiment করি যা দেখায় channel আর ownership কীভাবে একসাথে কাজ করে সমস্যা প্রতিরোধ করে: আমরা channel-এ value টা পাঠানোর _পরে_ spawned thread-এ `val` value ব্যবহার করার চেষ্টা করব। Listing 16-9-এর code compile করে দেখো কেন এই code allowed নয়।

<Listing number="16-9" file-name="src/main.rs" caption="Attempting to use `val` after we’ve sent it down the channel">

```rust,ignore,does_not_compile
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let val = String::from("hi");
        tx.send(val).unwrap();
        println!("val is {val}");
    });

    let received = rx.recv().unwrap();
    println!("Got: {received}");
}
```

</Listing>

এখানে আমরা `tx.send` দিয়ে channel-এ value পাঠানোর পরে `val` print করার চেষ্টা করছি। এটাকে allow করা খারাপ ধারণা: একবার value টা অন্য thread-এ পাঠানো হলে, সেই thread আমরা আবার value টা ব্যবহার করার আগে সেটা modify বা drop করে দিতে পারে। অন্য thread-এর পরিবর্তনের ফলে inconsistent বা অস্তিত্বহীন data-র কারণে error বা অপ্রত্যাশিত result আসতে পারে। কিন্তু Rust যদি আমরা Listing 16-9-এর code compile করার চেষ্টা করি, একটা error দেয়:

```console
$ cargo run
   Compiling message-passing v0.1.0 (file:///projects/message-passing)
error[E0382]: borrow of moved value: `val`
  --> src/main.rs:10:27
   |
 8 |         let val = String::from("hi");
   |             --- move occurs because `val` has type `String`, which does not implement the `Copy` trait
 9 |         tx.send(val).unwrap();
   |                 --- value moved here
10 |         println!("val is {val}");
   |                           ^^^ value borrowed here after move

For more information about this error, try `rustc --explain E0382`.
error: could not compile `message-passing` (bin "message-passing") due to 1 previous error
```

আমাদের concurrency ভুলের কারণে একটা compile-time error হয়েছে। `send` function তার parameter-এর ownership নিয়ে নেয়, আর যখন value টা move হয় তখন receiver তার ownership পায়। এটা আমাদের accidentally value পাঠানোর পরে সেটা আবার ব্যবহার করা থেকে বিরত রাখে; ownership system check করে যে সব কিছু ঠিক আছে।

<!-- Old headings. Do not remove or links may break. -->

<a id="sending-multiple-values-and-seeing-the-receiver-waiting"></a>

### একাধিক Value পাঠানো

Listing 16-8-এর code compile হয়েছে আর run হয়েছে, কিন্তু সেটা স্পষ্টভাবে দেখায়নি যে দুটো আলাদা thread channel-এর মাধ্যমে একে অপরের সাথে কথা বলছে।

Listing 16-10-তে আমরা কিছু পরিবর্তন করেছি যা প্রমাণ করবে যে Listing 16-8-এর code concurrently চলছে: spawned thread এখন একাধিক message পাঠাবে আর প্রতিটি message-এর মধ্যে এক সেকেন্ড করে pause করবে।

<Listing number="16-10" file-name="src/main.rs" caption="Sending multiple messages and pausing between each one">

```rust,noplayground
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let vals = vec![
            String::from("hi"),
            String::from("from"),
            String::from("the"),
            String::from("thread"),
        ];

        for val in vals {
            tx.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });

    for received in rx {
        println!("Got: {received}");
    }
}
```

</Listing>

এবার spawned thread-এর কাছে string-এর একটা vector আছে যা সে main thread-কে পাঠাবে। আমরা সেগুলোর উপর iterate করি, প্রতিটি আলাদাভাবে পাঠাই, আর `thread::sleep` function কে এক সেকেন্ডের `Duration` value দিয়ে call করে প্রতিটির মধ্যে pause করি।

main thread-এ আমরা আর `recv` function কে explicitly call করছি না: বদলে আমরা `rx`-কে একটা iterator হিসেবে treat করছি। প্রতিটি received value-এর জন্য আমরা সেটা print করছি। channel close হয়ে গেলে iteration শেষ হবে।

Listing 16-10-এর code run করার সময়, তুমি নিচের output দেখবে যেখানে প্রতিটি line-এর মধ্যে এক সেকেন্ডের pause থাকবে:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
Got: from
Got: the
Got: thread
```

যেহেতু main thread-এর `for` loop-এ কোনো pause বা delay করার code নেই, তাই আমরা বুঝতে পারি যে main thread spawned thread থেকে value receive করার জন্য অপেক্ষা করছে।

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-multiple-producers-by-cloning-the-transmitter"></a>

### একাধিক Producer তৈরি করা

আগে আমরা উল্লেখ করেছিলাম যে `mpsc` হলো _multiple producer, single consumer_-এর abbreviation। চলো `mpsc`-কে কাজে লাগাই আর Listing 16-10-এর code expand করে এমন একাধিক thread তৈরি করি যা সবাই একই receiver-কে value পাঠাবে। আমরা transmitter clone করে এটা করতে পারি, যেমন Listing 16-11-তে দেখানো হয়েছে।

<Listing number="16-11" file-name="src/main.rs" caption="Sending multiple messages from multiple producers">

```rust,noplayground
    // --snip--

    let (tx, rx) = mpsc::channel();

    let tx1 = tx.clone();
    thread::spawn(move || {
        let vals = vec![
            String::from("hi"),
            String::from("from"),
            String::from("the"),
            String::from("thread"),
        ];

        for val in vals {
            tx1.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });

    thread::spawn(move || {
        let vals = vec![
            String::from("more"),
            String::from("messages"),
            String::from("for"),
            String::from("you"),
        ];

        for val in vals {
            tx.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });

    for received in rx {
        println!("Got: {received}");
    }

    // --snip--
```

</Listing>

এবার প্রথম spawned thread তৈরি করার আগে আমরা transmitter-এর উপর `clone` call করি। এতে আমরা একটা নতুন transmitter পাব যা আমরা প্রথম spawned thread-কে দিতে পারি। আমরা original transmitter-টা দ্বিতীয় spawned thread-কে দিই। এতে আমরা দুটো thread পাই, প্রত্যেকেই এক receiver-কে ভিন্ন ভিন্ন message পাঠাচ্ছে।

যখন তুমি code টা run করবে, তোমার output এমন কিছু দেখাবে:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
Got: more
Got: from
Got: messages
Got: for
Got: the
Got: thread
Got: you
```

তোমার system-এর উপর ভিত্তি করে তুমি value গুলো অন্য কোনো ক্রমেও দেখতে পারো। এটাই concurrency-কে মজাদর আর একই সাথে কঠিন করে তোলে। তুমি যদি `thread::sleep` নিয়ে experiment করো, ভিন্ন ভিন্ন thread-এ একে ভিন্ন ভিন্ন value দিলে, প্রতিটি run আরও nondeterministic হবে আর প্রতিবার ভিন্ন output তৈরি করবে।

এখন যেহেতু আমরা দেখলাম channel কীভাবে কাজ করে, চলো দেখি concurrency-এর অন্য একটি পদ্ধতি।

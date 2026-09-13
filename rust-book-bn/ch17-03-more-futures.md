
<!-- Old headings. Do not remove or links may break. -->

<a id="yielding"></a>

### Runtime-কে Control Yield করা

[“আমাদের প্রথম Async প্রোগ্রাম”][async-program]<!-- ignore --> section-এর কথা মনে করো: প্রতিটি await point-এ Rust runtime-কে একটি task pause করে অন্যটিতে switch করার সুযোগ দেয়, যদি await করা future-টি ready না থাকে। এর উল্টোটাও সত্য: Rust async block-কে _শুধু_ await point-এই pause করে এবং runtime-কে control ফিরিয়ে দেয়। Await point-গুলোর মধ্যবর্তী সব কিছুই synchronous।

এর মানে হলো, তুমি যদি কোনো async block-এ await point ছাড়াই অনেক কাজ করো, সেই future অন্য কোনো future-কে অগ্রগতি করতে block করবে। তুমি হয়তো শুনে থাকবে একে এক future দ্বারা অন্য future-কে _starving_ করা বলা হয়। কিছু ক্ষেত্রে এটা বড় কোনো সমস্যা নাও হতে পারে। তবে তুমি যদি কোনো ধরনের দামি setup বা দীর্ঘস্থায়ী কাজ করো, অথবা তোমার এমন একটি future থাকে যা অনির্দিষ্টকালের জন্য কোনো নির্দিষ্ট কাজ করতেই থাকবে, তাহলে তোমাকে ভাবতে হবে কখন ও কোথায় runtime-কে control ফিরিয়ে দেবে।

চলো starvation সমস্যাটি দেখানোর জন্য একটি দীর্ঘস্থায়ী operation simulate করি, তারপর সেটা কীভাবে সমাধান করা যায় তা দেখি। Listing 17-14 একটি `slow` function চালু করে।

<Listing number="17-14" caption="Using `thread::sleep` to simulate slow operations" file-name="src/main.rs">

```rust
fn slow(name: &str, ms: u64) {
    thread::sleep(Duration::from_millis(ms));
    println!("'{name}' ran for {ms}ms");
}
```

</Listing>

এই কোড `trpl::sleep`-এর বদলে `std::thread::sleep` ব্যবহার করে, যাতে `slow` call করলে current thread কিছু milliseconds-এর জন্য block হয়। আমরা `slow`-কে এমন বাস্তব কাজের প্রতিনিধি হিসেবে ব্যবহার করতে পারি যেগুলো দীর্ঘস্থায়ী এবং blocking।

Listing 17-15-তে আমরা `slow` ব্যবহার করে এক জোড়া future-এ এ ধরনের CPU-bound কাজ emulate করি।

<Listing number="17-15" caption="Calling the `slow` function to simulate slow operations" file-name="src/main.rs">

```rust
extern crate trpl; // required for mdbook test

use std::{thread, time::Duration};

fn main() {
    trpl::block_on(async {
        // ANCHOR: slow-futures
        let a = async {
            println!("'a' started.");
            slow("a", 30);
            slow("a", 10);
            slow("a", 20);
            trpl::sleep(Duration::from_millis(50)).await;
            println!("'a' finished.");
        };

        let b = async {
            println!("'b' started.");
            slow("b", 75);
            slow("b", 10);
            slow("b", 15);
            slow("b", 350);
            trpl::sleep(Duration::from_millis(50)).await;
            println!("'b' finished.");
        };

        trpl::select(a, b).await;
        // ANCHOR_END: slow-futures
    });
}

fn slow(name: &str, ms: u64) {
    thread::sleep(Duration::from_millis(ms));
    println!("'{name}' ran for {ms}ms");
}
```

</Listing>

প্রতিটি future একগাদা slow operation সম্পন্ন করার _পরেই_ runtime-কে control ফিরিয়ে দেয়। তুমি এই কোডটি চালালে এই output পাবে:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-15/
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'a' ran for 10ms
'a' ran for 20ms
'b' started.
'b' ran for 75ms
'b' ran for 10ms
'b' ran for 15ms
'b' ran for 350ms
'a' finished.
```

Listing 17-5-তে যেখানে আমরা দুটি URL fetch করা future-কে race করতে `trpl::select` ব্যবহার করেছিলাম, সেই একইভাবে এখানেও `select` `a` শেষ হলেই শেষ হয়ে যায়। তবে দুটি future-এর `slow` call-গুলোর মধ্যে কোনো interleaving নেই। `a` future তার সব কাজ `trpl::sleep` call await না হওয়া পর্যন্ত করে, তারপর `b` future তার সব কাজ নিজের `trpl::sleep` call await না হওয়া পর্যন্ত করে, এবং শেষে `a` future সম্পূর্ণ হয়। দুটি future-কে তাদের slow কাজের মাঝে অগ্রগতি করতে দিতে হলে, আমাদের await point দরকার যাতে আমরা runtime-কে control ফিরিয়ে দিতে পারি। তার মানে আমাদের এমন কিছু দরকার যাকে আমরা await করতে পারি!

Listing 17-15-তেই আমরা এ ধরনের handoff ঘটতে দেখতে পাই: যদি আমরা `a` future-এর শেষে `trpl::sleep` সরিয়ে দিতাম, তবে `b` future একেবারেই না চলেই `a` সম্পূর্ণ হয়ে যেত। চলো `trpl::sleep` function কে একটি শুরুর point হিসেবে ব্যবহার করে দেখি, যাতে operation-গুলো পালা করে অগ্রগতি করতে পারে, যেমন Listing 17-16-তে দেখানো হয়েছে।

<Listing number="17-16" caption="Using `trpl::sleep` to let operations switch off making progress" file-name="src/main.rs">

```rust
        let one_ms = Duration::from_millis(1);

        let a = async {
            println!("'a' started.");
            slow("a", 30);
            trpl::sleep(one_ms).await;
            slow("a", 10);
            trpl::sleep(one_ms).await;
            slow("a", 20);
            trpl::sleep(one_ms).await;
            println!("'a' finished.");
        };

        let b = async {
            println!("'b' started.");
            slow("b", 75);
            trpl::sleep(one_ms).await;
            slow("b", 10);
            trpl::sleep(one_ms).await;
            slow("b", 15);
            trpl::sleep(one_ms).await;
            slow("b", 350);
            trpl::sleep(one_ms).await;
            println!("'b' finished.");
        };
```

</Listing>

আমরা প্রতিটি `slow` call-এর মাঝে `trpl::sleep` call ও await point যোগ করেছি। এখন দুটি future-এর কাজ interleave হয়:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-16
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'b' started.
'b' ran for 75ms
'a' ran for 10ms
'b' ran for 10ms
'a' ran for 20ms
'b' ran for 15ms
'a' finished.
```

`a` future এখনও একটু কাজ করে তারপর `b`-কে control দেয়, কারণ সে কখনো `trpl::sleep` call করার আগেই `slow` call করে, কিন্তু এরপর future-গুলো প্রতিবার একজন await point-এ পৌঁছালে আবার পালা কাটে। এই ক্ষেত্রে, আমরা প্রতিটি `slow` call-এর পরে এটি করেছি, কিন্তু আমরা কাজকে যেভাবে আমাদের কাছে সবচেয়ে বেশি মানানসই মনে হয় সেভাবে ভাগ করতে পারতাম।

তবে আমরা এখানে আসলে _sleep_ করতে চাই না: আমরা যত দ্রুত পারি অগ্রগতি করতে চাই। আমাদের শুধু runtime-কে control ফিরিয়ে দেওয়া দরকার। আমরা সেটা সরাসরি `trpl::yield_now` function ব্যবহার করে করতে পারি। Listing 17-17-তে আমরা সেই সব `trpl::sleep` call-কে `trpl::yield_now` দিয়ে প্রতিস্থাপন করি।

<Listing number="17-17" caption="Using `yield_now` to let operations switch off making progress" file-name="src/main.rs">

```rust
        let a = async {
            println!("'a' started.");
            slow("a", 30);
            trpl::yield_now().await;
            slow("a", 10);
            trpl::yield_now().await;
            slow("a", 20);
            trpl::yield_now().await;
            println!("'a' finished.");
        };

        let b = async {
            println!("'b' started.");
            slow("b", 75);
            trpl::yield_now().await;
            slow("b", 10);
            trpl::yield_now().await;
            slow("b", 15);
            trpl::yield_now().await;
            slow("b", 350);
            trpl::yield_now().await;
            println!("'b' finished.");
        };
```

</Listing>

এই কোড আসল উদ্দেশ্য সম্পর্কে বেশি পরিষ্কার, এবং `sleep` ব্যবহারের চেয়ে উল্লেখযোগ্যভাবে দ্রুত হতে পারে, কারণ `sleep`-এর মতো timer-গুলোর সূক্ষ্মতার সীমা থাকে। আমরা যে `sleep` version ব্যবহার করছি, সে উদাহরণস্বরূপ এক ন্যানোসেকেন্ডের `Duration` দিলেও অন্তত এক মিলিসেকেন্ড sleep করবে। আবার বলছি, আধুনিক কম্পিউটার বেশ _দ্রুত_: এক মিলিসেকেন্ডে তারা অনেক কিছু করতে পারে!

এর মানে হলো async compute-bound কাজের জন্যও কার্যকর হতে পারে, তোমার প্রোগ্রাম আর কী করছে তার ওপর নির্ভর করে, কারণ এটি প্রোগ্রামের বিভিন্ন অংশের মধ্যে সম্পর্ক গঠনের একটি কার্যকর tool দেয় (কিন্তু async state machine-এর overhead-এর একটি মূল্যে)। এটি _cooperative multitasking_-এর একটি রূপ, যেখানে প্রতিটি future-এর কাছে await point-এর মাধ্যমে কখন control দেবে তা ঠিক করার ক্ষমতা থাকে। ফলে প্রতিটি future-এর কাছে অনেকক্ষণ block না করার দায়িত্বও থাকে। কিছু Rust-ভিত্তিক embedded operating system-এ, এটাই হলো _একমাত্র_ ধরনের multitasking!

বাস্তব কোডে, তুমি সাধারণত প্রতিটি লাইনে function call-গুলোর সাথে await point alternate করবে না। যদিও এভাবে control yield করা তুলনামূলক কম খরচের, তবে সেটি একদম ফ্রি নয়। অনেক ক্ষেত্রে, একটি compute-bound task-কে ভাগ করতে গেলে সেটি উল্লেখযোগ্যভাবে ধীর হয়ে যেতে পারে, তাই মাঝে মাঝে একটি operation-কে সাময়িকভাবে block করতে দেওয়া _সামগ্রিক_ performance-এর জন্য ভালো। তোমার কোডের আসল performance bottleneck কী, তা দেখতে সবসময় measure করো। তবে মৌলিক গতিশীলতা মাথায় রাখা জরুরি, যদি তুমি দেখো অনেক কাজ serial-ভাবে ঘটছে যা তুমি concurrent হবে বলে আশা করেছিলে!

### নিজেদের Async Abstraction তৈরি করা

আমরা future-গুলোকে একসাথে যুক্ত করে নতুন pattern-ও তৈরি করতে পারি। যেমন, আমরা ইতিমধ্যে থাকা async building block দিয়ে একটি `timeout` function বানাতে পারি। কাজ শেষ হলে সেটি আরেকটি building block হবে যা দিয়ে আরও অনেক async abstraction তৈরি করা যাবে।

Listing 17-18 দেখায় একটি slow future-এর সাথে এই `timeout` কীভাবে কাজ করবে বলে আমরা আশা করি।

<Listing number="17-18" caption="Using our imagined `timeout` to run a slow operation with a time limit" file-name="src/main.rs">

```rust,ignore,does_not_compile
        let slow = async {
            trpl::sleep(Duration::from_secs(5)).await;
            "Finally finished"
        };

        match timeout(slow, Duration::from_secs(2)).await {
            Ok(message) => println!("Succeeded with '{message}'"),
            Err(duration) => {
                println!("Failed after {} seconds", duration.as_secs())
            }
        }
```

</Listing>

চলো এটি ইমপ্লিমেন্ট করি! শুরুতে, চলো `timeout`-এর API নিয়ে ভাবি:

- এটি নিজে একটি async function হতে হবে যাতে আমরা এটিকে await করতে পারি।
- এর প্রথম parameter একটি future হবে যেটি চালানো হবে। এটিকে আমরা generic বানাতে পারি যাতে যেকোনো future-এর সাথে কাজ করে।
- এর দ্বিতীয় parameter হবে সর্বোচ্চ অপেক্ষার সময়। আমরা `Duration` ব্যবহার করলে সেটি `trpl::sleep`-কে দেওয়া সহজ হয়।
- এটি একটি `Result` return করবে। Future সফলভাবে সম্পূর্ণ হলে `Result` হবে future থেকে উৎপন্ন value সহ `Ok`। Timeout আগে শেষ হলে `Result` হবে timeout যতক্ষণ অপেক্ষা করেছিল সেই duration সহ `Err`।

Listing 17-19 এই declaration-টি দেখায়।

<!-- This is not tested because it intentionally does not compile. -->

<Listing number="17-19" caption="Defining the signature of `timeout`" file-name="src/main.rs">

```rust,ignore,does_not_compile
async fn timeout<F: Future>(
    future_to_try: F,
    max_time: Duration,
) -> Result<F::Output, Duration> {
    // Here is where our implementation will go!
}
```

</Listing>

এটি আমাদের type-সংক্রান্ত লক্ষ্য পূরণ করে। এখন চলো ভাবি আমাদের কী _আচরণ_ দরকার: আমরা দেওয়া future-টিকে duration-এর বিরুদ্ধে race করাতে চাই। আমরা `trpl::sleep` ব্যবহার করে duration থেকে একটি timer future বানাতে পারি, এবং `trpl::select` ব্যবহার করে caller-দের দেওয়া future-টির সাথে সেই timer-টি চালাতে পারি।

Listing 17-20-তে আমরা `trpl::select` await করার ফলের ওপর match করে `timeout` ইমপ্লিমেন্ট করি।

<Listing number="17-20" caption="Defining `timeout` with `select` and `sleep`" file-name="src/main.rs">

```rust
use trpl::Either;

// --snip--

async fn timeout<F: Future>(
    future_to_try: F,
    max_time: Duration,
) -> Result<F::Output, Duration> {
    match trpl::select(future_to_try, trpl::sleep(max_time)).await {
        Either::Left(output) => Ok(output),
        Either::Right(_) => Err(max_time),
    }
}
```

</Listing>

`trpl::select`-এর ইমপ্লিমেন্টেশন fair নয়: এটি argument-গুলোকে যে ক্রমে দেওয়া হয় সেই ক্রমে poll করে (অন্যান্য `select` ইমপ্লিমেন্টেশন এলোমেলোভাবে কোন argument আগে poll করবে তা বেছে নেয়)। তাই আমরা `future_to_try`-কে প্রথমে `select`-কে দিই, যাতে `max_time` খুব ছোট duration হলেও সেটি সম্পূর্ণ হওয়ার সুযোগ পায়। `future_to_try` আগে শেষ হলে `select` `future_to_try`-এর output সহ `Left` return করবে। আর `timer` আগে শেষ হলে `select` timer-এর `()` output সহ `Right` return করবে।

যদি `future_to_try` সফল হয় এবং আমরা `Left(output)` পাই, আমরা `Ok(output)` return করি। অন্যথায় sleep timer শেষ হয়ে গেলে এবং আমরা `Right(())` পেলে, আমরা `()`-কে `_` দিয়ে ignore করি এবং বদলে `Err(max_time)` return করি।

এরকেই দিয়ে আমাদের একটি কাজ করা `timeout` তৈরি, যা আরও দুটি async helper থেকে তৈরি। কোড চালালে এটি timeout-এর পর failure mode print করবে:

```text
Failed after 2 seconds
```

যেহেতু future-গুলো অন্য future-এর সাথে যুক্ত হয়, তুমি ছোট async building block ব্যবহার করে বেশ শক্তিশালী tool তৈরি করতে পারো। যেমন, তুমি একই পদ্ধতি ব্যবহার করে timeout-কে retry-এর সাথে যুক্ত করতে পারো, এবং সেগুলোকে নেটওয়ার্ক call-এর মতো operation-এর সাথে (যেমন Listing 17-5-এ যা আছে) ব্যবহার করতে পারো।

বাস্তবে, তুমি সাধারণত সরাসরি `async` ও `await` নিয়ে কাজ করবে, এবং দ্বিতীয়তঃ `select`-এর মতো function ও `join!` macro-এর মতো macro নিয়ে, যাতে outermost future-গুলো কীভাবে execute হবে তা নিয়ন্ত্রণ করা যায়।

আমরা এখন একই সময়ে একাধিক future নিয়ে কাজ করার একাধিক উপায় দেখলাম। এর পরে, চলো দেখি কীভাবে _stream_ দিয়ে সময়ের সাথে সাথে একটি sequence-এ একাধিক future নিয়ে কাজ করা যায়।

[async-program]: ch17-01-futures-and-syntax.html#our-first-async-program

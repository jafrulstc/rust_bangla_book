<!-- Old headings. Do not remove or links may break. -->

<a id="turning-our-single-threaded-server-into-a-multithreaded-server"></a>
<a id="from-single-threaded-to-multithreaded-server"></a>

## Single-Threaded থেকে Multithreaded Server-এ

এই মুহূর্তে server প্রতিটি request পর্যায়ক্রমে process করবে, যার মানে প্রথম connection process হওয়া শেষ না হওয়া পর্যন্ত দ্বিতীয় connection কে process করবে না। যদি server আরও বেশি request পেতে থাকে, এই ধারাবাহিক (serial) সম্পাদন ক্রমশ কম কার্যকরী হয়ে পড়বে। যদি এমন কোনো request আসে যেটি process করতে অনেক সময় লাগে, পরবর্তী request গুলোকে অপেক্ষা করতে হবে যতক্ষণ না সেই দীর্ঘ request শেষ হচ্ছে, এমনকি নতুন request গুলো দ্রুত process হতে পারলেও। আমাদের এটি ঠিক করতে হবে, কিন্তু প্রথমে আমরা সমস্যাটি কাজ করতে দেখি।

<!-- Old headings. Do not remove or links may break. -->

<a id="simulating-a-slow-request-in-the-current-server-implementation"></a>

### একটি Slow Request Simulate করা

আমরা দেখবো কীভাবে ধীরে process হওয়া একটি request আমাদের বর্তমান server implementation-কে করা অন্যান্য request গুলোকে প্রভাবিত করতে পারে। Listing 21-10 _/sleep_-এ একটি request সামলানোর কোড implement করে একটি simulated slow response সহ, যা সাড়া দেওয়ার আগে server-কে পাঁচ সেকেন্ড sleep করাবে।

<Listing number="21-10" file-name="src/main.rs" caption="Simulating a slow request by sleeping for five seconds">

```rust,no_run
use std::{
    fs,
    io::{BufReader, prelude::*},
    net::{TcpListener, TcpStream},
    thread,
    time::Duration,
};
// --snip--

fn handle_connection(mut stream: TcpStream) {
    // --snip--

    let (status_line, filename) = match &request_line[..] {
        "GET / HTTP/1.1" => ("HTTP/1.1 200 OK", "hello.html"),
        "GET /sleep HTTP/1.1" => {
            thread::sleep(Duration::from_secs(5));
            ("HTTP/1.1 200 OK", "hello.html")
        }
        _ => ("HTTP/1.1 404 NOT FOUND", "404.html"),
    };

    // --snip--
}
```

</Listing>

যেহেতু এখন তিনটি case আছে তাই আমরা `if` থেকে `match`-এ চলে গেছি। string literal মান গুলোর সাথে pattern-match করতে আমাদের `request_line`-এর একটি slice-এ স্পষ্টভাবে match করতে হয়; `match` equality method-এর মতো স্বয়ংক্রিয়ভাবে referencing আর dereferencing করে না।

প্রথম arm টি Listing 21-9-এর `if` block-টির মতোই। দ্বিতীয় arm টি _/sleep_-এ একটি request-এ match করে। যখন সেই request গ্রহণ করা হবে, server সফল HTML পেজ render করার আগে পাঁচ সেকেন্ড sleep করবে। তৃতীয় arm টি Listing 21-9-এর `else` block-টির মতোই।

দেখতেই পাচ্ছ আমাদের server কতটা primitive: আসল library গুলো একাধিক request চেনার কাজটা অনেক কম verbose উপায়ে করতো!

`cargo run` দিয়ে server শুরু করো। তারপর দুটি browser window খোলো: একটিতে _http://127.0.0.1:7878_ আর অন্যটিতে _http://127.0.0.1:7878/sleep_। আগের মতো তুমি যদি _/_ URI কয়েকবার চাও, দেখবে এটি দ্রুত সাড়া দেয়। কিন্তু যদি _/sleep_ চাও এবং তারপর _/_ লোড করো, দেখবে _/_ ততক্ষণ অপেক্ষা করছে যতক্ষণ না `sleep` তার সম্পূর্ণ পাঁচ সেকেন্ড sleep করছে।

একটি slow request-এর পেছনে জমে থাকা request গুলোকে এড়াতে আমরা নানা প্রযুক্তি ব্যবহার করতে পারি, যার মধ্যে Chapter 17-এ যেমন async ব্যবহার করেছিলাম সেটাও আছে; আমরা যেটি implement করবো সেটি হলো একটি thread pool।

### একটি Thread Pool দিয়ে Throughput উন্নত করা

একটি _thread pool_ হলো spawned thread-দের একটি দল যারা কোনো task সামলানোর জন্য প্রস্তুত এবং অপেক্ষা করছে। যখন program একটি নতুন task পায়, সে পুল থেকে একটি thread-কে সেই task-এ assign করে, এবং সেই thread সেই task process করে। পুলের বাকি thread গুলো প্রথম thread কাজ করার সময় আসা অন্য কোনো task সামলাতে প্রস্তুত থাকে। যখন প্রথম thread তার task process করা শেষ করে, সে idle thread-দের পুলে ফিরে যায়, একটি নতুন task সামলানোর জন্য প্রস্তুত। একটি thread pool তোমাকে connection গুলো concurrently process করতে দেয়, যার ফলে তোমার server-এর throughput বাড়ে।

আমরা pool-এ thread-দের সংখ্যা একটি ছোট সংখ্যায় সীমিত রাখবো, যাতে DoS attack থেকে আত্মরক্ষা করা যায়; যদি আমাদের program প্রতিটি request আসার সময় একটি করে নতুন thread তৈরি করতো, তবে কেউ আমাদের server-এ ১০ মিলিয়ন request করে আমাদের সব resource শেষ করে দিয়ে আক্রমণ চালাতে পারতো এবং request process করা পুরোপুরি থমকে দিতে পারতো।

সুতরাং, আমরা সীমাহীন thread spawn করার বদলে pool-এ অপেক্ষা করা একটি নির্দিষ্ট সংখ্যক thread রাখবো। আসা request গুলো process করার জন্য pool-কে পাঠানো হবে। Pool আসা request-গুলোর একটি queue ধরে রাখবে। Pool-এর প্রতিটি thread এই queue থেকে একটি request pop করবে, সেটি handle করবে, এবং তারপর queue-এ আরেকটি request চাইবে। এই design-এ আমরা একসাথে সর্বোচ্চ _`N`_টি request concurrently process করতে পারবো, যেখানে _`N`_ হলো thread-দের সংখ্যা। যদি প্রতিটি thread কোনো দীর্ঘ-চলমান request-এ সাড়া দিচ্ছে, তবুও পরবর্তী request গুলো queue-তে জমতে পারে, কিন্তু সেই পর্যায়ে পৌঁছানোর আগে আমরা যত বেশি সংখ্যক দীর্ঘ-চলমান request সামলাতে পারি তার সংখ্যা বেড়ে গেছে।

এই প্রযুক্তিটি একটি web server-এর throughput বাড়ানোর অনেক উপায়ের মধ্যে একটি মাত্র। অন্যান্য যেসব option তুমি অন্বেষণ করতে পারো সেগুলো হলো fork/join model, single-threaded async I/O model, এবং multithreaded async I/O model। এই topic-এ তোমার আগ্রহ থাকলে অন্যান্য solution সম্পর্কে আরও পড়তে পারো এবং সেগুলো implement করার চেষ্টা করতে পারো; Rust-এর মতো low-level ভাষায় এই সব option-ই সম্ভব।

thread pool implement করা শুরু করার আগে চলো বলি পুল ব্যবহার করা দেখতে কেমন হবে। Code design করার সময়, client interface আগে লিখে ফেলা design-কে পরিচালিত করতে পারে। Code-এর API এমনভাবে structure করে লেখো যেভাবে তুমি তাকে call করতে চাও; তারপর, functionality implement করার পর আবার public API design করার বদলে সেই structure-এর ভেতরে functionality implement করো।

Chapter 12-তে project-এ আমরা যেমন test-driven development ব্যবহার করেছিলাম, এখানে আমরা compiler-driven development ব্যবহার করবো। আমরা এমন code লিখবো যা আমরা যে function গুলো চাই তাদের call করে, তারপর compiler থেকে error গুলো দেখে বুঝবো পরে কী পরিবর্তন করলে code টি কাজ করবে। তবে সেটা করার আগে, আমরা এমন একটি প্রযুক্তি নিয়ে আলোচনা করবো যা আমরা শুরুর পথ হিসেবে ব্যবহার করবো না।

<!-- Old headings. Do not remove or links may break. -->

<a id="code-structure-if-we-could-spawn-a-thread-for-each-request"></a>

#### প্রতিটি Request-এর জন্য একটি Thread Spawn করা

প্রথমে, চলো দেখি যদি আমাদের code প্রতিটি connection-এর জন্য সত্যিই নতুন thread তৈরি করতো, তাহলে কেমন দেখাতো। আগেই বলেছি, সম্ভাব্য সীমাহীন সংখ্যক thread spawn করার সমস্যার কারণে এটি আমাদের চূড়ান্ত পরিকল্পনা নয়, কিন্তু একটি কার্যকর multithreaded server প্রথমে পাওয়ার জন্য এটি একটি শুরুর পথ। তারপর, আমরা উন্নতি হিসেবে thread pool যোগ করবো, এবং দুটি solution-এর তুলনা করা সহজ হবে।

Listing 21-11 `for` loop-এর ভেতরে প্রতিটি stream সামলাতে একটি নতুন thread spawn করতে `main`-এ কী পরিবর্তন করতে হবে তা দেখায়।

<Listing number="21-11" file-name="src/main.rs" caption="Spawning a new thread for each stream">

```rust,no_run
fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        thread::spawn(|| {
            handle_connection(stream);
        });
    }
}
```

</Listing>

Chapter 16-তে যেমন শিখেছো, `thread::spawn` একটি নতুন thread তৈরি করে এবং তারপর closure-এর code সেই নতুন thread-এ চালায়। তুমি যদি এই code টি চালাও এবং browser-এ _/sleep_ লোড করো, তারপর আরও দুটি browser tab-এ _/_ লোড করো, দেখবে যে আসলেই _/_-এর request গুলোকে _/sleep_ শেষ হওয়ার জন্য অপেক্ষা করতে হচ্ছে না। তবে, যেমনটা বলেছি, এটি শেষ পর্যন্ত system-কে অভিভূত করবে কারণ তুমি কোনো সীমা ছাড়াই নতুন thread তৈরি করবে।

Chapter 17 থেকে তোমার মনে পড়তে পারে যে এটিই ঠিক সেই ধরনের পরিস্থিতি যেখানে async আর await সত্যিই দারুণ কাজ দেয়! thread pool বানানোর সময় এটি মনে রাখো এবং ভাবো async দিয়ে কী কী ভিন্ন বা একই হতো।

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-a-similar-interface-for-a-finite-number-of-threads"></a>

#### একটি নির্দিষ্ট সংখ্যক Thread তৈরি করা

আমরা চাই আমাদের thread pool অনুরূপ, পরিচিত উপায়ে কাজ করুক, যাতে thread থেকে thread pool-এ স্থানান্তরে আমাদের API ব্যবহার করা code-এ বড় পরিবর্তন না লাগে। Listing 21-12 `thread::spawn`-এর বদলে ব্যবহার করতে চাই এমন একটি `ThreadPool` struct-এর কাল্পনিক interface দেখায়।

<Listing number="21-12" file-name="src/main.rs" caption="Our ideal `ThreadPool` interface">

```rust,ignore,does_not_compile
fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    let pool = ThreadPool::new(4);

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        pool.execute(|| {
            handle_connection(stream);
        });
    }
}
```

</Listing>

আমরা `ThreadPool::new` ব্যবহার করে configurable সংখ্যক thread সহ একটি নতুন thread pool তৈরি করি, এই ক্ষেত্রে চারটি। তারপর, `for` loop-এ, `pool.execute`-এর interface `thread::spawn`-এর মতোই, এটি একটি closure নেয় যেটি pool প্রতিটি stream-এর জন্য চালাবে। আমাদের `pool.execute` implement করতে হবে যাতে এটি closure টি নেয় এবং pool-এর একটি thread-কে সেটি চালানোর জন্য দেয়। এই code টি এখনও compile হবে না, কিন্তু আমরা চেষ্টা করবো যাতে compiler আমাদের কীভাবে ঠিক করতে হবে সেটা বোঝাতে পারে।

<!-- Old headings. Do not remove or links may break. -->

<a id="building-the-threadpool-struct-using-compiler-driven-development"></a>

#### Compiler-Driven Development ব্যবহার করে `ThreadPool` তৈরি করা

_src/main.rs_-এ Listing 21-12-এর পরিবর্তন গুলো করো, এবং তারপর আমরা `cargo check` থেকে পাওয়া compiler error গুলো ব্যবহার করে আমাদের development পরিচালিত করবো। নিচে আমরা প্রথম যে error টি পাই তা দেখানো হলো:

```console
$ cargo check
    Checking hello v0.1.0 (file:///projects/hello)
error[E0433]: cannot find type `ThreadPool` in this scope
  --> src/main.rs:11:16
   |
11 |     let pool = ThreadPool::new(4);
   |                ^^^^^^^^^^ use of undeclared type `ThreadPool`

For more information about this error, try `rustc --explain E0433`.
error: could not compile `hello` (bin "hello") due to 1 previous error
```

দারুণ! এই error টি আমাদের বলছে আমাদের একটি `ThreadPool` type বা module দরকার, তাই চলো আমরা এখন একটি বানাই। আমাদের `ThreadPool` implementation টি আমাদের web server যে কাজ করছে তার ধরন থেকে স্বাধীন হবে। সুতরাং, আমরা `hello` crate-টিকে একটি binary crate থেকে library crate-এ পরিবর্তন করি আমাদের `ThreadPool` implementation ধারণ করার জন্য। Library crate-এ পরিবর্তন করার পর আমরা এই আলাদা thread pool library টি শুধু web request serve করার জন্য নয়, যেকোনো কাজের জন্য ব্যবহার করতে পারবো।

একটি _src/lib.rs_ file তৈরি করো যেখানে নিচের মতো কিছু থাকবে, যা আপাতত একটি `ThreadPool` struct-এর সবচেয়ে সরল definition:

<Listing file-name="src/lib.rs">

```rust,noplayground
pub struct ThreadPool;
```

</Listing>


তারপর, library crate থেকে `ThreadPool` কে scope-এ আনতে _src/main.rs_ file টি edit করো, _src/main.rs_-এর শীর্ষে নিচের code টি যোগ করে:

<Listing file-name="src/main.rs">

```rust,ignore
use hello::ThreadPool;
```

</Listing>

এই code টি এখনও কাজ করবে না, কিন্তু চলো আবার check করি যাতে আমরা পরের সেই error টি পাই যেটি আমাদের সামলাতে হবে:

```console
$ cargo check
    Checking hello v0.1.0 (file:///projects/hello)
error[E0599]: no associated function or constant named `new` found for struct `ThreadPool` in the current scope
  --> src/main.rs:12:28
   |
12 |     let pool = ThreadPool::new(4);
   |                            ^^^ associated function or constant not found in `ThreadPool`

For more information about this error, try `rustc --explain E0599`.
error: could not compile `hello` (bin "hello") due to 1 previous error
```

এই error টি নির্দেশ করে যে এরপর আমাদের `ThreadPool`-এর জন্য `new` নামের একটি associated function তৈরি করতে হবে। আমরা আরও জানি যে `new`-এর একটি parameter থাকতে হবে যা `4` কে argument হিসেবে গ্রহণ করতে পারে এবং একটি `ThreadPool` instance return করা উচিত। চলো এই বৈশিষ্ট্য গুলো সম্পন্ন এমন সবচেয়ে সরল `new` function implement করি:

<Listing file-name="src/lib.rs">

```rust,noplayground
pub struct ThreadPool;

impl ThreadPool {
    pub fn new(size: usize) -> ThreadPool {
        ThreadPool
    }
}
```

</Listing>

আমরা `size` parameter-এর type হিসেবে `usize` বেছে নিয়েছি কারণ আমরা জানি যে thread-দের ঋণাত্মক সংখ্যা কোনো অর্থ বহন করে না। আমরা আরও জানি এই `4` কে আমরা thread-দের একটি collection-এর element সংখ্যা হিসেবে ব্যবহার করবো, আর `usize` type টি ঠিক সেই কাজের জন্যই, যেমনটা Chapter 3-এর [“Integer Types”][integer-types]<!-- ignore --> section-এ আলোচনা করেছি।

চলো code টি আবার check করি:

```console
$ cargo check
    Checking hello v0.1.0 (file:///projects/hello)
error[E0599]: no method named `execute` found for struct `ThreadPool` in the current scope
  --> src/main.rs:17:14
   |
17 |         pool.execute(|| {
   |         -----^^^^^^^ method not found in `ThreadPool`

For more information about this error, try `rustc --explain E0599`.
error: could not compile `hello` (bin "hello") due to 1 previous error.
```

এখন error টি আসছে কারণ `ThreadPool`-এ আমাদের কোনো `execute` method নেই। [“Creating a Finite Number of Threads”](#creating-a-finite-number-of-threads)<!-- ignore --> section থেকে মনে করো আমরা স্থির করেছিলাম আমাদের thread pool-এর interface `thread::spawn`-এর মতোই হবে। এছাড়া, আমরা `execute` function টি এমনভাবে implement করবো যাতে এটি তাকে দেওয়া closure টি নেয় এবং pool-এর একটি idle thread-কে সেটি চালানোর জন্য দেয়।

আমরা `ThreadPool`-এ `execute` method define করবো যা একটি closure কে parameter হিসেবে নেয়। Chapter 13-এর [“Moving Captured Values Out of Closures”][moving-out-of-closures]<!-- ignore --> section থেকে মনে করো আমরা closure গুলোকে তিনটি ভিন্ন trait সহ parameter হিসেবে নিতে পারি: `Fn`, `FnMut`, এবং `FnOnce`। এখানে কোন ধরনের closure ব্যবহার করবো তা স্থির করতে হবে। আমরা জানি আমরা standard library-র `thread::spawn` implementation-এর মতো কিছু করবো, তাই আমরা `thread::spawn`-এর signature-এ তার parameter-এ কী bounds আছে তা দেখতে পারি। Documentation আমাদের নিচেরটা দেখায়:

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

`F` type parameter টি হলো যেটা নিয়ে এখানে আমাদের চিন্তা; `T` type parameter টি return value-এর সাথে সম্পর্কিত, সেটা নিয়ে আমরা চিন্তিত নই। আমরা দেখতে পাই `spawn`, `F`-এর trait bound হিসেবে `FnOnce` ব্যবহার করে। সম্ভবত এটাই আমরা চাই, কারণ আমরা শেষ পর্যন্ত `execute`-এ পাওয়া argument টি `spawn`-কে দেবো। আমরা আরও নিশ্চিত হতে পারি যে `FnOnce`-ই সেই trait যা আমরা ব্যবহার করতে চাই, কারণ একটি request চালানোর জন্য thread সেই request-এর closure টি শুধু একবারই execute করবে, যা `FnOnce`-এর `Once`-এর সাথে মেলে।

`F` type parameter-এর trait bound হিসেবে `Send` এবং lifetime bound `'static`-ও আছে, যা আমাদের পরিস্থিতিতে কাজে লাগে: closure টি একটি thread থেকে অন্যটিতে transfer করতে আমাদের `Send` দরকার, আর `'static` দরকার কারণ আমরা জানি না thread-টি execute হতে কত সময় নেবে। চলো `ThreadPool`-এ একটি `execute` method তৈরি করি যা `F` type-এর একটি generic parameter এই bound গুলো সহ নেবে:

<Listing file-name="src/lib.rs">

```rust,noplayground
impl ThreadPool {
    // --snip--
    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
    }
}
```

</Listing>

আমরা এখনও `FnOnce`-এর পরে `()` ব্যবহার করছি কারণ এই `FnOnce` এমন একটি closure কে নির্দেশ করে যেটি কোনো parameter নেয় না এবং unit type `()` return করে। Function definition-এর মতো, return type signature থেকে বাদ দেওয়া যেতে পারে, কিন্তু কোনো parameter না থাকলেও আমাদের parentheses রাখতে হবে।

আবারও বলছি, এটিই `execute` method-এর সবচেয়ে সরল implementation: এটি কিছুই করে না, কিন্তু আমরা শুধু চাই আমাদের code compile হোক। চলো এটি আবার check করি:

```console
$ cargo check
    Checking hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.24s
```

এটি compile হয়! কিন্তু মনে রেখো, তুমি যদি `cargo run` চালাও এবং browser-এ একটি request করো, তবে browser-এ তুমি chapter-এর শুরুতে যে error গুলো দেখেছিলে সেগুলো দেখতে পাবে। আমাদের library আসলে `execute`-কে দেওয়া closure টিকে এখনও call করছে না!

> Note: কঠোর compiler সম্পন্ন ভাষা যেমন Haskell আর Rust সম্পর্কে তুমি শুনতে পারো একটা কথা—“If the code compiles, it works.” কিন্তু এই কথাটি সবসময় সত্য নয়। আমাদের project compile হয়, কিন্তু এটি একেবারেই কিছু করে না! যদি আমরা একটি আসল, পূর্ণাঙ্গ project বানাতাম, এটাই হতো unit test লেখা শুরু করার উপযুক্ত সময়, যাতে code compile হয় _এবং_ আমরা যে আচরণ চাই সেটা আছে কিনা তা check করা যায়।

ভাবো: যদি আমরা closure-এর বদলে একটি future execute করতাম, তাহলে এখানে কী ভিন্ন হতো?

#### `new`-এ Thread-দের সংখ্যা যাচাই করা

আমরা `new` আর `execute`-এর parameter গুলো নিয়ে কিছুই করছি না। চলো এই function গুলোর body আমরা যা আচরণ চাই তা সহ implement করি। শুরুতে, চলো `new` নিয়ে ভাবি। আগে আমরা `size` parameter-এর জন্য unsigned type বেছেছিলাম কারণ ঋণাত্মক সংখ্যক thread সম্পন্ন একটি pool এর কোনো অর্থ নেই। তবে, শূন্য সংখ্যক thread সম্পন্ন একটি pool-এরও কোনো অর্থ নেই, অথচ শূন্য একটি সম্পূর্ণ বৈধ `usize`। আমরা code যোগ করবো যেটি একটি `ThreadPool` instance return করার আগে check করবে `size` শূন্যের চেয়ে বড় কি না, এবং শূন্য পেলে program কে panic করাবো `assert!` macro ব্যবহার করে, যেমন Listing 21-13-এ দেখানো হয়েছে।

<Listing number="21-13" file-name="src/lib.rs" caption="Implementing `ThreadPool::new` to panic if `size` is zero">

```rust,noplayground
impl ThreadPool {
    /// Create a new ThreadPool.
    ///
    /// The size is the number of threads in the pool.
    ///
    /// # Panics
    ///
    /// The `new` function will panic if the size is zero.
    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        ThreadPool
    }

    // --snip--
}
```

</Listing>

আমরা doc comment সহ আমাদের `ThreadPool`-এর জন্য কিছু documentation-ও যোগ করেছি। মনে রেখো, আমরা Chapter 14-এ যেমন আলোচনা করেছি, ভালো documentation practice অনুসরণ করে এমন একটি section যোগ করেছি যেখানে আমাদের function কখন panic করতে পারে তা call out করা হয়েছে। `cargo doc --open` চালিয়ে `ThreadPool` struct-এ click করে দেখো `new`-এর জন্য generated docs গুলো কেমন দেখায়!

এখানে যেমন `assert!` macro যোগ করেছি, তার বদলে আমরা `new` কে `build`-এ পরিবর্তন করে Listing 12-9-এর I/O project-তে `Config::build`-এর মতো একটি `Result` return করতে পারতাম। কিন্তু এই ক্ষেত্রে আমরা স্থির করেছি যে কোনো thread ছাড়াই একটি thread pool তৈরি করার চেষ্টা একটি unrecoverable error হবে। তুমি যদি আগ্রহী হও, নিচের signature সহ একটি `build` নামের function লিখে `new` function-এর সাথে তুলনা করে দেখতে পারো:

```rust,ignore
pub fn build(size: usize) -> Result<ThreadPool, PoolCreationError> {
```

#### Thread গুলোকে সংরক্ষণ করার জন্য জায়গা তৈরি করা

যেহেতু এখন আমাদের কাছে pool-এ সংরক্ষণ করার মতো বৈধ সংখ্যক thread আছে কিনা তা জানার উপায় আছে, আমরা সেই thread গুলো তৈরি করে struct return করার আগে `ThreadPool` struct-এ সংরক্ষণ করতে পারি। কিন্তু আমরা কীভাবে একটি thread “store” করবো? চলো আরেকবার `thread::spawn`-এর signature-টি দেখি:

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

`spawn` function একটি `JoinHandle<T>` return করে, যেখানে `T` হলো সেই type যা closure return করে। চলো আমরাও `JoinHandle` ব্যবহার করে দেখি কী হয়। আমাদের ক্ষেত্রে, আমরা thread pool-কে যে closure গুলো পাস করছি সেগুলো connection সামলাবে এবং কিছু return করবে না, তাই `T` হবে unit type `()`।

Listing 21-14-এর code টি compile হবে, কিন্তু এটি এখনও কোনো thread তৈরি করে না। আমরা `ThreadPool`-এর definition পরিবর্তন করেছি `thread::JoinHandle<()>` instance-দের একটি vector ধরে রাখার জন্য, vector-টিকে `size` capacity সহ initialize করেছি, কিছু code চালাতে একটি `for` loop স্থাপন করেছি thread তৈরি করার জন্য, এবং সেগুলো ধারণকারী একটি `ThreadPool` instance return করেছি।

<Listing number="21-14" file-name="src/lib.rs" caption="Creating a vector for `ThreadPool` to hold the threads">

```rust,ignore,not_desired_behavior
use std::thread;

pub struct ThreadPool {
    threads: Vec<thread::JoinHandle<()>>,
}

impl ThreadPool {
    // --snip--
    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        let mut threads = Vec::with_capacity(size);

        for _ in 0..size {
            // create some threads and store them in the vector
        }

        ThreadPool { threads }
    }
    // --snip--
}
```

</Listing>

আমরা library crate-এ `std::thread` কে scope-এ এনেছি কারণ `ThreadPool`-এর vector-এর item-দের type হিসেবে আমরা `thread::JoinHandle` ব্যবহার করছি।

একবার বৈধ size গ্রহণ হলে, আমাদের `ThreadPool` একটি নতুন vector তৈরি করে যা `size` সংখ্যক item ধরে রাখতে পারে। `with_capacity` function `Vec::new`-এর মতোই কাজ করে, কিন্তু একটি গুরুত্বপূর্ণ পার্থক্য সহ: এটি vector-এ আগে থেকেই জায়গা allocate করে। যেহেতু আমরা জানি আমাদের vector-এ `size` সংখ্যক element সংরক্ষণ করতে হবে, তাই এই allocation আগেই করা `Vec::new` ব্যবহারের চেয়ে সামান্য বেশি কার্যকরী, যেটি element insert হওয়ার সময় নিজেকে resize করে।

তুমি যখন আবার `cargo check` চালাবে, এটি সফল হবে।

<!-- Old headings. Do not remove or links may break. -->
<a id ="a-worker-struct-responsible-for-sending-code-from-the-threadpool-to-a-thread"></a>

#### `ThreadPool` থেকে একটি Thread-এ Code পাঠানো

Listing 21-14-এ আমরা `for` loop-এ thread তৈরি করা নিয়ে একটি comment রেখেছিলাম। এখানে আমরা দেখবো কীভাবে আমরা আসলে thread তৈরি করবো। Standard library `thread::spawn` কে thread তৈরির একটি উপায় হিসেবে দেয়, এবং `thread::spawn` thread তৈরি হওয়ার সাথে সাথে চালানোর জন্য কিছু code পাওয়ার আশা করে। তবে আমাদের ক্ষেত্রে, আমরা thread তৈরি করতে চাই এবং সেগুলোকে আমরা পরে যে code পাঠাবো তার জন্য _অপেক্ষা_ করতে বলতে চাই। Standard library-র thread implementation-এ সেটা করার কোনো উপায় নেই; আমাদের নিজেদের এটি implement করতে হবে।

আমরা এই behavior implement করবো `ThreadPool` এবং thread-দের মাঝে একটি নতুন data structure introduce করে, যেটি এই নতুন behavior পরিচালনা করবে। আমরা এই data structure কে _Worker_ বলবো, যা pooling implementation-এ একটি পরিচিত শব্দ। `Worker` কোড তুলে নেয় যা চালানো প্রয়োজন এবং সেই কোড তার thread-এ চালায়।

একটি রেস্তোরাঁর রান্নাঘরে কর্মরত মানুষদের কথা ভাবো: Worker গুলো অপেক্ষা করে যতক্ষণ না customer-দের থেকে order আসে, এবং তারপর তারা সেই order গুলো তুলে নিয়ে পূরণের দায়িত্ব পালন করে।

thread pool-এ `JoinHandle<()>` instance-দের একটি vector সংরক্ষণ করার বদলে আমরা `Worker` struct-এর instance গুলো সংরক্ষণ করবো। প্রতিটি `Worker` একটি মাত্র `JoinHandle<()>` instance সংরক্ষণ করবে। তারপর, আমরা `Worker`-এ একটি method implement করবো যা চালানোর জন্য closure নেবে এবং সেটিকে ইতিমধ্যে চলমান thread-এ execute করার জন্য পাঠাবে। আমরা প্রতিটি `Worker`-কে একটি `id`-ও দেবো, যাতে logging বা debugging এর সময় pool-এর ভিন্ন ভিন্ন `Worker` instance গুলোর মধ্যে পার্থক্য করা যায়।

একটি `ThreadPool` তৈরি করার সময় যে নতুন process টি ঘটবে তা এখানে দেওয়া হলো। এইভাবে `Worker` setup হওয়ার পর আমরা closure কে thread-এ পাঠানোর code implement করবো:

1. একটি `id` এবং একটি `JoinHandle<()>` ধরে রাখে এমন একটি `Worker` struct define করা।
2. `ThreadPool` কে পরিবর্তন করে `Worker` instance-দের একটি vector ধরে রাখা।
3. একটি `id` সংখ্যা নেয় এবং সেই `id` আর একটি empty closure সহ spawn করা thread ধরে রাখে এমন একটি `Worker` instance return করে এমন একটি `Worker::new` function define করা।
4. `ThreadPool::new`-এ, `for` loop counter ব্যবহার করে একটি `id` তৈরি করা, সেই `id` দিয়ে একটি নতুন `Worker` তৈরি করা, এবং সেই `Worker` কে vector-এ সংরক্ষণ করা।

তুমি যদি একটি challenge নিতে চাও, Listing 21-15-এর code দেখার আগে নিজে নিজে এই পরিবর্তন গুলো implement করার চেষ্টা করো।

প্রস্তুত? এখানে Listing 21-15-এ উপরের পরিবর্তন গুলো করার একটি উপায় দেখানো হলো।

<Listing number="21-15" file-name="src/lib.rs" caption="Modifying `ThreadPool` to hold `Worker` instances instead of holding threads directly">

```rust,noplayground
use std::thread;

pub struct ThreadPool {
    workers: Vec<Worker>,
}

impl ThreadPool {
    // --snip--
    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            workers.push(Worker::new(id));
        }

        ThreadPool { workers }
    }
    // --snip--
}

struct Worker {
    id: usize,
    thread: thread::JoinHandle<()>,
}

impl Worker {
    fn new(id: usize) -> Worker {
        let thread = thread::spawn(|| {});

        Worker { id, thread }
    }
}
```

</Listing>

আমরা `ThreadPool`-এর field-টির নাম `threads` থেকে পরিবর্তন করে `workers` করেছি কারণ এটি এখন `JoinHandle<()>` instance-দের বদলে `Worker` instance ধরে রাখছে। আমরা `for` loop-এর counter টি `Worker::new`-এর argument হিসেবে ব্যবহার করি, এবং প্রতিটি নতুন `Worker`-কে `workers` নামের vector-এ সংরক্ষণ করি।

বাইরের code (যেমন আমাদের _src/main.rs_-এর server) কে `ThreadPool`-এর ভেতরে `Worker` struct ব্যবহারের implementation detail জানার দরকার নেই, তাই আমরা `Worker` struct এবং তার `new` function কে private রাখি। `Worker::new` function আমরা যে `id` দিই তা ব্যবহার করে এবং একটি empty closure ব্যবহার করে নতুন thread spawn করে তৈরি করা একটি `JoinHandle<()>` instance সংরক্ষণ করে।

> Note: যদি operating system-এ পর্যাপ্ত system resource না থাকার কারণে thread তৈরি করতে না পারে, তবে `thread::spawn` panic করবে। সেটি আমাদের সম্পূর্ণ server কে panic করাবে, যদিও কিছু thread তৈরি সফল হতে পারে। সরলতার খাতিরে এই behavior মেনে নেওয়া ঠিক আছে, কিন্তু একটি production thread pool implementation-এ তুমি সম্ভবত [`std::thread::Builder`][builder]<!-- ignore --> এবং তার `Result` return করা [`spawn`][builder-spawn]<!-- ignore --> method ব্যবহার করতে চাইবে।

এই code টি compile হবে এবং `ThreadPool::new`-কে argument হিসেবে দেওয়া সংখ্যক `Worker` instance সংরক্ষণ করবে। কিন্তু আমরা _এখনও_ `execute`-এ পাওয়া closure টি process করছি না। চলো পরে সেটা কীভাবে করবো তা দেখি।

#### Channel-এর মাধ্যমে Thread-দের কাছে Request পাঠানো

পরের সমস্যা যেটা আমরা সামলাবো সেটা হলো `thread::spawn`-কে দেওয়া closure গুলো একেবারেই কিছু করে না। বর্তমানে আমরা `execute` method-এ যে closure টি execute করতে চাই তা পাই। কিন্তু `ThreadPool` তৈরি করার সময় প্রতিটি `Worker` তৈরি করার সময় আমাদের `thread::spawn`-কে একটি closure দিতে হবে যা সে চালাবে।

আমরা চাই এইমাত্র তৈরি করা `Worker` struct গুলো `ThreadPool`-এ ধরে রাখা একটি queue থেকে চালানোর কোড fetch করুক এবং সেই কোড তার thread-কে চালানোর জন্য পাঠাক।

Chapter 16-তে আমরা যে channel গুলো সম্পর্কে শিখেছি—দুটি thread-এর মধ্যে যোগাযোগের একটি সরল উপায়—এই use case-এর জন্য নিখুঁত। আমরা একটি channel কে job-দের queue হিসেবে কাজ করতে ব্যবহার করবো, এবং `execute` একটি job কে `ThreadPool` থেকে `Worker` instance গুলোতে পাঠাবে, যারা সেই job কে তাদের thread-এ পাঠাবে। এখানে পরিকল্পনা:

1. `ThreadPool` একটি channel তৈরি করবে এবং sender ধরে রাখবে।
2. প্রতিটি `Worker` receiver ধরে রাখবে।
3. আমরা একটি নতুন `Job` struct তৈরি করবো যা channel-এর মাধ্যমে পাঠানো closure গুলো ধরে রাখবে।
4. `execute` method তার execute করতে চাওয়া job কে sender এর মাধ্যমে পাঠাবে।
5. তার thread-এ, `Worker` তার receiver-এর ওপর loop করবে এবং যেকোনো পাওয়া job-এর closure গুলো execute করবে।

চলো শুরু করি `ThreadPool::new`-এ একটি channel তৈরি করে এবং Listing 21-16-এ দেখানো অনুযায়ী `ThreadPool` instance-এ sender ধরে রেখে। `Job` struct টি আপাতত কিছু ধরে রাখে না কিন্তু এটিই সেই type যা আমরা channel-এ পাঠানো item হিসেবে ব্যবহার করবো।

<Listing number="21-16" file-name="src/lib.rs" caption="Modifying `ThreadPool` to store the sender of a channel that transmits `Job` instances">

```rust,noplayground
use std::{sync::mpsc, thread};

pub struct ThreadPool {
    workers: Vec<Worker>,
    sender: mpsc::Sender<Job>,
}

struct Job;

impl ThreadPool {
    // --snip--
    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        let (sender, receiver) = mpsc::channel();

        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            workers.push(Worker::new(id));
        }

        ThreadPool { workers, sender }
    }
    // --snip--
}
```

</Listing>

`ThreadPool::new`-এ আমরা আমাদের নতুন channel তৈরি করি এবং pool-কে sender ধরে রাখতে বলি। এটি সফলভাবে compile হবে।

চলো thread pool channel তৈরি করার সময় প্রতিটি `Worker`-এ channel-এর receiver পাস করার চেষ্টা করি। আমরা জানি `Worker` instance গুলো যে thread spawn করে সেই thread-এ আমরা receiver ব্যবহার করতে চাই, তাই আমরা closure-এ `receiver` parameter কে reference করবো। Listing 21-17-এর code টি এখনও ঠিকমতো compile হবে না।

<Listing number="21-17" file-name="src/lib.rs" caption="Passing the receiver to each `Worker`">

```rust,ignore,does_not_compile
impl ThreadPool {
    // --snip--
    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        let (sender, receiver) = mpsc::channel();

        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            workers.push(Worker::new(id, receiver));
        }

        ThreadPool { workers, sender }
    }
    // --snip--
}

// --snip--

impl Worker {
    fn new(id: usize, receiver: mpsc::Receiver<Job>) -> Worker {
        let thread = thread::spawn(|| {
            receiver;
        });

        Worker { id, thread }
    }
}
```

</Listing>

আমরা কিছু ছোটখাটো সরল পরিবর্তন করেছি: আমরা receiver কে `Worker::new`-এ পাস করি, এবং তারপর সেটি closure-এর ভেতরে ব্যবহার করি।

আমরা যখন এই code টি check করার চেষ্টা করি, নিচের error টি পাই:

```console
$ cargo check
    Checking hello v0.1.0 (file:///projects/hello)
error[E0382]: use of moved value: `receiver`
  --> src/lib.rs:26:42
   |
21 |         let (sender, receiver) = mpsc::channel();
   |                      -------- move occurs because `receiver` has type `std::sync::mpsc::Receiver<Job>`, which does not implement the `Copy` trait
...
25 |         for id in 0..size {
   |         ----------------- inside of this loop
26 |             workers.push(Worker::new(id, receiver));
   |                                          ^^^^^^^^ value moved here, in previous iteration of loop
   |
note: consider changing this parameter type in method `new` to borrow instead if owning the value isn't necessary
  --> src/lib.rs:47:33
   |
47 |     fn new(id: usize, receiver: mpsc::Receiver<Job>) -> Worker {
   |        --- in this method       ^^^^^^^^^^^^^^^^^^^ this parameter takes ownership of the value

For more information about this error, try `rustc --explain E0382`.
error: could not compile `hello` (lib) due to 1 previous error
```

code টি `receiver` কে একাধিক `Worker` instance-এ পাস করার চেষ্টা করছে। এটি কাজ করবে না, যেমনটা Chapter 16 থেকে তোমার মনে পড়বে: Rust-এর channel implementation টি multiple _producer_, single _consumer_। এর মানে আমরা শুধু channel-এর consuming end কে clone করে এই code ঠিক করতে পারবো না। আমরা একাধিক consumer-কে একটি message একাধিকবার পাঠাতেও চাই না; আমরা চাই একাধিক `Worker` instance সহ একটি message list, যেখানে প্রতিটি message একবারই process হবে।

এছাড়া, channel queue থেকে একটি job তোলার কাজে `receiver` কে mutate করা জড়িত, তাই thread গুলোর `receiver` কে share এবং modify করার নিরাপদ উপায় দরকার; অন্যথায়, আমরা race condition-এ পড়তে পারি (যেমন Chapter 16-তে আলোচনা করেছি)।

Chapter 16-তে আলোচিত thread-safe smart pointer গুলো মনে করো: একাধিক thread-এ ownership share করতে এবং thread গুলোকে মান mutate করতে দিতে আমাদের `Arc<Mutex<T>>` ব্যবহার করতে হবে। `Arc` type একাধিক `Worker` instance-কে receiver-এর owner হতে দেবে, এবং `Mutex` নিশ্চিত করবে যে একই সময়ে শুধু একজন `Worker` receiver থেকে job পাবে। Listing 21-18 আমাদের যে পরিবর্তন গুলো করতে হবে তা দেখায়।

<Listing number="21-18" file-name="src/lib.rs" caption="Sharing the receiver among the `Worker` instances using `Arc` and `Mutex`">

```rust,noplayground
use std::{
    sync::{Arc, Mutex, mpsc},
    thread,
};
// --snip--

impl ThreadPool {
    // --snip--
    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        let (sender, receiver) = mpsc::channel();

        let receiver = Arc::new(Mutex::new(receiver));

        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            workers.push(Worker::new(id, Arc::clone(&receiver)));
        }

        ThreadPool { workers, sender }
    }

    // --snip--
}

// --snip--

impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        // --snip--
    }
}
```

</Listing>

`ThreadPool::new`-এ আমরা receiver-কে একটি `Arc` এবং একটি `Mutex`-এ রাখি। প্রতিটি নতুন `Worker`-এর জন্য আমরা `Arc` কে clone করি reference count বাড়াতে, যাতে `Worker` instance গুলো receiver-এর ownership share করতে পারে।

এই পরিবর্তন গুলোর সাথে code টি compile হয়! আমরা এগিয়ে যাচ্ছি!

#### `execute` Method টি Implement করা

চলো এবার `ThreadPool`-এ `execute` method implement করি। আমরা `Job` কে একটি struct থেকে পরিবর্তন করে একটি trait object-এর type alias-এ পরিণত করবো, যা `execute` যে type-এর closure গ্রহণ করে তা ধরে রাখে। Chapter 20-এর [“Type Synonyms and Type Aliases”][type-aliases]<!-- ignore --> section-এ যেমন আলোচনা করা হয়েছে, type alias আমাদের ব্যবহারের সুবিধার জন্য দীর্ঘ type কে ছোট করতে দেয়। Listing 21-19 দেখো।

<Listing number="21-19" file-name="src/lib.rs" caption="Creating a `Job` type alias for a `Box` that holds each closure and then sending the job down the channel">

```rust,noplayground
// --snip--

type Job = Box<dyn FnOnce() + Send + 'static>;

impl ThreadPool {
    // --snip--

    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);

        self.sender.send(job).unwrap();
    }
}

// --snip--
```

</Listing>

`execute`-এ পাওয়া closure দিয়ে একটি নতুন `Job` instance তৈরি করার পর আমরা সেই job টি channel-এর sending end দিয়ে পাঠাই। আমরা `send`-এর ক্ষেত্রে `unwrap` call করছি যদি পাঠানো ব্যর্থ হয়। এমনটি হতে পারে যদি, যেমন, আমরা আমাদের সব thread কে execute করা থেকে থামিয়ে দিই, যার মানে receiving end নতুন message গ্রহণ করা বন্ধ করে দিয়েছে। এই মুহূর্তে, আমরা আমাদের thread গুলোকে execute করা থেকে থামাতে পারি না: আমাদের thread গুলো pool যতক্ষণ থাকে ততক্ষণ execute করতে থাকে। আমরা `unwrap` ব্যবহার করছি কারণ আমরা জানি যে ব্যর্থতার case টি ঘটবে না, কিন্তু compiler সেটা জানে না।

কিন্তু আমাদের কাজ এখনও শেষ হয়নি! `Worker`-এ, `thread::spawn`-কে দেওয়া আমাদের closure টি এখনও শুধু channel-এর receiving end-কে _reference_ করছে। এর বদলে আমাদের দরকার closure টি চিরকাল loop করবে, channel-এর receiving end থেকে একটি job চাইবে এবং একটি পেলে সেটি চালাবে। চলো `Worker::new`-এ Listing 21-20-এ দেখানো পরিবর্তন করি।

<Listing number="21-20" file-name="src/lib.rs" caption="Receiving and executing the jobs in the `Worker` instance’s thread">

```rust,noplayground
// --snip--

impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        let thread = thread::spawn(move || {
            loop {
                let job = receiver.lock().unwrap().recv().unwrap();

                println!("Worker {id} got a job; executing.");

                job();
            }
        });

        Worker { id, thread }
    }
}
```

</Listing>

এখানে আমরা প্রথমে `receiver`-এ `lock` call করি mutex acquire করতে, এবং তারপর যেকোনো error-এ panic করতে `unwrap` call করি। lock acquire করা ব্যর্থ হতে পারে যদি mutex _poisoned_ state-এ থাকে, যা ঘটতে পারে যদি অন্য কোনো thread lock ধরে থাকা অবস্থায় panic করে এবং lock release না করে। এই পরিস্থিতিতে, `unwrap` call করে এই thread কে panic করাটাই সঠিক কাজ। তুমি চাইলে এই `unwrap` কে তোমার কাছে অর্থবহ কোনো error message সহ `expect`-এ পরিবর্তন করতে পারো।

যদি আমরা mutex-এর lock পেয়ে যাই, আমরা channel থেকে একটি `Job` receive করতে `recv` call করি। একটি শেষ `unwrap` এখানেও যেকোনো error পার করে যায়, যা ঘটতে পারে যদি sender ধরে রাখা thread shut down করে থাকে, ঠিক যেমনভাবে receiver shut down করলে `send` method `Err` return করে।

`recv` call টি block করে, তাই যদি এখনও কোনো job না থাকে তবে বর্তমান thread একটি job available না হওয়া পর্যন্ত অপেক্ষা করবে। `Mutex<T>` নিশ্চিত করে যে একই সময়ে শুধু একটি `Worker` thread-ই job request করার চেষ্টা করছে।

আমাদের thread pool এখন কার্যকর অবস্থায়! এটিকে একটি `cargo run` দাও এবং কয়েকটা request করো:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-20
cargo run
make some requests to 127.0.0.1:7878
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
warning: field `workers` is never read
 --> src/lib.rs:7:5
  |
6 | pub struct ThreadPool {
  |            ---------- field in this struct
7 |     workers: Vec<Worker>,
  |     ^^^^^^^
  |
  = note: `#[warn(dead_code)]` on by default

warning: fields `id` and `thread` are never read
  --> src/lib.rs:48:5
   |
47 | struct Worker {
   |        ------ fields in this struct
48 |     id: usize,
   |     ^^
49 |     thread: thread::JoinHandle<()>,
   |     ^^^^^^

warning: `hello` (lib) generated 2 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 4.91s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
```

সফল! এখন আমাদের এমন একটি thread pool আছে যেটি connection গুলোকে asynchronously execute করে। কখনোই চারটির বেশি thread তৈরি হয় না, তাই server অনেক request পেলেও আমাদের system overload হবে না। আমরা যদি _/sleep_-এ request করি, server অন্য একটি thread দিয়ে অন্যান্য request গুলো serve করতে পারবে।

> Note: তুমি যদি একসাথে একাধিক browser window-তে _/sleep_ খোলো, সেগুলো হয়তো পাঁচ সেকেন্ড ব্যবধানে একটি একটি করে load হবে। কিছু web browser ক্যাশেিং কারণে একই request-এর একাধিক instance sequentially execute করে। এই সীমাবদ্ধতা আমাদের web server-এর কারণে নয়।

এটি একটু থামে ভাবার উপযুক্ত সময়—যদি আমরা closure-এর বদলে করার জন্য কাজ future ব্যবহার করতাম তাহলে Listing 21-18, 21-19 এবং 21-20-এর code গুলো কীভাবে ভিন্ন হতো। কোন কোন type পরিবর্তন হতো? method signature গুলো কীভাবে ভিন্ন হতো, যদি হতো? code-এর কোন কোন অংশ একই থাকতো?

Chapter 17 এবং Chapter 19-এ `while let` loop সম্পর্কে শেখার পর তুমি ভাবতে পারো আমরা কেন `Worker` thread-এর code টি Listing 21-21-এ দেখানো মতো লিখলাম না।

<Listing number="21-21" file-name="src/lib.rs" caption="An alternative implementation of `Worker::new` using `while let`">

```rust,ignore,not_desired_behavior
// --snip--

impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        let thread = thread::spawn(move || {
            while let Ok(job) = receiver.lock().unwrap().recv() {
                println!("Worker {id} got a job; executing.");

                job();
            }
        });

        Worker { id, thread }
    }
}
```

</Listing>

এই code টি compile হয় এবং চলেও, কিন্তু কাঙ্ক্ষিত threading behavior দেয় না: একটি slow request এখনও অন্যান্য request-এর অপেক্ষা করতে বাধ্য করবে। কারণটা কিছুটা সূক্ষ্ম: `Mutex` struct-এর কোনো public `unlock` method নেই, কারণ lock-এর ownership `lock` method যে `LockResult<MutexGuard<T>>` return করে তার ভেতরের `MutexGuard<T>`-এর lifetime-এর ওপর ভিত্তি করে থাকে। Compile করার সময়, borrow checker তখন এই নিয়ম enforce করতে পারে যে একটি `Mutex` দ্বারা সুরক্ষিত resource-এ আমরা lock ধরে না থাকলে access করা যাবে না। তবে, এই implementation এর ফলে আমরা যদি `MutexGuard<T>`-এর lifetime সম্পর্কে সচেতন না থাকি তবে lock প্রত্যাশার চেয়ে বেশি সময় ধরে রাখা হতে পারে।

Listing 21-20-এর code যেটি `let job = receiver.lock().unwrap().recv().unwrap();` ব্যবহার করে তা কাজ করে কারণ `let`-এর ক্ষেত্রে, সমান চিহ্নের ডান পাশের expression-এ ব্যবহৃত যেকোনো temporary value `let` statement শেষ হলেই সাথে সাথে drop হয়ে যায়। তবে, `while let` (এবং `if let` এবং `match`) associated block-এর শেষ না হওয়া পর্যন্ত temporary value গুলো drop করে না। Listing 21-21-এ, `job()` call চলাকালীন পুরো সময় lock ধরে রাখা থাকে, যার মানে অন্যান্য `Worker` instance job গ্রহণ করতে পারে না।

[type-aliases]: ch20-03-advanced-types.html#type-synonyms-and-type-aliases
[integer-types]: ch03-02-data-types.html#integer-types
[moving-out-of-closures]: ch13-01-closures.html#moving-captured-values-out-of-closures
[builder]: ../std/thread/struct.Builder.html
[builder-spawn]: ../std/thread/struct.Builder.html#method.spawn

## Futures এবং Async Syntax

Rust-এ asynchronous programming-এর মূল উপাদানগুলো হলো _futures_ এবং Rust-এর `async` ও `await` keyword।

একটি _future_ হলো এমন একটি value যা এখনই ready নাও হতে পারে কিন্তু ভবিষ্যতে কোনো এক সময়ে ready হবে। (একই ধারণা অনেক ভাষায় দেখা যায়, কখনো অন্য নামে যেমন _task_ বা _promise_।) Rust একটি `Future` trait building block হিসেবে দেয়, যাতে ভিন্ন ভিন্ন async operation ভিন্ন data structure দিয়ে ইমপ্লিমেন্ট করা যায়, কিন্তু একটি common interface-এ। Rust-এ future হলো এমন type যা `Future` trait ইমপ্লিমেন্ট করে। প্রতিটি future নিজের কাছে রাখে কতটুকু অগ্রগতি হয়েছে এবং “ready” মানে কী, তার তথ্য।

তুমি `async` keyword-টি block ও function-এ প্রয়োগ করতে পারো, যাতে সেটি interrupt ও resume হতে পারে বলে উল্লেখ করা যায়। একটি async block বা async function-এর ভেতরে তুমি `await` keyword ব্যবহার করে একটি _future-কে await_ করতে পারো (অর্থাৎ, সেটি ready হওয়া পর্যন্ত অপেক্ষা করতে পারো)। Async block বা function-এর ভেতরে যেখানেই তুমি কোনো future-কে await করবে, সেটি সেই block বা function-এর জন্য pause ও resume-এর একটি potential spot। কোনো future-এর সাথে যোগাযোগ করে দেখা যে তার value এসেছে কি না, সেই প্রক্রিয়াকে বলে _polling_।

C# ও JavaScript-এর মতো আরও কিছু ভাষাও async programming-এর জন্য `async` ও `await` keyword ব্যবহার করে। তুমি যদি সেই ভাষাগুলোর সাথে পরিচিত হও, তবে হয়তো লক্ষ্য করবে যে Rust এই syntax কীভাবে সামলায় তাতে কিছু বড় পার্থক্য আছে। এর যথেষ্ট ভালো কারণ আছে, যেমন আমরা দেখব!

Async Rust লেখার সময় আমরা বেশিরভাগ ক্ষেত্রেই `async` ও `await` keyword ব্যবহার করি। Rust সেগুলোকে `Future` trait ব্যবহার করে সমমানের কোডে compile করে, ঠিক যেমন সে `for` loop-কে `Iterator` trait ব্যবহার করে সমমানের কোডে compile করে। যেহেতু Rust নিজে `Future` trait দেয়, তাই তুমি চাইলে প্রয়োজনে নিজের data type-এর জন্য সেটি ইমপ্লিমেন্ট করতে পারো। এই chapter জুড়ে যে function-গুলো দেখব তাদের অনেকেই নিজস্ব `Future` ইমপ্লিমেন্টেশন সহ type return করে। Chapter-এর শেষে আমরা এই trait-এর definition-এ ফিরে গিয়ে আরও বিস্তারিত দেখব, তবে এখন যতটুকু বলা হয়েছে তাতেই এগিয়ে যাওয়ার জন্য যথেষ্ট।

এটা হয়তো কিছুটা abstract মনে হতে পারে, তাই চলো আমাদের প্রথম async প্রোগ্রামটি লিখি: একটি ছোট web scraper। আমরা command line থেকে দুটি URL নেব, সে দুটিকে concurrently fetch করব, এবং যেটি আগে শেষ হয় তার result return করব। এই উদাহরণে বেশ কিছু নতুন syntax থাকবে, কিন্তু চিন্তা কোরো না—এগোনোর সময় যা যা জানা দরকার তার সবই বুঝিয়ে দেব।

## আমাদের প্রথম Async প্রোগ্রাম

এই chapter-এর ফোকাস যাতে async শেখায় থাকে, সেটা নিশ্চিত করতে আর ecosystem-এর বিভিন্ন অংশ নিয়ে ঘাঁটাঘাঁটি না করতে হয়, সে জন্য আমরা `trpl` crate তৈরি করেছি (`trpl` হলো “The Rust Programming Language”-এর সংক্ষিপ্ত রূপ)। এটি সেই সব type, trait ও function re-export করে যা তোমার দরকার হবে, প্রধানত [`futures`][futures-crate]<!-- ignore --> এবং [`tokio`][tokio]<!-- ignore --> crate থেকে। `futures` crate হলো Rust-এ async code নিয়ে experiment করার একটি official জায়গা, আর `Future` trait মূলত সেখানেই ডিজাইন করা হয়েছিল। Tokio হলো আজ Rust-এ সবচেয়ে বেশি ব্যবহৃত async runtime, বিশেষ করে web application-এর জন্য। বাইরে আরও অনেক চমৎকার runtime আছে, এবং তোমার উদ্দেশ্যে সেগুলো হয়তো বেশি উপযুক্তও। `trpl`-এর ভেতরে আমরা `tokio` crate ব্যবহার করি কারণ এটি ভালোভাবে টেস্ট করা ও ব্যাপকভাবে ব্যবহৃত।

কিছু ক্ষেত্রে `trpl` মূল API-কে rename বা wrap করেও দেয়, যাতে তুমি এই chapter-এর প্রাসঙ্গিক বিষয়েই মনোযোগ দিতে পারো। এই crate আসলে কী করে তা বুঝতে চাইলে আমরা তোমাকে [its source code][crate-source] দেখতে উৎসাহিত করব। সেখানে দেখতে পাবে প্রতিটি re-export কোন crate থেকে এসেছে, এবং আমরা বিস্তারিত comment রেখে দিয়েছি যে crate কী করে।

`hello-async` নামে একটি নতুন binary project তৈরি করো এবং dependency হিসেবে `trpl` crate যোগ করো:

```console
$ cargo new hello-async
$ cd hello-async
$ cargo add trpl
```

এখন আমরা `trpl` থেকে পাওয়া বিভিন্ন অংশ ব্যবহার করে আমাদের প্রথম async প্রোগ্রামটি লিখতে পারি। আমরা একটি ছোট command line tool বানাবো যেটি দুটি web page fetch করবে, প্রতিটির `<title>` element বের করবে, এবং যে পেজ এই পুরো প্রক্রিয়ায় আগে শেষ করবে তার title print করবে।

### `page_title` Function সংজ্ঞায়িত করা

চলো এমন একটি function দিয়ে শুরু করি যেটি একটি page URL parameter হিসেবে নেয়, সেটিতে request পাঠায়, এবং `<title>` element-এর text return করে (Listing 17-1 দেখো)।

<Listing number="17-1" file-name="src/main.rs" caption="Defining an async function to get the title element from an HTML page">

```rust
use trpl::Html;

async fn page_title(url: &str) -> Option<String> {
    let response = trpl::get(url).await;
    let response_text = response.text().await;
    Html::parse(&response_text)
        .select_first("title")
        .map(|title| title.inner_html())
}
```

</Listing>

প্রথমে আমরা `page_title` নামে একটি function সংজ্ঞায়িত করি এবং সেটিতে `async` keyword যোগ করি। তারপর `trpl::get` function ব্যবহার করে যে URL দেওয়া হয়েছে সেটি fetch করি এবং `await` keyword দিয়ে response-টি await করি। `response`-এর text পেতে আমরা তার `text` method call করি এবং আবার `await` keyword দিয়ে সেটি await করি। এই দুটি step-ই asynchronous। `get` function-এর ক্ষেত্রে, আমাদের সার্ভারের দিক থেকে response-এর প্রথম অংশ পাঠানোর অপেক্ষা করতে হয়, যার মধ্যে HTTP header, cookie ইত্যাদি থাকে এবং যা response body থেকে আলাদাভাবে deliver হতে পারে। বিশেষ করে body খুব বড় হলে পুরোটা এসে পৌঁছাতে কিছু সময় লাগতে পারে। যেহেতু আমাদের response-এর _সম্পূর্ণ অংশ_ এসে পৌঁছানোর অপেক্ষা করতে হয়, তাই `text` method-টিও async।

আমাদের এই দুটি future-কেই স্পষ্টভাবে await করতে হয়, কারণ Rust-এ future গুলো _lazy_: তুমি `await` keyword দিয়ে না চাইলে তারা কিছুই করে না। (আসলে, তুমি কোনো future ব্যবহার না করলে Rust একটি compiler warning দেখাবে।) এটা হয়তো Chapter 13-এর [“Processing a Series of Items with Iterators”][iterators-lazy]<!-- ignore --> section-এ iterator নিয়ে আলোচনার কথা মনে করিয়ে দেবে। Iterator তার `next` method call না করা পর্যন্ত কিছুই করে না—সরাসরি হোক বা `for` loop বা `map`-এর মতো method-এর মাধ্যমে যা ভেতরে ভেতরে `next` ব্যবহার করে। একইভাবে, future-ও স্পষ্টভাবে না চাইলে কিছু করে না। এই laziness-এর কারণে Rust async code-কে ততক্ষণ পর্যন্ত না চালায় যতক্ষণ না সেটি আসলেই দরকার।

> Note: এটি Chapter 16-এর [“Creating a New Thread with spawn”][thread-spawn]<!-- ignore --> section-এ `thread::spawn` ব্যবহার করার সময় যা আচরণ দেখেছিলাম তার থেকে আলাদা, যেখানে আমরা অন্য thread-কে যে closure দিয়েছিলাম সেটি সাথে সাথেই চলতে শুরু করেছিল। এটি অনেক অন্য ভাষা কীভাবে async-কে সামলায় তার থেকেও আলাদা। কিন্তু Rust-এর জন্য তার performance guarantee দিতে এটি গুরুত্বপূর্ণ, ঠিক যেমন iterator-এর ক্ষেত্রে।

`response_text` একবার পেলে আমরা সেটিকে `Html::parse` ব্যবহার করে `Html` type-এর একটি instance-এ parse করতে পারি। Raw string-এর বদলে এখন আমাদের কাছে এমন একটি data type আছে যা দিয়ে HTML-কে আরও সমৃদ্ধ data structure হিসেবে নাড়াচাড়া করা যায়। বিশেষ করে, আমরা `select_first` method ব্যবহার করে কোনো দেওয়া CSS selector-এর প্রথম instance খুঁজে পেতে পারি। `"title"` string দিলে আমরা document-এ প্রথম `<title>` element পেয়ে যাব, যদি কোনোটি থাকে। যেহেতু কোনো matching element নাও থাকতে পারে, তাই `select_first` একটি `Option<ElementRef>` return করে। শেষে আমরা `Option::map` method ব্যবহার করি, যা `Option`-এ item থাকলে তার সাথে কাজ করতে দেয়, আর না থাকলে কিছুই করে না। (এখানে আমরা `match` expression-ও ব্যবহার করতে পারতাম, কিন্তু `map` বেশি idiomatic।) `map`-এ আমরা যে function দিই তার body-তে আমরা `title`-এর `inner_html` call করে তার content পাই, যা একটি `String`। সবশেষে আমরা একটি `Option<String>` পাই।

খেয়াল করো যে Rust-এর `await` keyword তুমি যে expression-টি await করছ তার _পরে_ থাকে, আগে নয়। অর্থাৎ, এটি একটি _postfix_ keyword। অন্য ভাষায় `async` ব্যবহার করে থাকলে এটি তোমার চেনা ধারণার থেকে আলাদা মনে হতে পারে, কিন্তু Rust-এ এর ফলে method-এর chain অনেক বেশি পরিষ্কারভাবে কাজ করা যায়। ফলে আমরা `page_title`-এর body-কে এমনভাবে বদলাতে পারি যাতে `trpl::get` ও `text` function call-এর মাঝে `await` রেখে সেগুলো একসাথে chain করা যায়, যেমনটি Listing 17-2-তে দেখানো হয়েছে।

<Listing number="17-2" file-name="src/main.rs" caption="Chaining with the `await` keyword">

```rust
    let response_text = trpl::get(url).await.text().await;
```

</Listing>

এরকেই দিয়ে আমরা সফলভাবে আমাদের প্রথম async function লিখে ফেললাম! `main`-এ এটিকে call করার আগে চলো আরেকটু কথা বলি আমরা যা লিখলাম তার অর্থ নিয়ে।

যখন Rust `async` keyword দিয়ে চিহ্নিত কোনো _block_ দেখে, সেটি সেটিকে এমন একটি অনন্য, anonymous data type-এ compile করে যা `Future` trait ইমপ্লিমেন্ট করে। আর যখন Rust `async` দিয়ে চিহ্নিত কোনো _function_ দেখে, সেটি সেটিকে এমন একটি non-async function-এ compile করে যার body একটি async block। একটি async function-এর return type হলো সেই anonymous data type-এর type যা compiler সেই async block-এর জন্য তৈরি করে।

তাই, `async fn` লেখা মানে এমন একটি function লেখার সমান যে একটি return type-এর _future_ return করে। Compiler-এর কাছে Listing 17-1-এর `async fn page_title`-এর মতো একটি function definition এই নিচের non-async function-টির সমান:

```rust
# extern crate trpl; // required for mdbook test
use std::future::Future;
use trpl::Html;

fn page_title(url: &str) -> impl Future<Output = Option<String>> {
    async move {
        let text = trpl::get(url).await.text().await;
        Html::parse(&text)
            .select_first("title")
            .map(|title| title.inner_html())
    }
}
```

চলো transformed version-এর প্রতিটি অংশ দেখি:

- এটি Chapter 10-এর [“Traits as Parameters”][impl-trait]<!-- ignore --> section-এ আলোচনা করা `impl Trait` syntax ব্যবহার করে।
- Return করা value `Future` trait ইমপ্লিমেন্ট করে, যার একটি associated type হলো `Output`। খেয়াল করো, `Output` type হলো `Option<String>`, যা `page_title`-এর `async fn` version-এর মূল return type-এর সমান।
- মূল function-এর body-তে call করা সব কোড একটি `async move` block-এ wrap করা। মনে রেখো block গুলো expression। এই পুরো block-টিই function থেকে return করা expression।
- এই async block `Option<String>` type-এর একটি value উৎপন্ন করে, যেমনটি এইমাত্র বলা হয়েছে। সেই value-টি return type-এর `Output` type-এর সাথে মেলে। এটি অন্যান্য block-এর মতোই।
- নতুন function body একটি `async move` block কারণ সে `url` parameter ব্যবহার করে। (`async` ও `async move`-এর পার্থক্য নিয়ে chapter-এ আরও অনেক পরে কথা বলব।)

এখন আমরা `main`-এ `page_title` call করতে পারি।

<!-- Old headings. Do not remove or links may break. -->

<a id ="determining-a-single-pages-title"></a>

### একটি Runtime দিয়ে Async Function Execute করা

শুরুতে আমরা একটি single page-এর title পাব, যেমন Listing 17-3-তে দেখানো হয়েছে। দুর্ভাগ্যক্রমে, এই কোড এখনো compile হয় না।

<Listing number="17-3" file-name="src/main.rs" caption="Calling the `page_title` function from `main` with a user-supplied argument">

```rust,ignore,does_not_compile
async fn main() {
    let args: Vec<String> = std::env::args().collect();
    let url = &args[1];
    match page_title(url).await {
        Some(title) => println!("The title for {url} was {title}"),
        None => println!("{url} had no title"),
    }
}
```

</Listing>

আমরা Chapter 12-এর [“Accepting Command Line Arguments”][cli-args]<!-- ignore --> section-এ command line argument নেওয়ার যে pattern ব্যবহার করেছি, এখানেও সেটাই অনুসরণ করলাম। তারপর URL argument-টি `page_title`-কে দিই এবং result await করি। যেহেতু future থেকে উৎপন্ন value একটি `Option<String>`, তাই আমরা একটি `match` expression ব্যবহার করে page-এ `<title>` আছে কি না, তা হিসাব করে আলাদা message print করি।

`await` keyword আমরা শুধু async function বা block-এই ব্যবহার করতে পারি, আর Rust আমাদের বিশেষ `main` function-কে `async` হিসেবে চিহ্নিত করতে দেবে না।

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-03
cargo build
copy just the compiler error
-->

```text
error[E0752]: `main` function is not allowed to be `async`
 --> src/main.rs:6:1
  |
6 | async fn main() {
  | ^^^^^^^^^^^^^^^ `main` function is not allowed to be `async`
```

`main`-কে `async` হিসেবে চিহ্নিত করা যায় না, কারণ async code-এর একটি _runtime_ দরকার: এমন একটি Rust crate যা asynchronous code execute করার বিস্তারিত পরিচালনা করে। একটি প্রোগ্রামের `main` function একটি runtime _initialize_ করতে পারে, কিন্তু নিজে একটি runtime _নয়_। (এর কারণ কী, সেটা একটু পরে দেখব।) প্রতিটি Rust প্রোগ্রাম যা async code execute করে, তার কমপক্ষে এমন একটি জায়গা থাকে যেখানে সে future execute করা একটি runtime সেট আপ করে।

অধিকাংশ ভাষা যারা async সাপোর্ট করে তারা একটি runtime bundle করে দেয়, কিন্তু Rust দেয় না। বরং অনেকগুলো ভিন্ন async runtime পাওয়া যায়, প্রতিটি তার লক্ষ্য করা use case-এর জন্য উপযুক্ত ভিন্ন tradeoff নিয়ে তৈরি। যেমন, অনেক CPU core এবং প্রচুর RAM সহ একটি high-throughput web সার্ভারের প্রয়োজন একেবারেই আলাদা, যেখানে একটি single core, সামান্য RAM এবং কোনো heap allocation ক্ষমতা নেই এমন একটি microcontrollerের প্রয়োজন আলাদা। এই runtime দেওয়া crate গুলো সাধারণত file বা নেটওয়ার্ক I/O-এর মতো সাধারণ কার্যকারিতার async version-ও দেয়।

এখানে, এবং এই chapter-এর বাকি অংশ জুড়ে, আমরা `trpl` crate থেকে `block_on` function ব্যবহার করব, যেটি একটি future argument হিসেবে নেয় এবং সেই future সম্পূর্ণ না হওয়া পর্যন্ত current thread block করে রাখে। পর্দার আড়ালে `block_on` call করলে `tokio` crate ব্যবহার করে একটি runtime সেট আপ করা হয় যা দেওয়া future-টি চালায় (অন্য runtime crate-এর `block_on` function-এর সাথে `trpl` crate-এর `block_on`-এর আচরণ প্রায় একই)। Future সম্পূর্ণ হলে `block_on` সেই future যে value উৎপন্ন করেছে সেটি return করে।

আমরা `page_title` থেকে return হওয়া future-টি সরাসরি `block_on`-কে দিতে পারতাম, এবং সেটি সম্পূর্ণ হলে Listing 17-3-এ যেমন চেষ্টা করেছিলাম তেমনভাবেই resulting `Option<String>`-এর ওপর match করতে পারতাম। তবে এই chapter-এর বেশিরভাগ উদাহরণে (এবং বাস্তবে বেশিরভাগ async code-এ), আমরা শুধু একটি async function call করার বেশি কিছু করব, তাই বরং আমরা একটি `async` block পাস করব এবং `page_title` call-এর result স্পষ্টভাবে await করব, যেমন Listing 17-4-এ।

<Listing number="17-4" caption="Awaiting an async block with `trpl::block_on`" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook test does not pass args -->

```rust,should_panic,noplayground
fn main() {
    let args: Vec<String> = std::env::args().collect();

    trpl::block_on(async {
        let url = &args[1];
        match page_title(url).await {
            Some(title) => println!("The title for {url} was {title}"),
            None => println!("{url} had no title"),
        }
    })
}
```

</Listing>

এই কোড চালালে আমরা যে আচরণ প্রথমে আশা করেছিলাম তা-ই পাব:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-04
cargo build # skip all the build noise
cargo run -- "https://www.rust-lang.org"
# copy the output here
-->

```console
$ cargo run -- "https://www.rust-lang.org"
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.05s
     Running `target/debug/async_await 'https://www.rust-lang.org'`
The title for https://www.rust-lang.org was
            Rust Programming Language
```

ফু—অবশেষে আমরা কিছু কাজ করা async code পেলাম! কিন্তু দুটি site-এর মধ্যে race করার কোড যোগ করার আগে, চলো সাময়িকভাবে ফিরে যাই future গুলো কীভাবে কাজ করে তা দেখতে।

প্রতিটি _await point_—অর্থাৎ, যেখানে কোড `await` keyword ব্যবহার করে—সেখানে control runtime-এর হাতে ফিরে যায়। এটি কাজ করাতে Rust-কে async block-এর state ট্র্যাক রাখতে হয়, যাতে runtime কিছু অন্য কাজ শুরু করতে পারে এবং পরে প্রথমটিতে আবার এগোনোর চেষ্টা করতে পারে। এটি একটি অদৃশ্য state machine, যেমন তুমি প্রতিটি await point-এ current state সংরক্ষণ করতে নিচের মতো একটি enum লিখতে:

```rust
enum PageTitleFuture<'a> {
    Initial { url: &'a str },
    GetAwaitPoint { url: &'a str },
    TextAwaitPoint { response: trpl::Response },
}
```

তবে প্রতিটি state-এর মধ্যে রূপান্তরের কোড হাতে লিখলে সেটি বেশ ক্লান্তিকর এবং ভুলের সম্ভাবনাপূর্ণ, বিশেষ করে যখন তোমাকে পরে আরও কার্যকারিতা ও আরও state যোগ করতে হবে। সৌভাগ্যক্রমে, Rust compiler async code-এর জন্য state machine data structure স্বয়ংক্রিয়ভাবে তৈরি ও পরিচালনা করে। Data structure-এর চারপাশের স্বাভাবিক borrowing ও ownership নিয়ম সবই প্রযোজ্য থাকে, এবং খুশির ব্যাপার, compiler সেগুলোও check করে দেয় এবং কার্যকর error message দেয়। সেগুলোর কয়েকটি নিয়ে আমরা chapter-এ আরও পরে কাজ করব।

শেষ পর্যন্ত, এই state machine-টি যে কাউকে execute করতে হয়, আর সেটি হলো একটি runtime। (তাই হয়তো runtime নিয়ে পড়তে গিয়ে তুমি _executor_ শব্দের উল্লেখ দেখেছ: executor হলো runtime-এর সেই অংশ যা async code execute করার দায়িত্বে থাকে।)

এখন তুমি বুঝতে পারছ কেন Listing 17-3-এ compiler আমাদের `main`-কে নিজে একটি async function বানতে বারণ করেছিল। যদি `main` একটি async function হতো, তাহলে `main` যে future return করত তার state machine পরিচালনা করার জন্য অন্য কারও দরকার হতো, কিন্তু `main` তো প্রোগ্রামের শুরুর জায়গা! বরং আমরা `main`-এ `trpl::block_on` function call করে একটি runtime সেট আপ করি এবং `async` block থেকে return হওয়া future-টিকে সম্পূর্ণ না হওয়া পর্যন্ত চালাই।

> Note: কিছু runtime macro দেয়, যাতে তুমি একটি async `main` function লিখতে _পারো_। সেই macro গুলো `async fn main() { ... }`-কে একটি সাধারণ `fn main` হিসেবে rewrite করে, যা Listing 17-4-এ আমরা হাতে যা করেছি সেটাই করে: এমন একটি function call করে যা একটি future-কে `trpl::block_on`-এর মতো সম্পূর্ণ না হওয়া পর্যন্ত চালায়।

এখন চলো এই অংশগুলো একসাথে যোগ করি এবং দেখি কীভাবে আমরা concurrent code লিখতে পারি।

<!-- Old headings. Do not remove or links may break. -->

<a id="racing-our-two-urls-against-each-other"></a>

### দুটি URL-কে Concurrently একে অপরের সাথে Race করানো

Listing 17-5-এ আমরা command line থেকে দেওয়া দুটি ভিন্ন URL দিয়ে `page_title` call করি এবং যে future আগে শেষ হয় সেটি select করে race করাই।

<Listing number="17-5" caption="Calling `page_title` for two URLs to see which returns first" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook does not pass args -->

```rust,should_panic,noplayground
use trpl::{Either, Html};

fn main() {
    let args: Vec<String> = std::env::args().collect();

    trpl::block_on(async {
        let title_fut_1 = page_title(&args[1]);
        let title_fut_2 = page_title(&args[2]);

        let (url, maybe_title) =
            match trpl::select(title_fut_1, title_fut_2).await {
                Either::Left(left) => left,
                Either::Right(right) => right,
            };

        println!("{url} returned first");
        match maybe_title {
            Some(title) => println!("Its page title was: '{title}'"),
            None => println!("It had no title."),
        }
    })
}

async fn page_title(url: &str) -> (&str, Option<String>) {
    let response_text = trpl::get(url).await.text().await;
    let title = Html::parse(&response_text)
        .select_first("title")
        .map(|title| title.inner_html());
    (url, title)
}
```

</Listing>

আমরা শুরু করি user-দের দেওয়া প্রতিটি URL-এর জন্য `page_title` call করে। Resulting future-গুলো `title_fut_1` ও `title_fut_2` নামে সংরক্ষণ করি। মনে রেখো, এগুলো এখনো কিছু করে না, কারণ future lazy এবং আমরা এখনও সেগুলোকে await করিনি। তারপর সেই future-গুলো `trpl::select`-কে দিই, যেটি এমন একটি value return করে যা বোঝায় দেওয়া future-গুলোর মধ্যে কোনটি আগে শেষ হয়েছে।

> Note: পর্দার আড়ালে `trpl::select` `futures` crate-এ সংজ্ঞায়িত আরও general একটি `select` function-এর ওপর তৈরি। `futures` crate-এর `select` function অনেক কিছু করতে পারে যা `trpl::select` পারে না, কিন্তু তার সাথে কিছু অতিরিক্ত জটিলতাও আছে যা আমরা এখন এড়িয়ে যেতে পারি।

যেকোনো future-ই বৈধভাবে “জিততে” পারে, তাই একটি `Result` return করার কোনো মানে নেই। বরং `trpl::select` এমন একটি type return করে যা আমরা আগে দেখিনি, `trpl::Either`। `Either` type `Result`-এর মতোই একটু, কারণ এর দুটি case আছে। তবে `Result`-এর মতো নয়, `Either`-এ success বা failure-এর কোনো ধারণা থাকে না। বরং এটি “এটা বা ওটা” বোঝাতে `Left` ও `Right` ব্যবহার করে:

```rust
enum Either<A, B> {
    Left(A),
    Right(B),
}
```

`select` function প্রথম argument জিতলে সেই future-এর output সহ `Left` return করে, আর দ্বিতীয় future argument জিতলে তার output সহ `Right` return করে। এটি function call-এর সময় argument-গুলো যে ক্রমে থাকে তার সাথে মেলে: প্রথম argument দ্বিতীয়টির বাঁয়ে থাকে।

আমরা আরও `page_title` আপডেট করে দেওয়া URL-টিই আবার return করি। এভাবে, যদি আগে return হওয়া page-এ আমরা যে `<title>` resolve করতে পারি সেটি না থাকে, তবুও একটি অর্থপূর্ণ message print করতে পারব। সেই তথ্য হাতে রেখে, আমরা শেষে আমাদের `println!` output আপডেট করি যাতে বোঝানো যায় কোন URL আগে শেষ করেছে এবং সেই URL-এর web page-এর `<title>` কী, যদি থাকে।

তোমার এখন একটি ছোট কাজ করা web scraper তৈরি! দুটো URL বেছে নাও এবং command line tool-টি চালাও। তুমি হয়তো খুঁজে পাবে যে কিছু site সবসময় অন্যগুলোর চেয়ে দ্রুত, আবার কিছু ক্ষেত্রে কোন site দ্রুত সেটি run-এর পর পরিবর্তিত হয়। তার চেয়েও বেশি গুরুত্বপূর্ণ, তুমি future নিয়ে কাজ করার মৌলিক বিষয়গুলো শিখেছ, তাই এখন আমরা async দিয়ে আরও কী করা যায় সেটাতে গভীরভাবে নামতে পারি।

[impl-trait]: ch10-02-traits.html#traits-as-parameters
[iterators-lazy]: ch13-02-iterators.html
[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[cli-args]: ch12-01-accepting-command-line-arguments.html

<!-- TODO: map source link version to version of Rust? -->

[crate-source]: https://github.com/rust-lang/book/tree/main/packages/trpl
[futures-crate]: https://crates.io/crates/futures
[tokio]: https://tokio.rs

<!-- Old headings. Do not remove or links may break. -->

<a id="concurrency-with-async"></a>

## Async দিয়ে Concurrency প্রয়োগ করা

এই section-এ আমরা Chapter 16-এ thread দিয়ে যে concurrency-র চ্যালেঞ্জগুলো সামলেছিলাম, তার কিছুতে async প্রয়োগ করব। যেহেতু আগেই আমরা অনেক মূল ধারণা নিয়ে আলোচনা করেছি, এখানে আমরা thread ও future-এর মধ্যে পার্থক্য কী, সেদিকেই বেশি মনোযোগ দেব।

অনেক ক্ষেত্রে, async ব্যবহার করে concurrency করার API গুলো thread ব্যবহারের API-এর সাথে অনেকটাই মিল। আবার কিছু ক্ষেত্রে সেগুলো বেশ আলাদা। thread ও async-এর API একইরকম _দেখতে_ হলেও, তাদের আচরণ প্রায়ই আলাদা হয়—এবং তাদের performance বৈশিষ্ট্য প্রায় সব সময়েই আলাদা।

<!-- Old headings. Do not remove or links may break. -->

<a id="counting"></a>

### `spawn_task` দিয়ে নতুন Task তৈরি করা

Chapter 16-এর [“Creating a New Thread with `spawn`”][thread-spawn]<!-- ignore --> section-এ আমরা প্রথম যে কাজটি করেছিলাম তা হলো দুটি আলাদা thread-এ গণনা করা। চলো async দিয়ে সেটাই করি। `trpl` crate একটি `spawn_task` function দেয় যা `thread::spawn` API-এর সাথে দেখতে অনেকটা মিল, এবং একটি `sleep` function যা `thread::sleep` API-এর async version। আমরা এগুলো একসাথে ব্যবহার করে গণনার উদাহরণটি ইমপ্লিমেন্ট করতে পারি, যেমন Listing 17-6-তে দেখানো হয়েছে।

<Listing number="17-6" caption="Creating a new task to print one thing while the main task prints something else" file-name="src/main.rs">

```rust
use std::time::Duration;

fn main() {
    trpl::block_on(async {
        trpl::spawn_task(async {
            for i in 1..10 {
                println!("hi number {i} from the first task!");
                trpl::sleep(Duration::from_millis(500)).await;
            }
        });

        for i in 1..5 {
            println!("hi number {i} from the second task!");
            trpl::sleep(Duration::from_millis(500)).await;
        }
    });
}
```

</Listing>

শুরুর point হিসেবে আমরা `main` function-টি `trpl::block_on` দিয়ে সাজাই, যাতে আমাদের top-level function async হতে পারে।

> Note: এই অংশ থেকে chapter-এর প্রতিটি উদাহরণে `main`-এ `trpl::block_on` দিয়ে একই wrapping code থাকবে, তাই আমরা প্রায়ই `main`-এর মতোই সেটি skip করব। তোমার কোডে এটি যোগ করতে ভুলো না!

তারপর আমরা সেই block-এর ভেতরে দুটি loop লিখি, প্রতিটিতে একটি `trpl::sleep` call, যেটি পরবর্তী message পাঠানোর আগে অর্ধ সেকেন্ড (500 milliseconds) অপেক্ষা করে। একটি loop আমরা একটি `trpl::spawn_task`-এর body-তে রাখি, আর অন্যটি একটি top-level `for` loop-এ। আমরা `sleep` call-গুলোর পরে `await` যোগ করি।

এই কোড thread-ভিত্তিক ইমপ্লিমেন্টেশনের মতোই আচরণ করে—এমনকি তুমি যখন নিজে এটি চালাবে তখন তোমার terminal-এ message গুলো ভিন্ন ক্রমে দেখতে পাবে:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
```

এই version তখনই থেমে যায় যখন main async block-এর body-তে থাকা `for` loop শেষ হয়, কারণ `spawn_task` যে task spawn করে সেটি `main` function শেষ হলে shut down হয়ে যায়। তুমি যদি চাও এটি task সম্পূর্ণ না হওয়া পর্যন্ত চলুক, তাহলে তোমাকে একটি join handle ব্যবহার করে প্রথম task শেষ হওয়ার অপেক্ষা করতে হবে। Thread-এর ক্ষেত্রে, আমরা `join` method ব্যবহার করে thread কাজ শেষ না করা পর্যন্ত “block” করতাম। Listing 17-7-তে আমরা একই কাজের জন্য `await` ব্যবহার করতে পারি, কারণ task handle নিজেই একটি future। তার `Output` type একটি `Result`, তাই আমরা এটিকে await করার পরে আরও unwrap করি।

<Listing number="17-7" caption="Using `await` with a join handle to run a task to completion" file-name="src/main.rs">

```rust
        let handle = trpl::spawn_task(async {
            for i in 1..10 {
                println!("hi number {i} from the first task!");
                trpl::sleep(Duration::from_millis(500)).await;
            }
        });

        for i in 1..5 {
            println!("hi number {i} from the second task!");
            trpl::sleep(Duration::from_millis(500)).await;
        }

        handle.await.unwrap();
```

</Listing>

এই আপডেট করা version ততক্ষণ চলে যতক্ষণ না _দুটি_ loop-ই শেষ হয়:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

এপর্যন্ত মনে হচ্ছে async ও thread আমাদের একইরকম ফল দেয়, শুধু syntax আলাদা: `join` call করার বদলে `await` ব্যবহার করা, এবং `sleep` call-গুলো await করা।

বড় পার্থক্য হলো এটা করতে আমাদের আরেকটি operating system thread spawn করতে হয়নি। আসলে, এখানে আমাদের কোনো task spawn করারও দরকার নেই। যেহেতু async block গুলো anonymous future-এ compile হয়, আমরা প্রতিটি loop একটি করে async block-এ রেখে runtime-কে `trpl::join` function ব্যবহার করে দুটিকেই সম্পূর্ণ না হওয়া পর্যন্ত চালাতে পারি।

Chapter 16-এর [“Waiting for All Threads to Finish”][join-handles]<!-- ignore --> section-এ আমরা দেখিয়েছিলাম কীভাবে `std::thread::spawn` call করার সময় return হওয়া `JoinHandle` type-এর ওপর `join` method ব্যবহার করতে হয়। `trpl::join` function এর মতোই, কিন্তু future-এর জন্য। তুমি যখন একে দুটি future দাও, এটি এমন একটি নতুন single future উৎপন্ন করে যার output একটি tuple, যেটিতে তুমি দেওয়া প্রতিটি future-এর output থাকে—তবে তারা _দুজনেই_ সম্পূর্ণ হলে। তাই Listing 17-8-তে আমরা `trpl::join` ব্যবহার করি `fut1` ও `fut2` শেষ হওয়ার অপেক্ষা করতে। আমরা `fut1` ও `fut2`-কে await করি _না_, বরং `trpl::join` থেকে উৎপন্ন নতুন future-টিকে await করি। আমরা output-টি ignore করি, কারণ সেটি শুধু দুটি unit value-র একটি tuple।

<Listing number="17-8" caption="Using `trpl::join` to await two anonymous futures" file-name="src/main.rs">

```rust
        let fut1 = async {
            for i in 1..10 {
                println!("hi number {i} from the first task!");
                trpl::sleep(Duration::from_millis(500)).await;
            }
        };

        let fut2 = async {
            for i in 1..5 {
                println!("hi number {i} from the second task!");
                trpl::sleep(Duration::from_millis(500)).await;
            }
        };

        trpl::join(fut1, fut2).await;
```

</Listing>

এটি চালালে আমরা দেখব দুটি future-ই সম্পূর্ণ হয়ে শেষ হয়:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the first task!
hi number 1 from the second task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

এখন তুমি প্রতিবার হুবহু একই ক্রম দেখবে, যা thread এবং Listing 17-7-এর `trpl::spawn_task` দিয়ে যা দেখেছিলাম তার থেকে একেবারেই আলাদা। কারণ `trpl::join` function _fair_, অর্থাৎ সে প্রতিটি future-কে সমানভাবে check করে, তাদের মধ্যে পালা কাটে, এবং একজন এগিয়ে গেলে অন্যজন ready থাকলে তাকে কখনো এগিয়ে যেতে দেয় না। Thread-এর ক্ষেত্রে, অপারেটিং সিস্টেম স্থির করে কোন thread check করবে এবং কতক্ষণ চলতে দেবে। Async Rust-এ runtime স্থির করে কোন task check করবে। (বাস্তবে বিস্তারিত জটিল, কারণ একটি async runtime concurrency পরিচালনার অংশ হিসেবে পর্দার আড়ালে operating system thread ব্যবহার করতে পারে, তাই fairness guarantee করা runtime-এর জন্য বেশি কাজ—তবু সম্ভব!) Runtime-এর fairness guarantee করার কোনো বাধ্যবাধকতা নেই, এবং তারা প্রায়ই ভিন্ন API দেয় যাতে তুমি বেছে নিতে পারো তুমি fairness চাও কি না।

এই future-গুলো await করার কিছু variation চেষ্টা করে দেখো সেগুলো কী করে:

- এক বা উভয় loop-এর চারপাশ থেকে async block সরিয়ে দাও।
- প্রতিটি async block define করার পরপরই await করো।
- শুধু প্রথম loop-টিকে একটি async block-এ রাখো, এবং দ্বিতীয় loop-এর body-র পর সেই resulting future-টি await করো।

অতিরিক্ত চ্যালেঞ্জ হিসেবে, কোডটি চালানোর _আগে_ দেখো কি প্রতিটি ক্ষেত্রে output কী হবে তা বের করতে পারো কি না!

<!-- Old headings. Do not remove or links may break. -->

<a id="message-passing"></a>
<a id="counting-up-on-two-tasks-using-message-passing"></a>

### Message Passing ব্যবহার করে দুটি Task-এর মধ্যে Data পাঠানো

Future-গুলোর মধ্যে data share করাও পরিচিত মনে হবে: আমরা আবার message passing ব্যবহার করব, কিন্তু এবার type ও function-গুলোর async version দিয়ে। Chapter 16-এর [“Transfer Data Between Threads with Message Passing”][message-passing-threads]<!-- ignore --> section-এ যে পথে গিয়েছিলাম, তার থেকে একটু আলাদা পথে যাব, যাতে thread-ভিত্তিক ও future-ভিত্তিক concurrency-র মধ্যে কিছু মূল পার্থক্য দেখানো যায়। Listing 17-9-তে আমরা শুধু একটি single async block দিয়ে শুরু করব—আলাদা thread spawn করার মতো আলাদা task spawn করব _না_।

<Listing number="17-9" caption="Creating an async channel and assigning the two halves to `tx` and `rx`" file-name="src/main.rs">

```rust
        let (tx, mut rx) = trpl::channel();

        let val = String::from("hi");
        tx.send(val).unwrap();

        let received = rx.recv().await.unwrap();
        println!("received '{received}'");
```

</Listing>

এখানে আমরা `trpl::channel` ব্যবহার করি, যা Chapter 16-এ thread-দের সাথে ব্যবহৃত multiple-producer, single-consumer channel API-এর একটি async version। API-এর async version-টি thread-ভিত্তিক version-এর থেকে খুব একটা আলাদা নয়: এটি একটি immutable নয় বরং mutable receiver `rx` ব্যবহার করে, এবং তার `recv` method সরাসরি value উৎপন্ন করার বদলে এমন একটি future উৎপন্ন করে যাকে আমাদের await করতে হয়। এখন আমরা sender থেকে receiver-এ message পাঠাতে পারি। খেয়াল করো যে আমাদের আলাদা কোনো thread বা এমন কি task spawn করতেও হয় না; শুধু `rx.recv` call-টি await করলেই হয়।

`std::mpsc::channel`-এর synchronous `Receiver::recv` method কোনো message না পাওয়া পর্যন্ত block করে। `trpl::Receiver::recv` block করে না, কারণ সে async। Block করার বদলে সে runtime-এ control ফিরিয়ে দেয়, যতক্ষণ না হয় একটি message receive হয় অথবা channel-এর send side close হয়ে যায়। অন্যদিকে, আমরা `send` call-টি await করি না, কারণ সে block করে না। তার দরকারও নেই, কারণ যে channel-এ আমরা পাঠাচ্ছি সেটি unbounded।

> Note: যেহেতু এই সব async code `trpl::block_on` call-এ একটি async block-এ চলে, তাই এর ভেতরের সব কিছু block না করে এড়িয়ে যেতে পারে। তবে এর _বাইরের_ কোড `block_on` function return না করা পর্যন্ত block করবে। `trpl::block_on` function-এর মূল উদ্দেশ্যই এটেই: এটি তোমাকে _বেছে নিতে দেয়_ কোন জায়গায় কিছু async code-এর ওপর block করবে, আর সেই হিসেবে কোথায় sync ও async code-এর মধ্যে রূপান্তর হবে।

এই উদাহরণে দুটি বিষয় খেয়াল করো। প্রথম, message সাথে সাথেই এসে পৌঁছাবে। দ্বিতীয়, যদিও আমরা এখানে future ব্যবহার করছি, এখনও পর্যন্ত কোনো concurrency নেই। Listing-এর সবকিছু sequence-এ ঘটে, ঠিক যেমনটা হতো যদি কোনো future জড়িত না থাকত।

চলো প্রথম অংশটা সামলাই—কিছু message একটি সিরিজে পাঠিয়ে মাঝে মাঝে sleep করে, যেমন Listing 17-10-তে দেখানো হয়েছে।

<!-- We cannot test this one because it never stops! -->

<Listing number="17-10" caption="Sending and receiving multiple messages over the async channel and sleeping with an `await` between each message" file-name="src/main.rs">

```rust,ignore
extern crate trpl; // required for mdbook test

use std::time::Duration;

fn main() {
    trpl::block_on(async {
        // ANCHOR: many-messages
        let (tx, mut rx) = trpl::channel();

        let vals = vec![
            String::from("hi"),
            String::from("from"),
            String::from("the"),
            String::from("future"),
        ];

        for val in vals {
            tx.send(val).unwrap();
            trpl::sleep(Duration::from_millis(500)).await;
        }

        while let Some(value) = rx.recv().await {
            println!("received '{value}'");
        }
        // ANCHOR_END: many-messages
    });
}
```

</Listing>

Message পাঠানোর পাশাপাশি সেগুলো receive করতেও হবে। এই ক্ষেত্রে, যেহেতু আমরা জানি কয়টি message আসছে, তাই আমরা হাতে `rx.recv().await` চারবার call করে সেটা করতে পারতাম। কিন্তু বাস্তবে, আমরা সাধারণত কিছু _অজানা_ সংখ্যক message-এর অপেক্ষা করব, তাই আমাদের ততক্ষণ অপেক্ষা করতে হবে যতক্ষণ না আমরা নিশ্চিত হই আর কোনো message নেই।

Listing 16-10-তে আমরা একটি synchronous channel থেকে receive হওয়া সব item প্রসেস করতে একটি `for` loop ব্যবহার করেছিলাম। কিন্তু Rust-এ এখনও _asynchronously উৎপন্ন_ item-এর সিরিজের সাথে `for` loop ব্যবহারের কোনো উপায় নেই, তাই আমাদের এমন একটি loop ব্যবহার করতে হবে যা আমরা আগে দেখিনি: `while let` conditional loop। এটি Chapter 6-এর [“Concise Control Flow with `if let` and `let...else`”][if-let]<!-- ignore --> section-এ দেখা `if let` construct-এর loop version। Loop-টি ততক্ষণ execute হতে থাকবে যতক্ষণ এটি যে pattern specify করে তা value-র সাথে match করতে থাকে।

`rx.recv` call একটি future উৎপন্ন করে, যাকে আমরা await করি। Runtime সেই future-টিকে ready না হওয়া পর্যন্ত pause রাখবে। একবার কোনো message এলে, future ততবার `Some(message)`-এ resolve হবে যতবার message আসে। Channel close হয়ে গেলে, _কোনো_ message এসেছে কি না তা স্বতন্ত্র, future-টি `None`-এ resolve হবে যাতে বোঝানো যায় আর কোনো value নেই, তাই আমাদের polling বন্ধ করা উচিত—অর্থাৎ, await করা বন্ধ করা।

`while let` loop এই সবকিছুকে একত্র করে। যদি `rx.recv().await`-এর ফল `Some(message)` হয়, আমরা message-টিতে অ্যাক্সেস পাই এবং loop body-তে সেটি ব্যবহার করতে পারি, ঠিক যেমন `if let`-এ করতে পারতাম। আর ফল যদি `None` হয়, loop শেষ হয়। প্রতিবার loop সম্পূর্ণ হলে সে আবার await point-এ পৌঁছায়, তাই runtime পরবর্তী message না আসা পর্যন্ত তাকে আবার pause করে রাখে।

কোডটি এখন সফলভাবে সব message send ও receive করে। দুর্ভাগ্যক্রমে, এখনও কয়েকটি সমস্যা আছে। প্রথমত, message গুলো অর্ধ-সেকেন্ড পরপর আসে না। সেগুলো সব একসাথে আসে, প্রোগ্রাম শুরুর 2 সেকেন্ড (2,000 milliseconds) পর। দ্বিতীয়ত, এই প্রোগ্রাম আর কখনো exit-ও করে না! বরং সে চিরকাল নতুন message-এর জন্য অপেক্ষা করে। তোমাকে <kbd>ctrl</kbd>-<kbd>C</kbd> চেপে এটি shut down করতে হবে।

#### এক Async Block-এর ভেতরের কোড Linearly Execute হয়

চলো প্রথমে দেখি কেন message গুলো প্রতিটির মাঝে বিলম্ব না করে সব একসাথে, পুরো delay-এর পর আসে। কোনো নির্দিষ্ট async block-ের ভেতরে, কোডে `await` keyword গুলো যে ক্রমে আছে, সেটিই হলো প্রোগ্রাম চলার সময় সেগুলো execute হওয়ার ক্রম।

Listing 17-10-তে শুধু একটি async block আছে, তাই এর সবকিছু linearly চলে। এখনও কোনো concurrency নেই। সব `tx.send` call ঘটে, তার মাঝে মাঝে সব `trpl::sleep` call ও তাদের সংশ্লিষ্ট await point। তারপরই `while let` loop-টি `recv` call-গুলোর await point-গুলোতে যেতে পারে।

যে আচরণ আমরা চাই—প্রতিটি message-এর মাঝে sleep delay হবে—তা পেতে আমাদের `tx` ও `rx` operation-গুলোকে তাদের নিজস্ব async block-এ রাখতে হবে, যেমন Listing 17-11-তে। তখন runtime `trpl::join` ব্যবহার করে প্রতিটিকে আলাদাভাবে execute করতে পারবে, ঠিক Listing 17-8-এর মতো। আবারও, আমরা আলাদা future-গুলো নয়, বরং `trpl::join` call-এর result await করি। যদি আমরা আলাদা future-গুলো sequence-এ await করতাম, তাহলে আবার একটি sequential flow-এ ফিরে যেতাম—যা এড়াতেই আমরা চাইছি।

<!-- We cannot test this one because it never stops! -->

<Listing number="17-11" caption="Separating `send` and `recv` into their own `async` blocks and awaiting the futures for those blocks" file-name="src/main.rs">

```rust,ignore
        let tx_fut = async {
            let vals = vec![
                String::from("hi"),
                String::from("from"),
                String::from("the"),
                String::from("future"),
            ];

            for val in vals {
                tx.send(val).unwrap();
                trpl::sleep(Duration::from_millis(500)).await;
            }
        };

        let rx_fut = async {
            while let Some(value) = rx.recv().await {
                println!("received '{value}'");
            }
        };

        trpl::join(tx_fut, rx_fut).await;
```

</Listing>

Listing 17-11-এর আপডেট করা কোড দিয়ে, message গুলো 500-millisecond পরপর print হয়, 2 সেকেন্ড পর একসাথে নয়।

#### একটি Async Block-এ Ownership Move করা

তবে প্রোগ্রাম এখনও কখনো exit করে না, কারণ `while let` loop `trpl::join`-এর সাথে যেভাবে মিথস্ক্রিয়া করে তার কারণে:

- `trpl::join` থেকে return হওয়া future ততক্ষণেই সম্পূর্ণ হয় যখন দেওয়া _দুটি_ future-ই সম্পূর্ণ হয়।
- `tx_fut` future সম্পূর্ণ হয় `vals`-এর শেষ message পাঠানোর পর sleep শেষ হলে।
- `rx_fut` future `while let` loop শেষ না হওয়া পর্যন্ত সম্পূর্ণ হবে না।
- `while let` loop `rx.recv` await করে `None` না পাওয়া পর্যন্ত শেষ হবে না।
- `rx.recv` await করলে ততক্ষণই `None` return করবে যখন channel-এর অন্য প্রান্ত close হবে।
- Channel ততক্ষণই close হবে যখন আমরা `rx.close` call করব বা sender side, `tx`, drop হবে।
- আমরা কোথাও `rx.close` call করি না, এবং `tx` ততক্ষণ drop হবে না যতক্ষণ না `trpl::block_on`-এ দেওয়া outermost async block শেষ হবে।
- সেই block শেষ হতে পারে না কারণ সে `trpl::join` সম্পূর্ণ হওয়ার জন্য block হয়ে আছে, যা আমাদের এই list-এর শীর্ষে ফিরিয়ে নিয়ে যায়।

এখন, যে async block-এ আমরা message পাঠাই সে শুধু `tx`-কে _borrow_ করে, কারণ একটি message পাঠানোর জন্য ownership দরকার হয় না, কিন্তু যদি আমরা `tx`-কে সেই async block-এ _move_ করতে পারতাম, তবে সেই block শেষ হলে সেটি drop হয়ে যেত। Chapter 13-এর [“Capturing References or Moving Ownership”][capture-or-move]<!-- ignore --> section-এ তুমি শিখেছিলে কীভাবে closure-এর সাথে `move` keyword ব্যবহার করতে হয়, এবং Chapter 16-এর [“Using `move` Closures with Threads”][move-threads]<!-- ignore --> section-এ আলোচনা অনুযায়ী, thread-এর সাথে কাজ করার সময় প্রায়ই closure-এ data move করতে হয়। একই মৌলিক গতিশীলতা async block-এর ক্ষেত্রেও প্রযোজ্য, তাই `move` keyword async block-এর সাথেও ঠিক closure-এর মতো কাজ করে।

Listing 17-12-তে আমরা message পাঠানোর জন্য যে ব্যবহার করি সেই block-কে `async` থেকে `async move`-এ পরিবর্তন করি।

<Listing number="17-12" caption="A revision of the code from Listing 17-11 that correctly shuts down when complete" file-name="src/main.rs">

```rust
extern crate trpl; // required for mdbook test

use std::time::Duration;

fn main() {
    trpl::block_on(async {
        // ANCHOR: with-move
        let (tx, mut rx) = trpl::channel();

        let tx_fut = async move {
            // --snip--
            // ANCHOR_END: with-move
            let vals = vec![
                String::from("hi"),
                String::from("from"),
                String::from("the"),
                String::from("future"),
            ];

            for val in vals {
                tx.send(val).unwrap();
                trpl::sleep(Duration::from_millis(500)).await;
            }
        };

        let rx_fut = async {
            while let Some(value) = rx.recv().await {
                println!("received '{value}'");
            }
        };

        trpl::join(tx_fut, rx_fut).await;
    });
}
```

</Listing>

কোডের _এই_ version-টি চালালে, এটি শেষ message পাঠানো ও receive হওয়ার পর gracefully shut down হয়। এর পরে, চলো দেখি একাধিক future থেকে data পাঠাতে হলে কী পরিবর্তন করতে হবে।

#### `join!` Macro দিয়ে একাধিক Future একত্র করা

এই async channel-টিও একটি multiple-producer channel, তাই আমরা একাধিক future থেকে message পাঠাতে চাইলে `tx`-এর ওপর `clone` call করতে পারি, যেমন Listing 17-13-তে।

<Listing number="17-13" caption="Using multiple producers with async blocks" file-name="src/main.rs">

```rust
        let (tx, mut rx) = trpl::channel();

        let tx1 = tx.clone();
        let tx1_fut = async move {
            let vals = vec![
                String::from("hi"),
                String::from("from"),
                String::from("the"),
                String::from("future"),
            ];

            for val in vals {
                tx1.send(val).unwrap();
                trpl::sleep(Duration::from_millis(500)).await;
            }
        };

        let rx_fut = async {
            while let Some(value) = rx.recv().await {
                println!("received '{value}'");
            }
        };

        let tx_fut = async move {
            let vals = vec![
                String::from("more"),
                String::from("messages"),
                String::from("for"),
                String::from("you"),
            ];

            for val in vals {
                tx.send(val).unwrap();
                trpl::sleep(Duration::from_millis(1500)).await;
            }
        };

        trpl::join!(tx1_fut, tx_fut, rx_fut);
```

</Listing>

প্রথমে আমরা `tx` clone করে প্রথম async block-এর বাইরে `tx1` তৈরি করি। আমরা `tx`-এর যেমন করেছিলাম, সেই একইভাবে `tx1`-কে সেই block-এ move করি। তারপর, পরে, আমরা মূল `tx`-কে একটি _নতুন_ async block-এ move করি, যেখানে আমরা একটু ধীর delay-এ আরও message পাঠাই। এই নতুন async block-টি message receive করার async block-এর পরে রাখা হয়েছে, কিন্তু সেটি আগেও থাকতে পারত। মূল বিষয় হল future-গুলো await করার ক্রম, তাদের তৈরি হওয়ার ক্রম নয়।

Message পাঠানোর দুটি async block-ই `async move` block হতে হবে যাতে `tx` ও `tx1` উভয়ই সেই block-গুলো শেষ হলে drop হয়। অন্যথায়, আমরা যে অসীম loop দিয়ে শুরু করেছিলাম সেখানেই ফিরে যাব।

শেষে, অতিরিক্ত future-টি সামলাতে আমরা `trpl::join` থেকে `trpl::join!`-এ চলে যাই: `join!` macro compile সময়ে যতগুলো future আমরা জানি ততগুলো future await করে। অজানা সংখ্যক future-এর একটি collection await করা নিয়ে chapter-এ আরও পরে আলোচনা করব।

এখন আমরা দুটি sending future থেকেই সব message দেখি, এবং যেহেতু sending future-গুলো পাঠানোর পর সামান্য ভিন্ন delay ব্যবহার করে, message-গুলো সেই ভিন্ন ব্যবধানে receive হয়:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
received 'hi'
received 'more'
received 'from'
received 'the'
received 'messages'
received 'future'
received 'for'
received 'you'
```

আমরা message passing দিয়ে future-গুলোর মধ্যে কীভাবে data পাঠাতে হয়, এক async block-এর ভেতরের কোড কীভাবে sequentially চলে, কীভাবে এক async block-এ ownership move করতে হয়, এবং কীভাবে একাধিক future একত্র করতে হয়—এসব বিষয় অনুসন্ধান করেছি। এর পরে, চলো আলোচনা করি কীভাবে ও কেন runtime-কে জানাতে হয় যে সে অন্য কোনো task-এ switch করতে পারে।

[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[join-handles]: ch16-01-threads.html#waiting-for-all-threads-to-finish
[message-passing-threads]: ch16-02-message-passing.html
[if-let]: ch06-03-if-let.html
[capture-or-move]: ch13-01-closures.html#capturing-references-or-moving-ownership
[move-threads]: ch16-01-threads.html#using-move-closures-with-threads

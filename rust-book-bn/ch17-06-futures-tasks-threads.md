## সব একত্রে: Futures, Tasks, এবং Threads

[Chapter 16][ch16]<!-- ignore -->-তে যেমন দেখেছি, thread concurrency-র একটি পদ্ধতি দেয়। এই chapter-এ আমরা আরেকটি পদ্ধতি দেখেছি: future এবং stream সহ async ব্যবহার। তুমি যদি ভাবো কখন কোন পদ্ধতি বেছে নেবে, তবে উত্তর হলো: পরিস্থিতির ওপর নির্ভর করে! এবং অনেক ক্ষেত্রে, পছন্দটি thread _বা_ async নয়, বরং thread _এবং_ async।

অনেক operating system কয় দশক ধরে threading-ভিত্তিক concurrency model দিয়ে আসছে, এবং ফলে অনেক programming language সেগুলো সাপোর্ট করে। তবে এই model-গুলো tradeoff ছাড়া নয়। অনেক operating system-এ, প্রতিটি thread-এর জন্য যথেষ্ট memory ব্যবহার হয়। তাছাড়া, তোমার operating system ও hardware সাপোর্ট করলেই কেবল thread option হিসেবে থাকে। Mainstream desktop ও mobile কম্পিউটারের থেকে ভিন্ন, কিছু embedded system-এ আদৌ কোনো OS নেই, তাই সেখানে thread-ও নেই।

Async model ভিন্ন—এবং সর্বশেষে পরিপূরক—একটি tradeoff set দেয়। Async model-এ, concurrent operation-গুলোর নিজস্ব thread-এর প্রয়োজন নেই। বরং, সেগুলো task-এ চলতে পারে, যেমন streams section-এ আমরা একটি synchronous function থেকে কাজ শুরু করতে `trpl::spawn_task` ব্যবহার করেছি। একটি task একটি thread-এর মতো, কিন্তু operating system দ্বারা পরিচালিত হওয়ার বদলে এটি library-level code দ্বারা পরিচালিত: runtime।

Thread এবং task spawn করার API গুলো এতটা মিল কেন হবে তার কারণ আছে। Thread গুলো synchronous operation-গুলোর একটি set-এর জন্য একটি boundary হিসেবে কাজ করে; concurrency thread-গুলোর _মধ্যে_ সম্ভব। Task গুলো _asynchronous_ operation-গুলোর একটি set-ের জন্য boundary হিসেবে কাজ করে; concurrency task-গুলোর _মধ্যে_ এবং _ভেতরে_ উভয় সম্ভব, কারণ একটি task তার body-তে future-গুলোর মধ্যে switch করতে পারে। সবশেষে, future গুলো Rust-এর সবচেয়ে সূক্ষ্ম concurrency unit, এবং প্রতিটি future অন্যান্য future-গুলোর একটি tree উপস্থাপন করতে পারে। Runtime—বিশেষ করে তার executor—task পরিচালনা করে, এবং task গুলো future পরিচালনা করে। সেই হিসেবে, task গুলো runtime-পরিচালিত lightweight thread-এর মতো, অতিরিক্ত ক্ষমতা সহ যা আসে operating system-এর বদলে runtime দ্বারা পরিচালিত হওয়ার কারণে।

এর মানে এটা নয় যে async task সবসময় thread-এর চেয়ে ভালো (বা উল্টো)। Thread দিয়ে concurrency কোনো ক্ষেত্রে `async` দিয়ে concurrency-র চেয়ে একটি সহজ programming model। সেটি একটি শক্তিও হতে পারে আবার দুর্বলতাও। Thread কিছুটা “fire and forget”; তাদের future-এর কোনো native equivalent নেই, তাই সেগুলো operating system ছাড়া অন্য কারো দ্বারা interrupt না হয়ে সম্পূর্ণ না হওয়া পর্যন্ত চলে।

আর দেখা যায় যে thread এবং task প্রায়ই খুব ভালোভাবে একসাথে কাজ করে, কারণ task গুলোকে (অন্তত কিছু runtime-এ) thread-গুলোর মধ্যে move করা যায়। বাস্তবে, পর্দার আড়ালে আমরা যে runtime ব্যবহার করছি—যার মধ্যে `spawn_blocking` ও `spawn_task` function আছে—সে ডিফল্টভাবে multithreaded! অনেক runtime thread-গুলো বর্তমানে কীভাবে ব্যবহৃত হচ্ছে তার ভিত্তিতে সিস্টেমের সামগ্রিক performance উন্নত করতে thread-গুলোর মধ্যে task transparently move করতে _work stealing_ নামের একটি পদ্ধতি ব্যবহার করে। সেই পদ্ধতিতে আসলে thread _এবং_ task, ফলে future-ও প্রয়োজন।

কখন কোন পদ্ধতি ব্যবহার করবে তা ভাবার সময়, এই নিয়মগুলো মাথায় রাখো:

- যদি কাজটি _খুব parallelizable_ (অর্থাৎ, CPU-bound) হয়, যেমন একগাদা data প্রসেস করা যেখানে প্রতিটি অংশ আলাদাভাবে প্রসেস করা যায়, thread একটি ভালো পছন্দ।
- যদি কাজটি _খুব concurrent_ (অর্থাৎ, I/O-bound) হয়, যেমন বিভিন্ন উৎস থেকে আসা একগাদা message handle করা যা ভিন্ন ব্যবধানে বা ভিন্ন হারে আসতে পারে, async একটি ভালো পছন্দ।

আর তোমার যদি parallelism এবং concurrency উভয়ই দরকার হয়, তবে তোমাকে thread আর async-এর মধ্যে বেছে নিতে হবে না। তুমি সেগুলো স্বাধীনভাবে একসাথে ব্যবহার করতে পারো, প্রত্যেককে যেটাতে সে সবচেয়ে ভালো তা করতে দিয়ে। যেমন, Listing 17-25 বাস্তব Rust কোডে এই ধরনের mix-এর একটি বেশ সাধারণ উদাহরণ দেখায়।

<Listing number="17-25" caption="Sending messages with blocking code in a thread and awaiting the messages in an async block" file-name="src/main.rs">

```rust
use std::{thread, time::Duration};

fn main() {
    let (tx, mut rx) = trpl::channel();

    thread::spawn(move || {
        for i in 1..11 {
            tx.send(i).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });

    trpl::block_on(async {
        while let Some(message) = rx.recv().await {
            println!("{message}");
        }
    });
}
```

</Listing>

আমরা শুরু করি একটি async channel তৈরি করে, তারপর `move` keyword ব্যবহার করে channel-এর sender side-এর ownership নিয়ে একটি thread spawn করি। সেই thread-এর ভেতরে আমরা 1 থেকে 10 পর্যন্ত সংখ্যা পাঠাই, প্রতিটির মাঝে এক সেকেন্ড sleep করি। শেষে, আমরা chapter জুড়ে যেমন করেছি তেমনভাবে `trpl::block_on`-কে দেওয়া একটি async block দিয়ে তৈরি একটি future চালাই। সেই future-এ, আমরা সেই message-গুলো await করি, ঠিক যেমন আমরা অন্যান্য message-passing উদাহরণে দেখেছি।

এই chapter যে পরিস্থিতি দিয়ে শুরু করেছিলাম সেখানে ফিরে যাই, কল্পনা করো একটি dedicated thread দিয়ে কিছু video encoding task চালাচ্ছ (কারণ video encoding compute-bound), কিন্তু UI-কে একটি async channel দিয়ে জানাচ্ছ যে সেই operation-গুলো শেষ হয়েছে। বাস্তব use case-এ এ ধরনের সমন্বয়ের অসংখ্য উদাহরণ আছে।

## Summary

এই book-এ তুমি আর concurrency দেখবে, এটাই শেষ নয়। [Chapter 21][ch21]<!-- ignore -->-এর project এই concept গুলোকে এখানে আলোচনা করা সরল উদাহরণের চেয়ে অধিকতর বাস্তব পরিস্থিতিতে প্রয়োগ করবে এবং threading বনাম task ও future দিয়ে সমস্যা সমাধানের আরও সরাসরি তুলনা করবে।

তুমি যে পদ্ধতিই বেছে নাও না কেন, Rust তোমাকে নিরাপদ, দ্রুত, concurrent code লেখার জন্য প্রয়োজনীয় tool দেয়—তা সে high-throughput web সার্ভার হোক বা embedded operating system হোক।

এরপরে, আমরা কথা বলব Rust প্রোগ্রাম বড় হওয়ার সাথে সাথে সমস্যা model করার এবং সমাধান গঠনের idiomatic উপায় নিয়ে। সাথে, আমরা আলোচনা করব Rust-এর idiom গুলো কীভাবে object-oriented programming থেকে তোমার পরিচিত idiom-গুলোর সাথে সম্পর্কিত।

[ch16]: ch16-00-concurrency.html
[combining-futures]: ch17-03-more-futures.html#building-our-own-async-abstractions
[streams]: ch17-04-streams.html#composing-streams
[ch21]: ch21-00-final-project-a-web-server.html

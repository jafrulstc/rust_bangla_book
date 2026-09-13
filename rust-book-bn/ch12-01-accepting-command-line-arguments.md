## Command Line Argument গ্রহণ করা

সবার আগে সবার মতো `cargo new` দিয়ে একটি নতুন project তৈরি করি। আমাদের project-এর নাম দেব `minigrep`, যাতে সেটি তোমার সিস্টেমে হয়তো আগে থেকেই থাকা `grep` tool থেকে আলাদা করা যায়:

```console
$ cargo new minigrep
     Created binary (application) `minigrep` project
$ cd minigrep
```

প্রথম কাজ হলো `minigrep`-কে দুটি command line argument গ্রহণ করানো: file path এবং যে string খোঁজা হবে। অর্থাৎ, আমরা চাই আমাদের program-টি `cargo run` দিয়ে চালানো যাক, দুটি hyphen দিয়ে যা নির্দেশ করবে যে নিচের argument গুলো `cargo`-এর জন্য নয় বরং আমাদের program-এর জন্য, একটি string যেটা খোঁজা হবে, এবং একটি এমন file-এর path যেখানে খোঁজা হবে—এভাবে:

```console
$ cargo run -- searchstring example-filename.txt
```

এই মুহূর্তে, `cargo new` যে program তৈরি করেছে সেটি আমরা যে argument গুলো দেব সেগুলো process করতে পারে না। [crates.io](https://crates.io/)-এ এমন কিছু existing library আছে যা command line argument গ্রহণ করে এমন একটি program লেখায় সাহায্য করতে পারে, কিন্তু যেহেতু তুমি এইমাত্র এই concept শিখছ, চলো এই capability আমরা নিজেরাই implement করি।

### Argument Value গুলো পড়া

`minigrep`-কে আমরা যে command line argument গুলো পাঠাই সেগুলোর value পড়তে সক্ষম করতে, আমাদের Rust-এর standard library-তে থাকা `std::env::args` function-টি লাগবে। এই function-টি `minigrep`-কে পাঠানো command line argument গুলোর একটি iterator return করে। Iterator সম্পর্কে আমরা [Chapter 13][ch13]<!-- ignore
-->-এ বিস্তারিত আলোচনা করব। আপাতত, iterator সম্পর্কে তোমার শুধু দুটি বিষয় জানা দরকার: iterator একটি সিরিজ value তৈরি করে, এবং আমরা একটি iterator-এর উপর `collect` method call করে সেটিকে এমন একটি collection-এ রূপান্তর করতে পারি—যেমন একটি vector—যেটি iterator যতগুলো element তৈরি করে সবগুলো ধারণ করে।

Listing 12-1-এর code তোমার `minigrep` program-টিকে তাকে পাঠানো যেকোনো command line argument পড়তে দেয় এবং তারপর সেই value গুলোকে একটি vector-এ সংগ্রহ করে।

<Listing number="12-1" file-name="src/main.rs" caption="Command line argument গুলোকে একটি vector-এ সংগ্রহ করা এবং সেগুলো print করা">

```rust
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    dbg!(args);
}
```

</Listing>

প্রথমে আমরা একটি `use` statement দিয়ে `std::env` module-টিকে scope-এ আনি, যাতে আমরা এর `args` function ব্যবহার করতে পারি। খেয়াল করো যে `std::env::args` function-টি দুই স্তরের module-এর ভেতরে nested। [Chapter 7][ch7-idiomatic-use]<!-- ignore -->-এ যেমন আলোচনা করেছি, যেসব ক্ষেত্রে কাঙ্ক্ষিত function একাধিক module-এ nested থাকে, সেসব ক্ষেত্রে আমরা function-টির বদলে তার parent module-টিকে scope-এ আনা বেছেছি। এতে করে `std::env`-এর অন্যান্য function সহজেই ব্যবহার করতে পারব। এটি `use std::env::args` লেখার চেয়েও কম ambiguous, কারণ `args` লিখলে সেটিকে সহজেই এমন একটি function বলে ভ্রম হতে পারে যেটি current module-এ define করা।

> ### `args` Function এবং Invalid Unicode
>
> মনে রাখো, কোনো argument যদি invalid Unicode ধারণ করে তবে `std::env::args` panic করবে। তোমার program-কে যদি invalid Unicode ধারণকারী argument গ্রহণ করতে হয়, তবে `std::env::args_os` ব্যবহার করো। সেই function-টি এমন একটি iterator return করে যা `String` value-এর বদলে `OsString` value তৈরি করে। সরলতার জন্য আমরা এখানে `std::env::args` ব্যবহার করেছি, কারণ `OsString` value প্ল্যাটফর্মভেদে ভিন্ন এবং `String` value-এর চেয়ে কাজ করা বেশি জটিল।

`main`-এর প্রথম line-এ আমরা `env::args` call করি, এবং সাথে সাথে `collect` ব্যবহার করে iterator-টিকে একটি vector-এ রূপান্তর করি যেটি iterator যত value তৈরি করে সবগুলো ধারণ করে। আমরা `collect` function ব্যবহার করে অনেক ধরনের collection তৈরি করতে পারি, তাই আমরা `args`-এর type স্পষ্টভাবে annotate করে নির্দেশ করি যে আমরা string-এর একটি vector চাই। যদিও Rust-এ খুব কমই type annotate করতে হয়, `collect` এমন একটি function যেটি প্রায়ই annotate করতে হয়, কারণ Rust বুঝতে পারে না তুমি কোন ধরনের collection চাইছ।

সবশেষে, আমরা debug macro ব্যবহার করে vector-টি print করি। চলো প্রথমে কোনো argument ছাড়া এবং তারপর দুটি argument দিয়ে code-টি চালানোর চেষ্টা করি:

```console
$ cargo run
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.61s
     Running `target/debug/minigrep`
[src/main.rs:5:5] args = [
    "target/debug/minigrep",
]
```

```console
$ cargo run -- needle haystack
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 1.57s
     Running `target/debug/minigrep needle haystack`
[src/main.rs:5:5] args = [
    "target/debug/minigrep",
    "needle",
    "haystack",
]
```

খেয়াল করো যে vector-এর প্রথম value টি `"target/debug/minigrep"`, যেটি আমাদের binary-র নাম। এটি C-তে argument list-এর আচরণের সাথে মিলে যায়, যেখানে program-গুলো যে নাম দিয়ে সেগুলোকে invoke করা হয়েছে সেটি তাদের execution-এ ব্যবহার করতে পারে। Program-এর নামে access পাওয়া প্রায়ই সুবিধাজনক, যদি তুমি message-এ সেটি print করতে চাও বা program-টি যে command line alias দিয়ে invoke করা হয়েছে তার ওপর ভিত্তি করে আচরণ পরিবর্তন করতে চাও। কিন্তু এই chapter-এর উদ্দেশ্যে, আমরা সেটি উপেক্ষা করব এবং শুধু আমাদের দরকারি দুটি argument save করব।

### Argument Value গুলো Variable-এ সংরক্ষণ

এই মুহূর্তে program-টি command line argument হিসেবে উল্লেখ করা value গুলোতে access করতে সক্ষম। এখন আমাদের দুটি argument-এর value variable-এ সংরক্ষণ করতে হবে, যাতে আমরা সেগুলো program-এর বাকি অংশে ব্যবহার করতে পারি। সেটি আমরা Listing 12-2-তে করছি।

<Listing number="12-2" file-name="src/main.rs" caption="Query argument এবং file path argument ধারণ করার জন্য variable তৈরি">

```rust,should_panic,noplayground
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();

    let query = &args[1];
    let file_path = &args[2];

    println!("Searching for {query}");
    println!("In file {file_path}");
}
```

</Listing>

Vector print করার সময় যেমন দেখেছি, program-এর নাম `args[0]`-এ ভেক্টরের প্রথম value হিসেবে থাকে, তাই আমরা argument শুরু করছি index 1 থেকে। `minigrep`-এর নেওয়া প্রথম argument-টি হলো সেই string যেটি আমরা খুঁজছি, তাই আমরা প্রথম argument-এর একটি reference `query` variable-এ রাখি। দ্বিতীয় argument-টি হবে file path, তাই আমরা দ্বিতীয় argument-এর একটি reference `file_path` variable-ে রাখি।

আমরা সাময়িকভাবে এই variable-গুলোর value print করছি, যাতে প্রমাণ হয় code-টি আমাদের ইচ্ছামতো কাজ করছে। চলো `test` এবং `sample.txt` argument দিয়ে এই program-টি আবার চালাই:

```console
$ cargo run -- test sample.txt
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.0s
     Running `target/debug/minigrep test sample.txt`
Searching for test
In file sample.txt
```

দারুণ, program-টি কাজ করছে! আমাদের দরকারি argument-গুলোর value সঠিক variable-এ সংরক্ষিত হচ্ছে। পরে আমরা কিছু error handling যোগ করব, যাতে কিছু সম্ভাব্য ভুল পরিস্থিতি—যেমন user কোনো argument না দিলে—সামাল দেওয়া যায়; আপাতত, আমরা সেই পরিস্থিতি উপেক্ষা করে file-পড়ার capability যোগ করার দিকে মন দেব।

[ch13]: ch13-00-functional-features.html
[ch7-idiomatic-use]: ch07-04-bringing-paths-into-scope-with-the-use-keyword.html#creating-idiomatic-use-paths

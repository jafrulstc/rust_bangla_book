<!-- Old headings. Do not remove or links may break. -->

<a id="streams"></a>

## Streams: Sequence-এ Future

এই chapter-এর আগে [“Message Passing”][17-02-messages]<!-- ignore --> section-এ আমরা যেভাবে আমাদের async channel-এর receiver ব্যবহার করেছি, সেটা মনে করো। Async `recv` method সময়ের সাথে সাথে item-গুলোর একটি sequence উৎপন্ন করে। এটি একটি আরও general pattern-এর instance, যাকে _stream_ বলা হয়। অনেক ধারণা স্বাভাবিকভাবেই stream হিসেবে উপস্থাপন করা যায়: একটি queue-তে item available হওয়া, যখন সম্পূর্ণ data set কম্পিউটারের memory-র জন্য অনেক বড় হয় তখন filesystem থেকে ধাপে ধাপে data chunk টানা, অথবা সময়ের সাথে নেটওয়ার্ক জুড়ে data এসে পৌঁছানো। যেহেতু stream গুলো future, তাই আমরা সেগুলোকে অন্য যেকোনো ধরনের future-এর সাথে ব্যবহার করতে পারি এবং আকর্ষণীয়ভাবে যুক্ত করতে পারি। যেমন, আমরা event-গুলোকে batch করে অতিরিক্ত নেটওয়ার্ক call এড়াতে পারি, দীর্ঘস্থায়ী operation-গুলোর sequence-এ timeout সেট করতে পারি, অথবা অপ্রয়োজনীয় কাজ এড়াতে user interface event-কে throttle করতে পারি।

আমরা Chapter 13-এর [“The Iterator Trait and the `next` Method”][iterator-trait]<!-- ignore --> section-এ Iterator trait দেখার সময় item-গুলোর একটি sequence দেখেছিলাম, কিন্তু iterator ও async channel receiver-এর মধ্যে দুটি পার্থক্য আছে। প্রথম পার্থক্য হলো সময়: iterator গুলো synchronous, অন্যদিকে channel receiver asynchronous। দ্বিতীয় পার্থক্য হলো API। `Iterator`-এর সাথে সরাসরি কাজ করার সময় আমরা তার synchronous `next` method call করি। কিন্তু `trpl::Receiver` stream-এর ক্ষেত্রে আমরা বরং একটি asynchronous `recv` method call করি। এছাড়া, এই API গুলো খুব একইরকম মনে হয়, আর এই মিলটা কোনো কাকতালীয় ব্যাপার নয়। Stream হলো iteration-এর একটি asynchronous রূপ। তবে যেখানে `trpl::Receiver` নির্দিষ্টভাবে message receive করার অপেক্ষা করে, সেখানে general-purpose stream API অনেক বেশি বিস্তৃত: এটি `Iterator`-এর মতো পরবর্তী item দেয়, কিন্তু asynchronously।

Rust-এ iterator ও stream-এর মধ্যে মিল থাকার কারণে আমরা যেকোনো iterator থেকে একটি stream তৈরি করতে পারি। Iterator-এর মতো, আমরা একটি stream-এর সাথে তার `next` method call করে এবং তারপর output await করে কাজ করতে পারি, যেমন Listing 17-21-তে দেখানো হয়েছে, যেটি এখনও compile হয় না।

<Listing number="17-21" caption="Creating a stream from an iterator and printing its values" file-name="src/main.rs">

```rust,ignore,does_not_compile
        let values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        let iter = values.iter().map(|n| n * 2);
        let mut stream = trpl::stream_from_iter(iter);

        while let Some(value) = stream.next().await {
            println!("The value was: {value}");
        }
```

</Listing>

আমরা একটি সংখ্যার array দিয়ে শুরু করি, যাকে আমরা iterator-এ রূপান্তর করি এবং তারপর সব value দ্বিগুণ করতে `map` call করি। তারপর `trpl::stream_from_iter` function ব্যবহার করে iterator-টিকে stream-এ রূপান্তর করি। এর পর, আমরা যখন item গুলো stream-এ আসবে তখন `while let` loop দিয়ে সেগুলোর ওপর লুপ করি।

দুর্ভাগ্যক্রমে, কোডটি চালানোর চেষ্টা করলে সেটি compile হয় না, বরং জানায় যে কোনো `next` method নেই:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-21
cargo build
copy only the error output
-->

```text
error[E0599]: no method named `next` found for struct `tokio_stream::iter::Iter` in the current scope
  --> src/main.rs:10:40
   |
10 |         while let Some(value) = stream.next().await {
   |                                        ^^^^
   |
   = help: items from traits can only be used if the trait is in scope
help: the following traits which provide `next` are implemented but not in scope; perhaps you want to import one of them
   |
1  + use crate::trpl::StreamExt;
   |
1  + use futures_util::stream::stream::StreamExt;
   |
1  + use std::iter::Iterator;
   |
1  + use std::str::pattern::Searcher;
   |
help: there is a method `try_next` with a similar name
   |
10 |         while let Some(value) = stream.try_next().await {
   |                                        ~~~~~~~~
```

এই output যেমন ব্যাখ্যা করে, compiler error-এর কারণ হলো `next` method ব্যবহার করতে হলে আমাদের সঠিক trait scope-এ আনতে হবে। এতকণ আমাদের আলোচনা দেখে তুমি যুক্তিসঙ্গতভাবে আশা করতে পারো সেই trait-টি `Stream` হবে, কিন্তু আসলে সেটি `StreamExt`। _extension_-এর সংক্ষিপ্ত রূপ `Ext`, Rust community-তে একটি trait-কে অন্য দিয়ে extend করার একটি প্রচলিত pattern।

`Stream` trait এমন একটি low-level interface define করে যা effectively `Iterator` ও `Future` trait-কে একত্র করে। `StreamExt`, `Stream`-এর ওপর তৈরি higher-level API-এর একটি সেট দেয়, যার মধ্যে `next` method এবং `Iterator` trait দ্বারা দেওয়া অন্যান্য utility method-এর মতো method রয়েছে। `Stream` ও `StreamExt` এখনও Rust-এর standard library-র অংশ নয়, কিন্তু বেশিরভাগ ecosystem crate অনুরূপ definition ব্যবহার করে।

Compiler error-এর সমাধান হলো `trpl::StreamExt`-এর জন্য একটি `use` statement যোগ করা, যেমন Listing 17-22-তে।

<Listing number="17-22" caption="Successfully using an iterator as the basis for a stream" file-name="src/main.rs">

```rust
use trpl::StreamExt;

fn main() {
    trpl::block_on(async {
        let values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        // --snip--
```

</Listing>

এই সব অংশ একত্র করলে কোডটি আমরা যেমন চাই তেমনভাবে কাজ করে! তার চেয়েও বেশি, এখন `StreamExt` scope-এ থাকায় আমরা তার সব utility method ব্যবহার করতে পারি, ঠিক যেমন iterator-এর সাথে করি।

[17-02-messages]: ch17-02-concurrency-with-async.html#message-passing
[iterator-trait]: ch13-02-iterators.html#the-iterator-trait-and-the-next-method

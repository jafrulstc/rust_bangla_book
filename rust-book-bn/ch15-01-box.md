## `Box<T>` ব্যবহার করে Heap-এ Data Point করা

সবচেয়ে সরল smart pointer হলো box, যার type লেখা হয় `Box<T>`। _Box_ গুলো তোমাকে stack-এর বদলে heap-এ data store করতে দেয়। stack-এ যা থাকে তা হলো শুধু heap-এর data-টির দিকে নির্দেশ করা pointer। stack এবং heap-এর পার্থক্য পুনরায় দেখতে Chapter 4-এ ফিরে যাও।

Box-এর data stack-এর বদলে heap-এ store করার বাইরে কোনো performance overhead নেই। তবে এগুলোর বিশেষ কোনো ক্ষমতাও বেশি নেই। তুমি সাধারণত এই কয়েকটা ক্ষেত্রে এগুলো ব্যবহার করবে:

- যখন তোমার এমন একটা type থাকে যার size compile time-এ জানা যায় না, এবং তুমি সেই type-এর একটা value এমন context-এ ব্যবহার করতে চাও যেখানে exact size প্রয়োজন
- যখন তোমার কাছে প্রচুর data থাকে, এবং তুমি ownership transfer করতে চাও কিন্তু নিশ্চিত করতে চাও যে এমন করার সময় data copy হবে না
- যখন তুমি একটা value own করতে চাও, এবং তোমার কাছে শুধু এটুকু গুরুত্ব যে এটি এমন একটা type যা কোনো নির্দিষ্ট trait implement করে, নির্দিষ্ট কোনো type নয়

আমরা প্রথম পরিস্থিতিটি [“Box দিয়ে Recursive Type সক্ষম করা”](#enabling-recursive-types-with-boxes)<!-- ignore -->-এ দেখাব। দ্বিতীয় ক্ষেত্রে, প্রচুর data-এর ownership transfer করতে অনেক সময় লাগতে পারে কারণ stack-এ data copy করতে হয়। এই পরিস্থিতিতে performance উন্নত করতে আমরা প্রচুর data একটা box-এ heap-এ store করতে পারি। তাহলে stack-এ শুধু pointer-এর ছোট অংশটুকু copy হবে, আর যে data-কে refer করা হচ্ছে সেটা heap-এ এক জায়গায় থাকবে। তৃতীয় ক্ষেত্রটিকে _trait object_ বলা হয়, এবং Chapter 18-এর [“Using Trait Objects to Abstract over Shared Behavior”][trait-objects]<!-- ignore --> section-টি পুরোপুরি এই topic-কে নিয়ে। তাই এখানে তুমি যা শিখবে সেটা ওই section-এও কাজে লাগবে!

<!-- Old headings. Do not remove or links may break. -->

<a id="using-boxt-to-store-data-on-the-heap"></a>

### Heap-এ Data Store করা

`Box<T>`-এর heap storage use case নিয়ে আলোচনার আগে, আমরা syntax এবং `Box<T>`-এর ভেতরে store করা value-এর সাথে কীভাবে interact করতে হয় সেটা দেখব।

Listing 15-1 দেখায় কীভাবে একটা box ব্যবহার করে একটা `i32` value heap-এ store করা যায়।

<Listing number="15-1" file-name="src/main.rs" caption="Storing an `i32` value on the heap using a box">

```rust
fn main() {
    let b = Box::new(5);
    println!("b = {b}");
}
```

</Listing>

আমরা variable `b`-কে define করেছি যাতে সেটি এমন একটা `Box`-এর value ধারণ করে যা `5` value-টির দিকে point করে, যেটি heap-এ allocate করা। এই program-টি `b = 5` print করবে; এই ক্ষেত্রে আমরা box-এর ভেতরের data-এ এমনভাবে access করতে পারি যেমনভাবে করতাম যদি এই data stack-এ থাকত। অন্য যেকোনো owned value-এর মতো, যখন একটা box scope ছেড়ে যায়, যেমন `b` `main`-এর শেষে করে, তখন সেটি deallocate হবে। deallocation box-এর জন্যও (যা stack-এ store করা) এবং এটি যে data-কে point করে তার জন্যও (যা heap-এ store করা) ঘটবে।

stack-এ একটা মাত্র value রাখাটা খুব বেশি কাজের নয়, তাই তুমি এভাবে একা box খুব বেশি ব্যবহার করবে না। ডিফল্টভাবে stack-এ store হওয়া একটা single `i32` value-এর মতো value বেশিরভাগ ক্ষেত্রেই বেশি উপযুক্ত। চলো এমন একটা ক্ষেত্র দেখি যেখানে box আমাদের এমন কিছু type define করতে দেয় যা box না থাকলে define করা যেত না।

### Box দিয়ে Recursive Type সক্ষম করা

কোনো _recursive type_-এর value-এর অংশ হিসেবে সেই একই type-এর আরেকটা value থাকতে পারে। recursive type একটা সমস্যা তৈরি করে কারণ Rust-কে compile time-এ জানতে হয় একটা type কত জায়গা নেয়। কিন্তু recursive type-এর value-এর nesting তাত্ত্বিকভাবে অসীমভাবে চলতে থাকতে পারে, তাই Rust জানতে পারে না value-টির কত জায়গা দরকার। যেহেতু box-এর size জানা থাকে, আমরা recursive type-এর definition-এ একটা box বসিয়ে recursive type সক্ষম করতে পারি।

recursive type-এর উদাহরণ হিসেবে চলো cons list নিয়ে আলোচনা করি। এটি functional programming language-এ সাধারণত দেখা যায় এমন একটা data type। আমরা যে cons list type define করব সেটি recursion ছাড়া বেশ সরল; তাই এই উদাহরণে যে concept গুলো নিয়ে কাজ করব সেগুলো recursive type জড়িত যেকোনো জটিল পরিস্থিতিতে কাজে লাগবে।

<!-- Old headings. Do not remove or links may break. -->

<a id="more-information-about-the-cons-list"></a>

#### Cons List বোঝা

_cons list_ হলো Lisp programming language এবং তার dialect থেকে আসা একটি data structure, যা nested pair দিয়ে তৈরি এবং এটি Lisp-এর linked list সংস্করণ। এর নাম এসেছে Lisp-এর `cons` function (সংক্ষেপে _construct function_) থেকে, যা দুটো argument থেকে একটি নতুন pair তৈরি করে। একটি value এবং আরেকটি pair নিয়ে গঠিত একটি pair-এ `cons` call করে আমরা recursive pair দিয়ে গঠিত cons list তৈরি করতে পারি।

উদাহরণস্বরূপ, এখানে `1, 2, 3` list ধারণকারী একটি cons list-এর pseudocode representation দেওয়া হলো, যেখানে প্রতিটি pair বন্ধনীর ভেতরে আছে:

```text
(1, (2, (3, Nil)))
```

cons list-এর প্রতিটি item দুটি element ধারণ করে: বর্তমান item-এর value এবং পরবর্তী item-এর value। list-এর শেষ item-টি শুধু একটি `Nil` নামের value ধারণ করে, কোনো পরবর্তী item থাকে না। cons list তৈরি হয় `cons` function-কে recursively call করার মাধ্যমে। recursion-এর base case বোঝাতে canonical নামটি হলো `Nil`। মনে রাখবে এটি Chapter 6-এ আলোচিত “null” বা “nil” concept-এর মতো নয়, যা একটি invalid বা absent value।

cons list Rust-এ খুব বেশি ব্যবহৃত data structure নয়। Rust-এ তোমার কাছে যখন একটা list of item থাকে, বেশিরভাগ ক্ষেত্রে `Vec<T>` ব্যবহার করাই ভালো পছন্দ। অন্যান্য আরও জটিল recursive data type বিভিন্ন পরিস্থিতিতে _কাজের_ হয়, কিন্তু এই chapter-এ cons list দিয়ে শুরু করলে আমরা বড় কোনো distraction ছাড়াই দেখতে পারব কীভাবে box আমাদের একটি recursive data type define করতে দেয়।

Listing 15-2-তে একটি cons list-এর enum definition দেওয়া আছে। মনে রাখবে এই code এখনো compile হবে না, কারণ `List` type-এর size জানা নেই, যা আমরা দেখাব।

<Listing number="15-2" file-name="src/main.rs" caption="The first attempt at defining an enum to represent a cons list data structure of `i32` values">

```rust,ignore,does_not_compile
enum List {
    Cons(i32, List),
    Nil,
}
```

</Listing>

> নোট: আমরা এই উদাহরণের জন্য শুধুমাত্র `i32` value ধারণ করে এমন একটি cons list implement করছি। আমরা চাইলে Chapter 10-এ আলোচনা করা generics ব্যবহার করে এমন একটি cons list type define করতে পারতাম যা যেকোনো type-এর value store করতে পারে।

`List` type ব্যবহার করে `1, 2, 3` list store করলে Listing 15-3-এর code-এর মতো দেখাবে।

<Listing number="15-3" file-name="src/main.rs" caption="Using the `List` enum to store the list `1, 2, 3`">

```rust,ignore,does_not_compile
// --snip--

use crate::List::{Cons, Nil};

fn main() {
    let list = Cons(1, Cons(2, Cons(3, Nil)));
}
```

</Listing>

প্রথম `Cons` value-টি `1` এবং আরেকটি `List` value ধারণ করে। এই `List` value-টি আরেকটি `Cons` value যা `2` এবং আরেকটি `List` value ধারণ করে। এই `List` value-টি আরও একটি `Cons` value যা `3` এবং একটি `List` value ধারণ করে, যা শেষে `Nil` — list-এর শেষ নির্দেশকারী non-recursive variant।

Listing 15-3-এর code compile করার চেষ্টা করলে আমরা Listing 15-4-এ দেখানো error পাব।

<Listing number="15-4" caption="The error we get when attempting to define a recursive enum">

```console
$ cargo run
   Compiling cons-list v0.1.0 (file:///projects/cons-list)
error[E0072]: recursive type `List` has infinite size
 --> src/main.rs:1:1
  |
1 | enum List {
  | ^^^^^^^^^
2 |     Cons(i32, List),
  |               ---- recursive without indirection
  |
help: insert some indirection (e.g., a `Box`, `Rc`, or `&`) to break the cycle
  |
2 |     Cons(i32, Box<List>),
  |               ++++    +

For more information about this error, try `rustc --explain E0072`.
error: could not compile `cons-list` (bin "cons-list") due to 1 previous error
```

</Listing>

error-টি দেখাচ্ছে যে এই type-টির “infinite size” আছে। কারণ আমরা `List`-কে এমন একটি variant দিয়ে define করেছি যা recursive: এটি সরাসরি নিজের আরেকটি value ধারণ করে। ফলে Rust বুঝতে পারে না একটি `List` value store করতে কত জায়গা দরকার। চলো দেখি কেন এই error আসে। প্রথমে আমরা দেখব Rust কীভাবে সিদ্ধান্ত নেয় একটি non-recursive type-এর value store করতে কত জায়গা দরকার।

#### Non-Recursive Type-এর Size Compute করা

Chapter 6-এ enum definition নিয়ে আলোচনার সময় Listing 6-2-তে আমরা যে `Message` enum define করেছিলাম সেটি মনে করো:

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}
```

একটি `Message` value-এর জন্য কত জায়গা allocate করতে হবে তা নির্ধারণ করতে Rust প্রতিটি variant দেখে কোন সবচেয়ে বড় variant-এ সবচেয়ে বেশি জায়গা দরকার। Rust দেখে যে `Message::Quit`-এ কোনো জায়গা লাগে না, `Message::Move`-এ দুটি `i32` value store করার মতো জায়গা দরকার, ইত্যাদি। যেহেতু শুধু একটি variant ব্যবহৃত হবে, একটি `Message` value-এর সর্বোচ্চ প্রয়োজন হবে তার সবচেয়ে বড় variant-টি store করার জায়গা।

এবার তুলনা করো যখন Rust বুঝতে চেষ্টা করে Listing 15-2-এর `List` enum-এর মতো একটি recursive type-এর জন্য কত জায়গা দরকার। compiler প্রথমে `Cons` variant দেখে, যা একটি `i32` type-এর value এবং একটি `List` type-এর value ধারণ করে। তাই `Cons`-এ দরকার একটি `i32`-এর size সমান জায়গার সাথে একটি `List`-এর size সমান জায়গা। `List` type-এর জন্য কত জায়গা দরকার তা বোঝার জন্য compiler variant গুলো দেখে, `Cons` variant দিয়ে শুরু করে। `Cons` variant একটি `i32` type-এর value এবং একটি `List` type-এর value ধারণ করে, এবং এই প্রক্রিয়াটি অসীমভাবে চলতে থাকে, যেমন Figure 15-1-এ দেখানো হয়েছে।

<img alt="An infinite Cons list: a rectangle labeled 'Cons' split into two smaller rectangles. The first smaller rectangle holds the label 'i32', and the second smaller rectangle holds the label 'Cons' and a smaller version of the outer 'Cons' rectangle. The 'Cons' rectangles continue to hold smaller and smaller versions of themselves until the smallest comfortably sized rectangle holds an infinity symbol, indicating that this repetition goes on forever." src="img/trpl15-01.svg" class="center" style="width: 50%;" />

<span class="caption">Figure 15-1: অসীম `Cons` variant নিয়ে গঠিত একটি অসীম `List`</span>

<!-- Old headings. Do not remove or links may break. -->

<a id="using-boxt-to-get-a-recursive-type-with-a-known-size"></a>

#### জানা Size সহ একটি Recursive Type পাওয়া

যেহেতু Rust recursively define করা type-গুলোর জন্য কত জায়গা allocate করতে হবে তা বের করতে পারে না, compiler এই সাহায্যকারী পরামর্শসহ একটি error দেয়:

<!-- manual-regeneration
after doing automatic regeneration, look at listings/ch15-smart-pointers/listing-15-03/output.txt and copy the relevant line
-->

```text
help: insert some indirection (e.g., a `Box`, `Rc`, or `&`) to break the cycle
  |
2 |     Cons(i32, Box<List>),
  |               ++++    +
```

এই পরামর্শে _indirection_ বলতে বোঝানো হচ্ছে যে আমাদের সরাসরি একটি value store করার বদলে data structure-টি এমনভাবে পরিবর্তন করা উচিত যাতে সেটি value-টির দিকে নির্দেশ করা একটি pointer store করে।

যেহেতু `Box<T>` একটি pointer, Rust সবসময় জানে একটি `Box<T>`-এর কত জায়গা দরকার: একটি pointer-এর size সেটি যতটুকু data-কে point করছে তার উপর নির্ভর করে না। এর মানে হলো আমরা `Cons` variant-এ সরাসরি আরেকটি `List` value-এর বদলে একটি `Box<T>` বসাতে পারি। `Box<T>`-টি heap-এ থাকা পরবর্তী `List` value-টির দিকে point করবে, `Cons` variant-এর ভেতরে নয়। ধারণাগতভাবে, আমাদের কাছে এখনো একটি list আছে যা অন্য list ধারণ করে এমন list দিয়ে তৈরি, কিন্তু এই implementation এখন অন্যের ভেতরে রাখার বদলে একে অপরের পাশে রাখার মতো।

আমরা Listing 15-2-এর `List` enum-এর definition এবং Listing 15-3-এর `List`-এর usage পরিবর্তন করে Listing 15-5-এর code-এ নিয়ে যেতে পারি, যা compile হবে।

<Listing number="15-5" file-name="src/main.rs" caption="The definition of `List` that uses `Box<T>` in order to have a known size">

```rust
enum List {
    Cons(i32, Box<List>),
    Nil,
}

use crate::List::{Cons, Nil};

fn main() {
    let list = Cons(1, Box::new(Cons(2, Box::new(Cons(3, Box::new(Nil))))));
}
```

</Listing>

`Cons` variant-এ একটি `i32`-এর size এবং box-এর pointer data store করার জায়গা দরকার। `Nil` variant কোনো value store করে না, তাই এর `Cons` variant-এর চেয়ে stack-এ কম জায়গা দরকার। এখন আমরা জানি যে যেকোনো `List` value একটি `i32`-এর size এবং একটি box-এর pointer data-এর size নেবে। box ব্যবহার করে আমরা অসীম recursive chain ভেঙে ফেলেছি, তাই compiler একটি `List` value store করার জন্য যে জায়গা দরকার তা বের করতে পারে। Figure 15-2 দেখায় `Cons` variant এখন কেমন দেখায়।

<img alt="A rectangle labeled 'Cons' split into two smaller rectangles. The first smaller rectangle holds the label 'i32', and the second smaller rectangle holds the label 'Box' with one inner rectangle that contains the label 'usize', representing the finite size of the box's pointer." src="img/trpl15-02.svg" class="center" />

<span class="caption">Figure 15-2: একটি `List` যা অসীম size-এর নয়, কারণ `Cons` একটি `Box` ধারণ করে</span>

box শুধু indirection এবং heap allocation দেয়; অন্যান্য smart pointer type-এর সাথে যে বিশেষ ক্ষমতা থাকে সেগুলো এদের নেই। এগুলোর সেই বিশেষ ক্ষমতার কারণে যে performance overhead হয় তাও এদের নেই, তাই cons list-এর মতো ক্ষেত্রে যেখানে শুধু indirection-ই আমাদের দরকার, সেখানে এগুলো কাজে লাগে। box-এর আরও কিছু use case আমরা Chapter 18-এ দেখব।

`Box<T>` type একটি smart pointer কারণ এটি `Deref` trait implement করে, যা `Box<T>` value-কে reference-এর মতো বিবেচনা করতে দেয়। যখন একটি `Box<T>` value scope ছেড়ে যায়, তখন `Drop` trait implementation-এর কারণে box-টি যে heap data-কে point করছিল সেটিও পরিষ্কার করা হয়। এই দুটি trait এই chapter-এর বাকি অংশে আলোচনা করা অন্যান্য smart pointer type-এর functionality-র কাছে আরও বেশি গুরুত্বপূর্ণ হবে। চলো এই দুটি trait নিয়ে আরও বিস্তারিত আলোচনা করি।

[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior

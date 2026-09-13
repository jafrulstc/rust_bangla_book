## Vectors দিয়ে Value-এর List Store করা

আমরা যে প্রথম collection type-টা দেখব সেটা হলো `Vec<T>`, যাকে vector ও বলা হয়। Vector তোমাকে একটিমাত্র data structure-এ একাধিক value store করতে দেয়, যেখানে সব value মেমরিতে পাশাপাশি থাকে। Vector শুধুমাত্র একই type-এর value store করতে পারে। যখন তোমার কাছে item-গুলোর একটি list থাকে—যেমন একটি file-এর text-এর line গুলো বা একটি shopping cart-এর item-গুলোর দাম—তখনই vector কাজে লাগে।

### নতুন Vector তৈরি করা

নতুন, খালি একটি vector তৈরি করতে আমরা `Vec::new` function কল করি, Listing 8-1-এ যেমন দেখানো হয়েছে।

<Listing number="8-1" caption="নতুন, খালি একটি vector তৈরি করা যাতে `i32` type-এর value রাখা যায়">

```rust
    let v: Vec<i32> = Vec::new();
```

</Listing>

খেয়াল করো যে এখানে আমরা একটি type annotation যোগ করেছি। যেহেতু আমরা এই vector-এ কোনো value insert করছি না, তাই Rust জানে না আমরা কী ধরনের element store করতে চাই। এটি একটি গুরুত্বপূর্ণ বিষয়। Vector generics ব্যবহার করে implement করা হয়; নিজের type-এর সাথে generics কীভাবে ব্যবহার করতে হয় সেটা আমরা Chapter 10-এ দেখব। আপাতত জেনে রাখো যে standard library-তে দেওয়া `Vec<T>` type যেকোনো type ধরে রাখতে পারে। যখন আমরা নির্দিষ্ট কোনো type ধরে রাখার জন্য vector তৈরি করি, তখন আমরা type-টা angle bracket-এর ভেতর উল্লেখ করতে পারি। Listing 8-1-এ আমরা Rust-কে জানিয়েছি যে `v`-তে থাকা `Vec<T>` `i32` type-এর element ধরে রাখবে।

বেশিরভাগ ক্ষেত্রে তুমি একটি `Vec<T>` initial value-সহ তৈরি করবে, এবং Rust তোমার কোন type-এর value store করতে চাইছ সেটা infer করে নেবে, তাই খুব কমই এই type annotation-এর দরকার হয়। Rust সুবিধাজনকভাবে `vec!` macro দেয়, যা তোমার দেওয়া value গুলো ধরে রাখা নতুন vector তৈরি করবে। Listing 8-2 একটি নতুন `Vec<i32>` তৈরি করে যা `1`, `2`, ও `3` value গুলো ধরে রাখে। Integer type হলো `i32` কারণ সেটাই default integer type, যেমনটা আমরা Chapter 3-এর [“Data
Types”][data-types]<!-- ignore --> section-এ আলোচনা করেছি।

<Listing number="8-2" caption="Value সহ নতুন একটি vector তৈরি করা">

```rust
    let v = vec![1, 2, 3];
```

</Listing>

যেহেতু আমরা initial `i32` value দিয়েছি, Rust infer করতে পারে যে `v`-এর type হলো `Vec<i32>`, তাই type annotation আর দরকার নেই। এরপর আমরা দেখব কীভাবে একটি vector modify করতে হয়।

### Vector আপডেট করা

একটি vector তৈরি করে তাতে element যোগ করতে আমরা `push` method ব্যবহার করতে পারি, Listing 8-3-এ যেমন দেখানো হয়েছে।

<Listing number="8-3" caption="`push` method ব্যবহার করে একটি vector-এ value যোগ করা">

```rust
    let mut v = Vec::new();

    v.push(5);
    v.push(6);
    v.push(7);
    v.push(8);
```

</Listing>

অন্য যেকোনো variable-এর মতো, যদি আমরা এর value পরিবর্তন করতে চাই, তাহলে Chapter 3-এ আলোচনা করা অনুযায়ী `mut` keyword ব্যবহার করে সেটিকে mutable করতে হবে। আমরা ভেতরে যে সংখ্যাগুলো রাখছি সবই `i32` type-এর, এবং Rust সেটা data থেকে infer করে, তাই আমাদের `Vec<i32>` annotation লাগে না।

### Vector-এর Element Read করা

Vector-এ store করা কোনো value-কে reference করার দুটি উপায় আছে: indexing-এর মাধ্যমে অথবা `get` method ব্যবহার করে। নিচের example-গুলোতে, বুঝতে সুবিধা হওয়ার জন্য আমরা এই function-গুলো থেকে ফেরত আসা value-গুলোর type উল্লেখ করে দিয়েছি।

Listing 8-4-এ একটি vector-এর ভেতরের কোনো value access করার উভয় method দেখানো হয়েছে—indexing syntax ও `get` method।

<Listing number="8-4" caption="Indexing syntax এবং `get` method ব্যবহার করে একটি vector-এর item access করা">

```rust
    let v = vec![1, 2, 3, 4, 5];

    let third: &i32 = &v[2];
    println!("The third element is {third}");

    let third: Option<&i32> = v.get(2);
    match third {
        Some(third) => println!("The third element is {third}"),
        None => println!("There is no third element."),
    }
```

</Listing>

এখানে কয়েকটি বিষয় খেয়াল করো। আমরা তৃতীয় element পেতে index value `2` ব্যবহার করেছি কারণ vector সংখ্যা দিয়ে index করা হয়, শূন্য থেকে শুরু হয়ে। `&` ও `[]` ব্যবহার করলে আমরা সেই index value-তে থাকা element-এর একটি reference পাই। যখন আমরা `get` method-এ index argument হিসেবে পাস করি, তখন আমরা একটি `Option<&T>` পাই যা `match`-এর সাথে ব্যবহার করতে পারি।

Rust একটি element-কে reference করার এই দুটি উপায় দেয়, যাতে তুমি বেছে নিতে পারো যে বিদ্যমান element-এর range-এর বাইরের কোনো index value ব্যবহার করার চেষ্টা করলে program কীভাবে আচরণ করবে। একটি example হিসেবে দেখি, যখন আমাদের কাছে পাঁচটি element-বিশিষ্ট একটি vector আছে এবং আমরা প্রতিটি technique দিয়ে index 100-এর element access করার চেষ্টা করি তখন কী হয়, সেটা Listing 8-5-এ দেখানো হয়েছে।

<Listing number="8-5" caption="পাঁচটি element বিশিষ্ট একটি vector-এ index 100-এর element access করার চেষ্টা">

```rust,should_panic,panics
    let v = vec![1, 2, 3, 4, 5];

    let does_not_exist = &v[100];
    let does_not_exist = v.get(100);
```

</Listing>

এই code run করলে প্রথম `[]` method-টি program-কে panic করাবে কারণ এটি এমন একটি element-কে reference করে যা বিদ্যমান নেই। এই method তখন সবচেয়ে ভালো কাজে লাগে যখন তুমি চাও যে vector-এর শেষের দিকের element-এর বাইরে access করার চেষ্টা হলে program crash করুক।

অন্যদিকে, `get` method-কে vector-এর বাইরের কোনো index পাস করা হলে সেটা panic না করে `None` ফেরত দেয়। স্বাভাবিক পরিস্থিতিতে যদি vector-এর range-এর বাইরের কোনো element access করা মাঝে মাঝে ঘটতে পারে, তখন তুমি এই method ব্যবহার করবে। তারপর তোমার code-এ Chapter 6-এ আলোচিত অনুযায়ী `Some(&element)` অথবা `None` handle করার logic থাকবে। যেমন, index-টা হয়তো কোনো ব্যক্তি একটি সংখ্যা প্রবেশ করা থেকে আসতে পারে। যদি সে ভুলে অনেক বড় একটি সংখ্যা প্রবেশ করে এবং program একটি `None` value পায়, তুমি ব্যবহারকারীকে বলে দিতে পারো যে বর্তমান vector-এ কয়টি item আছে এবং তাকে একটি বৈধ value প্রবেশ করার আরেকটি সুযোগ দিতে পারো। এটা হবে typing ভুলের কারণে program crash করার চেয়ে অনেক বেশি user-friendly!

যখন program-এর কাছে একটি বৈধ reference থাকে, তখন borrow checker ownership ও borrowing rule (Chapter 4-এ আলোচিত) enforce করে নিশ্চিত করতে যে এই reference এবং vector-এর content-এর অন্য যেকোনো reference বৈধ থাকে। সেই rule-টা মনে করো যেটা বলে তুমি একই scope-এ mutable ও immutable reference একসাথে রাখতে পারবে না। সেই rule Listing 8-6-এও প্রযোজ্য, যেখানে আমরা একটি vector-এর প্রথম element-এর একটি immutable reference ধরে রেখে শেষে আরেকটি element যোগ করার চেষ্টা করছি। যদি আমরা পরে function-এর ভেতরে সেই element-কে আবার reference করার চেষ্টা করি তবে এই program কাজ করবে না।

<Listing number="8-6" caption="একটি item-এর reference ধরে রেখে একটি vector-এ element যোগ করার চেষ্টা">

```rust,ignore,does_not_compile
    let mut v = vec![1, 2, 3, 4, 5];

    let first = &v[0];

    v.push(6);

    println!("The first element is: {first}");
```

</Listing>

এই code compile করলে নিচের error পাওয়া যাবে:

```console
$ cargo run
   Compiling collections v0.1.0 (file:///projects/collections)
error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
 --> src/main.rs:6:5
  |
4 |     let first = &v[0];
  |                  - immutable borrow occurs here
5 |
6 |     v.push(6);
  |     ^^^^^^^^^ mutable borrow occurs here
7 |
8 |     println!("The first element is: {first}");
  |                                      ----- immutable borrow later used here

For more information about this error, try `rustc --explain E0502`.
error: could not compile `collections` (bin "collections") due to 1 previous error
```

Listing 8-6-এর code মনে হতে পারে যে কাজ করা উচিত: প্রথম element-এর reference কেন শেষে করা পরিবর্তনটা নিয়ে মাথা ঘামাবে? এই error-টি আসলে vector-এর কাজ করার ধরনের কারণে হয়েছে: যেহেতু vector value গুলোকে মেমরিতে পাশাপাশি রাখে, তাই vector-এর শেষে নতুন element যোগ করার সময় মেমরি allocate করে পুরনো element গুলোকে নতুন জায়গায় copy করতে হতে পারে, যদি vector বর্তমানে যেখানে store করা সেখানে সব element-কে পাশাপাশি রাখার মতো জায়গা না থাকে। সেই ক্ষেত্রে প্রথম element-এর reference deallocated মেমরিকে point করত। Borrowing rule গুলো program-কে সেই পরিস্থিতিতে পড়তে দেয় না।

> নোট: `Vec<T>` type-এর implementation সম্পর্কে আরও জানতে [“The
> Rustonomicon”][nomicon] দেখো।

### Vector-এর Value গুলোর উপর Iterate করা

একটি vector-এর প্রতিটি element-এ পালাক্রমে access করতে হলে আমরা index দিয়ে একটা একটা করে access করার বদলে সব element-এর উপর দিয়ে iterate করব। Listing 8-7 দেখায় কীভাবে একটি `for` loop ব্যবহার করে `i32` value-এর একটি vector-এর প্রতিটি element-এর immutable reference নিয়ে সেগুলো print করা যায়।

<Listing number="8-7" caption="`for` loop দিয়ে element-গুলোর উপর iterate করে একটি vector-এর প্রতিটি element print করা">

```rust
    let v = vec![100, 32, 57];
    for i in &v {
        println!("{i}");
    }
```

</Listing>

আমরা একটি mutable vector-এর প্রতিটি element-এর mutable reference-এর উপরও iterate করতে পারি, যাতে সব element-এ পরিবর্তন আনা যায়। Listing 8-8-এর `for` loop প্রতিটি element-এর সাথে `50` যোগ করবে।

<Listing number="8-8" caption="একটি vector-এর element-গুলোর mutable reference-এর উপর iterate করা">

```rust
    let mut v = vec![100, 32, 57];
    for i in &mut v {
        *i += 50;
    }
```

</Listing>

Mutable reference যে value-কে point করে সেটা পরিবর্তন করতে হলে আমাদের `+=` operator ব্যবহার করার আগে `*` dereference operator দিয়ে `i`-এর value-টায় পৌঁছাতে হবে। Dereference operator নিয়ে আমরা Chapter 15-এর [“Following the
Reference to the Value”][deref]<!-- ignore --> section-এ আরও কথা বলব।

একটি vector-এর উপর iterate করা, immutable হোক বা mutable, borrow checker-এর rule-এর কারণে safe। যদি আমরা Listing 8-7 ও Listing 8-8-এর `for` loop body-তে item insert বা remove করার চেষ্টা করতাম, তাহলে Listing 8-6-এর code-এর মতো একটি compiler error পেতাম। `for` loop যে vector-এর reference ধরে রাখে সেটা পুরো vector-এর একই সাথে modification হতে দেয় না।

### একাধিক Type Store করতে Enum ব্যবহার করা

Vector শুধুমাত্র একই type-এর value store করতে পারে। এটি মাঝে মাঝে অসুবিধার হতে পারে; ভিন্ন ভিন্ন type-এর item-গুলোর একটি list store করার প্রয়োজন নিশ্চয়ই থাকে। সৌভাগ্যক্রমে, একটি enum-এর variant গুলো একই enum type-এর অধীনে define করা থাকে, তাই যখন আমাদের ভিন্ন ভিন্ন type-এর element-কে একটি type দিয়ে represent করতে হবে, তখন আমরা একটি enum define করে ব্যবহার করতে পারি!

যেমন ধরো, আমরা একটি spreadsheet-এর একটি row থেকে value নিতে চাই যেখানে row-এর কিছু column-এ integer, কিছুতে floating-point number, আর কিছুতে string আছে। আমরা এমন একটি enum define করতে পারি যার variant গুলো ভিন্ন ভিন্ন value type ধরে রাখবে, এবং সব enum variant একই type হিসেবে গণ্য হবে: সেই enum-টি। তারপর আমরা সেই enum ধরে রাখার জন্য একটি vector তৈরি করতে পারি এবং এভাবে আসলে ভিন্ন ভিন্ন type store করতে পারি। এটা আমরা Listing 8-9-তে দেখিয়েছি।

<Listing number="8-9" caption="একটি vector-এ ভিন্ন ভিন্ন type-এর value store করতে একটি enum define করা">

```rust
    enum SpreadsheetCell {
        Int(i32),
        Float(f64),
        Text(String),
    }

    let row = vec![
        SpreadsheetCell::Int(3),
        SpreadsheetCell::Text(String::from("blue")),
        SpreadsheetCell::Float(10.12),
    ];
```

</Listing>

Rust-কে compile time-এ জানা দরকার vector-এ কোন কোন type থাকবে, যাতে প্রতিটি element store করতে heap-এ ঠিক কতটুকু মেমরি লাগবে সেটা নিখুঁতভাবে জানা যায়। এছাড়া এই vector-এ কোন কোন type allowed সেটা নিয়েও আমাদের explicit হতে হবে। যদি Rust একটি vector-কে যেকোনো type ধরে রাখতে দিত, তাহলে এমন হতে পারত যে এক বা একাধিক type vector-এর element-এর উপর করা operation-এ error ঘটাত। Enum ও `match` expression ব্যবহার করলে Rust compile time-ে নিশ্চিত করে যে প্রতিটি সম্ভাব্য case handle করা হয়েছে, যেমনটা Chapter 6-এ আলোচনা করা হয়েছে।

যদি তুমি না জানো যে program runtime-এ vector-এ store করার জন্য কোন সব type পাবে, তাহলে enum technique কাজ করবে না। তার বদলে তুমি একটি trait object ব্যবহার করতে পারো, যেটা নিয়ে আমরা Chapter 18-এ কথা বলব।

যেহেতু এখন vector ব্যবহারের সবচেয়ে সাধারণ কয়েকটি পদ্ধতি নিয়ে আলোচনা করেছি, তাই `Vec<T>`-তে standard library দ্বারা define করা অনেক কাজের method সম্পর্কে জানতে অবশ্যই [API documentation][vec-api]<!-- ignore --> দেখে নিও। যেমন, `push`-এর পাশাপাশি একটি `pop` method আছে যা শেষ element-কে remove করে ফেরত দেয়।

### একটি Vector Drop হলে এর Element গুলোও Drop হয়

অন্য যেকোনো `struct`-এর মতো, একটি vector তার scope ছেড়ে গেলে free হয়ে যায়, যেমন Listing 8-10-তে annotate করা হয়েছে।

<Listing number="8-10" caption="Vector ও এর element গুলো কোথায় drop হয় তা দেখানো হচ্ছে">

```rust
    {
        let v = vec![1, 2, 3, 4];

        // do stuff with v
    } // <- v goes out of scope and is freed here
```

</Listing>

Vector যখন drop হয়, তখন এর সব content-ও drop হয়, অর্থাৎ এটি যে integer গুলো ধরে রেখেছিল সেগুলোও clean up হবে। Borrow checker নিশ্চিত করে যে vector-এর content-এর কোনো reference শুধুমাত্র vector নিজে বৈধ থাকা অবস্থায়ই ব্যবহার করা হয়।

চলো পরের collection type-এ যাই: `String`!

[data-types]: ch03-02-data-types.html#data-types
[nomicon]: ../nomicon/vec/vec.html
[vec-api]: ../std/vec/struct.Vec.html
[deref]: ch15-02-deref.html#following-the-pointer-to-the-value-with-the-dereference-operator

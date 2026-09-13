## Lifetimes দিয়ে Reference Validate করা

Lifetimes হলো আরেক ধরনের generic, যা আমরা ইতিমধ্যে ব্যবহার করছি। Type-এর আমাদের কাঙ্ক্ষিত behavior আছে তা নিশ্চিত করার বদলে, lifetimes নিশ্চিত করে যে reference-গুলো যতক্ষণ আমাদের প্রয়োজন ততক্ষণ valid থাকবে।

Chapter 4-এর [“References and Borrowing”][references-and-borrowing]<!-- ignore --> section-এ আমরা যে বিষয়টি আলোচনা করিনি তা হলো—Rust-এ প্রতিটি reference-এর একটি lifetime আছে, যেটি হলো সেই scope যেখানে সেই reference-টি valid। বেশিরভাগ ক্ষেত্রে, lifetimes implicit এবং inferred, ঠিক যেমন বেশিরভাগ ক্ষেত্রে type-গুলো inferred হয়। আমরা শুধুমাত্র তখনই type annotate করতে বাধ্য যখন একাধিক type সম্ভব। একইভাবে, আমাদের তখনই lifetime annotate করতে হবে যখন reference-গুলোর lifetime কয়েকভাবে সম্পর্কিত হতে পারে। Rust আমাদেরকে সেই সম্পর্কগুলো generic lifetime parameter দিয়ে annotate করতে বাধ্য করে, যাতে runtime-এ ব্যবহৃত প্রকৃত reference-গুলো নিশ্চিতভাবে valid হবে।

Lifetime annotate করা বেশিরভাগ অন্যান্য programming language-এ একটি concept-ই নয়, তাই এটি তোমাকে অপরিচিত মনে হবে। যদিও এই chapter-এ আমরা lifetimes-এর সম্পূর্ণ আলোচনা করবো না, তবে সেইসব সাধারণ পরিস্থিতি আলোচনা করবো যেখানে তুমি lifetime syntax-এর মুখোমুখি হতে পারো, যাতে তুমি এই concept-টির সাথে স্বাচ্ছন্দ্য অর্জন করতে পারো।

<!-- Old headings. Do not remove or links may break. -->

<a id="preventing-dangling-references-with-lifetimes"></a>

### Dangling References

Lifetimes-এর প্রধান উদ্দেশ্য হলো dangling references প্রতিরোধ করা, যা যদি বিদ্যমান থাকতে দেওয়া হতো, তবে একটি প্রোগ্রামকে এমন কোনো data-কে refer করতে বাধ্য করতো যা সে actually refer করার কথা নয়। Listing 10-16-এর প্রোগ্রামটি বিবেচনা করো, যেটির একটি outer scope এবং একটি inner scope আছে।

<Listing number="10-16" caption="An attempt to use a reference whose value has gone out of scope">

```rust,ignore,does_not_compile
fn main() {
    let r;

    {
        let x = 5;
        r = &x;
    }

    println!("r: {r}");
}
```

</Listing>

> নোট: Listings 10-16, 10-17, এবং 10-23-এর উদাহরণগুলোতে variable-গুলোকে কোনো initial value না দিয়েই declare করা হয়েছে, যাতে variable-এর নামটি outer scope-এ বিদ্যমান থাকে। প্রথম দর্শনে, এটি এমন মনে হতে পারে যে Rust-এ null value না থাকার নিয়মের সাথে সাংঘর্ষিক। তবে, যদি আমরা কোনো variable-কে value দেওয়ার আগেই ব্যবহার করার চেষ্টা করি, তাহলে আমরা একটি compile-time error পাবো, যা প্রমাণ করে যে সত্যিই Rust null value allow করে না।

Outer scope `r` নামের একটি variable কোনো initial value ছাড়াই declare করে, এবং inner scope `x` নামের একটি variable `5` initial value সহ declare করে। Inner scope-এর ভেতরে, আমরা `r`-এর value হিসেবে `x`-এর একটি reference set করার চেষ্টা করি। তারপর, inner scope শেষ হয় এবং আমরা `r`-এর value print করার চেষ্টা করি। এই code compile হবে না, কারণ `r` যে value-টি refer করছে সেটি আমরা ব্যবহার করার আগেই scope থেকে বেরিয়ে গেছে। এই error message-টি এখানে দেওয়া হলো:

```console
$ cargo run
   Compiling chapter10 v0.1.0 (file:///projects/chapter10)
error[E0597]: `x` does not live long enough
 --> src/main.rs:6:13
  |
5 |         let x = 5;
  |             - binding `x` declared here
6 |         r = &x;
  |             ^^ borrowed value does not live long enough
7 |     }
  |     - `x` dropped here while still borrowed
8 |
9 |     println!("r: {r}");
  |                   - borrow later used here

For more information about this error, try `rustc --explain E0597`.
error: could not compile `chapter10` (bin "chapter10") due to 1 previous error
```

Error message-টি বলছে যে variable `x` "does not live long enough"। কারণ হলো যখন inner scope 7 নম্বর লাইনে শেষ হয় তখন `x` scope-এর বাইরে চলে যাবে। কিন্তু `r` এখনও outer scope-এর জন্য valid; যেহেতু এর scope বড়, আমরা বলি সে "lives longer"। যদি Rust এই code টি কাজ করতে দিতো, তবে `r` এমন memory-কে refer করতো যা `x` scope-এর বাইরে যাওয়ার সময় deallocate হয়ে গেছে, এবং `r` দিয়ে আমরা যা করার চেষ্টা করতাম তা সঠিকভাবে কাজ করতো না। তাহলে, Rust কীভাবে নির্ধারণ করে যে এই code-টি invalid? এটি একটি borrow checker ব্যবহার করে।

### The Borrow Checker

Rust compiler-এ একটি _borrow checker_ আছে যা scope-গুলো compare করে নির্ধারণ করে যে সব borrow-ই valid কিনা। Listing 10-17 Listing 10-16-এর একই code দেখায় কিন্তু variable-গুলোর lifetime দেখাতে annotation সহ।

<Listing number="10-17" caption="Annotations of the lifetimes of `r` and `x`, named `'a` and `'b`, respectively">

```rust,ignore,does_not_compile
fn main() {
    let r;                // ---------+-- 'a
                          //          |
    {                     //          |
        let x = 5;        // -+-- 'b  |
        r = &x;           //  |       |
    }                     // -+       |
                          //          |
    println!("r: {r}");   //          |
}                         // ---------+
```

</Listing>

এখানে, আমরা `r`-এর lifetime কে `'a` এবং `x`-এর lifetime কে `'b` দিয়ে annotate করেছি। যেমন দেখতে পাচ্ছো, ভেতরের `'b` block বাইরের `'a` lifetime block-এর চেয়ে অনেক ছোট। Compile time-এ, Rust দুটো lifetime-এর আকার compare করে দেখে যে `r`-এর lifetime `'a` কিন্তু এটি এমন memory-কে refer করে যার lifetime `'b`। প্রোগ্রামটি reject করা হয় কারণ `'b` এর চেয়ে `'a` ছোট: reference-এর subject reference-এর সমান সময় বাঁচে না।

Listing 10-18 code-টিকে ঠিক করে যাতে এতে কোনো dangling reference নেই এবং এটি কোনো error ছাড়াই compile হয়।

<Listing number="10-18" caption="A valid reference because the data has a longer lifetime than the reference">

```rust
fn main() {
    let x = 5;            // ----------+-- 'b
                          //           |
    let r = &x;           // --+-- 'a  |
                          //   |       |
    println!("r: {r}");   //   |       |
                          // --+       |
}                         // ----------+
```

</Listing>

এখানে, `x`-এর lifetime `'b`, যা এই ক্ষেত্রে `'a`-এর চেয়ে বড়। এর মানে `r` যখন `x` valid আছে তখনই `x`-কে refer করতে পারে, কারণ Rust জানে যে `r`-এর reference-টি `x` valid থাকা পর্যন্ত সবসময় valid থাকবে।

যেহেতু এখন তুমি জানো reference-গুলোর lifetime কোথায় এবং Rust কীভাবে reference-গুলো সবসময় valid হবে তা নিশ্চিত করতে lifetime analyze করে, চলো এবার function parameter ও return value-তে generic lifetime explore করি।

### In Function-এ Generic Lifetimes

আমরা এমন একটি function লিখবো যা দুটি string slice-এর মধ্যে দীর্ঘতমটি return করে। এই function দুটি string slice নেবে এবং একটি single string slice return করবে। আমরা `longest` function implement করার পর, Listing 10-19-এর code টির উচিত `The longest string is abcd` print করা।

<Listing number="10-19" file-name="src/main.rs" caption="A `main` function that calls the `longest` function to find the longer of two string slices">

```rust,ignore
fn main() {
    let string1 = String::from("abcd");
    let string2 = "xyz";

    let result = longest(string1.as_str(), string2);
    println!("The longest string is {result}");
}
```

</Listing>

মনে রেখো, আমরা চাই function-টি string না, বরং যেগুলো reference সেগুলো string slice নিক, কারণ আমরা চাই না `longest` function তার parameter-গুলোর ownership নিক। Listing 10-19-এ আমরা যে parameter-গুলো ব্যবহার করছি সেগুলোই কেন কাঙ্ক্ষিত, তার আরও আলোচনার জন্য Chapter 4-এর [“String Slices as Parameters”][string-slices-as-parameters]<!-- ignore --> দেখো।

যদি আমরা Listing 10-20-এ দেখানো মতো `longest` function implement করার চেষ্টা করি, তবে এটি compile হবে না।

<Listing number="10-20" file-name="src/main.rs" caption="An implementation of the `longest` function that returns the longer of two string slices but does not yet compile">

```rust,ignore,does_not_compile
fn longest(x: &str, y: &str) -> &str {
    if x.len() > y.len() { x } else { y }
}
```

</Listing>

এর বদলে, আমরা lifetime সম্পর্কে কথা বলা নিচের error টি পাই:

```console
$ cargo run
   Compiling chapter10 v0.1.0 (file:///projects/chapter10)
error[E0106]: missing lifetime specifier
 --> src/main.rs:9:33
  |
9 | fn longest(x: &str, y: &str) -> &str {
  |               ----     ----     ^ expected named lifetime parameter
  |
  = help: this function's return type contains a borrowed value, but the signature does not say whether it is borrowed from `x` or `y`
help: consider introducing a named lifetime parameter
  |
9 | fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
  |           ++++     ++          ++          ++

For more information about this error, try `rustc --explain E0106`.
error: could not compile `chapter10` (bin "chapter10") due to 1 previous error
```

Help text-এ প্রকাশ পায় যে return type-এ একটি generic lifetime parameter প্রয়োজন, কারণ Rust বুঝতে পারে না return করা reference-টি `x` নাকি `y`-কে refer করে। আসলে, আমরাও জানি না, কারণ এই function-এর body-তে `if` block একটি `x`-এর reference এবং `else` block একটি `y`-এর reference return করে!

আমরা যখন এই function define করছি, তখন আমরা জানি না এই function-এ কোন concrete value পাস করা হবে, তাই আমরা জানি না `if` case নাকি `else` case execute হবে। আমরা পাস করা reference-গুলোর concrete lifetime-ও জানি না, তাই Listing 10-17 এবং 10-18-এর মতো scope-এ দেখে নির্ধারণ করতে পারি না যে আমরা যে reference return করছি তা সবসময় valid থাকবে কিনা। Borrow checker এটিও নির্ধারণ করতে পারে না, কারণ সে জানে না `x` ও `y`-এর lifetime return value-র lifetime-এর সাথে কীভাবে সম্পর্কিত। এই error-টি fix করতে, আমরা generic lifetime parameter যোগ করবো যা reference-গুলোর মধ্যে সম্পর্ক define করবে, যাতে borrow checker তার analysis সম্পাদন করতে পারে।

### Lifetime Annotation Syntax

Lifetime annotation-গুলো কোনো reference-এর জীবনকাল পরিবর্তন করে না। বরং, সেগুলো একাধিক reference-এর lifetime-গুলোর পারস্পরিক সম্পর্ক বর্ণনা করে, lifetime-গুলোকে প্রভাবিত না করেই। ঠিক যেমন function signature-এ একটি generic type parameter specify করলে function যেকোনো type গ্রহণ করতে পারে, function generic lifetime parameter specify করে যেকোনো lifetime-সহ reference গ্রহণ করতে পারে।

Lifetime annotation-গুলোর syntax সামান্য অস্বাভাবিক: lifetime parameter-গুলোর নাম একটি apostrophe (`'`) দিয়ে শুরু হতে হবে এবং সাধারণত সম্পূর্ণ lowercase এবং খুব ছোট হয়, generic type-এর মতো। বেশিরভাগ মানুষ প্রথম lifetime annotation-এর জন্য `'a` নামটি ব্যবহার করে। আমরা একটি reference-এর `&`-এর পরে lifetime parameter annotation স্থাপন করি, একটি space ব্যবহার করে annotation-কে reference-এর type থেকে আলাদা করি।

এখানে কিছু উদাহরণ দেওয়া হলো—lifetime parameter ছাড়া একটি `i32`-এর reference, `'a` নামের lifetime parameter সহ একটি `i32`-এর reference, এবং `'a` lifetime সহ একটি `i32`-এর mutable reference:

```rust,ignore
&i32        // a reference
&'a i32     // a reference with an explicit lifetime
&'a mut i32 // a mutable reference with an explicit lifetime
```

এককভাবে একটি lifetime annotation-এর বিশেষ কোনো অর্থ নেই, কারণ annotation-গুলোর উদ্দেশ্য হলো Rust-কে বলা যে একাধিক reference-এর generic lifetime parameter-গুলো পরস্পরের সাথে কীভাবে সম্পর্কিত। চলো দেখি `longest` function-এর context-এ lifetime annotation-গুলো পরস্পরের সাথে কীভাবে সম্পর্কিত।

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-function-signatures"></a>

### In Function Signatures

Function signature-এ lifetime annotation ব্যবহার করতে, আমাদের function-ের নাম এবং parameter list-এর মাঝে angle bracket-এর ভেতর generic lifetime parameter-গুলো declare করতে হবে, ঠিক যেমন আমরা generic type parameter-গুলোর সাথে করেছি।

আমরা চাই signature-টি নিচের constraint-টি প্রকাশ করুক: Return করা reference ততক্ষণ valid থাকবে যতক্ষণ উভয় parameter-ই valid থাকে। এটিই parameter-গুলোর lifetime এবং return value-এর মধ্যে সম্পর্ক। আমরা lifetime-এর নাম `'a` দেবো এবং তারপর প্রতিটি reference-এ তা যোগ করবো, যেমন Listing 10-21-এ দেখানো হয়েছে।

<Listing number="10-21" file-name="src/main.rs" caption="The `longest` function definition specifying that all the references in the signature must have the same lifetime `'a`">

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

</Listing>

এই code টি compile হবে এবং Listing 10-19-এর `main` function-এর সাথে ব্যবহার করলে আমরা যে result চাই তা তৈরি করবে।

Function signature-টি এখন Rust-কে বলে যে কোনো এক lifetime `'a`-এর জন্য, function দুটি parameter নেয়, যার দুটোই string slice এবং যা অন্তত lifetime `'a`-এর সমান সময় বাঁচে। Function signature-টি এছাড়াও Rust-কে বলে যে function থেকে return করা string slice অন্তত lifetime `'a`-এর সমান সময় বাঁচবে। বাস্তবে, এর মানে হলো `longest` function দ্বারা return করা reference-এর lifetime সেই function argument দ্বারা refer করা value-গুলোর ছোট lifetime-টির সমান। এই সম্পর্কগুলোই আমরা চাই Rust যেন এই code analyze করার সময় ব্যবহার করে।

মনে রেখো, আমরা যখন এই function signature-এ lifetime parameter specify করছি, তখন আমরা পাস করা বা return করা কোনো value-র lifetime পরিবর্তন করছি না। বরং, আমরা specify করছি যে borrow checker যেন সেই constraint মেনে চলে না এমন কোনো value-কে reject করে। মনে রাখো `longest` function-কে জানার দরকার নেই যে `x` এবং `y` ঠিক কতক্ষণ বাঁচবে, শুধু জানা দরকার যে `'a`-এর জায়গায় কোনো একটি scope বসানো যাবে যা এই signature পূরণ করবে।

Function-এ lifetime annotate করার সময়, annotation-গুলো function body-তে নয়, function signature-এ থাকে। Lifetime annotation-গুলো function-এর contract-এর অংশ হয়ে যায়, ঠিক যেমন signature-এর type-গুলো। Function signature-এ lifetime contract থাকার অর্থ হলো Rust compiler যে analysis করে তা আরও সহজ হতে পারে। যদি কোনো function annotate করার ধরন বা তা call করার ধরনে কোনো সমস্যা থাকে, তবে compiler error-গুলো আমাদের code-এর অংশ এবং constraint-গুলোকে আরও নির্ভুলভাবে নির্দেশ করতে পারে। যদি এর বদলে Rust compiler lifetime-গুলোর সম্পর্ক কী হওয়া উচিত সে সম্পর্কে আরও বেশি inference করতো, তাহলে compiler হয়তো সমস্যার কারণ থেকে অনেক ধাপ দূরে আমাদের code-এর ব্যবহার নির্দেশ করতে পারতো।

যখন আমরা `longest`-এ concrete reference পাস করি, তখন `'a`-এর জায়গায় বসে এমন concrete lifetime হলো `x`-এর scope-এর সেই অংশ যা `y`-এর scope-এর সাথে overlap করে। অন্য কথায়, generic lifetime `'a` সেই concrete lifetime পাবে যা `x` ও `y`-এর lifetime-গুলোর মধ্যে ছোটটির সমান। যেহেতু আমরা return করা reference-কে একই lifetime parameter `'a` দিয়ে annotate করেছি, তাই return করা reference-টিও `x` ও `y`-এর lifetime-গুলোর ছোটটির সময়কাল পর্যন্ত valid থাকবে।

চলো দেখি ভিন্ন concrete lifetime সহ reference পাস করে lifetime annotation-গুলো কীভাবে `longest` function-কে সীমাবদ্ধ করে। Listing 10-22 একটি সরল উদাহরণ।

<Listing number="10-22" file-name="src/main.rs" caption="Using the `longest` function with references to `String` values that have different concrete lifetimes">

```rust
fn main() {
    let string1 = String::from("long string is long");

    {
        let string2 = String::from("xyz");
        let result = longest(string1.as_str(), string2.as_str());
        println!("The longest string is {result}");
    }
}
```

</Listing>

এই উদাহরণে, `string1` outer scope-এর শেষ পর্যন্ত valid, `string2` inner scope-এর শেষ পর্যন্ত valid, এবং `result` এমন কিছুকে refer করে যা inner scope-এর শেষ পর্যন্ত valid। এই code টি চালাও এবং দেখবে borrow checker এটি approve করে; এটি compile হবে এবং `The longest string is long string is long` print করবে।

এরপর, চলো এমন একটি উদাহরণ দেখি যা দেখায় যে `result`-এর reference-এর lifetime অবশ্যই দুটি argument-এর ছোট lifetime-টি হতে হবে। আমরা `result` variable-এর declaration-কে inner scope-এর বাইরে নিয়ে যাবো কিন্তু `result` variable-কে value assign করাটা `string2` সহ scope-এর ভেতরে রাখবো। তারপর, আমরা `result` ব্যবহার করে এমন `println!`-কে inner scope-এর বাইরে, inner scope শেষ হওয়ার পরে সরিয়ে নেবো। Listing 10-23-এর code টি compile হবে না।

<Listing number="10-23" file-name="src/main.rs" caption="Attempting to use `result` after `string2` has gone out of scope">

```rust,ignore,does_not_compile
fn main() {
    let string1 = String::from("long string is long");
    let result;
    {
        let string2 = String::from("xyz");
        result = longest(string1.as_str(), string2.as_str());
    }
    println!("The longest string is {result}");
}
```

</Listing>

যখন আমরা এই code টি compile করার চেষ্টা করি, আমরা এই error টি পাই:

```console
$ cargo run
   Compiling chapter10 v0.1.0 (file:///projects/chapter10)
error[E0597]: `string2` does not live long enough
 --> src/main.rs:6:44
  |
5 |         let string2 = String::from("xyz");
  |             ------- binding `string2` declared here
6 |         result = longest(string1.as_str(), string2.as_str());
  |                                            ^^^^^^^ borrowed value does not live long enough
7 |     }
  |     - `string2` dropped here while still borrowed
8 |     println!("The longest string is {result}");
  |                                      ------ borrow later used here

For more information about this error, try `rustc --explain E0597`.
error: could not compile `chapter10` (bin "chapter10") due to 1 previous error
```

Error-টি দেখায় যে `result`-এর জন্য `println!` statement-এ valid হতে হলে, `string2`-কে outer scope-এর শেষ পর্যন্ত valid থাকতে হবে। Rust এটি জানে কারণ আমরা একই lifetime parameter `'a` দিয়ে function parameter ও return value-এর lifetime annotate করেছি।

মানুষ হিসেবে, আমরা এই code টিতে দেখতে পারি যে `string1`, `string2`-এর চেয়ে দীর্ঘ, এবং তাই `result`-এ `string1`-এর একটি reference থাকবে। যেহেতু `string1` এখনও scope-এর বাইরে যায়নি, তাই `string1`-এর একটি reference `println!` statement-এর জন্য এখনও valid থাকবে। কিন্তু compiler এই ক্ষেত্রে reference-টি valid তা দেখতে পারে না। আমরা Rust-কে বলেছি যে `longest` function দ্বারা return করা reference-এর lifetime পাস করা reference-গুলোর lifetime-গুলোর ছোটটির সমান। তাই, borrow checker Listing 10-23-এর code-টিকে সম্ভবত invalid reference থাকতে পারে এমন হিসেবে disallow করে।

আরও experiment design করে দেখো যেখানে `longest` function-এ পাস করা reference-গুলোর value ও lifetime-গুলো এবং return করা reference-টি কীভাবে ব্যবহৃত হয় সেগুলো পরিবর্তন করা হবে। Compile করার আগে তোমার experiment-গুলো borrow checker পাস করবে কিনা সে সম্পর্কে hypothesis তৈরি করো; তারপর check করো তুমি ঠিক বলেছো কিনা!

<!-- Old headings. Do not remove or links may break. -->

<a id="thinking-in-terms-of-lifetimes"></a>

### Relationships

তোমার lifetime parameter কীভাবে specify করতে হবে তা নির্ভর করে তোমার function কী করছে তার উপর। উদাহরণস্বরূপ, যদি আমরা `longest` function-এর implementation পরিবর্তন করে দীর্ঘতম string slice-এর বদলে সবসময় প্রথম parameter-টি return করি, তবে আমাদের `y` parameter-এ lifetime specify করার প্রয়োজন হবে না। নিচের code টি compile হবে:

<Listing file-name="src/main.rs">

```rust
fn longest<'a>(x: &'a str, y: &str) -> &'a str {
    x
}
```

</Listing>

আমরা `x` parameter এবং return type-এর জন্য একটি lifetime parameter `'a` specify করেছি, কিন্তু `y` parameter-এর জন্য নয়, কারণ `y`-এর lifetime-এর `x` বা return value-এর lifetime-এর সাথে কোনো সম্পর্ক নেই।

কোনো function থেকে reference return করার সময়, return type-এর জন্য lifetime parameter-টি হবে parameter-গুলোর মধ্যে কোনো একটির lifetime parameter-এর সাথে মিলতে হবে। যদি return করা reference কোনো parameter-কে refer _না_ করে, তবে এটি অবশ্যই এই function-এর ভেতরে তৈরি করা কোনো value-কে refer করবে। তবে এটি একটি dangling reference হবে কারণ value-টি function-এর শেষে scope-এর বাইরে চলে যাবে। `longest` function-এর এই attempted implementation-টি বিবেচনা করো যা compile হবে না:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
fn longest<'a>(x: &str, y: &str) -> &'a str {
    let result = String::from("really long string");
    result.as_str()
}
```

</Listing>

এখানে, যদিও আমরা return type-এর জন্য একটি lifetime parameter `'a` specify করেছি, এই implementation compile হতে ব্যর্থ হবে কারণ return value-এর lifetime parameter-গুলোর lifetime-এর সাথে আদৌ কোনোভাবে সম্পর্কিত নয়। এখানে আমরা যে error message টি পাই:

```console
$ cargo run
   Compiling chapter10 v0.1.0 (file:///projects/chapter10)
error[E0515]: cannot return value referencing local variable `result`
  --> src/main.rs:11:5
   |
11 |     result.as_str()
   |     ------^^^^^^^^^
   |     |
   |     returns a value referencing data owned by the current function
   |     `result` is borrowed here

For more information about this error, try `rustc --explain E0515`.
error: could not compile `chapter10` (bin "chapter10") due to 1 previous error
```

সমস্যাটি হলো `result` `longest` function-এর শেষে scope-এর বাইরে চলে যায় এবং clean up হয়। আমরা আবার function থেকে `result`-এর একটি reference return করার চেষ্টা করছি। এমন কোনো lifetime parameter specify করার উপায় নেই যা dangling reference-টি পরিবর্তন করবে, এবং Rust আমাদের একটি dangling reference তৈরি করতে দেবে না। এই ক্ষেত্রে, সবচেয়ে ভালো সমাধান হবে একটি reference-এর বদলে একটি owned data type return করা, যাতে calling function-টি তারপর সেই value clean up করার দায়িত্ব পালন করে।

পরিশেষে, lifetime syntax হলো function-গুলোর বিভিন্ন parameter এবং return value-এর lifetime-গুলোকে সংযুক্ত করা। একবার সেগুলো সংযুক্ত হলে, Rust-এর কাছে memory-safe operation allow করা এবং dangling pointer তৈরি করবে বা অন্যথায় memory safety ভঙ্গ করবে এমন operation disallow করার জন্য যথেষ্ট তথ্য থাকে।

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-struct-definitions"></a>

### In Struct Definitions

এখন পর্যন্ত, আমরা যেসব struct define করেছি সবগুলোই owned type ধারণ করে। আমরা reference ধারণ করতে struct-ও define করতে পারি, কিন্তু সেই ক্ষেত্রে আমাদের struct-এর definition-এ প্রতিটি reference-এ একটি lifetime annotation যোগ করতে হবে। Listing 10-24-তে একটি `ImportantExcerpt` নামের struct আছে যা একটি string slice ধারণ করে।

<Listing number="10-24" file-name="src/main.rs" caption="A struct that holds a reference, requiring a lifetime annotation">

```rust
struct ImportantExcerpt<'a> {
    part: &'a str,
}

fn main() {
    let novel = String::from("Call me Ishmael. Some years ago...");
    let first_sentence = novel.split('.').next().unwrap();
    let i = ImportantExcerpt {
        part: first_sentence,
    };
}
```

</Listing>

এই struct-এর single field `part` একটি string slice ধারণ করে, যা একটি reference। Generic data type-এর মতোই, আমরা struct definition-এর body-তে lifetime parameter ব্যবহার করতে পারি সেজন্য struct-এর নামের পরে angle bracket-এর ভেতর generic lifetime parameter-এর নাম declare করি। এই annotation-টির মানে হলো `ImportantExcerpt`-এর একটি instance তার `part` field-এ যে reference ধারণ করে তার চেয়ে বেশি সময় বাঁচবে না।

এখানে `main` function-টি `ImportantExcerpt` struct-এর একটি instance তৈরি করে যা `novel` variable-এর owned `String`-এর প্রথম বাক্যের একটি reference ধারণ করে। `novel`-এর data `ImportantExcerpt` instance তৈরি হওয়ার আগেই বিদ্যমান। এছাড়াও, `novel` `ImportantExcerpt` scope-এর বাইরে যাওয়ার পরে নিজেই scope-এর বাইরে যায়, তাই `ImportantExcerpt` instance-এর reference-টি valid।

### Lifetime Elision

তুমি শিখেছো যে প্রতিটি reference-এর একটি lifetime আছে এবং reference ব্যবহার করে এমন function বা struct-এর জন্য lifetime parameter specify করতে হয়। কিন্তু আমাদের Listing 4-9-তে একটি function ছিল, যা আবার Listing 10-25-তে দেখানো হয়েছে, যা lifetime annotation ছাড়াই compile হয়েছিল।

<Listing number="10-25" file-name="src/lib.rs" caption="A function we defined in Listing 4-9 that compiled without lifetime annotations, even though the parameter and return type are references">

```rust
fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }

    &s[..]
}
```

</Listing>

এই function-টি lifetime annotation ছাড়াই কেন compile হয় তার কারণ ঐতিহাসিক: Rust-এর early version-গুলোতে (pre-1.0), এই code টি compile হতো না, কারণ প্রতিটি reference-এর জন্য একটি explicit lifetime প্রয়োজন ছিল। সেই সময়ে, function signature-টি এভাবে লেখা হতো:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

প্রচুর Rust code লেখার পর, Rust team আবিষ্কার করলো যে Rust programmer-রা নির্দিষ্ট পরিস্থিতিতে বারবার একই lifetime annotation লিখছে। এই পরিস্থিতিগুলো predictable ছিল এবং কয়েকটি deterministic pattern অনুসরণ করতো। Developer-রা এই pattern-গুলোকে compiler-এর code-এ program করেছিল যাতে borrow checker এই পরিস্থিতিতে lifetime infer করতে পারে এবং explicit annotation-এর প্রয়োজন না হয়।

Rust history-র এই অংশটি প্রাসঙ্গিক কারণ ভবিষ্যতে আরও deterministic pattern আবির্ভূত হয়ে compiler-এ যোগ হওয়া সম্ভব। ভবিষ্যতে, আরও কম lifetime annotation-এর প্রয়োজন হতে পারে।

Rust-এর reference analysis-এ program করা pattern-গুলোকে _lifetime elision rule_ বলা হয়। এগুলো programmer-দের অনুসরণ করার নিয়ম নয়; এগুলো এমন কিছু particular case যা compiler বিবেচনা করবে, এবং তোমার code যদি এই case-গুলোর সাথে মিলে যায়, তবে তোমার lifetime explicitly লেখার প্রয়োজন নেই।

Elision rule-গুলো পূর্ণ inference দেয় না। Rust rule-গুলো apply করার পরও যদি reference-গুলোর lifetime কী হবে তা নিয়ে কোনো ambiguity থাকে, তবে compiler বাকি reference-গুলোর lifetime কী হওয়া উচিত তা guess করবে না। Guess করার বদলে, compiler তোমাকে এমন একটি error দেবে যা তুমি lifetime annotation যোগ করে resolve করতে পারবে।

Function বা method parameter-এর lifetime-কে _input lifetime_ বলা হয়, এবং return value-এর lifetime-কে _output lifetime_ বলা হয়।

Compiler যখন explicit annotation নেই, তখন reference-গুলোর lifetime বের করতে তিনটি rule ব্যবহার করে। প্রথম rule-টি input lifetime-এর ক্ষেত্রে প্রযোজ্য, এবং দ্বিতীয় ও তৃতীয় rule-টি output lifetime-এর ক্ষেত্রে প্রযোজ্য। Compiler যদি তিনটি rule-এর শেষে পৌঁছানোর পরেও এমন কোনো reference থাকে যার lifetime সে বের করতে পারে না, তবে compiler একটি error দিয়ে থেমে যাবে। এই rule-গুলো `fn` definition এবং `impl` block-এর ক্ষেত্রেও প্রযোজ্য।

প্রথম rule-টি হলো compiler যে প্রতিটি parameter reference সেই প্রতিটি parameter-কে একটি lifetime parameter assign করে। অন্য কথায়, একটি parameter সহ একটি function একটি lifetime parameter পায়: `fn foo<'a>(x: &'a i32)`; দুটি parameter সহ একটি function দুটি আলাদা lifetime parameter পায়: `fn foo<'a, 'b>(x: &'a i32, y: &'b i32)`; এবং এভাবেই চলতে থাকে।

দ্বিতীয় rule-টি হলো, যদি ঠিক একটি input lifetime parameter থাকে, তবে সেই lifetime-টি সব output lifetime parameter-এ assign করা হয়: `fn foo<'a>(x: &'a i32) -> &'a i32`।

তৃতীয় rule-টি হলো, যদি একাধিক input lifetime parameter থাকে, কিন্তু তার মধ্যে একটি `&self` বা `&mut self` হয় কারণ এটি একটি method, তবে `self`-এর lifetime-টি সব output lifetime parameter-এ assign করা হয়। এই তৃতীয় rule-টি method-গুলোকে পড়তে এবং লিখতে আরও সহজ করে তোলে কারণ কম symbol প্রয়োজন হয়।

চলো আমরা নিজেদেরকে compiler ভাবি। আমরা এই rule-গুলো apply করে Listing 10-25-এর `first_word` function-এর signature-এর reference-গুলোর lifetime বের করবো। Signature-টি শুরুতে কোনো lifetime ছাড়াই শুরু হয়:

```rust,ignore
fn first_word(s: &str) -> &str {
```

তারপর, compiler প্রথম rule-টি apply করে, যা specify করে যে প্রতিটি parameter নিজস্ব lifetime পায়। আমরা এটিকে স্বাভাবিকভাবে `'a` বলবো, তাই এখন signature-টি এমন:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &str {
```

দ্বিতীয় rule-টি apply হয় কারণ ঠিক একটি input lifetime আছে। দ্বিতীয় rule-টি specify করে যে একটি input parameter-এর lifetime output lifetime-এ assign করা হয়, তাই signature-টি এখন এমন:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

এখন এই function signature-এ সব reference-এর lifetime আছে, এবং compiler এই function signature-এ lifetime annotate করার প্রয়োজন ছাড়াই তার analysis চালিয়ে যেতে পারে।

চলো আরেকটি উদাহরণ দেখি, এবার সেই `longest` function ব্যবহার করে যার সাথে আমরা Listing 10-20-তে কাজ শুরু করার সময় কোনো lifetime parameter ছিল না:

```rust,ignore
fn longest(x: &str, y: &str) -> &str {
```

চলো প্রথম rule-টি apply করি: প্রতিটি parameter নিজস্ব lifetime পায়। এবার আমাদের একটির বদলে দুটি parameter আছে, তাই আমাদের দুটি lifetime আছে:

```rust,ignore
fn longest<'a, 'b>(x: &'a str, y: &'b str) -> &str {
```

তুমি দেখতে পাচ্ছো যে দ্বিতীয় rule-টি apply হয় না, কারণ একাধিক input lifetime আছে। তৃতীয় rule-টিও apply হয় না, কারণ `longest` একটি method নয়, একটি function, তাই parameter-গুলোর কোনোটিই `self` নয়। তিনটি rule-ই কাজ করার পরও, আমরা এখনও return type-এর lifetime কী হবে তা বের করতে পারিনি। এটিই কারণ যে Listing 10-20-তে code compile করার চেষ্টা করলে আমরা error পেয়েছি: Compiler lifetime elision rule-গুলো কাজ করেছে কিন্তু signature-এর সব reference-এর lifetime এখনও বের করতে পারেনি।

যেহেতু তৃতীয় rule-টি আসলে শুধু method signature-এ apply হয়, তাই চলো এবার সেই context-এ lifetime দেখি যেন বোঝা যায় তৃতীয় rule-টির অর্থ কী যে কারণে আমাদের method signature-এ খুব বেশি lifetime annotate করতে হয় না।

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-method-definitions"></a>

### In Method Definitions

আমরা যখন lifetime সহ একটি struct-এর উপর method implement করি, তখন আমরা Listing 10-11-এ দেখানো generic type parameter-এর মতো একই syntax ব্যবহার করি। আমরা কোথায় lifetime parameter declare এবং ব্যবহার করবো তা নির্ভর করে সেগুলো struct field-এর সাথে সম্পর্কিত নাকি method parameter ও return value-এর সাথে তার উপর।

Struct field-এর জন্য lifetime name সবসময় `impl` keyword-এর পরে declare করতে হবে এবং তারপর struct-এর নামের পরে ব্যবহার করতে হবে, কারণ সেই lifetime-গুলো struct-এর type-এর অংশ।

`impl` block-এর ভেতরের method signature-এ, reference-গুলো struct-এর field-গুলোর reference-এর lifetime-এর সাথে যুক্ত থাকতে পারে, অথবা সেগুলো independent হতে পারে। এছাড়াও, lifetime elision rule-গুলো প্রায়শই এমনভাবে কাজ করে যে method signature-এ lifetime annotation-এর প্রয়োজন হয় না। চলো Listing 10-24-তে আমরা যে `ImportantExcerpt` নামের struct define করেছি তা ব্যবহার করে কিছু উদাহরণ দেখি।

প্রথমে, আমরা `level` নামের একটি method ব্যবহার করবো যার একমাত্র parameter হলো `self`-এর একটি reference এবং যার return value একটি `i32`, যা কোনো কিছুর reference নয়:

```rust
impl<'a> ImportantExcerpt<'a> {
    fn level(&self) -> i32 {
        3
    }
}
```

`impl`-এর পরে lifetime parameter declaration এবং type name-এর পরে এর ব্যবহার আবশ্যক, কিন্তু প্রথম elision rule-এর কারণে আমাদের `self`-এর reference-এর lifetime annotate করার প্রয়োজন নেই।

এখানে এমন একটি উদাহরণ দেওয়া হলো যেখানে তৃতীয় lifetime elision rule-টি apply হয়:

```rust
impl<'a> ImportantExcerpt<'a> {
    fn announce_and_return_part(&self, announcement: &str) -> &str {
        println!("Attention please: {announcement}");
        self.part
    }
}
```

এখানে দুটি input lifetime আছে, তাই Rust প্রথম lifetime elision rule apply করে এবং `&self` ও `announcement` উভয়কেই তাদের নিজস্ব lifetime দেয়। তারপর, যেহেতু parameter-গুলোর মধ্যে একটি `&self`, তাই return type `&self`-এর lifetime পায়, এবং সব lifetime-ই হিসাব হয়ে যায়।

### The Static Lifetime

আমরা আলোচনা করতে চাই এমন একটি special lifetime হলো `'static`, যা নির্দেশ করে যে প্রভাবিত reference-টি প্রোগ্রামের সম্পূর্ণ সময়কাল ধরে বাঁচতে _পারে_। সব string literal-এরই `'static` lifetime আছে, যা আমরা নিচের মতো annotate করতে পারি:

```rust
let s: &'static str = "I have a static lifetime.";
```

এই string-এর text সরাসরি প্রোগ্রামের binary-তে সংরক্ষিত থাকে, যা সবসময় available থাকে। তাই সব string literal-এর lifetime-ই `'static`।

তুমি হয়তো error message-এ `'static` lifetime ব্যবহার করার পরামর্শ দেখতে পাবে। কিন্তু একটি reference-এর জন্য lifetime হিসেবে `'static` specify করার আগে ভাবো তোমার কাছে থাকা reference-টি আসলেই প্রোগ্রামের সম্পূর্ণ সময়কাল ধরে বাঁচে কিনা, এবং তুমি কি চাও সেটি বাঁচুক। বেশিরভাগ ক্ষেত্রে, `'static` lifetime suggest করা একটি error message একটি dangling reference তৈরি করার চেষ্টা অথবা available lifetime-গুলোর mismatch থেকে উৎপন্ন হয়। সেসব ক্ষেত্রে, সমাধান হলো সেই সমস্যাগুলো fix করা, `'static` lifetime specify করা নয়।

<!-- Old headings. Do not remove or links may break. -->

<a id="generic-type-parameters-trait-bounds-and-lifetimes-together"></a>

## Generic Type Parameters, Trait Bounds, এবং Lifetimes

চলো সংক্ষেপে দেখি একটি function-এ একসাথে generic type parameter, trait bound, এবং lifetime specify করার syntax!

```rust
use std::fmt::Display;

fn longest_with_an_announcement<'a, T>(
    x: &'a str,
    y: &'a str,
    ann: T,
) -> &'a str
where
    T: Display,
{
    println!("Announcement! {ann}");
    if x.len() > y.len() { x } else { y }
}
```

এটি Listing 10-21-এর সেই `longest` function, যা দুটি string slice-এর মধ্যে দীর্ঘতমটি return করে। কিন্তু এখন এতে `T` generic type-এর একটি অতিরিক্ত parameter আছে যার নাম `ann`, যা `where` clause দ্বারা specify করা অনুযায়ী `Display` trait implement করে এমন যেকোনো type দ্বারা পূরণ করা যেতে পারে। এই অতিরিক্ত parameter-টি `{}` দিয়ে print করা হবে, যে কারণে `Display` trait bound প্রয়োজনীয়। যেহেতু lifetimes এক ধরনের generic, তাই lifetime parameter `'a` এবং generic type parameter `T`-র declaration একই angle bracket-এর ভেতরে function-এর নামের পরে একই list-এ থাকে।

## Summary

এই chapter-টিতে আমরা অনেক কিছু cover করেছি! এখন যেহেতু তুমি generic type parameter, trait ও trait bound, এবং generic lifetime parameter সম্পর্কে জানো, তুমি পুনরাবৃত্তি ছাড়াই code লেখার জন্য প্রস্তুত যা অনেক ভিন্ন ভিন্ন পরিস্থিতিতে কাজ করবে। Generic type parameter তোমাকে ভিন্ন ভিন্ন type-এ code apply করতে দেয়। Trait এবং trait bound নিশ্চিত করে যে type-গুলো generic হলেও, সেগুলোর মধ্যে code-এর প্রয়োজনীয় behavior থাকবে। তুমি শিখেছো কীভাবে lifetime annotation ব্যবহার করে নিশ্চিত করতে হয় যে এই flexible code-এ কোনো dangling reference থাকবে না। আর এই সম্পূর্ণ analysis টাই compile time-এ ঘটে, যা runtime performance-কে প্রভাবিত করে না!

বিশ্বাস করো বা না করো, এই chapter-এ আলোচনা করা topic-গুলোর উপর আরও অনেক কিছু শেখার আছে: Chapter 18 trait object নিয়ে আলোচনা করে, যা trait ব্যবহার করার আরেকটি উপায়। এছাড়াও lifetime annotation সম্পর্কিত আরও জটিল পরিস্থিতি আছে যা তুমি শুধুমাত্র অত্যন্ত advanced পরিস্থিতিতে প্রয়োজন করবে; সেগুলোর জন্য তোমার [Rust Reference][reference] পড়া উচিত। কিন্তু এরপরে, তুমি শিখবে কীভাবে Rust-এ test লিখতে হয় যাতে তোমার code যেমন কাজ করা উচিত ঠিক তেমনই কাজ করছে তা নিশ্চিত করতে পারো।

[references-and-borrowing]: ch04-02-references-and-borrowing.html#references-and-borrowing
[string-slices-as-parameters]: ch04-03-slices.html#string-slices-as-parameters
[reference]: ../reference/trait-bounds.html

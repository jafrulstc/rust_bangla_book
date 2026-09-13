## References এবং Borrowing

Listing 4-5-এর tuple code-এর সমস্যা হলো, আমাদের `String`-টি calling function-এ ফেরত দিতে হয় যাতে `calculate_length`-কে কল করার পরেও আমরা সেই `String` ব্যবহার করতে পারি, কারণ `String`-টি `calculate_length`-এ move হয়ে গিয়েছিল। এর বদলে আমরা `String` value-টির একটি reference দিতে পারি। Reference একটি pointer-এর মতো, এটি এমন একটি address যা আমরা অনুসরণ করে সেই address-এ সংরক্ষিত data-তে access করতে পারি; কিন্তু সেই data-এর owner হলো অন্য কোনো variable। Pointer-এর থেকে পার্থক্য হলো, reference গ্যারান্টি দেয় যে তার lifetime জুড়ে এটি একটি নির্দিষ্ট type-এর valid value-কেই নির্দেশ করবে।

নিচে দেখানো হলো কীভাবে তুমি এমন একটি `calculate_length` function define করবে ও ব্যবহার করবে যা parameter হিসেবে কোনো object-এর reference নেয়, value-এর ownership নেওয়ার বদলে:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let s1 = String::from("hello");

    let len = calculate_length(&s1);

    println!("The length of '{s1}' is {len}.");
}

fn calculate_length(s: &String) -> usize {
    s.len()
}
```

</Listing>

প্রথমে খেয়াল করো যে variable declaration ও function-এর return value-তে থাকা সব tuple code মুছে গেছে। দ্বিতীয়ত, খেয়াল করো যে আমরা `calculate_length`-এ `&s1` পাস করি, আর এর definition-এ আমরা `String`-এর বদলে `&String` নিই। এই ampersand চিহ্নগুলো reference নির্দেশ করে, এবং এগুলো তোমাকে ownership না নিয়েই কোনো value-কে refer করতে দেয়। Figure 4-6 এই concept-টি চিত্রিত করে।

<img alt="Three tables: the table for s contains only a pointer to the table
for s1. The table for s1 contains the stack data for s1 and points to the
string data on the heap." src="img/trpl04-06.svg" class="center" />

<span class="caption">Figure 4-6: A diagram of `&String` `s` pointing at
`String` `s1`</span>

> নোট: `&` ব্যবহার করে referencing-এর বিপরীত হলো _dereferencing_, যা dereference operator `*` দিয়ে করা হয়। আমরা Chapter 8-তে dereference operator-এর কিছু ব্যবহার দেখব এবং Chapter 15-তে dereferencing-এর বিস্তারিত আলোচনা করব।

চলো এখানকার function call-টি একটু কাছ থেকে দেখি:

```rust
    let s1 = String::from("hello");

    let len = calculate_length(&s1);
```

`&s1` syntax আমাদের এমন একটি reference তৈরি করতে দেয় যা `s1`-এর value-কে _refer_ করে কিন্তু তার owner হয় না। যেহেতু reference-টি owner নয়, তাই reference-টি ব্যবহার করা বন্ধ হয়ে গেলে এটি যে value-কে নির্দেশ করছিল তা drop হবে না।

একইভাবে, function-এর signature-এ `&` ব্যবহার করে নির্দেশ করা হয় যে parameter `s`-এর type একটি reference। চলো কিছু ব্যাখ্যামূলক annotation যোগ করি:

```rust
fn calculate_length(s: &String) -> usize { // s is a reference to a String
    s.len()
} // Here, s goes out of scope. But because s does not have ownership of what
  // it refers to, the String is not dropped.
```

Variable `s`-এর valid থাকার scope যেকোনো function parameter-এর scope-এর মতোই, কিন্তু reference যে value-কে নির্দেশ করে তা `s`-এর ব্যবহার শেষ হলে drop হয় না, কারণ `s`-এর ownership নেই। Function-গুলোর parameter হিসেবে আসল value-এর বদলে reference থাকলে, আমাদের ownership ফেরত দেওয়ার জন্য value গুলো return করতে হয় না, কারণ আমরা ownership-ই কখনো পাইনি।

কোনো reference তৈরি করার কাজটিকে আমরা _borrowing_ বলি। বাস্তব জীবনের মতোই, যদি কোনো ব্যক্তি কোনো জিনিসের owner হয়, তবে তুমি তার কাছ থেকে সেটি borrow করতে পারো। কাজ শেষ হলে তোমাকে সেটি ফেরত দিতে হয়। তুমি সেটির owner নও।

তাহলে, আমরা যা borrow করছি তা পরিবর্তন করার চেষ্টা করলে কী হয়? Listing 4-6-এর code-টি চেষ্টা করো। Spoiler alert: এটা কাজ করবে না!

<Listing number="4-6" file-name="src/main.rs" caption="Attempting to modify a borrowed value">

```rust,ignore,does_not_compile
fn main() {
    let s = String::from("hello");

    change(&s);
}

fn change(some_string: &String) {
    some_string.push_str(", world");
}
```

</Listing>

এখানে error দেখো:

```console
$ cargo run
   Compiling ownership v0.1.0 (file:///projects/ownership)
error[E0596]: cannot borrow `*some_string` as mutable, as it is behind a `&` reference
 --> src/main.rs:8:5
  |
8 |     some_string.push_str(", world");
  |     ^^^^^^^^^^^ `some_string` is a `&` reference, so it cannot be borrowed as mutable
  |
help: consider changing this to be a mutable reference
  |
7 | fn change(some_string: &mut String) {
  |                         +++

For more information about this error, try `rustc --explain E0596`.
error: could not compile `ownership` (bin "ownership") due to 1 previous error
```

ঠিক যেমন variable গুলো default হিসেবে immutable হয়, reference-গুলোও তাই। আমরা যে জিনিসের reference আছে তা পরিবর্তন করতে পারি না।

### Mutable Reference

আমরা Listing 4-6-এর code-টি ঠিক করে borrow করা value পরিবর্তন করতে পারি—পরিবর্তে _mutable reference_ ব্যবহার করে কয়েকটি ছোট পরিবর্তন করলেই হবে:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let mut s = String::from("hello");

    change(&mut s);
}

fn change(some_string: &mut String) {
    some_string.push_str(", world");
}
```

</Listing>

প্রথমে আমরা `s`-কে `mut` করে দিই। তারপর `change` function-কে যেখানে কল করি সেখানে `&mut s` দিয়ে একটি mutable reference তৈরি করি এবং function signature আপডেট করে `some_string: &mut String` দিয়ে mutable reference গ্রহণ করি। এতে খুব পরিষ্কার বোঝানো হয় যে `change` function যে value borrow করবে তা mutate করবে।

Mutable reference-এর একটি বড় সীমাবদ্ধতা আছে: তোমার যদি কোনো value-এর একটি mutable reference থাকে, তবে সেই value-এর আর কোনো reference থাকতে পারবে না। নিচের code-টি যা `s`-এর দুটি mutable reference তৈরি করার চেষ্টা করে, তা fail করবে:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
    let mut s = String::from("hello");

    let r1 = &mut s;
    let r2 = &mut s;

    println!("{r1}, {r2}");
```

</Listing>

এখানে error দেখো:

```console
$ cargo run
   Compiling ownership v0.1.0 (file:///projects/ownership)
error[E0499]: cannot borrow `s` as mutable more than once at a time
 --> src/main.rs:5:14
  |
4 |     let r1 = &mut s;
  |              ------ first mutable borrow occurs here
5 |     let r2 = &mut s;
  |              ^^^^^^ second mutable borrow occurs here
6 |
7 |     println!("{r1}, {r2}");
  |                -- first borrow later used here

For more information about this error, try `rustc --explain E0499`.
error: could not compile `ownership` (bin "ownership") due to 1 previous error
```

এই error-টি বলছে যে এই code-টি invalid, কারণ আমরা একই সময়ে `s`-কে একের বেশি বার mutable হিসেবে borrow করতে পারি না। প্রথম mutable borrow টি `r1`-এ আছে এবং এটিকে `println!`-এ ব্যবহার না হওয়া পর্যন্ত টিকে থাকতে হবে, কিন্তু সেই mutable reference তৈরি এবং তার ব্যবহারের মধ্যেই আমরা `r2`-তে আরেকটি mutable reference তৈরি করার চেষ্টা করেছি যা `r1`-এর মতো একই data borrow করে।

একই data-এর একই সময়ে একাধিক mutable reference থাকতে না দেওয়ার এই সীমাবদ্ধতা mutation কে অনুমোদন দেয় কিন্তু অনেক নিয়ন্ত্রিতভাবে। নতুন Rustacean-দের এটা নিয়ে বেশ ঝামেলা পোহাতে হয়, কারণ বেশিরভাগ ভাষা তোমাকে যখন খুশি mutate করতে দেয়। এই সীমাবদ্ধতার সুবিধা হলো Rust compile time-এই data race প্রতিরোধ করতে পারে। _Data race_ হলো race condition-এর মতোই, এবং এটি ঘটে যখন এই তিনটি আচরণ একসাথে ঘটে:

- দুটি বা তার বেশি pointer একই সময়ে একই data access করে।
- অন্তত একটি pointer data-তে write করতে ব্যবহৃত হচ্ছে।
- Data access synchronize করার জন্য কোনো mechanism ব্যবহৃত হচ্ছে না।

Data race undefined behavior তৈরি করে এবং runtime-এ সেগুলো খুঁজে বের করে ঠিক করা কঠিন; Rust এই সমস্যা প্রতিরোধ করে data race সহ code compile করতেই অস্বীকার করে!

যথারীতি, আমরা curly bracket ব্যবহার করে একটি নতুন scope তৈরি করতে পারি, যা একাধিক mutable reference-কে অনুমোদন দেয়, শুধু _একই সময়ে_ নয়:

```rust
    let mut s = String::from("hello");

    {
        let r1 = &mut s;
    } // r1 goes out of scope here, so we can make a new reference with no problems.

    let r2 = &mut s;
```

Rust mutable এবং immutable reference-কে একসাথে মেশানোর ক্ষেত্রেও অনুরূপ একটি নিয়ম প্রয়োগ করে। নিচের code-টি error ঘটায়:

```rust,ignore,does_not_compile
    let mut s = String::from("hello");

    let r1 = &s; // no problem
    let r2 = &s; // no problem
    let r3 = &mut s; // BIG PROBLEM

    println!("{r1}, {r2}, and {r3}");
```

এখানে error দেখো:

```console
$ cargo run
   Compiling ownership v0.1.0 (file:///projects/ownership)
error[E0502]: cannot borrow `s` as mutable because it is also borrowed as immutable
 --> src/main.rs:6:14
  |
4 |     let r1 = &s; // no problem
  |              -- immutable borrow occurs here
5 |     let r2 = &s; // no problem
6 |     let r3 = &mut s; // BIG PROBLEM
  |              ^^^^^^ mutable borrow occurs here
7 |
8 |     println!("{r1}, {r2}, and {r3}");
  |                -- immutable borrow later used here

For more information about this error, try `rustc --explain E0502`.
error: could not compile `ownership` (bin "ownership") due to 1 previous error
```

ফুহ! একই value-তে immutable reference থাকা অবস্থায় আমরা _একই সাথে_ mutable reference-ও রাখতে পারি না।

Immutable reference-এর ব্যবহারকারীরা আশা করে না যে value-টি হঠাৎ তাদের নাকের ডগায় পরিবর্তিত হয়ে যাবে! তবে একাধিক immutable reference অনুমোদিত, কারণ যারা শুধু data পড়ছে তাদের কেউই অন্য কারও data পড়ার ক্ষমতাকে প্রভাবিত করতে পারে না।

খেয়াল করো যে একটি reference-এর scope শুরু হয় যেখানে সেটি প্রথম পরিচিত হয় এবং চলতে থাকে সেই reference-টির শেষ ব্যবহার পর্যন্ত। যেমন, নিচের code-টি compile হবে, কারণ immutable reference-গুলোর শেষ ব্যবহর হয় `println!`-এ, mutable reference পরিচিত হওয়ার আগেই:

```rust
    let mut s = String::from("hello");

    let r1 = &s; // no problem
    let r2 = &s; // no problem
    println!("{r1} and {r2}");
    // Variables r1 and r2 will not be used after this point.

    let r3 = &mut s; // no problem
    println!("{r3}");
```

Immutable reference `r1` এবং `r2`-এর scope শেষ হয় সেই `println!`-এর পরে যেখানে সেগুলো সর্বশেষ ব্যবহৃত হয়েছে, যা mutable reference `r3` তৈরির আগে। এই scope-গুলো overlapping নয়, তাই এই code-টি অনুমোদিত: Compiler বুঝতে পারে যে scope-এর শেষের আগেই কোনো এক মুহূর্তে reference আর ব্যবহৃত হচ্ছে না।

যদিও borrowing error গুলো মাঝে মাঝে বিরক্তিকর, মনে রেখো যে এটি Rust compiler একটি সম্ভাব্য bug শীঘ্রই (compile time-এ, runtime-এ নয়) ধরিয়ে দিচ্ছে এবং তোমাকে ঠিক কোথায় সমস্যা তা দেখাচ্ছে। ফলে তোমার data যে তুমি যা ভাবছো তা নয়—এটা খুঁজে বের করতে হয় না।

### Dangling Reference

Pointer সহ ভাষাগুলোতে ভুলবশত _dangling pointer_—এমন একটি pointer যা memory-তে এমন কোনো জায়গা refer করে যা হয়তো অন্য কাউকে দেওয়া হয়ে গেছে—তৈরি করা সহজ, শুধু কোনো memory free করে তার pointer সেভ রাখলেই হয়। Rust-এ এর বিপরীত, compiler গ্যারান্টি দেয় যে reference কখনো dangling reference হবে না: তোমার যদি কোনো data-এর reference থাকে, compiler নিশ্চিত করবে যে data-টি reference-টির আগে scope-ের বাইরে যাবে না।

চলো একটি dangling reference তৈরি করার চেষ্টা করি, দেখি Rust কীভাবে সেগুলোকে compile-time error-এ প্রতিহত করে:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
fn main() {
    let reference_to_nothing = dangle();
}

fn dangle() -> &String {
    let s = String::from("hello");

    &s
}
```

</Listing>

এখানে error দেখো:

```console
$ cargo run
   Compiling ownership v0.1.0 (file:///projects/ownership)
error[E0106]: missing lifetime specifier
 --> src/main.rs:5:16
  |
5 | fn dangle() -> &String {
  |                ^ expected named lifetime parameter
  |
  = help: this function's return type contains a borrowed value, but there is no value for it to be borrowed from
help: consider using the `'static` lifetime, but this is uncommon unless you're returning a borrowed value from a `const` or a `static`
  |
5 | fn dangle() -> &'static String {
  |                 +++++++
help: instead, you are more likely to want to return an owned value
  |
5 - fn dangle() -> &String {
5 + fn dangle() -> String {
  |

For more information about this error, try `rustc --explain E0106`.
error: could not compile `ownership` (bin "ownership") due to 1 previous error
```

এই error message-টি এমন একটি feature-এর কথা বলে যা আমরা এখনো cover করিনি: lifetime। Lifetime নিয়ে আমরা Chapter 10-তে বিস্তারিত আলোচনা করব। কিন্তু lifetime সম্পর্কিত অংশগুলো উপেক্ষা করলেও, message-টিতে এই code কেন সমস্যার কারণ তার মূল বিষয়টি আছে:

```text
this function's return type contains a borrowed value, but there is no value
for it to be borrowed from
```

চলো আমাদের `dangle` code-টির প্রতিটি ধাপে ঠিক কী ঘটছে তা একটু কাছ থেকে দেখি:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
fn dangle() -> &String { // dangle returns a reference to a String

    let s = String::from("hello"); // s is a new String

    &s // we return a reference to the String, s
} // Here, s goes out of scope and is dropped, so its memory goes away.
  // Danger!
```

</Listing>

যেহেতু `s` তৈরি হয়েছে `dangle`-এর ভেতরে, তাই `dangle`-এর code শেষ হলে `s`-এর memory deallocate হবে। কিন্তু আমরা তার একটি reference ফেরত দেওয়ার চেষ্টা করেছি। এর মানে এই reference টি একটি invalid `String`-কে নির্দেশ করবে। এটা চলবে না! Rust আমাদের এটা করতে দেবে না।

সমাধান হলো `String`-টিকে সরাসরি ফেরত দেওয়া:

```rust
fn no_dangle() -> String {
    let s = String::from("hello");

    s
}
```

এটি কোনো সমস্যা ছাড়াই কাজ করে। Ownership move হয়ে বাইরে চলে যায়, আর কিছু deallocate হয় না।

### Reference-এর নিয়ম

আমরা reference নিয়ে যা আলোচনা করেছি তার পুনরাবৃত্তি করি:

- যেকোনো সময়ে, তোমার কাছে হয় _একটি_ mutable reference থাকতে পারে, _অথবা_ যেকোনো সংখ্যক immutable reference থাকতে পারে।
- Reference সব সময় valid হতে হবে।

এবার চলো অন্য ধরনের একটি reference দেখি: slice।

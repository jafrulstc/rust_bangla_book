## Slice Type

_Slice_ তোমাকে একটি [collection](ch08-00-common-collections.md)<!-- ignore -->-এর contiguous element সিরিজকে reference করার সুযোগ দেয়। Slice এক ধরনের reference, তাই এর ownership নেই।

এখানে একটি ছোট programming সমস্যা দেওয়া হলো: এমন একটি function লেখো যা স্পেস দিয়ে আলাদা করা শব্দের একটি string নেয় এবং সেই string-এ যে প্রথম শব্দটি পায় তা ফেরত দেয়। Function-টি যদি string-এ কোনো স্পেস না খুঁজে পায়, তবে পুরো string-টিই একটি শব্দ হতে হবে, তাই পুরো string-টি ফেরত দেওয়া উচিত।

> নোট: Slice পরিচয় করানোর উদ্দেশ্যে, এই section-এ আমরা শুধু ASCII ধরে নিচ্ছি; UTF-8 হ্যান্ডলিং নিয়ে আরও বিস্তারিত আলোচনা Chapter 8-এর [“Storing UTF-8 Encoded Text with Strings”][strings]<!-- ignore --> section-এ আছে।

চলো দেখি এই function-টির signature slice ব্যবহার না করে কেমন হতে পারে, যাতে বুঝতে পারি slice আসলে কোন সমস্যার সমাধান করে:

```rust,ignore
fn first_word(s: &String) -> ?
```

`first_word` function-টির একটি parameter আছে যার type `&String`। আমাদের ownership দরকার নেই, তাই এটাই চলবে। (Idiomatic Rust-এ, function গুলো দরকার না হলে তাদের argument-এর ownership নেয় না, আর এর কারণ এগিয়ে গেলেই পরিষ্কার হবে।) কিন্তু আমরা কী ফেরত দেব? আমাদের কাছে একটি string-এর *অংশ* সম্পর্কে কথা বলার কোনো উপায় নেই। তবে আমরা একটি স্পেস দিয়ে চিহ্নিত শব্দের শেষ index ফেরত দিতে পারি। চলো সেটাই চেষ্টা করি, যেমন Listing 4-7-তে দেখানো হয়েছে।

<Listing number="4-7" file-name="src/main.rs" caption="The `first_word` function that returns a byte index value into the `String` parameter">

```rust
fn first_word(s: &String) -> usize {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return i;
        }
    }

    s.len()
}

fn main() {}
```

</Listing>

যেহেতু আমাদের `String`-টি element by element ঘুরে যেতে হবে এবং দেখতে হবে কোনো value স্পেস কি না, তাই আমরা `as_bytes` method ব্যবহার করে আমাদের `String`-টিকে byte-এর array-তে রূপান্তর করব।

```rust,ignore
    let bytes = s.as_bytes();
```

এরপর, আমরা `iter` method ব্যবহার করে byte-এর array-এর উপর একটি iterator তৈরি করি:

```rust,ignore
    for (i, &item) in bytes.iter().enumerate() {
```

Iterator নিয়ে আমরা [Chapter 13][ch13]<!-- ignore -->-তে আরও বিস্তারিত আলোচনা করব। আপাতত এটুকু জেনো যে `iter` এমন একটি method যা একটি collection-এর প্রতিটি element ফেরত দেয় এবং `enumerate`-এর কাজ হলো `iter`-এর ফলাফলকে wrap করে প্রতিটি element একটি tuple-এর অংশ হিসেবে ফেরত দেওয়া। `enumerate` থেকে ফেরত আসা tuple-টির প্রথম element টি হলো index, আর দ্বিতীয় element টি হলো সেই element-এর একটি reference। এটি আমাদের নিজেদের index হিসাব করার চেয়ে কিছুটা সুবিধাজনক।

যেহেতু `enumerate` method একটি tuple ফেরত দেয়, আমরা pattern ব্যবহার করে সেই tuple-টি destructure করতে পারি। Pattern নিয়ে আমরা [Chapter 6][ch6]<!-- ignore -->-তে আরও আলোচনা করব। `for` loop-এ আমরা এমন একটি pattern specify করি যাতে tuple-এর index-এর জন্য `i` এবং tuple-এর single byte-এর জন্য `&item` আছে। যেহেতু `.iter().enumerate()` থেকে আমরা element-এর একটি reference পাই, তাই pattern-এ আমরা `&` ব্যবহার করি।

`for` loop-এর ভেতরে আমরা byte literal syntax ব্যবহার করে স্পেস নির্দেশক byte-টি খুঁজি। স্পেস পেলে আমরা সেই অবস্থান ফেরত দিই। অন্যথায়, `s.len()` ব্যবহার করে আমরা string-এর length ফেরত দিই।

```rust,ignore
        if item == b' ' {
            return i;
        }
    }

    s.len()
```

এখন আমাদের string-এ প্রথম শব্দের শেষ index বের করার উপায় আছে, কিন্তু একটি সমস্যা আছে। আমরা একটি `usize` এককভাবে ফেরত দিচ্ছি, কিন্তু সেটি শুধু `&String`-এর context-এই একটি অর্থপূর্ণ সংখ্যা। অন্য কথায়, যেহেতু এটি `String` থেকে আলাদা একটি value, তাই এটি ভবিষ্যতেও valid থাকবে এমন কোনো গ্যারান্টি নেই। Listing 4-8-এর program-টি বিবেচনা করো যা Listing 4-7-এর `first_word` function-টি ব্যবহার করে।

<Listing number="4-8" file-name="src/main.rs" caption="Storing the result from calling the `first_word` function and then changing the `String` contents">

```rust
fn main() {
    let mut s = String::from("hello world");

    let word = first_word(&s); // word will get the value 5

    s.clear(); // this empties the String, making it equal to ""

    // word still has the value 5 here, but s no longer has any content that we
    // could meaningfully use with the value 5, so word is now totally invalid!
}
```

</Listing>

এই program-টি কোনো error ছাড়াই compile হয়, এবং আমরা `s.clear()` কল করার পরেও `word` ব্যবহার করলেও তাই হতো। যেহেতু `word` কোনোভাবেই `s`-এর state-এর সাথে যুক্ত নয়, তাই `word` এখনো value `5` ধারণ করে। আমরা সেই value `5` ব্যবহার করে variable `s` থেকে প্রথম শব্দটি বের করার চেষ্টা করতে পারি, কিন্তু তা একটি bug হবে, কারণ আমরা `word`-এ `5` সংরক্ষণ করার পর থেকে `s`-এর content পরিবর্তিত হয়ে গেছে।

`word`-এর index যে `s`-এর data-এর সাথে sync থাকবে না তা নিয়ে চিন্তা করা ক্লান্তিকর এবং error-prone! এই index-গুলো পরিচালনা করা আরও নাজুক হয়ে যায় যদি আমরা একটি `second_word` function লিখি। তার signature হতে হবে এমন:

```rust,ignore
fn second_word(s: &String) -> (usize, usize) {
```

এখন আমরা একটি শুরুর index _এবং_ একটি শেষের index ট্র্যাক করছি, এবং আমাদের কাছে আরও বেশি value আছে যা নির্দিষ্ট state-এর data থেকে হিসাব করা হয়েছে কিন্তু সেই state-এর সাথে কোনোভাবেই যুক্ত নয়। আমাদের তিনটি পরস্পর সম্পর্কহীন variable ভাসছে যেগুলো একসাথে sync রাখতে হবে।

আমাদের সৌভাগ্য যে Rust-এ এই সমস্যার একটি সমাধান আছে: string slice।

### String Slice

_String slice_ হলো একটি `String`-এর element-গুলোর একটি contiguous sequence-এর reference, এবং এটি দেখতে এমন:

```rust
    let s = String::from("hello world");

    let hello = &s[0..5];
    let world = &s[6..11];
```

পুরো `String`-এর reference হওয়ার বদলে, `hello` হলো `String`-এর একটি অংশের reference, যা অতিরিক্ত `[0..5]` অংশে নির্দিষ্ট করা। আমরা square bracket-এর ভেতর একটি range দিয়ে `[starting_index..ending_index]` specify করে slice তৈরি করি, যেখানে _`starting_index`_ হলো slice-এর প্রথম অবস্থান এবং _`ending_index`_ হলো slice-এর শেষ অবস্থানের চেয়ে এক বেশি। ভেতরে, slice data structure-টি শুরুর অবস্থান ও slice-এর length সংরক্ষণ করে, যা _`ending_index`_ থেকে _`starting_index`_ বিয়োগ করার সমতুল্য। সুতরাং, `let world = &s[6..11];` এর ক্ষেত্রে, `world` হবে এমন একটি slice যা `s`-এর index 6-এর byte-টিকে নির্দেশ করে এমন একটি pointer ধারণ করে এবং তার length value `5`।

Figure 4-7 এটি একটি diagram-এ দেখায়।

<img alt="Three tables: a table representing the stack data of s, which points
to the byte at index 0 in a table of the string data &quot;hello world&quot; on
the heap. The third table represents the stack data of the slice world, which
has a length value of 5 and points to byte 6 of the heap data table."
src="img/trpl04-07.svg" class="center" style="width: 50%;" />

<span class="caption">Figure 4-7: A string slice referring to part of a
`String`</span>

Rust-এর `..` range syntax-এ, তুমি যদি index 0 থেকে শুরু করতে চাও, তবে দুই ডটের আগের value বাদ দিতে পারো। অন্য কথায়, এগুলো সমান:

```rust
let s = String::from("hello");

let slice = &s[0..2];
let slice = &s[..2];
```

একইভাবে, তোমার slice যদি `String`-এর শেষ byte পর্যন্ত পরিসীমা জুড়ে থাকে, তবে তুমি শেষের সংখ্যাটি বাদ দিতে পারো। এর মানে এগুলো সমান:

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[3..len];
let slice = &s[3..];
```

তুমি দুটি value ই বাদ দিয়ে পুরো string-এর একটি slice নিতে পারো। তাই এগুলো সমান:

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[0..len];
let slice = &s[..];
```

> নোট: String slice range index গুলো অবশ্যই valid UTF-8 character boundary-তে হতে হবে। তুমি যদি একটি multibyte character-এর মাঝখানে কোনো string slice তৈরি করার চেষ্টা করো, তবে তোমার program error সহ exit করবে।

এত কিছু মাথায় রেখে, চলো `first_word`-কে আবার লেখা যাক যাতে সে একটি slice ফেরত দেয়। "string slice" বোঝায় এমন type-টি লেখা হয় `&str`:

<Listing file-name="src/main.rs">

```rust
fn first_word(s: &String) -> &str {
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

Listing 4-7-এর মতো একই উপায়ে আমরা শব্দের শেষের index বের করি—প্রথম স্পেসটি খুঁজে বের করে। স্পেস পেলে আমরা string-এর শুরু এবং স্পেসের index-কে শুরু ও শেষ index হিসেবে ব্যবহার করে একটি string slice ফেরত দিই।

এখন আমরা `first_word` কল করলে, আমরা এমন একটি single value ফেরত পাই যা underlying data-এর সাথে যুক্ত। Value-টি তৈরি হয় slice-এর শুরু পয়েন্টের একটি reference এবং slice-এর element সংখ্যা দিয়ে।

Slice ফেরত দেওয়া একটি `second_word` function-এর জন্যও কাজ করবে:

```rust,ignore
fn second_word(s: &String) -> &str {
```

এখন আমাদের কাছে এমন একটি straightforward API আছে যা নষ্ট করা অনেক কঠিন, কারণ compiler নিশ্চিত করবে যে `String`-এর ভেতরের reference গুলো valid থাকে। Listing 4-8-এর program-টির bug মনে আছে, যেখানে আমরা প্রথম শব্দের শেষের index পেয়েছিলাম কিন্তু তারপর string clear করে দিয়েছিলাম ফলে আমাদের index invalid হয়ে গিয়েছিল? সেই code-টি logically ভুল ছিল কিন্তু কোনো তাৎক্ষণিক error দেখায়নি। সমস্যাগুলো পরে দেখা দিত যদি আমরা empty করা string-এর সাথে সেই প্রথম শব্দের index ব্যবহার করতে থাকতাম। Slice এই bug-কে অসম্ভব করে দেয় এবং আমাদের code-এ সমস্যা আছে তা অনেক আগেই জানিয়ে দেয়। `first_word`-এর slice সংস্করণ ব্যবহার করলে একটি compile-time error ছুঁড়বে:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
fn main() {
    let mut s = String::from("hello world");

    let word = first_word(&s);

    s.clear(); // error!

    println!("the first word is: {word}");
}
```

</Listing>

এখানে compiler error দেখো:

```console
$ cargo run
   Compiling ownership v0.1.0 (file:///projects/ownership)
error[E0502]: cannot borrow `s` as mutable because it is also borrowed as immutable
  --> src/main.rs:18:5
   |
16 |     let word = first_word(&s);
   |                           -- immutable borrow occurs here
17 |
18 |     s.clear(); // error!
   |     ^^^^^^^^^ mutable borrow occurs here
19 |
20 |     println!("the first word is: {word}");
   |                                   ---- immutable borrow later used here

For more information about this error, try `rustc --explain E0502`.
error: could not compile `ownership` (bin "ownership") due to 1 previous error
```

Borrowing নিয়ম থেকে মনে করো, আমাদের যদি কোনো জিনিসের immutable reference থাকে, তবে আমরা আর mutable reference নিতে পারি না। যেহেতু `clear`-কে `String` truncate করতে হয়, তাই এর একটি mutable reference দরকার। `clear` কলের পরের `println!`-এ `word`-এর reference ব্যবহৃত হয়, তাই সেই মুহূর্তে immutable reference-টি এখনো active থাকতে হবে। Rust `clear`-এর mutable reference এবং `word`-এর immutable reference-কে একই সময়ে থাকতে না দিয়ে compilation fail করে দেয়। Rust শুধু আমাদের API ব্যবহার করা সহজ করেই দেয়নি, বরং compile time-এই সম্পূর্ণ একটি শ্রেণীর error দূর করেছে!

<!-- Old headings. Do not remove or links may break. -->

<a id="string-literals-are-slices"></a>

#### String Literal যেহেতু Slice

মনে করো আমরা বলেছিলাম string literal গুলো binary-এর ভেতরে সংরক্ষিত থাকে। এখন যেহেতু আমরা slice জানি, string literal গুলোকে সঠিকভাবে বুঝতে পারি:

```rust
let s = "Hello, world!";
```

এখানে `s`-এর type হলো `&str`: এটি এমন একটি slice যা binary-এর সেই নির্দিষ্ট পয়েন্টকে নির্দেশ করে। এটিই কারণ যে string literal গুলো immutable; `&str` একটি immutable reference।

#### String Slice যেহেতু Parameter

তুমি যে literal এবং `String` value উভয়েরই slice নিতে পারো এটা জানলে `first_word`-এ আরও একটি উন্নতি করতে পারি, আর সেটি হলো এর signature:

```rust,ignore
fn first_word(s: &String) -> &str {
```

বেশি অভিজ্ঞ একজন Rustacean এর বদলে Listing 4-9-এ দেখানো signature লিখবেন, কারণ এটি আমাদেরকে একই function `&String` value এবং `&str` value উভয়ের ওপরই ব্যবহার করতে দেয়।

<Listing number="4-9" caption="Improving the `first_word` function by using a string slice for the type of the `s` parameter">

```rust,ignore
fn first_word(s: &str) -> &str {
```

</Listing>

আমাদের যদি একটি string slice থাকে, তবে আমরা সেটি সরাসরি পাস করতে পারি। আমাদের যদি একটি `String` থাকে, তবে আমরা সেই `String`-এর একটি slice অথবা `String`-টির একটি reference পাস করতে পারি। এই flexibility পায় deref coercions নামের একটি feature-এর সুবিধা নিয়ে, যা নিয়ে আমরা Chapter 15-এর [“Using Deref Coercions in Functions and Methods”][deref-coercions]<!-- ignore --> section-এ আলোচনা করব।

কোনো function-কে `String`-এর reference-এর বদলে string slice গ্রহণ করতে দিলে আমাদের API আরও general ও কার্যকরী হয়, কোনো functionality হারায় না:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let my_string = String::from("hello world");

    // `first_word` works on slices of `String`s, whether partial or whole.
    let word = first_word(&my_string[0..6]);
    let word = first_word(&my_string[..]);
    // `first_word` also works on references to `String`s, which are equivalent
    // to whole slices of `String`s.
    let word = first_word(&my_string);

    let my_string_literal = "hello world";

    // `first_word` works on slices of string literals, whether partial or
    // whole.
    let word = first_word(&my_string_literal[0..6]);
    let word = first_word(&my_string_literal[..]);

    // Because string literals *are* string slices already,
    // this works too, without the slice syntax!
    let word = first_word(my_string_literal);
}
```

</Listing>

### অন্যান্য Slice

তুমি যেমন ভাবতে পারো, string slice শুধু string-এর জন্যই নির্দিষ্ট। কিন্তু একটি আরও general slice type-ও আছে। এই array-টি বিবেচনা করো:

```rust
let a = [1, 2, 3, 4, 5];
```

ঠিক যেমন আমরা একটি string-এর অংশকে refer করতে চাইতে পারি, আমরা একটি array-এর অংশকেও refer করতে চাইতে পারি। আমরা এটা করব এভাবে:

```rust
let a = [1, 2, 3, 4, 5];

let slice = &a[1..3];

assert_eq!(slice, &[2, 3]);
```

এই slice-টির type হলো `&[i32]`। এটি string slice-এর মতোই কাজ করে—প্রথম element-এর একটি reference এবং একটি length সংরক্ষণ করে। তুমি এই ধরনের slice সব ধরনের অন্যান্য collection-এর জন্য ব্যবহার করবে। এই collection-গুলো নিয়ে আমরা Chapter 8-তে vector আলোচনার সময় বিস্তারিত আলোচনা করব।

## Summary

Ownership, borrowing এবং slice-এর concept গুলো Rust program-এ compile time-এ memory safety নিশ্চিত করে। Rust language তোমাকে অন্যান্য systems programming language-এর মতোই তোমার memory ব্যবহারের উপর নিয়ন্ত্রণ দেয়। কিন্তু data-এর owner scope-এর বাইরে গেলে স্বয়ংক্রিয়ভাবে সেই data পরিষ্কার করার অর্থ হলো তোমাকে এই নিয়ন্ত্রণ পেতে অতিরিক্ত code লিখতে বা debug করতে হয় না।

Ownership Rust-এর আরও অনেক অংশের কাজকে প্রভাবিত করে, তাই বইয়ের বাকি অংশ জুড়ে আমরা এই concept গুলো নিয়ে আরও কথা বলব। চলো এবার Chapter 5-এ যাই এবং data-এর টুকরো গুলোকে একসাথে একটি `struct`-এ সাজানোর বিষয়ে দেখি।

[ch13]: ch13-02-iterators.html
[ch6]: ch06-02-match.html#patterns-that-bind-to-values
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[deref-coercions]: ch15-02-deref.html#using-deref-coercions-in-functions-and-methods

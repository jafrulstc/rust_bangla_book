## String দিয়ে UTF-8 Encoded Text Store করা

আমরা Chapter 4-এ string নিয়ে কথা বলেছি, কিন্তু এবার সেগুলো নিয়ে আরও বিস্তারিত আলোচনা করব। নতুন Rustacean-রা সাধারণত তিনটি কারণে string নিয়ে আটকে যায়: Rust-এর possible error expose করার প্রবণতা, string-এর অনেক প্রোগ্রামারের ধারণার চেয়ে বেশি জটিল data structure হওয়া, এবং UTF-8। অন্যান্য programming language থেকে এলে এই বিষয়গুলো মিলে বেশ কঠিন মনে হতে পারে।

আমরা string-কে collection হিসেবে আলোচনা করছি কারণ string-কে একটি byte collection হিসেবে implement করা হয়, এর সাথে কিছু method আছে যা সেই byte-গুলোকে text হিসেবে interpret করলে কাজে লাগে। এই section-এ আমরা `String`-এর সেইসব operation নিয়ে কথা বলব যেগুলো প্রতিটি collection type-এ থাকে, যেমন তৈরি করা, আপডেট করা এবং read করা। এছাড়া আমরা এও আলোচনা করব কীভাবে `String` অন্যান্য collection থেকে আলাদা, বিশেষ করে মানুষ ও কম্পিউটার কীভাবে `String` data-কে ভিন্নভাবে interpret করে তার কারণে একটি `String`-এ indexing কেন জটিল।

<!-- Old headings. Do not remove or links may break. -->

<a id="what-is-a-string"></a>

### String Define করা

আমরা প্রথমে _string_ বলতে কী বুঝাচ্ছি তা define করি। Rust-এ core language-এ শুধু একটিই string type আছে, সেটা হলো string slice `str`, যা সাধারণত তার borrowed form `&str` আকারে দেখা যায়। Chapter 4-এ আমরা string slice নিয়ে কথা বলেছি, যা অন্য কোথাও store করা UTF-8 encoded string data-এর reference। যেমন string literal গুলো program-এর binary-তে store করা থাকে, তাই সেগুলো string slice।

`String` type, যা Rust-এর core language-এ না থেকে standard library-তে দেওয়া আছে, সেটা একটি growable, mutable, owned, UTF-8 encoded string type। Rustacean-রা যখন Rust-এ “strings” এর কথা বলে, তখন তারা হয়তো `String` বা string slice `&str` যেকোনো একটিকেই বোঝাতে পারে, শুধু একটিকে নয়। যদিও এই section-টি মূলত `String` নিয়ে, Rust-এর standard library-তে দুই ধরনের type-ই ব্যাপকভাবে ব্যবহৃত হয়, এবং `String` ও string slice দুটোই UTF-8 encoded।

### নতুন String তৈরি করা

`Vec<T>`-এ যেসব operation available সেগুলোর অনেকগুলোই `String`-এও available, কারণ `String` আসলে কিছু extra guarantee, restriction ও capability সহ একটি byte vector-এর চারপাশে একটি wrapper হিসেবে implement করা। এমন একটি function যা `Vec<T>` ও `String` দুটোর সাথেই একইভাবে কাজ করে সেটা হলো `new` function, যা instance তৈরি করে, Listing 8-11-তে দেখানো হয়েছে।

<Listing number="8-11" caption="নতুন, খালি একটি `String` তৈরি করা">

```rust
    let mut s = String::new();
```

</Listing>

এই line-টি একটি নতুন, খালি string তৈরি করে যার নাম `s`, যেখানে আমরা পরে data load করতে পারি। প্রায়ই আমাদের কাছে কিছু initial data থাকবে যা দিয়ে আমরা string শুরু করতে চাই। সেটার জন্য আমরা `to_string` method ব্যবহার করি, যা যেকোনো type-এ যেখানে `Display` trait implement করা সেখানে available, ঠিক যেমন string literal-এ। Listing 8-12 দুটি example দেখায়।

<Listing number="8-12" caption="`to_string` method ব্যবহার করে একটি string literal থেকে `String` তৈরি করা">

```rust
    let data = "initial contents";

    let s = data.to_string();

    // The method also works on a literal directly:
    let s = "initial contents".to_string();
```

</Listing>

এই code-টি `initial contents` ধারণ করে এমন একটি string তৈরি করে।

আমরা `String::from` function ব্যবহার করেও একটি string literal থেকে `String` তৈরি করতে পারি। Listing 8-13-এর code-টি `to_string` ব্যবহার করা Listing 8-12-এর code-এর সমতুল্য।

<Listing number="8-13" caption="`String::from` function ব্যবহার করে একটি string literal থেকে `String` তৈরি করা">

```rust
    let s = String::from("initial contents");
```

</Listing>

যেহেতু string অনেক কাজে ব্যবহৃত হয়, তাই string-এর জন্য বিভিন্ন generic API আছে যা আমাদের অনেক option দেয়। কিছু কিছু redundant মনে হতে পারে, কিন্তু প্রতিটির নিজস্ব জায়গা আছে! এই ক্ষেত্রে `String::from` ও `to_string` একই কাজ করে, তাই কোনটা বেছে নেবে সেটা style ও readability-এর বিষয়।

মনে রেখো যে string গুলো UTF-8 encoded, তাই আমরা এগুলোতে যেকোনো properly encoded data রাখতে পারি, Listing 8-14-তে যেমন দেখানো হয়েছে।

<Listing number="8-14" caption="বিভিন্ন ভাষার greeting string-এ store করা">

```rust
    let hello = String::from("السلام عليكم");
    let hello = String::from("Dobrý den");
    let hello = String::from("Hello");
    let hello = String::from("שלום");
    let hello = String::from("नमस्ते");
    let hello = String::from("こんにちは");
    let hello = String::from("안녕하세요");
    let hello = String::from("你好");
    let hello = String::from("Olá");
    let hello = String::from("Здравствуйте");
    let hello = String::from("Hola");
}
```

</Listing>

এই সবগুলোই বৈধ `String` value।

### String আপডেট করা

একটি `String` এর size বড় হতে পারে এবং এর content পরিবর্তন হতে পারে, ঠিক `Vec<T>`-এর content-এর মতো, যদি তুমি এতে আরও data push করো। এছাড়া তুমি সুবিধাজনকভাবে `+` operator বা `format!` macro ব্যবহার করে `String` value গুলো concatenate করতে পারো।

<!-- Old headings. Do not remove or links may break. -->

<a id="appending-to-a-string-with-push_str-and-push"></a>

#### `push_str` বা `push` দিয়ে Append করা

আমরা `push_str` method ব্যবহার করে একটি string slice append করার মাধ্যমে একটি `String`-কে বড় করতে পারি, Listing 8-15-তে যেমন দেখানো হয়েছে।

<Listing number="8-15" caption="`push_str` method ব্যবহার করে একটি `String`-এ string slice append করা">

```rust
    let mut s = String::from("foo");
    s.push_str("bar");
```

</Listing>

এই দুটি line-এর পর `s`-এর মান হবে `foobar`। `push_str` method একটি string slice নেয় কারণ আমরা সবসময় parameter-এর ownership নিতে চাই না। যেমন, Listing 8-16-এর code-এ, আমরা `s2`-এর content `s1`-এ append করার পরও `s2` ব্যবহার করতে চাই।

<Listing number="8-16" caption="একটি string slice-এর content `String`-এ append করার পর সেই string slice ব্যবহার করা">

```rust
    let mut s1 = String::from("foo");
    let s2 = "bar";
    s1.push_str(s2);
    println!("s2 is {s2}");
```

</Listing>

যদি `push_str` method `s2`-এর ownership নিত, তাহলে আমরা শেষ line-এ এর value print করতে পারতাম না। কিন্তু এই code ঠিক যেমন আশা করছিলাম তেমনই কাজ করে!

`push` method একটি single character কে parameter হিসেবে নেয় এবং সেটিকে `String`-এ যোগ করে। Listing 8-17 `push` method ব্যবহার করে একটি `String`-এ _l_ অক্ষরটি যোগ করে।

<Listing number="8-17" caption="`push` ব্যবহার করে একটি `String` value-তে একটি character যোগ করা">

```rust
    let mut s = String::from("lo");
    s.push('l');
```

</Listing>

ফলে `s`-এর মান হবে `lol`।

<!-- Old headings. Do not remove or links may break. -->

<a id="concatenation-with-the--operator-or-the-format-macro"></a>

#### `+` বা `format!` দিয়ে Concatenation করা

প্রায়শই তুমি দুটি বিদ্যমান string-কে একসাথে যোগ করতে চাইবে। তার একটি উপায় হলো `+` operator ব্যবহার করা, Listing 8-18-তে যেমন দেখানো হয়েছে।

<Listing number="8-18" caption="`+` operator ব্যবহার করে দুটি `String` value-কে নতুন একটি `String` value-তে একত্র করা">

```rust
    let s1 = String::from("Hello, ");
    let s2 = String::from("world!");
    let s3 = s1 + &s2; // note s1 has been moved here and can no longer be used
```

</Listing>

`s3` string-টি `Hello, world!` ধারণ করবে। যোগের পর `s1` আর বৈধ না থাকার কারণ এবং আমরা `s2`-এর একটি reference ব্যবহার করার কারণ—এই দুটিই `+` operator ব্যবহার করলে যে method-টি কল হয় তার signature-এর সাথে সম্পর্কিত। `+` operator `add` method ব্যবহার করে, যার signature মোটামুটি এরকম:

```rust,ignore
fn add(self, s: &str) -> String {
```

Standard library-তে তুমি `add`-কে generics ও associated type দিয়ে define করা দেখবে। এখানে আমরা concrete type বসিয়ে দিয়েছি, যেটা হয় যখন আমরা এই method-টি `String` value দিয়ে কল করি। Generics নিয়ে আমরা Chapter 10-এ আলোচনা করব। এই signature আমাদের `+` operator-এর কঠিন অংশগুলো বুঝতে যে সূত্র দেয় সেটা দেয়।

প্রথমত, `s2`-এর আগে `&` আছে, যার মানে আমরা প্রথম string-এর সাথে দ্বিতীয় string-এর একটি reference যোগ করছি। এটা `add` function-এর `s` parameter-এর কারণে: আমরা একটি `String`-এ শুধু একটি string slice যোগ করতে পারি; দুটি `String` value একসাথে যোগ করতে পারি না। কিন্তু অপেক্ষা করো—`&s2`-এর type হলো `&String`, `&str` নয়, যেমনটা `add`-এর দ্বিতীয় parameter-এ specify করা। তাহলে Listing 8-18 compile করে কেন?

`add`-কে কল করার সময় আমরা `&s2` ব্যবহার করতে পারার কারণ হলো compiler `&String` argument-কে `&str`-এ coerce করতে পারে। যখন আমরা `add` method কল করি, Rust একটি deref coercion ব্যবহার করে, যা এখানে `&s2`-কে `&s2[..]`-এ পরিণত করে। Deref coercion নিয়ে আমরা Chapter 15-তে আরও গভীরভাবে আলোচনা করব। যেহেতু `add` `s` parameter-এর ownership নেয় না, তাই এই operation-এর পরও `s2` একটি বৈধ `String` থাকবে।

দ্বিতীয়ত, signature-এ দেখা যায় যে `add` `self`-এর ownership নেয় কারণ `self`-এর আগে `&` _নেই_। এর মানে Listing 8-18-এর `s1` `add` কলে move হবে এবং এর পরে আর বৈধ থাকবে না। সুতরাং, যদিও `let s3 = s1 + &s2;` মনে হয় যে দুটি string-ই copy করে নতুন একটি string তৈরি করবে, এই statement আসলে `s1`-এর ownership নেয়, `s2`-এর content-এর একটি copy append করে, এবং তারপর result-এর ownership ফেরত দেয়। অন্য কথায়, মনে হয় অনেক copy হচ্ছে, কিন্তু আসলে তা নয়; implementation টা copy করার চেয়ে বেশি efficient।

যদি আমাদের একাধিক string concatenate করতে হয়, তাহলে `+` operator-এর আচরণ জটিল হয়ে যায়:

```rust
    let s1 = String::from("tic");
    let s2 = String::from("tac");
    let s3 = String::from("toe");

    let s = s1 + "-" + &s2 + "-" + &s3;
```

এখানে `s`-এর মান হবে `tic-tac-toe`। সব সেই `+` ও `"` character-গুলোর মধ্যে কী হচ্ছে বোঝা কঠিন। আরও জটিল উপায়ে string একত্র করতে আমরা এর বদলে `format!` macro ব্যবহার করতে পারি:

```rust
    let s1 = String::from("tic");
    let s2 = String::from("tac");
    let s3 = String::from("toe");

    let s = format!("{s1}-{s2}-{s3}");
```

এই code-টিও `s`-এর মান `tic-tac-toe` করে। `format!` macro `println!`-এর মতো কাজ করে, কিন্তু screen-এ output print করার বদলে এটি content সহ একটি `String` ফেরত দেয়। `format!` ব্যবহার করা code-এর সংস্করণটি পড়তে অনেক সহজ, এবং `format!` macro যে code generate করে সেটি reference ব্যবহার করে, তাই এই কল তার কোনো parameter-এর ownership নেয় না।

### String-এ Indexing করা

অনেক অন্যান্য programming language-এ index দিয়ে reference করে string-এর একক character access করা একটি বৈধ ও সাধারণ operation। কিন্তু Rust-এ তুমি indexing syntax ব্যবহার করে একটি `String`-এর অংশ access করার চেষ্টা করলে error পাবে। Listing 8-19-এর invalid code-টি বিবেচনা করো।

<Listing number="8-19" caption="একটি `String`-এর সাথে indexing syntax ব্যবহার করার চেষ্টা">

```rust,ignore,does_not_compile
    let s1 = String::from("hi");
    let h = s1[0];
```

</Listing>

এই code-টি নিচের error দেবে:

```console
$ cargo run
   Compiling collections v0.1.0 (file:///projects/collections)
error[E0277]: the type `str` cannot be indexed by `{integer}`
 --> src/main.rs:3:16
  |
3 |     let h = s1[0];
  |                ^ string indices are ranges of `usize`
  |
  = help: the trait `SliceIndex<str>` is not implemented for `{integer}`
  = note: you can use `.chars().nth()` or `.bytes().nth()`
          for more information, see chapter 8 in The Book: <https://doc.rust-lang.org/book/ch08-02-strings.html#indexing-into-strings>
help: `usize` implements trait `SliceIndex<T>`
 --> /rustc/88d9e12ae178fab0fb5cc050a94da85685d449ea/library/core/src/slice/index.rs:179:0
  |
  = note: `SliceIndex<[T]>`
 --> /rustc/88d9e12ae178fab0fb5cc050a94da85685d449ea/library/core/src/bstr/traits.rs:197:0
  |
  = note: `SliceIndex<ByteStr>`
  = note: required for `String` to implement `Index<{integer}>`

For more information about this error, try `rustc --explain E0277`.
error: could not compile `collections` (bin "collections") due to 1 previous error
```

Error-টিই কথা বলে: Rust string-গুলো indexing support করে না। কিন্তু কেন না? এই প্রশ্নের উত্তর দিতে হলে আমাদের আলোচনা করতে হবে Rust কীভাবে string মেমরিতে store করে।

#### Internal Representation

একটি `String` হলো একটি `Vec<u8>`-এর উপর একটি wrapper। Listing 8-14 থেকে আমাদের properly encoded UTF-8 example string-গুলোর কয়েকটি দেখি। প্রথমে এই একটি:

```rust
    let hello = String::from("Hola");
```

এই ক্ষেত্রে `len` হবে `4`, যার মানে `"Hola"` string-টি ধারণ করে এমন vector-টি 4 byte দীর্ঘ। এই অক্ষরগুলোর প্রতিটি UTF-8-এ encode করার সময় 1 byte নেয়। কিন্তু নিচের line-টি তোমাকে চমকে দিতে পারে (খেয়াল করো যে এই string-টি বড় ছাঁদের Cyrillic অক্ষর _Ze_ দিয়ে শুরু, 3 সংখ্যাটি দিয়ে নয়):

```rust
    let hello = String::from("Здравствуйте");
```

তোমাকে জিজ্ঞেস করা হলে এই string-টির দৈর্ঘ্য কত, তুমি হয়তো বলবে 12। আসলে Rust-এর উত্তর 24: সেটাই হলো “Здравствуйте”-কে UTF-8-এ encode করতে যত byte লাগে, কারণ এই string-এ প্রতিটি Unicode scalar value 2 byte storage নেয়। সুতরাং, string-এর byte-গুলোর উপর index করা সবসময় একটি বৈধ Unicode scalar value-এর সাথে মিলবে না। এটা দেখাতে এই invalid Rust code-টি বিবেচনা করো:

```rust,ignore,does_not_compile
let hello = "Здравствуйте";
let answer = &hello[0];
```

তুমি আগেই জানো যে `answer` প্রথম অক্ষর `З` হবে না। UTF-8-এ encode করার সময় `З`-এর প্রথম byte হলো `208` এবং দ্বিতীয়টি `151`, তাই মনে হতে পারে `answer` আসলে `208` হওয়া উচিত, কিন্তু `208` নিজে একটি বৈধ character নয়। কেউ যদি এই string-এর প্রথম অক্ষর চায় তাহলে `208` ফেরত দেওয়া সম্ভবত সেই user-এর কাঙ্ক্ষিত নয়; তবে byte index 0-তে Rust-এর কাছে যে data আছে সেটাই এটুকু। User সাধারণত byte value ফেরত পেতে চায় না, এমনকি string-এ শুধু Latin অক্ষর থাকলেও: যদি `&"hi"[0]` এমন বৈধ code হতো যা byte value ফেরত দেয়, তাহলে সেটা `h` নয়, `104` ফেরত দিত।

তাহলে উত্তর হলো, অপ্রত্যাশিত কোনো value ফেরত দিয়ে এবং এমন কিছু bug তৈরি করে যা সাথে সাথে ধরা নাও পড়তে পারে—এগুলো এড়াতে Rust এই code-টি আদৌ compile করে না এবং development process-এর শুরুতেই ভুল বোঝাবুঝি প্রতিরোধ করে।

<!-- Old headings. Do not remove or links may break. -->

<a id="bytes-and-scalar-values-and-grapheme-clusters-oh-my"></a>

#### Byte, Scalar Value, এবং Grapheme Cluster

UTF-8 সম্পর্কে আরেকটি বিষয় হলো Rust-এর দৃষ্টিকোণ থেকে string-কে দেখার আসলে তিনটি প্রাসঙ্গিক উপায় আছে: byte, scalar value এবং grapheme cluster (যাকে আমরা _অক্ষর_ বলব তার সবচেয়ে কাছের জিনিস)।

যদি আমরা Devanagari script-এ লেখা Hindi শব্দ “नमस्ते”-কে দেখি, এটি `u8` value-এর একটি vector হিসেবে store করা থাকে যা দেখতে এরকম:

```text
[224, 164, 168, 224, 164, 174, 224, 164, 184, 224, 165, 141, 224, 164, 164,
224, 165, 135]
```

এটি 18 byte এবং কম্পিউটার আসলে এই data এভাবেই store করে। যদি আমরা সেগুলোকে Unicode scalar value হিসেবে দেখি, যেটা Rust-এর `char` type, সেই byte-গুলো দেখতে এরকম:

```text
['न', 'म', 'स', '्', 'त', 'े']
```

এখানে ছয়টি `char` value আছে, কিন্তু চতুর্থ ও ষষ্ঠটি অক্ষর নয়: এগুলো diacritic, যা একা কোনো অর্থ বহন করে না। শেষে, যদি আমরা সেগুলোকে grapheme cluster হিসেবে দেখি, তাহলে আমরা এমন চারটি অক্ষর পাব যা মানুষ এই Hindi শব্দটি তৈরি করে বলে মনে করে:

```text
["न", "म", "स्", "ते"]
```

Rust কম্পিউটারে store করা raw string data-কে interpret করার বিভিন্ন উপায় দেয়, যাতে প্রতিটি program তার প্রয়োজনীয় interpretation বেছে নিতে পারে, data যে ভাষারই হোক না কেন।

Rust যে আরেকটি কারণে আমাদের `String`-এ index করে character পেতে দেয় না সেটা হলো, indexing operation সবসময় constant time (O(1)) নেওয়ার কথা। কিন্তু একটি `String`-এর ক্ষেত্রে সেই performance guarantee করা সম্ভব নয়, কারণ Rust-কে কতগুলো বৈধ character আছে তা নির্ধারণ করতে শুরু থেকে index পর্যন্ত content-এর উপর দিয়ে হাঁটতে হবে।

### String Slice করা

String-এ index করা প্রায়ই খারাপ ধারণা, কারণ string-indexing operation-এর return type কী হওয়া উচিত সেটা স্পষ্ট নয়: একটি byte value, একটি character, একটি grapheme cluster, নাকি একটি string slice। সুতরাং তুমি যদি সত্যিই index ব্যবহার করে string slice তৈরি করতে চাও, তাহলে Rust তোমাকে আরও নির্দিষ্ট হতে বলে।

একটি single সংখ্যা সহ `[]` ব্যবহার করে index করার বদলে তুমি একটি range সহ `[]` ব্যবহার করে নির্দিষ্ট byte ধারণ করে এমন একটি string slice তৈরি করতে পারো:

```rust
let hello = "Здравствуйте";

let s = &hello[0..4];
```

এখানে `s` হবে একটি `&str` যা string-টির প্রথম 4 byte ধারণ করে। আগে আমরা বলেছিলাম যে এই character গুলোর প্রতিটি 2 byte, যার মানে `s` হবে `Зд`।

যদি আমরা `&hello[0..1]`-এর মতো কোনো character-এর byte-এর শুধু একটি অংশ slice করার চেষ্টা করি, তাহলে Rust vector-এ অবৈধ index access করার মতোই runtime-এ panic করবে:

```console
$ cargo run
   Compiling collections v0.1.0 (file:///projects/collections)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.43s
     Running `target/debug/collections`

thread 'main' (6017738) panicked at src/main.rs:4:19:
end byte index 1 is not a char boundary; it is inside 'З' (bytes 0..2 of string)
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Range দিয়ে string slice তৈরি করার সময় সাবধান থাকো, কারণ এতে তোমার program crash করতে পারে।

<!-- Old headings. Do not remove or links may break. -->

<a id="methods-for-iterating-over-strings"></a>

### String-এর উপর Iterate করা

String-ের অংশগুলোর উপর operation করার সবচেয়ে ভালো উপায় হলো স্পষ্টভাবে বলে দেওয়া যে তুমি character চাই নাকি byte। একক Unicode scalar value-এর জন্য `chars` method ব্যবহার করো। “Зд”-এর উপর `chars` কল করলে দুটি `char` type-এর value আলাদা করে ফেরত দেয়, এবং তুমি প্রতিটি element access করতে সেই result-এর উপর iterate করতে পারো:

```rust
for c in "Зд".chars() {
    println!("{c}");
}
```

এই code নিচের গুলো print করবে:

```text
З
д
```

অন্যদিকে, `bytes` method প্রতিটি raw byte ফেরত দেয়, যা তোমার domain-এ কাজে লাগতে পারে:

```rust
for b in "Зд".bytes() {
    println!("{b}");
}
```

এই code এই string তৈরি করা 4 byte-গুলো print করবে:

```text
208
151
208
180
```

কিন্তু মনে রেখো যে বৈধ Unicode scalar value 1 byte-এর বেশি দিয়ে তৈরি হতে পারে।

Devanagari script-এর মতো ক্ষেত্রে string থেকে grapheme cluster পাওয়া জটিল, তাই এই functionality standard library-তে দেওয়া নেই। তোমার যদি এই functionality দরকার হয় তাহলে [crates.io](https://crates.io/)<!-- ignore -->-তে অন্যান্য Rust user-দের share করা crate গুলো ব্যবহার করতে পারো।

<!-- Old headings. Do not remove or links may break. -->

<a id="strings-are-not-so-simple"></a>

### String-এর জটিলতা Handle করা

সারসংক্ষেপে, string জটিল। বিভিন্ন programming language এই জটিলতা প্রোগ্রামারের কাছে কীভাবে উপস্থাপন করবে সেটা নিয়ে ভিন্ন ভিন্ন সিদ্ধান্ত নেয়। Rust বেছে নিয়েছে সব Rust program-এর জন্য `String` data-এর সঠিক handling-কে default behavior বানাতে, যার মানে প্রোগ্রামারদের UTF-8 data handle করার বিষয়ে শুরুতেই বেশি ভাবতে হয়। এই trade-off অন্যান্য programming language-এ দৃশ্যমান হওয়ার চেয়ে string-এর বেশি জটিলতা expose করে, কিন্তু development life cycle-এর শেষ দিকে non-ASCII character জড়িত error handle করতে হয় না।

খুশির খবর হলো standard library `String` ও `&str` type-এর উপর built হওয়া প্রচুর functionality দেয় যা এই জটিল পরিস্থিতিগুলো সঠিকভাবে handle করতে সাহায্য করে। কাজের কিছু method যেমন string-এর ভেতরে search করার জন্য `contains` এবং একটি string-এর কিছু অংশ অন্য string দিয়ে substitute করার জন্য `replace`-এর documentation দেখতে ভুলো না।

চলো এবার কিছু কম জটিল বিষয়ে চলে যাই: hash map!

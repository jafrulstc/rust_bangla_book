## Data Types

Rust-এ প্রতিটি value-র একটি নির্দিষ্ট _data type_ থাকে, যা Rust-কে বলে দেয় কী ধরনের data specify করা হচ্ছে যাতে সে জানে সেই data-এর সাথে কীভাবে কাজ করতে হবে। আমরা data type-এর দুটি subset দেখব: scalar এবং compound।

মনে রাখবে যে Rust একটি _statically typed_ language, যার মানে হলো compile time-এ সব variable-এর type সম্পর্কে জানা থাকতে হবে। সাধারণত value এবং সেটা কীভাবে ব্যবহার করা হয়েছে তার ওপর ভিত্তি করে compiler বুঝে নিতে পারে আমরা কোন type ব্যবহার করতে চাই। যেসব ক্ষেত্রে অনেকগুলো type-ই সম্ভব, যেমন Chapter 2-এর [“Comparing the Guess to the Secret Number”][comparing-the-guess-to-the-secret-number]<!-- ignore --> section-এ আমরা `parse` ব্যবহার করে একটি `String`-কে numeric type-এ convert করেছিলাম, সেসব ক্ষেত্রে আমাদের একটি type annotation যোগ করতে হয়, এভাবে:

```rust
let guess: u32 = "42".parse().expect("Not a number!");
```

উপরের code-এ দেখানো `: u32` type annotation যোগ না করলে Rust নিচের error দেখাবে, যার মানে হলো আমরা কোন type ব্যবহার করতে চাই তা জানতে compiler-কে আমাদের কাছ থেকে আরও তথ্য দরকার:

```console
$ cargo build
   Compiling no_type_annotations v0.1.0 (file:///projects/no_type_annotations)
error[E0284]: type annotations needed
 --> src/main.rs:2:9
  |
2 |     let guess = "42".parse().expect("Not a number!");
  |         ^^^^^        ----- type must be known at this point
  |
  = note: cannot satisfy `<_ as FromStr>::Err == _`
help: consider giving `guess` an explicit type
  |
2 |     let guess: /* Type */ = "42".parse().expect("Not a number!");
  |              ++++++++++++

For more information about this error, try `rustc --explain E0284`.
error: could not compile `no_type_annotations` (bin "no_type_annotations") due to 1 previous error
```

অন্যান্য data type-এর জন্য তুমি বিভিন্ন type annotation দেখতে পাবে।

### Scalar Types

_scalar_ type একটি একক value উপস্থাপন করে। Rust-এ চারটি primary scalar type আছে: integers, floating-point numbers, Booleans, এবং characters। অন্যান্য programming language থেকে তুমি এগুলো চিনতে পারবে। চলো দেখি Rust-এ এগুলো কীভাবে কাজ করে।

#### Integer Types

_integer_ হলো এমন একটি number যার কোনো ভগ্নাংশ অংশ নেই। আমরা Chapter 2-তে একটি integer type ব্যবহার করেছিলাম, `u32` type। এই type declaration নির্দেশ করে যে এর সাথে যুক্ত value টি একটি unsigned integer (signed integer type-গুলো `u`-এর বদলে `i` দিয়ে শুরু হয়) হবে যা 32 bits জায়গা নেয়। Table 3-1 Rust-এর built-in integer type-গুলো দেখায়। আমরা এই variant-গুলোর যেকোনো একটি ব্যবহার করে একটি integer value-এর type declare করতে পারি।

<span class="caption">Table 3-1: Integer Types in Rust</span>

| Length  | Signed  | Unsigned |
| ------- | ------- | -------- |
| 8-bit   | `i8`    | `u8`     |
| 16-bit  | `i16`   | `u16`    |
| 32-bit  | `i32`   | `u32`    |
| 64-bit  | `i64`   | `u64`    |
| 128-bit | `i128`  | `u128`   |
| Architecture-dependent | `isize` | `usize`  |

প্রতিটি variant হয় signed অথবা unsigned হতে পারে এবং প্রতিটির একটি সুনির্দিষ্ট size আছে। _Signed_ আর _unsigned_ বলতে বোঝায় সেই number-টি negative হতে পারবে কি না—অন্য কথায়, number-টির সাথে sign দরকার (signed) নাকি সেটা শুধু positive-ই হবে এবং তাই sign ছাড়াই represent করা যাবে (unsigned)। এটা কাগজে number লেখার মতো: যখন sign গুরুত্বপূর্ণ, তখন কোনো number-কে plus sign বা minus sign সহ দেখানো হয়; কিন্তু যখন ধরে নেওয়া নিরাপদ যে number-টি positive, তখন সেটা কোনো sign ছাড়াই দেখানো হয়। Signed number-গুলো [two’s complement][twos-complement]<!-- ignore --> representation ব্যবহার করে store করা হয়।

প্রতিটি signed variant -(2<sup>n − 1</sup>) থেকে 2<sup>n − 1</sup> − 1 পর্যন্ত (inclusive) number store করতে পারে, যেখানে _n_ হলো সেই variant-টি যত bit ব্যবহার করে। সুতরাং, একটি `i8` -(2<sup>7</sup>) থেকে 2<sup>7</sup> − 1 পর্যন্ত number store করতে পারে, যা −128 থেকে 127 এর সমান। Unsigned variant-গুলো 0 থেকে 2<sup>n</sup> − 1 পর্যন্ত number store করতে পারে, তাই একটি `u8` 0 থেকে 2<sup>8</sup> − 1 পর্যন্ত number store করতে পারে, যা 0 থেকে 255 এর সমান।

এছাড়াও, `isize` আর `usize` type-গুলো নির্ভর করে তোমার program যে computer-এ run হচ্ছে তার architecture-এর ওপর: 64-bit architecture হলে 64 bits এবং 32-bit architecture হলে 32 bits।

তুমি integer literal গুলো Table 3-2-তে দেখানো যেকোনো রূপে লিখতে পারো। মনে রাখবে যে একাধিক numeric type-এর হতে পারে এমন number literal-গুলো type designate করতে একটি type suffix নেয়, যেমন `57u8`। Number literal-গুলো `_`-কে visual separator হিসেবেও ব্যবহার করতে পারে যাতে number-টি পড়তে সহজ হয়, যেমন `1_000`, যার value `1000` লিখলে যা হতো তার সমানই থাকবে।

<span class="caption">Table 3-2: Integer Literals in Rust</span>

| Number literals  | Example       |
| ---------------- | ------------- |
| Decimal          | `98_222`      |
| Hex              | `0xff`        |
| Octal            | `0o77`        |
| Binary           | `0b1111_0000` |
| Byte (`u8` only) | `b'A'`        |

তাহলে তুমি কীভাবে বুঝবে কোন integer type ব্যবহার করবে? অনিশ্চিত হলে, Rust-এর default-গুলো শুরু করার জন্য সাধারণত ভালো জায়গা: Integer type-গুলোর default হলো `i32`। তুমি মূলত `isize` বা `usize` ব্যবহার করবে যখন কোনো collection-কে index করবে।

> ##### Integer Overflow
>
> ধরো তোমার একটি `u8` type-এর variable আছে যা 0 থেকে 255-এর মধ্যে value ধারণ করতে পারে। যদি তুমি সেই variable-কে ওই range-এর বাইরের কোনো value-তে পরিবর্তন করার চেষ্টা করো, যেমন 256, তাহলে _integer overflow_ ঘটবে, যার ফলে দুটি behavior-এর একটি হতে পারে। যখন তুমি debug mode-এ compile করো, তখন Rust integer overflow-এর জন্য check রাখে যা এই behavior ঘটলে runtime-এ তোমার program-কে _panic_ করায়। যখন কোনো program error সহ exit করে তখন Rust তাকে _panicking_ বলে; আমরা panic সম্পর্কে বিস্তারিত Chapter 9-এর [“Unrecoverable Errors with `panic!`”][unrecoverable-errors-with-panic]<!-- ignore --> section-এ আলোচনা করব।
>
> যখন তুমি `--release` flag দিয়ে release mode-এ compile করো, তখন Rust panic ঘটানো integer overflow-এর জন্য check রাখে _না_। এর বদলে, overflow ঘটলে Rust _two’s complement wrapping_ সম্পন্ন করে। সংক্ষেপে, type-টি যে maximum value ধরতে পারে তার চেয়ে বড় যে value-গুলো সেগুলো type-টি যে minimum value ধরতে পারে সেখানে “wrap around” করে। একটি `u8`-এর ক্ষেত্রে, value 256 হয়ে যায় 0, value 257 হয়ে যায় 1, এবং এভাবে চলতে থাকে। Program-টি panic করবে না, কিন্তু variable-টির এমন একটি value থাকবে যা সম্ভবত তুমি যা আশা করছিলে তা নয়। Integer overflow-এর wrapping behavior-এর ওপর নির্ভর করাকে একটি error হিসেবে ধরা হয়।
>
> Overflow-এর সম্ভাবনাকে explicitly handle করতে তুমি primitive numeric type-গুলোর জন্য standard library দ্বারা provide করা এই method family-গুলো ব্যবহার করতে পারো:
>
> - সব compilation mode-এ `wrapping_add`-এর মতো `wrapping_*` method দিয়ে wrap করো।
> - Overflow হলে `checked_*` method দিয়ে `None` value return করো।
> - `overflowing_*` method দিয়ে value এবং একটি Boolean return করো যা নির্দেশ করে overflow হয়েছিল কি না।
> - `saturating_*` method দিয়ে value-এর minimum বা maximum value-এ saturate করো।

#### Floating-Point Types

Rust-এ _floating-point number_-এর জন্য দুটি primitive type আছে, যেগুলো দশমিক বিন্দু সহ number। Rust-এর floating-point type হলো `f32` এবং `f64`, যথাক্রমে 32 bits ও 64 bits size-এর। Default type হলো `f64` কারণ আধুনিক CPU-তে এর গতি `f32`-এর প্রায় একই, কিন্তু এটি আরও বেশি precision দিতে সক্ষম। সব floating-point type-ই signed।

এখানে floating-point number-এর ব্যবহার দেখানো একটি উদাহরণ দেওয়া হলো:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let x = 2.0; // f64

    let y: f32 = 3.0; // f32
}
```

Floating-point number-গুলো IEEE-754 standard অনুসারে represent করা হয়।

#### Numeric Operations

Rust সব number type-এর জন্য যে প্রাথমিক গাণিতিক operation আশা করো সেগুলো support করে: addition, subtraction, multiplication, division, এবং remainder। Integer division শূন্যের দিকে কাছের পূর্ণ সংখ্যায় truncate করে। নিচের code দেখায় কীভাবে তুমি একটি `let` statement-এ প্রতিটি numeric operation ব্যবহার করবে:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    // addition
    let sum = 5 + 10;

    // subtraction
    let difference = 95.5 - 4.3;

    // multiplication
    let product = 4 * 30;

    // division
    let quotient = 56.7 / 32.2;
    let truncated = -5 / 3; // Results in -1

    // remainder
    let remainder = 43 % 5;
}
```

এই statement-গুলোর প্রতিটি expression একটি গাণিতিক operator ব্যবহার করে এবং একটি একক value-তে evaluate হয়, যা তারপর একটি variable-এর সাথে bind হয়। [Appendix B][appendix_b]<!-- ignore -->-তে Rust-এর সব operator-এর একটি তালিকা আছে।

#### The Boolean Type

অন্যান্য বেশিরভাগ programming language-এর মতোই, Rust-এ Boolean type-এর দুটি সম্ভাব্য value আছে: `true` এবং `false`। Boolean এক byte size-এর। Rust-এ Boolean type `bool` ব্যবহার করে specify করা হয়। যেমন:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let t = true;

    let f: bool = false; // with explicit type annotation
}
```

Boolean value ব্যবহারের প্রধান উপায় হলো conditionals-এর মাধ্যমে, যেমন একটি `if` expression। আমরা Rust-এ `if` expression কীভাবে কাজ করে তা [“Control Flow”][control-flow]<!-- ignore --> section-এ আলোচনা করব।

#### The Character Type

Rust-এর `char` type হলো language-টির সবচেয়ে primitive alphabetic type। এখানে `char` value declare করার কিছু উদাহরণ দেওয়া হলো:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let c = 'z';
    let z: char = 'ℤ'; // with explicit type annotation
    let heart_eyed_cat = '😻';
}
```

লক্ষ্য করো যে আমরা `char` literal গুলো single quotation mark দিয়ে specify করি, string literal-এর বিপরীতে যেগুলো double quotation mark ব্যবহার করে। Rust-এর `char` type 4 byte size-এর এবং এটি একটি Unicode scalar value represent করে, যার মানে এটি শুধু ASCII-এর চেয়ে অনেক বেশি কিছু represent করতে পারে। Accent সহ অক্ষর; Chinese, Japanese, এবং Korean character; emoji; এবং zero-width space—সবই Rust-এ valid `char` value। Unicode scalar value-গুলোর সীমা `U+0000` থেকে `U+D7FF` এবং `U+E000` থেকে `U+10FFFF` পর্যন্ত (inclusive)। তবে, Unicode-এ “character” সত্যিকার অর্থে কোনো concept নয়, তাই একটি “character” কী সে সম্পর্কে তোমার মানুষিক ধারণা হয়তো Rust-এর `char`-এর সাথে মিলবে না। আমরা এই topic নিয়ে Chapter 8-এর [“Storing UTF-8 Encoded Text with Strings”][strings]<!-- ignore -->-এ বিস্তারিত আলোচনা করব।

### Compound Types

_compound type_-গুলো একাধিক value-কে একটি type-এ একত্রিত করতে পারে। Rust-এ দুটি primitive compound type আছে: tuple এবং array।

#### The Tuple Type

একটি _tuple_ হলো বিভিন্ন type-এর অনেকগুলো value-কে একটি compound type-এ একত্রিত করার একটি সাধারণ উপায়। Tuple-এর length fixed: একবার declare হয়ে গেলে, সেগুলোর size বাড়তে বা কমতে পারে না।

আমরা parentheses-এর ভেতরে comma দিয়ে আলাদা করা value-এর তালিকা লিখে একটি tuple তৈরি করি। Tuple-এর প্রতিটি position-এর একটি type থাকে, এবং tuple-এর বিভিন্ন value-গুলোর type এক হওয়ার দরকার নেই। এই উদাহরণে আমরা optional type annotation যোগ করেছি:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let tup: (i32, f64, u8) = (500, 6.4, 1);
}
```

`tup` variable-টি পুরো tuple-এর সাথে bind হয় কারণ একটি tuple-কে একটি একক compound element হিসেবে ধরা হয়। একটি tuple থেকে আলাদা আলাদা value বের করতে আমরা pattern matching ব্যবহার করে একটি tuple value destructure করতে পারি, এভাবে:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let tup = (500, 6.4, 1);

    let (x, y, z) = tup;

    println!("The value of y is: {y}");
}
```

এই program প্রথমে একটি tuple তৈরি করে এবং সেটিকে `tup` variable-এর সাথে bind করে। তারপর এটি `let` দিয়ে একটি pattern ব্যবহার করে `tup`-কে নিয়ে তাকে তিনটি আলাদা variable—`x`, `y`, এবং `z`—এ পরিণত করে। একে _destructuring_ বলা হয় কারণ এটি একক tuple-টিকে তিন ভাগে ভাঙে। সবশেষে, program `y`-এর value print করে, যা `6.4`।

আমরা একটি tuple element-কে সরাসরি একটি period (`.`) এবং তারপর আমরা যে value-টি access করতে চাই তার index দিয়েও access করতে পারি। যেমন:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let x: (i32, f64, u8) = (500, 6.4, 1);

    let five_hundred = x.0;

    let six_point_four = x.1;

    let one = x.2;
}
```

এই program-টি `x` tuple তৈরি করে এবং তারপর তাদের নিজ নিজ index ব্যবহার করে tuple-এর প্রতিটি element access করে। বেশিরভাগ programming language-এর মতোই, একটি tuple-এ প্রথম index হলো 0।

কোনো value ছাড়া tuple-টির একটি বিশেষ নাম আছে, _unit_। এই value এবং এর সংশ্লিষ্ট type দুটোকেই `()` লেখা হয় এবং এগুলো একটি empty value বা empty return type represent করে। কোনো expression যদি অন্য কোনো value return না করে তবে সে implicit ভাবে unit value return করে।

#### The Array Type

একাধিক value-এর collection রাখার আরেকটি উপায় হলো _array_। Tuple-এর বিপরীতে, একটি array-র প্রতিটি element-এর type একই হতে হবে। অন্যান্য কিছু language-এর array-এর বিপরীতে, Rust-এর array-এর length fixed।

আমরা একটি array-র value গুলো square brackets-এর ভেতরে comma দিয়ে আলাদা করা তালিকা হিসেবে লিখি:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let a = [1, 2, 3, 4, 5];
}
```

Array তখন কার্যকর যখন তুমি চাও তোমার data stack-এ allocate হোক, যেমনটা আমরা এ পর্যন্ত দেখেছি অন্যান্য type-গুলোর ক্ষেত্রে, heap-এর বদলে (আমরা stack আর heap নিয়ে আরও আলোচনা করব [Chapter 4][stack-and-heap]<!-- ignore -->-এ) অথবা যখন তুমি নিশ্চিত করতে চাও যে তোমার সবসময় একটি নির্দিষ্ট সংখ্যক element আছে। তবে array, vector type-এর মতো সেটা পরিমাণে flexible নয়। Vector হলো standard library দ্বারা provide করা একই রকমের একটি collection type যাকে বড় বা ছোট হওয়ার অনুমতি _আছে_ কারণ এর content heap-এ থাকে। তুমি যদি নিশ্চিত না হও যে array ব্যবহার করবে নাকি vector, সম্ভবত তোমার vector ব্যবহার করা উচিত। [Chapter 8][vectors]<!-- ignore --> vector নিয়ে আরও বিস্তারিত আলোচনা করে।

তবে array তখন বেশি কার্যকর যখন তুমি জানো element-এর সংখ্যা পরিবর্তনের দরকার হবে না। যেমন, যদি তুমি কোনো program-এ মাসের নাম ব্যবহার করো, তাহলে সম্ভবত তুমি vector-এর বদলে array ব্যবহার করবে কারণ তুমি জানো এতে সবসময় 12টি element থাকবে:

```rust
let months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];
```

তুমি একটি array-র type square brackets দিয়ে লিখবে—প্রতিটি element-এর type, একটি semicolon, এবং তারপর array-তে element-এর সংখ্যা, এভাবে:

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```

এখানে, `i32` হলো প্রতিটি element-এর type। Semicolon-এর পরে, `5` number-টি নির্দেশ করে যে array-তে পাঁচটি element আছে।

তুমি একটি array-কে এমনভাবেও initialize করতে পারো যাতে প্রতিটি element-এর জন্য একই value থাকে—initial value, একটি semicolon, এবং তারপর square brackets-এ array-র length specify করে, যেমন এখানে দেখানো হয়েছে:

```rust
let a = [3; 5];
```

`a` নামের array-টিতে `5`টি element থাকবে যেগুলোর প্রতিটির initial value `3` হবে। এটি `let a = [3, 3, 3, 3, 3];` লেখার সমান, কিন্তু আরও সংক্ষিপ্তভাবে।

<!-- Old headings. Do not remove or links may break. -->
<a id="accessing-array-elements"></a>

#### Array Element Access

একটি array হলো পরিচিত এবং fixed size এর মেমরির একটি একক অংশ যা stack-এ allocate করা যায়। তুমি indexing ব্যবহার করে array-র element access করতে পারো, এভাবে:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let a = [1, 2, 3, 4, 5];

    let first = a[0];
    let second = a[1];
}
```

এই উদাহরণে, `first` নামের variable-টি `1` value পাবে কারণ সেটি array-তে `[0]` index-এর value। `second` নামের variable-টি array-তে `[1]` index থেকে `2` value পাবে।

#### Invalid Array Element Access

চলো দেখি কী হয় যদি তুমি কোনো array-র শেষের বাইরের কোনো element access করার চেষ্টা করো। ধরো তুমি Chapter 2-এর guessing game-এর মতো ব্যবহারকারীর কাছ থেকে একটি array index পাওয়ার জন্য এই code টি run করো:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,panics
use std::io;

fn main() {
    let a = [1, 2, 3, 4, 5];

    println!("Please enter an array index.");

    let mut index = String::new();

    io::stdin()
        .read_line(&mut index)
        .expect("Failed to read line");

    let index: usize = index
        .trim()
        .parse()
        .expect("Index entered was not a number");

    let element = a[index];

    println!("The value of the element at index {index} is: {element}");
}
```

এই code সফলভাবে compile হয়। যদি তুমি এই code `cargo run` দিয়ে run করো এবং `0`, `1`, `2`, `3`, বা `4` input করো, তবে program সেই index-এর সংশ্লিষ্ট value print করবে। কিন্তু তুমি যদি array-র শেষের বাইরের কোনো number দাও, যেমন `10`, তাহলে নিচের মতো output দেখবে:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access
cargo run
10
-->

```console
thread 'main' panicked at src/main.rs:19:19:
index out of bounds: the len is 5 but the index is 10
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Indexing operation-এ invalid value ব্যবহারের কারণে program-টি runtime error-এ পরিণত হলো। Program একটি error message দিয়ে exit করল এবং শেষ `println!` statement-টি execute করল না। তুমি যখন indexing ব্যবহার করে কোনো element access করার চেষ্টা করো, তখন Rust check করবে যে তুমি যে index specify করেছ সেটি array-র length-এর চেয়ে ছোট কি না। যদি index টি length-এর সমান বা তার চেয়ে বড় হয়, Rust panic করবে। এই check টি runtime-এ হতেই হবে, বিশেষ করে এই ক্ষেত্রে, কারণ compiler সম্ভব না জানতে পারে যে ব্যবহারকারী পরে code run করার সময় কোন value input করবে।

এটি Rust-এর memory safety principle-গুলো কাজে দেখার একটি উদাহরণ। অনেক low-level language-এ এই ধরনের check করা হয় না, এবং তুমি ভুল index দিলে invalid memory access করা যেতে পারে। Rust memory access-এর অনুমতি দিয়ে চালিয়ে যাওয়ার বদলে সাথে সাথে exit করে এই ধরনের error-এর বিরুদ্ধে তোমাকে রক্ষা করে। Chapter 9 Rust-এর error handling এবং কীভাবে তুমি পড়তে সহজ, নিরাপদ code লিখবে যা না panic করে আবার invalid memory access-ও করতে দেয় না, তার আরও আলোচনা করে।

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[twos-complement]: https://en.wikipedia.org/wiki/Two%27s_complement
[control-flow]: ch03-05-control-flow.html#control-flow
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[stack-and-heap]: ch04-01-what-is-ownership.html#the-stack-and-the-heap
[vectors]: ch08-01-vectors.html
[unrecoverable-errors-with-panic]: ch09-01-unrecoverable-errors-with-panic.html
[appendix_b]: appendix-02-operators.md

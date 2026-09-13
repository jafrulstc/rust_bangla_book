## Generic Data Types

আমরা function signature বা struct-এর মতো item-এর definition তৈরি করতে generics ব্যবহার করি, যা তারপর অনেক ভিন্ন concrete data type-এর সাথে ব্যবহার করা যায়। চলো প্রথমে দেখি কীভাবে function, struct, enum এবং method-এ generics ব্যবহার করে define করতে হয়। তারপর আলোচনা করবো generics code-এর performance-এর উপর কী প্রভাব ফেলে।

### In Function Definitions

Generics ব্যবহার করে এমন একটি function define করার সময়, আমরা function-এর signature-এ যেখানে সাধারণত parameter ও return value-র data type specify করি সেখানে generics-কে স্থাপন করি। এটি আমাদের code-কে আরও flexible করে এবং function-এর caller-কে আরও বেশি functionality দেয়, অথচ code duplication রোধ করে।

আমাদের `largest` function-এর ধারা অব্যাহত রেখে, Listing 10-4 দুটি function দেখায় যেগুলো দুটোই একটি slice-এর মধ্যে সবচেয়ে বড় value খুঁজে বের করে। এরপর আমরা এগুলোকে একটি single function-এ একত্রিত করবো যা generics ব্যবহার করে।

<Listing number="10-4" file-name="src/main.rs" caption="Two functions that differ only in their names and in the types in their signatures">

```rust
fn largest_i32(list: &[i32]) -> &i32 {
    let mut largest = &list[0];

    for item in list {
        if item > largest {
            largest = item;
        }
    }

    largest
}

fn largest_char(list: &[char]) -> &char {
    let mut largest = &list[0];

    for item in list {
        if item > largest {
            largest = item;
        }
    }

    largest
}

fn main() {
    let number_list = vec![34, 50, 25, 100, 65];

    let result = largest_i32(&number_list);
    println!("The largest number is {result}");

    let char_list = vec!['y', 'm', 'a', 'q'];

    let result = largest_char(&char_list);
    println!("The largest char is {result}");
}
```

</Listing>

`largest_i32` function-টি হলো সেটিই যা আমরা Listing 10-3-এ extract করেছিলাম, যা একটি slice-এ সবচেয়ে বড় `i32` খুঁজে বের করে। `largest_char` function-টি একটি slice-এ সবচেয়ে বড় `char` খুঁজে বের করে। দুটো function-এর body-তেই একই code আছে, তাই চলো একটি single function-এ generic type parameter ব্যবহার করে সেই duplication দূর করি।

একটি নতুন single function-এ type-গুলোকে parameterize করতে, আমাদের type parameter-এর একটি নাম দিতে হবে, ঠিক যেমন আমরা function-এর value parameter-এর জন্য করি। তুমি যেকোনো identifier কে type parameter নাম হিসেবে ব্যবহার করতে পারো। কিন্তু আমরা `T` ব্যবহার করবো, কারণ রীতি অনুসারে, Rust-এ type parameter নামগুলো ছোট হয়, প্রায়শই একটি মাত্র অক্ষর, এবং Rust-এর type-naming convention হলো UpperCamelCase। _type_-এর সংক্ষিপ্ত রূপ হিসেবে `T` বেশিরভাগ Rust programmer-এর ডিফল্ট পছন্দ।

যখন আমরা একটি parameter function-ের body-তে ব্যবহার করি, তখন আমাদের parameter-এর নাম signature-এ declare করতে হয় যাতে compiler বুঝতে পারে সেই নামের অর্থ কী। একইভাবে, যখন আমরা একটি function signature-এ type parameter নাম ব্যবহার করি, তখন আমাদের সেই type parameter নামটি ব্যবহারের আগে declare করতে হয়। Generic `largest` function define করতে, আমরা function-এর নাম এবং parameter list-এর মাঝে angle bracket `<>`-এর ভেতর type নাম declaration স্থাপন করি, এভাবে:

```rust,ignore
fn largest<T>(list: &[T]) -> &T {
```

আমরা এই definition-টিকে এভাবে পড়ি—"Function `largest` কোনো এক type `T`-এর উপর generic।" এই function-এ `list` নামের একটি parameter আছে, যা `T` type-এর value-গুলোর একটি slice। `largest` function একই type `T`-এর একটি value-র reference return করবে।

Listing 10-5 দেখায় স্বাক্ষরে generic data type ব্যবহার করে একত্রিত `largest` function definition। Listing-টি আরও দেখায় কীভাবে আমরা এই function-কে `i32` value অথবা `char` value-র slice দিয়ে call করতে পারি। মনে রেখো এই code এখনও compile হবে না।

<Listing number="10-5" file-name="src/main.rs" caption="The `largest` function using generic type parameters; this doesn’t compile yet">

```rust,ignore,does_not_compile
fn largest<T>(list: &[T]) -> &T {
    let mut largest = &list[0];

    for item in list {
        if item > largest {
            largest = item;
        }
    }

    largest
}

fn main() {
    let number_list = vec![34, 50, 25, 100, 65];

    let result = largest(&number_list);
    println!("The largest number is {result}");

    let char_list = vec!['y', 'm', 'a', 'q'];

    let result = largest(&char_list);
    println!("The largest char is {result}");
}
```

</Listing>

আমরা যদি এই code টি এখন compile করি, তাহলে এই error পাবো:

```console
$ cargo run
   Compiling chapter10 v0.1.0 (file:///projects/chapter10)
error[E0369]: binary operation `>` cannot be applied to type `&T`
 --> src/main.rs:5:17
  |
5 |         if item > largest {
  |            ---- ^ ------- &T
  |            |
  |            &T
  |
help: consider restricting type parameter `T` with trait `PartialOrd`
  |
1 | fn largest<T: std::cmp::PartialOrd>(list: &[T]) -> &T {
  |             ++++++++++++++++++++++

For more information about this error, try `rustc --explain E0369`.
error: could not compile `chapter10` (bin "chapter10") due to 1 previous error
```

help text-এ `std::cmp::PartialOrd`-এর কথা বলা হয়েছে, যা একটি trait, এবং আমরা পরের section-এ trait নিয়ে আলোচনা করবো। এখন শুধু এটুকু জেনো যে এই error-টি বলছে `largest`-এর body সেই সব সম্ভাব্য type-এর জন্য কাজ করবে না যেগুলো `T` হতে পারে। যেহেতু আমরা body-তে `T` type-এর value compare করতে চাই, তাই আমরা শুধুমাত্র এমন type ব্যবহার করতে পারবো যাদের value-কে order করা যায়। Comparison enable করতে, standard library-তে `std::cmp::PartialOrd` trait আছে যা তুমি type-এর উপর implement করতে পারো (এই trait সম্পর্কে বিস্তারিত জানতে Appendix C দেখো)। Listing 10-5 fix করতে, আমরা help text-এর পরামর্শ অনুসরণ করে `T`-র জন্য valid type-গুলোকে শুধুমাত্র সেইসব type-এ সীমাবদ্ধ করতে পারি যেগুলো `PartialOrd` implement করে। তাহলে listing-টি compile হবে, কারণ standard library `PartialOrd` কে `i32` ও `char` উভয়ের উপরই implement করে।

### In Struct Definitions

আমরা `<>` syntax ব্যবহার করে এক বা একাধিক field-এ generic type parameter ব্যবহার করতে ও struct define করতে পারি। Listing 10-6 একটি `Point<T>` struct define করে যা যেকোনো type-এর `x` ও `y` coordinate value ধারণ করে।

<Listing number="10-6" file-name="src/main.rs" caption="A `Point<T>` struct that holds `x` and `y` values of type `T`">

```rust
struct Point<T> {
    x: T,
    y: T,
}

fn main() {
    let integer = Point { x: 5, y: 10 };
    let float = Point { x: 1.0, y: 4.0 };
}
```

</Listing>

struct definition-এ generics ব্যবহারের syntax function definition-এ ব্যবহৃত syntax-এর মতোই। প্রথমে, আমরা struct-এর নামের ঠিক পরে angle bracket-এর ভেতর type parameter-এর নাম declare করি। তারপর, struct definition-ে যেখানে অন্যথায় আমরা concrete data type specify করতাম, সেখানে আমরা generic type ব্যবহার করি।

মনে রেখো, যেহেতু আমরা `Point<T>` define করতে শুধু একটি generic type ব্যবহার করেছি, এই definition বলে যে `Point<T>` struct কোনো এক type `T`-এর উপর generic, এবং field `x` ও `y` _দুটোই_ সেই একই type—type-টি যেটাই হোক না কেন। যদি আমরা `Point<T>`-র এমন একটি instance তৈরি করি যার ভিন্ন ভিন্ন type-এর value আছে, Listing 10-7-এর মতো, তাহলে আমাদের code compile হবে না।

<Listing number="10-7" file-name="src/main.rs" caption="The fields `x` and `y` must be the same type because both have the same generic data type `T`.">

```rust,ignore,does_not_compile
struct Point<T> {
    x: T,
    y: T,
}

fn main() {
    let wont_work = Point { x: 5, y: 4.0 };
}
```

</Listing>

এই উদাহরণে, যখন আমরা পূর্ণসংখ্যা value `5` কে `x`-এ assign করি, তখন আমরা compiler-কে জানাই যে `Point<T>`-র এই instance-এর জন্য generic type `T` একটি পূর্ণসংখ্যা হবে। তারপর, যখন আমরা `y`-এর জন্য `4.0` specify করি, যাকে আমরা `x`-এর সমান type হিসেবে define করেছি, তখন আমরা এই রকম একটি type mismatch error পাবো:

```console
$ cargo run
   Compiling chapter10 v0.1.0 (file:///projects/chapter10)
error[E0308]: mismatched types
 --> src/main.rs:7:38
  |
7 |     let wont_work = Point { x: 5, y: 4.0 };
  |                                      ^^^ expected integer, found floating-point number

For more information about this error, try `rustc --explain E0308`.
error: could not compile `chapter10` (bin "chapter10") due to 1 previous error
```

এমন একটি `Point` struct define করতে যেখানে `x` ও `y` দুটোই generic কিন্তু ভিন্ন type হতে পারে, আমরা একাধিক generic type parameter ব্যবহার করতে পারি। উদাহরণস্বরূপ, Listing 10-8-এ, আমরা `Point`-র definition পরিবর্তন করে `T` ও `U` type-এর উপর generic করি যেখানে `x` হলো `T` type এবং `y` হলো `U` type।

<Listing number="10-8" file-name="src/main.rs" caption="A `Point<T, U>` generic over two types so that `x` and `y` can be values of different types">

```rust
struct Point<T, U> {
    x: T,
    y: U,
}

fn main() {
    let both_integer = Point { x: 5, y: 10 };
    let both_float = Point { x: 1.0, y: 4.0 };
    let integer_and_float = Point { x: 5, y: 4.0 };
}
```

</Listing>

এখন দেখানো `Point`-র সব instance-ই allowed! তুমি একটি definition-ে যত খুশি তত generic type parameter ব্যবহার করতে পারো, কিন্তু কয়েকটির বেশি ব্যবহার করলে তোমার code পড়তে কঠিন হয়ে যায়। তোমার code-এ অনেক generic type-এর প্রয়োজন হলে, সেটি ইঙ্গিত দেয় যে তোমার code-কে ছোট ছোট অংশে পুনর্গঠন করা প্রয়োজন।

### In Enum Definitions

যেমনটা struct-এর সাথে করেছি, আমরা enum-ও define করতে পারি যাদের variant-এ generic data type ধারণ করে। চলো আরেকবার standard library থেকে প্রাপ্ত `Option<T>` enum-টি দেখি, যা আমরা Chapter 6-এ ব্যবহার করেছি:

```rust
enum Option<T> {
    Some(T),
    None,
}
```

এই definition এখন তোমার কাছে বেশি অর্থবহ মনে হওয়া উচিত। যেমন দেখতে পাচ্ছো, `Option<T>` enum `T` type-এর উপর generic এবং এর দুটি variant আছে: `Some`, যা `T` type-ের একটি value ধারণ করে, এবং একটি `None` variant যা কোনো value ধারণ করে না। `Option<T>` enum ব্যবহার করে আমরা optional value-র বিমূর্ত concept-টি প্রকাশ করতে পারি, এবং যেহেতু `Option<T>` generic, তাই optional value-র type যেটাই হোক না কেন আমরা এই abstraction ব্যবহার করতে পারি।

Enum-এ একাধিক generic type-ও ব্যবহার করা যায়। Chapter 9-এ আমরা যে `Result` enum-এর definition ব্যবহার করেছি তা একটি উদাহরণ:

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

`Result` enum দুটি type—`T` ও `E`-এর উপর generic, এবং এর দুটি variant আছে: `Ok`, যা `T` type-এর একটি value ধারণ করে, এবং `Err`, যা `E` type-এর একটি value ধারণ করে। এই definition-এর কারণে যেকোনো জায়গায় আমরা যেখানে এমন একটি operation আছে যা সফল হতে পারে (কোনো এক type `T`-এর value return করবে) অথবা ব্যর্থ হতে পারে (কোনো এক type `E`-এর error return করবে), সেখানে `Result` enum ব্যবহার করা সুবিধাজনক। আসলে, এটাই আমরা Listing 9-3-তে একটি file open করতে ব্যবহার করেছি, যেখানে file সফলভাবে open হলে `T`-র জায়গায় `std::fs::File` type বসতো এবং file open করতে সমস্যা হলে `E`-র জায়গায় `std::io::Error` type বসতো।

তোমার code-এ এমন পরিস্থিতি চিনতে পারলে যেখানে একাধিক struct বা enum definition শুধুমাত্র তারা যে value ধারণ করে তার type-এ আলাদা, তুমি generic type ব্যবহার করে duplication এড়াতে পারো।

### In Method Definitions

আমরা struct ও enum-এর উপর method implement করতে পারি (যেমন Chapter 5-এ করেছি) এবং সেগুলোর definition-এও generic type ব্যবহার করতে পারি। Listing 10-9 দেখায় Listing 10-6-এ আমরা যে `Point<T>` struct define করেছিলাম তার উপর `x` নামের একটি method implement করা হলো।

<Listing number="10-9" file-name="src/main.rs" caption="Implementing a method named `x` on the `Point<T>` struct that will return a reference to the `x` field of type `T`">

```rust
struct Point<T> {
    x: T,
    y: T,
}

impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }
}

fn main() {
    let p = Point { x: 5, y: 10 };

    println!("p.x = {}", p.x());
}
```

</Listing>

এখানে, আমরা `Point<T>`-র উপর `x` নামের একটি method define করেছি যা `x` field-এর data-র একটি reference return করে।

মনে রেখো, আমাদের `impl`-এর ঠিক পরে `T` declare করতে হবে যাতে আমরা `T` ব্যবহার করে specify করতে পারি যে আমরা `Point<T>` type-এর উপর method implement করছি। `impl`-এর পরে `T`-কে generic type হিসেবে declare করার মাধ্যমে, Rust বুঝতে পারে যে `Point`-এর angle bracket-এ থাকা type-টি একটি generic type, কোনো concrete type নয়। আমরা চাইলে এই generic parameter-এর জন্য struct definition-এ declare করা generic parameter-এর চেয়ে ভিন্ন নাম বেছে নিতে পারতাম, কিন্তু একই নাম ব্যবহার করাই রীতি। যদি তুমি এমন একটি `impl`-এর ভেতরে কোনো method লেখো যা generic type declare করে, সেই method টাইপটির যেকোনো instance-এর জন্য define করা হবে, generic type-এর জায়গায় যে concrete type পরিশেষে বসবে তা যেটাই হোক না কেন।

আমরা একটি type-এর উপর method define করার সময় generic type-এর উপর constraint-ও specify করতে পারি। উদাহরণস্বরূপ, আমরা যেকোনো generic type-এর `Point<T>` instance-এর বদলে শুধুমাত্র `Point<f32>` instance-এর উপর method implement করতে পারি। Listing 10-10-তে, আমরা concrete type `f32` ব্যবহার করি, যার মানে আমরা `impl`-এর পরে কোনো type declare করি না।

<Listing number="10-10" file-name="src/main.rs" caption="An `impl` block that only applies to a struct with a particular concrete type for the generic type parameter `T`">

```rust
impl Point<f32> {
    fn distance_from_origin(&self) -> f32 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
}
```

</Listing>

এই code-এর মানে হলো `Point<f32>` type-এর একটি `distance_from_origin` method থাকবে; `Point<T>`-র অন্যান্য instance যেখানে `T`-র type `f32` নয় সেগুলোর ক্ষেত্রে এই method define করা থাকবে না। এই method পরিমাপ করে আমাদের point (0.0, 0.0) coordinate-এর point থেকে কতদূরে আছে এবং এমন কিছু mathematical operation ব্যবহার করে যা শুধুমাত্র floating-point type-এর জন্য available।

Struct definition-এ generic type parameter-গুলো সবসময় সেই struct-এর method signature-এ ব্যবহৃত parameter-গুলোর সমান হয় না। Listing 10-11 `Point` struct-এর জন্য `X1` ও `Y1` generic type এবং `mixup` method signature-এর জন্য `X2` ও `Y2` generic type ব্যবহার করে উদাহরণটিকে পরিষ্কার করে। এই method `self` `Point`-এর (যার type `X1`) `x` value এবং পাস করা `Point`-এর (যার type `Y2`) `y` value নিয়ে একটি নতুন `Point` instance তৈরি করে।

<Listing number="10-11" file-name="src/main.rs" caption="A method that uses generic types that are different from its struct’s definition">

```rust
struct Point<X1, Y1> {
    x: X1,
    y: Y1,
}

impl<X1, Y1> Point<X1, Y1> {
    fn mixup<X2, Y2>(self, other: Point<X2, Y2>) -> Point<X1, Y2> {
        Point {
            x: self.x,
            y: other.y,
        }
    }
}

fn main() {
    let p1 = Point { x: 5, y: 10.4 };
    let p2 = Point { x: "Hello", y: 'c' };

    let p3 = p1.mixup(p2);

    println!("p3.x = {}, p3.y = {}", p3.x, p3.y);
}
```

</Listing>

`main`-এ, আমরা এমন একটি `Point` define করেছি যার `x` একটি `i32` (value `5`) এবং `y` একটি `f64` (value `10.4`)। `p2` variable হলো এমন একটি `Point` struct যার `x` একটি string slice (value `"Hello"`) এবং `y` একটি `char` (value `c`)। `p1`-এর উপর `p2` argument দিয়ে `mixup` call করলে আমরা `p3` পাই, যার `x` একটি `i32` হবে কারণ `x` এসেছে `p1` থেকে। `p3` variable-এর `y` একটি `char` হবে কারণ `y` এসেছে `p2` থেকে। `println!` macro call টি `p3.x = 5, p3.y = c` print করবে।

এই উদাহরণের উদ্দেশ্য এমন একটি পরিস্থিতি দেখানো যেখানে কিছু generic parameter `impl`-এর সাথে এবং কিছু method definition-এর সাথে declare করা হয়। এখানে, generic parameter `X1` ও `Y1`-কে `impl`-এর পরে declare করা হয়েছে কারণ এগুলো struct definition-এর সাথে যায়। আর generic parameter `X2` ও `Y2`-কে `fn mixup`-এর পরে declare করা হয়েছে কারণ এগুলো শুধুমাত্র method-টির সাথে প্রাসঙ্গিক।

### Performance of Code Using Generics

তুমি হয়তো ভাবছো generic type parameter ব্যবহার করলে কোনো runtime cost আছে কিনা। ভালো খবর হলো generic type ব্যবহার করলে তোমার প্রোগ্রাম concrete type ব্যবহারের চেয়ে বেশি ধীরে চলবে না।

Rust এটি অর্জন করে compile time-এ generics ব্যবহার করা code-এর _monomorphization_ সম্পাদন করার মাধ্যমে। _Monomorphization_ হলো generic code-কে নির্দিষ্ট code-এ রূপান্তর করার প্রক্রিয়া, যেখানে compile করার সময় ব্যবহৃত concrete type-গুলো ভরে দেওয়া হয়। এই প্রক্রিয়ায়, compiler সেই ধাপগুলোর উল্টো কাজ করে যা আমরা Listing 10-5-এ generic function তৈরি করতে ব্যবহার করেছিলাম: compiler সব জায়গা দেখে যেখানে generic code-কে call করা হয়েছে এবং generic code-টি যে concrete type-গুলোর সাথে call করা হয়েছে সেগুলোর জন্য code generate করে।

চলো দেখি এটি কীভাবে কাজ করে, standard library-র generic `Option<T>` enum ব্যবহার করে:

```rust
let integer = Some(5);
let float = Some(5.0);
```

Rust যখন এই code compile করে, তখন এটি monomorphization সম্পাদন করে। সেই প্রক্রিয়ায়, compiler `Option<T>` instance-এ ব্যবহৃত value-গুলো পড়ে এবং দুই ধরনের `Option<T>` চিনে নেয়: একটি হলো `i32` এবং অন্যটি হলো `f64`। এইভাবে, এটি `Option<T>`-র generic definition-কে `i32` ও `f64`-এ বিশেষায়িত দুটি definition-এ প্রসারিত করে, ফলে generic definition-টি specific definition-গুলো দিয়ে প্রতিস্থাপিত হয়।

Code-টির monomorphized version নিচের মতো দেখায় (compiler আমাদের এখানে যে নামগুলো ব্যবহার করেছি তার চেয়ে ভিন্ন নাম ব্যবহার করে):

<Listing file-name="src/main.rs">

```rust
enum Option_i32 {
    Some(i32),
    None,
}

enum Option_f64 {
    Some(f64),
    None,
}

fn main() {
    let integer = Option_i32::Some(5);
    let float = Option_f64::Some(5.0);
}
```

</Listing>

Generic `Option<T>`-কে compiler তৈরি করা specific definition-গুলো দিয়ে প্রতিস্থাপিত করা হয়েছে। যেহেতু Rust প্রতিটি instance-এ type specify করে code-এ প্রসারিত করে দেয়, তাই আমরা generics ব্যবহারের জন্য কোনো runtime cost দিই না। Code যখন চলে, তখন এটি ঠিক এমনভাবেই চলে যেন আমরা প্রতিটি definition নিজে হাতে duplicate করেছি। Monomorphization প্রক্রিয়াটি Rust-এর generics-কে runtime-এ অত্যন্ত efficient করে তোলে।

## Struct ব্যবহার করে একটি উদাহরণ প্রোগ্রাম

কখন আমাদের struct ব্যবহার করতে হতে পারে সেটা বোঝার জন্য, চলো এমন একটি program লিখি যেটা একটি আয়তকার (rectangle) ক্ষেত্রের ক্ষেত্রফল হিসাব করে। আমরা প্রথমে আলাদা আলাদা single variable ব্যবহার করে শুরু করব, তারপর একে একে refactor করে প্রোগ্রামটিকে struct ব্যবহার করার রূপে নিয়ে আসব।

চলো Cargo দিয়ে _rectangles_ নামে একটি নতুন binary project বানাই, যেটা pixel-এ উল্লেখিত একটি rectangle-এর width আর height নেবে আর ঐ rectangle-এর ক্ষেত্রফল হিসাব করবে। Listing 5-8-তে আমাদের project-এর _src/main.rs_-এ ছোট একটি program দেখানো হলো যেটা এই কাজটাই করে।

<Listing number="5-8" file-name="src/main.rs" caption="আলাদা width ও height variable দিয়ে একটি rectangle-এর ক্ষেত্রফল হিসাব করা">

```rust
fn main() {
    let width1 = 30;
    let height1 = 50;

    println!(
        "The area of the rectangle is {} square pixels.",
        area(width1, height1)
    );
}

fn area(width: u32, height: u32) -> u32 {
    width * height
}
```

</Listing>

এখন, এই program-টি `cargo run` দিয়ে চালাও:

```console
$ cargo run
   Compiling rectangles v0.1.0 (file:///projects/rectangles)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.42s
     Running `target/debug/rectangles`
The area of the rectangle is 1500 square pixels.
```

এই কোড প্রতিটি dimension `area` function-এ পাঠিয়ে rectangle-এর ক্ষেত্রফল বের করতে সক্ষম, কিন্তু কোডটিকে আরও পরিষ্কার ও পড়তে সহজ করার উপায় আছে।

এই কোডের সমস্যাটি `area`-র signature-এ স্পষ্ট:

```rust,ignore
fn area(width: u32, height: u32) -> u32 {
```

`area` function-টি একটি rectangle-এর ক্ষেত্রফল হিসাব করার কথা, কিন্তু আমরা যে function লিখেছি তার দুটি parameter আছে, আর আমাদের program-এর কোথাও স্পষ্ট নয় যে এই parameter দুটি পরস্পর সম্পর্কিত। width আর height-কে একসাথে গোছালে কোডটি আরও পড়তে সহজ ও পরিচালনা করা সহজ হতো। আমরা এর আগেই Chapter 3-এর [“The Tuple Type”][the-tuple-type]<!-- ignore --> section-এ এর একটি উপায় আলোচনা করেছি: tuple ব্যবহার করা।

### Tuple দিয়ে Refactor করা

Listing 5-9-তে আমাদের program-এর আরেকটি version দেখানো হলো যেটা tuple ব্যবহার করে।

<Listing number="5-9" file-name="src/main.rs" caption="Tuple দিয়ে rectangle-এর width ও height উল্লেখ করা">

```rust
fn main() {
    let rect1 = (30, 50);

    println!(
        "The area of the rectangle is {} square pixels.",
        area(rect1)
    );
}

fn area(dimensions: (u32, u32)) -> u32 {
    dimensions.0 * dimensions.1
}
```

</Listing>

একটা দিক থেকে এই program-টি আগের চেয়ে ভালো। Tuple আমাদের কিছুটা structure যোগ করতে দেয়, আর এখন আমরা মাত্র একটি argument পাঠাচ্ছি। কিন্তু অন্য দিক থেকে এই version কম স্পষ্ট: Tuple তার element-এর নাম রাখে না, তাই আমাদের tuple-এর অংশগুলোকে index করে access করতে হয়, ফলে আমাদের calculation কম স্পষ্ট হয়ে যায়।

ক্ষেত্রফল হিসাবের ক্ষেত্রে width আর height পরস্পর বিনিময় করলে কোনো সমস্যা নেই, কিন্তু যদি আমরা rectangle-টিকে screen-এ আঁকতে চাইতাম, তাহলে বিষয়টা গুরুত্বপূর্ণ হতো! আমাদের মনে রাখতে হতো যে `width` হলো tuple index `0` আর `height` হলো tuple index `1`। অন্য কেউ যদি আমাদের কোড ব্যবহার করত, তবে তার পক্ষে এটা বুঝে মনে রাখা আরও কঠিন হতো। যেহেতু আমরা আমাদের data-এর অর্থ কোডে তুলে ধরিনি, তাই এখন error ঢুকিয়ে দেওয়া সহজ হয়ে গেছে।

<!-- Old headings. Do not remove or links may break. -->

<a id="refactoring-with-structs-adding-more-meaning"></a>

### Struct দিয়ে Refactor করা

আমরা struct ব্যবহার করে data-কে label দিয়ে অর্থবহ করি। আমরা যে tuple ব্যবহার করছি সেটাকে এমন একটি struct-এ রূপান্তর করতে পারি যার পুরোটার জন্য একটি নাম থাকবে এবং প্রতিটি অংশের জন্যও আলাদা নাম থাকবে, যেমন Listing 5-10-তে দেখানো হয়েছে।

<Listing number="5-10" file-name="src/main.rs" caption="একটি `Rectangle` struct define করা">

```rust
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };

    println!(
        "The area of the rectangle is {} square pixels.",
        area(&rect1)
    );
}

fn area(rectangle: &Rectangle) -> u32 {
    rectangle.width * rectangle.height
}
```

</Listing>

এখানে আমরা একটি struct define করে তার নাম দিয়েছি `Rectangle`। Curly brackets-এর ভেতরে আমরা `width` আর `height` নামের দুটি field define করেছি—দুটোরই type `u32`। তারপর `main`-এ আমরা `Rectangle`-এর একটি নির্দিষ্ট instance তৈরি করেছি যার width `30` আর height `50`।

এখন আমাদের `area` function-টি একটি মাত্র parameter দিয়ে define করা, যার নাম আমরা দিয়েছি `rectangle`—এর type হলো `Rectangle` struct instance-এর immutable borrow। Chapter 4-এ যেমন বলা হয়েছে, আমরা struct-এর ownership নেওয়ার বদলে তাকে borrow করতে চাই। এভাবে `main` নিজের ownership বজায় রাখে আর `rect1` ব্যবহার চালিয়ে যেতে পারে—এ কারণেই আমরা function signature-এ ও function call করার সময় `&` ব্যবহার করি।

`area` function `Rectangle` instance-এর `width` ও `height` field access করে (খেয়াল করো, borrow করা struct instance-এর field access করলে field value move হয় না, তাই আমরা প্রায়ই struct-এর borrow দেখি)। এখন `area`-র function signature ঠিক যা বোঝাতে চাই তা-ই বলছে: `Rectangle`-এর `width` ও `height` field ব্যবহার করে তার ক্ষেত্রফল হিসাব করো। এতে বোঝানো যায় যে width আর height পরস্পর সম্পর্কিত, আর tuple index value `0` বা `1` ব্যবহারের বদলে এই value-গুলোর বর্ণনামূলক নাম দেওয়া হয়েছে। স্পষ্টতার দিক থেকে এটি একটি জয়।

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-useful-functionality-with-derived-traits"></a>

### Derived Trait দিয়ে Functionality যোগ করা

Program debug করার সময় কোনো `Rectangle` instance print করে তার সব field-এর value দেখতে পারলে সুবিধা হতো। Listing 5-11 আগের chapter-গুলোতে যেমন [`println!` macro][println]<!-- ignore --> ব্যবহার করেছি সেটা ব্যবহার করার চেষ্টা করছে। কিন্তু এটা কাজ করবে না।

<Listing number="5-11" file-name="src/main.rs" caption="একটি `Rectangle` instance print করার চেষ্টা">

```rust,ignore,does_not_compile
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };

    println!("rect1 is {rect1}");
}
```

</Listing>

এই কোড compile করার সময় আমরা একটি error পাব, যার মূল message হলো:

```text
error[E0277]: `Rectangle` doesn't implement `std::fmt::Display`
  --> src/main.rs:12:24
   |
12 |     println!("rect1 is {rect1}");
   |                        ^^^^^^^ `Rectangle` cannot be formatted with the default formatter
   |
help: the trait `std::fmt::Display` is not implemented for `Rectangle`
  --> src/main.rs:1:1
   |
 1 | struct Rectangle {
   | ^^^^^^^^^^^^^^^^
   = note: in format strings you may be able to use `{:?}` (or {:#?} for pretty-print) instead

For more information about this error, try `rustc --explain E0277`.
error: could not compile `rectangles` (bin "rectangles") due to 1 previous error
```

`println!` macro বিভিন্ন ধরনের formatting করতে পারে, আর default হিসেবে curly brackets `println!`-কে বলে `Display` নামের formatting ব্যবহার করতে—যেটা সরাসরি end user-এর ব্যবহারের জন্য উদ্দেশ্যপ্রণোদিত output। এ পর্যন্ত আমরা যে primitive type দেখেছি সেগুলো default হিসেবে `Display` implement করে, কারণ একটি `1` বা অন্য কোনো primitive type-কে user-এর কাছে দেখানোর একটাই স্বাভাবিক উপায় আছে। কিন্তু struct-এর ক্ষেত্রে `println!` কীভাবে output format করবে তা ততটা স্পষ্ট নয়, কারণ এখানে আরও বেশি display সম্ভাবনা আছে: তুমি কি comma চাও নাকি চাও না? Curly brackets print করবে নাকি করবে না? সব field দেখানো হবে নাকি নয়? এই অস্পষ্টতার কারণে Rust অনুমান করে বসে না আমরা কী চাই, আর struct-গুলোর সাথে `println!` আর `{}` placeholder-এর জন্য কোনো পূর্ব-প্রস্তুত `Display` implementation দেওয়া থাকে না।

Error-গুলো পড়তে থাকলে আমরা এই সহায়ক note-টি পাব:

```text
help: the trait `std::fmt::Display` is not implemented for `Rectangle`
  --> src/main.rs:1:1
```

চলো চেষ্টা করি! এখন `println!` macro call-টি দাঁড়াবে `println!("rect1 is {rect1:?}");`। Curly brackets-এর ভেতরে `:?` specifier বসালে `println!` বোঝে যে আমরা `Debug` নামের একটি output format ব্যবহার করতে চাই। `Debug` trait আমাদের struct-কে developer-দের কাজে লাগার মতোভাবে print করতে দেয়, যাতে কোড debug করার সময় আমরা এর value দেখতে পাই।

এই পরিবর্তন নিয়ে কোড compile করো। আরে! আমরা এখনও একটি error পাচ্ছি:

```text
error[E0277]: `Rectangle` doesn't implement `Debug`
  --> src/main.rs:12:31
   |
12 |     println!("rect1 is {:?}", rect1);
   |                        ----   ^^^^^ `Rectangle` cannot be formatted using `{:?}` because it doesn't implement `Debug`
   |                        |
   |                        required by this formatting parameter
   |
   = help: the trait `Debug` is not implemented for `Rectangle`
help: consider annotating `Rectangle` with `#[derive(Debug)]`
   |
 1 + #[derive(Debug)]
 2 | struct Rectangle {
   |

For more information about this error, try `rustc --explain E0277`.
error: could not compile `rectangles` (bin "rectangles") due to 1 previous error
```

কিন্তু আবারও compiler একটি সহায়ক note দেয়:

```text
   |                        required by this formatting parameter
   |
```

Rust-এ আসলেই debug তথ্য print করার functionality আছে, কিন্তু আমাদের struct-এর জন্য এই functionality চালু করতে হলে explicitly opt in করতে হবে। সেটা করতে আমরা struct definition-এর ঠিক আগে `#[derive(Debug)]` outer attribute যোগ করি, যেমন Listing 5-12-তে দেখানো হয়েছে।

<Listing number="5-12" file-name="src/main.rs" caption="`Debug` trait derive করার attribute যোগ করা এবং debug formatting দিয়ে `Rectangle` instance print করা">

```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };

    println!("rect1 is {rect1:?}");
}
```

</Listing>

এখন আমরা যখন program চালাব, কোনো error পাব না, আর নিচের output দেখতে পাব:

```console
$ cargo run
   Compiling rectangles v0.1.0 (file:///projects/rectangles)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.48s
     Running `target/debug/rectangles`
rect1 is Rectangle { width: 30, height: 50 }
```

দারুণ! Output খুব সুন্দর নয়, কিন্তু এটি এই instance-এর সব field-এর value দেখায়, যা debugging-এর সময় অবশ্যই কাজে দেবে। যখন struct বড় হবে, তখন একটু পড়তে সহজ output পাওয়া কাজে লাগে; সেসব ক্ষেত্রে আমরা `println!` string-এ `{:?}`-এর বদলে `{:#?}` ব্যবহার করতে পারি। এই উদাহরণে `{:#?}` style ব্যবহার করলে নিচের output পাওয়া যাবে:

```console
$ cargo run
   Compiling rectangles v0.1.0 (file:///projects/rectangles)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.48s
     Running `target/debug/rectangles`
rect1 is Rectangle {
    width: 30,
    height: 50,
}
```

`Debug` format ব্যবহার করে value print করার আরেকটি উপায় হলো [`dbg!` macro][dbg]<!-- ignore --> ব্যবহার করা। এটি একটি expression-এর ownership নেয় (`println!`-এর মতো নয়, যেটা reference নেয়), তোমার কোডে যেখানে সেই `dbg!` macro call হয়েছে তার file ও line number, এবং সেই expression-এর ফলস্বরূপ value print করে, এবং সেই value-র ownership return করে।

> নোট: `dbg!` macro call করলে standard error console stream (`stderr`)-এ print করে, অন্যদিকে `println!` standard output console stream (`stdout`)-এ print করে। `stderr` আর `stdout` সম্পর্কে আরও কথা থাকবে Chapter 12-এর [“Redirecting Errors to Standard Error” section-এ][err]<!-- ignore -->।

এখানে এমন একটি উদাহরণ দেখানো হলো যেখানে আমরা `width` field-এ assign হওয়া value এবং `rect1`-এ পুরো struct-এর value—দুটোর প্রতিই আগ্রহ রাখি:

```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let scale = 2;
    let rect1 = Rectangle {
        width: dbg!(30 * scale),
        height: 50,
    };

    dbg!(&rect1);
}
```

আমরা `dbg!` কে `30 * scale` expression-টির চারপাশে বসাতে পারি, আর যেহেতু `dbg!` expression-এর value-র ownership return করে, তাই `width` field এমন value পাবে যেন সেখানে `dbg!` call-ই নেই। আমরা চাই না `dbg!` যেন `rect1`-এর ownership নিয়ে নেয়, তাই পরের call-এ আমরা `rect1`-এর reference ব্যবহার করি। এই উদাহরণের output দেখতে এরকম:

```console
$ cargo run
   Compiling rectangles v0.1.0 (file:///projects/rectangles)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.61s
     Running `target/debug/rectangles`
[src/main.rs:10:16] 30 * scale = 60
[src/main.rs:14:5] &rect1 = Rectangle {
    width: 60,
    height: 50,
}
```

দেখা যাচ্ছে প্রথম output-টি এসেছে _src/main.rs_-এর line 10 থেকে, যেখানে আমরা `30 * scale` expression debug করছি, আর এর ফল value হলো `60` (integer-এর জন্য implement করা `Debug` formatting শুধু তাদের value print করে)। _src/main.rs_-এর line 14-এর `dbg!` call-টি `&rect1`-এর value output করে, যেটি হলো `Rectangle` struct। এই output `Rectangle` type-এর pretty `Debug` formatting ব্যবহার করে। তোমার কোড কী করছে তা বোঝার চেষ্টা করার সময় `dbg!` macro বেশ কাজে লাগতে পারে!

`Debug` trait ছাড়াও Rust আমাদের custom type-গুলোতে কাজে লাগার মতো behavior যোগ করতে `derive` attribute-এর সাথে ব্যবহারের জন্য আরও বেশ কিছু trait দিয়েছে। সেই trait ও তাদের behavior-এর তালিকা [Appendix C][app-c]<!-- ignore -->-এ দেওয়া আছে। Chapter 10-এ আমরা দেখব কীভাবে এই trait-গুলো custom behavior সহ implement করতে হয় এবং কীভাবে নিজের trait তৈরি করতে হয়। `derive` ছাড়াও আরও অনেক attribute আছে; আরও তথ্যের জন্য [Rust Reference-এর “Attributes” section][attributes] দেখো।

আমাদের `area` function বেশ নির্দিষ্ট: এটি শুধু rectangle-এর ক্ষেত্রফল হিসাব করে। এই behavior-টিকে আমাদের `Rectangle` struct-এর সাথে আরও ঘনিষ্ঠভাবে যুক্ত করতে পারলে সুবিধা হতো, কারণ এটি অন্য কোনো type-এর সাথে কাজ করবে না। চলো দেখি কীভাবে আমরা `area` function-টিকে আমাদের `Rectangle` type-এ define করা একটি `area` method-এ রূপান্তর করে এই কোডটিকে আরও refactor করতে পারি।

[the-tuple-type]: ch03-02-data-types.html#the-tuple-type
[app-c]: appendix-03-derivable-traits.md
[println]: ../std/macro.println.html
[dbg]: ../std/macro.dbg.html
[err]: ch12-06-writing-to-stderr-instead-of-stdout.html
[attributes]: ../reference/attributes.html

## Macros

আমরা এই book জুড়ে `println!`-এর মতো macro ব্যবহার করেছি, কিন্তু একটি macro কী এবং তা কীভাবে কাজ করে তা সম্পূর্ণভাবে explore করিনি। _macro_ term-টি Rust-এ feature-এর একটি family-কে বোঝায়—`macro_rules!` সহ declarative macro এবং তিন ধরনের procedural macro:

- Custom `#[derive]` macro যা struct এবং enum-এর উপর ব্যবহৃত `derive` attribute দিয়ে যোগ করা code specify করে
- Attribute-like macro যা যেকোনো item-এ ব্যবহারযোগ্য custom attribute define করে
- Function-like macro যা function call-এর মতো দেখায় কিন্তু তাদের argument হিসেবে specified token-গুলোর উপর কাজ করে

আমরা এগুলোর প্রতিটি পর্যায়ক্রমে আলোচনা করব, কিন্তু প্রথমে, চলো দেখি যখন আমাদের ইতিমধ্যে function আছে তখন আমরা কেন macro প্রয়োজন।

### The Difference Between Macros and Functions

Fundamentally, macro হলো এমন code লেখার একটি উপায় যা অন্য code লেখে, যাকে _metaprogramming_ বলা হয়। Appendix C-তে, আমরা `derive` attribute আলোচনা করি, যা তোমার জন্য বিভিন্ন trait-এর implementation generate করে। আমরা এই book জুড়ে `println!` এবং `vec!` macro-ও ব্যবহার করেছি। এই সব macro-ই তুমি ম্যানুয়ালি যে code লিখেছো তার চেয়ে বেশি code produce করতে _expand_ হয়।

Metaprogramming তোমার লিখতে এবং maintain করতে হবে এমন code-এর পরিমাণ কমানোর জন্য useful, যা function-গুলোরও একটি role। তবে, macro-গুলোর এমন কিছু অতিরিক্ত power আছে যা function-গুলোর নেই।

একটি function signature-কে অবশ্যই declare করতে হয় function-টির কতগুলো এবং কী type-এর parameter আছে। অন্যদিকে, macro একটি variable সংখ্যক parameter নিতে পারে: আমরা এক argument সহ `println!("hello")` অথবা দুই argument সহ `println!("hello {}", name)` কল করতে পারি। এছাড়াও, macro-গুলো compiler code-এর অর্থ ব্যাখ্যা করার আগে expand হয়, তাই একটি macro উদাহরণস্বরূপ একটি নির্দিষ্ট type-এর উপর একটি trait implement করতে পারে। একটি function পারে না, কারণ এটি runtime-এ call হয় এবং একটি trait-কে compile time-এ implement করতে হয়।

Function-এর বদলে macro implement করার downside হলো macro definition-গুলো function definition-এর চেয়ে বেশি complex কারণ তুমি Rust code লিখছো যা Rust code লেখে। এই indirection-এর কারণে, macro definition সাধারণত function definition-এর চেয়ে পড়তে, বুঝতে এবং maintain করতে বেশি কঠিন।

Macro এবং function-এর মধ্যে আরেকটি গুরুত্বপূর্ণ পার্থক্য হলো তোমাকে একটি file-এ macro define করতে হবে বা সেগুলোকে scope-এ আনতে হবে তুমি সেগুলোকে call করার _আগে_, function-গুলোর বিপরীতে যেগুলো তুমি যেকোনো জায়গায় define করতে পারো এবং যেকোনো জায়গায় call করতে পারো।

<!-- Old headings. Do not remove or links may break. -->

<a id="declarative-macros-with-macro_rules-for-general-metaprogramming"></a>

### Declarative Macros for General Metaprogramming

Rust-এ macro-এর সবচেয়ে widely ব্যবহৃত form হলো _declarative macro_। এগুলোকে কখনো "macros by example," "`macro_rules!` macro," বা শুধু plain "macro" বলা হয়। তাদের core-এ, declarative macro তোমাকে একটি Rust `match` expression-এর মতো কিছু লিখতে দেয়। Chapter 6-এ আলোচনা করা হয়েছে, `match` expression হলো এমন control structure যা একটি expression নেয়, expression-টির resultant value-কে pattern-গুলোর সাথে তুলনা করে, এবং তারপর matching pattern-এর সাথে যুক্ত code run করে। Macro-গুলোও একটি value-কে নির্দিষ্ট code-এর সাথে যুক্ত pattern-গুলোর সাথে তুলনা করে: এই পরিস্থিতিতে, value-টি হলো macro-তে pass করা literal Rust source code; pattern-গুলো source code-টির structure-এর সাথে তুলনা করা হয়; এবং প্রতিটি pattern-এর সাথে যুক্ত code, যখন match করে, macro-তে pass করা code-টিকে replace করে। এই সবকিছু compilation-এর সময় ঘটে।

একটি macro define করতে, তুমি `macro_rules!` construct ব্যবহার করো। চলো `vec!` macro কীভাবে define করা তা দেখে `macro_rules!` ব্যবহার explore করি। Chapter 8 cover করেছে কীভাবে আমরা `vec!` macro ব্যবহার করে নির্দিষ্ট value-সহ একটি নতুন vector তৈরি করতে পারি। উদাহরণস্বরূপ, নিচের macro তিনটি integer ধারণকারী একটি নতুন vector তৈরি করে:

```rust
let v: Vec<u32> = vec![1, 2, 3];
```

আমরা `vec!` macro ব্যবহার করে দুটি integer-এর একটি vector বা পাঁচটি string slice-এর একটি vector-ও তৈরি করতে পারি। আমরা একই কাজ করতে একটি function ব্যবহার করতে পারতাম না কারণ আমরা value-গুলোর সংখ্যা বা type আগে থেকে জানতাম না।

Listing 20-35 `vec!` macro-এর একটি সামান্য simplified definition দেখায়।

<Listing number="20-35" file-name="src/lib.rs" caption="A simplified version of the `vec!` macro definition">

```rust,noplayground
#[macro_export]
macro_rules! vec {
    ( $( $x:expr ),* ) => {
        {
            let mut temp_vec = Vec::new();
            $(
                temp_vec.push($x);
            )*
            temp_vec
        }
    };
}
```

</Listing>

> Note: Standard library-তে `vec!` macro-এর actual definition-এ সঠিক পরিমাণ memory আগে থেকে allocate করার code অন্তর্ভুক্ত। সেই code একটি optimization যা আমরা এখানে include করি না, উদাহরণটি সহজ করতে।

`#[macro_export]` annotation নির্দেশ করে যে যখনই macro-টি যে crate-এ define করা সেটিকে scope-এ আনা হয় তখন এই macro-টিকে available করা উচিত। এই annotation ছাড়া, macro-টিকে scope-এ আনা যাবে না।

তারপর আমরা `macro_rules!` এবং আমরা যে macro-টি define করছি তার নাম দিয়ে macro definition শুরু করি _exclamation mark ছাড়া_। নামটি, এই ক্ষেত্রে `vec`, macro definition-এর body নির্দেশকারী curly bracket দ্বারা অনুসরণ করা হয়।

`vec!` body-তে structure-টি একটি `match` expression-এর structure-এর মতো। এখানে আমাদের একটি arm আছে pattern `( $( $x:expr ),* )` সহ, তারপর `=>` এবং এই pattern-এর সাথে যুক্ত code-এর block। যদি pattern match করে, সংশ্লিষ্ট code block emit করা হবে। যেহেতু এটি এই macro-তে একমাত্র pattern, match করার মাত্র একটি valid উপায় আছে; অন্য যেকোনো pattern error ঘটাবে। আরও complex macro-তে একাধিক arm থাকবে।

Macro definition-এ valid pattern syntax Chapter 19-এ cover করা pattern syntax থেকে ভিন্ন কারণ macro pattern value-এর পরিবর্তে Rust code structure-এর সাথে match করা হয়। চলো Listing 20-29-এ pattern piece-গুলো কী বোঝায় তা পর্যায়ক্রমে দেখি; সম্পূর্ণ macro pattern syntax-এর জন্য, [Rust
Reference][ref] দেখো।

প্রথমে, আমরা সম্পূর্ণ pattern-টিকে encompass করতে parentheses-এর একটি set ব্যবহার করি। আমরা macro system-এ একটি variable declare করতে একটি dollar sign (`$`) ব্যবহার করি যা pattern-এর সাথে match করা Rust code ধারণ করবে। Dollar sign এটি পরিষ্কার করে যে এটি একটি macro variable, regular Rust variable নয়। তারপর parentheses-এর একটি set আসে যা replacement code-তে ব্যবহারের জন্য parentheses-এর ভেতরে pattern-এর সাথে match করা value capture করে। `$()`-এর ভেতরে হলো `$x:expr`, যা যেকোনো Rust expression-এর সাথে match করে এবং expression-টিকে নাম `$x` দেয়।

`$()`-এর পরে comma নির্দেশ করে যে `$()`-এর code-এর সাথে match করা code-এর প্রতিটি instance-এর মধ্যে একটি literal comma separator character থাকতে হবে। `*` specify করে যে pattern-টি `*`-এর আগে যা কিছু আছে তার শূন্য বা ততোধিক সাথে match করে।

যখন আমরা এই macro-টিকে `vec![1, 2, 3];` দিয়ে call করি, `$x` pattern তিনটি expression `1`, `2`, এবং `3` এর সাথে তিনবার match করে।

এখন চলো এই arm-এর সাথে যুক্ত code-এর body-তে pattern-টি দেখি: `$()*`-এর ভেতরের `temp_vec.push()` pattern যতবার match করে ততবার generate হয়, `$()` pattern-টি কতবার match করে তার উপর নির্ভর করে শূন্য বা ততোধিক বার। `$x` প্রতিটি matched expression দিয়ে replace করা হয়। যখন আমরা এই macro-টিকে `vec![1, 2, 3];` দিয়ে call করি, এই macro call-টিকে replace করে যে code generate হয় তা নিচের মতো হবে:

```rust,ignore
{
    let mut temp_vec = Vec::new();
    temp_vec.push(1);
    temp_vec.push(2);
    temp_vec.push(3);
    temp_vec
}
```

আমরা এমন একটি macro define করেছি যা যেকোনো type-এর যেকোনো সংখ্যক argument নিতে পারে এবং specify করা element-গুলো ধারণকারী একটি vector তৈরি করতে code generate করতে পারে।

Macro লেখার বিষয়ে আরও জানতে, online documentation বা অন্যান্য resource-এ consult করো, যেমন Daniel Keep শুরু করে এবং Lukas Wirth continue করেছেন এমন [“The Little Book of Rust Macros”][tlborm]।

### Procedural Macros for Generating Code from Attributes

Macro-এর দ্বিতীয় form হলো procedural macro, যা একটি function-এর মতো বেশি কাজ করে (এবং procedure-এর একটি type)। _Procedural macro_ কিছু code input হিসেবে accept করে, সেই code-এর উপর কাজ করে, এবং কিছু code output হিসেবে produce করে declarative macro-এর মতো pattern-গুলোর সাথে match করে এবং code-কে অন্য code দিয়ে replace করার বদলে। Procedural macro-এর তিন ধরন হলো custom `derive`, attribute-like, এবং function-like, এবং সবগুলো একইভাবে কাজ করে।

Procedural macro তৈরি করার সময়, definition-গুলো অবশ্যই একটি বিশেষ crate type সহ তাদের নিজস্ব crate-এ থাকতে হবে। এটি complex technical কারণে, যা আমরা ভবিষ্যতে eliminate করার আশা করি। Listing 20-36-তে, আমরা দেখাই কীভাবে একটি procedural macro define করতে হয়, যেখানে `some_attribute` একটি নির্দিষ্ট macro variety ব্যবহারের জন্য একটি placeholder।

<Listing number="20-36" file-name="src/lib.rs" caption="An example of defining a procedural macro">

```rust,ignore
use proc_macro::TokenStream;

#[some_attribute]
pub fn some_name(input: TokenStream) -> TokenStream {
}
```

</Listing>

যে function একটি procedural macro define করে সেটি একটি `TokenStream` input হিসেবে নেয় এবং একটি `TokenStream` output হিসেবে produce করে। `TokenStream` type Rust-এর সাথে included থাকা `proc_macro` crate দ্বারা define করা হয় এবং token-গুলোর একটি sequence represent করে। এটি macro-টির core: macro যে source code-এর উপর কাজ করছে সেটি input `TokenStream` তৈরি করে, এবং macro যে code produce করে সেটি output `TokenStream`। Function-টির সাথে একটি attribute যুক্ত থাকে যা specify করে আমরা কোন ধরনের procedural macro তৈরি করছি। একই crate-এ একাধিক ধরনের procedural macro থাকতে পারে।

চলো procedural macro-এর বিভিন্ন ধরন দেখি। আমরা একটি custom `derive` macro দিয়ে শুরু করব এবং তারপর অন্য form-গুলোকে ভিন্ন বানানো ছোট dissimilarity-গুলো ব্যাখ্যা করব।

<!-- Old headings. Do not remove or links may break. -->

<a id="how-to-write-a-custom-derive-macro"></a>

### Custom `derive` Macros

চলো `hello_macro` নামের একটি crate তৈরি করি যা `HelloMacro` নামের একটি trait define করে যার `hello_macro` নামের একটি associated function আছে। আমাদের user-দের প্রতিটি type-এর জন্য `HelloMacro` trait implement করার বদলে, আমরা একটি procedural macro provide করব যাতে user-রা `hello_macro` function-এর একটি default implementation পেতে তাদের type-কে `#[derive(HelloMacro)]` দিয়ে annotate করতে পারে। Default implementation `Hello, Macro! My name is
TypeName!` print করবে যেখানে `TypeName` সেই type-এর নাম যার উপর এই trait define করা হয়েছে। অন্য কথায়, আমরা এমন একটি crate লিখব যা অন্য একজন programmer-কে আমাদের crate ব্যবহার করে Listing 20-37-এর মতো code লিখতে দেয়।

<Listing number="20-37" file-name="src/main.rs" caption="The code a user of our crate will be able to write when using our procedural macro">

```rust,ignore,does_not_compile
use hello_macro::HelloMacro;
use hello_macro_derive::HelloMacro;

#[derive(HelloMacro)]
struct Pancakes;

fn main() {
    Pancakes::hello_macro();
}
```

</Listing>

এই code আমরা শেষ করলে `Hello, Macro! My name is Pancakes!` print করবে। প্রথম step হলো এই মতো একটি নতুন library crate তৈরি করা:

```console
$ cargo new hello_macro --lib
```

তারপর, Listing 20-38-তে, আমরা `HelloMacro` trait এবং এর associated function define করব।

<Listing file-name="src/lib.rs" number="20-38" caption="A simple trait that we will use with the `derive` macro">

```rust,noplayground
pub trait HelloMacro {
    fn hello_macro();
}
```

</Listing>

আমাদের একটি trait এবং এর function আছে। এই মুহূর্তে, আমাদের crate user desired functionality achieve করতে trait implement করতে পারে, যেমন Listing 20-39-তে।

<Listing number="20-39" file-name="src/main.rs" caption="How it would look if users wrote a manual implementation of the `HelloMacro` trait">

```rust,ignore
use hello_macro::HelloMacro;

struct Pancakes;

impl HelloMacro for Pancakes {
    fn hello_macro() {
        println!("Hello, Macro! My name is Pancakes!");
    }
}

fn main() {
    Pancakes::hello_macro();
}
```

</Listing>

তবে, তাদের `hello_macro` সহ ব্যবহার করতে চাই এমন প্রতিটি type-এর জন্য implementation block লিখতে হবে; আমরা তাদের এই কাজ করা থেকে বিরত রাখতে চাই।

এছাড়াও, আমরা এখনো `hello_macro` function-কে এমন default implementation provide করতে পারি না যা trait implement করা type-টির নাম print করবে: Rust-এর reflection capability নেই, তাই এটি runtime-এ type-টির নাম look up করতে পারে না। আমাদের compile time-এ code generate করতে একটি macro প্রয়োজন।

পরবর্তী step হলো procedural macro define করা। এই লেখার সময়ে, procedural macro-গুলোর তাদের নিজস্ব crate-এ থাকতে হবে। সবশেষে, এই restriction তুলে নেওয়া হতে পারে। Crate এবং macro crate structure করার convention নিচের মতো: `foo` নামের একটি crate-এর জন্য, একটি custom `derive` procedural macro crate-কে `foo_derive` বলা হয়। চলো আমাদের `hello_macro` project-এর ভেতরে `hello_macro_derive` নামে একটি নতুন crate শুরু করি:

```console
$ cargo new hello_macro_derive --lib
```

আমাদের দুটি crate tightly related, তাই আমরা আমাদের `hello_macro` crate-এর directory-র ভেতরে procedural macro crate তৈরি করি। যদি আমরা `hello_macro`-তে trait definition পরিবর্তন করি, তবে আমাদের `hello_macro_derive`-তে procedural macro-এর implementation-ও পরিবর্তন করতে হবে। দুটি crate আলাদাভাবে publish করতে হবে, এবং এই crate-গুলো ব্যবহারকারী programmer-দের উভয়কে dependency হিসেবে যোগ করতে এবং উভয়কে scope-এ আনতে হবে। আমরা পরিবর্তে `hello_macro` crate-কে `hello_macro_derive`-কে dependency হিসেবে ব্যবহার করতে এবং procedural macro code-টি re-export করতে বলতে পারতাম। তবে, আমরা যেভাবে project structure করেছি তাতে programmer-রা `hello_macro` ব্যবহার করতে পারবে এমনকি তারা যদি `derive` functionality না চায়।

আমাদের `hello_macro_derive` crate-টিকে procedural macro crate হিসেবে declare করতে হবে। আমাদের একটু পরেই দেখবো হিসেবে `syn` এবং `quote` crate থেকেও functionality প্রয়োজন, তাই আমাদের সেগুলোকে dependency হিসেবে যোগ করতে হবে। `hello_macro_derive`-এর _Cargo.toml_ file-এ নিম্নলিখিত যোগ করো:

<Listing file-name="hello_macro_derive/Cargo.toml">

```toml
[lib]
proc-macro = true

[dependencies]
syn = "2.0"
quote = "1.0"
```

</Listing>

Procedural macro define করা শুরু করতে, `hello_macro_derive` crate-এর জন্য তোমার _src/lib.rs_ file-এ Listing 20-40-এর code রাখো। খেয়াল করো যে আমরা `impl_hello_macro` function-এর জন্য definition না যোগ করা পর্যন্ত এই code compile হবে না।

<Listing number="20-40" file-name="hello_macro_derive/src/lib.rs" caption="Code that most procedural macro crates will require in order to process Rust code">

```rust,ignore,does_not_compile
use proc_macro::TokenStream;
use quote::quote;

#[proc_macro_derive(HelloMacro)]
pub fn hello_macro_derive(input: TokenStream) -> TokenStream {
    // Construct a representation of Rust code as a syntax tree
    // that we can manipulate.
    let ast = syn::parse(input).unwrap();

    // Build the trait implementation.
    impl_hello_macro(&ast)
}
```

</Listing>

খেয়াল করো যে আমরা code-টিকে `hello_macro_derive` function এবং `impl_hello_macro` function-এ ভাগ করেছি, যেখানে প্রথমটি `TokenStream` parse করার জন্য দায়ী, এবং দ্বিতীয়টি syntax tree transform করার জন্য দায়ী: এতে একটি procedural macro লেখা আরও convenient হয়। বাইরের function-এ code (এই ক্ষেত্রে `hello_macro_derive`) তুমি যে বা যা create করবে প্রায় প্রতিটি procedural macro crate-এর জন্য একই থাকবে। ভেতরের function-এর (এই ক্ষেত্রে `impl_hello_macro`) body-তে তুমি যে code specify করবে তা তোমার procedural macro-এর উদ্দেশ্যের উপর নির্ভর করে ভিন্ন হবে।

আমরা তিনটি নতুন crate introduce করেছি: `proc_macro`, [`syn`][syn]<!-- ignore -->, এবং [`quote`][quote]<!-- ignore -->। `proc_macro` crate Rust-এর সাথে আসে, তাই আমাদের সেটি _Cargo.toml_-এ dependency-তে যোগ করার প্রয়োজন ছিল না। `proc_macro` crate হলো compiler-এর API যা আমাদের আমাদের code থেকে Rust code read এবং manipulate করতে দেয়।

`syn` crate একটি string থেকে Rust code parse করে এমন একটি data structure-এ যা আমরা operation করতে পারি। `quote` crate `syn` data structure-গুলোকে আবার Rust code-এ পরিণত করে। এই crate-গুলো আমরা যে কোনো ধরনের Rust code handle করতে চাই তা parse করা অনেক সহজ করে তোলে: Rust code-এর জন্য একটি সম্পূর্ণ parser লেখা কোনো simple task নয়।

আমাদের library-র একজন user যখন একটি type-এর উপর `#[derive(HelloMacro)]` specify করে তখন `hello_macro_derive` function-টি call হবে। এটি সম্ভব কারণ আমরা এখানে `hello_macro_derive` function-টিকে `proc_macro_derive` দিয়ে annotate করেছি এবং নাম `HelloMacro` specify করেছি, যা আমাদের trait নাম-এর সাথে match করে; এটি বেশিরভাগ procedural macro-এর অনুসরণ করা convention।

`hello_macro_derive` function প্রথমে `input`-কে একটি `TokenStream` থেকে এমন একটি data structure-এ রূপান্তর করে যা আমরা interpret করতে এবং operation করতে পারি। এখানেই `syn` কাজে আসে। `syn`-এর `parse` function একটি `TokenStream` নেয় এবং parse করা Rust code represent করে এমন একটি `DeriveInput` struct return করে। Listing 20-41 `struct Pancakes;` string parse করার মাধ্যমে পাওয়া `DeriveInput` struct-এর relevant অংশ-গুলো দেখায়।

<Listing number="20-41" caption="The `DeriveInput` instance we get when parsing the code that has the macro’s attribute in Listing 20-37">

```rust,ignore
DeriveInput {
    // --snip--

    ident: Ident {
        ident: "Pancakes",
        span: #0 bytes(95..103)
    },
    data: Struct(
        DataStruct {
            struct_token: Struct,
            fields: Unit,
            semi_token: Some(
                Semi
            )
        }
    )
}
```

</Listing>

এই struct-এর field-গুলো দেখায় যে আমরা যে Rust code parse করেছি তা একটি unit struct যার `ident` (_identifier_, যার মানে নাম) `Pancakes`। এই struct-এ সব ধরনের Rust code describe করার জন্য আরও field আছে; আরও information-এর জন্য [`syn` documentation for `DeriveInput`][syn-docs] দেখো।

শীঘ্রই আমরা `impl_hello_macro` function define করব, যেখানে আমরা যে নতুন Rust code include করতে চাই তা build করব। কিন্তু তার আগে, খেয়াল করো যে আমাদের `derive` macro-এর output-ও একটি `TokenStream`। Returned `TokenStream` আমাদের crate user-রা যে code লেখে তাতে যোগ করা হয়, তাই তারা যখন তাদের crate compile করবে, তখন তারা modified `TokenStream`-এ আমরা যে extra functionality provide করি তা পাবে।

তুমি হয়তো খেয়াল করেছো যে আমরা `syn::parse` function-এ call fail হলে `hello_macro_derive` function-কে panic করাতে `unwrap` call করছি। আমাদের procedural macro-এর error-এ panic করা প্রয়োজন কারণ `proc_macro_derive` function-গুলোকে procedural macro API মেনে চলতে `Result`-এর পরিবর্তে `TokenStream` return করতে হবে। আমরা `unwrap` ব্যবহার করে এই উদাহরণটি simplified করেছি; production code-এ, তোমার `panic!` বা `expect` ব্যবহার করে কী ভুল হয়েছে তার বিষয়ে আরও specific error message provide করা উচিত।

এখন যেহেতু annotated Rust code-কে একটি `TokenStream` থেকে একটি `DeriveInput` instance-এ রূপান্তর করার code আছে, চলো annotated type-এর উপর `HelloMacro` trait implement করে এমন code generate করি, যেমন Listing 20-42-তে দেখানো হয়েছে।

<Listing number="20-42" file-name="hello_macro_derive/src/lib.rs" caption="Implementing the `HelloMacro` trait using the parsed Rust code">

```rust,ignore
fn impl_hello_macro(ast: &syn::DeriveInput) -> TokenStream {
    let name = &ast.ident;
    let generated = quote! {
        impl HelloMacro for #name {
            fn hello_macro() {
                println!("Hello, Macro! My name is {}!", stringify!(#name));
            }
        }
    };
    generated.into()
}
```

</Listing>

আমরা `ast.ident` ব্যবহার করে annotated type-এর নাম (identifier) ধারণকারী একটি `Ident` struct instance পাই। Listing 20-41-এর struct দেখায় যে যখন আমরা Listing 20-37-এর code-এর উপর `impl_hello_macro` function run করি, আমরা যে `ident` পাব তার `ident` field-এর value `"Pancakes"` থাকবে। সুতরাং, Listing 20-42-তে `name` variable একটি `Ident` struct instance ধারণ করবে যা print করলে string `"Pancakes"` হবে, Listing 20-37-এর struct-এর নাম।

`quote!` macro আমাদের যে Rust code return করতে চাই তা define করতে দেয়। Compiler `quote!` macro-এর execution-এর সরাসরি result থেকে ভিন্ন কিছু expect করে, তাই আমাদের এটিকে একটি `TokenStream`-এ রূপান্তর করতে হবে। আমরা এটি `into` method call করে করি, যা এই intermediate representation consume করে এবং প্রয়োজনীয় `TokenStream` type-এর একটি value return করে।

`quote!` macro কিছু খুব দারুণ templating mechanics-ও provide করে: আমরা `#name` লিখতে পারি, এবং `quote!` এটিকে `name` variable-এর value দিয়ে replace করবে। তুমি regular macro যেভাবে কাজ করে তার মতো কিছু repetition-ও করতে পারো। একটি পুঙ্খানুপুঙ্খ introduction-এর জন্য [the `quote` crate’s docs][quote-docs] দেখো।

আমরা চাই আমাদের procedural macro user যে type-টিকে annotate করেছে তার জন্য আমাদের `HelloMacro` trait-এর একটি implementation generate করুক, যা আমরা `#name` ব্যবহার করে পেতে পারি। Trait implementation-এ একটি function আছে `hello_macro`, যার body-তে আমরা যে functionality provide করতে চাই তা আছে: `Hello, Macro! My name is` এবং তারপর annotated type-এর নাম print করা।

এখানে ব্যবহৃত `stringify!` macro Rust-এ built-in। এটি একটি Rust expression নেয়, যেমন `1 + 2`, এবং compile time-এ expression-টিকে একটি string literal-এ পরিণত করে, যেমন `"1 + 2"`। এটি `format!` বা `println!` থেকে ভিন্ন, যেগুলো macro expression evaluate করে এবং তারপর result-কে একটি `String`-এ পরিণত করে। এমন সম্ভাবনা আছে যে `#name` input হয়তো literally print করার জন্য একটি expression, তাই আমরা `stringify!` ব্যবহার করি। `stringify!` ব্যবহার করা compile time-এ `#name`-কে একটি string literal-এ রূপান্তর করে একটি allocation-ও বাঁচায়।

এই মুহূর্তে, `cargo build` উভয় `hello_macro` এবং `hello_macro_derive`-তে successfully complete করা উচিত। চলো এই crate-গুলোকে Listing 20-37-এর code-এর সাথে hook করি procedural macro-টি action-এ দেখতে! তোমার _projects_ directory-তে `cargo new pancakes` ব্যবহার করে একটি নতুন binary project তৈরি করো। আমাদের `pancakes` crate-এর _Cargo.toml_-এ `hello_macro` এবং `hello_macro_derive`-কে dependency হিসেবে যোগ করতে হবে। তুমি তোমার `hello_macro` এবং `hello_macro_derive`-এর version [crates.io](https://crates.io/)<!-- ignore -->-এ publish করলে, সেগুলো regular dependency হবে; না হলে, তুমি সেগুলোকে নিম্নরূপ `path` dependency হিসেবে specify করতে পারো:

```toml
[dependencies]
hello_macro = { path = "../hello_macro" }
hello_macro_derive = { path = "../hello_macro/hello_macro_derive" }
```

Listing 20-37-এর code _src/main.rs_-এ রাখো, এবং `cargo run` run করো: এটি `Hello, Macro! My name is Pancakes!` print করা উচিত। `HelloMacro` trait-এর implementation procedural macro থেকে include হয়েছে `pancakes` crate-কে এটি implement করার প্রয়োজন ছাড়াই; `#[derive(HelloMacro)]` trait implementation-টি যোগ করেছে।

এরপর, চলো explore করি অন্যান্য ধরনের procedural macro কীভাবে custom `derive` macro থেকে ভিন্ন।

### Attribute-Like Macros

Attribute-like macro গুলো custom `derive` macro-গুলোর মতো, কিন্তু `derive` attribute-এর জন্য code generate করার বদলে, তারা তোমাকে নতুন attribute তৈরি করতে দেয়। তারা আরও flexible: `derive` শুধুমাত্র struct এবং enum-এর জন্য কাজ করে; attribute-গুলো অন্যান্য item-এও apply করা যেতে পারে, যেমন function। এখানে একটি attribute-like macro ব্যবহারের একটি উদাহরণ দেওয়া হলো। ধরা যাক তোমার একটি `route` নামের attribute আছে যা একটি web application framework ব্যবহার করলে function-কে annotate করে:

```rust,ignore
#[route(GET, "/")]
fn index() {
```

এই `#[route]` attribute-টি framework দ্বারা একটি procedural macro হিসেবে define করা হবে। Macro definition function-টির signature এমন দেখাবে:

```rust,ignore
#[proc_macro_attribute]
pub fn route(attr: TokenStream, item: TokenStream) -> TokenStream {
```

এখানে, আমাদের `TokenStream` type-এর দুটি parameter আছে। প্রথমটি attribute-এর contents-এর জন্য: `GET, "/"` অংশ। দ্বিতীয়টি attribute-টি যে item-এর সাথে যুক্ত সেটির body: এই ক্ষেত্রে, `fn index() {}` এবং function-এর body-এর বাকি অংশ।

এছাড়া, attribute-like macro গুলো custom `derive` macro-গুলোর মতোই কাজ করে: তুমি `proc-macro` crate type সহ একটি crate তৈরি করো এবং এমন একটি function implement করো যা তুমি যে code চাই তা generate করে!

### Function-Like Macros

Function-like macro গুলো এমন macro define করে যা function call-এর মতো দেখায়। `macro_rules!` macro-গুলোর মতো, এগুলো function-গুলোর চেয়ে বেশি flexible; উদাহরণস্বরূপ, তারা একটি unknown সংখ্যক argument নিতে পারে। তবে, `macro_rules!` macro-গুলো শুধুমাত্র পূর্বের [“Declarative
Macros for General Metaprogramming”][decl]<!-- ignore --> section-এ আলোচিত match-like syntax ব্যবহার করে define করা যেতে পারে। Function-like macro গুলো একটি `TokenStream` parameter নেয়, এবং তাদের definition অন্য দুই ধরনের procedural macro-গুলোর মতো Rust code ব্যবহার করে সেই `TokenStream` manipulate করে। একটি function-like macro-এর উদাহরণ হলো একটি `sql!` macro যা এভাবে call করা হতে পারে:

```rust,ignore
let sql = sql!(SELECT * FROM posts WHERE id=1);
```

এই macro এর ভেতরে SQL statement parse করবে এবং check করবে যে এটি syntactically correct, যা একটি `macro_rules!` macro যা করতে পারে তার চেয়ে অনেক বেশি complex processing। `sql!` macro এভাবে define করা হবে:

```rust,ignore
#[proc_macro]
pub fn sql(input: TokenStream) -> TokenStream {
```

এই definition custom `derive` macro-এর signature-এর মতো: আমরা parentheses-এর ভেতরে থাকা token গুলো receive করি এবং আমরা যে code generate করতে চাই তা return করি।

## Summary

ফুঃ! এখন তোমার toolbox-এ Rust-এর এমন কিছু feature আছে যা তুমি সম্ভবত প্রায়ই ব্যবহার করবে না, কিন্তু তুমি জানবে যে এগুলো খুব নির্দিষ্ট পরিস্থিতিতে available। আমরা বেশ কিছু complex topic introduce করেছি যাতে তুমি সেগুলো error message suggestion-এ বা অন্যের code-এ encounter করলে এই concept এবং syntax-গুলো চিনতে পারো। তোমাকে solution-এ গাইড করতে এই chapter-টিকে একটি reference হিসেবে ব্যবহার করো।

এরপর, আমরা সারা book জুড়ে আলোচিত সবকিছু practice-এ রাখব এবং আরও একটি project করব!

[ref]: ../reference/macros-by-example.html
[tlborm]: https://veykril.github.io/tlborm/
[syn]: https://crates.io/crates/syn
[quote]: https://crates.io/crates/quote
[syn-docs]: https://docs.rs/syn/2.0/syn/struct.DeriveInput.html
[quote-docs]: https://docs.rs/quote
[decl]: #declarative-macros-with-macro_rules-for-general-metaprogramming

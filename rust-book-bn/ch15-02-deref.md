<!-- Old headings. Do not remove or links may break. -->

<a id="treating-smart-pointers-like-regular-references-with-the-deref-trait"></a>
<a id="treating-smart-pointers-like-regular-references-with-deref"></a>

## Smart Pointer কে Regular Reference-এর মতো বিবেচনা করা

`Deref` trait implement করলে তুমি _dereference operator_ `*`-এর behavior কাস্টমাইজ করতে পারো (গুণ বা glob operator-এর সাথে গুলিয়ে ফেলবে না)। এমনভাবে `Deref` implement করে যাতে একটি smart pointer-কে regular reference-এর মতো বিবেচনা করা যায়, তুমি এমন code লিখতে পারবে যা reference-এ কাজ করে এবং সেই code smart pointer-এর সাথেও কাজ করবে।

চলো আগে দেখি regular reference-এর সাথে dereference operator কীভাবে কাজ করে। তারপর, আমরা `Box<T>`-এর মতো আচরণ করে এমন একটি custom type define করার চেষ্টা করব এবং দেখব কেন dereference operator আমাদের নতুন define করা type-এ reference-এর মতো কাজ করে না। আমরা দেখব `Deref` trait implement করলে কীভাবে smart pointer-গুলো reference-এর অনুরূপভাবে কাজ করতে পারে। তারপর আমরা Rust-এর deref coercion feature দেখব এবং কীভাবে এটি আমাদের reference অথবা smart pointer যেকোনোটির সাথেই কাজ করতে দেয়।

<!-- Old headings. Do not remove or links may break. -->

<a id="following-the-pointer-to-the-value-with-the-dereference-operator"></a>
<a id="following-the-pointer-to-the-value"></a>

### Reference-টি অনুসরণ করে Value-এ যাওয়া

regular reference হলো pointer-এর একটি প্রকার, এবং pointer-কে এমন একটি তীর হিসেবে ভাবা যায় যা অন্য কোথাও store করা কোনো value-কে নির্দেশ করে। Listing 15-6-তে আমরা একটি `i32` value-এর reference তৈরি করি এবং তারপর dereference operator ব্যবহার করে reference-টি অনুসরণ করে value-এ পৌঁছাই।

<Listing number="15-6" file-name="src/main.rs" caption="Using the dereference operator to follow a reference to an `i32` value">

```rust
fn main() {
    let x = 5;
    let y = &x;

    assert_eq!(5, x);
    assert_eq!(5, *y);
}
```

</Listing>

variable `x` একটি `i32` value `5` ধারণ করে। আমরা `y`-কে `x`-এর reference হিসেবে সেট করেছি। আমরা assert করতে পারি যে `x` এর মান `5`। কিন্তু `y`-এর value নিয়ে assertion করতে হলে, আমাদের `*y` ব্যবহার করতে হবে reference-টি অনুসরণ করে যে value-টির দিকে point করছে সেখানে পৌঁছাতে (তাই _dereference_), যাতে compiler actual value-টি compare করতে পারে। একবার `y`-কে dereference করলে, আমরা `y`-এর দিকে নির্দেশ করা integer value-টিতে access পাই যা আমরা `5`-এর সাথে compare করতে পারি।

যদি আমরা এর বদলে `assert_eq!(5, y);` লিখতাম, তাহলে এই compilation error পেতাম:

```console
$ cargo run
   Compiling deref-example v0.1.0 (file:///projects/deref-example)
error[E0277]: can't compare `{integer}` with `&{integer}`
 --> src/main.rs:6:5
  |
6 |     assert_eq!(5, y);
  |     ^^^^^^^^^^^^^^^^ no implementation for `{integer} == &{integer}`
  |
  = help: the trait `PartialEq<&{integer}>` is not implemented for `{integer}`
  = help: the following other types implement trait `PartialEq<Rhs>`:
            f128
            f16
            f32
            f64
            i128
            i16
            i32
            i64
          and 8 others

For more information about this error, try `rustc --explain E0277`.
error: could not compile `deref-example` (bin "deref-example") due to 1 previous error
```

একটি number এবং সেই number-এর reference-এর মধ্যে compare করা allowed নয় কারণ এগুলো ভিন্ন type। আমাদের dereference operator ব্যবহার করতে হবে reference-টি অনুসরণ করে যে value-টির দিকে point করছে সেখানে পৌঁছাতে।

### `Box<T>` কে Reference-এর মতো ব্যবহার করা

আমরা Listing 15-6-এর code-টি reference-এর বদলে `Box<T>` ব্যবহার করে আবার লিখতে পারি; Listing 15-7-এ `Box<T>`-এ ব্যবহৃত dereference operator Listing 15-6-এ reference-এ ব্যবহৃত dereference operator-এর মতোই কাজ করে।

<Listing number="15-7" file-name="src/main.rs" caption="Using the dereference operator on a `Box<i32>`">

```rust
fn main() {
    let x = 5;
    let y = Box::new(x);

    assert_eq!(5, x);
    assert_eq!(5, *y);
}
```

</Listing>

Listing 15-7 এবং Listing 15-6-এর মূল পার্থক্য হলো এখানে আমরা `y`-কে `x`-এর value-কে point করা reference-এর বদলে `x`-এর copied value-কে point করা একটি box instance হিসেবে সেট করেছি। শেষ assertion-এ আমরা dereference operator ব্যবহার করে box-এর pointer অনুসরণ করতে পারি একইভাবে যেভাবে `y` reference থাকলে করতাম। এরপর আমরা দেখব `Box<T>`-এ এমন কী আছে যা আমাদের নিজস্ব box type define করে dereference operator ব্যবহার করতে দেয়।

### আমাদের নিজস্ব Smart Pointer Define করা

চলো standard library-র দেওয়া `Box<T>` type-এর মতো একটি wrapper type বানাই, যাতে আমরা বুঝতে পারি smart pointer type গুলো ডিফল্টভাবে reference-এর থেকে কীভাবে আলাদাভাবে behavior করে। তারপর আমরা দেখব কীভাবে dereference operator ব্যবহার করার ক্ষমতা যোগ করতে হয়।

> নোট: আমরা যে `MyBox<T>` type বানাবো সেটি এবং আসল `Box<T>`-এর মধ্যে একটি বড় পার্থক্য আছে: আমাদের সংস্করণটি তার data heap-এ store করবে না। আমরা এই উদাহরণটি `Deref`-এর দিকে কেন্দ্রিত করেছি, তাই data আসলে কোথায় store করা হচ্ছে সেটা pointer-এর মতো behavior করার চেয়ে কম গুরুত্বপূর্ণ।

`Box<T>` type শেষ পর্যন্ত একটি element সহ একটি tuple struct হিসেবে define করা, তাই Listing 15-8 একইভাবে একটি `MyBox<T>` type define করে। আমরা `Box<T>`-এ define করা `new` function-এর মতো করতে একটি `new` function-ও define করব।

<Listing number="15-8" file-name="src/main.rs" caption="Defining a `MyBox<T>` type">

```rust
struct MyBox<T>(T);

impl<T> MyBox<T> {
    fn new(x: T) -> MyBox<T> {
        MyBox(x)
    }
}
```

</Listing>

আমরা `MyBox` নামের একটি struct define করি এবং generic parameter `T` declare করি কারণ আমরা চাই আমাদের type যেকোনো type-এর value ধারণ করুক। `MyBox` type একটি tuple struct যার একটি element `T` type-এর। `MyBox::new` function একটি `T` type-ের parameter নেয় এবং একটি `MyBox` instance return করে যা পাস করা value ধারণ করে।

চলো Listing 15-7-এর `main` function-টি Listing 15-8-এ যোগ করার চেষ্টা করি এবং `Box<T>`-এর বদলে আমরা define করা `MyBox<T>` type ব্যবহার করতে পরিবর্তন করি। Listing 15-9-এর code compile হবে না, কারণ Rust জানে না `MyBox` কীভাবে dereference করতে হয়।

<Listing number="15-9" file-name="src/main.rs" caption="Attempting to use `MyBox<T>` in the same way we used references and `Box<T>`">

```rust,ignore,does_not_compile
fn main() {
    let x = 5;
    let y = MyBox::new(x);

    assert_eq!(5, x);
    assert_eq!(5, *y);
}
```

</Listing>

এই compilation error-টি পাওয়া যাবে:

```console
$ cargo run
   Compiling deref-example v0.1.0 (file:///projects/deref-example)
error[E0614]: type `MyBox<{integer}>` cannot be dereferenced
  --> src/main.rs:14:19
   |
14 |     assert_eq!(5, *y);
   |                   ^^ can't be dereferenced

For more information about this error, try `rustc --explain E0614`.
error: could not compile `deref-example` (bin "deref-example") due to 1 previous error
```

আমাদের `MyBox<T>` type-টি dereference করা যায় না কারণ আমরা আমাদের type-এ সেই ক্ষমতা implement করিনি। `*` operator দিয়ে dereference সক্ষম করতে আমরা `Deref` trait implement করি।

<!-- Old headings. Do not remove or links may break. -->

<a id="treating-a-type-like-a-reference-by-implementing-the-deref-trait"></a>

### `Deref` Trait Implement করা

Chapter 10-এর [“Implementing a Trait on a Type”][impl-trait]<!-- ignore -->-এ আলোচনা করা হয়েছে, একটি trait implement করতে হলে আমাদের trait-এর required method-গুলোর implementation দিতে হয়। standard library-র দেওয়া `Deref` trait-এ আমাদের `deref` নামের একটি method implement করতে হয় যা `self` কে borrow করে এবং ভেতরের data-এর একটি reference return করে। Listing 15-10-এ `MyBox<T>`-এর definition-এ যোগ করার জন্য `Deref`-এর একটি implementation দেওয়া আছে।

<Listing number="15-10" file-name="src/main.rs" caption="Implementing `Deref` on `MyBox<T>`">

```rust
use std::ops::Deref;

impl<T> Deref for MyBox<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}
```

</Listing>

`type Target = T;` syntax-টি `Deref` trait-এর ব্যবহারের জন্য একটি associated type define করে। associated type হলো generic parameter declare করার একটি সামান্য ভিন্ন উপায়, কিন্তু তোমার এখন এগুলো নিয়ে চিন্তা করার দরকার নেই; আমরা এগুলো Chapter 20-এ আরও বিস্তারিত আলোচনা করব।

আমরা `deref` method-এর body-তে `&self.0` দিয়েছি যাতে `deref` সেই value-এর একটি reference return করে যাতে আমরা `*` operator দিয়ে access করতে চাই; Chapter 5-এর [“Creating Different Types with Tuple Structs”][tuple-structs]<!-- ignore -->-এ মনে করো যে `.0` একটি tuple struct-এর প্রথম value-তে access করে। Listing 15-9-তে `MyBox<T>` value-তে `*` call করা `main` function-টি এখন compile হয়, এবং assertion গুলো pass করে!

`Deref` trait না থাকলে compiler শুধুমাত্র `&` reference dereference করতে পারে। `deref` method compiler-কে এমন যেকোনো type-এর value নেওয়ার ক্ষমতা দেয় যা `Deref` implement করে এবং `deref` method call করে এমন একটি reference পায় যা সে জানে কীভাবে dereference করতে হয়।

Listing 15-9-তে যখন আমরা `*y` লিখেছিলাম, behind the scenes Rust আসলে এই code-টি চালিয়েছিল:

```rust,ignore
*(y.deref())
```

Rust `*` operator-কে `deref` method-এ একটি call দিয়ে এবং তারপর একটি সাধারণ dereference দিয়ে replace করে, যাতে আমাদের ভাবতে না হয় `deref` method call করতে হবে কি না। এই Rust feature আমাদের এমন code লিখতে দেয় যা আমাদের কাছে regular reference থাকলেও অথবা `Deref` implement করে এমন type থাকলেও একইভাবে কাজ করে।

`deref` method কেন একটি value-এর reference return করে এবং `*(y.deref())`-এ বন্ধনীর বাইরের সাধারণ dereference এখনো প্রয়োজনীয়, তার কারণ ownership system-এর সাথে সম্পর্কিত। যদি `deref` method reference-এর বদলে সরাসরি value return করত, তাহলে value-টি `self` থেকে move হয়ে যেত। এই ক্ষেত্রে অথবা dereference operator যেখানে ব্যবহার করি বেশিরভাগ ক্ষেত্রেই আমরা `MyBox<T>`-এর ভেতরের value-এর ownership নিতে চাই না।

মনে রাখবে `*` operator কে আমরা code-এ যতবার `*` ব্যবহার করি ততবার একটি `deref` method call এবং তারপর একবার `*` operator call দিয়ে replace করা হয়। যেহেতু `*` operator-এর substitution অসীমভাবে recurse করে না, আমরা `i32` type-এর data পাই, যা Listing 15-9-এর `assert_eq!`-এর `5`-এর সাথে match করে।

<!-- Old headings. Do not remove or links may break. -->

<a id="implicit-deref-coercions-with-functions-and-methods"></a>
<a id="using-deref-coercions-in-functions-and-methods"></a>

### Function এবং Method-এ Deref Coercion ব্যবহার করা

_deref coercion_ এমন একটি type-এর reference-কে, যা `Deref` trait implement করে, অন্য একটি type-এর reference-এ রূপ নেয়। উদাহরণস্বরূপ, deref coercion `&String`-কে `&str`-এ রূপান্তর করতে পারে কারণ `String` `Deref` trait implement করে যাতে সে `&str` return করে। deref coercion হলো একটি সুবিধা যা Rust function এবং method-এর argument-এ সম্পন্ন করে, এবং এটি শুধুমাত্র সেই type-গুলোতে কাজ করে যা `Deref` trait implement করে। এটি স্বয়ংক্রিয়ভাবে ঘটে যখন আমরা একটি নির্দিষ্ট type-ের value-এর reference কোনো function অথবা method-এর argument হিসেবে pass করি যা function অথবা method definition-এর parameter type-এর সাথে match করে না। `deref` method-এর একটি sequence call আমরা যে type দিয়েছি সেটিকে parameter-এর প্রয়োজনীয় type-এ রূপান্তর করে।

deref coercion Rust-এ যোগ করা হয়েছিল যাতে function এবং method call লেখা programmer-দের `&` এবং `*` দিয়ে অনেক explicit reference এবং dereference যোগ করতে না হয়। deref coercion feature আমাদের আরও বেশি code লেখার সুবিধা দেয় যা reference অথবা smart pointer উভয়ের জন্যই কাজ করে।

deref coercion কাজে দেখতে, চলো Listing 15-8-তে define করা `MyBox<T>` type এবং Listing 15-10-এ যোগ করা `Deref`-এর implementation ব্যবহার করি। Listing 15-11 দেখায় এমন একটি function-এর definition যার একটি string slice parameter আছে।

<Listing number="15-11" file-name="src/main.rs" caption="A `hello` function that has the parameter `name` of type `&str`">

```rust
fn hello(name: &str) {
    println!("Hello, {name}!");
}
```

</Listing>

আমরা `hello` function-কে একটি string slice argument দিয়ে call করতে পারি, যেমন `hello("Rust");`। deref coercion `hello`-কে `MyBox<String>` type-এর value-এর reference দিয়ে call করতে সক্ষম করে, যেমন Listing 15-12-তে দেখানো হয়েছে।

<Listing number="15-12" file-name="src/main.rs" caption="Calling `hello` with a reference to a `MyBox<String>` value, which works because of deref coercion">

```rust
fn main() {
    let m = MyBox::new(String::from("Rust"));
    hello(&m);
}
```

</Listing>

এখানে আমরা `hello` function-কে `&m` argument দিয়ে call করছি, যা `MyBox<String>` value-এর একটি reference। যেহেতু আমরা Listing 15-10-এ `MyBox<T>`-তে `Deref` trait implement করেছি, Rust `deref` call করে `&MyBox<String>`-কে `&String`-এ রূপ দিতে পারে। standard library `String`-এর জন্য `Deref`-এর একটি implementation দেয় যা একটি string slice return করে, এবং এটি `Deref`-এর API documentation-এ আছে। Rust আবার `deref` call করে `&String`-কে `&str`-এ রূপ দেয়, যা `hello` function-এর definition-এর সাথে match করে।

যদি Rust deref coercion implement না করত, তাহলে `&MyBox<String>` type-এর value দিয়ে `hello` call করতে Listing 15-12-এর বদলে আমাদের Listing 15-13-এর code লিখতে হতো।

<Listing number="15-13" file-name="src/main.rs" caption="The code we would have to write if Rust didn’t have deref coercion">

```rust
fn main() {
    let m = MyBox::new(String::from("Rust"));
    hello(&(*m)[..]);
}
```

</Listing>

`(*m)` `MyBox<String>`-কে `String`-এ dereference করে। তারপর `&` এবং `[..]` `String`-টির একটি string slice নেয় যা পুরো string-এর সমান, `hello`-এর signature-এর সাথে match করতে। deref coercion ছাড়া সব চিহ্ন জড়িত থাকায় এই code পড়তে, লিখতে এবং বুঝতে কঠিন। deref coercion Rust-কে এই রূপান্তরগুলো আমাদের জন্য স্বয়ংক্রিয়ভাবে সামলাতে দেয়।

যখন জড়িত type-গুলোর জন্য `Deref` trait define করা থাকে, Rust type-গুলো analyze করে এবং parameter-এর type-এর সাথে match করার জন্য একটি reference পেতে প্রয়োজনমতো `Deref::deref` ব্যবহার করে। `Deref::deref`-কে কতবার insert করতে হবে তা compile time-এ resolve হয়, তাই deref coercion ব্যবহার করার জন্য কোনো runtime penalty নেই!

<!-- Old headings. Do not remove or links may break. -->

<a id="how-deref-coercion-interacts-with-mutability"></a>

### Mutable Reference এর সাথে Deref Coercion পরিচালনা

immutable reference-এ `*` operator override করতে তুমি `Deref` trait যেমন ব্যবহার করো, তেমনিভাবে mutable reference-এ `*` operator override করতে তুমি `DerefMut` trait ব্যবহার করতে পারো।

Rust তিনটি ক্ষেত্রে type এবং trait implementation খুঁজে পেলে deref coercion করে:

1. `T: Deref<Target=U>` হলে `&T` থেকে `&U`-তে
2. `T: DerefMut<Target=U>` হলে `&mut T` থেকে `&mut U`-তে
3. `T: Deref<Target=U>` হলে `&mut T` থেকে `&U`-তে

প্রথম দুটি ক্ষেত্র একই, শুধু দ্বিতীয়টিতে mutability আছে। প্রথম ক্ষেত্রটি বলে যে তোমার কাছে যদি `&T` থাকে এবং `T` কোনো `U` type-এ `Deref` implement করে, তুমি স্বচ্ছভাবে একটি `&U` পেতে পারো। দ্বিতীয় ক্ষেত্রটি বলে যে mutable reference-এর জন্যও একই deref coercion ঘটে।

তৃতীয় ক্ষেত্রটি আরও জটিল: Rust একটি mutable reference-কে immutable-এও coerce করবে। কিন্তু উল্টোটা _সম্ভব নয়_: immutable reference কখনো mutable reference-এ coerce হবে না। borrowing rule-এর কারণে, তোমার কাছে যদি একটি mutable reference থাকে, সেই mutable reference-টি অবশ্যই সেই data-টির একমাত্র reference হতে হবে (নাহলে program compile হতো না)। একটি mutable reference-কে একটি immutable reference-এ রূপ দিলে borrowing rule কখনো ভাঙবে না। একটি immutable reference-কে mutable reference-এ রূপ দিতে গেলে প্রয়োজন হবে যে প্রাথমিক immutable reference-টি সেই data-টির একমাত্র immutable reference হয়, কিন্তু borrowing rule সেটা guarantee করে না। তাই Rust এই ধারণা করতে পারে না যে একটি immutable reference-কে mutable reference-এ রূপ দেওয়া সম্ভব।

[impl-trait]: ch10-02-traits.html#implementing-a-trait-on-a-type
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs

## Advanced Functions and Closures

এই section function এবং closure সম্পর্কিত কিছু advanced feature explore করে, যার মধ্যে function pointer এবং closure return করা অন্তর্ভুক্ত।

### Function Pointers

আমরা কীভাবে function-গুলোতে closure pass করতে হয় তা নিয়ে কথা বলেছি; তুমি regular function-গুলোও function-গুলোতে pass করতে পারো! এই technique তখন useful যখন তুমি একটি নতুন closure define করার পরিবর্তে এমন একটি function pass করতে চাইছো যা তুমি ইতিমধ্যে define করেছ। Function গুলো `fn` type-এ coerce হয় (একটি ছোট _f_ সহ), `Fn` closure trait-এর সাথে confuse করবে না। `fn` type-কে _function pointer_ বলা হয়। Function pointer দিয়ে function pass করা তোমাকে function-গুলোকে অন্য function-এর argument হিসেবে ব্যবহার করতে দেয়।

একটি parameter function pointer তা specify করার syntax closure-গুলোর মতো, যেমন Listing 20-28-তে দেখানো হয়েছে, যেখানে আমরা একটি `add_one` function define করেছি যা তার parameter-এ 1 যোগ করে। `do_twice` function দুটি parameter নেয়: যেকোনো function-এর একটি function pointer যা একটি `i32` parameter নেয় এবং একটি `i32` return করে, এবং একটি `i32` value। `do_twice` function `f` function-টিকে দুবার কল করে, এতে `arg` value pass করে, তারপর দুটি function call result একসাথে যোগ করে। `main` function `do_twice`-কে `add_one` এবং `5` argument দিয়ে কল করে।

<Listing number="20-28" file-name="src/main.rs" caption="Using the `fn` type to accept a function pointer as an argument">

```rust
fn add_one(x: i32) -> i32 {
    x + 1
}

fn do_twice(f: fn(i32) -> i32, arg: i32) -> i32 {
    f(arg) + f(arg)
}

fn main() {
    let answer = do_twice(add_one, 5);

    println!("The answer is: {answer}");
}
```

</Listing>

এই code `The answer is: 12` print করে। আমরা specify করি যে `do_twice`-এর parameter `f` একটি `fn` যা `i32` type-এর একটি parameter নেয় এবং একটি `i32` return করে। তারপর আমরা `do_twice`-এর body-তে `f` কল করতে পারি। `main`-এ, আমরা `do_twice`-এ প্রথম argument হিসেবে function name `add_one` pass করতে পারি।

Closure-এর বিপরীতে, `fn` একটি trait নয় একটি type, তাই আমরা `Fn` trait-গুলোর একটিকে trait bound হিসেবে নিয়ে একটি generic type parameter declare করার পরিবর্তে সরাসরি parameter type হিসেবে `fn` specify করি।

Function pointer গুলো closure trait-এর তিনটি (`Fn`, `FnMut`, এবং `FnOnce`) সম্পূর্ণই implement করে, যার মানে তুমি সবসময় একটি function pointer-কে closure expect করা এমন একটি function-এর জন্য argument হিসেবে pass করতে পারো। Function লেখার সময় generic type এবং closure trait-গুলোর একটি ব্যবহার করা সবচেয়ে ভালো যাতে তোমার function গুলো function বা closure উভয়ই accept করতে পারে।

তা সত্ত্বেও, এমন একটি উদাহরণ যেখানে তুমি শুধুমাত্র `fn` accept করতে চাইবে closure নয়, তা হলো যখন external code-এর সাথে interface করবে যাতে closure নেই: C function গুলো function-কে argument হিসেবে accept করতে পারে, কিন্তু C-তে closure নেই।

Closure inline define করা বা একটি named function ব্যবহার—এই দুটির যেকোনো একটি তুমি ব্যবহার করতে পারো এমন একটি উদাহরণ হিসেবে, চলো standard library-তে `Iterator` trait দ্বারা provide করা `map` method-এর একটি ব্যবহার দেখি। `map` method ব্যবহার করে number-গুলোর একটি vector-কে string-গুলোর একটি vector-এ পরিণত করতে, আমরা একটি closure ব্যবহার করতে পারি, যেমন Listing 20-29-তে।

<Listing number="20-29" caption="Using a closure with the `map` method to convert numbers to strings">

```rust
    let list_of_numbers = vec![1, 2, 3];
    let list_of_strings: Vec<String> =
        list_of_numbers.iter().map(|i| i.to_string()).collect();
```

</Listing>

অথবা আমরা closure-এর পরিবর্তে `map`-এ argument হিসেবে একটি named function ব্যবহার করতে পারি। Listing 20-30 দেখায় তা কেমন দেখাবে।

<Listing number="20-30" caption="Using the `String::to_string` function with the `map` method to convert numbers to strings">

```rust
    let list_of_numbers = vec![1, 2, 3];
    let list_of_strings: Vec<String> =
        list_of_numbers.iter().map(ToString::to_string).collect();
```

</Listing>

খেয়াল করো যে আমাদের [“Advanced Traits”][advanced-traits]<!-- ignore --> section-এ আলোচিত fully qualified syntax ব্যবহার করতে হবে কারণ `to_string` নামে একাধিক function available আছে।

এখানে, আমরা `ToString` trait-এ define করা `to_string` function ব্যবহার করছি, যা standard library `Display` implement করে এমন যেকোনো type-এর জন্য implement করেছে।

Chapter 6-এর [“Enum Values”][enum-values]<!-- ignore --> section থেকে মনে করো যে আমরা যে প্রতিটি enum variant define করি তার নাম একটি initializer function-ও হয়ে যায়। আমরা এই initializer function-গুলোকে function pointer হিসেবে ব্যবহার করতে পারি যা closure trait-গুলো implement করে, যার মানে আমরা initializer function-গুলোকে closure নেয় এমন method-গুলোর জন্য argument হিসেবে specify করতে পারি, যেমন Listing 20-31-তে দেখানো হয়েছে।

<Listing number="20-31" caption="Using an enum initializer with the `map` method to create a `Status` instance from numbers">

```rust
    enum Status {
        Value(u32),
        Stop,
    }

    let list_of_statuses: Vec<Status> = (0u32..20).map(Status::Value).collect();
```

</Listing>

এখানে, আমরা `Status::Value`-এর initializer function ব্যবহার করে `map` যে range-এর উপর কল করা হয়েছে তার প্রতিটি `u32` value দিয়ে `Status::Value` instance তৈরি করি। কিছু মানুষ এই style পছন্দ করে এবং কিছু মানুষ closure ব্যবহার করতে পছন্দ করে। এগুলো একই code-এ compile হয়, তাই তোমার কাছে যেটা clearer মনে হয় সেটাই ব্যবহার করো।

### Returning Closures

Closure গুলো trait দ্বারা represent করা হয়, যার মানে তুমি closure সরাসরি return করতে পারো না। বেশিরভাগ ক্ষেত্রে যেখানে তুমি একটি trait return করতে চাইতে পারো, সেখানে তুমি trait implement করে এমন concrete type-টিকে function-এর return value হিসেবে ব্যবহার করতে পারো। তবে, তুমি সাধারণত closure-গুলোর সাথে এটি করতে পারবে না কারণ তাদের return করা যায় এমন কোনো concrete type নেই; function pointer `fn`-কে return type হিসেবে ব্যবহার করার অনুমতি নেই যদি closure তার scope থেকে কোনো value capture করে, উদাহরণস্বরূপ।

এর বদলে, তুমি সাধারণত Chapter 10-এ আমরা যে শিখেছি `impl Trait` syntax ব্যবহার করবে। তুমি যেকোনো function type return করতে পারো, `Fn`, `FnOnce`, এবং `FnMut` ব্যবহার করে। উদাহরণস্বরূপ, Listing 20-32-তে code ঠিকঠাক compile হবে।

<Listing number="20-32" caption="Returning a closure from a function using the `impl Trait` syntax">

```rust
fn returns_closure() -> impl Fn(i32) -> i32 {
    |x| x + 1
}
```

</Listing>

তবে, Chapter 13-এর [“Inferring and Annotating Closure
Types”][closure-types]<!-- ignore --> section-এ যেমন আমরা উল্লেখ করেছি, প্রতিটি closure তার নিজস্ব distinct type। যদি তোমার একই signature কিন্তু ভিন্ন implementation সহ একাধিক function-এর সাথে কাজ করতে হয়, তবে তোমাকে সেগুলোর জন্য একটি trait object ব্যবহার করতে হবে। বিবেচনা করো তুমি যদি Listing 20-33-তে দেখানো code এর মতো লেখো তবে কী হয়।

<Listing file-name="src/main.rs" number="20-33" caption="Creating a `Vec<T>` of closures defined by functions that return `impl Fn` types">

```rust,ignore,does_not_compile
fn main() {
    let handlers = vec![returns_closure(), returns_initialized_closure(123)];
    for handler in handlers {
        let output = handler(5);
        println!("{output}");
    }
}

fn returns_closure() -> impl Fn(i32) -> i32 {
    |x| x + 1
}

fn returns_initialized_closure(init: i32) -> impl Fn(i32) -> i32 {
    move |x| x + init
}
```

</Listing>

এখানে আমাদের দুটি function আছে, `returns_closure` এবং `returns_initialized_closure`, যাদের উভয়ই `impl Fn(i32) -> i32` return করে। খেয়াল করো যে তারা যে closure return করে তা ভিন্ন, যদিও তারা একই type implement করে। যদি আমরা এটি compile করার চেষ্টা করি, Rust আমাদের জানায় যে এটি কাজ করবে না:

```text
$ cargo build
   Compiling functions-example v0.1.0 (file:///projects/functions-example)
error[E0308]: mismatched types
  --> src/main.rs:2:44
   |
 2 |     let handlers = vec![returns_closure(), returns_initialized_closure(123)];
   |                                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ expected opaque type, found a different opaque type
...
 9 | fn returns_closure() -> impl Fn(i32) -> i32 {
   |                         ------------------- the expected opaque type
...
13 | fn returns_initialized_closure(init: i32) -> impl Fn(i32) -> i32 {
   |                                              ------------------- the found opaque type
   |
   = note: expected opaque type `impl Fn(i32) -> i32`
              found opaque type `impl Fn(i32) -> i32`
   = note: distinct uses of `impl Trait` result in different opaque types

For more information about this error, try `rustc --explain E0308`.
error: could not compile `functions-example` (bin "functions-example") due to 1 previous error
```

Error message আমাদের বলে যে যখনই আমরা একটি `impl Trait` return করি, Rust একটি unique _opaque type_ তৈরি করে, এমন একটি type যেখানে আমরা Rust আমাদের জন্য যা construct করে তার detail দেখতে পারি না, এবং আমরা Rust যে type generate করবে তা guess করে নিজে লিখতে পারব না। সুতরাং, যদিও এই function-গুলো এমন closure return করে যা একই trait, `Fn(i32) -> i32`, implement করে, Rust প্রতিটির জন্য যে opaque type generate করে তা distinct। (এটি এমনভাবে যে Rust distinct async block-এর জন্য ভিন্ন concrete type produce করে এমনকি যখন তাদের output type একই থাকে, যেমন আমরা Chapter 17-এর [“The `Pin` Type and the `Unpin` Trait”][future-types]<!-- ignore -->-এ দেখেছি, তার মতো।) আমরা এই problem-এর সমাধান এখন কয়েকবার দেখেছি: আমরা একটি trait object ব্যবহার করতে পারি, যেমন Listing 20-34-তে।

<Listing number="20-34" caption="Creating a `Vec<T>` of closures defined by functions that return `Box<dyn Fn>` so that they have the same type">

```rust
fn returns_closure() -> Box<dyn Fn(i32) -> i32> {
    Box::new(|x| x + 1)
}

fn returns_initialized_closure(init: i32) -> Box<dyn Fn(i32) -> i32> {
    Box::new(move |x| x + init)
}
```

</Listing>

এই code ঠিকঠাক compile হবে। Trait object সম্পর্কে আরও জানতে, Chapter 18-এর [“Using Trait Objects To Abstract over Shared
Behavior”][trait-objects]<!-- ignore --> section-এ refer করো।

এরপর, চলো macro দেখি!

[advanced-traits]: ch20-02-advanced-traits.html#advanced-traits
[enum-values]: ch06-01-defining-an-enum.html#enum-values
[closure-types]: ch13-01-closures.html#closure-type-inference-and-annotation
[future-types]: ch17-03-more-futures.html
[trait-objects]: ch18-02-trait-objects.html

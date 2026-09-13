<!-- Old headings. Do not remove or links may break. -->

<a id="closures-anonymous-functions-that-can-capture-their-environment"></a>
<a id="closures-anonymous-functions-that-capture-their-environment"></a>

## Closures

Rust-এর closure হলো anonymous function (নামহীন function), যাকে তুমি variable-এ সংরক্ষণ করতে পারো অথবা অন্য function-এ argument হিসেবে pass করতে পারো। তুমি এক জায়গায় closure define করে অন্য জায়গায় ভিন্ন context-এ evaluate করার জন্য call করতে পারো। Function-এর থেকে ভিন্ন, closure তাদের define করা scope থেকে value capture করতে পারে। আমরা দেখাব কীভাবে এই closure feature গুলো code reuse ও behavior customization-এ সাহায্য করে।

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-an-abstraction-of-behavior-with-closures"></a>
<a id="refactoring-using-functions"></a>
<a id="refactoring-with-closures-to-store-code"></a>
<a id="capturing-the-environment-with-closures"></a>

### Capturing the Environment

প্রথমে দেখব কীভাবে closure পরে ব্যবহারের জন্য তাদের define করা environment থেকে value capture করতে পারে। একটি scenario দেখা যাক: মাঝে মাঝেই আমাদের T-shirt কোম্পানি promotion হিসেবে তাদের mailing list-এর কাউকে exclusive, limited-edition shirt উপহার দেয়। Mailing list-এ থাকা মানুষেরা optionally তাদের profile-এ প্রিয় color যোগ করতে পারে। যদি free shirt-এর জন্য নির্বাচিত ব্যক্তির প্রিয় color set করা থাকে, তবে সে সেই color-এর shirt পাবে। আর যদি ব্যক্তি কোনো প্রিয় color specify না করে, তবে সে সেই color-এর shirt পাবে যা কোম্পানির কাছে সবচেয়ে বেশি পরিমাণে আছে।

এটি implement করার অনেক উপায় আছে। এই example-এ আমরা `ShirtColor` নামের একটি enum ব্যবহার করব যার `Red` এবং `Blue` নামে দুটি variant আছে (সরলতার জন্য color-এর সংখ্যা সীমিত রাখা হয়েছে)। আমরা কোম্পানির inventory `Inventory` নামের একটি struct দিয়ে represent করব, যার `shirts` নামের একটি field আছে—এটি একটি `Vec<ShirtColor>`, যা বর্তমানে স্টকে থাকা shirt-এর color গুলো represent করে। `Inventory`-তে define করা `giveaway` method টি free-shirt winner-এর optional shirt color preference পায় এবং সেই ব্যক্তি যে color shirt পাবে সেটি return করে। এই setup দেখানো হলো Listing 13-1-এ।

<Listing number="13-1" file-name="src/main.rs" caption="Shirt company giveaway situation">

```rust,noplayground
#[derive(Debug, PartialEq, Copy, Clone)]
enum ShirtColor {
    Red,
    Blue,
}

struct Inventory {
    shirts: Vec<ShirtColor>,
}

impl Inventory {
    fn giveaway(&self, user_preference: Option<ShirtColor>) -> ShirtColor {
        user_preference.unwrap_or_else(|| self.most_stocked())
    }

    fn most_stocked(&self) -> ShirtColor {
        let mut num_red = 0;
        let mut num_blue = 0;

        for color in &self.shirts {
            match color {
                ShirtColor::Red => num_red += 1,
                ShirtColor::Blue => num_blue += 1,
            }
        }
        if num_red > num_blue {
            ShirtColor::Red
        } else {
            ShirtColor::Blue
        }
    }
}

fn main() {
    let store = Inventory {
        shirts: vec![ShirtColor::Blue, ShirtColor::Red, ShirtColor::Blue],
    };

    let user_pref1 = Some(ShirtColor::Red);
    let giveaway1 = store.giveaway(user_pref1);
    println!(
        "The user with preference {:?} gets {:?}",
        user_pref1, giveaway1
    );

    let user_pref2 = None;
    let giveaway2 = store.giveaway(user_pref2);
    println!(
        "The user with preference {:?} gets {:?}",
        user_pref2, giveaway2
    );
}
```

</Listing>

`main`-এ define করা `store`-এ এই limited-edition promotion-এর জন্য দুটি blue shirt এবং একটি red shirt বাকি আছে। আমরা red shirt preference সহ একজন user এবং কোনো preference ছাড়া একজন user-এর জন্য `giveaway` method টি call করি।

এটাও বলে রাখা ভালো, এই code অনেকভাবেই implement করা যেত, কিন্তু এখানে closure-এর উপর focus করার জন্য আমরা তোমার ইতিমধ্যে শেখা concept গুলোতেই আটকে রেখেছি, শুধু `giveaway` method-এর body টাছাড়া যেখানে closure ব্যবহার করা হয়েছে। `giveaway` method-এ আমরা user preference `Option<ShirtColor>` type-এর একটি parameter হিসেবে পাই এবং `user_preference`-এর উপর `unwrap_or_else` method call করি। [`unwrap_or_else` method on `Option<T>`][unwrap-or-else]<!-- ignore --> standard library-তে define করা। এটি একটি argument নেয়: এমন একটি closure যার কোনো argument নেই এবং যে একটি `T` value return করে (`Option<T>`-এর `Some` variant-এ যে type store করা থাকে, এই ক্ষেত্রে `ShirtColor`)। যদি `Option<T>` টি `Some` variant হয়, তবে `unwrap_or_else` `Some`-এর ভেতরের value টি return করে। আর যদি `Option<T>` টি `None` variant হয়, তবে `unwrap_or_else` closure-টি call করে এবং closure-এর return করা value টি return করে।

আমরা closure expression `|| self.most_stocked()` কে `unwrap_or_else`-এর argument হিসেবে specify করি। এটি এমন একটি closure যার কোনো parameter নেই (closure-এর parameter থাকলে সেগুলো দুটি vertical pipe-এর মাঝে থাকত)। Closure-এর body `self.most_stocked()` কে call করে। আমরা এখানে closure-টি define করছি, আর `unwrap_or_else`-এর implementation প্রয়োজন হলে পরে closure-টি evaluate করবে।

এই code টি run করলে নিচের output পাওয়া যায়:

```console
$ cargo run
   Compiling shirt-company v0.1.0 (file:///projects/shirt-company)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.27s
     Running `target/debug/shirt-company`
The user with preference Some(Red) gets Red
The user with preference None gets Blue
```

এখানে একটি আকর্ষণীয় ব্যাপার হলো—আমরা এমন একটি closure pass করেছি যা current `Inventory` instance-এর উপর `self.most_stocked()` call করে। Standard library-কে আমাদের define করা `Inventory` বা `ShirtColor` type সম্পর্কে কিছু জানার দরকার হয়নি, এমনকি এই scenario-তে আমরা যে logic ব্যবহার করতে চাই সে সম্পর্কেও নয়। Closure-টি `self` `Inventory` instance-এর একটি immutable reference capture করে এবং সেটিকে আমাদের specify করা code-সহ `unwrap_or_else` method-এ পাঠায়। Function-গুলো অন্যদিকে এভাবে তাদের environment capture করতে পারে না।

<!-- Old headings. Do not remove or links may break. -->

<a id="closure-type-inference-and-annotation"></a>

### Inferring এবং Annotating Closure Type

Function আর closure-এর মধ্যে আরও পার্থক্য আছে। Closure-এ সাধারণত `fn` function-এর মতো parameter ও return value-এর type annotate করার প্রয়োজন হয় না। Function-এ type annotation আবশ্যক, কারণ সেই type গুলো user-দের কাছে exposed একটি explicit interface-এর অংশ। এই interface rigid ভাবে define করা থাকা দরকার যাতে সবাই একমত হয় যে function কোন ধরনের value ব্যবহার করে আর return করে। Closure অন্যদিকে এমন exposed interface-এ ব্যবহার হয় না: এগুলো variable-এ store করা হয়, নাম ছাড়া ব্যবহার করা হয় এবং library-এর user-দের কাছে expose করা হয় না।

Closure সাধারণত ছোট হয় এবং যেকোনো arbitrary scenario-তে নয় বরং একটি সীমিত context-এ প্রাসঙ্গিক হয়। এই সীমিত context-এ compiler বেশিরভাগ variable-এর type infer করতে পারার মতোই parameter ও return type infer করতে পারে (কিছু বিরল ক্ষেত্রে compiler-কে closure-এর type annotation ও লাগতে পারে)।

Variable-এর মতোই, আমরা চাইলে প্রয়োজনের চেয়ে একটু বেশি verbose হলেও explicitness ও clarity বাড়াতে type annotation যোগ করতে পারি। একটি closure-এর type annotate করলে সেটি Listing 13-2-এ দেখানো definition-এর মতো দেখাবে। এই example-এ আমরা একটি closure define করে সেটি একটি variable-এ store করছি, এমন নয় যে যেখানে সেটি argument হিসেবে pass করব সেখানেই define করছি, যেমনটা Listing 13-1-এ করেছিলাম।

<Listing number="13-2" file-name="src/main.rs" caption="Adding optional type annotations of the parameter and return value types in the closure">

```rust
    let expensive_closure = |num: u32| -> u32 {
        println!("calculating slowly...");
        thread::sleep(Duration::from_secs(2));
        num
    };
```

</Listing>

Type annotation যোগ করার পর, closure-এর syntax দেখতে function-এর syntax-এর কাছাকাছি লাগে। এখানে তুলনার জন্য আমরা একটি function define করছি যা তার parameter-এ ১ যোগ করে এবং একটি closure যার behavior একই, কিছু space দিয়ে সংশ্লিষ্ট অংশ গুলো সারিবদ্ধ করে। এটি দেখায় যে closure syntax, pipe ব্যবহার ও optional অংশ গুলো ছাড়া, function syntax-এর মতোই:

```rust,ignore
fn  add_one_v1   (x: u32) -> u32 { x + 1 }
let add_one_v2 = |x: u32| -> u32 { x + 1 };
let add_one_v3 = |x|             { x + 1 };
let add_one_v4 = |x|               x + 1  ;
```

প্রথম line-টিতে একটি function definition দেখানো হয়েছে আর দ্বিতীয় line-টিতে একটি সম্পূর্ণ annotated closure definition। তৃতীয় line-এ আমরা closure definition থেকে type annotation গুলো সরিয়েছি। চতুর্থ line-এ আমরা bracket গুলো সরিয়েছি, যেগুলো optional কারণ closure body-তে শুধু একটি expression আছে। এগুলো সবই valid definition, যা call করলে একই behavior পাওয়া যাবে। `add_one_v3` ও `add_one_v4` line গুলোর জন্য, compile করতে হলে closure-গুলোকে evaluate করা প্রয়োজন, কারণ type গুলো ব্যবহার থেকে infer হবে। এটি `let v = Vec::new();`-এর মতো—যেখানেও হয় type annotation অথবা কোনো type-এর value `Vec`-এ যোগ করা দরকার, তাহলেই Rust type infer করতে পারবে।

Closure definition-এর জন্য compiler তার প্রতিটি parameter এবং return value-এর জন্য একটি concrete type infer করবে। উদাহরণস্বরূপ, Listing 13-3 একটি ছোট closure-এর definition দেখায় যেটি শুধু তার parameter হিসেবে যে value পায় সেটাই return করে। এই closure-টি এই example-এর উদ্দেশ্য ছাড়া বিশেষ কাজের নয়। লক্ষ্য করো যে আমরা definition-এ কোনো type annotation যোগ করিনি। Type annotation না থাকায় আমরা closure-টিকে যেকোনো type দিয়ে call করতে পারি, যেমনটা এখানে প্রথমে `String` দিয়ে করেছি। এরপর যদি আমরা `example_closure`-কে integer দিয়ে call করার চেষ্টা করি, একটি error পাব।

<Listing number="13-3" file-name="src/main.rs" caption="Attempting to call a closure whose types are inferred with two different types">

```rust,ignore,does_not_compile
    let example_closure = |x| x;

    let s = example_closure(String::from("hello"));
    let n = example_closure(5);
```

</Listing>

Compiler আমাদের এই error টি দেয়:

```console
$ cargo run
   Compiling closure-example v0.1.0 (file:///projects/closure-example)
error[E0308]: mismatched types
 --> src/main.rs:5:29
  |
5 |     let n = example_closure(5);
  |             --------------- ^ expected `String`, found integer
  |             |
  |             arguments to this function are incorrect
  |
note: expected because the closure was earlier called with an argument of type `String`
 --> src/main.rs:4:29
  |
4 |     let s = example_closure(String::from("hello"));
  |             --------------- ^^^^^^^^^^^^^^^^^^^^^ expected because this argument is of type `String`
  |             |
  |             in this closure call
note: closure parameter defined here
 --> src/main.rs:2:28
  |
2 |     let example_closure = |x| x;
  |                            ^
help: try using a conversion method
  |
5 |     let n = example_closure(5.to_string());
  |                              ++++++++++++

For more information about this error, try `rustc --explain E0308`.
error: could not compile `closure-example` (bin "closure-example") due to 1 previous error
```

প্রথমবার যখন আমরা `example_closure`-কে `String` value দিয়ে call করি, compiler `x`-এর type এবং closure-এর return type দুটোকেই `String` infer করে। এরপর সেই type গুলো `example_closure`-এর closure-এ lock হয়ে যায়, তাই পরের বার একই closure-কে ভিন্ন type দিয়ে ব্যবহার করতে গেলে আমরা type error পাই।

### Capturing References বা Moving Ownership

Closure তাদের environment থেকে তিনভাবে value capture করতে পারে, যা সরাসরি function-এর parameter নেওয়ার তিনটি উপায়ের সাথে মিলে যায়: immutable borrow, mutable borrow এবং ownership নেওয়া। Closure এগুলোর মধ্যে কোনটি ব্যবহার করবে তা নির্ধারণ করে function-এর body captured value গুলোর সাথে কী করে তার উপর ভিত্তি করে।

Listing 13-4-এ আমরা এমন একটি closure define করি যা `list` নামের vector-টির একটি immutable reference capture করে, কারণ value print করার জন্য তার শুধু একটি immutable reference-ই দরকার।

<Listing number="13-4" file-name="src/main.rs" caption="Defining and calling a closure that captures an immutable reference">

```rust
fn main() {
    let list = vec![1, 2, 3];
    println!("Before defining closure: {list:?}");

    let only_borrows = || println!("From closure: {list:?}");

    println!("Before calling closure: {list:?}");
    only_borrows();
    println!("After calling closure: {list:?}");
}
```

</Listing>

এই example এটাও দেখায় যে একটি variable একটি closure definition-এর সাথে bind হতে পারে, এবং আমরা পরে variable নাম ও parentheses ব্যবহার করে closure-টিকে call করতে পারি, ঠিক যেন variable নামটি একটি function নাম।

যেহেতু একই সময়ে `list`-এ একাধিক immutable reference থাকতে পারে, তাই closure define হওয়ার আগের code থেকে, closure define হওয়ার পরে কিন্তু call হওয়ার আগের code থেকে, এবং closure call হওয়ার পরের code থেকেও `list` এখনও accessible। এই code compile হয়, run হয়, এবং নিচের output print করে:

```console
$ cargo run
   Compiling closure-example v0.1.0 (file:///projects/closure-example)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.43s
     Running `target/debug/closure-example`
Before defining closure: [1, 2, 3]
Before calling closure: [1, 2, 3]
From closure: [1, 2, 3]
After calling closure: [1, 2, 3]
```

এরপর Listing 13-5-এ আমরা closure body পরিবর্তন করি যাতে সে `list` vector-এ একটি element যোগ করে। এখন closure-টি একটি mutable reference capture করে।

<Listing number="13-5" file-name="src/main.rs" caption="Defining and calling a closure that captures a mutable reference">

```rust
fn main() {
    let mut list = vec![1, 2, 3];
    println!("Before defining closure: {list:?}");

    let mut borrows_mutably = || list.push(7);

    borrows_mutably();
    println!("After calling closure: {list:?}");
}
```

</Listing>

এই code compile হয়, run হয়, এবং নিচের output print করে:

```console
$ cargo run
   Compiling closure-example v0.1.0 (file:///projects/closure-example)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.43s
     Running `target/debug/closure-example`
Before defining closure: [1, 2, 3]
After calling closure: [1, 2, 3, 7]
```

লক্ষ্য করো যে `borrows_mutably` closure-এর definition আর call-এর মাঝে আর কোনো `println!` নেই: যখন `borrows_mutably` define করা হয়, তখন এটি `list`-এর একটি mutable reference capture করে। Closure call হওয়ার পর আমরা আর closure-টি ব্যবহার করি না, তাই mutable borrow-টি শেষ হয়ে যায়। Closure definition আর closure call-এর মাঝে print করার জন্য একটি immutable borrow allowed নয়, কারণ mutable borrow থাকলে অন্য কোনো borrow allowed নয়। কী error message পাও দেখার জন্য সেখানে একটি `println!` যোগ করে দেখো!

যদি তুমি চাও যে closure body-এ strictly ownership প্রয়োজন না হলেও closure তার environment-এ ব্যবহৃত value গুলোর ownership নিক, তাহলে তুমি parameter list-এর আগে `move` keyword ব্যবহার করতে পারো।

এই technique মূলত তখন কাজে লাগে যখন একটি নতুন thread-কে data move করে দেওয়া হয় যাতে সেই data-এর ownership নতুন thread-এর কাছে থাকে। Thread এবং কেন তুমি সেগুলো ব্যবহার করতে চাইতে পারো তা আমরা Chapter 16-এ concurrency আলোচনার সময় বিস্তারিত আলোচনা করব, কিন্তু আপাতত চলো `move` keyword প্রয়োজন এমন একটি closure ব্যবহার করে নতুন thread spawn করা সংক্ষেপে দেখি। Listing 13-6 দেখায় Listing 13-4 কে modify করে main thread-এর বদলে একটি নতুন thread-এ vector print করা।

<Listing number="13-6" file-name="src/main.rs" caption="Using `move` to force the closure for the thread to take ownership of `list`">

```rust
use std::thread;

fn main() {
    let list = vec![1, 2, 3];
    println!("Before defining closure: {list:?}");

    thread::spawn(move || println!("From thread: {list:?}"))
        .join()
        .unwrap();
}
```

</Listing>

আমরা একটি নতুন thread spawn করি, thread-টিকে argument হিসেবে run করার জন্য একটি closure দিয়ে দিই। Closure body list print করে। Listing 13-4-এ closure শুধু একটি immutable reference দিয়ে `list` কে capture করেছিল, কারণ সেটিই print করার জন্য `list`-এ access-এর সবচেয়ে কম পরিমাণ। এই example-এ, closure body-এর শুধু একটি immutable reference-ই প্রয়োজন হলেও, আমাদের `move` keyword closure definition-এর শুরুতে বসিয়ে specify করতে হবে যে `list` কে closure-এ move করা হবে। যদি main thread নতুন thread-এর উপর `join` call করার আগে আরও কিছু operation সম্পন্ন করে, তাহলে নতুন thread-টি main thread-এর বাকি অংশ শেষ হওয়ার আগেই শেষ হয়ে যেতে পারে, অথবা main thread-ই আগে শেষ হতে পারে। যদি main thread `list`-এর ownership ধরে রাখে কিন্তু নতুন thread-এর আগে শেষ হয়ে যায় এবং `list` কে drop করে, তাহলে thread-এর immutable reference-টি invalid হয়ে যাবে। তাই compiler চায় যে `list` কে নতুন thread-কে দেওয়া closure-এ move করতে হবে, যাতে reference-টি valid থাকে। কী compiler error পাও তা দেখার জন্য `move` keyword সরিয়ে দাও অথবা closure define হওয়ার পরে main thread-এ `list` ব্যবহার করার চেষ্টা করো!

<!-- Old headings. Do not remove or links may break. -->

<a id="storing-closures-using-generic-parameters-and-the-fn-traits"></a>
<a id="limitations-of-the-cacher-implementation"></a>
<a id="moving-captured-values-out-of-the-closure-and-the-fn-traits"></a>
<a id="moving-captured-values-out-of-closures-and-the-fn-traits"></a>

### Moving Captured Values Out of Closures

Closure একবার environment থেকে কোনো value-এর reference বা ownership capture করলে (ফলে closure-এ কী _into_ move হলো তা প্রভাবিত হয়), closure-এর body-এর code নির্ধারণ করে যে পরে closure evaluate হলে সেই reference বা value গুলোর কী হবে (ফলে closure থেকে কী _out of_ move হলো তা প্রভাশিত হয়)।

Closure body নিচের যেকোনো একটি করতে পারে: কোনো captured value কে closure-এর বাইরে move করা, captured value-কে mutate করা, value-কে move বা mutate করা না, অথবা শুরাতেই environment থেকে কিছুই না capture করা।

Closure কীভাবে environment থেকে value capture ও handle করে তা প্রভাবিত করে যে closure কোন trait গুলো implement করবে, আর trait-ই হলো সেই উপায় যার মাধ্যমে function আর struct specify করতে পারে তারা কোন ধরনের closure ব্যবহার করতে পারবে। Closure স্বয়ংক্রিয়ভাবে এই তিনটি `Fn` trait-এর একটি, দুটি, বা সবগুলোই additive ভাবে implement করবে, নির্ভর করে closure-এর body value গুলোকে কীভাবে handle করে তার উপর:

* `FnOnce` এমন closure-এর জন্য প্রযোজ্য যেগুলো একবার call করা যায়। সব closure-ই অন্তত এই trait implement করে, কারণ সব closure-ই call করা যায়। যে closure তার body থেকে captured value কে বাইরে move করে, সে শুধুমাত্র `FnOnce` implement করবে এবং অন্য কোনো `Fn` trait implement করবে না, কারণ সেটিকে শুধু একবারই call করা যায়।
* `FnMut` এমন closure-এর জন্য প্রযোজ্য যেগুলো তাদের body থেকে captured value কে বাইরে move করে না কিন্তু captured value কে mutate করতে পারে। এই closure গুলো একাধিকবার call করা যায়।
* `Fn` এমন closure-এর জন্য প্রযোজ্য যেগুলো তাদের body থেকে captured value কে বাইরে move করে না এবং captured value কে mutate করে না, এবং যেসব closure তাদের environment থেকে কিছুই capture করে না। এই closure গুলো তাদের environment কে mutate না করেই একাধিকবার call করা যায়, যা এমন ক্ষেত্রে গুরুত্বপূর্ণ যেমন একটি closure-কে concurrently একাধিকবার call করা।

চলো Listing 13-1-এ ব্যবহৃত `Option<T>`-এর `unwrap_or_else` method-এর definition-টি দেখি:

```rust,ignore
impl<T> Option<T> {
    pub fn unwrap_or_else<F>(self, f: F) -> T
    where
        F: FnOnce() -> T
    {
        match self {
            Some(x) => x,
            None => f(),
        }
    }
}
```

স্মরণ করো যে `T` হলো সেই generic type যা `Option`-এর `Some` variant-এ value-এর type represent করে। সেই `T` type টিই `unwrap_or_else` function-এর return type-ও: যেমন একটি `Option<String>`-এর উপর `unwrap_or_else` call করলে একটি `String` পাওয়া যাবে।

এরপর লক্ষ্য করো যে `unwrap_or_else` function-এ আরও একটি generic type parameter `F` আছে। `F` type টি হলো `f` নামের parameter-এর type, যা আমরা `unwrap_or_else` call করার সময় যে closure provide করি।

`F` generic type-এর উপর specify করা trait bound হলো `FnOnce() -> T`, যার মানে `F` কে অবশ্যই একবার call করা যোগ্য হতে হবে, কোনো argument নেবে না এবং একটি `T` return করবে। Trait bound-এ `FnOnce` ব্যবহার করায় এই constraint প্রকাশ পায় যে `unwrap_or_else` `f` কে একবারের বেশি call করবে না। `unwrap_or_else`-এর body-তে দেখা যায়, `Option` যদি `Some` হয় তবে `f` কে call করা হবে না। আর `Option` যদি `None` হয় তবে `f` কে একবার call করা হবে। যেহেতু সব closure-ই `FnOnce` implement করে, তাই `unwrap_or_else` তিন ধরনের closure-ই গ্রহণ করে এবং যতটা সম্ভব flexible।

> Note: আমরা যা করতে চাই তার জন্য যদি environment থেকে কোনো value capture করার প্রয়োজন না হয়, তবে closure-এর বদলে আমরা `Fn` trait গুলোর যেকোনো একটি implement করে এমন কিছু প্রয়োজন হলে একটি function-এর নাম ব্যবহার করতে পারি। যেমন, একটি `Option<Vec<T>>` value-তে আমরা `unwrap_or_else(Vec::new)` call করতে পারি, যাতে value `None` হলে একটি নতুন, empty vector পাওয়া যায়। Compiler স্বয়ংক্রিয়ভাবে function definition-এর জন্য যে `Fn` trait টি applicable সেটি implement করে।

এখন চলো standard library-এর `sort_by_key` method টি দেখি, যা slice-এ define করা, যাতে বোঝা যায় এটি `unwrap_or_else` থেকে কীভাবে আলাদা এবং কেন `sort_by_key` trait bound-এ `FnOnce`-এর বদলে `FnMut` ব্যবহার করে। Closure-টি একটি argument পায়—বিবেচ্য slice-এর current item-এর একটি reference—এবং এটি `K` type-এর এমন একটি value return করে যা order করা যায়। এই function তখন কাজে লাগে যখন তুমি একটি slice-কে প্রতিটি item-এর কোনো নির্দিষ্ট attribute অনুসারে sort করতে চাও। Listing 13-7-এ আমাদের কাছে `Rectangle` instance-গুলোর একটি list আছে, এবং আমরা `sort_by_key` ব্যবহার করে সেগুলোকে তাদের `width` attribute অনুসারে কম থেকে বেশি order করি।

<Listing number="13-7" file-name="src/main.rs" caption="Using `sort_by_key` to order rectangles by width">

```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let mut list = [
        Rectangle { width: 10, height: 1 },
        Rectangle { width: 3, height: 5 },
        Rectangle { width: 7, height: 12 },
    ];

    list.sort_by_key(|r| r.width);
    println!("{list:#?}");
}
```

</Listing>

এই code যা print করে:

```console
$ cargo run
   Compiling rectangles v0.1.0 (file:///projects/rectangles)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.41s
     Running `target/debug/rectangles`
[
    Rectangle {
        width: 3,
        height: 5,
    },
    Rectangle {
        width: 7,
        height: 12,
    },
    Rectangle {
        width: 10,
        height: 1,
    },
]
```

`sort_by_key` কে যে `FnMut` closure নেওয়ার জন্য define করা হয়েছে তার কারণ হলো এটি closure-টিকে একাধিকবার call করে: slice-এর প্রতিটি item-এর জন্য একবার। Closure `|r| r.width` তার environment থেকে কিছু capture, mutate বা বাইরে move করে না, তাই এটি trait bound-এর requirement মেটায়।

অন্যদিকে, Listing 13-8 এমন একটি closure-এর example দেখায় যা শুধুমাত্র `FnOnce` trait implement করে, কারণ এটি environment থেকে একটি value কে বাইরে move করে। Compiler আমাদের এই closure-টি `sort_by_key`-এর সাথে ব্যবহার করতে দেবে না।

<Listing number="13-8" file-name="src/main.rs" caption="Attempting to use an `FnOnce` closure with `sort_by_key`">

```rust,ignore,does_not_compile
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let mut list = [
        Rectangle { width: 10, height: 1 },
        Rectangle { width: 3, height: 5 },
        Rectangle { width: 7, height: 12 },
    ];

    let mut sort_operations = vec![];
    let value = String::from("closure called");

    list.sort_by_key(|r| {
        sort_operations.push(value);
        r.width
    });
    println!("{list:#?}");
}
```

</Listing>

এটি একটি artificially বানানো, জটিল (এবং কাজ করে না এমন) উপায় `list` sort করার সময় `sort_by_key` closure-টিকে কতবার call করে তা count করার চেষ্টা। এই code টি এই counting করার চেষ্টা করে `value`—closure-এর environment থেকে একটি `String`—কে `sort_operations` vector-এ push করার মাধ্যমে। Closure-টি `value` কে capture করে এবং তারপর `value`-এর ownership `sort_operations` vector-এ হস্তান্তর করে `value`-কে closure-ের বাইরে move করে। এই closure কে একবার call করা যায়; দ্বিতীয়বার call করার চেষ্টা কাজ করবে না, কারণ `value` তখন আর environment-এ থাকবে না যাতে সেটিকে আবার `sort_operations`-এ push করা যায়! তাই এই closure শুধুমাত্র `FnOnce` implement করে। এই code compile করার চেষ্টা করলে আমরা এই error পাই যে `value` কে closure থেকে বাইরে move করা যাচ্ছে না, কারণ closure-টিকে অবশ্যই `FnMut` implement করতে হবে:

```console
$ cargo run
   Compiling rectangles v0.1.0 (file:///projects/rectangles)
error[E0507]: cannot move out of `value`, a captured variable in an `FnMut` closure
  --> src/main.rs:18:30
   |
15 |     let value = String::from("closure called");
   |         -----   ------------------------------ move occurs because `value` has type `String`, which does not implement the `Copy` trait
   |         |
   |         captured outer variable
16 |
17 |     list.sort_by_key(|r| {
   |                      --- captured by this `FnMut` closure
18 |         sort_operations.push(value);
   |                              ^^^^^ `value` is moved here
   |
help: `Fn` and `FnMut` closures require captured values to be able to be consumed multiple times, but `FnOnce` closures may consume them only once
  --> /rustc/88d9e12ae178fab0fb5cc050a94da85685d449ea/library/alloc/src/slice.rs:249:11
help: consider cloning the value if the performance cost is acceptable
   |
18 |         sort_operations.push(value.clone());
   |                                   ++++++++

For more information about this error, try `rustc --explain E0507`.
error: could not compile `rectangles` (bin "rectangles") due to 1 previous error
```

Error-টি closure body-এর সেই line-এ নির্দেশ করে যেখানে `value` কে environment থেকে বাইরে move করা হয়েছে। এটি fix করতে হলে আমাদের closure body এমনভাবে পরিবর্তন করতে হবে যাতে সে environment থেকে value বাইরে move না করে। Environment-এ একটি counter রেখে closure body-এ তার value increment করা closure-টি কতবার call হলো তা count করার একটি অধিক natural উপায়। Listing 13-9-এর closure-টি `sort_by_key`-এর সাথে কাজ করে, কারণ এটি শুধু `num_sort_operations` counter-এর একটি mutable reference capture করে এবং তাই একাধিকবার call করা যায়।

<Listing number="13-9" file-name="src/main.rs" caption="Using an `FnMut` closure with `sort_by_key` is allowed.">

```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let mut list = [
        Rectangle { width: 10, height: 1 },
        Rectangle { width: 3, height: 5 },
        Rectangle { width: 7, height: 12 },
    ];

    let mut num_sort_operations = 0;
    list.sort_by_key(|r| {
        num_sort_operations += 1;
        r.width
    });
    println!("{list:#?}, sorted in {num_sort_operations} operations");
}
```

</Listing>

`Fn` trait গুলো তখন গুরুত্বপূর্ণ যখন তুমি এমন function বা type define করো বা ব্যবহার করো যা closure ব্যবহার করে। পরের section-এ আমরা iterator নিয়ে আলোচনা করব। অনেক iterator method closure argument নেয়, তাই এই closure-এর বিস্তারিত বিষয় গুলো মনে রেখো যখন আমরা এগিয়ে যাব!

[unwrap-or-else]: ../std/option/enum.Option.html#method.unwrap_or_else

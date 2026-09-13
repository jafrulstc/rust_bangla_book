## Pattern ব্যবহার করা যায় এমন সব জায়গা

Rust-এ pattern নানা জায়গায় উপস্থিত হয়, এবং তুমি নিজে না জেনেই এগুলো অনেকবার ব্যবহার করেছ! এই section-এ আমরা সব জায়গা আলোচনা করব যেখানে pattern valid।

### `match` Arm

Chapter 6-এ আলোচনা করা হয়েছে যে আমরা `match` expression-এর arm-এ pattern ব্যবহার করি। Formally, একটি `match` expression হলো `match` keyword, যে value-টির সাথে match করানো হবে, এবং এক বা তার বেশি match arm—যেখানে প্রতিটি arm একটি pattern ও একটি expression নিয়ে গঠিত, যে expression-টি run হবে যদি value সেই arm-এর pattern-এর সাথে match করে। এমনভাবে:

<!--
  Manually formatted rather than using Markdown intentionally: Markdown does not
  support italicizing code in the body of a block like this!
-->

<pre><code>match <em>VALUE</em> {
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
}</code></pre>

উদাহরণস্বরূপ, Listing 6-5-এর সেই `match` expression-টি নিচে দেওয়া হলো, যেটি `x` variable-এ থাকা একটি `Option<i32>` value-এর সাথে match করে:

```rust,ignore
match x {
    None => None,
    Some(i) => Some(i + 1),
}
```

এই `match` expression-এ pattern গুলো হলো প্রতিটি arrow-এর বাঁ পাশের `None` এবং `Some(i)`।

`match` expression-এর একটি requirement হলো এগুলোকে exhaustive হতে হয়—অর্থাৎ `match` expression-এর value-এর সব সম্ভাবনা অবশ্যই cover করতে হবে। প্রতিটি সম্ভাবনা cover করা হয়েছে কি না তা নিশ্চিত করার একটি উপায় হলো শেষ arm-এ একটি catch-all pattern রাখা: যেমন, এমন একটি variable name যেটি যেকোনো value-এর সাথে match করে—সেটি কখনো fail করবে না এবং তাই বাকি সব case cover করবে।

বিশেষ pattern `_` যেকোনো value-এর সাথে match করে, কিন্তু কখনো কোনো variable-এ bind করে না, তাই এটি প্রায়ই শেষ match arm-এ ব্যবহৃত হয়। যেমন, তুমি যখন নির্দিষ্ট না করা যেকোনো value ignore করতে চাও, তখন `_` pattern কাজে লাগে। আমরা এই chapter-এ পরে [`_` সহ আরও বিস্তারিত][ignoring-values-in-a-pattern]<!-- ignore --> section-এ `_` pattern নিয়ে আলোচনা করব।

### `let` Statement

এই chapter-এর আগে আমরা শুধু `match` এবং `if let`-এর সাথে pattern ব্যবহার নিয়ে explicitly আলোচনা করেছি, কিন্তু আসলে আমরা অন্য জায়গাতেও pattern ব্যবহার করেছি, যার মধ্যে `let` statement-ও আছে। যেমন, নিচের সহজ `let` দিয়ে variable assignment-টি দেখো:

```rust
let x = 5;
```

তুমি যতবার এমন `let` statement ব্যবহার করেছ, প্রতিবারই আসলে pattern ব্যবহার করেছ, যদিও তা তোমার খেয়াল নাও থাকতে পারে! আরো formally, একটি `let` statement দেখতে এমন:

<!--
  Manually formatted rather than using Markdown intentionally: Markdown does not
  support italicizing code in the body of a block like this!
-->

<pre>
<code>let <em>PATTERN</em> = <em>EXPRESSION</em>;</code>
</pre>

`let x = 5;`-এর মতো statement-এ, যেখানে PATTERN-এর জায়গায় একটি variable name আছে, সেই variable name হলো একটি বিশেষ সরল রূপের pattern। Rust expression-টিকে pattern-এর সাথে তুলনা করে এবং যে নামগুলো পায় সেগুলো assign করে। তাই `let x = 5;` উদাহরণে `x` হলো এমন একটি pattern যার অর্থ “যা কিছু এখানে match করে তা `x` variable-এ bind করো।” যেহেতু নাম `x`-ই পুরো pattern, এই pattern-টি কার্যত বোঝায় “value যেই হোক না কেন, সবকিছু `x` variable-এ bind করো।”

`let`-এর pattern-matching দিকটি আরও পরিষ্কার করে দেখতে, Listing 19-1 দেখো, যেখানে `let`-এর সাথে pattern ব্যবহার করে একটি tuple destructure করা হয়েছে।


<Listing number="19-1" caption="Using a pattern to destructure a tuple and create three variables at once">

```rust
    let (x, y, z) = (1, 2, 3);
```

</Listing>

এখানে আমরা একটি tuple-কে একটি pattern-এর সাথে match করছি। Rust `(1, 2, 3)` value-টিকে `(x, y, z)` pattern-এর সাথে তুলনা করে দেখে যে value-টি pattern-এর সাথে match করে—অর্থাৎ উভয়ের element-এর সংখ্যা একই—তাই Rust `1`-কে `x`-এ, `2`-কে `y`-এ এবং `3`-কে `z`-এ bind করে। তুমি এই tuple pattern-টিকে এমন হিসেবে ভাবতে পারো যেটি ভেতরে তিনটি আলাদা variable pattern nest করে রেখেছে।

যদি pattern-এ element-এর সংখ্যা tuple-এর element-এর সংখ্যার সাথে না মেলে, তাহলে overall type match করবে না এবং আমরা একটি compiler error পাব। যেমন, Listing 19-2-তে তিনটি element বিশিষ্ট একটি tuple-কে দুটি variable-এ destructure করার চেষ্টা দেখানো হয়েছে, যা কাজ করবে না।

<Listing number="19-2" caption="Incorrectly constructing a pattern whose variables don’t match the number of elements in the tuple">

```rust,ignore,does_not_compile
    let (x, y) = (1, 2, 3);
```

</Listing>

এই code compile করার চেষ্টা করলে নিচের type error-টি পাওয়া যাবে:

```console
$ cargo run
   Compiling patterns v0.1.0 (file:///projects/patterns)
error[E0308]: mismatched types
 --> src/main.rs:2:9
  |
2 |     let (x, y) = (1, 2, 3);
  |         ^^^^^^   --------- this expression has type `({integer}, {integer}, {integer})`
  |         |
  |         expected a tuple with 3 elements, found one with 2 elements
  |
  = note: expected tuple `({integer}, {integer}, {integer})`
             found tuple `(_, _)`

For more information about this error, try `rustc --explain E0308`.
error: could not compile `patterns` (bin "patterns") due to 1 previous error
```

Error থেকে মুক্তি পেতে আমরা [`_` বা `..` দিয়ে tuple-এর এক বা একাধিক value ignore করতে পারি][ignoring-values-in-a-pattern]<!-- ignore -->, যেমন তুমি পরে দেখবে। কিন্তু সমস্যা যদি হয় pattern-এ variable বেশি আছে, তাহলে সমাধান হলো variable সরিয়ে type match করানো—যাতে variable-এর সংখ্যা tuple-এর element-এর সংখ্যার সমান হয়।

### Conditional `if let` Expression

Chapter 6-এ আমরা আলোচনা করেছি কীভাবে `if let` expression-টি মূলত এমন একটি `match`-এর সংক্ষিপ্ত রূপ হিসেবে ব্যবহৃত হয়, যেটি শুধু একটি case match করে। Optional ভাবে, `if let`-এর সাথে একটি `else` থাকতে পারে, যেখানে `if let`-এর pattern match না করলে যে code টি run হবে তা থাকে।

Listing 19-3 দেখায় যে `if let`, `else if`, এবং `else if let` expression গুলো একসাথে mix করেও ব্যবহার করা যায়। এতে `match` expression-এর চেয়ে বেশি flexibility পাওয়া যায়, কারণ `match`-এ আমরা শুধু একটি মাত্র value-কে pattern-এর সাথে তুলনা করতে পারি। এছাড়া, Rust-এর কোনো শর্ত নেই যে `if let`, `else if`, এবং `else if let` arm-গুলোর condition গুলো পরস্পরের সাথে সম্পর্কিত হতে হবে।

Listing 19-3-এর code টি বিভিন্ন condition check করে ঠিক করে যে background-এ কোন color ব্যবহার করা হবে। এই উদাহরণে আমরা এমন কিছু hardcoded value দিয়ে variable তৈরি করেছি, যা একটি আসল program সম্ভবত user input থেকে পেত।

<Listing number="19-3" file-name="src/main.rs" caption="Mixing `if let`, `else if`, `else if let`, and `else`">

```rust
fn main() {
    let favorite_color: Option<&str> = None;
    let is_tuesday = false;
    let age: Result<u8, _> = "34".parse();

    if let Some(color) = favorite_color {
        println!("Using your favorite color, {color}, as the background");
    } else if is_tuesday {
        println!("Tuesday is green day!");
    } else if let Ok(age) = age {
        if age > 30 {
            println!("Using purple as the background color");
        } else {
            println!("Using orange as the background color");
        }
    } else {
        println!("Using blue as the background color");
    }
}
```

</Listing>

User যদি কোনো favorite color উল্লেখ করে, সেই color-টি background হিসেবে ব্যবহৃত হবে। কোনো favorite color উল্লেখ না থাকলে এবং আজকে যদি Tuesday হয়, তাহলে background color green হবে। অন্যথায়, user যদি তার age একটি string হিসেবে দেয় এবং আমরা যদি সেটিকে number হিসেবে successfully parse করতে পারি, তাহলে number-এর value অনুযায়ী color হবে purple বা orange। এর কোনো condition-ই প্রযোজ্য না হলে background color blue হবে।

এই conditional structure আমাদের জটিল requirement support করতে দেয়। এখানকার hardcoded value অনুযায়ী এই উদাহরণটি `Using purple as the background color` print করবে।

তুমি খেয়াল করবে যে `if let` নতুন variable introduce করতে পারে যা বিদ্যমান variable-কে shadow করে—`match` arm যেভাবে করে: `if let Ok(age) = age` line-টি একটি নতুন `age` variable introduce করে, যা `Ok` variant-এর ভেতরের value ধারণ করে এবং বিদ্যমান `age` variable-কে shadow করে। এর মানে হলো `if age > 30` condition-টি আমাদের সেই block-এর ভেতরে রাখতে হবে: আমরা এই দুটি condition-কে `if let Ok(age) = age && age > 30` আকারে একসাথে combine করতে পারব না। যে নতুন `age` আমরা 30-এর সাথে compare করতে চাই, সেটি ততক্ষণ পর্যন্ত valid নয় যতক্ষণ না নতুন scope টি curly bracket দিয়ে শুরু হয়।

`if let` expression ব্যবহারের অসুবিধা হলো compiler exhaustiveness check করে না, অন্যদিকে `match` expression-এ সেটি করে। যদি আমরা শেষ `else` block টা বাদ দিতাম এবং ফলে কিছু case handle করা বাদ পড়ত, তাহলে compiler আমাদের সম্ভাব্য logic bug সম্পর্কে alert করত না।

### `while let` Conditional Loop

`if let`-এর গঠনের মতোই, `while let` conditional loop একটি `while` loop-কে ততক্ষণ পর্যন্ত run করতে দেয় যতক্ষণ একটি pattern match করতে থাকে। Listing 19-4-এ আমরা এমন একটি `while let` loop দেখাচ্ছি যেটি thread-এর মধ্যে পাঠানো message-এর জন্য অপেক্ষা করে, কিন্তু এক্ষেত্রে একটি `Option`-এর বদলে `Result` check করা হচ্ছে।

<Listing number="19-4" caption="Using a `while let` loop to print values for as long as `rx.recv()` returns `Ok`">

```rust
    let (tx, rx) = std::sync::mpsc::channel();
    std::thread::spawn(move || {
        for val in [1, 2, 3] {
            tx.send(val).unwrap();
        }
    });

    while let Ok(value) = rx.recv() {
        println!("{value}");
    }
```

</Listing>

এই উদাহরণটি প্রথমে `1`, তারপর `2`, তারপর `3` print করে। `recv` method টি channel-এর receiver side থেকে প্রথম message-টি বের করে আনে এবং একটি `Ok(value)` return করে। Chapter 16-এ যখন আমরা প্রথম `recv` দেখেছিলাম, তখন আমরা সরাসরি error unwrap করেছিলাম, অথবা `for` loop ব্যবহার করে এটিকে একটি iterator হিসেবে ব্যবহার করেছিলাম। কিন্তু Listing 19-4 যেমন দেখায়, আমরা `while let`-ও ব্যবহার করতে পারি, কারণ প্রতিবার একটি message এলে `recv` method একটি `Ok` return করে—যতক্ষণ sender বেঁচে আছে—এবং sender side disconnect হলে একটি `Err` produce করে।

### `for` Loop

`for` loop-এ, `for` keyword-এর ঠিক পরে যে value টি আসে সেটি একটি pattern। যেমন, `for x in y`-এ `x` হলো pattern। Listing 19-5 দেখায় কীভাবে `for` loop-এ একটি pattern ব্যবহার করে একটি tuple-কে destructure, অর্থাৎ ভেঙে, আলাদা করা যায়।


<Listing number="19-5" caption="Using a pattern in a `for` loop to destructure a tuple">

```rust
    let v = vec!['a', 'b', 'c'];

    for (index, value) in v.iter().enumerate() {
        println!("{value} is at index {index}");
    }
```

</Listing>

Listing 19-5-এর code টি নিচের output টি print করবে:


```console
$ cargo run
   Compiling patterns v0.1.0 (file:///projects/patterns)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.52s
     Running `target/debug/patterns`
a is at index 0
b is at index 1
c is at index 2
```

আমরা `enumerate` method দিয়ে একটি iterator-কে adapt করি যাতে সেটি একটি value এবং সেই value-এর index, একটি tuple-এ রেখে, produce করে। প্রথমে produce হওয়া value টি হলো `(0, 'a')` tuple-টি। যখন এই value-টিকে `(index, value)` pattern-এর সাথে match করানো হয়, তখন index হবে `0` এবং value হবে `'a'`, ফলে output-এর প্রথম line টি print হয়।


### Function Parameter

Function parameter গুলোও pattern হতে পারে। Listing 19-6-এর code টি—যেখানে `foo` নামে একটি function declare করা হয়েছে যেটি `x` নামে একটি `i32` type-এর parameter নেয়—এখন তোমার চেনা চেনা মনে হওয়ার কথা।

<Listing number="19-6" caption="A function signature using patterns in the parameters">

```rust
fn foo(x: i32) {
    // code goes here
}
```

</Listing>

`x` অংশটিও একটি pattern! `let`-এর মতো করে আমরা একটি function-এর argument-এ একটি tuple-কে pattern-এর সাথে match করাতে পারি। Listing 19-7 একটি tuple-এর value গুলোকে function-এ pass করার সময় ভাগ করে দেখায়।

<Listing number="19-7" file-name="src/main.rs" caption="A function with parameters that destructure a tuple">

```rust
fn print_coordinates(&(x, y): &(i32, i32)) {
    println!("Current location: ({x}, {y})");
}

fn main() {
    let point = (3, 5);
    print_coordinates(&point);
}
```

</Listing>

এই code টি `Current location: (3, 5)` print করে। `&(3, 5)` value-গুলো `&(x, y)` pattern-এর সাথে match করে, তাই `x` হলো value `3` এবং `y` হলো value `5`।

আমরা closure parameter list-এও function parameter list-এর মতো একইভাবে pattern ব্যবহার করতে পারি, কারণ closure গুলো function-এর মতোই—যেমনটা Chapter 13-এ আলোচনা করা হয়েছে।

এখন পর্যন্ত তুমি pattern ব্যবহারের বিভিন্ন উপায় দেখেছ, কিন্তু pattern গুলো সব জায়গায় একইভাবে কাজ করে না। কিছু জায়গায় pattern গুলো অবশ্যই irrefutable হতে হবে; অন্য ক্ষেত্রে সেগুলো refutable হতে পারে। পরে আমরা এই দুটি concept নিয়ে আলোচনা করব।

[ignoring-values-in-a-pattern]: ch19-03-pattern-syntax.html#ignoring-values-in-a-pattern

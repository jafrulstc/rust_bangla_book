## Pattern Syntax

এই section-এ আমরা pattern-এ valid সব syntax একত্রিত করব এবং আলোচনা করব কেন এবং কখন তুমি প্রতিটি ব্যবহার করতে চাইতে পারো।

### Matching Literals

Chapter 6-এ যেমন দেখেছ, তুমি pattern-কে সরাসরি literal-এর সাথে match করাতে পারো। নিচের code-টি কিছু উদাহরণ দেখায়:

```rust
    let x = 1;

    match x {
        1 => println!("one"),
        2 => println!("two"),
        3 => println!("three"),
        _ => println!("anything"),
    }
```

এই code টি `one` print করে, কারণ `x`-এর value `1`। যখন তুমি চাও তোমার code কোনো নির্দিষ্ট concrete value পেলে একটি action নিক, তখন এই syntax কাজে লাগে।

### Matching Named Variables

Named variables হলো irrefutable pattern যা যেকোনো value-এর সাথে match করে, এবং আমরা এই book-এ সেগুলো অনেকবার ব্যবহার করেছি। তবে `match`, `if let`, বা `while let` expression-এ তুমি named variable ব্যবহার করলে একটি জটিলতা দেখা দেয়। যেহেতু এই ধরনের প্রতিটি expression একটি নতুন scope শুরু করে, তাই এই expression-গুলোর ভেতরে pattern-এর অংশ হিসেবে declare করা variable গুলো construct-টির বাইরে একই নামের অন্য সব variable-কে shadow করবে—ঠিক যেমন সব ক্ষেত্রে variable-এর ক্ষেত্রে হয়। Listing 19-11-তে আমরা `x` নামে একটি variable `Some(5)` value দিয়ে এবং একটি `y` variable `10` value দিয়ে declare করেছি। তারপর আমরা `x` value-এর ওপর একটি `match` expression তৈরি করেছি। match arm-এর pattern গুলো এবং শেষের `println!` লক্ষ্য করো, এবং এই code টি run করার আগে বা পড়া চালিয়ে যাওয়ার আগে ভাবার চেষ্টা করো যে এই code টি কী print করবে।

<Listing number="19-11" file-name="src/main.rs" caption="A `match` expression with an arm that introduces a new variable which shadows an existing variable `y`">

```rust
    let x = Some(5);
    let y = 10;

    match x {
        Some(50) => println!("Got 50"),
        Some(y) => println!("Matched, y = {y}"),
        _ => println!("Default case, x = {x:?}"),
    }

    println!("at the end: x = {x:?}, y = {y}");
```

</Listing>

চলো দেখি `match` expression-টি run হলে কী হয়। প্রথম match arm-এর pattern টি `x`-এর define করা value-এর সাথে match করে না, তাই code এগিয়ে যায়।

দ্বিতীয় match arm-এর pattern টি `y` নামে একটি নতুন variable introduce করে যা `Some` value-এর ভেতরের যেকোনো value-এর সাথে match করবে। যেহেতু আমরা `match` expression-এর ভেতরে একটি নতুন scope-এ আছি, তাই এটি একটি নতুন `y` variable—শুরুতে `10` value দিয়ে declare করা সেই `y` নয়। এই নতুন `y` binding যেকোনো `Some`-এর ভেতরের value-এর সাথে match করবে, যা আমাদের `x`-এ আছে। তাই এই নতুন `y` `x`-এর `Some`-এর ভেতরের value-এর সাথে bind হবে। সেই value টি `5`, তাই সেই arm-এর expression-টি execute হয় এবং `Matched, y = 5` print করে।

`x` যদি `Some(5)` না হয়ে `None` value হত, তাহলে প্রথম দুটি arm-এর pattern গুলো match করত না, তাই value-টি underscore-এর সাথে match করত। আমরা underscore arm-এর pattern-এ `x` variable introduce করিনি, তাই expression-এর `x` এখনও সেই বাইরের `x` যাকে shadow করা হয়নি। এই hypothetical case-এ `match` টি `Default case, x = None` print করত।

`match` expression শেষ হলে এর scope শেষ হয়, এবং ভেতরের `y`-এর scope-ও শেষ হয়। শেষ `println!` টি `at the end: x = Some(5), y = 10` produce করে।

বাইরের `x` ও `y`-এর value তুলনা করার জন্য—বিদ্যমান `y` variable-কে shadow করে এমন নতুন variable introduce করার বদলে—আমাদের একটি match guard condition ব্যবহার করতে হত। আমরা match guard নিয়ে পরে [“Adding Conditionals with Match Guards”](#adding-conditionals-with-match-guards)<!-- ignore --> section-এ আলোচনা করব।

<!-- Old headings. Do not remove or links may break. -->
<a id="multiple-patterns"></a>

### Matching Multiple Pattern

`match` expression-এ তুমি `|` syntax ব্যবহার করে একাধিক pattern match করতে পারো, যা হলো pattern-এর _or_ operator। যেমন, নিচের code-এ আমরা `x`-এর value-কে match arm-এর সাথে match করাই, যার প্রথমটিতে একটি _or_ বিকল্প আছে—অর্থাৎ `x`-এর value যদি সেই arm-এর যেকোনো একটি value-এর সাথে match করে, তাহলে সেই arm-এর code টি run হবে:


```rust
    let x = 1;

    match x {
        1 | 2 => println!("one or two"),
        3 => println!("three"),
        _ => println!("anything"),
    }
```

এই code টি `one or two` print করে।

### `..=` দিয়ে Range of Value Matching

`..=` syntax আমাদের value-এর একটি inclusive range-এর সাথে match করতে দেয়। নিচের code-এ, যখন একটি pattern প্রদত্ত range-এর যেকোনো value-এর সাথে match করে, তখন সেই arm-টি execute হবে:

```rust
    let x = 5;

    match x {
        1..=5 => println!("one through five"),
        _ => println!("something else"),
    }
```

`x` যদি `1`, `2`, `3`, `4`, বা `5` হয়, তাহলে প্রথম arm-টি match করবে। একই ধারণা প্রকাশ করতে `|` operator ব্যবহারের চেয়ে একাধিক match value-এর জন্য এই syntax বেশি convenient; যদি আমরা `|` ব্যবহার করতাম, তাহলে `1 | 2 | 3 | 4 | 5` লিখতে হতো। একটি range উল্লেখ করা অনেক ছোট, বিশেষত যদি আমরা, ধরা যাক, 1 থেকে 1,000-এর মধ্যে যেকোনো number match করতে চাই!

Compile করার সময় compiler check করে যে range-টি খালি নয়, এবং যেহেতু Rust শুধু `char` এবং numeric value-এর ক্ষেত্রেই বলতে পারে যে একটি range খালি কি না, তাই range গুলো শুধু numeric বা `char` value-এর সাথেই allowed।

এখানে `char` value-এর range ব্যবহার করে একটি উদাহরণ দেওয়া হলো:

```rust
    let x = 'c';

    match x {
        'a'..='j' => println!("early ASCII letter"),
        'k'..='z' => println!("late ASCII letter"),
        _ => println!("something else"),
    }
```

Rust বুঝতে পারে যে `'c'` প্রথম pattern-এর range-এর ভেতরে আছে এবং `early ASCII letter` print করে।

### Destructuring দিয়ে Value ভেঙে আলাদা করা

আমরা pattern ব্যবহার করে struct, enum, এবং tuple-কে destructure করে এই value-গুলোর বিভিন্ন অংশ ব্যবহার করতে পারি। চলো প্রতিটি value ধরে দেখি।

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs"></a>

#### Struct

Listing 19-12 একটি `Point` struct দেখায় যার দুটি field আছে—`x` এবং `y`—যেগুলোকে আমরা একটি `let` statement-এর সাথে pattern ব্যবহার করে ভেঙে আলাদা করতে পারি।

<Listing number="19-12" file-name="src/main.rs" caption="Destructuring a struct’s fields into separate variables">

```rust
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point { x: 0, y: 7 };

    let Point { x: a, y: b } = p;
    assert_eq!(0, a);
    assert_eq!(7, b);
}
```

</Listing>

এই code টি `a` এবং `b` নামে দুটি variable তৈরি করে যেগুলো `p` struct-এর `x` এবং `y` field-এর value-এর সাথে match করে। এই উদাহরণ দেখায় যে pattern-এ variable-গুলোর নাম struct-এর field-এর নামের সাথে match করার কোনো প্রয়োজন নেই। তবে field-এর নাম অনুযায়ী variable-এর নাম রাখলে মনে রাখা সহজ হয় যে কোন variable কোন field থেকে এসেছে। এই প্রচলিত ব্যবহারের কারণে, এবং যেহেতু `let Point { x: x, y: y } = p;` লেখায় অনেক পুনরাবৃত্তি থাকে, তাই struct field match করার pattern-এর জন্য Rust-এ একটি shorthand আছে: তোমাকে শুধু struct field-টির নাম লিখতে হবে, এবং pattern থেকে তৈরি হওয়া variable-গুলোর নাম একই হবে। Listing 19-13 এর আচরণ Listing 19-12-এর code-এর মতোই, কিন্তু `let` pattern-এ তৈরি হওয়া variable-গুলো `a` এবং `b` এর বদলে `x` এবং `y`।

<Listing number="19-13" file-name="src/main.rs" caption="Destructuring struct fields using struct field shorthand">

```rust
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point { x: 0, y: 7 };

    let Point { x, y } = p;
    assert_eq!(0, x);
    assert_eq!(7, y);
}
```

</Listing>

এই code টি `x` এবং `y` variable তৈরি করে যেগুলো `p` variable-এর `x` এবং `y` field-এর সাথে match করে। ফলাফল হলো `x` এবং `y` variable-গুলো `p` struct থেকে আসা value গুলো ধারণ করে।

আমরা struct pattern-এর অংশ হিসেবে সব field-এর জন্য variable তৈরি করার বদলে literal value দিয়েও destructure করতে পারি। এতে আমরা কিছু field নির্দিষ্ট value-এর জন্য test করতে পারি এবং একই সাথে বাকি field গুলোকে destructure করার জন্য variable তৈরি করতে পারি।

Listing 19-14-তে আমাদের এমন একটি `match` expression আছে যা `Point` value গুলোকে তিনটি case-এ ভাগ করে: এমন point যা সরাসরি `x` axis-এ অবস্থিত (`y = 0` হলে এটি true), `y` axis-এ অবস্থিত (`x = 0`), অথবা কোনো axis-এই নেই।

<Listing number="19-14" file-name="src/main.rs" caption="Destructuring and matching literal values in one pattern">

```rust
fn main() {
    let p = Point { x: 0, y: 7 };

    match p {
        Point { x, y: 0 } => println!("On the x axis at {x}"),
        Point { x: 0, y } => println!("On the y axis at {y}"),
        Point { x, y } => {
            println!("On neither axis: ({x}, {y})");
        }
    }
}
```

</Listing>

প্রথম arm-টি `y` field-এর value literal `0`-এর সাথে match করলে match হবে বলে উল্লেখ করে যেকোনো সেই point-এর সাথে match করবে যা `x` axis-এ অবস্থিত। Pattern-টি একটি `x` variable ও তৈরি করে যা আমরা এই arm-এর code-এ ব্যবহার করতে পারি।

একইভাবে, দ্বিতীয় arm-টি `x` field-এর value `0` হলে match হবে বলে উল্লেখ করে যেকোনো `y` axis-এর point-এর সাথে match করে এবং `y` field-এর value-এর জন্য একটি `y` variable তৈরি করে। তৃতীয় arm-টি কোনো literal উল্লেখ করে না, তাই এটি অন্য যেকোনো `Point`-এর সাথে match করবে এবং `x` এবং `y` উভয় field-এর জন্য variable তৈরি করবে।

এই উদাহরণে `p` value-টি `x`-এ `0` থাকার কারণে দ্বিতীয় arm-এর সাথে match করে, তাই এই code টি `On the y axis at 7` print করবে।

মনে রেখো যে একটি `match` expression প্রথম matching pattern খুঁজে পেলেই arm check করা বন্ধ করে দেয়, তাই `Point { x: 0, y: 0 }` যদি `x` axis ও `y` axis উভয়ের ওপর থাকে, তবু এই code টি শুধু `On the x axis at 0` print করত।

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-enums"></a>

#### Enum

আমরা এই book-এ enum কে destructure করেছি (যেমন Chapter 6-এর Listing 6-5), কিন্তু এখনও explicitly আলোচনা করিনি যে একটি enum-কে destructure করার pattern-টি enum-এর ভেতরে define করা data-এর গঠনের সাথে মিলে যায়। উদাহরণস্বরূপ, Listing 19-15-তে আমরা Listing 6-2 থেকে `Message` enum টি ব্যবহার করে এমন একটি `match` লিখেছি যার pattern গুলো প্রতিটি inner value-কে destructure করবে।

<Listing number="19-15" file-name="src/main.rs" caption="Destructuring enum variants that hold different kinds of values">

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

fn main() {
    let msg = Message::ChangeColor(0, 160, 255);

    match msg {
        Message::Quit => {
            println!("The Quit variant has no data to destructure.");
        }
        Message::Move { x, y } => {
            println!("Move in the x direction {x} and in the y direction {y}");
        }
        Message::Write(text) => {
            println!("Text message: {text}");
        }
        Message::ChangeColor(r, g, b) => {
            println!("Change color to red {r}, green {g}, and blue {b}");
        }
    }
}
```

</Listing>

এই code টি `Change color to red 0, green 160, and blue 255` print করবে। `msg`-এর value পরিবর্তন করে দেখো যাতে অন্য arm-গুলোর code ও run হয়।

`Message::Quit`-এর মতো কোনো data ছাড়া enum variant-এর ক্ষেত্রে আমরা value-টিকে আর বেশি destructure করতে পারি না। আমরা শুধু literal `Message::Quit` value-এর সাথে match করতে পারি, এবং সেই pattern-এ কোনো variable নেই।

`Message::Move`-এর মতো struct-সদৃশ enum variant-এর ক্ষেত্রে আমরা struct match করার pattern-এর মতো একটি pattern ব্যবহার করতে পারি। variant-এর নামের পরে আমরা curly bracket দিয়ে তারপর field গুলো variable সহ লিখি, যাতে অংশগুলো ভেঙে এই arm-এর code-এ ব্যবহার করা যায়। এখানে আমরা Listing 19-13-এর মতো shorthand রূপ ব্যবহার করেছি।

`Message::Write`-এর মতো একটি element বিশিষ্ট tuple ধারণকারী এবং `Message::ChangeColor`-এর মতো তিনটি element বিশিষ্ট tuple ধারণকারী tuple-সদৃশ enum variant-এর ক্ষেত্রে pattern-টি tuple match করার pattern-এর মতো। pattern-এ variable-এর সংখ্যা অবশ্যই আমরা যে variant-টি match করছি তার element-এর সংখ্যার সমান হতে হবে।

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-nested-structs-and-enums"></a>

#### Nested Struct এবং Enum

এ পর্যন্ত আমাদের সব উদাহরণে শুধু এক স্তর গভীর struct বা enum match করা হয়েছে, কিন্তু matching nested item-এও কাজ করতে পারে! যেমন, আমরা Listing 19-15-এর code টি এমনভাবে refactor করতে পারি যাতে `ChangeColor` message-এ RGB এবং HSV color support করে, যেমন Listing 19-16-তে দেখানো হয়েছে।

<Listing number="19-16" caption="Matching on nested enums">

```rust
enum Color {
    Rgb(i32, i32, i32),
    Hsv(i32, i32, i32),
}

enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(Color),
}

fn main() {
    let msg = Message::ChangeColor(Color::Hsv(0, 160, 255));

    match msg {
        Message::ChangeColor(Color::Rgb(r, g, b)) => {
            println!("Change color to red {r}, green {g}, and blue {b}");
        }
        Message::ChangeColor(Color::Hsv(h, s, v)) => {
            println!("Change color to hue {h}, saturation {s}, value {v}");
        }
        _ => (),
    }
}
```

</Listing>

`match` expression-টির প্রথম arm-এর pattern-টি এমন একটি `Message::ChangeColor` enum variant-এর সাথে match করে যা একটি `Color::Rgb` variant ধারণ করে; তারপর pattern-টি তিনটি inner `i32` value-এর সাথে bind হয়। দ্বিতীয় arm-এর pattern-টিও একটি `Message::ChangeColor` enum variant-এর সাথে match করে, কিন্তু inner enum-টি `Color::Hsv`-এর সাথে match করে। আমরা একটি `match` expression-এই এই জটিল condition গুলো উল্লেখ করতে পারি, যদিও এখানে দুটি enum জড়িত।

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs-and-tuples"></a>

#### Struct এবং Tuple

আমরা আরও জটিল উপায়ে destructuring pattern গুলো mix, match এবং nest করতে পারি। নিচের উদাহরণটি একটি জটিল destructure দেখায় যেখানে আমরা একটি tuple-এর ভেতরে struct এবং tuple nest করেছি এবং সব primitive value কে বের করে আনছি:

```rust
    let ((feet, inches), Point { x, y }) = ((3, 10), Point { x: 3, y: -10 });
```

এই code টি আমাদের জটিল type গুলোকে তাদের উপাদানে ভাগ করতে দেয় যাতে আমরা আগ্রহী value গুলো আলাদাভাবে ব্যবহার করতে পারি।

Pattern দিয়ে destructuring করা হলো value-গুলোর অংশ—যেমন একটি struct-এর প্রতিটি field-এর value—আলাদাভাবে ব্যবহারের একটি convenient উপায়।

### Pattern-এ Value Ignore করা

তুমি দেখেছ যে মাঝে মাঝে pattern-এ value ignore করা কাজে দেয়, যেমন একটি `match`-এর শেষ arm-এ এমন একটি catch-all পাওয়ার জন্য যা আসলে কিছুই করে না কিন্তু বাকি সব possible value কে অবশ্যই cover করে। একটি pattern-এ সম্পূর্ণ value বা value-এর কিছু অংশ ignore করার কয়েকটি উপায় আছে: `_` pattern ব্যবহার করা (যা তুমি দেখেছ), অন্য pattern-এর ভেতরে `_` pattern ব্যবহার করা, underscore দিয়ে শুরু হওয়া কোনো নাম ব্যবহার করা, অথবা `..` ব্যবহার করে একটি value-এর বাকি অংশ ignore করা। চলো দেখি কীভাবে এবং কেন এই pattern গুলোর প্রতিটি ব্যবহার করতে হয়।

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-entire-value-with-_"></a>

#### `_` দিয়ে সম্পূর্ণ Value

আমরা underscore-কে একটি wildcard pattern হিসেবে ব্যবহার করেছি যা যেকোনো value-এর সাথে match করবে কিন্তু value-টির সাথে bind করবে না। এটি বিশেষত একটি `match` expression-এর শেষ arm হিসেবে কাজে লাগে, কিন্তু আমরা যেকোনো pattern-এ—function parameter সহ—এটি ব্যবহার করতে পারি, যেমন Listing 19-17-তে দেখানো হয়েছে।

<Listing number="19-17" file-name="src/main.rs" caption="Using `_` in a function signature">

```rust
fn foo(_: i32, y: i32) {
    println!("This code only uses the y parameter: {y}");
}

fn main() {
    foo(3, 4);
}
```

</Listing>

এই code টি প্রথম argument হিসেবে pass করা `3` value-টিকে সম্পূর্ণভাবে ignore করবে এবং `This code only uses the y parameter: 4` print করবে।

যখন তুমি কোনো নির্দিষ্ট function parameter আর দরকার করো না, বেশিরভাগ ক্ষেত্রে তুমি signature এমনভাবে পরিবর্তন করবে যাতে unused parameter টি না থাকে। তবে function parameter ignore করা বিশেষ ক্ষেত্রে কাজে লাগতে পারে—যেমন, যখন তুমি একটি trait implement করছ এবং তোমার একটি নির্দিষ্ট type signature দরকার, কিন্তু তোমার implementation-এর function body-তে parameter-গুলোর একটি দরকার নেই। তখন তুমি unused function parameter সম্পর্কে compiler warning পাওয়া এড়াতে পারো, যা তুমি নাম ব্যবহার করলে পেতে।

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-parts-of-a-value-with-a-nested-_"></a>

#### Nested `_` দিয়ে Value-এর কিছু অংশ

আমরা অন্য pattern-এর ভেতরে `_` ব্যবহার করে একটি value-এর শুধু একটি অংশ ignore করতে পারি—যেমন, যখন আমরা শুধু একটি value-এর একটি অংশ test করতে চাই কিন্তু সংশ্লিষ্ট code-এ বাকি অংশগুলোর কোনো দরকার নেই। Listing 19-18-তে এমন code দেখানো হয়েছে যা একটি setting-এর value manage করার দায়িত্বে আছে। Business requirement হলো user-কে একটি setting-এর বিদ্যমান customization overwrite করতে দেওয়া যাবে না, কিন্তু setting-টি যদি বর্তমানে unset থাকে তাহলে তা unset করে value দেওয়া যাবে।

<Listing number="19-18" caption="Using an underscore within patterns that match `Some` variants when we don’t need to use the value inside the `Some`">

```rust
    let mut setting_value = Some(5);
    let new_setting_value = Some(10);

    match (setting_value, new_setting_value) {
        (Some(_), Some(_)) => {
            println!("Can't overwrite an existing customized value");
        }
        _ => {
            setting_value = new_setting_value;
        }
    }

    println!("setting is {setting_value:?}");
```

</Listing>

এই code টি প্রথমে `Can't overwrite an existing customized value` এবং তারপর `setting is Some(5)` print করবে। প্রথম match arm-এ আমাদের কোনো `Some` variant-এর ভেতরের value-গুলোর সাথে match করার বা সেগুলো ব্যবহার করার দরকার নেই, কিন্তু আমাদের সেই case test করতে হবে যেখানে `setting_value` এবং `new_setting_value` উভয়ই `Some` variant। সেই ক্ষেত্রে আমরা `setting_value` পরিবর্তন না করার কারণটি print করি, এবং এটি পরিবর্তিত হয় না।

অন্য সব case-এ (অর্থাৎ `setting_value` বা `new_setting_value` যদি `None` হয়) দ্বিতীয় arm-এর `_` pattern-এর মাধ্যমে আমরা `new_setting_value`-কে `setting_value` হতে দিতে চাই।

আমরা একই pattern-এর একাধিক জায়গায় underscore ব্যবহার করে নির্দিষ্ট value গুলো ignore করতে পারি। Listing 19-19 পাঁচটি উপাদান বিশিষ্ট একটি tuple-এর দ্বিতীয় এবং চতুর্থ value ignore করার একটি উদাহরণ দেখায়।

<Listing number="19-19" caption="Ignoring multiple parts of a tuple">

```rust
    let numbers = (2, 4, 8, 16, 32);

    match numbers {
        (first, _, third, _, fifth) => {
            println!("Some numbers: {first}, {third}, {fifth}");
        }
    }
```

</Listing>

এই code টি `Some numbers: 2, 8, 32` print করবে এবং `4` ও `16` value গুলো ignore হবে।

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-unused-variable-by-starting-its-name-with-_"></a>

#### নামের শুরুতে `_` দিয়ে একটি Unused Variable

তুমি একটি variable তৈরি করে সেটি কোথাও ব্যবহার না করলে Rust সাধারণত একটি warning দেয়, কারণ unused variable একটি bug হতে পারে। তবে মাঝে মাঝে এমন একটি variable তৈরি করতে পারা সুবিধাজনক যেটি তুমি এখনো ব্যবহার করবে না—যেমন যখন তুমি শুধু prototype বানাচ্ছ বা একটি project শুরু করছ। এই পরিস্থিতিতে তুমি variable-এর নাম underscore দিয়ে শুরু করে Rust-কে বলতে পারো যে সে যেন unused variable সম্পর্কে তোমাকে warning না দেয়। Listing 19-20-তে আমরা দুটি unused variable তৈরি করেছি, কিন্তু এই code compile করলে আমাদের শুধু একটির বিষয়ে warning পাওয়া উচিত।

<Listing number="19-20" file-name="src/main.rs" caption="Starting a variable name with an underscore to avoid getting unused variable warnings">

```rust
fn main() {
    let _x = 5;
    let y = 10;
}
```

</Listing>

এখানে আমরা `y` variable টি ব্যবহার না করার জন্য warning পাব, কিন্তু `_x` ব্যবহার না করার জন্য warning পাব না।

মনে রেখো যে শুধু `_` ব্যবহার করা এবং underscore দিয়ে শুরু হওয়া কোনো নাম ব্যবহার করার মধ্যে একটি সূক্ষ্ম পার্থক্য আছে। `_x` syntax টি এখনও value-টিকে variable-এ bind করে, কিন্তু `_` আদৌ কোনো bind করে না। এই পার্থক্যটি যেখানে গুরুত্বপূর্ণ হয়ে দাঁড়ায় সেই case টি দেখাতে, Listing 19-21 আমাদের একটি error দেবে।

<Listing number="19-21" caption="An unused variable starting with an underscore still binds the value, which might take ownership of the value.">

```rust,ignore,does_not_compile
    let s = Some(String::from("Hello!"));

    if let Some(_s) = s {
        println!("found a string");
    }

    println!("{s:?}");
```

</Listing>

আমরা একটি error পাব কারণ `s` value-টি এখনও `_s`-এ move হবে, যা আমাদের `s` আবার ব্যবহার করতে বাধা দেয়। তবে শুধু underscore ব্যবহার করলে কখনো value-টির সাথে bind করে না। Listing 19-22 কোনো error ছাড়াই compile হবে কারণ `s` কে `_`-এ move করা হয় না।

<Listing number="19-22" caption="Using an underscore does not bind the value.">

```rust
    let s = Some(String::from("Hello!"));

    if let Some(_) = s {
        println!("found a string");
    }

    println!("{s:?}");
```

</Listing>

এই code টি নিখুঁতভাবে কাজ করে কারণ আমরা কখনো `s`-কে কোনো কিছুর সাথে bind করি না; এটি move হয় না।

<a id="ignoring-remaining-parts-of-a-value-with-"></a>

#### `..` দিয়ে Value-এর বাকি অংশ

অনেক অংশ বিশিষ্ট value-এর ক্ষেত্রে আমরা `..` syntax ব্যবহার করে নির্দিষ্ট অংশ ব্যবহার করে বাকিটা ignore করতে পারি, ফলে প্রতিটি ignored value-এর জন্য underscore লিখতে হয় না। `..` pattern টি একটি value-এর সেই সব অংশ ignore করে যেগুলো আমরা pattern-এর বাকি অংশে explicitly match করিনি। Listing 19-23-তে আমাদের একটি `Point` struct আছে যা ত্রিমাত্রিক space-এ একটি coordinate ধারণ করে। `match` expression-এ আমরা শুধু `x` coordinate নিয়ে কাজ করতে চাই এবং `y` ও `z` field-এর value গুলো ignore করতে চাই।

<Listing number="19-23" caption="Ignoring all fields of a `Point` except for `x` by using `..`">

```rust
    struct Point {
        x: i32,
        y: i32,
        z: i32,
    }

    let origin = Point { x: 0, y: 0, z: 0 };

    match origin {
        Point { x, .. } => println!("x is {x}"),
    }
```

</Listing>

আমরা `x` value টি লিখে তারপর শুধু `..` pattern টি যোগ করেছি। এটি `y: _` এবং `z: _` লেখার চেয়ে দ্রুত, বিশেষত যখন আমরা এমন struct নিয়ে কাজ করি যার অনেক গুলো field আছে কিন্তু শুধু এক বা দুটি field প্রাসঙ্গিক।

`..` syntax টি যত গুলো value প্রয়োজন তত গুলোতে বিস্তৃত হবে। Listing 19-24 দেখায় কীভাবে একটি tuple-এর সাথে `..` ব্যবহার করতে হয়।

<Listing number="19-24" file-name="src/main.rs" caption="Matching only the first and last values in a tuple and ignoring all other values">

```rust
fn main() {
    let numbers = (2, 4, 8, 16, 32);

    match numbers {
        (first, .., last) => {
            println!("Some numbers: {first}, {last}");
        }
    }
}
```

</Listing>

এই code-এ প্রথম এবং শেষ value গুলো `first` এবং `last`-এর সাথে match করে। `..` মাঝের সব কিছুর সাথে match করবে এবং সেগুলো ignore করবে।

তবে, `..` ব্যবহার করতে হলে তা অবশ্যই unambiguous হতে হবে। কোনো value গুলো match করার জন্য এবং কোন গুলো ignore করার জন্য নির্দিষ্ট করা আছে তা যদি পরিষ্কার না হয়, তাহলে Rust আমাদের একটি error দেবে। Listing 19-25 এমন একটি উদাহরণ দেখায় যেখানে `..` ambiguously ব্যবহার করা হয়েছে, তাই এটি compile হবে না।

<Listing number="19-25" file-name="src/main.rs" caption="An attempt to use `..` in an ambiguous way">

```rust,ignore,does_not_compile
fn main() {
    let numbers = (2, 4, 8, 16, 32);

    match numbers {
        (.., second, ..) => {
            println!("Some numbers: {second}")
        },
    }
}
```

</Listing>

এই উদাহরণটি compile করালে আমরা এই error-টি পাই:

```console
$ cargo run
   Compiling patterns v0.1.0 (file:///projects/patterns)
error: `..` can only be used once per tuple pattern
 --> src/main.rs:5:22
  |
5 |         (.., second, ..) => {
  |          --          ^^ can only be used once per tuple pattern
  |          |
  |          previously used here

error: could not compile `patterns` (bin "patterns") due to 1 previous error
```

Rust-এর পক্ষে নির্ধারণ করা অসম্ভব যে `second`-এর সাথে একটি value match করার আগে tuple-এ কতগুলো value ignore করতে হবে এবং তার পরে আরও কতগুলো value ignore করতে হবে। এই code-টি দ্বারা বোঝানো হতে পারে যে আমরা `2` ignore করতে চাই, `second`-কে `4`-এ bind করতে চাই, এবং তারপর `8`, `16`, এবং `32` ignore করতে চাই; অথবা আমরা `2` এবং `4` ignore করতে চাই, `second`-কে `8`-এ bind করতে চাই, এবং তারপর `16` ও `32` ignore করতে চাই; ইত্যাদি। `second` variable নামটি Rust-এর কাছে কোনো বিশেষ অর্থ বহন করে না, তাই আমরা একটি compiler error পাই কারণ দুটি জায়গায় এভাবে `..` ব্যবহার করা ambiguous।

<!-- Old headings. Do not remove or links may break. -->

<a id="extra-conditionals-with-match-guards"></a>

### Match Guard দিয়ে Conditional যোগ করা

একটি _match guard_ হলো একটি অতিরিক্ত `if` condition, যা একটি `match` arm-এ pattern-এর পরে উল্লেখ করা হয় এবং সেই arm-টি select করার জন্য এটিও অবশ্যই match করতে হবে। Match guard গুলো শুধু pattern-এর চেয়ে বেশি জটিল ধারণা প্রকাশ করতে কাজে লাগে। তবে মনে রাখবে যে এগুলো শুধু `match` expression-এই available, `if let` বা `while let` expression-এ নয়।

condition-এ pattern-এ তৈরি করা variable গুলো ব্যবহার করা যেতে পারে। Listing 19-26-তে এমন একটি `match` দেখানো হয়েছে যার প্রথম arm-এ `Some(x)` pattern আছে এবং সাথে `if x % 2 == 0` match guard আছে (যা `true` হবে যদি number টি even হয়)।

<Listing number="19-26" caption="Adding a match guard to a pattern">

```rust
    let num = Some(4);

    match num {
        Some(x) if x % 2 == 0 => println!("The number {x} is even"),
        Some(x) => println!("The number {x} is odd"),
        None => (),
    }
```

</Listing>

এই উদাহরণটি `The number 4 is even` print করবে। যখন `num`-কে প্রথম arm-এর pattern-এর সাথে তুলনা করা হয়, তখন এটি match করে কারণ `Some(4)` এর সাথে `Some(x)` match করে। তারপর match guard টি check করে `x`-কে 2 দিয়ে ভাগ করলে ভাগশেষ 0 এর সমান কি না, এবং যেহেতু সমান, তাই প্রথম arm-টি select হয়।

`num` যদি `Some(4)` এর বদলে `Some(5)` হত, তাহলে প্রথম arm-এর match guard টি `false` হত, কারণ 5 কে 2 দিয়ে ভাগ করলে ভাগশেষ 1, যা 0 এর সমান নয়। তখন Rust দ্বিতীয় arm-এ যেত, যা match করত কারণ দ্বিতীয় arm-এ কোনো match guard নেই এবং তাই এটি যেকোনো `Some` variant-এর সাথে match করে।

একটি pattern-এর ভেতরে `if x % 2 == 0` condition প্রকাশ করার কোনো উপায় নেই, তাই match guard আমাদের এই logic প্রকাশ করার ক্ষমতা দেয়। এই অতিরিক্ত প্রকাশ ক্ষমতার অসুবিধা হলো match guard expression জড়িত থাকলে compiler exhaustiveness check করার চেষ্টা করে না।

Listing 19-11 আলোচনার সময় আমরা উল্লেখ করেছিলাম যে আমরা match guard ব্যবহার করে আমাদের pattern-shadowing সমস্যা সমাধান করতে পারি। মনে করো যে আমরা `match` expression-এর ভেতরে pattern-এ একটি নতুন variable তৈরি করেছিলাম—`match`-এর বাইরের variable ব্যবহার না করে। সেই নতুন variable-এর কারণে আমরা বাইরের variable-টির value-এর সাথে test করতে পারছিলাম না। Listing 19-27 দেখায় কীভাবে আমরা এই সমস্যা সমাধানে একটি match guard ব্যবহার করতে পারি।

<Listing number="19-27" file-name="src/main.rs" caption="Using a match guard to test for equality with an outer variable">

```rust
fn main() {
    let x = Some(5);
    let y = 10;

    match x {
        Some(50) => println!("Got 50"),
        Some(n) if n == y => println!("Matched, n = {n}"),
        _ => println!("Default case, x = {x:?}"),
    }

    println!("at the end: x = {x:?}, y = {y}");
}
```

</Listing>

এই code টি এখন `Default case, x = Some(5)` print করবে। দ্বিতীয় match arm-এর pattern-টি এমন কোনো নতুন `y` variable introduce করে না যা বাইরের `y`-কে shadow করবে, অর্থাৎ আমরা match guard-এ বাইরের `y` ব্যবহার করতে পারি। pattern টি `Some(y)` হিসেবে উল্লেখ করার বদলে—যা বাইরের `y`-কে shadow করত—আমরা `Some(n)` উল্লেখ করেছি। এটি একটি নতুন `n` variable তৈরি করে যা কিছুই shadow করে না, কারণ `match`-এর বাইরে কোনো `n` variable নেই।

`if n == y` match guard টি একটি pattern নয় এবং তাই এটি কোনো নতুন variable introduce করে না। এই `y` _হলো_ সেই বাইরের `y`, এটিকে shadow করে এমন নতুন কোনো `y` নয়, এবং আমরা `n`-কে `y`-এর সাথে তুলনা করে এমন একটি value খুঁজতে পারি যার value বাইরের `y`-এর সমান।

তুমি একটি match guard-এ _or_ operator `|` ব্যবহার করে একাধিক pattern উল্লেখ করতে পারো; match guard-এর condition টি সব pattern-এর ক্ষেত্রেই প্রযোজ্য হবে। Listing 19-28 দেখায় `|` ব্যবহার করা একটি pattern-এর সাথে match guard combine করলে কী precedence হয়। এই উদাহরণের গুরুত্বপূর্ণ অংশ হলো `if y` match guard টি `4`, `5`, _এবং_ `6`-এর ক্ষেত্রে প্রযোজ্য, যদিও মনে হতে পারে যে `if y` শুধু `6`-এর ক্ষেত্রে প্রযোজ্য।

<Listing number="19-28" caption="Combining multiple patterns with a match guard">

```rust
    let x = 4;
    let y = false;

    match x {
        4 | 5 | 6 if y => println!("yes"),
        _ => println!("no"),
    }
```

</Listing>

Match condition টি বলে যে arm-টি শুধু তখনই match করবে যখন `x`-এর value `4`, `5`, বা `6`-এর সমান _এবং_ `y`-এর value `true`। এই code টি run করার সময় প্রথম arm-এর pattern টি match করে কারণ `x`-এর value `4`, কিন্তু `if y` match guard টি `false`, তাই প্রথম arm-টি select হয় না। code টি দ্বিতীয় arm-এ চলে যায়, যা match করে, এবং এই program-টি `no` print করে। কারণ হলো `if` condition টি পুরো `4 | 5 | 6` pattern-এর ক্ষেত্রে প্রযোজ্য, শুধু শেষ value `6`-এর ক্ষেত্রে নয়। অর্থাৎ, একটি pattern-এর সাপেক্ষে match guard-এর precedence আচরণ এমন:

```text
(4 | 5 | 6) if y => ...
```

এরকম নয়:

```text
4 | 5 | (6 if y) => ...
```

code টি run করার পর precedence আচরণটি স্পষ্ট হয়ে যায়: যদি match guard-টি শুধু `|` operator দিয়ে উল্লেখ করা value list-এর শেষ value-টির ক্ষেত্রে প্রযোজ্য হত, তাহলে arm-টি match করত এবং program-টি `yes` print করত।

<!-- Old headings. Do not remove or links may break. -->

<a id="-bindings"></a>

### `@` Binding ব্যবহার করা

_at_ operator `@` আমাদের একই সাথে একটি value test করার সময় সেই value-টিকে ধারণ করে এমন একটি variable তৈরি করতে দেয়। Listing 19-29-তে আমরা test করতে চাই যে একটি `Message::Hello`-এর `id` field `3..=7` range-এর ভেতরে আছে কি না। আমরা এটিও চাই যে value-টি `id` variable-এ bind হোক, যাতে আমরা সেটি arm-এর সাথে যুক্ত code-এ ব্যবহার করতে পারি।

<Listing number="19-29" caption="Using `@` to bind to a value in a pattern while also testing it">

```rust
    enum Message {
        Hello { id: i32 },
    }

    let msg = Message::Hello { id: 5 };

    match msg {
        Message::Hello { id: id @ 3..=7 } => {
            println!("Found an id in range: {id}")
        }
        Message::Hello { id: 10..=12 } => {
            println!("Found an id in another range")
        }
        Message::Hello { id } => println!("Found some other id: {id}"),
    }
```

</Listing>

এই উদাহরণটি `Found an id in range: 5` print করবে। `3..=7` range-এর আগে `id @` উল্লেখ করার মাধ্যমে আমরা range-এর সাথে match হওয়া যেকোনো value-কে `id` নামের একটি variable-এ capture করছি, এবং একই সাথে test করছি যে value-টি range pattern-এর সাথে match করে কি না।

দ্বিতীয় arm-টিতে, যেখানে pattern-এ শুধু একটি range উল্লেখ করা আছে, সেখানে arm-এর সাথে যুক্ত code-এ এমন কোনো variable নেই যা `id` field-এর actual value ধারণ করে। `id` field-এর value 10, 11, বা 12 হতে পারত, কিন্তু সেই pattern-এর সাথে যুক্ত code-টি জানে না সেটি কোনটি। pattern-টির code `id` field থেকে আসা value টি ব্যবহার করতে পারে না, কারণ আমরা `id` value-টিকে কোনো variable-এ save করিনি।

শেষ arm-টিতে, যেখানে আমরা কোনো range ছাড়া একটি variable উল্লেখ করেছি, সেখানে arm-এর code-এ `id` নামের একটি variable-এ value টি ব্যবহারের জন্য পাওয়া যায়। কারণ আমরা struct field shorthand syntax ব্যবহার করেছি। কিন্তু এই arm-এ আমরা `id` field-এর value-টির কোনো test প্রয়োগ করিনি, যেমনটা প্রথম দুটি arm-এ করেছি: যেকোনো value এই pattern-এর সাথে match করবে।

`@` ব্যবহার করলে আমরা একই pattern-এর ভেতরে একটি value test করতে এবং সেটি একটি variable-এ save করতে পারি।

## Summary

Rust-এর pattern গুলো বিভিন্ন ধরনের data-এর মধ্যে পার্থক্য করতে খুবই কাজের। `match` expression-এ ব্যবহৃত হলে Rust নিশ্চিত করে যে তোমার pattern গুলো প্রতিটি possible value cover করে, নাহলে তোমার program compile হবে না। `let` statement এবং function parameter-এ pattern-এর ব্যবহার সেই construct গুলোকে আরও কাজের করে তোলে—value গুলোকে ছোট অংশে destructure করে সেই অংশগুলোকে variable-এ assign করার ক্ষমতা দেয়। আমরা আমাদের প্রয়োজন অনুযায়ী সরল বা জটিল pattern তৈরি করতে পারি।

এর পরে, book-এর শেষ ঠিক আগের chapter হিসেবে, আমরা Rust-এর বিভিন্ন feature-এর কিছু advanced দিক নিয়ে আলোচনা করব।

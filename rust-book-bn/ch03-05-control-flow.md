## Control Flow

কোনো condition `true` হলে কিছু code run করার ক্ষমতা এবং কোনো condition `true` থাকা পর্যন্ত কিছু code বারবার run করার ক্ষমতা—এগুলো বেশিরভাগ programming language-এর মূল উপাদান। Rust code-এর execution-এর flow নিয়ন্ত্রণ করতে দেওয়া সবচেয়ে সাধারণ construct গুলো হলো `if` expression এবং loop।

### `if` Expressions

একটি `if` expression তোমাকে condition অনুযায়ী তোমার code branch করতে দেয়। তুমি একটি condition দাও এবং তারপর বলো, “এই condition পূরণ হলে, এই code block run করো। Condition পূরণ না হলে, এই code block run করো না।”

`if` expression explore করার জন্য তোমার _projects_ directory-তে _branches_ নামে একটি নতুন project তৈরি করো। _src/main.rs_ file-এ নিচের code টি লেখো:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let number = 3;

    if number < 5 {
        println!("condition was true");
    } else {
        println!("condition was false");
    }
}
```

সব `if` expression `if` keyword দিয়ে শুরু হয়, তারপর একটি condition থাকে। এই ক্ষেত্রে, condition টি check করে `number` variable-এর value 5 থেকে কম কি না। আমরা condition `true` হলে যে code block execute করব সেটি condition-এর ঠিক পরেই curly brackets-এর ভেতরে রাখি। `if` expression-গুলোতে condition-গুলোর সাথে যুক্ত code block-গুলোকে মাঝে মাঝে _arm_ বলা হয়, ঠিক যেমন `match` expression-এর arm, যা নিয়ে আমরা Chapter 2-এর [“Comparing the Guess to the Secret Number”][comparing-the-guess-to-the-secret-number]<!-- ignore --> section-এ আলোচনা করেছি।

Optional ভাবে, আমরা একটি `else` expression-ও যোগ করতে পারি, যেমনটা আমরা এখানে করেছি, যাতে condition `false` evaluate হলে program execute করার জন্য একটি alternative code block পায়। তুমি যদি `else` expression না দাও এবং condition `false` হয়, তাহলে program শুধু `if` block টা skip করে পরের code-এ চলে যাবে।

এই code টি run করে দেখো; তোমার নিচের output দেখা উচিত:

```console
$ cargo run
   Compiling branches v0.1.0 (file:///projects/branches)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.31s
     Running `target/debug/branches`
condition was true
```

চলো `number`-এর value এমন একটি value-তে পরিবর্তন করি যা condition-টিকে `false` করে দেয় এবং কী হয় দেখি:

```rust,ignore
    let number = 7;
```

Program-টি আবার run করো, এবং output এ দেখো:

```console
$ cargo run
   Compiling branches v0.1.0 (file:///projects/branches)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.31s
     Running `target/debug/branches`
condition was false
```

এটাও উল্লেখ করার মতো যে এই code-এর condition টি _অবশ্যই_ একটি `bool` হতে হবে। Condition টি `bool` না হলে আমরা একটি error পাব। যেমন, নিচের code টি run করে দেখো:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
fn main() {
    let number = 3;

    if number {
        println!("number was three");
    }
}
```

এবার `if` condition টি `3` value-তে evaluate হয়, আর Rust একটি error দেখায়:

```console
$ cargo run
   Compiling branches v0.1.0 (file:///projects/branches)
error[E0308]: mismatched types
 --> src/main.rs:4:8
  |
4 |     if number {
  |        ^^^^^^ expected `bool`, found integer

For more information about this error, try `rustc --explain E0308`.
error: could not compile `branches` (bin "branches") due to 1 previous error
```

Error-টি নির্দেশ করে যে Rust একটি `bool` expect করেছিল কিন্তু একটি integer পেয়েছে। Ruby বা JavaScript-এর মতো language-এর বিপরীতে, Rust non-Boolean type-কে স্বয়ংক্রিয়ভাবে Boolean-এ convert করার চেষ্টা করবে না। তোমাকে explicit হতে হবে এবং সবসময় `if`-এর condition হিসেবে একটি Boolean দিতে হবে। যদি আমরা চাই যে `if` code block টি শুধু তখনই run হোক যখন কোনো number `0`-এর সমান নয়, যেমন, আমরা `if` expression-টিকে নিচের মতো পরিবর্তন করতে পারি:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let number = 3;

    if number != 0 {
        println!("number was something other than zero");
    }
}
```

এই code টি run করলে `number was something other than zero` print হবে।

#### Handling Multiple Conditions with `else if`

তুমি `if` এবং `else`-কে একটি `else if` expression-এ একত্রিত করে একাধিক condition ব্যবহার করতে পারো। যেমন:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let number = 6;

    if number % 4 == 0 {
        println!("number is divisible by 4");
    } else if number % 3 == 0 {
        println!("number is divisible by 3");
    } else if number % 2 == 0 {
        println!("number is divisible by 2");
    } else {
        println!("number is not divisible by 4, 3, or 2");
    }
}
```

এই program-টির চারটি সম্ভাব্য path আছে যেগুলো নিতে পারে। এটি run করার পর তোমার নিচের output দেখা উচিত:

```console
$ cargo run
   Compiling branches v0.1.0 (file:///projects/branches)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.31s
     Running `target/debug/branches`
number is divisible by 3
```

এই program execute হওয়ার সময় এটি প্রতিটি `if` expression পালা ক্রমে check করে এবং যে প্রথম body-এর condition `true` evaluate হয় সেটি execute করে। লক্ষ্য করো যে 6 কে 2 দিয়ে ভাগ যায় সত্ত্বেও, আমরা `number is divisible by 2` output দেখি না, আবার `else` block থেকে `number is not divisible by 4, 3, or 2` text-ও দেখি না। কারণ Rust শুধু প্রথম `true` condition-এর জন্য block execute করে, এবং একবার এটি একটি পেলে বাকিগুলো check-ও করে না।

খুব বেশি `else if` expression ব্যবহার করলে তোমার code cluttered হয়ে যেতে পারে, তাই একাধিক হলে তুমি হয়তো তোমার code refactor করতে চাইবে। Chapter 6 এই ধরনের case-গুলোর জন্য `match` নামে একটি শক্তিশালী Rust branching construct বর্ণনা করে।

#### Using `if` in a `let` Statement

যেহেতু `if` একটি expression, আমরা এটিকে একটি `let` statement-এর ডান পাশে ব্যবহার করে outcome-টি একটি variable-এ assign করতে পারি, যেমন Listing 3-2-তে।

<Listing number="3-2" file-name="src/main.rs" caption="Assigning the result of an `if` expression to a variable">

```rust
fn main() {
    let condition = true;
    let number = if condition { 5 } else { 6 };

    println!("The value of number is: {number}");
}
```

</Listing>

`number` variable-টি `if` expression-এর outcome-এর ওপর ভিত্তি করে একটি value-এর সাথে bind হবে। কী হয় দেখতে এই code টি run করো:

```console
$ cargo run
   Compiling branches v0.1.0 (file:///projects/branches)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.30s
     Running `target/debug/branches`
The value of number is: 5
```

মনে রাখবে যে code block গুলো তাদের ভেতরের শেষ expression-টিতে evaluate হয়, এবং একা number গুলোও expression। এই ক্ষেত্রে, পুরো `if` expression-টির value নির্ভর করে কোন code block execute হয় তার ওপর। এর মানে হলো `if`-এর প্রতিটি arm থেকে result হওয়ার সম্ভাবনা থাকা value-গুলোর type একই হতে হবে; Listing 3-2-তে, `if` arm এবং `else` arm দুটোর result-ই `i32` integer ছিল। যদি type গুলো mismatch হয়, যেমন নিচের উদাহরণে, আমরা একটি error পাব:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
fn main() {
    let condition = true;

    let number = if condition { 5 } else { "six" };

    println!("The value of number is: {number}");
}
```

এই code compile করার চেষ্টা করলে আমরা একটি error পাব। `if` এবং `else` arm-গুলোর value type incompatible, এবং Rust ঠিক কোথায় সমস্যা তা program-এ স্পষ্ট করে নির্দেশ করে:

```console
$ cargo run
   Compiling branches v0.1.0 (file:///projects/branches)
error[E0308]: `if` and `else` have incompatible types
 --> src/main.rs:4:44
  |
4 |     let number = if condition { 5 } else { "six" };
  |                                 -          ^^^^^ expected integer, found `&str`
  |                                 |
  |                                 expected because of this

For more information about this error, try `rustc --explain E0308`.
error: could not compile `branches` (bin "branches") due to 1 previous error
```

`if` block-এর expression-টি একটি integer-এ evaluate হয়, আর `else` block-এর expression-টি একটি string-এ। এটি কাজ করবে না, কারণ variable-গুলোর একটি একক type হতে হবে, এবং Rust-এর compile time-এ নিশ্চিতভাবে জানা দরকার `number` variable-টির type কী। `number`-এর type জানা থাকলে compiler verify করতে পারে যে আমরা যেখানে `number` ব্যবহার করছি সব জায়গায় type-টি valid কি না। `number`-এর type শুধু runtime-এ নির্ধারিত হলে Rust সেটা করতে পারত না; তাহলে compiler আরও জটিল হয়ে যেত এবং যদি সে প্রতিটি variable-এর জন্য একাধিক কাল্পনিক type ট্র্যাক রাখত, তবে code সম্পর্কে আরও কম গ্যারান্টি দিতে পারত।

### Repetition with Loops

একাধিকবার কোনো code block execute করাটা প্রায়ই কার্যকর। এই কাজের জন্য Rust কয়েকটি _loop_ দেয়, যা loop body-এর ভেতরের code শেষ পর্যন্ত run করে এবং তারপর সাথে সাথে আবার শুরু থেকে শুরু করে। Loop নিয়ে experiment করতে চলো _loops_ নামে একটি নতুন project বানাই।

Rust-এ তিন ধরনের loop আছে: `loop`, `while`, এবং `for`। চলো প্রতিটি চেষ্টা করি।

#### Repeating Code with `loop`

`loop` keyword Rust-কে বলে একটি code block বারবার execute করতে—চিরকাল অথবা তুমি স্পষ্টভাবে থামতে বলা পর্যন্ত।

উদাহরণস্বরূপ, তোমার _loops_ directory-তে _src/main.rs_ file-টিকে নিচের মতো দেখতে পরিবর্তন করো:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore
fn main() {
    loop {
        println!("again!");
    }
}
```

এই program-টি run করলে আমরা আমরা manually না থামানো পর্যন্ত এটি ক্রমাগত `again!` print হতে দেখব। বেশিরভাগ terminal একটি continual loop-এ আটকে থাকা program-কে interrupt করতে <kbd>ctrl</kbd>-<kbd>C</kbd> keyboard shortcut support করে। এটা একবার চেষ্টা করে দেখো:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-32-loop
cargo run
CTRL-C
-->

```console
$ cargo run
   Compiling loops v0.1.0 (file:///projects/loops)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.08s
     Running `target/debug/loops`
again!
again!
again!
again!
^Cagain!
```

`^C` symbol টি বোঝায় তুমি কোথায় <kbd>ctrl</kbd>-<kbd>C</kbd> চেপেছিলে।

`^C`-এর পরে `again!` শব্দটি দেখতে পাওয়া যাবে কি না, তা নির্ভর করে interrupt signal পাওয়ার সময় code loop-এর কোন জায়গায় ছিল তার ওপর।

ভাগ্যক্রমে, Rust code ব্যবহার করে loop থেকে বেরিয়ে আসার একটি উপায়ও দেয়। তুমি loop-টি কখন execute করা বন্ধ করবে তা program-কে বলতে loop-এর ভেতরে `break` keyword বসাতে পারো। মনে করো আমরা এটি guessing game-এর [“Quitting After a Correct Guess”][quitting-after-a-correct-guess]<!-- ignore --> section-এ Chapter 2-তে করেছিলাম, ব্যবহারকারী সঠিক number guess করে game জেতার পর program থেকে exit করার জন্য।

আমরা guessing game-এ `continue`-ও ব্যবহার করেছিলাম, যা একটি loop-এ program-কে বলে এই iteration-এর বাকি যত code আছে সব skip করে পরের iteration-এ যেতে।

#### Returning Values from Loops

একটি `loop`-এর ব্যবহার হলো এমন কোনো operation retry করা যা ব্যর্থ হতে পারে বলে তুমি জানো, যেমন একটি thread তার কাজ শেষ করেছে কি না তা check করা। তোমার হয়তো সেই operation-এর result টি loop-এর বাইরে তোমার code-এর বাকি অংশে পাস করাও দরকার। এটি করতে, তুমি loop থামাতে যে `break` expression ব্যবহার করো তার পরে returned করতে চাও এমন value যোগ করতে পারো; সেই value টি loop-এর বাইরে returned হবে যাতে তুমি সেটি ব্যবহার করতে পারো, যেমন এখানে দেখানো হয়েছে:

```rust
fn main() {
    let mut counter = 0;

    let result = loop {
        counter += 1;

        if counter == 10 {
            break counter * 2;
        }
    };

    println!("The result is {result}");
}
```

Loop-এর আগে, আমরা `counter` নামের একটি variable declare করি এবং এটিকে `0` দিয়ে initialize করি। তারপর, আমরা loop থেকে returned হওয়া value ধরে রাখার জন্য `result` নামে একটি variable declare করি। Loop-এর প্রতিটি iteration-এ, আমরা `counter` variable-এ `1` যোগ করি, এবং তারপর check করি `counter` টি `10`-এর সমান কি না। যখন সমান হয়, আমরা `break` keyword-এর সাথে `counter * 2` value ব্যবহার করি। Loop-এর পর, আমরা `result`-এ value assign করা statement শেষ করতে একটি semicolon ব্যবহার করি। সবশেষে, আমরা `result`-এর value print করি, যা এই ক্ষেত্রে `20`।

তুমি একটি loop-এর ভেতর থেকেও `return` করতে পারো। যদিও `break` শুধু বর্তমান loop থেকে exit করে, `return` সবসময় বর্তমান function থেকে exit করে।

<!-- Old headings. Do not remove or links may break. -->
<a id="loop-labels-to-disambiguate-between-multiple-loops"></a>

#### Disambiguating with Loop Labels

তোমার যদি loop-এর ভেতরে loop থাকে, `break` এবং `continue` সেই মুহূর্তের innermost loop-এ প্রযোজ্য হয়। তুমি optional ভাবে একটি loop-এ একটি _loop label_ specify করতে পারো যা তুমি তারপর `break` বা `continue`-এর সাথে ব্যবহার করে specify করতে পারবে যে সেই keyword-গুলো innermost loop-এর বদলে labeled loop-এ প্রযোজ্য হবে। Loop label অবশ্যই একটি single quote দিয়ে শুরু হতে হবে। এখানে দুটি nested loop-সহ একটি উদাহরণ দেওয়া হলো:

```rust
fn main() {
    let mut count = 0;
    'counting_up: loop {
        println!("count = {count}");
        let mut remaining = 10;

        loop {
            println!("remaining = {remaining}");
            if remaining == 9 {
                break;
            }
            if count == 2 {
                break 'counting_up;
            }
            remaining -= 1;
        }

        count += 1;
    }
    println!("End count = {count}");
}
```

Outer loop-টির label `'counting_up`, এবং এটি 0 থেকে 2 পর্যন্ত count up করবে। Label-বিহীন inner loop টি 10 থেকে 9 পর্যন্ত count down করে। প্রথম `break` যেটি কোনো label specify করে না সেটি শুধু inner loop থেকে exit করবে। `break 'counting_up;` statement-টি outer loop থেকে exit করবে। এই code টি print করে:

```console
$ cargo run
   Compiling loops v0.1.0 (file:///projects/loops)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.58s
     Running `target/debug/loops`
count = 0
remaining = 10
remaining = 9
count = 1
remaining = 10
remaining = 9
count = 2
remaining = 10
End count = 2
```

<!-- Old headings. Do not remove or links may break. -->
<a id="conditional-loops-with-while"></a>

#### Streamlining Conditional Loops with while

প্রায়ই একটি program-এর কোনো loop-এর ভেতরে কোনো condition evaluate করার প্রয়োজন হয়। Condition `true` থাকা পর্যন্ত loop টি run হয়। Condition টি `true` না হলে program `break` call করে, loop থামিয়ে দেয়। `loop`, `if`, `else`, এবং `break`-এর সমন্বয়ে এই ধরনের behavior implement করা সম্ভব; তুমি চাইলে এখন একটি program-এ সেটা চেষ্টা করে দেখতে পারো। তবে এই pattern টি এতটাই সাধারণ যে Rust-এ এর জন্য একটি built-in language construct আছে, যাকে `while` loop বলা হয়। Listing 3-3-তে, আমরা `while` ব্যবহার করে program-টিকে তিনবার loop করি, প্রতিবার count down করি, এবং তারপর loop-এর পর একটি message print করে exit করি।

<Listing number="3-3" file-name="src/main.rs" caption="Using a `while` loop to run code while a condition evaluates to `true`">

```rust
fn main() {
    let mut number = 3;

    while number != 0 {
        println!("{number}!");

        number -= 1;
    }

    println!("LIFTOFF!!!");
}
```

</Listing>

এই construct টি `loop`, `if`, `else`, এবং `break` ব্যবহার করলে যে nesting দরকার হতো তার অনেকটাই দূর করে দেয়, এবং এটি আরও পরিষ্কার। কোনো condition `true` evaluate হওয়া পর্যন্ত code টি run হয়; অন্যথায়, এটি loop থেকে exit করে।

#### Looping Through a Collection with `for`

তুমি চাইলে `while` construct ব্যবহার করে কোনো collection, যেমন একটি array-র, element-গুলোর ওপর loop করতে পারো। যেমন, Listing 3-4-তে loop-টি `a` array-র প্রতিটি element print করে।

<Listing number="3-4" file-name="src/main.rs" caption="Looping through each element of a collection using a `while` loop">

```rust
fn main() {
    let a = [10, 20, 30, 40, 50];
    let mut index = 0;

    while index < 5 {
        println!("the value is: {}", a[index]);

        index += 1;
    }
}
```

</Listing>

এখানে, code টি array-র element গুলোর মধ্য দিয়ে count up করে। এটি index `0` থেকে শুরু করে এবং তারপর array-র শেষ index না পৌঁছানো পর্যন্ত loop করে (অর্থাৎ, যখন `index < 5` আর `true` থাকে না)। এই code টি run করলে array-র প্রতিটি element print হবে:

```console
$ cargo run
   Compiling loops v0.1.0 (file:///projects/loops)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.32s
     Running `target/debug/loops`
the value is: 10
the value is: 20
the value is: 30
the value is: 40
the value is: 50
```

পাঁচটি array value-ই প্রত্যাশিতভাবে terminal-এ দেখা যায়। যদিও `index` কখনো এক সময় `5` value-তে পৌঁছাবে, loop টি array থেকে ষষ্ঠ কোনো value fetch করার চেষ্টার আগেই execute করা বন্ধ করে দেয়।

তবে এই পদ্ধতিটি error-prone; index value বা test condition ভুল হলে আমরা program-টিকে panic করাতে পারি। যেমন, তুমি যদি `a` array-র definition কে চারটি element-এ পরিবর্তন করো কিন্তু condition টি `while index < 4` এ আপডেট করতে ভুলে যাও, তাহলে code টি panic করবে। এটি ধীরও, কারণ compiler loop-এর প্রতিটি iteration-এ index টি array-র bounds-এর মধ্যে আছে কি না তার conditional check perform করার জন্য runtime code যোগ করে।

একটি আরও সংক্ষিপ্ত alternative হিসেবে, তুমি একটি `for` loop ব্যবহার করতে পারো এবং একটি collection-এর প্রতিটি item-এর জন্য কিছু code execute করতে পারো। একটি `for` loop Listing 3-5-এর code-এর মতো দেখায়।

<Listing number="3-5" file-name="src/main.rs" caption="Looping through each element of a collection using a `for` loop">

```rust
fn main() {
    let a = [10, 20, 30, 40, 50];

    for element in a {
        println!("the value is: {element}");
    }
}
```

</Listing>

এই code টি run করলে আমরা Listing 3-4-এর মতো একই output দেখব। তার চেয়ে গুরুত্বপূর্ণ, আমরা এখন code-টির safety বাড়িয়েছি এবং array-র শেষের বাইরে চলে যাওয়া অথবা যথেষ্ট দূরে না যেয়ে কিছু item miss করার কারণে হতে পারে এমন bug-এর সম্ভাবনা দূর করেছি। `for` loop থেকে generated machine code আরও efficient হতে পারে কারণ প্রতিটি iteration-এ index-টিকে array-র length-এর সাথে compare করার দরকার নেই।

`for` loop ব্যবহার করলে, তুমি Listing 3-4-এর পদ্ধতির মতো array-তে value সংখ্যা পরিবর্তন করলে অন্য কোনো code পরিবর্তন করতে মনে রাখার দরকার নেই।

`for` loop-গুলোর safety এবং conciseness এগুলোকে Rust-এ সবচেয়ে বেশি ব্যবহৃত loop construct বানিয়েছে। এমন পরিস্থিতিতেও যেখানে তুমি কোনো code নির্দিষ্ট সংখ্যক বার run করতে চাও, যেমন Listing 3-3-তে `while` loop ব্যবহৃত countdown উদাহরণে, বেশিরভাগ Rustacean একটি `for` loop ব্যবহার করবেন। সেটি করার উপায় হলো standard library দ্বারা provide করা একটি `Range` ব্যবহার করা, যা একটি number থেকে শুরু করে আরেকটি number-এর আগে শেষ হয়ে সব number ক্রমানুসারে generate করে।

এখানে একটি `for` loop এবং আরেকটি method যা নিয়ে আমরা এখনও কথা বলিনি—`rev`, যা range-টিকে reverse করে—ব্যবহার করে countdown টি দেখতে কেমন হবে:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    for number in (1..4).rev() {
        println!("{number}!");
    }
    println!("LIFTOFF!!!");
}
```

এই code টি একটু ভালো, তাই না?

## Summary

তুমি পারিয়েছ! এটি একটি বড় chapter ছিল: তুমি variables, scalar এবং compound data type, function, comment, `if` expression, এবং loop সম্পর্কে জানলে! এই chapter-এ আলোচিত concept-গুলো দিয়ে practice করতে নিচের কাজগুলো করার program বানানোর চেষ্টা করো:

- Fahrenheit এবং Celsius-এর মধ্যে temperature convert করো।
- *n*তম Fibonacci number generate করো।
- গানের repetition-এর সুবিধা নিয়ে Christmas carol “The Twelve Days of Christmas”-এর গানের কথা print করো।

তুমি যখন এগিয়ে যাওয়ার জন্য প্রস্তুত, আমরা Rust-এ এমন একটি concept নিয়ে কথা বলব যা অন্যান্য programming language-এ সাধারণভাবে _থাকে না_: ownership।

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[quitting-after-a-correct-guess]: ch02-00-guessing-game-tutorial.html#quitting-after-a-correct-guess

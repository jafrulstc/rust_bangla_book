<!-- Old headings. Do not remove or links may break. -->

<a id="the-match-control-flow-operator"></a>

## `match` Control Flow Construct

Rust-এ `match` নামে একটি অত্যন্ত শক্তিশালী control flow construct আছে যা তোমাকে একটি value-কে একাধিক pattern-এর সাথে তুলনা করতে এবং কোন pattern match করে তার ভিত্তিতে code execute করতে দেয়। Pattern গুলো literal value, variable name, wildcard ইত্যাদি অনেক কিছু দিয়ে গঠিত হতে পারে; [Chapter 19][ch19-00-patterns]<!-- ignore --> সব ধরনের pattern এবং সেগুলো কী করে তা আলোচনা করে। `match`-এর শক্তি আসে pattern-গুলোর expressiveness থেকে এবং এই ব্যাপার থেকে যে compiler নিশ্চিত করে যে সব সম্ভাব্য case-ই handle করা হয়েছে।

একটি `match` expression-কে এমন একটি coin-sorting machine (মুদ্রা বাছাই যন্ত্র) হিসেবে ভাবতে পারো: মুদ্রা গুলো একটি পথ বেয়ে নিচে নেমে যায় যাতে বিভিন্ন মাপের গর্ত রয়েছে, এবং প্রতিটি মুদ্রা প্রথম যে গর্তে নিজের মাপে মানিয়ে যায় সেখান দিয়ে নিচে পড়ে যায়। একইভাবে, একটি `match`-এ value-গুলো প্রতিটি pattern-এর মধ্য দিয়ে যায়, এবং যে প্রথম pattern-এ value-টি "fit" হয়, সেখানে value-টি সংশ্লিষ্ট code block-এ প্রবেশ করে যা execution-এর সময় ব্যবহৃত হয়।

মুদ্রার কথা উঠলে চলো মুদ্রাকেই একটি উদাহরণ হিসেবে `match`-এর সাথে ব্যবহার করি! আমরা এমন একটি function লিখতে পারি যা একটি অজানা US মুদ্রা নেয় এবং counting machine-এর মতো করে নির্ধারণ করে এটি কোন মুদ্রা এবং তার value cent-এ ফেরত দেয়, যেমনটা Listing 6-3-তে দেখানো হয়েছে।

<Listing number="6-3" caption="একটি enum এবং একটি `match` expression যার pattern গুলো ঐ enum-এর variants">

```rust
enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter,
}

fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter => 25,
    }
}
```

</Listing>

চলো `value_in_cents` function-টির ভেতরের `match`-টি একটু খুলে দেখি। প্রথমে আমরা `match` keyword-টি দিয়ে তারপর একটি expression দিয়েছি, যা এই ক্ষেত্রে `coin` value-টি। এটা `if`-এর সাথে ব্যবহৃত conditional expression-এর মতো মনে হলেও একটা বড় পার্থক্য আছে: `if`-এর ক্ষেত্রে condition-টি একটি Boolean value-তে evaluate করতে হয়, কিন্তু এখানে যেকোনো type হতে পারে। এই উদাহরণে `coin`-এর type হলো `Coin` enum যা আমরা প্রথম লাইনে define করেছি।

এরপর আসে `match` arm গুলো। একটি arm-এর দুটি অংশ: একটি pattern এবং কিছু code। এখানে প্রথম arm-এর pattern হলো `Coin::Penny` value, এবং তারপর `=>` operator যা pattern এবং run করার জন্য code-কে আলাদা করে। এই ক্ষেত্রে code-টি হলো শুধু `1` value। প্রতিটি arm পরের arm থেকে একটি comma দিয়ে আলাদা করা থাকে।

যখন `match` expression execute হয়, তখন এটি result value-টিকে প্রতিটি arm-এর pattern-এর সাথে ক্রমান্বয়ে তুলনা করে। কোনো pattern যদি value-টির সাথে match করে, তবে সেই pattern-এর সাথে যুক্ত code execute হয়। যদি pattern-টি value-এর সাথে match না করে, তবে execution পরের arm-এ চলে যায়, ঠিক coin-sorting machine-এর মতো। আমাদের যত খুশি তত arm থাকতে পারে: Listing 6-3-তে আমাদের `match`-এ চারটি arm আছে।

প্রতিটি arm-এর সাথে যুক্ত code হলো একটি expression, এবং match করা arm-এর সেই expression-এর result value-টিই পুরো `match` expression-এর জন্য return হওয়া value।

যদি match arm-এর code ছোট হয়, যেমন Listing 6-3-তে যেখানে প্রতিটি arm শুধু একটি value return করে, সেক্ষেত্রে আমরা সাধারণত curly bracket ব্যবহার করি না। যদি তুমি একটি match arm-এ একাধিক লাইনের code run করতে চাও, তবে curly bracket ব্যবহার করতেই হবে, এবং সেক্ষেত্রে arm-এর শেষের comma-টি optional হয়ে যায়। উদাহরণস্বরূপ, নিচের code-টি method-টিকে `Coin::Penny` দিয়ে call করলে প্রতিবার "Lucky penny!" প্রিন্ট করে, কিন্তু এটি তবুও সেই block-এর শেষ value `1`-ই return করে:

```rust
fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => {
            println!("Lucky penny!");
            1
        }
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter => 25,
    }
}
```

### Pattern-এর সাথে Value Bind করা

Match arm-গুলোর আরেকটি কাজের feature হলো সেগুলো pattern-এর সাথে match হওয়া value-টির অংশের সাথে bind করতে পারে। এভাবেই আমরা enum variant-এর ভেতর থেকে value বের করতে পারি।

উদাহরণ হিসেবে চলো আমাদের enum variant-গুলোর একটিকে এমনভাবে পরিবর্তন করি যাতে এটি ভেতরে data ধরে রাখে। 1999 থেকে 2008 সাল পর্যন্ত United States প্রতিটি 50 state-এর জন্য আলাদা design সহ quarter তৈরি করেছিল একপাশে। অন্য কোনো মুদ্রায় state design ছিল না, তাই শুধু quarter-এই এই অতিরিক্ত value বহন করে। আমরা এই তথ্য আমাদের `enum`-এ যোগ করতে পারি `Quarter` variant-কে পরিবর্তন করে এর ভেতরে একটি `UsState` value সংরক্ষণ করার মাধ্যমে, যেমনটা আমরা Listing 6-4-তে করেছি।

<Listing number="6-4" caption="একটি `Coin` enum যার `Quarter` variant একটি `UsState` value-ও ধরে রাখে">

```rust
#[derive(Debug)] // so we can inspect the state in a minute
enum UsState {
    Alabama,
    Alaska,
    // --snip--
}

enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter(UsState),
}
```

</Listing>

কল্পনা করো একজন বন্ধু ৫০টি state quarter-এর সম্পূর্ণ সংগ্রহ করতে চাইছে। আমরা যখন আমাদের ছোটখাটো মুদ্রাগুলো ধরন অনুযায়ী বাছাই করবো, তখন প্রতিটি quarter-এর সাথে যুক্ত state-এর নামও বলে দেবো যাতে সেটি যদি আমার বন্ধুর সংগ্রহে না থাকে, তবে সে সেটি সংগ্রহে যোগ করতে পারে।

এই code-এর match expression-এ আমরা `state` নামে একটি variable যোগ করি সেই pattern-এ যা `Coin::Quarter` variant-এর value-গুলোর সাথে match করে। যখন একটি `Coin::Quarter` match করবে, তখন `state` variable-টি ঐ quarter-এর state-এর value-এর সাথে bind হবে। তারপর আমরা সেই arm-এর code-এ `state` ব্যবহার করতে পারবো, এভাবে:

```rust
fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter(state) => {
            println!("State quarter from {state:?}!");
            25
        }
    }
}
```

যদি আমরা `value_in_cents(Coin::Quarter(UsState::Alaska))` call করতাম, তবে `coin` value হতো `Coin::Quarter(UsState::Alaska)`। যখন আমরা সেই value-টিকে প্রতিটি match arm-এর সাথে তুলনা করি, তখন `Coin::Quarter(state)`-এ পৌঁানোর আগ পর্যন্ত কোনো arm-ই match করে না। সেই মুহূর্তে, `state`-এর binding হবে value `UsState::Alaska`। এরপর আমরা সেই binding-টি `println!` expression-এ ব্যবহার করতে পারি, ফলে `Quarter`-এর জন্য `Coin` enum variant-এর ভেতরের state value-টি পেয়ে যাই।

<!-- Old headings. Do not remove or links may break. -->

<a id="matching-with-optiont"></a>

### `Option<T>`-এর সাথে `match` Pattern


পূর্ববর্তী section-এ, আমরা `Option<T>` ব্যবহারের সময় `Some` case-এর ভেতর থেকে `T` value বের করতে চেয়েছিলাম; আমরা `Coin` enum-এর মতোই `Option<T>`-কেও `match` দিয়ে handle করতে পারি! মুদ্রা তুলনার বদলে আমরা `Option<T>`-এর variants গুলোর তুলনা করবো, কিন্তু `match` expression-টি যেভাবে কাজ করে তা একই থাকে।

ধরো আমরা এমন একটি function লিখতে চাই যা একটি `Option<i32>` নেয় এবং, যদি ভেতরে কোনো value থাকে, তবে সেই value-এর সাথে 1 যোগ করে। যদি ভেতরে কোনো value না থাকে, তবে function-টি `None` value return করবে এবং কোনো operation চালানোর চেষ্টা করবে না।

`match`-এর সুবাদে এই function-টি লেখা খুবই সহজ, এবং এটি Listing 6-5-এর মতো দেখাবে।

<Listing number="6-5" caption="একটি function যা একটি `Option<i32>`-এর উপর `match` expression ব্যবহার করে">

```rust
    fn plus_one(x: Option<i32>) -> Option<i32> {
        match x {
            None => None,
            Some(i) => Some(i + 1),
        }
    }

    let five = Some(5);
    let six = plus_one(five);
    let none = plus_one(None);
}
```

</Listing>

চলো `plus_one`-এর প্রথম execution-টি একটু বিস্তারিত দেখি। যখন আমরা `plus_one(five)` call করি, তখন `plus_one`-এর body-তে variable `x`-এর value হবে `Some(5)`। তারপর আমরা সেটিকে প্রতিটি match arm-এর সাথে তুলনা করি:

```rust,ignore
            None => None,
```

`Some(5)` value-টি `None` pattern-এর সাথে match করে না, তাই আমরা পরের arm-এ এগিয়ে যাই:

```rust,ignore
            Some(i) => Some(i + 1),
```

`Some(5)` কি `Some(i)`-এর সাথে match করে? হ্যাঁ! এটি একই variant। `i` টি `Some`-এর ভেতরে থাকা value-এর সাথে bind হয়, তাই `i` এর value নেয় `5`। তারপর match arm-এর code execute হয়, তাই আমরা `i`-এর value-তে 1 যোগ করি এবং ভেতরে মোট `6` সহ একটি নতুন `Some` value তৈরি করি।

এবার চলো Listing 6-5-তে `plus_one`-এর দ্বিতীয় call-টি বিবেচনা করি, যেখানে `x` হলো `None`। আমরা `match`-এ প্রবেশ করি এবং প্রথম arm-এর সাথে তুলনা করি:

```rust,ignore
            None => None,
```

এটি match করে! যোগ করার মতো কোনো value নেই, তাই program থেমে যায় এবং `=>`-এর ডান পাশের `None` value return করে। যেহেতু প্রথম arm-ই match করেছে, তাই অন্য কোনো arm-এর সাথে তুলনা করা হয় না।

`match` এবং enum-এর combination অনেক ক্ষেত্রেই কাজের। তুমি Rust code-এ এই pattern প্রচুর দেখতে পাবে: একটি enum-এর বিরুদ্ধে `match` করা, একটি variable-কে ভেতরের data-র সাথে bind করা, এবং তারপর সেটির ভিত্তিতে code execute করা। প্রথমে এটা একটু কঠিন মনে হতে পারে, কিন্তু একবার অভ্যস্ত হলে তুমি কামনা করবে যে সব language-এ এটা থাকলে ভালো হতো। এটি সব সময় user-দের প্রিয় একটি feature।

### Match গুলো Exhaustive

`match`-এর আরও একটি দিক আলোচনা করা দরকার: arm-গুলোর pattern গুলো অবশ্যই সব সম্ভাবনা cover করবে। আমাদের `plus_one` function-এর এই version-টি বিবেচনা করো, যাতে একটি bug আছে এবং যা compile হবে না:

```rust,ignore,does_not_compile
    fn plus_one(x: Option<i32>) -> Option<i32> {
        match x {
            Some(i) => Some(i + 1),
        }
    }
```

আমরা `None` case handle করিনি, তাই এই code-টি একটি bug তৈরি করবে। সৌভাগ্যক্রমে এটি এমন একটি bug যা Rust ধরতে জানে। আমরা যদি এই code compile করার চেষ্টা করি, তবে এই error পাবো:

```console
$ cargo run
   Compiling enums v0.1.0 (file:///projects/enums)
error[E0004]: non-exhaustive patterns: `None` not covered
 --> src/main.rs:3:15
  |
3 |         match x {
  |               ^ pattern `None` not covered
  |
note: `Option<i32>` defined here
 --> /rustc/88d9e12ae178fab0fb5cc050a94da85685d449ea/library/core/src/option.rs:598:0
 ::: /rustc/88d9e12ae178fab0fb5cc050a94da85685d449ea/library/core/src/option.rs:602:4
  |
  = note: not covered
  = note: the matched value is of type `Option<i32>`
help: ensure that all possible cases are being handled by adding a match arm with a wildcard pattern or an explicit pattern as shown
  |
4 ~             Some(i) => Some(i + 1),
5 ~             None => todo!(),
  |

For more information about this error, try `rustc --explain E0004`.
error: could not compile `enums` (bin "enums") due to 1 previous error
```

Rust জানে যে আমরা সব সম্ভাব্য case cover করিনি, এমনকি কোন pattern টা ভুলে গেছি সেটাও জানে! Rust-এর match গুলো _exhaustive_: code valid হতে হলে আমাদের শেষ পর্যন্ত প্রতিটি সম্ভাবনা exhaust করতে হবে। বিশেষত `Option<T>`-এর ক্ষেত্রে, যখন Rust আমাদেরকে `None` case স্পষ্টভাবে handle করতে ভুলতে দেয় না, তখন এটি আমাদেরকে এই ভুল ধরে রাখে যে হয়তো আমাদের কাছে value আছে অথচ তা null হতে পারে — ফলে আগে আলোচিত billion-dollar mistake-টি অসম্ভব হয়ে পড়ে।

### Catch-All Pattern এবং `_` Placeholder

Enum ব্যবহার করে আমরা কয়েকটি নির্দিষ্ট value-র জন্য বিশেষ action নিতে পারি, কিন্তু বাকি সব value-র জন্য একটি default action নিতে পারি। কল্পনা করো আমরা এমন একটি game implement করছি যেখানে, যদি তুমি একটি ডাইস রোলে 3 পাও, তবে তোমার player নড়ে না বরং একটা সুন্দর নতুন টুপি পায়। যদি 7 পাও, তবে তোমার player একটি সুন্দর টুপি হারায়। অন্য সব value-র জন্য, তোমার player সেই সংখ্যক ঘর game board-এ সামনে যায়। এখানে একটি `match` দেওয়া হলো যা সেই logic implement করে, যেখানে ডাইস রোলের result টি একটি random value-র বদলে hardcoded করা হয়েছে, এবং বাকি সব logic function দিয়ে দেখানো হয়েছে যাদের কোনো body নেই, কারণ এই উদাহরণে সেগুলো আসলে implement করা scope-এর বাইরে:

```rust
    let dice_roll = 9;
    match dice_roll {
        3 => add_fancy_hat(),
        7 => remove_fancy_hat(),
        other => move_player(other),
    }

    fn add_fancy_hat() {}
    fn remove_fancy_hat() {}
    fn move_player(num_spaces: u8) {}
```

প্রথম দুটি arm-এ pattern গুলো হলো literal value `3` এবং `7`। বাকি সব সম্ভাব্য value cover করে এমন শেষ arm-টির pattern হলো সেই variable যার নাম আমরা `other` দিয়েছি। `other` arm-এর জন্য run হওয়া code-টি সেই variable-টিকে `move_player` function-এ পাস করে ব্যবহার করে।

এই code compile হয়, যদিও আমরা একটি `u8`-এর সব সম্ভাব্য value তালিকাবদ্ধ করিনি, কারণ শেষ pattern-টি স্পষ্টভাবে তালিকাভুক্ত নয় এমন সব value-র সাথে match করবে। এই catch-all pattern-টি `match`-এর exhaustive হওয়ার শর্ত পূরণ করে। খেয়াল করো যে আমাদের catch-all arm-টি সবার শেষে রাখতে হবে, কারণ pattern গুলো ক্রমান্বয়ে evaluate হয়। যদি আমরা catch-all arm-টি আগে রাখতাম, তবে অন্য arm গুলো আর কখনোই run হতো না, তাই একটি catch-all-এর পরে আর arm যোগ করলে Rust আমাদের সতর্ক করবে!

Rust-এ আরও একটি pattern আছে যা আমরা তখন ব্যবহার করতে পারি যখন একটি catch-all চাই কিন্তু catch-all pattern-এর value টি _use_ করতে চাই না: `_` হলো একটি বিশেষ pattern যা যেকোনো value-র সাথে match করে এবং সেই value-র সাথে bind করে না। এটি Rust-কে জানায় যে আমরা value-টি ব্যবহার করতে যাচ্ছি না, তাই Rust একটি unused variable সম্পর্কে আমাদের সতর্ক করবে না।

চলো game-টির নিয়ম পরিবর্তন করি: এখন তুমি যদি 3 বা 7 ছাড়া অন্য কিছু রোল করো, তবে আবার রোল করতে হবে। আমরা আর catch-all value ব্যবহার করতে চাই না, তাই আমরা `other` নামের variable-টির বদলে `_` ব্যবহার করে আমাদের code পরিবর্তন করতে পারি:

```rust
    let dice_roll = 9;
    match dice_roll {
        3 => add_fancy_hat(),
        7 => remove_fancy_hat(),
        _ => reroll(),
    }

    fn add_fancy_hat() {}
    fn remove_fancy_hat() {}
    fn reroll() {}
```

এই উদাহরণটিও exhaustive হওয়ার শর্ত পূরণ করে, কারণ আমরা শেষ arm-এ অন্য সব value স্পষ্টভাবে ignore করছি; আমরা কিছুই ভুলিনি।

সবশেষে, আমরা আবার একবার game-টির নিয়ম পরিবর্তন করবো যাতে তুমি 3 বা 7 ছাড়া অন্য কিছু রোল করলে তোমার পালায় আর কিছুই না ঘটে। আমরা সেটি `_` arm-এর সাথে যুক্ত code হিসেবে unit value (["The Tuple Type"][tuples]<!-- ignore --> section-এ উল্লেখিত empty tuple type) ব্যবহার করে প্রকাশ করতে পারি:

```rust
    let dice_roll = 9;
    match dice_roll {
        3 => add_fancy_hat(),
        7 => remove_fancy_hat(),
        _ => (),
    }

    fn add_fancy_hat() {}
    fn remove_fancy_hat() {}
```

এখানে আমরা Rust-কে স্পষ্টভাবে বলছি যে আগের কোনো arm-এর pattern-এর সাথে match না হওয়া অন্য কোনো value আমরা ব্যবহার করবো না, এবং এই ক্ষেত্রে আমরা কোনো code run করতে চাই না।

Pattern এবং matching সম্পর্কে আরও অনেক কিছু আছে যা আমরা [Chapter 19][ch19-00-patterns]<!-- ignore -->-এ আলোচনা করবো। আপাতত, আমরা `if let` syntax-এ এগিয়ে যাবো, যা এমন পরিস্থিতিতে কাজে লাগে যেখানে `match` expression-টি একটু বেশি verbose।

[tuples]: ch03-02-data-types.html#the-tuple-type
[ch19-00-patterns]: ch19-00-patterns.html

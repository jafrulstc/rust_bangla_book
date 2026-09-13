## `if let` এবং `let...else` দিয়ে Concise Control Flow

`if let` syntax তোমাকে `if` এবং `let`-কে একসাথে এমনভাবে যুক্ত করতে দেয় যা একটি pattern-এর সাথে match হওয়া value-গুলো handle করার জন্য কম verbose উপায়, বাকি গুলো ignore করে। Listing 6-6-এর program-টি বিবেচনা করো যা `config_max` variable-তে থাকা একটি `Option<u8>` value-তে match করে কিন্তু শুধু তখনই code execute করতে চায় যখন value-টি `Some` variant হয়।

<Listing number="6-6" caption="একটি `match` যা শুধু value যখন `Some` হয় তখনই code execute করা নিয়ে চিন্তা করে">

```rust
    let config_max = Some(3u8);
    match config_max {
        Some(max) => println!("The maximum is configured to be {max}"),
        _ => (),
    }
```

</Listing>

যদি value `Some` হয়, তবে আমরা pattern-এ value-টিকে `max` variable-এর সাথে bind করে `Some` variant-এর value-টি প্রিন্ট করি। আমরা `None` value নিয়ে কিছু করতে চাই না। `match` expression-এর শর্ত পূরণের জন্য আমাদের শুধু একটি variant process করার পরেও `_ => ()` যোগ করতে হয়, যা যোগ করতে বেশ বিরক্তিকর boilerplate code।

তার বদলে আমরা এটিকে `if let` ব্যবহার করে আরও সংক্ষেপে লিখতে পারি। নিচের code-টি Listing 6-6-এর `match`-টির মতোই আচরণ করে:

```rust
    let config_max = Some(3u8);
    if let Some(max) = config_max {
        println!("The maximum is configured to be {max}");
    }
```

`if let` syntax একটি pattern এবং একটি expression নেয় যাদের মাঝে একটি equal sign থাকে। এটি `match`-এর মতোই কাজ করে, যেখানে expression-টি `match`-কে দেওয়া হয় এবং pattern-টি হয় তার প্রথম arm। এই ক্ষেত্রে pattern-টি হলো `Some(max)`, এবং `max` টি `Some`-এর ভেতরের value-এর সাথে bind হয়। তারপর আমরা `if let` block-এর body-তে `max` ব্যবহার করতে পারি, ঠিক যেমন আমরা সংশ্লিষ্ট `match` arm-এ `max` ব্যবহার করেছিলাম। `if let` block-এর code শুধু তখনই run হয় যখন value-টি pattern-এর সাথে match করে।

`if let` ব্যবহার করার অর্থ হলো কম typing, কম indentation, এবং কম boilerplate code। তবে, তুমি `match`-এর সেই exhaustive checking হারাও যা নিশ্চিত করে যে তুমি কোনো case handle করতে ভুলে যাচ্ছো না। `match` এবং `if let`-এর মধ্যে কোনটা বেছে নেবে তা নির্ভর করে তোমার নির্দিষ্ট পরিস্থিতিতে তুমি কী করছো এবং conciseness অর্জন করা exhaustive checking হারানোর বিনিময়ে ঠিক আছে কিনা তার উপর।

অন্য কথায়, তুমি `if let`-কে এমন একটি `match`-এর syntax sugar হিসেবে ভাবতে পারো যা value যখন একটি pattern-এর সাথে match করে তখন code run করে এবং বাকি সব value ignore করে।

আমরা একটি `if let`-এর সাথে একটি `else` যুক্ত করতে পারি। `else`-এর সাথে যুক্ত code block-টি ঠিক সেই block-টির মতোই যা `if let` এবং `else`-এর সমতুল্য `match` expression-এর `_` case-এর সাথে যুক্ত থাকতো। Listing 6-4-তে `Coin` enum definition-টি মনে করো, যেখানে `Quarter` variant একটি `UsState` value-ও ধরে রাখতো। যদি আমরা quarter-এর state ঘোষণা করার সাথে সাথে সব non-quarter মুদ্রা count করতে চাইতাম, তবে সেটি আমরা একটি `match` expression দিয়ে করতে পারতাম, এভাবে:

```rust
    let mut count = 0;
    match coin {
        Coin::Quarter(state) => println!("State quarter from {state:?}!"),
        _ => count += 1,
    }
```

অথবা আমরা একটি `if let` এবং `else` expression ব্যবহার করতে পারতাম, এভাবে:

```rust
    let mut count = 0;
    if let Coin::Quarter(state) = coin {
        println!("State quarter from {state:?}!");
    } else {
        count += 1;
    }
```

## `let...else` দিয়ে "Happy Path"-এ থাকা

সাধারণ pattern টি হলো — যখন একটি value উপস্থিত থাকে তখন কিছু computation করা এবং অন্যথায় একটি default value return করা। `UsState` value সহ মুদ্রার আমাদের উদাহরণটি এগিয়ে নিয়ে যেতে গিয়ে, যদি আমরা quarter-এ থাকা state-এর বয়সের উপর নির্ভর করে কিছু মজার কথা বলতে চাইতাম, তবে আমরা `UsState`-এ একটি method যোগ করতে পারি যা একটি state-এর বয়স যাচাই করবে, এভাবে:

```rust
impl UsState {
    fn existed_in(&self, year: u16) -> bool {
        match self {
            UsState::Alabama => year >= 1819,
            UsState::Alaska => year >= 1959,
            // -- snip --
        }
    }
}
```

তারপর, আমরা হয়তো মুদ্রার ধরনের উপর `if let` দিয়ে match করতাম, যেমনটা Listing 6-7-এ condition-এর body-তে একটি `state` variable যোগ করা হয়েছে।

<Listing number="6-7" caption="`if let`-এর ভেতরে nested condition ব্যবহার করে একটি state 1900 সালে ছিল কিনা তা যাচাই করা">

```rust
fn describe_state_quarter(coin: Coin) -> Option<String> {
    if let Coin::Quarter(state) = coin {
        if state.existed_in(1900) {
            Some(format!("{state:?} is pretty old, for America!"))
        } else {
            Some(format!("{state:?} is relatively new."))
        }
    } else {
        None
    }
}
```

</Listing>

এটি কাজ তো সম্পন্ন করে, কিন্তু এটি কাজটিকে `if let` statement-এর body-এর ভেতরে ঠেলে দিয়েছে, এবং যদি করণীয় কাজটি আরও জটিল হয়, তবে বোঝা কঠিন হতে পারে যে top-level branch গুলো কীভাবে সম্পর্কিত। আমরা এই বিষয়টির সুযোগ নিতে পারি যে expression গুলো value উৎপন্ন করে — হয় `if let` থেকে `state` উৎপন্ন করতে পারি নয়তো আগে ফেরত যেতে পারি, যেমন Listing 6-8-এ। (তুমি একই জিনিস একটি `match` দিয়েও করতে পারতে।)

<Listing number="6-8" caption="value উৎপন্ন করতে বা আগে ফেরত যেতে `if let` ব্যবহার করা">

```rust
fn describe_state_quarter(coin: Coin) -> Option<String> {
    let state = if let Coin::Quarter(state) = coin {
        state
    } else {
        return None;
    };

    if state.existed_in(1900) {
        Some(format!("{state:?} is pretty old, for America!"))
    } else {
        Some(format!("{state:?} is relatively new."))
    }
}
```

</Listing>

তবে এটি তার নিজস্ব উপায়ে অনুসরণ করতে কিছুটা বিরক্তিকর! `if let`-এর একটি branch value উৎপন্ন করে, এবং অন্যটি সম্পূর্ণভাবে function থেকে ফেরত যায়।

এই সাধারণ pattern-টিকে আরও সুন্দরভাবে প্রকাশ করার জন্য, Rust-এ `let...else` আছে। `let...else` syntax এর বাম পাশে একটি pattern এবং ডান পাশে একটি expression নেয়, যা `if let`-এর মতোই, কিন্তু এর কোনো `if` branch নেই, শুধু একটি `else` branch আছে। যদি pattern match করে, তবে এটি pattern থেকে value-টিকে outer scope-এ bind করবে। যদি pattern match _না_ করে, তবে program `else` arm-এ প্রবেশ করবে, যার ফলে function থেকে ফেরত যেতেই হবে।

Listing 6-9-তে তুমি দেখতে পাবে `if let`-এর বদলে `let...else` ব্যবহার করলে Listing 6-8 কেমন দেখায়।

<Listing number="6-9" caption="function-এর মধ্য দিয়ে flow পরিষ্কার করতে `let...else` ব্যবহার করা">

```rust
fn describe_state_quarter(coin: Coin) -> Option<String> {
    let Coin::Quarter(state) = coin else {
        return None;
    };

    if state.existed_in(1900) {
        Some(format!("{state:?} is pretty old, for America!"))
    } else {
        Some(format!("{state:?} is relatively new."))
    }
}
```

</Listing>

খেয়াল করো যে এভাবে এটি function-এর প্রধান body-তে "happy path"-এ থাকে, `if let` যেমন দুটি branch-এর জন্য উল্লেখযোগ্যভাবে ভিন্ন control flow ছিল তেমন নয়।

যদি তোমার এমন পরিস্থিতি হয় যেখানে তোমার program-এর logic একটি `match` দিয়ে প্রকাশ করতে গেলে খুব verbose হয়ে যায়, তবে মনে রাখবে যে `if let` এবং `let...else`-ও তোমার Rust toolbox-এ আছে।

## Summary

এখন আমরা cover করেছি কীভাবে enum ব্যবহার করে এমন custom type তৈরি করা যায় যা একগুচ্ছ enumerated value-এর একটি হতে পারে। আমরা দেখিয়েছি কীভাবে standard library-র `Option<T>` type তোমাকে type system ব্যবহার করে error প্রতিরোধে সাহায্য করে। যখন enum value-গুলোর ভেতরে data থাকে, তখন তুমি কতগুলো case handle করতে চাও তার উপর নির্ভর করে সেই value গুলো extract করে ব্যবহার করার জন্য তুমি `match` বা `if let` ব্যবহার করতে পারো।

তোমার Rust program গুলো এখন struct এবং enum ব্যবহার করে তোমার domain-এর ধারণা প্রকাশ করতে পারে। API-তে ব্যবহারের জন্য custom type তৈরি করা type safety নিশ্চিত করে: compiler নিশ্চিত করবে যে তোমার function গুলো শুধুমাত্র প্রতিটি function-এর প্রত্যাশিত type-এর value-ই পাবে।

তোমার user-দের কাছে একটি সুসংগঠিত API প্রদান করতে যা ব্যবহার করা সহজ এবং যা শুধু তোমার user-দের যা দরকার ঠিক ততটাই প্রকাশ করে, চলো এবার Rust-এর module গুলোর দিকে এগোই।

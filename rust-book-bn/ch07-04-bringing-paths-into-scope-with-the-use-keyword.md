## `use` Keyword দিয়ে Path-কে Scope-এ আনা

Function call করার জন্য প্রতিবার পুরো path লিখতে হয় — এটা অসুবিধাজনক এবং বারবার একই জিনিস লেখার মতো মনে হতে পারে। Listing 7-7-তে, আমরা `add_to_waitlist` function-এর জন্য absolute নাকি relative path যেটাই বেছে নিই না কেন, প্রতিবার `add_to_waitlist` call করার সময় আমাদের `front_of_house` এবং `hosting`-ও specify করতে হতো। সৌভাগ্যক্রমে এই প্রক্রিয়াটি সহজ করার একটা উপায় আছে: আমরা একবার `use` keyword দিয়ে কোনো path-এর shortcut তৈরি করে নিতে পারি, এবং তারপর scope-এর অন্য কোথাও ছোট নামটি ব্যবহার করতে পারি।

Listing 7-11-তে আমরা `crate::front_of_house::hosting` module-টিকে `eat_at_restaurant` function-এর scope-এ নিয়ে এসেছি, যাতে `eat_at_restaurant`-এর ভেতরে `add_to_waitlist` function call করতে শুধু `hosting::add_to_waitlist` specify করলেই চলে।

<Listing number="7-11" file-name="src/lib.rs" caption="`use` দিয়ে একটি module-কে scope-এ আনা">

```rust,noplayground,test_harness
mod front_of_house {
    pub mod hosting {
        pub fn add_to_waitlist() {}
    }
}

use crate::front_of_house::hosting;

pub fn eat_at_restaurant() {
    hosting::add_to_waitlist();
}
```

</Listing>

কোনো scope-এ `use` এবং একটি path যোগ করা filesystem-এ symbolic link তৈরি করার মতো। crate root-এ `use crate::front_of_house::hosting` যোগ করার ফলে, `hosting` এখন সেই scope-এ একটি valid নাম, ঠিক যেন `hosting` module-টিই crate root-এ define করা ছিল। `use` দিয়ে scope-এ আনা path অন্যান্য path-এর মতোই privacy check করে।

খেয়াল করো `use` শুধু সেই scope-এর জন্য shortcut তৈরি করে যেখানে `use` লেখা হয়েছে। Listing 7-12 `eat_at_restaurant` function-টিকে `customer` নামে একটি নতুন child module-এ move করে, যা `use` statement থেকে আলাদা একটি scope, তাই function body compile হবে না।

<Listing number="7-12" file-name="src/lib.rs" caption="একটি `use` statement শুধু যে scope-এ আছে সেখানেই প্রযোজ্য।">

```rust,noplayground,test_harness,does_not_compile,ignore
mod front_of_house {
    pub mod hosting {
        pub fn add_to_waitlist() {}
    }
}

use crate::front_of_house::hosting;

mod customer {
    pub fn eat_at_restaurant() {
        hosting::add_to_waitlist();
    }
}
```

</Listing>

Compiler error দেখায় যে shortcut-টি `customer` module-এর ভেতরে আর প্রযোজ্য নয়:

```console
$ cargo build
   Compiling restaurant v0.1.0 (file:///projects/restaurant)
error[E0433]: cannot find module or crate `hosting` in this scope
  --> src/lib.rs:11:9
   |
11 |         hosting::add_to_waitlist();
   |         ^^^^^^^ use of unresolved module or unlinked crate `hosting`
   |
   = help: if you wanted to use a crate named `hosting`, use `cargo add hosting` to add it to your `Cargo.toml`
help: consider importing this module through its public re-export
   |
10 +     use crate::hosting;
   |

warning: unused import: `crate::front_of_house::hosting`
 --> src/lib.rs:7:5
  |
7 | use crate::front_of_house::hosting;
  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  |
  = note: `#[warn(unused_imports)]` (part of `#[warn(unused)]`) on by default

For more information about this error, try `rustc --explain E0433`.
warning: `restaurant` (lib) generated 1 warning
error: could not compile `restaurant` (lib) due to 1 previous error; 1 warning emitted
```

খেয়াল করো এখানে একটা warning আছে যে `use`-টি আর তার scope-এ ব্যবহৃত হচ্ছে না! এই সমস্যার সমাধান করতে হলে `use`-টিকেও `customer` module-এর ভেতরে move করো, অথবা child `customer` module-এর ভেতর থেকে parent module-এর shortcut-কে `super::hosting` দিয়ে refer করো।

### Idiomatic `use` Path তৈরি করা

Listing 7-11-তে তুমি হয়তো ভেবেছিলে আমরা কেন `use crate::front_of_house::hosting` specify করে `eat_at_restaurant`-এ `hosting::add_to_waitlist` call করলাম, কেন না Listing 7-13-এর মতো `use` path-টিকে একদম `add_to_waitlist` function পর্যন্ত টেনে একই ফল পাওয়া গেল।

<Listing number="7-13" file-name="src/lib.rs" caption="`use` দিয়ে `add_to_waitlist` function-কে scope-এ আনা, যা unidiomatic">

```rust,noplayground,test_harness
mod front_of_house {
    pub mod hosting {
        pub fn add_to_waitlist() {}
    }
}

use crate::front_of_house::hosting::add_to_waitlist;

pub fn eat_at_restaurant() {
    add_to_waitlist();
}
```

</Listing>

যদিও Listing 7-11 এবং Listing 7-13 উভয়ই একই কাজ করে, Listing 7-11 হলো `use` দিয়ে function scope-ে আনার idiomatic উপায়। Function-এর parent module-কে `use` দিয়ে scope-এ আনলে function call করার সময় আমাদের parent module-টি specify করতে হয়। Function call করার সময় parent module specify করলে বোঝা যায় যে function-টি locally define করা নয়, সেই সাথে পুরো path-এর পুনরাবৃত্তিও কমে। Listing 7-13-এর code থেকে স্পষ্ট নয় যে `add_to_waitlist` কোথায় define করা।

অন্যদিকে, struct, enum এবং অন্যান্য item-কে `use` দিয়ে scope-ে আনার সময় full path specify করাটাই idiomatic। Listing 7-14 standard library-র `HashMap` struct-কে একটি binary crate-এর scope-এ আনার idiomatic উপায় দেখায়।

<Listing number="7-14" file-name="src/main.rs" caption="`HashMap`-কে idiomatic উপায়ে scope-ে আনা">

```rust
use std::collections::HashMap;

fn main() {
    let mut map = HashMap::new();
    map.insert(1, 2);
}
```

</Listing>

এই idiom-এর পেছনে কোনো শক্তিশালী কারণ নেই: এটি শুধু এমন একটি convention যা গড়ে উঠেছে, এবং মানুষ Rust code এভাবেই পড়তে ও লিখতে অভ্যস্ত হয়েছে।

এই idiom-এর একটি ব্যতিক্রম হলো যদি তুমি একই নামের দুটি item-কে `use` statement দিয়ে scope-ে আনতে চান, কারণ Rust সেটা অনুমোদন করে না। Listing 7-15 দেখায় কীভাবে একই নামের কিন্তু ভিন্ন parent module-এর দুটি `Result` type-কে scope-এ আনা যায়, এবং কীভাবে তাদের refer করা যায়।

<Listing number="7-15" file-name="src/lib.rs" caption="একই নামের দুটি type-কে একই scope-এ আনতে হলে তাদের parent module ব্যবহার করতে হয়।">

```rust,noplayground
use std::fmt;
use std::io;

fn function1() -> fmt::Result {
    // --snip--
}

fn function2() -> io::Result<()> {
    // --snip--
}
```

</Listing>

দেখতেই পাচ্ছ, parent module ব্যবহার করলে দুটি `Result` type আলাদা করা যায়। যদি আমরা তার বদলে `use std::fmt::Result` এবং `use std::io::Result` specify করতাম, তবে একই scope-ে দুটি `Result` type চলে আসত, এবং `Result` ব্যবহার করলে Rust বুঝতে পারত না কোনটি বোঝানো হয়েছে।

### `as` Keyword দিয়ে নতুন নাম দেওয়া

একই নামের দুটি type-কে `use` দিয়ে একই scope-এ আনার সমস্যার আরেকটি সমাধান আছে: path-এর পরে আমরা `as` এবং type-টির জন্য একটি নতুন local নাম, বা _alias_, specify করতে পারি। Listing 7-16 Listing 7-15-এর code-টিকে অন্যভাবে লেখার উপায় দেখায়, যেখানে দুটি `Result` type-এর একটিকে `as` দিয়ে rename করা হয়েছে।

<Listing number="7-16" file-name="src/lib.rs" caption="`as` keyword দিয়ে scope-ে আনার সময় একটি type-এর নাম পরিবর্তন করা">

```rust,noplayground
use std::fmt::Result;
use std::io::Result as IoResult;

fn function1() -> Result {
    // --snip--
}

fn function2() -> IoResult<()> {
    // --snip--
}
```

</Listing>

দ্বিতীয় `use` statement-এ আমরা `std::io::Result` type-টির জন্য নতুন নাম `IoResult` বেছে নিয়েছি, যা `std::fmt` থেকে আসা `Result`-এর সাথে conflict করবে না — সেটিকেও আমরা scope-এ এনেছি। Listing 7-15 এবং Listing 7-16 দুটোই idiomatic, তাই পছন্দ তোমার!

### `pub use` দিয়ে নাম Re-export করা

আমরা `use` keyword দিয়ে কোনো নাম scope-ে আনলে সেই নামটি যে scope-এ import করা হয়েছে সেখানে private থাকে। সেই scope-এর বাইরের code যাতে সেই নামটিকে ওই scope-ে define করা হয়েছে এমনভাবে refer করতে পারে, সে জন্য আমরা `pub` এবং `use` একসাথে ব্যবহার করতে পারি। এই technique-কে _re-exporting_ বলা হয়, কারণ আমরা একটি item-কে scope-ে আনছি কিন্তু সেই সাথে সেই item-টিকে অন্যদের নিজেদের scope-ে আনার জন্যও available করছি।

Listing 7-17 Listing 7-11-এর code-টি দেখায়, root module-এর `use`-কে `pub use`-তে পরিবর্তন করা হয়েছে।

<Listing number="7-17" file-name="src/lib.rs" caption="`pub use` দিয়ে একটি নামকে নতুন scope থেকে যেকোনো code-এর ব্যবহারের জন্য available করা">

```rust,noplayground,test_harness
mod front_of_house {
    pub mod hosting {
        pub fn add_to_waitlist() {}
    }
}

pub use crate::front_of_house::hosting;

pub fn eat_at_restaurant() {
    hosting::add_to_waitlist();
}
```

</Listing>

এই পরিবর্তনের আগে, external code-কে `add_to_waitlist` function-টি `restaurant::front_of_house::hosting::add_to_waitlist()` path দিয়ে call করতে হতো, যার জন্য `front_of_house` module-কেও `pub` হিসেবে চিহ্নিত করতে হতো। এখন এই `pub use` root module থেকে `hosting` module-টিকে re-export করেছে, তাই external code `restaurant::hosting::add_to_waitlist()` path ব্যবহার করতে পারবে।

Re-exporting তখন কাজে লাগে যখন তোমার code-এর internal structure এমনভাবে না থাকে যেমনভাবে তোমার code call করা programmer-রা domain সম্পর্কে ভাববেন। যেমন, এই রেস্তোরাঁর রূপকে রেস্তোরাঁ চালানো মানুষ ভাবেন “front of house” এবং “back of house” হিসেবে। কিন্তু রেস্তোরাঁয় আসা customer সম্ভবত এই ভাবে রেস্তোরাঁর অংশগুলো নিয়ে ভাববেন না। `pub use` ব্যবহার করে আমরা আমাদের code এক structure-এ লিখতে পারি কিন্তু ভিন্ন structure expose করতে পারি। এতে আমাদের library library-তে কাজ করা programmer-দের জন্য এবং library call করা programmer-দের জন্য সুসংগঠিত হয়। `pub use`-এর আরেকটি example এবং এটি তোমার crate-এর documentation-কে কীভাবে প্রভাবিত করে তা আমরা Chapter 14-এর [“Exporting a Convenient Public API”][ch14-pub-use]<!-- ignore --> section-এ দেখব।

### External Package ব্যবহার করা

Chapter 2-তে আমরা একটি guessing game project প্রোগ্রাম করেছিলাম যা random সংখ্যা পাওয়ার জন্য `rand` নামের একটি external package ব্যবহার করত। আমাদের project-এ `rand` ব্যবহার করতে আমরা _Cargo.toml_-এ এই লাইনটি যোগ করেছিলাম:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch02-00-guessing-game-tutorial.md
* ch14-03-cargo-workspaces.md
-->

<Listing file-name="Cargo.toml">

```toml
rand = "0.10.1"
```

</Listing>

_Cargo.toml_-এ `rand`-কে dependency হিসেবে যোগ করলে Cargo [crates.io](https://crates.io/)-থেকে `rand` package এবং তার যেকোনো dependency download করে এবং `rand`-কে আমাদের project-এ available করে।

তারপর, `rand` definition-গুলোকে আমাদের package-এর scope-ে আনতে আমরা crate-এর নাম `rand` দিয়ে শুরু হওয়া একটি `use` লাইন যোগ করেছিলাম এবং যেসব item scope-ে আনতে চেয়েছি সেগুলো তালিকাভুক্ত করেছি। মনে করো Chapter 2-এর [“Generating a Random Number”][rand]<!-- ignore --> section-এ আমরা `rand::prelude` module-এর item-গুলো scope-ে এনেছিলাম এবং `rand::rng` function call করেছিলাম:

```rust,ignore
// ANCHOR: all
use std::io;

// ANCHOR: ch07-04
use rand::prelude::*;

fn main() {
    // ANCHOR_END: ch07-04
    println!("Guess the number!");

    // ANCHOR: ch07-04
    let secret_number = rand::rng().random_range(1..=100);
    // ANCHOR_END: ch07-04

    println!("The secret number is: {secret_number}");

    println!("Please input your guess.");

    let mut guess = String::new();

    io::stdin()
        .read_line(&mut guess)
        .expect("Failed to read line");

    println!("You guessed: {guess}");
    // ANCHOR: ch07-04
}
// ANCHOR_END: ch07-04
// ANCHOR_END: all
```

Rust community-র সদস্যরা [crates.io](https://crates.io/)-তে অনেকগুলো package available করে রেখেছেন, এবং এগুলোর যেকোনোটিকে তোমার package-এ টেনে আনতে একই ধাপ দরকার: সেগুলোকে তোমার package-এর _Cargo.toml_ file-ে তালিকাভুক্ত করা এবং `use` ব্যবহার করে সেগুলোর crate থেকে item scope-ে আনা।

খেয়াল রাখো, standard `std` library-ও আমাদের package-এর বাইরের একটি crate। যেহেতু standard library Rust language-এর সাথেই ship করা হয়, তাই `std` অন্তর্ভুক্ত করতে _Cargo.toml_ পরিবর্তন করতে হয় না। কিন্তু সেখান থেকে আমাদের package-এর scope-ে item আনতে `use` দিয়ে refer করতে হয়। যেমন, `HashMap`-এর জন্য আমরা এই লাইনটি ব্যবহার করব:

```rust
use std::collections::HashMap;
```

এটি একটি absolute path যা `std` দিয়ে শুরু — standard library crate-টির নাম।

<!-- Old headings. Do not remove or links may break. -->

<a id="using-nested-paths-to-clean-up-large-use-lists"></a>

### Nested Path ব্যবহার করে বড় `use` List পরিষ্কার রাখা

যদি আমরা একই crate বা একই module-এ define করা একাধিক item ব্যবহার করি, তবে প্রতিটি item আলাদা লাইনে তালিকাভুক্ত করলে আমাদের file-এ অনেক vertical জায়গা দখল হতে পারে। যেমন, Listing 2-4-এর guessing game-এ আমাদের এই দুটি `use` statement ছিল যা `std` থেকে item scope-ে আনে:

<Listing file-name="src/main.rs">

```rust,ignore
// --snip--
use std::cmp::Ordering;
use std::io;
// --snip--
```

</Listing>

এর বদলে আমরা nested path ব্যবহার করে একই item-গুলো এক লাইনে scope-ে আনতে পারি। এটি করতে হলে path-এর common অংশটি specify করতে হয়, তারপর দুটি colon, এবং তারপর path-গুলোর যে অংশ ভিন্ন সেগুলোর তালিকা দিয়ে দিতে হয় curly bracket-এ, যেমন Listing 7-18-তে দেখানো হয়েছে।

<Listing number="7-18" file-name="src/main.rs" caption="একই prefix-এর একাধিক item scope-ে আনতে nested path specify করা">

```rust,ignore
// --snip--
use std::{cmp::Ordering, io};
// --snip--
```

</Listing>

বড় প্রোগ্রামে, একই crate বা module থেকে অনেক item nested path দিয়ে scope-ে আনলে আলাদা `use` statement-এর সংখ্যা অনেক কমে যায়!

আমরা কোনো path-এর যেকোনো স্তরে nested path ব্যবহার করতে পারি, যা তখন কাজে লাগে যখন একটি common subpath share করে এমন দুটি `use` statement একত্রিত করতে চাই। যেমন, Listing 7-19 দুটি `use` statement দেখায়: একটি `std::io`-কে scope-ে আনে এবং একটি `std::io::Write`-কে scope-ে আনে।

<Listing number="7-19" file-name="src/lib.rs" caption="দুটি `use` statement যেখানে একটি অপরটির subpath">

```rust,noplayground
use std::io;
use std::io::Write;
```

</Listing>

এই দুটি path-এর common অংশ হলো `std::io`, এবং সেটিই প্রথম পুরো path। এই দুটি path-কে একটি `use` statement-এ মার্জ করতে আমরা nested path-এ `self` ব্যবহার করতে পারি, যেমন Listing 7-20-তে দেখানো হয়েছে।

<Listing number="7-20" file-name="src/lib.rs" caption="Listing 7-19-এর path-গুলোকে একটি `use` statement-এ একত্রিত করা">

```rust,noplayground
use std::io::{self, Write};
```

</Listing>

এই লাইনটি `std::io` এবং `std::io::Write` উভয়কেই scope-ে আনে।

<!-- Old headings. Do not remove or links may break. -->

<a id="the-glob-operator"></a>

### Glob Operator দিয়ে Item Import করা

যদি আমরা কোনো path-এ define করা সব public item scope-ে আনতে চাই, তবে সেই path-এর পরে `*` glob operator specify করতে পারি:

```rust
use std::collections::*;
```

এই `use` statement-টি `std::collections`-এ define করা সব public item current scope-ে আনে। Glob operator ব্যবহারে সাবধান! Glob ব্যবহার করলে বুঝতে কঠিন হয়ে যায় কোন নামগুলো scope-এ আছে এবং তোমার প্রোগ্রামে ব্যবহৃত কোনো নাম কোথায় define করা ছিল। এছাড়া, যদি dependency তার definition পরিবর্তন করে, তবে তুমি যা import করেছ তাও পরিবর্তন হয়ে যায় — যার ফলে dependency upgrade করার সময় compiler error আসতে পারে, যেমন যদি dependency তোমার একই scope-এর কোনো definition-এর নামের সাথে মিলে যায় এমন একটি definition যোগ করে।

Glob operator প্রায়শই testing-এর সময় ব্যবহৃত হয় test করা সব কিছুকে `tests` module-ে আনার জন্য; এ বিষয়ে আমরা Chapter 11-এর [“How to Write Tests”][writing-tests]<!-- ignore --> section-ে কথা বলব। Glob operator কখনো কখনো prelude pattern-এর অংশ হিসেবেও ব্যবহৃত হয়: সেই pattern সম্পর্কে আরও তথ্যের জন্য [the standard library documentation](../std/prelude/index.html#other-preludes)<!-- ignore --> দেখো।

[ch14-pub-use]: ch14-02-publishing-to-crates-io.html#exporting-a-convenient-public-api
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number
[writing-tests]: ch11-01-writing-tests.html#how-to-write-tests

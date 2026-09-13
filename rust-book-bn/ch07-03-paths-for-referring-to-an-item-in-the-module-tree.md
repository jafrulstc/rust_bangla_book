## Module Tree-তে কোনো Item-কে Refer করার জন্য Path

Rust-কে কোনো module tree-তে কোনো item কোথায় পাওয়া যাবে তা দেখাতে আমরা filesystem navigate করার সময় path যেভাবে ব্যবহার করি, সেভাবে path ব্যবহার করি। কোনো function-কে call করতে হলে আমাদের তার path জানতে হবে।

Path দুটি form-এ আসতে পারে:

- একটি _absolute path_ হলো crate root থেকে শুরু হওয়া পুরো path; অন্য কোনো external crate-এর code-এর জন্য absolute path শুরু হয় crate-এর নাম দিয়ে, আর current crate-এর code-এর জন্য এটি শুরু হয় literal `crate` দিয়ে।
- একটি _relative path_ শুরু হয় current module থেকে এবং `self`, `super`, অথবা current module-এর কোনো identifier ব্যবহার করে।

Absolute এবং relative উভয় path-ই এক বা একাধিক identifier দ্বারা গঠিত হয়, যেগুলো double colon (`::`) দিয়ে আলাদা করা থাকে।

Listing 7-1-তে ফিরে গিয়ে ধরো আমরা `add_to_waitlist` function-টিকে call করতে চাই। এটি এটা জিজ্ঞেস করার মতো: `add_to_waitlist` function-টির path কী? Listing 7-3-এ Listing 7-1 দেওয়া আছে, কিছু module ও function বাদ দিয়ে।

আমরা `eat_at_restaurant` নামের একটি নতুন function থেকে `add_to_waitlist` function-টিকে call করার দুটি উপায় দেখাব, যে function-টি crate root-এ define করা। এই path-গুলো সঠিক, কিন্তু আরও একটি সমস্যা বাকি আছে যার কারণে এই example-টি এভাবে compile হবে না। কেন সেটা আমরা একটু পরে ব্যাখ্যা করব।

`eat_at_restaurant` function-টি আমাদের library crate-এর public API-এর অংশ, তাই আমরা এটিকে `pub` keyword দিয়ে চিহ্নিত করেছি। [“Exposing Paths with the `pub` Keyword”][pub]<!-- ignore --> section-এ আমরা `pub` সম্পর্কে আরও বিস্তারিত জানাব।

<Listing number="7-3" file-name="src/lib.rs" caption="Absolute এবং relative path ব্যবহার করে `add_to_waitlist` function-কে call করা">

```rust,ignore,does_not_compile
mod front_of_house {
    mod hosting {
        fn add_to_waitlist() {}
    }
}

pub fn eat_at_restaurant() {
    // Absolute path
    crate::front_of_house::hosting::add_to_waitlist();

    // Relative path
    front_of_house::hosting::add_to_waitlist();
}
```

</Listing>

`eat_at_restaurant`-এ আমরা প্রথমবার `add_to_waitlist` function-কে call করার সময় absolute path ব্যবহার করেছি। `add_to_waitlist` function-টি `eat_at_restaurant`-এর একই crate-এ define করা, যার মানে আমরা `crate` keyword ব্যবহার করে absolute path শুরু করতে পারি। তারপর আমরা পরপর প্রতিটি module অন্তর্ভুক্ত করি যতক্ষণ না `add_to_waitlist`-এ পৌঁছাই। তুমি এমন একটি filesystem কল্পনা করতে পারো যার structure একই রকম: `add_to_waitlist` program-টি run করতে আমরা path `/front_of_house/hosting/add_to_waitlist` উল্লেখ করতাম; `crate` নাম দিয়ে crate root থেকে শুরু করা ঠিক তোমার shell-এ filesystem root থেকে শুরু করতে `/` ব্যবহারের মতো।

`eat_at_restaurant`-এ দ্বিতীয়বার `add_to_waitlist` call করার সময় আমরা relative path ব্যবহার করেছি। Path শুরু হয়েছে `front_of_house` দিয়ে — module tree-তে `eat_at_restaurant`-এর একই স্তরে define করা সেই module-টির নাম। এখানে filesystem-এর সমতুল্য হবে `front_of_house/hosting/add_to_waitlist` path ব্যবহার করা। কোনো module-এর নাম দিয়ে শুরু করার অর্থ হলো path-টি relative।

Relative নাকি absolute path ব্যবহার করবে সেটা তুমি তোমার project অনুযায়ী ঠিক করবে, এবং এটি নির্ভর করে তুমি কোনো item-এর definition code সেই item-টি ব্যবহার করে এমন code থেকে আলাদাভাবে নাকি একসাথে move করতে বেশি পারো কিনা। যেমন, যদি আমরা `front_of_house` module এবং `eat_at_restaurant` function-কে একসাথে একটি `customer_experience` নামের module-এ move করি, তবে `add_to_waitlist`-এর absolute path আপডেট করতে হবে, কিন্তু relative path এখনও valid থাকবে। কিন্তু যদি আমরা `eat_at_restaurant` function-টিকে আলাদাভাবে `dining` নামে একটি module-এ move করি, তবে `add_to_waitlist` call-এর absolute path একই থাকবে, কিন্তু relative path আপডেট করতে হবে। সাধারণভাবে আমাদের পছন্দ absolute path ব্যবহার করা, কারণ বেশিরভাগ ক্ষেত্রেই আমরা চাই code definition এবং item call স্বাধীনভাবে move করতে পারি।

চলো Listing 7-3 compile করার চেষ্টা করি এবং দেখি কেন এটি এখনও compile হয় না! আমরা যে error গুলো পাব সেগুলো Listing 7-4-এ দেখানো হয়েছে।

<Listing number="7-4" caption="Listing 7-3-এর code build করার সময় compiler error">

```console
$ cargo build
   Compiling restaurant v0.1.0 (file:///projects/restaurant)
error[E0603]: module `hosting` is private
 --> src/lib.rs:9:28
  |
9 |     crate::front_of_house::hosting::add_to_waitlist();
  |                            ^^^^^^^  --------------- function `add_to_waitlist` is not publicly re-exported
  |                            |
  |                            private module
  |
note: the module `hosting` is defined here
 --> src/lib.rs:2:5
  |
2 |     mod hosting {
  |     ^^^^^^^^^^^

error[E0603]: module `hosting` is private
  --> src/lib.rs:12:21
   |
12 |     front_of_house::hosting::add_to_waitlist();
   |                     ^^^^^^^  --------------- function `add_to_waitlist` is not publicly re-exported
   |                     |
   |                     private module
   |
note: the module `hosting` is defined here
  --> src/lib.rs:2:5
   |
 2 |     mod hosting {
   |     ^^^^^^^^^^^

For more information about this error, try `rustc --explain E0603`.
error: could not compile `restaurant` (lib) due to 2 previous errors
```

</Listing>

Error message বলছে যে `hosting` module-টি private। অন্য কথায়, `hosting` module এবং `add_to_waitlist` function-এর জন্য আমাদের path সঠিক, কিন্তু Rust আমাদের সেগুলো ব্যবহার করতে দেবে না কারণ private section-এ এর access নেই। Rust-এ সব item (function, method, struct, enum, module এবং constant) ডিফল্টভাবে তার parent module-এর কাছে private। তুমি কোনো function বা struct-এর মতো item-কে private করতে চাইলে সেটিকে একটি module-এর ভেতরে রাখো।

Parent module-এর item-গুলো child module-এর ভেতরের private item ব্যবহার করতে পারে না, কিন্তু child module-এর item-গুলো তাদের ancestor module-এর item ব্যবহার করতে পারে। এর কারণ child module তাদের implementation detail wrap করে লুকিয়ে রাখে, কিন্তু child module যে context-এ define করা সেটা দেখতে পায়। আমাদের রূপক এগিয়ে নিয়ে যেতে গেলে privacy rule-গুলোকে রেস্তোরাঁর back office-এর মতো ভাবতে পারো: সেখানে যা হয় সেটা রেস্তোরাঁর customer-দের কাছে private, কিন্তু office manager যে রেস্তোরাঁ চালান সেখানে সব কিছু দেখতে ও করতে পারেন।

Rust এভাবে module system কাজ করার ব্যবস্থা করেছে যাতে inner implementation detail লুকানোটাই ডিফল্ট হয়। ফলে তুমি জানো তোমার inner code-এর কোন অংশগুলো outer code না ভেঙে পরিবর্তন করতে পারবে। তবে Rust `pub` keyword ব্যবহার করে কোনো item-কে public করে child module-এর code-এর inner অংশ ancestor module-এর কাছে expose করার সুযোগ দেয়।

### `pub` Keyword দিয়ে Path Expose করা

চলো Listing 7-4-এর error-এ ফিরে যাই যেখানে বলা হয়েছিল `hosting` module-টি private। আমরা চাই parent module-এর `eat_at_restaurant` function যেন child module-এর `add_to_waitlist` function-এ access পায়, তাই আমরা Listing 7-5-এর মতো `hosting` module-কে `pub` keyword দিয়ে চিহ্নিত করি।

<Listing number="7-5" file-name="src/lib.rs" caption="`eat_at_restaurant` থেকে ব্যবহার করতে `hosting` module-কে `pub` হিসেবে declare করা">

```rust,ignore,does_not_compile
mod front_of_house {
    pub mod hosting {
        fn add_to_waitlist() {}
    }
}

// -- snip --
```

</Listing>

দুর্ভাগ্যবশত Listing 7-5-এর code-টি এখনও compiler error দেয়, যেমন Listing 7-6-এ দেখানো হয়েছে।

<Listing number="7-6" caption="Listing 7-5-এর code build করার সময় compiler error">

```console
$ cargo build
   Compiling restaurant v0.1.0 (file:///projects/restaurant)
error[E0603]: function `add_to_waitlist` is private
  --> src/lib.rs:10:37
   |
10 |     crate::front_of_house::hosting::add_to_waitlist();
   |                                     ^^^^^^^^^^^^^^^ private function
   |
note: the function `add_to_waitlist` is defined here
  --> src/lib.rs:3:9
   |
 3 |         fn add_to_waitlist() {}
   |         ^^^^^^^^^^^^^^^^^^^^

error[E0603]: function `add_to_waitlist` is private
  --> src/lib.rs:13:30
   |
13 |     front_of_house::hosting::add_to_waitlist();
   |                              ^^^^^^^^^^^^^^^ private function
   |
note: the function `add_to_waitlist` is defined here
  --> src/lib.rs:3:9
   |
 3 |         fn add_to_waitlist() {}
   |         ^^^^^^^^^^^^^^^^^^^^

For more information about this error, try `rustc --explain E0603`.
error: could not compile `restaurant` (lib) due to 2 previous errors
```

</Listing>

কী হলো? `mod hosting`-এর সামনে `pub` keyword যোগ করলে module-টি public হয়ে যায়। এই পরিবর্তনের ফলে, যদি আমরা `front_of_house`-এ access পাই, তবে `hosting`-এও access পাব। কিন্তু `hosting`-এর _content_ এখনও private; module-টিকে public করলে তার content public হয়ে যায় না। কোনো module-এর উপর `pub` keyword শুধু ancestor module-এর code-কে সেটিকে refer করতে দেয়, তার inner code-এ access দেয় না। যেহেতু module হলো container, শুধু module-টিকে public করে খুব বেশি কিছু করা যায় না; আমাদের এক ধাপ এগিয়ে যেতে হবে এবং module-এর ভেতরের এক বা একাধিক item-কেও public করতে হবে।

Listing 7-6-এর error গুলো বলছে `add_to_waitlist` function-টি private। Privacy rule module-এর পাশাপাশি struct, enum, function এবং method-এর ক্ষেত্রেও প্রযোজ্য।

চলো Listing 7-7-এর মতো `add_to_waitlist` function-টির definition-এর আগে `pub` keyword যোগ করে সেটিকেও public করি।

<Listing number="7-7" file-name="src/lib.rs" caption="`mod hosting` এবং `fn add_to_waitlist`-এ `pub` keyword যোগ করলে `eat_at_restaurant` থেকে function-টিকে call করা যায়।">

```rust,noplayground,test_harness
mod front_of_house {
    pub mod hosting {
        pub fn add_to_waitlist() {}
    }
}

// -- snip --
```

</Listing>

এখন code compile হবে! কেন `pub` keyword যোগ করলে privacy rule মেনে `eat_at_restaurant`-এ এই path-গুলো ব্যবহার করা যায় তা বুঝতে চলো absolute এবং relative path-গুলো দেখি।

Absolute path-এ আমরা শুরু করি `crate` দিয়ে, আমাদের crate-এর module tree-এর root। `front_of_house` module-টি crate root-এ define করা। যদিও `front_of_house` public নয়, যেহেতু `eat_at_restaurant` function-টি `front_of_house`-এর একই module-এ define করা (অর্থাৎ `eat_at_restaurant` এবং `front_of_house` sibling), তাই `eat_at_restaurant` থেকে আমরা `front_of_house`-কে refer করতে পারি। এরপর আসে `pub` দিয়ে চিহ্নিত `hosting` module। আমরা `hosting`-এর parent module-এ access পাই, তাই `hosting`-এও access পাই। সবশেষে, `add_to_waitlist` function-টি `pub` দিয়ে চিহ্নিত, এবং আমরা এর parent module-এ access পাই, তাই এই function call কাজ করবে!

Relative path-এ logic absolute path-এর মতোই, শুধু প্রথম ধাপটা ছাড়া: crate root থেকে শুরু না করে path শুরু হয় `front_of_house` থেকে। `front_of_house` module-টি `eat_at_restaurant`-এর একই module-এ define করা, তাই যে module-এ `eat_at_restaurant` define করা সেখান থেকে শুরু হওয়া relative path কাজ করে। তারপর, যেহেতু `hosting` এবং `add_to_waitlist` `pub` দিয়ে চিহ্নিত, path-এর বাকি অংশ কাজ করে এবং এই function call-টি valid!

যদি তুমি তোমার library crate অন্যান্য project যাতে ব্যবহার করতে পারে সেভাবে share করার পরিকল্পনা করো, তবে তোমার public API হলো তোমার crate-এর user-দের সাথে একটি contract যা নির্ধারণ করে তারা কীভাবে তোমার code-এর সাথে interact করবে। Public API-এ পরিবর্তন ম্যানেজ করার সময় এমন অনেক বিষয় বিবেচনা করতে হয় যাতে অন্যের তোমার crate-এর উপর depend করা সহজ হয়। এই বিষয়গুলো এই book-এর scope-এর বাইরে; এ বিষয়ে আগ্রহী হলে [the Rust API Guidelines][api-guidelines] দেখো।

> #### Binary এবং Library সহ Package-এর জন্য Best Practice
>
> আমরা বলেছিলাম একটি package-ে _src/main.rs_ binary crate root এবং _src/lib.rs_ library crate root উভয়ই থাকতে পারে, এবং ডিফল্টভাবে দুটি crate-এরই নাম package-টির নামের সাথে একই হবে। সাধারণত, যে package-গুলোতে library এবং binary crate উভয়ই থাকে সেগুলোতে binary crate-এ ঠিক ততটুকু code থাকে যতটুকু দরকার একটি executable শুরু করতে যা library crate-এ define করা code-কে call করে। এর ফলে অন্যান্য project package-টির বেশিরভাগ functionality থেকে উপকৃত হতে পারে কারণ library crate-এর code share করা যায়।
>
> Module tree _src/lib.rs_-এ define করা থাকা উচিত। তারপর, যেকোনো public item binary crate-এ package-টির নাম দিয়ে path শুরু করে ব্যবহার করা যাবে। Binary crate তখন library crate-এর একজন user হয়ে যায়, ঠিক যেমন একটি সম্পূর্ণ external crate এই library crate-টি ব্যবহার করত: এটি শুধু public API-ই ব্যবহার করতে পারবে। এটি তোমাকে ভালো API design করতে সাহায্য করে; তুমি শুধু author-ই নও, তুমি client-ও!
>
> [Chapter 12][ch12]<!-- ignore -->-তে আমরা এই organization practice দেখাব একটি command line program দিয়ে যাতে একটি binary crate এবং একটি library crate উভয়ই থাকবে।

### `super` দিয়ে Relative Path শুরু করা

আমরা `super` ব্যবহার করে এমন relative path তৈরি করতে পারি যা current module বা crate root-এর বদলে parent module থেকে শুরু হয়। এটি filesystem path-কে `..` syntax দিয়ে শুরু করার মতো, যা parent directory-তে যাওয়া বোঝায়। `super` ব্যবহার করে আমরা এমন একটি item-কে refer করতে পারি যেটি আমরা জানি parent module-এ আছে, যা module tree পুনর্বিন্যাস করা সহজ করে তোলে যখন module-টি তার parent-এর সাথে ঘনিষ্ঠভাবে সম্পর্কিত কিন্তু parent সম্ভবত একদিন module tree-এর অন্য কোথাও move হয়ে যেতে পারে।

Listing 7-8-এর code-টি এমন পরিস্থিতি model করে যেখানে একজন chef ভুল order ঠিক করে স্বয়ং customer-এর কাছে নিয়ে যান। `back_of_house` module-এ define করা `fix_incorrect_order` function-টি parent module-এ define করা `deliver_order` function-কে `super` দিয়ে শুরু করা path উল্লেখ করে call করে।

<Listing number="7-8" file-name="src/lib.rs" caption="`super` দিয়ে শুরু হওয়া relative path ব্যবহার করে function call করা">

```rust,noplayground,test_harness
fn deliver_order() {}

mod back_of_house {
    fn fix_incorrect_order() {
        cook_order();
        super::deliver_order();
    }

    fn cook_order() {}
}
```

</Listing>

`fix_incorrect_order` function-টি `back_of_house` module-এ আছে, তাই আমরা `super` ব্যবহার করে `back_of_house`-এর parent module-এ যেতে পারি, যা এই ক্ষেত্রে `crate`, অর্থাৎ root। সেখান থেকে আমরা `deliver_order` খুঁজি এবং পেয়ে যাই। সফল! আমরা মনে করি `back_of_house` module এবং `deliver_order` function-টি সম্ভবত একে অপরের সাথে একই সম্পর্কে থাকবে এবং crate-এর module tree পুনর্বিন্যাস করলে একসাথে move হবে। তাই আমরা `super` ব্যবহার করেছি, যাতে ভবিষ্যতে এই code অন্য কোনো module-এ move হলে আমাদের কম জায়গায় code আপডেট করতে হয়।

### Struct এবং Enum-কে Public করা

আমরা `pub` ব্যবহার করে struct এবং enum-কেও public হিসেবে চিহ্নিত করতে পারি, কিন্তু struct এবং enum-এর সাথে `pub` ব্যবহারে কিছু extra detail আছে। যদি আমরা কোনো struct definition-এর আগে `pub` ব্যবহার করি, তবে struct-টি public হয়ে যায়, কিন্তু struct-এর field গুলো এখনও private থাকবে। আমরা প্রতিটি field আলাদাভাবে case-by-case public বা না-ও করতে পারি। Listing 7-9-তে আমরা একটি public `back_of_house::Breakfast` struct define করেছি যার `toast` field public কিন্তু `seasonal_fruit` field private। এটি এমন একটি রেস্তোরাঁর অবস্থা model করে যেখানে customer বেছে নিতে পারে তার খাবারের সাথে কোন রুটি আসবে, কিন্তু chef সিদ্ধান্ত নেন কোন ফল খাবারের সাথে দেওয়া হবে — তা নির্ভর করে কোনটি season-এ আছে এবং stock-এ আছে তার উপর। যেহেতু available ফল দ্রুত পরিবর্তন হয়, তাই customer ফল বেছে নিতে পারে না বা কোন ফল পাবে সেটাও দেখতে পারে না।

<Listing number="7-9" file-name="src/lib.rs" caption="কিছু public field এবং কিছু private field সহ একটি struct">

```rust,noplayground
mod back_of_house {
    pub struct Breakfast {
        pub toast: String,
        seasonal_fruit: String,
    }

    impl Breakfast {
        pub fn summer(toast: &str) -> Breakfast {
            Breakfast {
                toast: String::from(toast),
                seasonal_fruit: String::from("peaches"),
            }
        }
    }
}

pub fn eat_at_restaurant() {
    // Order a breakfast in the summer with Rye toast.
    let mut meal = back_of_house::Breakfast::summer("Rye");
    // Change our mind about what bread we'd like.
    meal.toast = String::from("Wheat");
    println!("I'd like {} toast please", meal.toast);

    // The next line won't compile if we uncomment it; we're not allowed
    // to see or modify the seasonal fruit that comes with the meal.
    // meal.seasonal_fruit = String::from("blueberries");
}
```

</Listing>

যেহেতু `back_of_house::Breakfast` struct-এর `toast` field public, তাই `eat_at_restaurant`-এ আমরা dot notation ব্যবহার করে `toast` field-এ লিখতে ও পড়তে পারি। খেয়াল করো `eat_at_restaurant`-এ আমরা `seasonal_fruit` field ব্যবহার করতে পারি না, কারণ `seasonal_fruit` private। `seasonal_fruit` field-এর value পরিবর্তন করে এমন লাইনটি uncomment করে দেখো কোন error পাও!

এছাড়া খেয়াল করো, যেহেতু `back_of_house::Breakfast`-এর একটি private field আছে, তাই struct-টিকে এমন একটি public associated function দিতে হবে যা `Breakfast`-এর একটি instance construct করে (আমরা এখানে নাম দিয়েছি `summer`)। যদি `Breakfast`-এর এমন কোনো function না থাকত, তবে আমরা `eat_at_restaurant`-এ `Breakfast`-এর কোনো instance তৈরি করতে পারতাম না, কারণ `eat_at_restaurant`-এ private `seasonal_fruit` field-এর value set করা যেত না।

অন্যদিকে, যদি আমরা কোনো enum-কে public করি, তবে তার সব variant তখন public হয়ে যায়। আমাদের শুধু `enum` keyword-এর আগে `pub` দিতে হয়, যেমন Listing 7-10-তে দেখানো হয়েছে।

<Listing number="7-10" file-name="src/lib.rs" caption="কোনো enum-কে public হিসেবে চিহ্নিত করলে তার সব variant public হয়ে যায়।">

```rust,noplayground
mod back_of_house {
    pub enum Appetizer {
        Soup,
        Salad,
    }
}

pub fn eat_at_restaurant() {
    let order1 = back_of_house::Appetizer::Soup;
    let order2 = back_of_house::Appetizer::Salad;
}
```

</Listing>

যেহেতু আমরা `Appetizer` enum-টিকে public করেছি, তাই `eat_at_restaurant`-এ আমরা `Soup` এবং `Salad` variant ব্যবহার করতে পারি।

Enum খুব একটা কাজের নয় যদি তার variant public না হয়; প্রতিটি enum variant-এর সাথে প্রতিবার `pub` annotate করতে হতো এটা বিরক্তিকর হতো, তাই enum variant-এর ডিফল্ট হলো public হওয়া। Struct প্রায়শই তার field public না হলেও কাজের, তাই struct field সাধারণ নিয়ম মেনে চলে — `pub` দিয়ে annotate না করা পর্যন্ত সবকিছু ডিফল্টভাবে private থাকে।

`pub`-এর সাথে জড়িত আরও একটি পরিস্থিতি আছে যা আমরা এখনও cover করিনি, এবং সেটিই আমাদের module system-এর শেষ feature: `use` keyword। আমরা প্রথমে শুধু `use`-ই cover করব, তারপর দেখাব কীভাবে `pub` এবং `use` একসাথে ব্যবহার করতে হয়।

[pub]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[api-guidelines]: https://rust-lang.github.io/api-guidelines/
[ch12]: ch12-00-an-io-project.html

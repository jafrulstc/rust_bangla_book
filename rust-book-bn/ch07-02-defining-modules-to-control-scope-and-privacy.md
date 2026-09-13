<!-- Old headings. Do not remove or links may break. -->

<a id="defining-modules-to-control-scope-and-privacy"></a>

## Modules দিয়ে Scope এবং Privacy নিয়ন্ত্রণ

এই section-এ আমরা module এবং module system-এর অন্যান্য অংশ নিয়ে কথা বলব — বিশেষ করে _path_, যা item-কে নাম দিতে দেয়; `use` keyword, যা কোনো path-কে scope-এ নিয়ে আসে; এবং `pub` keyword, যা item-কে public করে তোলে। এছাড়া আমরা `as` keyword, external package এবং glob operator নিয়েও আলোচনা করব।

### Modules Cheat Sheet

Module এবং path-এর বিস্তারিত আলোচনায় যাওয়ার আগে এখানে একটি দ্রুত reference দিচ্ছি — compiler-এ module, path, `use` keyword এবং `pub` keyword কীভাবে কাজ করে, এবং বেশিরভাগ developer কীভাবে তাদের code সাজান। এই chapter জুড়ে আমরা প্রতিটি নিয়মের example দেখব, কিন্তু module কীভাবে কাজ করে সেটা মনে করিয়ে নেওয়ার জন্য এই জায়গাটি খুব কাজের।

- **Crate root থেকে শুরু**: একটি crate compile করার সময় compiler প্রথমে crate root file-এ (library crate-এর জন্য সাধারণত _src/lib.rs_, এবং binary crate-এর জন্য _src/main.rs_) compile করার মতো code খুঁজে দেখে।
- **Module declare করা**: crate root file-এ তুমি নতুন module declare করতে পারো; ধরো `mod garden;` দিয়ে তুমি একটি “garden” module declare করলে। compiler নিচের জায়গাগুলোতে সেই module-এর code খুঁজবে:
  - Inline, `mod garden`-এর পরের সেমিকলনের পরিবর্তে ব্যবহৃত curly bracket-এর ভেতরে
  - _src/garden.rs_ file-এ
  - _src/garden/mod.rs_ file-এ
- **Submodule declare করা**: crate root ছাড়া অন্য যেকোনো file-ে তুমি submodule declare করতে পারো। যেমন, তুমি _src/garden.rs_-এ `mod vegetables;` declare করতে পারো। compiler তখন parent module-এর নামে একটি directory-র ভেতরে নিচের জায়গাগুলোতে submodule-এর code খুঁজবে:
  - Inline, `mod vegetables`-এর পরে সরাসরি curly bracket-এ সেমিকলনের বদলে
  - _src/garden/vegetables.rs_ file-এ
  - _src/garden/vegetables/mod.rs_ file-এ
- **Module-এর ভেতরের code-এর path**: একবার কোনো module তোমার crate-এর অংশ হয়ে গেলে, privacy rule যতটা অনুমোদন করে, তুমি একই crate-এর অন্য যেকোনো জায়গা থেকে সেই module-এর code-কে তার path দিয়ে refer করতে পারো। যেমন, garden vegetables module-এর একটি `Asparagus` type পাওয়া যাবে `crate::garden::vegetables::Asparagus` path-এ।
- **Private vs. public**: কোনো module-ের ভেতরের code তার parent module-এর কাছে ডিফল্টভাবে private থাকে। কোনো module-কে public করতে হলে `mod`-এর বদলে `pub mod` দিয়ে declare করো। Public module-এর ভেতরের item-গুলোকেও public করতে চাইলে সেগুলোর declaration-এর আগে `pub` ব্যবহার করো।
- **`use` keyword**: কোনো scope-এর ভেতরে `use` keyword দিয়ে item-গুলোর shortcut তৈরি করা যায়, যাতে বারবার লম্বা path লিখতে না হয়। যে কোনো scope থেকে যদি `crate::garden::vegetables::Asparagus` refer করা যায়, তবে তুমি `use crate::garden::vegetables::Asparagus;` লিখে একটি shortcut তৈরি করতে পারো, এবং তারপর থেকে সেই scope-এ ওই type ব্যবহার করতে শুধু `Asparagus` লিখলেই হবে।

এখানে আমরা `backyard` নামে একটি binary crate তৈরি করছি যা এই নিয়মগুলো দেখায়। Crate-টির directory, যার নামও _backyard_, নিচের file ও directory-গুলো ধারণ করে:

```text
backyard
├── Cargo.lock
├── Cargo.toml
└── src
    ├── garden
    │   └── vegetables.rs
    ├── garden.rs
    └── main.rs
```

এই ক্ষেত্রে crate root file হলো _src/main.rs_, যার ভেতরে আছে:

<Listing file-name="src/main.rs">

```rust,noplayground,ignore
use crate::garden::vegetables::Asparagus;

pub mod garden;

fn main() {
    let plant = Asparagus {};
    println!("I'm growing {plant:?}!");
}
```

</Listing>

`pub mod garden;` লাইনটি compiler-কে বলে দেয় _src/garden.rs_-এ যা যা code আছে সব অন্তর্ভুক্ত করতে, যা হলো:

<Listing file-name="src/garden.rs">

```rust,noplayground,ignore
pub mod vegetables;
```

</Listing>

এখানে, `pub mod vegetables;` মানে _src/garden/vegetables.rs_-এর code-ও অন্তর্ভুক্ত হলো। সেই code হলো:

```rust,noplayground,ignore
#[derive(Debug)]
pub struct Asparagus {}
```

এবার চলো এই নিয়মগুলোর বিস্তারিতে যাই এবং সেগুলো কাজ করতে দেখাই!

### Related Code Module-এ একসাথে গ্রুপ করা

_Module_ আমাদের কোনো crate-এর ভেতরে code সাজাতে দেয় — পড়তে সুবিধা হয় এবং সহজে reuse করা যায়। Module আমাদের item-এর _privacy_ নিয়ন্ত্রণ করতেও দেয়, কারণ কোনো module-ের ভেতরের code ডিফল্টভাবে private থাকে। Private item হলো internal implementation detail যা বাইরে থেকে ব্যবহার করা যায় না। আমরা চাইলে module এবং তার ভেতরের item-গুলোকে public করতে পারি, যাতে external code সেগুলো ব্যবহার করতে পারে এবং depend করতে পারে।

উদাহরণ হিসেবে চলো এমন একটি library crate লিখি যা একটি রেস্তোরাঁর functionality দেয়। আমরা function-গুলোর signature define করব কিন্তু body খালি রাখব, যাতে রেস্তোরাঁর implementation-এর বদলে শুধু code-এর organization-এর দিকে মনোযোগ দিতে পারি।

রেস্তোরাঁ শিল্পে রেস্তোরাঁর কিছু অংশকে front of house এবং কিছু অংশকে back of house বলা হয়। _Front of house_ হলো সেই জায়গা যেখানে customer থাকে; এর মধ্যে পড়ে host যেখানে customer-কে বসায়, server যেখানে order এবং payment নেয়, এবং bartender যেখানে drink বানায়। _Back of house_ হলো সেই জায়গা যেখানে chef এবং cook রান্নাঘরে কাজ করেন, dishwasher পরিষ্কার করেন, এবং manager প্রশাসনিক কাজ করেন।

আমাদের crate-কে এভাবে সাজাতে হলে আমরা এর function-গুলোকে nested module-এ ভাগ করতে পারি। `cargo new restaurant --lib` চালিয়ে `restaurant` নামে একটি নতুন library তৈরি করো। তারপর Listing 7-1-এর code _src/lib.rs_-এ লেখো কয়েকটি module ও function signature define করতে; এই code হলো front of house section।

<Listing number="7-1" file-name="src/lib.rs" caption="একটি `front_of_house` module যার ভেতরে আরও module আছে এবং সেগুলোর ভেতরে function">

```rust,noplayground
mod front_of_house {
    mod hosting {
        fn add_to_waitlist() {}

        fn seat_at_table() {}
    }

    mod serving {
        fn take_order() {}

        fn serve_order() {}

        fn take_payment() {}
    }
}
```

</Listing>

আমরা `mod` keyword এবং তার পরে module-এর নাম (এই ক্ষেত্রে `front_of_house`) দিয়ে একটি module define করি। তারপর module-এর body curly bracket-এর ভেতরে থাকে। Module-এর ভেতরে আমরা আরও module রাখতে পারি, যেমন এখানে `hosting` এবং `serving` module রাখা হয়েছে। Module-এ আরও অন্যান্য item-এর definition রাখা যায় — যেমন struct, enum, constant, trait এবং Listing 7-1-এর মতো function।

Module ব্যবহার করে আমরা সম্পর্কিত definition গুলো একসাথে গ্রুপ করতে পারি এবং নাম দিয়ে বলতে পারি কেন সেগুলো সম্পর্কিত। এই code ব্যবহার করা programmer-রা পুরো definition পড়ার বদলে গ্রুপ অনুযায়ী code navigate করতে পারবে, ফলে তাদের প্রাসঙ্গিক definition খুঁজে পাওয়া সহজ হবে। এই code-এ নতুন functionality যোগ করতে চাওয়া programmer-রাও জানবেন কোথায় code রাখলে প্রোগ্রামটি সুসংগঠিত থাকবে।

আগেই বলেছিলাম _src/main.rs_ এবং _src/lib.rs_-কে _crate root_ বলা হয়। এদের এই নাম হওয়ার কারণ — এই দুটি file-এর যেকোনো একটির content crate-এর module structure-এর root-এ `crate` নামের একটি module হিসেবে তৈরি করে, যাকে _module tree_ বলা হয়।

Listing 7-2 Listing 7-1-এর structure-এর module tree দেখায়।

<Listing number="7-2" caption="Listing 7-1-এর code-এর module tree">

```text
crate
 └── front_of_house
     ├── hosting
     │   ├── add_to_waitlist
     │   └── seat_at_table
     └── serving
         ├── take_order
         ├── serve_order
         └── take_payment
```

</Listing>

এই tree দেখায় কিছু module কীভাবে অন্য module-এর ভেতরে nest করে; যেমন `hosting` হলো `front_of_house`-এর ভেতরে nested। Tree থেকে আরও দেখা যায় কিছু module _sibling_, অর্থাৎ এরা একই module-এ define করা; `hosting` এবং `serving` হলো `front_of_house`-এ define করা sibling। যদি module A, module B-এর ভেতরে থাকে, তবে আমরা বলি module A হলো module B-এর _child_ এবং module B হলো module A-এর _parent_। খেয়াল করো পুরো module tree-টি implicit module `crate`-এর অধীনে rooted।

Module tree সম্ভবত তোমার কম্পিউটারের filesystem-এর directory tree-কে মনে করিয়ে দেবে; এটা খুব মানানসই তুলনা! Filesystem-এর directory-র মতোই তুমি তোমার code সাজাতে module ব্যবহার করো। আর directory-র ভেতরের file-এর মতোই, আমাদের module খুঁজে বের করার একটা উপায় দরকার।

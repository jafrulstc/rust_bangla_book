## Crate টি Crates.io-তে Publish করা

আমরা আমাদের project-এর dependency হিসেবে [crates.io](https://crates.io/)<!-- ignore --> থেকে package ব্যবহার করেছি, কিন্তু তুমি নিজের package publish করেও অন্য মানুষের সাথে তোমার code share করতে পারো। [crates.io](https://crates.io/)<!-- ignore -->-এর crate registry তোমার package-গুলোর source code distribute করে, তাই এটি মূলত open source code host করে।

Rust এবং Cargo-র এমন কিছু feature আছে যা তোমার publish করা package-কে মানুষের কাছে সহজে খুঁজে পাওয়া ও ব্যবহার করা সহজ করে তোলে। আমরা এখন এর মধ্যে কিছু feature নিয়ে আলোচনা করব, তারপর ব্যাখ্যা করব কীভাবে একটি package publish করতে হয়।

### কাজে লাগার মতো Documentation Comment লেখা

তোমার package সঠিকভাবে document করলে অন্যান্য user-রা বুঝতে পারবে কীভাবে এবং কখন সেগুলো ব্যবহার করতে হয়, তাই documentation লেখার জন্য সময় ব্যয় করাটা মূল্যবান। Chapter 3-তে আমরা আলোচনা করেছি কীভাবে দুটি slash, `//`, ব্যবহার করে Rust code comment করতে হয়। Rust-এ documentation-এর জন্য আরও এক ধরনের comment আছে, সুবিধাজনকভাবে যাকে _documentation comment_ বলা হয়, যা HTML documentation তৈরি করতে পারে। এই HTML public API item-গুলোর documentation comment-এর content প্রদর্শন করে, যা সেই সব programmer-দের জন্য যারা জানতে চায় তোমার crate কীভাবে _ব্যবহার_ করতে হয়, না কি তোমার crate কীভাবে _implement_ করা হয়েছে।

Documentation comment-এ দুটির বদলে তিনটি slash, `///`, ব্যবহার করা হয় এবং text format করার জন্য Markdown notation support করে। Documentation comment যেই item-টি নিয়ে লেখা হচ্ছে, তার ঠিক আগে রাখতে হয়। Listing 14-1 `my_crate` নামের একটি crate-এর `add_one` function-এর জন্য একটি documentation comment দেখাচ্ছে।

<Listing number="14-1" file-name="src/lib.rs" caption="A documentation comment for a function">

```rust,ignore
/// Adds one to the number given.
///
/// # Examples
///
/// ```
/// let arg = 5;
/// let answer = my_crate::add_one(arg);
///
/// assert_eq!(6, answer);
/// ```
pub fn add_one(x: i32) -> i32 {
    x + 1
}
```

</Listing>

এখানে আমরা `add_one` function যা করে তার একটি description দিয়েছি, `Examples` heading দিয়ে একটি section শুরু করেছি, এবং তারপর এমন code দিয়েছি যা `add_one` function কীভাবে ব্যবহার করতে হয় তা demonstrate করে। আমরা `cargo doc` run করে এই documentation comment থেকে HTML documentation তৈরি করতে পারি। এই command Rust-এর সাথে distributed `rustdoc` tool-টি run করে এবং তৈরি করা HTML documentation _target/doc_ directory-তে রাখে।

সুবিধার জন্য, `cargo doc --open` run করলে তোমার বর্তমান crate-এর documentation-এর (এবং তোমার crate-এর সব dependency-এর documentation-এর) জন্য HTML build করবে এবং ফলাফলটি একটি web browser-এ খুলবে। `add_one` function-এ যাও এবং তুমি দেখবে documentation comment-এর text কীভাবে render হয়েছে, যেমন Figure 14-1-এ দেখানো হয়েছে।

<img alt="Rendered HTML documentation for the `add_one` function of `my_crate`" src="img/trpl14-01.png" class="center" />

<span class="caption">Figure 14-1: The HTML documentation for the `add_one`
function</span>

#### সাধারণত ব্যবহৃত Section গুলো

Listing 14-1-এ আমরা `# Examples` Markdown heading ব্যবহার করেছি HTML-এ "Examples" শিরোনামের একটি section তৈরি করার জন্য। নিচে আরও কিছু section দেওয়া হলো যা crate author-রা সাধারণত তাদের documentation-এ ব্যবহার করে:

- **Panics**: এই পরিস্থিতিগুলো যেখানে document করা function-টি panic করতে পারে। Function call করা যারা তাদের program-এ panic চায় না, তাদের নিশ্চিত করা উচিত যে তারা এই পরিস্থিতিতে function-টি call করবে না।
- **Errors**: যদি function-টি একটি `Result` return করে, তাহলে কী ধরনের error ঘটতে পারে এবং কোন শর্তে সেই error-গুলো return হতে পারে তা বর্ণনা করা caller-দের জন্য সাহায্যকর, যাতে তারা বিভিন্ন ধরনের error আলাদাভাবে handle করার জন্য code লিখতে পারে।
- **Safety**: যদি function-টি call করা `unsafe` হয় (আমরা Chapter 20-এ unsafety নিয়ে আলোচনা করব), তাহলে এমন একটি section থাকা উচিত যা ব্যাখ্যা করে কেন function-টি unsafe এবং function-টি caller-দের থেকে কোন invariant গুলো uphold করা expect করে।

বেশিরভাগ documentation comment-এ এই সব section প্রয়োজন হয় না, কিন্তু এটি একটি ভালো checklist যা তোমাকে মনে করিয়ে দেবে তোমার code-এর কোন দিকগুলো সম্পর্কে user-রা জানতে আগ্রহী।

#### Documentation Comment কে Test হিসেবে ব্যবহার করা

তোমার documentation comment-এ example code block যোগ করলে তা তোমার library কীভাবে ব্যবহার করতে হয় তা demonstrate করতে সাহায্য করে, আর এর একটি অতিরিক্ত সুবিধা হলো: `cargo test` run করলে তোমার documentation-এর code example গুলো test হিসেবে run হবে! Example সহ documentation-এর চেয়ে ভালো আর কিছু নেই। কিন্তু example যদি কাজ না করে, তার চেয়ে খারাপ আর কিছু নেই, কারণ documentation লেখার পর থেকে code পরিবর্তন হয়েছে। আমরা যদি Listing 14-1 থেকে `add_one` function-এর documentation সহ `cargo test` run করি, আমরা test ফলাফলে এমন একটি section দেখব যা দেখতে এরকম:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-01/
cargo test
copy just the doc-tests section below
-->

```text
   Doc-tests my_crate

running 1 test
test src/lib.rs - add_one (line 5) ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.27s
```

এখন যদি আমরা function বা example-এ পরিবর্তন করি যাতে example-এর `assert_eq!` panic করে, এবং আবার `cargo test` run করি, আমরা দেখব doc test গুলো ধরে ফেলবে যে example এবং code একে অপরের সাথে sync-এ নেই!

<!-- Old headings. Do not remove or links may break. -->

<a id="commenting-contained-items"></a>

#### Contained Item-এর Comment

`//!` doc comment style-টি comment গুলোর *পরে* থাকা item-এর বদলে comment গুলো *ধারণ করে* এমন item-এ documentation যোগ করে। আমরা সাধারণত crate root file-এ (convention অনুযায়ী _src/lib.rs_) অথবা কোনো module-এর ভেতরে এই doc comment গুলো ব্যবহার করি পুরো crate বা module সম্পর্কে documentation দেওয়ার জন্য।

উদাহরণস্বরূপ, `add_one` function ধারণকারী `my_crate` crate-টির উদ্দেশ্য বর্ণনা করে এমন documentation যোগ করতে হলে, আমরা `//!` দিয়ে শুরু হওয়া documentation comment গুলো _src/lib.rs_ file-এর শুরুতে যোগ করি, যেমন Listing 14-2-তে দেখানো হয়েছে।

<Listing number="14-2" file-name="src/lib.rs" caption="The documentation for the `my_crate` crate as a whole">

```rust,ignore
//! # My Crate
//!
//! `my_crate` is a collection of utilities to make performing certain
//! calculations more convenient.

/// Adds one to the number given.
// --snip--
```

</Listing>

খেয়াল করো যে `//!` দিয়ে শুরু হওয়া শেষ লাইনের পর কোনো code নেই। যেহেতু আমরা comment গুলো `///`-এর বদলে `//!` দিয়ে শুরু করেছি, আমরা এই comment-টির পরে আসা কোনো item-এর বদলে এই comment-টি যে item-টি ধারণ করে তাকে document করছি। এই ক্ষেত্রে সেই item-টি হলো _src/lib.rs_ file, যা crate root। এই comment গুলো পুরো crate-টি বর্ণনা করে।

যখন আমরা `cargo doc --open` run করব, এই comment গুলো crate-এর public item-গুলোর তালিকার উপরে `my_crate`-এর documentation-এর front page-এ প্রদর্শিত হবে, যেমন Figure 14-2-তে দেখানো হয়েছে।

Item-এর ভেতরের documentation comment গুলো বিশেষ করে crate এবং module বর্ণনা করার জন্য কাজে লাগে। এগুলো ব্যবহার করে container-এর সামগ্রিক উদ্দেশ্য ব্যাখ্যা করো, যাতে তোমার user-রা crate-এর সংগঠন বুঝতে পারে।

<img alt="Rendered HTML documentation with a comment for the crate as a whole" src="img/trpl14-02.png" class="center" />

<span class="caption">Figure 14-2: The rendered documentation for `my_crate`,
including the comment describing the crate as a whole</span>

<!-- Old headings. Do not remove or links may break. -->

<a id="exporting-a-convenient-public-api-with-pub-use"></a>

### সুবিধাজনক Public API Export করা

একটি crate publish করার সময় তোমার public API-এর structure একটি বড় বিবেচ্য বিষয়। যারা তোমার crate ব্যবহার করবে তারা তোমার চেয়ে এই structure-এ কম পরিচিত, আর তোমার crate-এ যদি বড় module hierarchy থাকে তবে তারা তাদের প্রয়োজনীয় piece গুলো খুঁজে পেতে অসুবিধা হতে পারে।

Chapter 7-এ আমরা আলোচনা করেছি কীভাবে `pub` keyword ব্যবহার করে item গুলো public করতে হয়, এবং কীভাবে `use` keyword দিয়ে item গুলো scope-এ আনতে হয়। তবে যে structure তোমার কাছে crate develop করার সময় যুক্তিযুক্ত মনে হয়, তা তোমার user-দের জন্য খুব একটা সুবিধাজনক নাও হতে পারে। তুমি হয়তো তোমার struct গুলো এমন একটি hierarchy-তে organize করতে চাইবে যাতে একাধিক level আছে, কিন্তু তখন যারা hierarchy-এর গভীরে থাকা কোনো type ব্যবহার করতে চাইবে তারা সেই type-টি আসলে আছে কিনা তা জানতে অসুবিধা হবে। তাছাড়া `use my_crate::some_module::another_module::UsefulType;` এর বদলে `use my_crate::UsefulType;` লিখতে পারলে তারা বিরক্ত হবে না।

খবর ভালো এই যে, অন্য কোনো library থেকে ব্যবহার করার জন্য structure টি যদি সুবিধাজনক না হয়, তবে তোমাকে তোমার internal organization পুনরায় সাজাতে হবে না: এর বদলে তুমি `pub use` ব্যবহার করে item গুলো re-export করে এমন একটি public structure তৈরি করতে পারো যা তোমার private structure থেকে আলাদা। *Re-exporting* একটি public item কে একটি location থেকে নিয়ে অন্য location-এ public করে, যেন সেটি সেই অন্য location-এই define করা হয়েছে।

উদাহরণস্বরূপ, ধরো আমরা artistic concept model করার জন্য `art` নামের একটি library বানালাম। এই library-তে দুটি module আছে: `kinds` module, যাতে `PrimaryColor` এবং `SecondaryColor` নামের দুটি enum আছে, এবং `utils` module, যাতে `mix` নামের একটি function আছে, যেমন Listing 14-3-তে দেখানো হয়েছে।

<Listing number="14-3" file-name="src/lib.rs" caption="An `art` library with items organized into `kinds` and `utils` modules">

```rust,noplayground,test_harness
//! # Art
//!
//! A library for modeling artistic concepts.

pub mod kinds {
    /// The primary colors according to the RYB color model.
    pub enum PrimaryColor {
        Red,
        Yellow,
        Blue,
    }

    /// The secondary colors according to the RYB color model.
    pub enum SecondaryColor {
        Orange,
        Green,
        Purple,
    }
}

pub mod utils {
    use crate::kinds::*;

    /// Combines two primary colors in equal amounts to create
    /// a secondary color.
    pub fn mix(c1: PrimaryColor, c2: PrimaryColor) -> SecondaryColor {
        // --snip--
    }
}
```

</Listing>

Figure 14-3 দেখায় `cargo doc` দ্বারা তৈরি এই crate-এর documentation-এর front page দেখে কেমন হবে।

<img alt="Rendered documentation for the `art` crate that lists the `kinds` and `utils` modules" src="img/trpl14-03.png" class="center" />

<span class="caption">Figure 14-3: The front page of the documentation for `art`
that lists the `kinds` and `utils` modules</span>

খেয়াল করো যে `PrimaryColor` এবং `SecondaryColor` type গুলো front page-এ তালিকাভুক্ত নেই, `mix` function-টিও নয়। সেগুলো দেখতে হলে আমাদের `kinds` এবং `utils`-এ click করতে হবে।

এই library-র উপর নির্ভরশীল অন্য কোনো crate-কে `art` থেকে item গুলো scope-এ আনার জন্য এমন `use` statement লাগবে যা বর্তমানে define করা module structure উল্লেখ করবে। Listing 14-4 এমন একটি crate-এর উদাহরণ দেখায় যা `art` crate থেকে `PrimaryColor` এবং `mix` item ব্যবহার করে।

<Listing number="14-4" file-name="src/main.rs" caption="A crate using the `art` crate’s items with its internal structure exported">

```rust,ignore
use art::kinds::PrimaryColor;
use art::utils::mix;

fn main() {
    let red = PrimaryColor::Red;
    let yellow = PrimaryColor::Yellow;
    mix(red, yellow);
}
```

</Listing>

Listing 14-4-এর code-এর author, যিনি `art` crate ব্যবহার করেছেন, তাকে খুঁজে বের করতে হয়েছে যে `PrimaryColor` হলো `kinds` module-এ এবং `mix` হলো `utils` module-এ। `art` crate-এর module structure যারা `art` crate নিয়ে কাজ করছেন developer-দের কাছে বেশি প্রাসঙ্গিক, যারা এটি ব্যবহার করছেন তাদের চেয়ে। Internal structure এমন কেউ যিনি `art` crate কীভাবে ব্যবহার করতে হয় তা বুঝতে চান তার জন্য কোনো কার্যকর তথ্য ধারণ করে না, বরং confusion তৈরি করে কারণ যারা এটি ব্যবহার করেন তাদের খুঁজে বের করতে হয় কোথায় তাকা যাবে, এবং `use` statement-এ module name গুলো উল্লেখ করতে হয়।

Internal organization টি public API থেকে সরাতে, আমরা Listing 14-3-এর `art` crate code-কে modify করে `pub use` statement যোগ করতে পারি যাতে item গুলো top level-এ re-export হয়, যেমন Listing 14-5-তে দেখানো হয়েছে।

<Listing number="14-5" file-name="src/lib.rs" caption="Adding `pub use` statements to re-export items">

```rust,ignore
//! # Art
//!
//! A library for modeling artistic concepts.

pub use self::kinds::PrimaryColor;
pub use self::kinds::SecondaryColor;
pub use self::utils::mix;

pub mod kinds {
    // --snip--
}

pub mod utils {
    // --snip--
}
```

</Listing>

`cargo doc` এই crate-এর জন্য যে API documentation তৈরি করবে তা এখন front page-এ re-export গুলো তালিকাভুক্ত করবে এবং link করবে, যেমন Figure 14-4-তে দেখানো হয়েছে, যার ফলে `PrimaryColor` এবং `SecondaryColor` type এবং `mix` function খুঁজে পাওয়া সহজ হয়।

<img alt="Rendered documentation for the `art` crate with the re-exports on the front page" src="img/trpl14-04.png" class="center" />

<span class="caption">Figure 14-4: The front page of the documentation for `art`
that lists the re-exports</span>

`art` crate-এর user-রা এখনও Listing 14-3-এর internal structure দেখতে এবং ব্যবহার করতে পারে যেমন Listing 14-4-তে demonstrate করা হয়েছে, অথবা তারা Listing 14-5-এর অধিক সুবিধাজনক structure ব্যবহার করতে পারে, যেমন Listing 14-6-তে দেখানো হয়েছে।

<Listing number="14-6" file-name="src/main.rs" caption="A program using the re-exported items from the `art` crate">

```rust,ignore
use art::PrimaryColor;
use art::mix;

fn main() {
    // --snip--
}
```

</Listing>

যেখানে অনেক nested module আছে, সেখানে top level-এ `pub use` দিয়ে type গুলো re-export করলে crate ব্যবহার করা মানুষের অভিজ্ঞতায় বড় পার্থক্য আনতে পারে। `pub use` এর আরেকটি সাধারণ ব্যবহার হলো বর্তমান crate-এ একটি dependency-এর definition গুলো re-export করা, যাতে সেই crate-এর definition গুলো তোমার crate-এর public API-এর অংশ হয়ে যায়।

কার্যকর একটি public API structure তৈরি করা science এর চেয়ে art বেশি, এবং তুমি তোমার user-দের জন্য সবচেয়ে ভালো যে API কাজ করে তা খুঁজে বের করতে iterate করতে পারো। `pub use` বেছে নিলে তুমি crate-টি ভেতরে কীভাবে structure করবে তাতে flexibility পাবে এবং সেই internal structure টি তোমার user-দের সামনে যা উপস্থাপন করবে তা থেকে আলাদা রাখতে পারবে। তুমি যে crate গুলো install করেছ তার কিছু code দেখে বুঝতে পারো তাদের internal structure public API থেকে আলাদা কিনা।

### Crates.io Account তৈরি করা

কোনো crate publish করার আগে তোমাকে [crates.io](https://crates.io/)<!-- ignore -->-তে একটি account তৈরি করতে হবে এবং একটি API token নিতে হবে। সেটি করতে [crates.io](https://crates.io/)<!-- ignore -->-এর home page-এ যাও এবং একটি GitHub account দিয়ে log in করো। (বর্তমানে GitHub account থাকা একটি requirement, কিন্তু ভবিষ্যতে site-টি account তৈরির অন্য উপায়ও support করতে পারে।) একবার log in করার পর, [https://crates.io/me/](https://crates.io/me/)<!-- ignore -->-এ তোমার account settings দেখো এবং তোমার API key retrieve করো। তারপর, `cargo login` command টি run করো এবং যখন prompt করা হবে তখন তোমার API key paste করো, এভাবে:

```console
$ cargo login
abcdefghijklmnopqrstuvwxyz012345
```

এই command টি Cargo-কে তোমার API token জানাবে এবং সেটি _~/.cargo/credentials.toml_-এ locally store করবে। মনে রেখো যে এই token টি একটি secret: এটি অন্য কারও সাথে share করবে না। যদি কোনো কারণে কারও সাথে share করেই ফেলো, তবে সেটি revoke করে [crates.io](https://crates.io/)<!-- ignore -->-তে নতুন token generate করবে।

### নতুন Crate-এ Metadata যোগ করা

ধরো তোমার এমন একটি crate আছে যা তুমি publish করতে চাও। Publish করার আগে তোমাকে crate-টির _Cargo.toml_ file-এর `[package]` section-এ কিছু metadata যোগ করতে হবে।

তোমার crate-টির একটি unique নাম প্রয়োজন। Locally crate নিয়ে কাজ করার সময় তুমি crate-টির যা খুশি নাম রাখতে পারো। তবে [crates.io](https://crates.io/)<!-- ignore -->-তে crate-এর নাম first-come, first-served ভিত্তিতে allocate করা হয়। একবার কোনো crate-এর নাম নেওয়া হলে অন্য কেউ সেই নামে crate publish করতে পারবে না। কোনো crate publish করার চেষ্টা করার আগে তুমি যে নাম ব্যবহার করতে চাও তা খুঁজে দেখো। যদি নামটি ব্যবহৃত হয়ে থাকে, তবে তোমাকে অন্য নাম খুঁজতে হবে এবং publish করার জন্য নতুন নাম ব্যবহার করতে _Cargo.toml_ file-এর `[package]` section-এর অধীনে `name` field সম্পাদনা করতে হবে, এভাবে:

<span class="filename">Filename: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
```

তুমি যদি unique নামই বেছে থাকো, তবুও এই মুহূর্তে crate publish করতে `cargo publish` run করলে একটি warning এবং তারপর একটি error পাবে:

<!-- manual-regeneration
Create a new package with an unregistered name, making no further modifications
  to the generated package, so it is missing the description and license fields.
cargo publish
copy just the relevant lines below
-->

```console
$ cargo publish
    Updating crates.io index
warning: manifest has no description, license, license-file, documentation, homepage or repository.
See https://doc.rust-lang.org/cargo/reference/manifest.html#package-metadata for more info.
--snip--
error: failed to publish to registry at https://crates.io

Caused by:
  the remote server responded with an error (status 400 Bad Request): missing or empty metadata fields: description, license. Please see https://doc.rust-lang.org/cargo/reference/manifest.html for more information on configuring these fields
```

এটি error দেখাবে কারণ তুমি কিছু অত্যাবশ্যক তথ্য দিতে ভুলে গেছ: একটি description এবং license প্রয়োজন যাতে মানুষ জানতে পারে তোমার crate কী করে এবং কোন শর্তে তারা এটি ব্যবহার করতে পারে। _Cargo.toml_-এ এক বা দুটি বাক্যের একটি description যোগ করো, কারণ এটি search ফলাফলে তোমার crate-এর সাথে দেখাবে। `license` field-এর জন্য তোমাকে একটি _license identifier value_ দিতে হবে। [Linux Foundation-এর Software Package Data Exchange (SPDX)][spdx] এই value-এর জন্য তুমি যে identifier গুলো ব্যবহার করতে পারো তার তালিকা রয়েছে। উদাহরণস্বরূপ, তুমি যদি তোমার crate MIT License দিয়ে license করে থাকো তবে তা উল্লেখ করতে `MIT` identifier যোগ করো:

<span class="filename">Filename: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
license = "MIT"
```

তুমি যদি এমন কোনো license ব্যবহার করতে চাও যা SPDX-তে নেই, তবে সেই license-এর text একটি file-এ রাখতে হবে, সেই file-টি তোমার project-এ include করতে হবে, এবং তারপর `license` key-এর বদলে `license-file` ব্যবহার করে সেই file-টির নাম উল্লেখ করতে হবে।

কোন license তোমার project-এর জন্য উপযুক্ত সে বিষয়ে পরামর্শ এই book-এর scope-এর বাইরে। Rust community-র অনেকেই Rust-এর মতো করে `MIT OR Apache-2.0` দুটি license একসাথে ব্যবহার করে তাদের project license করেন। এই অনুশীলন দেখায় যে তুমি `OR` দিয়ে আলাদা করে একাধিক license identifier উল্লেখ করে তোমার project-এর জন্য একাধিক license রাখতে পারো।

Unique নাম, version, তোমার description এবং একটি license যোগ করার পর publish করার জন্য প্রস্তুত একটি project-এর _Cargo.toml_ file দেখতে এমন হতে পারে:

<span class="filename">Filename: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
version = "0.1.0"
edition = "2024"
description = "A fun game where you guess what number the computer has chosen."
license = "MIT OR Apache-2.0"

[dependencies]
```

[Cargo-র documentation](https://doc.rust-lang.org/cargo/)-এ অন্যান্য metadata বর্ণনা করা আছে যা তুমি specify করতে পারো, যাতে অন্যরা তোমার crate সহজে খুঁজে পেতে ও ব্যবহার করতে পারে।

### Crates.io-তে Publish করা

এখন যেহেতু তুমি account তৈরি করেছ, API token save করেছ, তোমার crate-এর জন্য নাম বেছেছ এবং প্রয়োজনীয় metadata specify করেছ, তুমি publish করার জন্য প্রস্তুত! একটি crate publish করলে একটি নির্দিষ্ট version [crates.io](https://crates.io/)<!-- ignore -->-তে upload হয় যাতে অন্যরা সেটি ব্যবহার করতে পারে।

সতর্ক থেকো, কারণ একটি publish _permanent_। সেই version কখনো overwrite করা যাবে না, এবং কিছু নির্দিষ্ট পরিস্থিতি ছাড়া code delete করা যাবে না। Crates.io-র একটি বড় লক্ষ্য হলো code-এর একটি permanent archive হিসেবে কাজ করা, যাতে [crates.io](https://crates.io/)<!-- ignore --> থেকে নেওয়া crate-এর উপর নির্ভরশীল সব project-এর build কাজ চালিয়ে যেতে পারে। version deletion অনুমোদন করলে সেই লক্ষ্য পূরণ অসম্ভব হয়ে পড়বে। তবে তুমি যে পরিমাণ crate version publish করতে পারবে তার কোনো সীমা নেই।

আবার `cargo publish` command টি run করো। এখন এটি success করবে:

<!-- manual-regeneration
go to some valid crate, publish a new version
cargo publish
copy just the relevant lines below
-->

```console
$ cargo publish
    Updating crates.io index
   Packaging guessing_game v0.1.0 (file:///projects/guessing_game)
    Packaged 6 files, 1.2KiB (895.0B compressed)
   Verifying guessing_game v0.1.0 (file:///projects/guessing_game)
   Compiling guessing_game v0.1.0
(file:///projects/guessing_game/target/package/guessing_game-0.1.0)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.19s
   Uploading guessing_game v0.1.0 (file:///projects/guessing_game)
    Uploaded guessing_game v0.1.0 to registry `crates-io`
note: waiting for `guessing_game v0.1.0` to be available at registry
`crates-io`.
You may press ctrl-c to skip waiting; the crate should be available shortly.
   Published guessing_game v0.1.0 at registry `crates-io`
```

অভিনন্দন! তুমি এখন Rust community-র সাথে তোমার code share করেছ, এবং যে কেউ সহজেই তোমার crate তাদের project-এর dependency হিসেবে যোগ করতে পারবে।

### বর্তমান Crate-এর একটি নতুন Version Publish করা

যখন তুমি তোমার crate-এ পরিবর্তন এনেছ এবং একটি নতুন version release করার জন্য প্রস্তুত, তখন তুমি তোমার _Cargo.toml_ file-এ উল্লেখিত `version` value পরিবর্তন করো এবং পুনরায় publish করো। [Semantic Versioning rule][semver] ব্যবহার করে ঠিক করো তুমি যে ধরনের পরিবর্তন করেছ তার ভিত্তিতে পরবর্তী version number কী হওয়া উচিত। তারপর, নতুন version upload করতে `cargo publish` run করো।

<!-- Old headings. Do not remove or links may break. -->

<a id="removing-versions-from-cratesio-with-cargo-yank"></a>
<a id="deprecating-versions-from-cratesio-with-cargo-yank"></a>

### Crates.io থেকে Version Deprecate করা

যদিও তুমি একটি crate-এর আগের version গুলো remove করতে পারো না, তবে ভবিষ্যতের কোনো project যেন সেগুলোকে নতুন dependency হিসেবে যোগ করতে না পারে তা তুমি prevent করতে পারো। এটি তখন কাজে লাগে যখন কোনো crate version কোনো কারণে broken থাকে। এমন পরিস্থিতিতে Cargo একটি crate version yank করার সুবিধা দেয়।

কোনো version _Yank_ করলে নতুন project যেন সেই version-এর উপর নির্ভর করতে না পারে তা prevent করা হয়, কিন্তু যে সব বিদ্যমান project এর উপর নির্ভর করে তারা চালিয়ে যেতে পারে। মূলত, একটি yank মানে হলো যাদের _Cargo.lock_ আছে তাদের সব project ভেঙে যাবে না, এবং ভবিষ্যতে generate হওয়া যেকোনো _Cargo.lock_ file এই yanked version ব্যবহার করবে না।

কোনো crate-এর কোনো version yank করতে, যে crate তুমি আগে publish করেছ তার directory তে `cargo yank` run করো এবং তুমি কোন version টি yank করতে চাও তা specify করো। উদাহরণস্বরূপ, যদি আমরা `guessing_game` নামের একটি crate version 1.0.1 publish করে থাকি এবং সেটিকে yank করতে চাই, তাহলে `guessing_game`-এর project directory-তে নিচের command টি run করব:

<!-- manual-regeneration:
cargo yank carol-test --version 2.1.0
cargo yank carol-test --version 2.1.0 --undo
-->

```console
$ cargo yank --vers 1.0.1
    Updating crates.io index
        Yank guessing_game@1.0.1
```

command-এ `--undo` যোগ করলে তুমি একটি yank undo করতে পারবে এবং আবার project গুলোকে একটি version-এর উপর নির্ভর করার অনুমতি দিতে পারবে:

```console
$ cargo yank --vers 1.0.1 --undo
    Updating crates.io index
      Unyank guessing_game@1.0.1
```

একটি yank কোনো code delete করে _না_। এটি যেমন accidentally upload হওয়া secret delete করতে পারে না। যদি সেটি ঘটে, তবে তোমাকে সেই secret গুলো তৎক্ষণাৎ reset করতে হবে।

[spdx]: https://spdx.org/licenses/
[semver]: https://semver.org/

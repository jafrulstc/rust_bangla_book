## Packages এবং Crates

module system-এর যে অংশগুলো আমরা আগে cover করব সেগুলো হলো packages এবং crates।

একটি _crate_ হলো এতটুকু code যতটুকু Rust compiler একসাথে বিবেচনা করে। তুমি `cargo`-র বদলে `rustc` চালালে এবং একটি মাত্র source code file pass করলে (যেমন আমরা Chapter 1-এর [“Rust Program Basics”][basics]<!-- ignore --> section-এ করেছিলাম), compiler ওই file-টিকেই একটি crate হিসেবে বিবেচনা করে। Crate-এর ভেতরে module থাকতে পারে, এবং সেই module-গুলো অন্য কোনো file-এও define করা থাকতে পারে যা crate-এর সাথে compile হয় — যেমনটা আমরা পরের section-গুলোতে দেখব।

একটি crate দুটি form-এর যেকোনো একটিতে আসতে পারে: binary crate অথবা library crate। _Binary crate_ হলো এমন প্রোগ্রাম যাকে তুমি executable-এ compile করতে পারো এবং run করতে পারো — যেমন একটি command line program বা একটি server। প্রতিটির একটি `main` নামে function থাকতেই হবে যা executable run করলে কী হবে তা define করে। আমরা এ পর্যন্ত যে crate-গুলো তৈরি করেছি সেগুলো সবই binary crate ছিল।

_Library crate_-এর কোনো `main` function নেই, এবং সেগুলো executable-এ compile হয় না। তার বদলে সেগুলো এমন functionality define করে যা একাধিক project-এর সাথে share করার উদ্দেশ্যে তৈরি। যেমন, [Chapter 2][rand]<!-- ignore -->-তে আমরা যে `rand` crate ব্যবহার করেছি সেটি random সংখ্যা তৈরি করার functionality দেয়। Rustacean-রা যখন “crate” বলে, বেশিরভাগ ক্ষেত্রে তারা library crate-ই বোঝায়, এবং সাধারণ programming concept “library”-র সাথে একই অর্থে “crate” শব্দটি ব্যবহার করে।

_crate root_ হলো সেই source file যেখান থেকে Rust compiler শুরু করে এবং যা তোমার crate-এর root module হিসেবে কাজ করে (module সম্পর্কে বিস্তারিত আমরা [“Control Scope and Privacy with Modules”][modules]<!-- ignore -->-তে জানাব)।

একটি _package_ হলো এক বা একাধিক crate-এর একটি bundle যা একসেট functionality প্রদান করে। একটি package-এ একটি _Cargo.toml_ file থাকে যা বর্ণনা করে কীভাবে সেই crate-গুলো build করতে হবে। আসলে Cargo নিজেই একটি package, যেটির ভেতরে সেই command line tool-টির binary crate আছে যা তুমি তোমার code build করতে ব্যবহার করছ। Cargo package-টির আরও একটি library crate আছে যার উপর সেই binary crate-টি depend করে। অন্যান্য project-ও সেই Cargo library crate-এর উপর depend করতে পারে এবং Cargo command line tool-এর মতো একই logic ব্যবহার করতে পারে।

একটি package-এ তোমার যত খুশি binary crate থাকতে পারে, কিন্তু সর্বোচ্চ একটি মাত্র library crate থাকতে পারে। একটি package-এ অন্তত একটি crate থাকতেই হবে — সেটা library হোক বা binary crate।

চলো দেখি আমরা একটি package তৈরি করলে কী হয়। প্রথমে আমরা `cargo new my-project` command-টি দিই:

```console
$ cargo new my-project
     Created binary (application) `my-project` package
$ ls my-project
Cargo.toml
src
$ ls my-project/src
main.rs
```

`cargo new my-project` চালানোর পর আমরা `ls` দিয়ে দেখি Cargo কী তৈরি করেছে। _my-project_ directory-তে একটি _Cargo.toml_ file আছে, যা আমাদের একটি package দেয়। এছাড়া একটি _src_ directory আছে যার ভেতরে _main.rs_ আছে। তোমার text editor-এ _Cargo.toml_ খুললে দেখবে সেখানে _src/main.rs_-এর কোনো উল্লেখ নেই। Cargo একটি convention অনুসরণ করে — _src/main.rs_ হলো এমন একটি binary crate-এর crate root যার নাম package-টির নামের সাথে একই। একইভাবে, Cargo জানে যদি package directory-তে _src/lib.rs_ থাকে, তবে package-টিতে একটি library crate আছে যার নাম package-টির নামের সাথে একই, এবং _src/lib.rs_ হলো সেই crate-এর crate root। Cargo এই crate root file-গুলোকে `rustc`-এ পাঠায় library বা binary build করার জন্য।

এখানে আমাদের এমন একটি package আছে যাতে শুধু _src/main.rs_ আছে, অর্থাৎ এতে শুধু একটি binary crate আছে যার নাম `my-project`। যদি কোনো package-এ _src/main.rs_ এবং _src/lib.rs_ দুটোই থাকে, তবে তাতে দুটি crate থাকে: একটি binary এবং একটি library — দুটোরই নাম package-টির নামের সাথে একই। একটি package-এ একাধিক binary crate থাকতে পারে — _src/bin_ directory-তে file রাখলেই হবে: প্রতিটি file একেকটি আলাদা binary crate হবে।

[basics]: ch01-02-hello-world.html#rust-program-basics
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number

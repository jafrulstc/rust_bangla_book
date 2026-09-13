## Release Profile দিয়ে Build Customize করা

Rust-এ _release profile_ হলো predefined, customizable profile যেগুলোর ভিন্ন ভিন্ন configuration আছে এবং যা একজন programmer-কে code compile করার বিভিন্ন option-এ বেশি নিয়ন্ত্রণ দেওয়ার সুযোগ করে দেয়। প্রতিটি profile অন্যগুলো থেকে স্বাধীনভাবে configure করা হয়।

Cargo-র দুটি main profile আছে: `dev` profile, যেটা Cargo তখন ব্যবহার করে যখন তুমি `cargo build` run করো, আর `release` profile, যেটা Cargo তখন ব্যবহার করে যখন তুমি `cargo build --release` run করো। `dev` profile development-এর জন্য ভালো default নিয়ে define করা, আর `release` profile-এ release build-এর জন্য ভালো default আছে।

এই profile-গুলোর নাম মনে হতে পারে তোমার build-এর output থেকে পরিচিত:

<!-- manual-regeneration
anywhere, run:
cargo build
cargo build --release
and ensure output below is accurate
-->

```console
$ cargo build
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
$ cargo build --release
    Finished `release` profile [optimized] target(s) in 0.32s
```

এই `dev` এবং `release` হলো compiler দ্বারা ব্যবহৃত ভিন্ন ভিন্ন profile।

প্রতিটি profile-এর জন্য Cargo-র কিছু default setting থাকে, যেগুলো তখন apply হয় যখন তুমি project-এর _Cargo.toml_ file-এ স্পষ্টভাবে কোনো `[profile.*]` section যোগ করোনি। যেকোনো profile-এর জন্য `[profile.*]` section যোগ করলে তুমি সেই profile-এর default setting-এর যেকোনো অংশ override করতে পারো। উদাহরণস্বরূপ, `dev` এবং `release` profile-এর জন্য `opt-level` setting-এর default value নিচে দেওয়া হলো:

<span class="filename">Filename: Cargo.toml</span>

```toml
[profile.dev]
opt-level = 0

[profile.release]
opt-level = 3
```

`opt-level` setting নিয়ন্ত্রণ করে Rust তোমার code-এ কতগুলো optimization apply করবে, যার range 0 থেকে 3। বেশি optimization apply করলে compile-এ সময় বাড়ে, তাই development চলাকালীন যখন তুমি প্রায়ই code compile করো, তখন তোমার কম optimization চাইবে যাতে দ্রুত compile হয়, এমনকি যদি ফলাফলস্বরূপ code ধীরে চলেও। তাই `dev` profile-এর জন্য default `opt-level` `0`। যখন তুমার code release করার সময় আসবে, তখন compile-এ বেশি সময় ব্যয় করাটা ভালো। তুমি release mode-এ একবারই compile করবে, কিন্তু সেই compile হওয়া program অনেকবার run করবে, তাই release mode বেশি compile time-এর বিনিময়ে দ্রুত চলা code প্রদান করে। এ কারণেই `release` profile-এর জন্য default `opt-level` `3`।

তুমি একটি default setting _Cargo.toml_-এ ভিন্ন value যোগ করে override করতে পারো। উদাহরণস্বরূপ, যদি আমরা development profile-এ optimization level 1 ব্যবহার করতে চাই, তাহলে আমরা আমাদের project-এর _Cargo.toml_ file-এ এই দুটি লাইন যোগ করতে পারি:

<span class="filename">Filename: Cargo.toml</span>

```toml
[profile.dev]
opt-level = 1
```

এই code `0` default setting টি override করে। এখন যখন আমরা `cargo build` run করব, Cargo `dev` profile-এর default গুলোর সাথে আমাদের `opt-level` customization ব্যবহার করবে। যেহেতু আমরা `opt-level` করেছি `1`, Cargo default-এর চেয়ে বেশি optimization apply করবে, কিন্তু release build-এর মতো এত বেশি নয়।

প্রতিটি profile-এর সম্পূর্ণ configuration option ও default-এর তালিকার জন্য [Cargo-র documentation](https://doc.rust-lang.org/cargo/reference/profiles.html) দেখো।

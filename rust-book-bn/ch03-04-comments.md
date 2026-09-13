## Comments

সব programmer-ই তাদের code সহজে বোঝার মতো করে লেখার চেষ্টা করেন, কিন্তু মাঝে মাঝে কিছু বাড়তি ব্যাখ্যা দরকার হয়। এসব ক্ষেত্রে, programmer-রা তাদের source code-এ _comment_ রেখে দেন যা compiler উপেক্ষা করবে কিন্তু source code পড়া মানুষের কাজে লাগতে পারে।

এখানে একটি সহজ comment দেওয়া হলো:

```rust
// hello, world
```

Rust-এ idiomatic comment style হলো দুটি slash দিয়ে comment শুরু করা, এবং comment টি ওই line-এর শেষ পর্যন্ত চলে। একাধিক line-এর বেশি বিস্তৃত comment-এর জন্য তোমার প্রতিটি line-এ `//` রাখতে হবে, এভাবে:

```rust
// So we're doing something complicated here, long enough that we need
// multiple lines of comments to do it! Whew! Hopefully, this comment will
// explain what's going on.
```

Comment গুলো code ধারণ করা line-এর শেষেও বসানো যেতে পারে:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let lucky_number = 7; // I'm feeling lucky today
}
```

কিন্তু তুমি সাধারণত এগুলোকে এই ফর্ম্যাটে দেখবে, যেখানে comment টি যে code-টি annotate করছে তার উপরে একটি আলাদা line-এ থাকে:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    // I'm feeling lucky today
    let lucky_number = 7;
}
```

Rust-এ আরেক ধরনের comment আছে, documentation comment, যা নিয়ে আমরা Chapter 14-এর [“Publishing a Crate to Crates.io”][publishing]<!-- ignore --> section-এ আলোচনা করব।

[publishing]: ch14-02-publishing-to-crates-io.html

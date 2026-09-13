<!-- Old headings. Do not remove or links may break. -->

<a id="installing-binaries-from-cratesio-with-cargo-install"></a>

## `cargo install` দিয়ে Binary Install করা

`cargo install` command তোমাকে locally binary crate install করে ব্যবহার করতে দেয়। এটি system package replace করার জন্য নয়; এটি Rust developer-দের জন্য একটি সুবিধাজনক উপায় যাতে তারা [crates.io](https://crates.io/)<!-- ignore -->-এ অন্যরা share করা tool install করতে পারে। খেয়াল রাখো যে তুমি শুধুমাত্র এমন package install করতে পারবে যাদের binary target আছে। একটি _binary target_ হলো সেই runnable program যা তৈরি হয় যদি crate-এ একটি _src/main.rs_ file থাকে বা অন্য কোনো file binary হিসেবে specify করা থাকে, যার বিপরীতে library target যা নিজে থেকে runnable নয় কিন্তু অন্যান্য program-এ include করার জন্য উপযুক্ত। সাধারণত crate গুলোর README file-এ তথ্য থাকে যে একটি crate library, নাকি binary target আছে, নাকি দুটোই।

`cargo install` দিয়ে install করা সব binary installation root-এর _bin_ folder-এ store করা হয়। তুমি যদি _rustup.rs_ ব্যবহার করে Rust install করে থাকো এবং কোনো custom configuration না থাকে, তবে এই directory টি হবে *$HOME/.cargo/bin*। নিশ্চিত করো যে এই directory টি তোমার `$PATH`-এ আছে, যাতে তুমি `cargo install` দিয়ে install করা program গুলো run করতে পারো।

উদাহরণস্বরূপ, Chapter 12-তে আমরা উল্লেখ করেছিলাম যে file search করার জন্য `grep` tool-এর একটি Rust implementation আছে যার নাম `ripgrep`। `ripgrep` install করতে, আমরা নিচের command টি run করতে পারি:

<!-- manual-regeneration
cargo install something you don't have, copy relevant output below
-->

```console
$ cargo install ripgrep
    Updating crates.io index
  Downloaded ripgrep v14.1.1
  Downloaded 1 crate (213.6 KB) in 0.40s
  Installing ripgrep v14.1.1
--snip--
   Compiling grep v0.3.2
    Finished `release` profile [optimized + debuginfo] target(s) in 6.73s
  Installing ~/.cargo/bin/rg
   Installed package `ripgrep v14.1.1` (executable `rg`)
```

output-এর শেষ থেকে দ্বিতীয় লাইনটি দেখায় install করা binary-টির location এবং নাম, যা `ripgrep`-এর ক্ষেত্রে `rg`। যতক্ষণ আগেই বলা হয়েছে তেমন installation directory টি তোমার `$PATH`-এ আছে, তুমি তখন `rg --help` run করতে পারবে এবং file search করার জন্য একটি দ্রুত, Rustier tool ব্যবহার শুরু করতে পারবে!

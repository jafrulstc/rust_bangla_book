## Appendix D: Useful Development Tools

এই appendix-এ আমরা Rust project-এর দেওয়া কিছু useful development tool নিয়ে আলোচনা করব। আমরা automatic formatting, warning fix করার দ্রুত উপায়, একটি linter এবং IDE-র সাথে integration দেখব।

### `rustfmt` দিয়ে Automatic Formatting

`rustfmt` tool তোমার code কে community code style অনুযায়ী পুনরায় format করে। অনেক collaborative project `rustfmt` ব্যবহার করে, যাতে Rust লেখার সময় কোন style ব্যবহার করব সে নিয়ে বিতর্ক না হয়: সবাই এই tool ব্যবহার করে নিজেদের code format করে।

Rust installation-এ ডিফল্টভাবেই `rustfmt` অন্তর্ভুক্ত থাকে, তাই তোমার সিস্টেমে `rustfmt` ও `cargo-fmt` program দুটি ইতিমধ্যেই থাকা উচিত। এই দুটি command `rustc` ও `cargo`-র মতোই, কারণ `rustfmt` আরও fine-grained control দেয় এবং `cargo-fmt` Cargo ব্যবহার করে এমন project-এর convention বোঝে। যেকোনো Cargo project format করতে নিচের command দাও:

```console
$ cargo fmt
```

এই command চালালে বর্তমান crate-এর সব Rust code পুনরায় format হয়। এটি শুধু code style পরিবর্তন করবে, code-এর semantics পরিবর্তন করবে না। `rustfmt` সম্পর্কে আরও তথ্যের জন্য [এর documentation][rustfmt] দেখো।

### `rustfix` দিয়ে Code Fix করা

`rustfix` tool Rust installation-এ অন্তর্ভুক্ত থাকে এবং এটি স্বয়ংক্রিয়ভাবে এমন compiler warning fix করতে পারে যেগুলোর সমস্যা সমাধানের স্পষ্ট উপায় আছে এবং যেটা সম্ভবত তুমি চাও। তুমি আগেই compiler warning দেখেছ। উদাহরণস্বরূপ, এই code-টি বিবেচনা করো:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let mut x = 42;
    println!("{x}");
}
```

এখানে আমরা variable `x`-কে mutable হিসেবে define করেছি, কিন্তু আসলে কখনো এটিকে mutate করি না। Rust আমাদের সে সম্পর্কে সতর্ক করে:

```console
$ cargo build
   Compiling myprogram v0.1.0 (file:///projects/myprogram)
warning: variable does not need to be mutable
 --> src/main.rs:2:9
  |
2 |     let mut x = 0;
  |         ----^
  |         |
  |         help: remove this `mut`
  |
  = note: `#[warn(unused_mut)]` on by default
```

warning-এ suggest করা হয়েছে আমরা `mut` keyword সরিয়ে দিই। `cargo fix` command চালিয়ে আমরা `rustfix` tool ব্যবহার করে সেই suggestion স্বয়ংক্রিয়ভাবে apply করতে পারি:

```console
$ cargo fix
    Checking myprogram v0.1.0 (file:///projects/myprogram)
      Fixing src/main.rs (1 fix)
    Finished dev [unoptimized + debuginfo] target(s) in 0.59s
```

আমরা যখন _src/main.rs_ আবার দেখব, তখন দেখব `cargo fix` code পরিবর্তন করে দিয়েছে:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    let x = 42;
    println!("{x}");
}
```

এখন variable `x` immutable, এবং warning আর দেখা যাচ্ছে না।

তুমি `cargo fix` command ব্যবহার করে তোমার code কে এক Rust edition থেকে অন্য edition-এ স্থানান্তর করতেও পারো। Edition সম্পর্কে আলোচনা করা হয়েছে [Appendix E][editions]<!--
ignore -->-তে।

### Clippy দিয়ে আরও Lint

Clippy tool হলো কিছু lint-এর সংগ্রহ, যা তোমার code analyze করে যাতে তুমি সাধারণ ভুল ধরতে পারো এবং তোমার Rust code উন্নত করতে পারো। Clippy স্ট্যান্ডার্ড Rust installation-এ অন্তর্ভুক্ত থাকে।

যেকোনো Cargo project-এ Clippy-র lint চালাতে নিচের command দাও:

```console
$ cargo clippy
```

উদাহরণস্বরূপ, ধরো তুমি এমন একটি program লিখছ যা pi-র মতো একটি mathematical constant-এর approximate value ব্যবহার করে, যেমনটা নিচের program করে:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = 3.1415;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

এই project-এ `cargo clippy` চালালে এই error পাওয়া যাবে:

```text
error: approximate value of `f{32, 64}::consts::PI` found
 --> src/main.rs:2:13
  |
2 |     let x = 3.1415;
  |             ^^^^^^
  |
  = note: `#[deny(clippy::approx_constant)]` on by default
  = help: consider using the constant directly
  = help: for further information visit https://rust-lang.github.io/rust-clippy/master/index.html#approx_constant
```

এই error তোমাকে জানায় যে Rust-এ ইতিমধ্যেই একটি আরও নিখুঁত `PI` constant define করা আছে, এবং তুমি সেই constant ব্যবহার করলে তোমার program আরও সঠিক হবে। তারপর তুমি তোমার code পরিবর্তন করে `PI` constant ব্যবহার করবে।

নিচের code-এ কোনো error বা warning আসে না Clippy থেকে:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = std::f64::consts::PI;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

Clippy সম্পর্কে আরও তথ্যের জন্য [এর documentation][clippy] দেখো।

### `rust-analyzer` ব্যবহার করে IDE Integration

IDE integration-এ সাহায্য করতে Rust community [`rust-analyzer`][rust-analyzer]<!-- ignore --> ব্যবহার করার সুপারিশ করে। এই tool হলো compiler-centric utility-র একটি সেট যা [Language Server Protocol][lsp]<!-- ignore --> বলে কথা বলে—যা IDE এবং programming language-র মধ্যে যোগাযোগের একটি specification। বিভিন্ন client `rust-analyzer` ব্যবহার করতে পারে, যেমন [the Rust analyzer plug-in for Visual Studio Code][vscode]।

Installation instruction-এর জন্য `rust-analyzer` project-এর [home page][rust-analyzer]<!-- ignore --> দেখো, তারপর তোমার নির্দিষ্ট IDE-তে language server support install করো। তোমার IDE autocompletion, jump to definition এবং inline error-এর মতো ক্ষমতা পাবে।

[rustfmt]: https://github.com/rust-lang/rustfmt
[editions]: appendix-05-editions.md
[clippy]: https://github.com/rust-lang/rust-clippy
[rust-analyzer]: https://rust-analyzer.github.io
[lsp]: http://langserver.org/
[vscode]: https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer

## Hello, Cargo!

Cargo হলো Rust-এর build system এবং package manager। বেশিরভাগ Rustacean-ই তাদের Rust project manage করতে এই tool ব্যবহার করেন, কারণ Cargo অনেক কাজ তোমার হয়ে করে দেয় — যেমন তোমার code build করা, তোমার code যেসব library-এর উপর নির্ভর করে সেগুলো download করা, এবং সেই library-গুলো build করা। (তোমার code যেসব library প্রয়োজন সেগুলোকে আমরা _dependency_ বলি।)

যেসব Rust program সবচেয়ে সহজ, যেমন আমরা এ পর্যন্ত যেটা লিখলাম, সেগুলোর কোনো dependency নেই। আমরা যদি "Hello, world!" project-টা Cargo দিয়ে build করতাম, তাহলে Cargo-এর শুধু সেই অংশটাই ব্যবহার হতো যেটা তোমার code build করে। তুমি যত জটিল Rust program লিখবে, তত dependency যোগ করবে, আর Cargo দিয়ে শুরু করা project-এ dependency যোগ করা অনেক সহজ হয়ে যায়।

যেহেতু Rust project-গুলোর বিশাল সংখ্যাগরিষ্ঠ অংশ Cargo ব্যবহার করে, এই book-ের বাকি অংশে ধরে নেওয়া হবে তুমিও Cargo ব্যবহার করছো। ["Installation"][installation]<!-- ignore --> section-এ আলোচিত official installer ব্যবহার করলে Cargo একসাথে Rust-এর সাথে install হয়ে যায়। তুমি যদি অন্য কোনো উপায়ে Rust install করে থাকো, তাহলে নিচের command দিয়ে যাচাই করো Cargo install আছে কিনা:

```console
$ cargo --version
```

Version number দেখতে পেলে তোমার কাছে আছে! `command not found`-এর মতো কোনো error দেখলে তোমার install করার পদ্ধতির documentation দেখে বের করো কীভাবে আলাদাভাবে Cargo install করতে হয়।

### Cargo দিয়ে Project তৈরি করা

Cargo দিয়ে একটা নতুন project বানাই এবং দেখি আমাদের আগের "Hello, world!" project থেকে সেটা কীভাবে আলাদা। তোমার _projects_ directory-তে ফিরে যাও (বা যেখানে তুমি code রাখার সিদ্ধান্ত নিয়েছো)। তারপর যেকোনো operating system-ে নিচের command চালাও:

```console
$ cargo new hello_cargo
$ cd hello_cargo
```

প্রথম command-টা _hello_cargo_ নামে একটা নতুন directory এবং project বানায়। আমরা আমাদের project-এর নাম দিয়েছি _hello_cargo_, আর Cargo একই নামের একটা directory-তে তার file তৈরি করে।

_hello_cargo_ directory-তে যাও এবং file-গুলো list করো। দেখবে আমাদের জন্য Cargo দুটো file এবং একটা directory বানিয়েছে: একটা _Cargo.toml_ file এবং ভেতরে _main.rs_ file সহ একটা _src_ directory।

এটা সাথে সাথে একটা _.gitignore_ file সহ একটা নতুন Git repository-ও initialize করে। তুমি কোনো existing Git repository-র ভেতরে `cargo new` চালালে Git file তৈরি হবে না; `cargo new --vcs=git` ব্যবহার করে এই behavior override করতে পারো।

> নোট: Git একটা common version control system। `--vcs` flag ব্যবহার করে তুমি `cargo new`-কে অন্য কোনো version control system বা একেবারে কোনো version control ছাড়াই কাজ করতে বলতে পারো। Available option দেখতে `cargo new --help` চালাও।

তোমার পছন্দের text editor-এ _Cargo.toml_ খোলো। এটা Listing 1-2-এর code-এর মতো দেখানোর কথা।

<Listing number="1-2" file-name="Cargo.toml" caption="`cargo new` দিয়ে তৈরি *Cargo.toml*-এর content">

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

</Listing>

এই file [_TOML_][toml]<!-- ignore --> (_Tom's Obvious, Minimal Language_) format-এ আছে, যেটা Cargo-এর configuration format।

প্রথম line `[package]` একটা section heading যেটা বোঝায় পরের statement-গুলো একটা package configure করছে। এই file-এ আমরা যত তথ্য যোগ করবো, তত নতুন section যোগ করবো।

পরের তিনটি line Cargo-এর তোমার program compile করার জন্য দরকারি configuration তথ্য সেট করে: নাম, version, এবং কোন Rust edition ব্যবহার করতে হবে। `edition` key নিয়ে আমরা [Appendix E][appendix-e]<!-- ignore -->-তে আলোচনা করবো।

শেষ line `[dependencies]` একটা section-এর শুরু, যেখানে তোমার project-এর যেকোনো dependency list করবে। Rust-এ code-এর package-কে _crate_ বলা হয়। এই project-ের জন্য আমাদের আর কোনো crate লাগবে না, কিন্তু Chapter 2-এর প্রথম project-এ লাগবে, তখন এই dependencies section ব্যবহার করবো।

এখন _src/main.rs_ খোলো এবং দেখো:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    println!("Hello, world!");
}
```

Cargo তোমার জন্য একটা "Hello, world!" program বানিয়ে দিয়েছে, ঠিক যেমনটা আমরা Listing 1-1-এ লিখেছিলাম! এ পর্যন্ত আমাদের project আর Cargo-এর বানানো project-ের মধ্যে পার্থক্য হলো — Cargo code-টা _src_ directory-তে রেখেছে, এবং সবার উপরের directory-তে একটা _Cargo.toml_ configuration file আছে।

Cargo চায় তোমার source file-গুলো _src_ directory-র ভেতরে থাকুক। Top-level project directory শুধু README file, license তথ্য, configuration file, এবং তোমার code-এর সাথে সরাসরি সম্পর্কহীন অন্যান্য জিনিসের জন্য। Cargo ব্যবহার করলে তোমার project organized থাকে। সবকিছুর একটা জায়গা থাকে, আর সবকিছু তার জায়গায় থাকে।

তুমি যদি এমন কোনো project শুরু করে থাকো যেটাতে Cargo ব্যবহার হয়নি — যেমন আমরা "Hello, world!" project-টা করেছিলাম — সেটাকে Cargo ব্যবহার করে এমন project-এ convert করতে পারো। Project code _src_ directory-তে move করো এবং একটা মানানসই _Cargo.toml_ file বানাও। সেই _Cargo.toml_ file পাওয়ার একটা সহজ উপায় হলো `cargo init` চালানো, যেটা তোমার জন্য সেটা অটোমেটিক বানিয়ে দেবে।

### Cargo Project Build এবং Run করা

এখন দেখি Cargo দিয়ে "Hello, world!" program build এবং run করলে কী আলাদা হয়! তোমার _hello_cargo_ directory থেকে নিচের command দিয়ে project build করো:

```console
$ cargo build
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 2.85 secs
```

এই command বর্তমান directory-র বদলে _target/debug/hello_cargo_-এ (বা Windows-এ _target\debug\hello_cargo.exe_-এ) একটা executable file তৈরি করে। যেহেতু default build একটা debug build, Cargo binary-টা _debug_ নামের একটা directory-তে রাখে। এই command দিয়ে executable run করতে পারো:

```console
$ ./target/debug/hello_cargo # or .\target\debug\hello_cargo.exe on Windows
Hello, world!
```

সব ঠিক থাকলে terminal-এ `Hello, world!` print হওয়ার কথা। প্রথমবার `cargo build` চালালে Cargo top level-এ আরেকটা নতুন file তৈরি করে: _Cargo.lock_। এই file তোমার project-এর dependency-গুলোর সঠিক version track রাখে। এই project-ের কোনো dependency নেই, তাই file-টা বেশ ফাঁকা। তোমাকে কখনো নিজে এই file change করতে হবে না; Cargo এর content তোমার হয়ে manage করে।

আমরা এইমাত্র `cargo build` দিয়ে একটা project build করলাম এবং `./target/debug/hello_cargo` দিয়ে run করলাম, কিন্তু `cargo run` ব্যবহার করলে একই command-এ code compile করে তারপর সেই executable run করা যায়:

```console
$ cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

`cargo build` মনে রাখা এবং তারপর সম্পূর্ণ binary path ব্যবহার করার চেয়ে `cargo run` ব্যবহার করা অনেক সুবিধাজনক, তাই বেশিরভাগ developer `cargo run` ব্যবহার করেন।

খেয়াল করো এবার আমরা Cargo-এর `hello_cargo` compile করার কোনো output দেখতে পাইনি। Cargo বুঝতে পেরেছে file change হয়নি, তাই সেটা আবার build করেনি, শুধু binary-টা run করেছে। তুমি যদি তোমার source code modify করে থাকো, তাহলে Cargo run করার আগে project-টা rebuild করতো, আর তুমি নিচের output দেখতে পেতে:

```console
$ cargo run
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.33 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

Cargo-ের `cargo check` নামে আরেকটা command আছে। এই command দ্রুত যাচাই করে যে তোমার code compile হয় কিনা, কিন্তু কোনো executable তৈরি করে না:

```console
$ cargo check
   Checking hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.32 secs
```

কেন তুমি executable চাইবে না? প্রায়ই `cargo check` `cargo build`-এর চেয়ে অনেক দ্রুত, কারণ এটা executable তৈরি করার step skip করে। তুমি যদি code লেখার সময় ক্রমাগত তোমার কাজ check করো, তাহলে `cargo check` দ্রুত জানিয়ে দেবে তোমার project এখনও compile হচ্ছে কিনা! তাই অনেক Rustacean লেখার সময় program compile হয় কিনা নিশ্চিত করতে মাঝে মাঝে `cargo check` চালান। তারপর executable ব্যবহার করতে চাইলে `cargo build` চালান।

চলো Cargo সম্পর্কে এ পর্যন্ত যা শিখলাম সেটা একবার রিভিউ করি:

- `cargo new` দিয়ে আমরা একটা project তৈরি করতে পারি।
- `cargo build` দিয়ে আমরা একটা project build করতে পারি।
- `cargo run` দিয়ে আমরা এক ধাপে project build এবং run করতে পারি।
- `cargo check` দিয়ে আমরা binary তৈরি না করেই error আছে কিনা check করতে পারি।
- আমাদের code-এর একই directory-তে build result save করার বদলে Cargo সেটা _target/debug_ directory-তে রাখে।

Cargo ব্যবহারের আরেকটা সুবিধা হলো — তুমি যেই operating system-এ কাজ করো না কেন command-গুলো একই। তাই এখন থেকে আমরা Linux/macOS এবং Windows-ের জন্য আলাদা instruction দেবো না।

### Release-এর জন্য Build করা

তোমার project যখন অবশেষে release-এর জন্য প্রস্তুত, তখন `cargo build --release` চালিয়ে সেটা optimization সহ compile করতে পারো। এই command _target/debug_-এর বদলে _target/release_-এ executable তৈরি করে। Optimization তোমার Rust code দ্রুত চালায়, কিন্তু সেগুলো চালু করলে তোমার program compile হতে যে সময় লাগে সেটা বেড়ে যায়। এই জন্যই দুটো আলাদা profile আছে: একটা development-এর জন্য, যখন তুমি দ্রুত এবং বারবার rebuild করতে চাও, আরেকটা final program-ের জন্য যেটা তুমি user-কে দেবে এবং যেটা বারবার rebuild হবে না এবং যত দ্রুত সম্ভব চলবে। তুমি যদি তোমার code-এর running time benchmark করো, তাহলে অবশ্যই `cargo build --release` চালিয়ে _target/release_-এর executable দিয়ে benchmark করবে।

<!-- Old headings. Do not remove or links may break. -->
<a id="cargo-as-convention"></a>

### Cargo-এর Convention কাজে লাগানো

সহজ project-গুলোতে শুধু `rustc` ব্যবহারের চেয়ে Cargo বিশেষ কিছু বাড়তি সুবিধা দেয় না, কিন্তু তোমার program যত জটিল হবে এর মূল্য বুঝতে পারবে। একবার program multiple file-ে ছড়িয়ে গেলে বা dependency দরকার হলে, build coordinate করা Cargo-কে দিয়ে দেওয়া অনেক সহজ।

`hello_cargo` project-টা যত সহজই হোক না কেন, এখন এটা তোমার Rust career-ের বাকি অংশে যেসব real tool ব্যবহার করবে তার অনেকটাই ব্যবহার করছে। আসলে কোনো existing project-এ কাজ করতে তুমি নিচের command-গুলো ব্যবহার করতে পারো — Git দিয়ে code checkout করতে, সেই project-ের directory-তে যেতে এবং build করতে:

```console
$ git clone example.org/someproject
$ cd someproject
$ cargo build
```

Cargo নিয়ে আরও তথ্যের জন্য [its documentation][cargo] দেখো।

## Summary

তোমার Rust যাত্রা দারুণ শুরু হয়েছে! এই chapter-ে তুমি শিখেছ কীভাবে:

- `rustup` ব্যবহার করে Rust-এর সবচেয়ে নতুন stable version install করতে হয়।
- নতুন একটা Rust version-এ update করতে হয়।
- Locally install করা documentation খুলতে হয়।
- সরাসরি `rustc` ব্যবহার করে একটা "Hello, world!" program লিখতে ও run করতে হয়।
- Cargo-ের convention ব্যবহার করে নতুন একটা project তৈরি এবং run করতে হয়।

এখন একটু বড়সড় একটা program বানিয়ে ফেলার একদম ঠিক সময়, যাতে Rust code পড়তে এবং লিখতে অভ্যস্ত হও। তাই Chapter 2-তে আমরা একটা guessing game program বানাবো। তুমি যদি আগে common programming concept-গুলো Rust-এ কীভাবে কাজ করে সেটা শিখতে চাও, তাহলে Chapter 3 দেখো এবং তারপর আবার Chapter 2-তে ফিরে এসো।

[installation]: ch01-01-installation.html#installation
[toml]: https://toml.io
[appendix-e]: appendix-05-editions.html
[cargo]: https://doc.rust-lang.org/cargo/

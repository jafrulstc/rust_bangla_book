<!-- Anchor preserved for cross-references from other chapters. -->
<a id="installation"></a>

## ইনস্টল করা

প্রথম step হলো Rust install করা। আমরা `rustup` এর মাধ্যমে Rust download করবো, যেটা Rust-এর বিভিন্ন version এবং সম্পর্কিত tool manage করার একটা command line tool। এই download করার জন্য তোমার internet connection লাগবে।

> নোট: কোনো কারণে যদি তুমি `rustup` ব্যবহার না করতে চাও, তাহলে আরও অপশনের জন্য [Other Rust Installation Methods page][otherinstall] দেখো।

নিচের step-গুলো অনুসরণ করলে Rust compiler-এর সবচেয়ে নতুন stable version install হবে। Rust-এর stability guarantee নিশ্চিত করে যে এই book-এর সব example যেগুলো compile হয়, সেগুলো নতুন Rust version-এও compile হতে থাকবে। Version-ভেদে output সামান্য আলাদা হতে পারে, কারণ Rust প্রায়ই error message এবং warning উন্নত করে। অর্থাৎ, এই step-গুলো দিয়ে তুমি যেকোনো নতুন stable version install করলে এই book-এর content-এর সাথে সেটা ঠিকমতো কাজ করবে।

> ### Command Line Notation
>
> এই chapter এবং পুরো book জুড়ে আমরা কিছু command দেখাবো যেগুলো terminal-এ ব্যবহার করা হয়। যেসব line তোমাকে terminal-এ লিখতে হবে সেগুলোর শুরুতে `$` থাকে। তোমাকে `$` character টাইপ করতে হবে না; এটা command line prompt, যেটা দিয়ে বোঝানো হয় যে command-এর শুরু এখানে। যেসব line `$` দিয়ে শুরু হয় না সেগুলো সাধারণত আগের command-এর output দেখায়। আর PowerShell-specific example-এ `$` এর বদলে `>` ব্যবহার করা হবে।

### Linux বা macOS-এ `rustup` install করা

তুমি যদি Linux বা macOS ব্যবহার করো, তাহলে একটা terminal খোলো এবং নিচের command লেখো:

```console
$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
```

এই command-টা একটা script download করে এবং `rustup` tool install শুরু করে, যেটা Rust-এর সবচেয়ে নতুন stable version install করে। তোমার password চাওয়া হতে পারে। install সফল হলে নিচের line দেখতে পাবে:

```text
Rust is installed now. Great!
```

তোমার একটা _linker_ ও লাগবে — এমন একটা program যেটা Rust-এর compiled output-গুলোকে একটা file-এ যুক্ত করে। সম্ভবত তোমার কাছে আগে থেকেই একটা আছে। যদি linker error পাও, তাহলে একটা C compiler install করতে হবে, যেটার সাথে সাধারণত একটা linker থাকে। C compiler আরও কাজে লাগে, কারণ কিছু common Rust package C code-এর উপর নির্ভর করে এবং সেগুলোর জন্য C compiler দরকার হয়।

macOS-এ নিচের command চালিয়ে তুমি একটা C compiler পেতে পারো:

```console
$ xcode-select --install
```

Linux user-দের সাধারণত তাদের distribution-এর documentation অনুযায়ী GCC বা Clang install করা উচিত। যেমন, তুমি যদি Ubuntu ব্যবহার করো, তাহলে `build-essential` package install করতে পারো।

### Windows-এ `rustup` install করা

Windows-এ [https://www.rust-lang.org/tools/install][install]<!-- ignore
--> page-এ যাও এবং Rust install করার instruction অনুসরণ করো। install-এর কোনো এক পর্যায়ে তোমাকে Visual Studio install করতে বলা হবে। এটা একটা linker এবং program compile করার জন্য দরকারি native library দেয়। এই step-এ আরও সাহায্য দরকার হলে [https://rust-lang.github.io/rustup/installation/windows-msvc.html][msvc]<!-- ignore --> দেখো।

এই book-এর বাকি অংশে এমন command ব্যবহার করা হয়েছে যেগুলো _cmd.exe_ এবং PowerShell — দুই জায়গাতেই কাজ করে। কোনো specific পার্থক্য থাকলে আমরা বুঝিয়ে দেবো কোনটা ব্যবহার করতে হবে।

<!-- Anchor preserved for cross-references from other chapters. -->
<a id="troubleshooting"></a>

### সমস্যা সমাধান (Troubleshooting)

Rust ঠিকমতো install হয়েছে কিনা যাচাই করতে একটা shell খোলো এবং নিচের line লেখো:

```console
$ rustc --version
```

তোমার সবচেয়ে নতুন stable version-এর version number, commit hash এবং commit date নিচের format-এ দেখতে পাওয়ার কথা:

```text
rustc x.y.z (abcabcabc yyyy-mm-dd)
```

এই তথ্য দেখতে পেলে বুঝবে Rust সফলভাবে install হয়েছে! না দেখলে যাচাই করো যে Rust তোমার `%PATH%` system variable-এ আছে কিনা, নিচের মতো করে।

Windows CMD-তে ব্যবহার করো:

```console
> echo %PATH%
```

PowerShell-এ ব্যবহার করো:

```powershell
> echo $env:Path
```

Linux এবং macOS-ে ব্যবহার করো:

```console
$ echo $PATH
```

সব ঠিক থাকলেও যদি Rust কাজ না করে, তাহলে এমন অনেক জায়গা আছে যেখান থেকে সাহায্য নিতে পারো। অন্য Rustacean-দের (হ্যাঁ, আমরা নিজেদের এই মজার nickname-এ ডাকি!) সাথে যোগাযোগ করার উপায় [the community page][community]-এ খুঁজে নাও।

### Update এবং Uninstall করা

`rustup` দিয়ে Rust install করা হলে নতুন version-এ update করা খুব সহজ। তোমার shell থেকে নিচের update script-টা চালাও:

```console
$ rustup update
```

Rust এবং `rustup` uninstall করতে তোমার shell থেকে নিচের uninstall script-টা চালাও:

```console
$ rustup self uninstall
```

<!-- Old headings. Do not remove or links may break. -->
<a id="local-documentation"></a>

### Local Documentation পড়া

Rust install করার সময় একসাথে documentation-এর একটা local copy-ও install হয়, যাতে তুমি offline-এ পড়তে পারো। Browser-এ local documentation খুলতে `rustup doc` চালাও।

কোনো type বা function standard library থেকে এসেছে কিন্তু তুমি জানো না সেটা কী করে বা কীভাবে ব্যবহার করতে হয় — তখন application programming interface (API) documentation দেখে জেনে নাও!

<!-- Old headings. Do not remove or links may break. -->
<a id="text-editors-and-integrated-development-environments"></a>

### Text Editor এবং IDE ব্যবহার করা

এই book ধরে নেয় না তুমি Rust code লেখার জন্য কোন tool ব্যবহার করছো। যেকোনো text editor-ই কাজ চালিয়ে নিতে পারবে! তবে অনেক text editor এবং integrated development environment (IDE)-এ Rust-এর জন্য built-in support থাকে। Rust website-এর [the tools page][tools]-এ তুমি বেশ কিছু editor এবং IDE-এর একটা বেশ আপডেট-থাকা list পাবে।

### এই Book Offline-এ কাজ করা

কয়েকটা example-এ আমরা standard library-এর বাইরের কিছু Rust package ব্যবহার করবো। সেই example-গুলো নিজে ট্রাই করতে হলে তোমার হয় internet connection লাগবে, নয়তো আগেই সেই dependency-গুলো download করে রাখতে হবে। আগেই dependency download করতে নিচের command-গুলো চালাও। (`cargo` কী এবং এই command-গুলো কী করে সেটা পরে বিস্তারিত বুঝিয়ে দেবো।)

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
* ch14-03-cargo-workspaces.md
-->

```console
$ cargo new get-dependencies
$ cd get-dependencies
$ cargo add rand@0.10.1 trpl@0.2.0
```

এতে এই package-গুলোর download cache হয়ে যাবে, ফলে পরে আর download করতে হবে না। এই command একবার চালানোর পর তোমার `get-dependencies` folder আর রাখার দরকার নেই। এই command চালালে এই book-এর বাকি অংশের সব `cargo` command-এ তুমি `--offline` flag ব্যবহার করতে পারবে, যাতে network ব্যবহার না করে cache করা version-গুলো ব্যবহার হয়।

[otherinstall]: https://forge.rust-lang.org/infra/other-installation-methods.html
[install]: https://www.rust-lang.org/tools/install
[msvc]: https://rust-lang.github.io/rustup/installation/windows-msvc.html
[community]: https://www.rust-lang.org/community
[tools]: https://www.rust-lang.org/tools

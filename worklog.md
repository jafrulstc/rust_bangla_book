# Rust Book Bangla Translation — Work Log

এই file-এ প্রতিটা translation agent নিজের work record append করবে।
Coordinator (main agent) এখান থেকে progress track করবে।

## Project Info
- Source: `/home/z/my-project/rust-book-source/src/` (১১২টা .md file)
- Output: `/home/z/my-project/rust-book-bn/`
- Guide: `/home/z/my-project/rust-book-bn/_TRANSLATION_GUIDE.md`
- Execution: Parallel (waves)
- Total Tasks: 23

## Task Map
| Task ID | Chapter | Model | Status |
|---------|---------|-------|--------|
| 1 | Front matter (title, foreword, SUMMARY, intro) | sonnet | pending |
| 2 | Ch01 Getting Started | sonnet | pending |
| 3 | Ch02 Guessing Game | opus | pending |
| 4 | Ch03 Common Concepts | sonnet | pending |
| 5 | Ch04 Ownership | opus | pending |
| 6 | Ch05 Structs | sonnet | pending |
| 7 | Ch06 Enums | sonnet | pending |
| 8 | Ch07 Modules | sonnet | pending |
| 9 | Ch08 Collections | sonnet | pending |
| 10 | Ch09 Error Handling | sonnet | pending |
| 11 | Ch10 Generics/Traits/Lifetimes | opus | pending |
| 12 | Ch11 Testing | sonnet | pending |
| 13 | Ch12 I/O Project | sonnet | pending |
| 14 | Ch13 Closures/Iterators | sonnet | pending |
| 15 | Ch14 Cargo | sonnet | pending |
| 16 | Ch15 Smart Pointers | opus | pending |
| 17 | Ch16 Concurrency | sonnet | pending |
| 18 | Ch17 Async/Await | opus | pending |
| 19 | Ch18 OOP | sonnet | pending |
| 20 | Ch19 Patterns | sonnet | pending |
| 21 | Ch20 Advanced Features | opus | pending |
| 22 | Ch21 Web Server | sonnet | pending |
| 23 | Appendices | sonnet | pending |

---
Task ID: 1
Agent: general-purpose (sonnet)
Task: Front matter (title-page, foreword, SUMMARY, ch00-introduction) অনুবাদ

Work Log:
- worklog.md read করলাম — প্রথম task, আগে কেউ কাজ করেনি।
- _TRANSLATION_GUIDE.md read করে নিয়মাবলী (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive অপরিবর্তিত, দাঁড়ি ব্যবহার) মেনে নিলাম।
- ৪টি source file read করলাম: title-page.md, foreword.md, SUMMARY.md, ch00-00-introduction.md।
- title-page.md — চলিত ভাষায় অনুবাদ; book title "The Rust Programming Language", লেখকের নাম, `edition = "2024"`, `rustup doc --book` ইত্যাদি অপরিবর্তিত রাখলাম; mdBook `<!-- ignore -->` directive preserve করলাম; community translations blockquote-এর ইমোজি/link অপরিবর্তিত।
- foreword.md — Bec Rumbul-এর লেখা; reader-কে "তোমাকে" হিসেবে address করলাম; ownership/memory safety/compiler/community/Rust Foundation ইত্যাদি technical term English-এ রাখলাম।
- SUMMARY.md — সব chapter title text translate করলাম; link URL ও filename সম্পূর্ণ অপরিবর্তিত; heading-এ থাকা code/keyword (`match`, `if let`, `let...else`, `panic!`, `Result`, `cargo install`, `Send`, `Sync`, `Box<T>`, `Rc<T>`, `RefCell<T>`, `Drop`, `use`) English-এ রাখলাম।
- ch00-00-introduction.md — Note blockquote, সব heading, সব paragraph অনুবাদ; `<span id="ferris"></span>` anchor ও Ferris table-এর `<img>` tag ও image path অপরিবর্তিত; table-এর Meaning cell গুলো Bangla-য়; `[nsprust]`, `[nsp]`, `[book]` link reference অপরিবর্তিত।

Stage Summary:
- Files translated: title-page.md, foreword.md, SUMMARY.md, ch00-00-introduction.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: Book title "The Rust Programming Language" proper noun হিসেবে English-এ রাখা হয়েছে। Ferris table-এর image src ও alt attribute অপরিবর্তিত, শুধু table-এর "Meaning" column text Bangla-য়। SUMMARY-এ "Programming a Guessing Game" → "একটি Guessing Game প্রোগ্রাম করা" রাখা হয়েছে (পরের chapter translation-এ এই শিরোনামের সাথে consistency রাখতে হবে)।

---
Task ID: 4
Agent: general-purpose (sonnet)
Task: Chapter 3 (Common Programming Concepts) অনুবাদ

Work Log:
- worklog.md read করলাম — Task 1 (Front matter) আগেই complete হয়েছে।
- _TRANSLATION_GUIDE.md read করে সব নিয়ম (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive ও Markdown structure preserve, দাঁড়ি ব্যবহার) মেনে নিলাম।
- ৬টি source file read করলাম: ch03-00, ch03-01 (variables/mutability), ch03-02 (data-types), ch03-03 (functions), ch03-04 (comments), ch03-05 (control-flow)।
- ch03-00-common-programming-concepts.md — chapter intro ও Keywords blockquote অনুবাদ; keyword, variable, function ইত্যাদি term English-এ; `[appendix_a]` link reference অপরিবর্তিত।
- ch03-01-variables-and-mutability.md — mutability/immutable/shadowing/scope/mut ইত্যাদি term English-এ রেখে বর্ণনা চলিত ভাষায়; সব `{{#rustdoc_include}}` ও `{{#include}}` directive, `<span class="filename">`, `<a id="constants">` anchor, code block (rust/console) অপরিবর্তিত; `THREE_HOURS_IN_SECONDS`, `mut`, `let`, `const` সব keyword English-এ।
- ch03-02-data-types.md — scalar/compound/tuple/array/expression ইত্যাদি technical term English-এ; Table 3-1 ও Table 3-2 সম্পূর্ণ preserve (code cell অপরিবর্তিত); Integer Overflow blockquote-তে panic/wrapping/checked_*/overflowing_*/saturating_* ইত্যাদি term English-এ; `<sup>` tag অপরিবর্তিত; link reference সব অপরিবর্তিত। একটি ছোট broken markdown link ঠিক করলাম।
- ch03-03-how-functions-work.md — parameter/argument/statement/expression/snake case ইত্যাদি term English-এ; `<Listing>` directive অপরিবর্তিত; সব code block ও output include directive অপরিবর্তিত; `mismatched types`, `()` unit type ইত্যাদি English-এ।
- ch03-04-comments.md — comment/documentation comment term English-এ; নমুনা comment code block-এর ভেতরের text (// So we're doing something...) অপরিবর্তিত রাখা হয়েছে কারণ এটি code block; `[publishing]` link reference অপরিবর্তিত।
- ch03-05-control-flow.md — `if`/`else`/`else if`/`loop`/`while`/`for`/`break`/`continue`/`match`/`return` সব keyword English-এ; arm/loop label/Range/rev ইত্যাদি term English-ে; ৩টি `<Listing>` directive ও `<kbd>ctrl</kbd>-<kbd>C</kbd>` tag, manual-regeneration comment block, `<a id="...">` anchor সব preserve; final Summary section অনুবাদ।

Stage Summary:
- Files translated: ch03-00-common-programming-concepts.md, ch03-01-variables-and-mutability.md, ch03-02-data-types.md, ch03-03-how-functions-work.md, ch03-04-comments.md, ch03-05-control-flow.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: সব mdBook directive (`{{#rustdoc_include}}`, `{{#include}}`, `<Listing>`, `<span class="filename">`, `<span class="caption">`, manual-regeneration comment block) অপরিবর্তিত রাখা হয়েছে। ch03-02-data-types.md-তে একটি accidental broken markdown link ছিল যেটা fix করেছি (`[`if` expression কীভাবে কাজ করে] Rust-এ সেটা` → স্বাভাবিক বাক্যে)। Chapter title গুলো heading-এ English-এ রাখা হয়েছে guide-এর নিয়ম অনুযায়ী (যেমন "## Variables এবং Mutability", "## Data Types", "## Functions", "## Comments", "## Control Flow")। Integer Overflow blockquote-তে "panic" শব্দটি technical term হিসেবে English-এ রাখা হয়েছে।


---
Task ID: 2
Agent: general-purpose (sonnet)
Task: Chapter 1 (Getting Started) অনুবাদ

Work Log:
- worklog.md read করলাম — Task 1 (Front matter) এবং Task 4 (Ch03) আগেই complete হয়েছে।
- _TRANSLATION_GUIDE.md read করে সব নিয়ম (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive ও Markdown structure preserve, দাঁড়ি ব্যবহার, inline code ও code block অপরিবর্তিত) মেনে নিলাম।
- ৪টি source file read করলাম: ch01-00-getting-started.md, ch01-01-installation.md, ch01-02-hello-world.md, ch01-03-hello-cargo.md।
- ch01-00-getting-started.md — chapter intro অনুবাদ; heading `# Getting Started` → `# শুরু করা`; bullet point-এ `cargo`, `Hello, world!` ইত্যাদি English-এ।
- ch01-01-installation.md — Installation/Troubleshooting/Command Line Notation ইত্যাদি section অনুবাদ; সব code block (console/text/powershell/cmd) ও ভেতরের output অপরিবর্তিত; `rustup`, `rustc`, `cargo`, `%PATH%`, `$env:Path`, `$PATH` ইত্যাদি English-এ; OS-specific instruction (Linux/macOS/Windows) অনুবাদ কিন্তু command ও path অপরিবর্তিত; "Rustacean" nickname-টি English-এ রাখলাম; existing `<a id="local-documentation">`, `<a id="text-editors-and-integrated-development-environments">` ইত্যাদি anchor preserve; HTML comment `<!-- Old headings... -->` ও `<!-- ignore -->` directive অপরিবর্তিত; `[otherinstall]`, `[install]`, `[msvc]`, `[community]`, `[tools]` link reference অপরিবর্তিত।
- ch01-02-hello-world.md — "Hello, World!" program-এর anatomy, compilation ও execution section অনুবাদ; `<Listing number="1-1" ...>` directive অপরিবর্তিত (শুধু caption text translate করা হয়েছে); rust code block সম্পূর্ণ অপরিবর্তিত; `fn main`, `println!`, `rustc`, `rustfmt` ইত্যাদি English-এ; `gcc`/`clang`/`.rb`/`.py`/`.js` extension অপরিবর্তিত; existing anchor (`creating-a-project-directory`, `writing-and-running-a-rust-program`, `anatomy-of-a-rust-program`, `compiling-and-running-are-separate-steps`) সব preserve; `[troubleshooting]`, `[devtools]`, `[ch20-macros]` link reference অপরিবর্তিত।
- ch01-03-hello-cargo.md — Cargo পরিচিতি, project তৈরি, build/run, `cargo check`, release build ও Summary section অনুবাদ; `<Listing number="1-2" ...>` directive ও ভেতরের TOML code block সম্পূর্ণ অপরিবর্তিত; `<span class="filename">Filename: src/main.rs</span>` অপরিবর্তিত; `cargo new`/`cargo build`/`cargo run`/`cargo check`/`cargo init`/`--vcs`/`--offline`/`--release` সব command ও flag English-এ; Cargo.toml/Cargo.lock/target/debug/target/release/src/main.rs সব path অপরিবর্তিত; `[installation]`, `[toml]`, `[appendix-e]`, `[cargo]` link reference অপরিবর্তিত।

Stage Summary:
- Files translated: ch01-00-getting-started.md, ch01-01-installation.md, ch01-02-hello-world.md, ch01-03-hello-cargo.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: দুটি নতুন explicit anchor যোগ করা হয়েছে যাতে অন্য chapter থেকে cross-reference (`ch01-01-installation.html#installation` ও `#troubleshooting`) অটুট থাকে: `## ইনস্টল করা` heading-এর আগে `<a id="installation"></a>` এবং `### সমস্যা সমাধান (Troubleshooting)` heading-এর আগে `<a id="troubleshooting"></a>` (কারণ Bangla heading text থেকে auto-generated anchor ASCII হয় না)। `## Hello, World!`, `## Hello, Cargo!`, এবং `## Summary` heading-গুলো English-এ রাখা হয়েছে কারণ এগুলো canonical program name বা conventional section label। `### Command Line Notation` ও `### Reading the Local Documentation` ইত্যাদি technical-convention heading-এ mixed English+Bangla ব্যবহার করা হয়েছে। Operating-system-specific instruction অনুবাদ করা হয়েছে কিন্তু সব command, path ও output অপরিবর্তিত। Listing caption text-গুলো Bangla-য় অনুবাদ করা হয়েছে (কিন্তু ভেতরের inline code English-এ)।

---
Task ID: 3
Agent: general-purpose (opus)
Task: Chapter 2 (Guessing Game Tutorial) অনুবাদ

Work Log:
- worklog.md ও _TRANSLATION_GUIDE.md read করা হয়েছে।
- source file ch02-00-guessing-game-tutorial.md (952 lines) সম্পূর্ণ read করা হয়েছে।
- সম্পূর্ণ chapter চলিত ভাষায় অনুবাদ করা হয়েছে — tutorial tone, দাঁড়ি ব্যবহার।
- সব code block (rust, toml, console), inline code, mdBook include directive (`{{#...}}`), HTML comment (manual-regeneration, Old headings), Listing tag, span.filename, anchor `<a id="...">`, kbd tag ও reference link definition অপরিবর্তিত রাখা হয়েছে।
- Technical terms (prelude, shadowing, ownership, reference, match, enum, variant, Result, expect, crate, etc.) English-এ রাখা হয়েছে।
- Heading text Bangla-তে অনুবাদ করা হয়েছে, কিন্তু heading-এ থাকা code/keyword (`Result`, `println!`) English-এ রাখা হয়েছে।
- Listing caption ও blockquote `> Note:` syntax preserve করা হয়েছে।
- Structure verification: 18 headings, 36 code blocks (72 fences), 21 include directives, 6 Listing tags, 6 filename spans, 3 anchor tags, 19 reference link defs, 33 `<!--` occurrences — সব source-এর সাথে match করে।

Stage Summary:
- Files translated: ch02-00-guessing-game-tutorial.md
- Output path: /home/z/my-project/rust-book-bn/ch02-00-guessing-game-tutorial.md
- Output line count: 626 (source: 952; line count কম কারণ Bangla text-এ word wrapping ঘন, কিন্তু content সম্পূর্ণ)
- Notes: কোনো special issue নেই। সব structural element source-এর সাথে exact match করে। Listing caption গুলো English-এ রাখা হয়েছে যাতে rendered output-এ কোনো formatting issue না হয়।

---
Task ID: 15
Agent: general-purpose (sonnet)
Task: Chapter 14 (More about Cargo and Crates.io) অনুবাদ

Work Log:
- worklog.md read করলাম — Task 1 (Front matter), Task 4 (Ch03), Task 2 (Ch01), Task 3 (Ch02) আগেই complete হয়েছে।
- _TRANSLATION_GUIDE.md read করে সব নিয়ম (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive ও Markdown structure preserve, দাঁড়ি ব্যবহার) মেনে নিলাম।
- ৬টি source file read করলাম preprocessed source থেকে: ch14-00 (intro), ch14-01 (release profiles), ch14-02 (publishing to crates.io), ch14-03 (workspaces), ch14-04 (installing binaries), ch14-05 (extending cargo)।
- ch14-00-more-about-cargo.md — chapter intro অনুবাদ; cargo, crates.io, release profile, workspace, dependency ইত্যাদি technical term English-এ; `<!-- ignore -->` directive ও link অপরিবর্তিত।
- ch14-01-release-profiles.md — release profile, dev profile, opt-level, Cargo.toml ইত্যাদি term English-এ; সব code block (console/toml), manual-regeneration HTML comment, `<span class="filename">` সম্পূর্ণ অপরিবর্তিত।
- ch14-02-publishing-to-crates-io.md — documentation comment, public API, pub use, re-export, registry, API token, publish, Semantic Versioning, yank ইত্যাদি term English-এ; সব `<Listing>` directive, code block (rust,ignore / rust,noplayground,test_harness / console / toml / text), `<span class="filename">` ও `<span class="caption">`, `<img>` tag, `<a id="...">` anchor, `<!-- Old headings. Do not remove or links may break. -->` comment, manual-regeneration comment, `[spdx]` ও `[semver]` link reference সব অপরিবর্তিত; Listing caption English-এ রাখা হয়েছে (Task 3 এর convention অনুসরণ করে)।
- ch14-03-cargo-workspaces.md — workspace, package, crate, binary crate, library crate, dependency, path dependency, resolver, target directory ইত্যাদি term English-এ; সব console/text/toml/rust code block অপরিবর্তিত; directory tree text block অপরিবর্তিত; `<Listing>`, manual-regeneration comment, `<!-- When updating the version of rand... -->` comment, `<!-- Old headings -->` comment, `<a id="...">` anchor সব preserve।
- ch14-04-installing-binaries.md — `cargo install`, binary crate, binary target, library target, `$PATH`, `$HOME/.cargo/bin`, ripgrep/rg ইত্যাদি English-এ; `<!-- Old headings -->` comment, `<a id="...">` anchor, manual-regeneration comment, console code block অপরিবর্তিত।
- ch14-05-extending-cargo.md — cargo subcommand, custom command, `cargo install`, `cargo --list`, `$PATH` ইত্যাদি English-এ; সব link ও `<!-- ignore -->` directive অপরিবর্তিত; Summary section অনুবাদ।

Stage Summary:
- Files translated: ch14-00-more-about-cargo.md, ch14-01-release-profiles.md, ch14-02-publishing-to-crates-io.md, ch14-03-cargo-workspaces.md, ch14-04-installing-binaries.md, ch14-05-extending-cargo.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: সব code block (rust, toml, console, text), inline code, mdBook directive (`<Listing>`, `<span class="filename">`, `<span class="caption">`, `<img>`, `<a id="...">`), HTML comment (manual-regeneration, Old headings, version-sync reminder) ও reference link definition অপরিবর্তিত রাখা হয়েছে। Listing caption গুলো Task 3 (Ch02) convention অনুসরণ করে English-এ রাখা হয়েছে rendered output-এ formatting issue এড়াতে। Cargo command ও flag সব English-এ (cargo build/run/test/doc/publish/yank/login/install, --release, --vers, --undo, -p, --lib, etc.)। `cargo yank`, `cargo login`, `cargo doc --open`, `cargo install`, `cargo new --lib` সব command অপরিবর্তিত। কোনো special issue নেই।

---
Task ID: 7
Agent: general-purpose (sonnet)
Task: Chapter 6 (Enums and Pattern Matching) অনুবাদ

Work Log:
- worklog.md read করলাম — Task 1 (Front matter), Task 4 (Ch03), Task 2 (Ch01), Task 3 (Ch02) আগেই complete হয়েছে।
- _TRANSLATION_GUIDE.md read করে সব নিয়ম (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive ও Markdown structure preserve, দাঁড়ি ব্যবহার, inline code ও code block অপরিবর্তিত) মেনে নিলাম।
- ৪টি source file read করলাম preprocessed source থেকে: ch06-00-enums.md, ch06-01-defining-an-enum.md, ch06-02-match.md, ch06-03-if-let.md।
- ch06-00-enums.md — chapter intro অনুবাদ; enumerations/_enums_/variant/`Option`/`match`/`if let` ইত্যাদি technical term English-এ।
- ch06-01-defining-an-enum.md — IP address (IpAddrKind/IpAddr/V4/V6) example, `Message` enum, `Option<T>` enum ও null vs Option-এর discussion চলিত ভাষায় অনুবাদ; সব rust code block, console output, `<Listing number="6-1"...>` ও `6-2` directive অপরিবর্তিত; Tony Hoare-র "billion-dollar mistake" quote সম্পূর্ণ অপরিবর্তিত (English-এ রাখা হয়েছে কারণ এটি একটি historical quote); `<!-- Old headings. Do not remove or links may break. -->` comment ও `<a id="the-option-enum-and-its-advantages-over-null-values"></a>` anchor preserve; `[IpAddr]`, `[option]`, `[docs]` link reference অপরিবর্তিত; struct/enum/variant/field/impl/method/scope/prelude/generic type parameter ইত্যাদি term English-এ।
- ch06-02-match.md — `match` construct, Coin enum example (Penny/Nickel/Dime/Quarter), Patterns That Bind to Values section, `Option<T>` match pattern, Matches Are Exhaustive ও Catch-All Patterns (`_` placeholder) section অনুবাদ; সব rust code block (rust,ignore ও does_not_compile), console error output (`error[E0277]`/`error[E0004]`), `<Listing number="6-3"...>` থেকে `6-5` পর্যন্ত directive অপরিবর্তিত; `<!-- Old headings... -->` ও `<a id="the-match-control-flow-operator">`/`<a id="matching-with-optiont">` anchor preserve; `[ch19-00-patterns]`, `[tuples]` link reference অপরিবর্তিত; arm/pattern/wildcard/exhaustive/literal value ইত্যাদি term English-এ।
- ch06-03-if-let.md — `if let`/`let...else` syntax, `else` clause, Listing 6-6 থেকে 6-9 পর্যন্ত সব example অনুবাদ; সব rust code block ও `<Listing number="6-6"...>` থেকে `6-9` directive অপরিবর্তিত; "syntax sugar"/"boilerplate code"/"happy path" ইত্যাদি term English-এ; final Summary section অনুবাদ; module-এর দিকে transition sentence অনুবাদ।

Stage Summary:
- Files translated: ch06-00-enums.md, ch06-01-defining-an-enum.md, ch06-02-match.md, ch06-03-if-let.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: সব mdBook directive (`<Listing number="6-N" caption="...">`, `<!-- ignore -->`, `<!-- Old headings. Do not remove or links may break. -->`, `<a id="...">` anchor) সম্পূর্ণ অপরিবর্তিত রাখা হয়েছে। Listing caption গুলো Bangla-য় অনুবাদ করা হয়েছে কিন্তু ভেতরের inline code (`struct`/`match`/`Option<i32>` ইত্যাদি) English-এ। Tony Hoare-র "billion-dollar mistake" quote সম্পূর্ণ English-এ অপরিবর্তিত রাখা হয়েছে কারণ এটি একটি historical/canonical quote এবং অনুবাদ করলে মূল অর্থ নষ্ট হতে পারতো। Heading গুলো Bangla-য় কিন্তু heading-এ থাকা code/keyword (`match`, `Option<T>`, `if let`, `let...else`) English-এ। চলিত ভাষা ও দাঁড়ি ব্যবহার করা হয়েছে। কোনো special issue নেই।

---
Task ID: 9
Agent: general-purpose (sonnet)
Task: Chapter 8 (Common Collections) অনুবাদ

Work Log:
- worklog.md read করলাম — Task 1, 2, 3, 4 আগেই complete হয়েছে।
- _TRANSLATION_GUIDE.md read করে সব নিয়ম (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive ও Markdown structure preserve, দাঁড়ি ব্যবহার) মেনে নিলাম।
- ৪টি source file read করলাম (preprocessed source থেকে): ch08-00-common-collections.md, ch08-01-vectors.md, ch08-02-strings.md, ch08-03-hash-maps.md।
- ch08-00-common-collections.md — chapter intro অনুবাদ; collection, vector, string, hash map, map, heap ইত্যাদি term English-এ; bullet list-এর _vector_, _string_, _hash map_, `String` সব preserve; `[collections]` link reference অপরিবর্তিত।
- ch08-01-vectors.md — `Vec<T>`, vector, generics, `mut`, `push`, `get`, indexing, `Option<&T>`, `match`, `Some`, `None`, panic, borrow checker, ownership, borrowing, immutable/mutable reference, dereference operator, enum, variant, trait object, `struct`, drop ইত্যাদি term English-এ; সব `<Listing>` directive, code block (rust, console), `<span class="filename">`, `<!-- ignore -->`, HTML comment, reference link definition অপরিবর্তিত; Listing caption গুলো Bangla-য়। একটি stray character ঢুকে গিয়েছিল (heading-এ) সেটা fix করলাম।
- ch08-02-strings.md — `String`, `&str`, `str`, string slice, string literal, `Vec<u8>`, `to_string`, `String::from`, `Display` trait, `push_str`, `push`, `+` operator, `add` method, `format!`, deref coercion, `chars`, `bytes`, UTF-8, Unicode scalar value, grapheme cluster, `char`, `&` reference, `&mut`, `&[T]`, indexing, string slice ইত্যাদি term English-এ; সব `<Listing>` directive, code block (rust, rust,ignore, console, text), `<a id="...">` anchor (what-is-a-string, appending-to-a-string-with-push_str-and-push, concatenation-with-the--operator-or-the-format-macro, bytes-and-scalar-values-and-grapheme-clusters-oh-my, methods-for-iterating-over-strings, strings-are-not-so-simple), `<!-- Old headings. Do not remove or links may break. -->` comment সব preserve; সব code block অপরিবর্তিত; crates.io link ও reference অপরিবর্তিত।
- ch08-03-hash-maps.md — `HashMap<K, V>`, hashing function, hash, map, object, hash table, dictionary, associative array, `new`, `insert`, `get`, `Option<&V>`, `copied`, `unwrap_or`, `Copy` trait, ownership, lifetime, `entry`, `Entry`, `or_insert`, `&mut V`, `split_whitespace`, `BuildHasher` trait, hasher, SipHash, DoS attack ইত্যাদি term English-এ; সব `<Listing>` directive, code block, `<a id="...">` anchor (hash-maps-and-ownership, only-inserting-a-value-if-the-key-has-no-value), `<!-- Old headings. Do not remove or links may break. -->` comment, `[^siphash]` footnote ও footnote definition সব preserve; reference link definition অপরিবর্তিত; Summary section-এর ৩টি exercise অনুবাদ করা হয়েছে কিন্তু example string ("Add Sally to Engineering") অপরিবর্তিত।

Stage Summary:
- Files translated: ch08-00-common-collections.md, ch08-01-vectors.md, ch08-02-strings.md, ch08-03-hash-maps.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: সব mdBook directive (`<Listing>`, `<a id="...">`, `<!-- Old headings. Do not remove or links may break. -->`, `<!-- ignore -->`) ও footnote `[^siphash]` সম্পূর্ণ অপরিবর্তিত রাখা হয়েছে যাতে cross-reference link না ভাঙে। সব code block (rust, rust,ignore, rust,should_panic,panics, rust,ignore,does_not_compile, console, text, toml) ও ভেতরের comment ("// do stuff with v", "// note s1 has been moved here and can no longer be used", "// field_name and field_value are invalid at this point, try using them and see what compiler error you get!", "// The method also works on a literal directly:", "// <- v goes out of scope and is freed here") সম্পূর্ণ অপরিবর্তিত। Listing caption গুলো Bangla-য় অনুবাদ করা হয়েছে (কিন্তু ভেতরের inline code English-এ)। Listing 8-14-এর multilingual greeting string গুলো (আরবি, হিন্দি, হিব্রু, জাপানি, কোরিয়ান, চাইনিজ, পর্তুগিজ, রাশিয়ান, স্প্যানিশ ইত্যাদি) অপরিবর্তিত। Heading-গুলো mixed English+Bangla যেখানে প্রযোজ্য (যেমন "## Vectors দিয়ে Value-এর List Store করা", "## String দিয়ে UTF-8 Encoded Text Store করা", "## Hash Map-এ Key সহ সম্পর্কিত Value Store করা")। একটি stray character ভুলবশত ch08-01-এর একটি heading-এ ঢুকে গিয়েছিল যেটা পরে fix করা হয়েছে।

---
Task ID: 17
Agent: general-purpose (sonnet)
Task: Chapter 16 (Fearless Concurrency) অনুবাদ

Work Log:
- worklog.md read করলাম — Task 1, 2, 3, 4 আগেই complete হয়েছে।
- _TRANSLATION_GUIDE.md read করে সব নিয়ম (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive ও Markdown structure preserve, দাঁড়ি ব্যবহার) মেনে নিলাম।
- ৫টি source file read করলাম (preprocessed source থেকে): ch16-00-concurrency.md, ch16-01-threads.md, ch16-02-message-passing.md, ch16-03-shared-state.md, ch16-04-extensible-concurrency-sync-and-send.md।
- ch16-00-concurrency.md — chapter intro ও > Note: blockquote অনুবাদ; concurrent/parallel/concurrency/message-passing/shared-state/Sync/Send সব technical term English-এ; chapter title "Fearless Concurrency" ও "fearless concurrency" নামটি proper-noun হিসেবে English-এ রাখা হয়েছে।
- ch16-01-threads.md — thread/spawn/join/JoinHandle/move/closure/ownership/race condition/deadlock/Copy/Drop ইত্যাদি term English-এ; সব code block (rust, console, text), Listing directive, manual-regeneration HTML comment, Old headings comment, `<a id="...">` anchor, `[capture]` link reference অপরিব্তিত; thread::spawn/thread::sleep/Duration/println!/vec!/drop/Rust-এর error message সব অপরিবর্তিত।
- ch16-02-message-passing.md — channel/transmitter/receiver/mpsc/Send/Result/recv/try_recv/unwrap/String/vec!/thread::spawn সব term English-এ; Old headings comment + `<a id="...">` anchor সব preserve; সব code block ও Go slogan quote ("Do not communicate by sharing memory; instead, share memory by communicating.") অপরিবর্তিত।
- ch16-03-shared-state.md — Mutex/mutual exclusion/lock/guard/MutexGuard/LockResult/Deref/Drop/Rc<T>/Arc<T>/atomic/interior mutability/RefCell<T>/Cell<T>/reference cycle/deadlock/Send/Sync ইত্যাদি term English-এ; সব code block, Listing directive, Old headings comment, anchor, `[atomic]` link reference অপরিবর্তিত; Go slogan quote অপরিবর্তিত।
- ch16-04-extensible-concurrency-sync-and-send.md — Send/Sync/marker trait/std::marker/raw pointer/unsafe/thread-safe/Rustonomicon সব term English-ে; দুটি Old headings anchor (`extensible-concurrency-with-the-sync-and-send-traits` ও `extensible-concurrency-with-the-send-and-sync-traits`) সব preserve; `[shared-access]` ও `[nomicon]` link reference অপরিবর্তিত; "The Rustonomicon" proper noun অপরিবর্তিত।

Stage Summary:
- Files translated: ch16-00-concurrency.md, ch16-01-threads.md, ch16-02-message-passing.md, ch16-03-shared-state.md, ch16-04-extensible-concurrency-sync-and-send.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: কোনো special issue নেই। সব structural element (code block, Listing directive, manual-regeneration comment, Old headings comment block, `<a id="...">` anchor, link reference) source-এর সাথে exact match করে। "Fearless Concurrency" chapter title ও "fearless concurrency" phrase টি proper noun হিসেবে English-এ রাখা হয়েছে। Go slogan quote দুটি জায়গায় (ch16-02 ও ch16-03) English-এই অপরিবর্তিত রাখা হয়েছে কারণ সেটি canonical quote। সব compiler error message (E0373, E0382, E0277) সম্পূর্ণ অপরিবর্তিত। সব thread/concurrency terminology (thread, spawn, join, channel, mpsc, transmitter, receiver, Mutex, Arc, Rc, RefCell, Send, Sync, lock, blocking, deadlock, race condition, atomic, interior mutability, ownership, move, closure, panic) English-এ রাখা হয়েছে।

---
Task ID: 23
Agent: general-purpose (sonnet)
Task: Appendices (A–G) অনুবাদ

Work Log:
- worklog.md read করলাম — Task 1 (Front matter), Task 4 (Ch03), Task 2 (Ch01), Task 3 (Ch02) ইতিমধ্যে complete হয়েছে।
- _TRANSLATION_GUIDE.md read করে সব নিয়ম (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive ও Markdown structure preserve, দাঁড়ি ব্যবহার) মেনে নিলাম।
- ৮টি source file read করলাম preprocessed source থেকে: appendix-00, appendix-01-keywords, appendix-02-operators, appendix-03-derivable-traits, appendix-04-useful-development-tools, appendix-05-editions, appendix-06-translation, appendix-07-nightly-rust।
- appendix-00.md — ছোট chapter intro অনুবাদ; "Appendix" heading অপরিবর্তিত।
- appendix-01-keywords.md — Keywords Currently in Use ও Keywords Reserved for Future Use list-এর সব keyword (`as`, `async`, `await`, `break`, `const`, `continue`, `crate`, `dyn`, `else`, `enum`, `extern`, `false`, `fn`, `for`, `if`, `impl`, `in`, `let`, `loop`, `match`, `mod`, `move`, `mut`, `pub`, `ref`, `return`, `Self`, `self`, `static`, `struct`, `super`, `trait`, `true`, `type`, `union`, `unsafe`, `use`, `where`, `while` এবং reserved গুলো `abstract`...`yield`) অপরিবর্তিত; শুধু description text Bangla-তে; Raw Identifiers section-এ সব code block (rust,ignore,does_not_compile / rust / text) ও compiler error output সম্পূর্ণ অপরিবর্তিত; `<span class="filename">`, `<!-- ignore -->` directive, `[raw-identifiers]`, `[union]`, `[appendix-e]` link reference অপরিবর্তিত।
- appendix-02-operators.md — Table B-1 (Operators) সম্পূর্ণ preserve; Operator/Example/Overloadable column অপরিবর্তিত, শুধু Explanation cell Bangla-তে; সব trait নাম (`Not`, `PartialEq`, `Rem`, `RemAssign`, `BitAnd`, `BitAndAssign`, `Mul`, `MulAssign`, `Deref`, `Add`, `AddAssign`, `Neg`, `Sub`, `SubAssign`, `Div`, `DivAssign`, `Shl`, `ShlAssign`, `PartialOrd`, `Shr`, `ShrAssign`, `BitXor`, `BitXorAssign`, `BitOr`, `BitOrAssign`) English-এ; <code>&vert;</code> HTML entity সম্পূর্ণ preserve; Table B-2 থেকে B-10 পর্যন্ত সব stand-alone/path/generics/trait bound/macro/comment/parentheses/curly/square bracket syntax table preserve; `<span class="caption">` সব অপরিবর্তিত।
- appendix-03-derivable-traits.md — `derive` attribute ও সব trait (`Debug`, `PartialEq`, `Eq`, `PartialOrd`, `Ord`, `Clone`, `Copy`, `Hash`, `Default`) heading English-এ; method নাম (`eq`, `partial_cmp`, `cmp`, `clone`, `hash`, `default`), type নাম (`HashMap<K, V>`, `BTreeSet<T>`, `Option<T>`, `Ordering`, `Iterator<Item=T>`, `Vec<u8>`) English-এ; `NaN`, `assert_eq!`, `unwrap_or_default`, `gen_range`, `to_vec`, `..Default::default()` সব English-এ; `[custom-derive-macros]`, `[stack-only-data-copy]`, `[variables-and-data-interacting-with-clone]`, `[creating-instances-from-other-instances-with-struct-update-syntax]` link reference ও `<!-- ignore -->` directive সব অপরিবর্তিত; standard library documentation link `../std/index.html` অপরিবর্তিত।
- appendix-04-useful-development-tools.md — `rustfmt`, `cargo-fmt`, `rustc`, `cargo`, `rustfix`, `cargo fix`, `cargo clippy`, `rust-analyzer`, `cargo build`, `cargo new` সব tool/command English-এ; সব code block (rust, console, text) ও ভেতরের compiler output সম্পূর্ণ অপরিবর্তিত; `<span class="filename">`, `<Listing file-name="...">` directive অপরিবর্তিত; `[rustfmt]`, `[editions]`, `[clippy]`, `[rust-analyzer]`, `[lsp]`, `[vscode]` link reference সব অপরিবর্তিত; Language Server Protocol term English-এ।
- appendix-05-editions.md — Edition concept, six-week release cycle, Rust 2015/2018/2021/2024 edition, `edition` key, `Cargo.toml`, `cargo fix` সব English-এ; `[edition-guide]` link reference অপরিবর্তিত; italic `_edition_`, `_Cargo.toml_`, `_The Rust Edition Guide_` formatting preserve।
- appendix-06-translation.md — শুধু intro paragraph Bangla-তে; সব language name ও link URL সম্পূর্ণ অপরিবর্তিত (Português, 简体中文, 正體中文, Українська, Español, Русский, ইত্যাদি); `[label]` link reference অপরিবর্তিত।
- appendix-07-nightly-rust.md — "Stability Without Stagnation", "Choo, Choo! Release Channels and Riding the Trains", "Maintenance time", "Unstable Features", "RFC Process and Teams" section heading-গুলো mixed English+Bangla ব্যবহার করা হয়েছে (canonical phrase হিসেবে English preserve); সব ASCII art diagram code block (`text` language) সম্পূর্ণ অপরিবর্তিত—অত্যন্ত গুরুত্বপূর্ণ কারণ এগুলো train model বোঝায়; `nightly`, `beta`, `stable`, `rustup`, `rustc`, `cargo`, `rustup toolchain install nightly`, `rustup toolchain list`, `rustup override set nightly`, `cargo fix`, `feature flag`, `feature gate`, `RFC`, `Request For Comments` সব term English-এ; সব code block (console, powershell, text) অপরিবর্তিত; `<!-- ignore -->` directive ও `[“Unstable Features”](#unstable-features)` anchor link অপরিবর্তিত; Rust governance link `https://www.rust-lang.org/governance` অপরিবর্তিত।

Stage Summary:
- Files translated: appendix-00.md, appendix-01-keywords.md, appendix-02-operators.md, appendix-03-derivable-traits.md, appendix-04-useful-development-tools.md, appendix-05-editions.md, appendix-06-translation.md, appendix-07-nightly-rust.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: সব keyword table, operator table (Table B-1 থেকে B-10), code block (rust, console, text, powershell, rust,ignore,does_not_compile), ASCII train model diagram, mdBook directive (`<!-- ignore -->`, `<span class="filename">`, `<span class="caption">`, `<Listing>`) সম্পূর্ণ অপরিবর্তিত। Heading-গুলোতে canonical English phrase যেখানে প্রযোজ্য (যেমন "Stability Without Stagnation", "Maintenance time", "Unstable Features", "RFC Process and Teams") preserve করা হয়েছে কারণ এগুলো Rust community-র পরিচিত পরিভাষা। সব trait/method/type name, tool name, command, edition identifier, language name ইত্যাদি English-এ। চলিত ভাষা ও দাঁড়ি ব্যবহৃত। কোনো special issue নেই।

---
Task ID: 19
Agent: general-purpose (sonnet)
Task: Chapter 18 (OOP Features of Rust) অনুবাদ

Work Log:
- worklog.md read করলাম — Task 1, 2, 3, 4 আগেই complete হয়েছে।
- _TRANSLATION_GUIDE.md read করে সব নিয়ম (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive ও Markdown structure preserve, দাঁড়ি ব্যবহার) মেনে নিলাম।
- ৪টি source file read করলাম preprocessed source থেকে: ch18-00-oop.md, ch18-01-what-is-oo.md, ch18-02-trait-objects.md, ch18-03-oo-design-patterns.md।
- ch18-00-oop.md — chapter intro অনুবাদ; OOP/object/Simula/Alan Kay/architecture ইত্যাদি technical term ও proper noun English-এ; `<!-- Old headings... -->` ও `<a id="object-oriented-programming-features-of-rust">` anchor preserve।
- ch18-01-what-is-oo.md — Objects/Encapsulation/Inheritance section অনুবাদ; `pub`/`impl`/`struct`/`enum`/`HashSet`/`Vec` ইত্যাদি keyword ও type English-এ; Gang of Four blockquote, Polymorphism blockquote, সব code block (rust,noplayground), ২টি `<Listing>` directive অপরিবর্তিত; object/encapsulation/inheritance/polymorphism/bounded parametric polymorphism ইত্যাদি term English-এ।
- ch18-02-trait-objects.md — trait object/dynamic dispatch/dyn compatibility/monomorphization/static dispatch/duck typing ইত্যাদি term English-এ; সব code block (rust + console), ৮টি `<Listing>` directive, ২টি `<a id>` anchor, `<!-- Old headings -->` ও `<!-- ignore -->` directive, ৩টি reference link definition (`[performance-of-code-using-generics]`, `[dynamically-sized]`, `[dyn-compatibility]`) অপরিবর্তিত; `Box<dyn Draw>`, `dyn` keyword সব English-এ।
- ch18-03-oo-design-patterns.md — state pattern/blog post workflow অনুবাদ; state object/trait object/deref coercion/ownership/dyn compatibility ইত্যাদি term English-এ; সব code block (rust, rust+ignore, rust+ignore+does_not_compile), ১২টি `<Listing>` directive, ৯টি `<a id>` anchor, `<!-- Old headings -->` ও `<!-- ignore -->` directive, ২টি reference link definition (`[more-info-than-rustc]`, `[macros]`) অপরিবর্তিত; "Why Not An Enum?" blockquote-এর শিরোনাম English-এ রাখা হয়েছে কারণ এটি একটি common/conventional aside শিরোনাম এবং `match` keyword এর সাথে সরাসরি সম্পর্কিত।
- Structure verification: code block count, Listing count, anchor count সব source-এর সাথে exact match করে।

Stage Summary:
- Files translated: ch18-00-oop.md, ch18-01-what-is-oo.md, ch18-02-trait-objects.md, ch18-03-oo-design-patterns.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: সব technical term (object-oriented, encapsulation, inheritance, polymorphism, trait object, dyn, vtable নাম না থাকলেও dynamic dispatch, static dispatch, design pattern, state pattern, state object, deref coercion, monomorphization, duck typing, dyn compatibility, ownership) English-এ রাখা হয়েছে। Book/proper noun ("Gang of Four", Simula, Alan Kay, Design Patterns book title) English-এ। "Why Not An Enum?" blockquote-এর শিরোনাম এবং Summary heading English-এ রাখা হয়েছে conventional section label হিসেবে; বাকি heading গুলো Bangla-য় অনুবাদ করা হয়েছে (heading-এ থাকা `Post`, `content`, `approve` ইত্যাদি inline code English-এ)। কোনো special issue নেই।

---
Task ID: 14
Agent: general-purpose (sonnet)
Task: Chapter 13 (Functional Language Features: Iterators and Closures) অনুবাদ

Work Log:
- worklog.md read করলাম — Task 1 (Front matter), 2 (Ch01), 3 (Ch02), 4 (Ch03), 7 (Ch06), 9 (Ch08), 15 (Ch14), 17 (Ch16) আগেই complete হয়েছে।
- _TRANSLATION_GUIDE.md read করে সব নিয়ম (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive ও Markdown structure preserve, দাঁড়ি ব্যবহার, inline code ও code block অপরিবর্তিত) মেনে নিলাম।
- ৫টি source file read করলাম preprocessed source থেকে: ch13-00 (functional-features intro), ch13-01 (closures), ch13-02 (iterators), ch13-03 (improving I/O project), ch13-04 (performance + summary)।
- ch13-00-functional-features.md — chapter intro অনুবাদ; functional programming, closure, iterator ইত্যাদি term English-এ; bullet list-এর _Closures_, _Iterators_, I/O project reference সব preserve; heading "Functional Language Features: Iterators এবং Closures" রাখা হয়েছে।
- ch13-01-closures.md — closure/anonymous function/capture/environment/FnOnce/FnMut/Fn/trait bound/`move` keyword/borrow/immutable reference/mutable reference/ownership/generic type/`Option<T>`/`unwrap_or_else`/`sort_by_key`/`FnOnce`/`FnMut`/`Fn`/associated type/consume/mutate ইত্যাদি term English-এ; সব `<Listing number="13-1"...>` থেকে `13-9` পর্যন্ত directive, code block (rust, rust,noplayground, rust,ignore, rust,ignore,does_not_compile, console), Old headings comment, `<a id="...">` anchor (closures-anonymous-functions-that-can-capture-their-environment, closures-anonymous-functions-that-capture-their-environment, creating-an-abstraction-of-behavior-with-closures, refactoring-using-functions, refactoring-with-closures-to-store-code, capturing-the-environment-with-closures, closure-type-inference-and-annotation, storing-closures-using-generic-parameters-and-the-fn-traits, limitations-of-the-cacher-implementation, moving-captured-values-out-of-the-closure-and-the-fn-traits, moving-captured-values-out-of-closures-and-the-fn-traits), `<!-- ignore -->` directive ও `[unwrap-or-else]` link reference সব preserve; > Note: blockquote অনুবাদ কিন্তু syntax preserve; Listing caption English-এ (Task 3 ও 15 convention অনুসরণ করে)।
- ch13-02-iterators.md — iterator/lazy/consume/consuming adapter/iterator adapter/`Iterator` trait/`next` method/`Item`/associated type/`Some`/`None`/immutable reference/mutable reference/ownership/`iter`/`into_iter`/`iter_mut`/`sum`/`map`/`collect`/`filter`/`Vec<_>`/closure/capture environment ইত্যাদি term English-এ; সব `<Listing number="13-10"...>` থেকে `13-16` directive, code block (rust, rust,noplayground, rust,not_desired_behavior, console), Old headings comment, `<a id="using-closures-that-capture-their-environment"></a>` anchor সব preserve; Listing caption English-এ।
- ch13-03-improving-our-io-project.md — iterator/`clone`/ownership/`Config::build`/`env::args`/`Iterator` trait/`impl Iterator<Item = String>`/`impl Trait`/`next`/`match`/`Some`/`None`/iterator adapter/mutable state/parallel/`search`/`filter`/`collect`/`impl Iterator<Item = &'a str>`/`for` loop/laziness ইত্যাদি term English-এ; সব `<Listing number="13-17"...>` থেকে `13-22` directive, code block (rust,ignore, rust,ignore,does_not_compile, rust,ignore,noplayground), `<span class="filename">` tag, Old headings comment, anchor (using-iterator-trait-methods-instead-of-indexing, making-code-clearer-with-iterator-adapters, choosing-between-loops-or-iterators), `<!-- ignore -->` directive ও `[impl-trait]` link reference সব preserve; Listing caption English-ে।
- ch13-04-performance.md — benchmark/iterator/zero-cost abstraction/loop unrolling/bounds checking/assembly/runtime overhead ইত্যাদি term English-ে; সব code block (text), Old headings comment, `<a id="comparing-performance-loops-vs-iterators"></a>` anchor preserve; Bjarne Stroustrup-এর zero-overhead principle quote সম্পূর্ণ English-এ অপরিবর্তিত রাখা হয়েছে (historical/canonical quote); final Summary section অনুবাদ।
- Structure verification: ch13-00 (0 Listing, 0 anchor, 0 fence, 0 old-heading), ch13-01 (9 Listing, 11 anchor, 34 fence, 4 old-heading), ch13-02 (7 Listing, 1 anchor, 18 fence, 1 old-heading), ch13-03 (6 Listing, 3 anchor, 14 fence, 3 old-heading), ch13-04 (0 Listing, 1 anchor, 2 fence, 1 old-heading) — সব source-এর সাথে exact match করে।

Stage Summary:
- Files translated: ch13-00-functional-features.md, ch13-01-closures.md, ch13-02-iterators.md, ch13-03-improving-our-io-project.md, ch13-04-performance.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: সব mdBook directive (`<Listing>`, `<span class="filename">`, `<a id="...">`, `<!-- Old headings. Do not remove or links may break. -->`, `<!-- ignore -->`) ও reference link definition (`[unwrap-or-else]`, `[impl-trait]`) সম্পূর্ণ অপরিবর্তিত রাখা হয়েছে যাতে cross-reference link না ভাঙে। সব code block (rust, rust,noplayground, rust,ignore, rust,ignore,does_not_compile, rust,not_desired_behavior, rust,ignore,noplayground, console, text) ও ভেতরের comment, error message (E0308, E0507), compiler output সম্পূর্ণ অপরিবর্তিত। Listing caption গুলো Task 3 (Ch02) ও Task 15 (Ch14) convention অনুসরণ করে English-ে রাখা হয়েছে rendered output-এ formatting issue এড়াতে। Bjarne Stroustrup-এর zero-overhead principle quote (ch13-04) সম্পূর্ণ English-ে অপরিবর্তিত রাখা হয়েছে কারণ সেটি canonical quote। Heading-গুলো mixed English+Bangla যেখানে প্রযোজ্য (যেমন "## Closures", "### Capturing the Environment", "### Inferring এবং Annotating Closure Type", "### Capturing References বা Moving Ownership", "### Moving Captured Values Out of Closures", "## Processing a Series of Items with Iterators", "### The `Iterator` Trait এবং `next` Method", "### Methods That Consume the Iterator", "### Methods That Produce Other Iterators", "### Closures That Capture Their Environment", "## Improving Our I/O Project", "### Removing a `clone` Using an Iterator", "#### Using the Returned Iterator Directly", "#### Using `Iterator` Trait Methods", "### Clarifying Code with Iterator Adapters", "### Choosing Between Loops এবং Iterators", "## Performance in Loops vs. Iterators", "## Summary")। closure/iterator/adaptor/consumer/lazy/ownership/borrow/move/Fn/FnMut/FnOnce সব technical term English-ে রাখা হয়েছে। কোনো special issue নেই।

---
Task ID: 20
Agent: general-purpose (sonnet)
Task: Chapter 19 (Patterns and Matching) অনুবাদ

Work Log:
- worklog.md read করলাম — Task 1, 2, 3, 4 আগেই complete হয়েছে।
- _TRANSLATION_GUIDE.md read করে সব নিয়ম (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive ও Markdown structure preserve, দাঁড়ি ব্যবহার, inline code ও code block অপরিবর্তিত) মেনে নিলাম।
- ৪টি source file read করলাম preprocessed source থেকে: ch19-00-patterns.md, ch19-01-all-the-places-for-patterns.md, ch19-02-refutability.md, ch19-03-pattern-syntax.md (864 lines)।
- ch19-00-patterns.md — chapter intro অনুবাদ; pattern, match, destructuring, wildcards, placeholders ইত্যাদি term English-এ; Literals/Destructured arrays/Variables/Wildcards/Placeholders bullet list অপরিবর্তিত (technical term list)।
- ch19-01-all-the-places-for-patterns.md — `match` arm, `let` statement, `if let`, `while let`, `for` loop, function parameter সব section অনুবাদ; সব code block (rust, console), `<pre><code>` block, `<Listing>` directive (caption English-এ রাখা হয়েছে ch02 convention অনুসারে), HTML comment (`<!-- Manually formatted -->`), `<!-- ignore -->` directive, `<a id="...">` anchor, link reference `[ignoring-values-in-a-pattern]:` সম্পূর্ণ অপরিবর্তিত; `match`, `if let`, `else if`, `else if let`, `else`, `while let`, `for`, `let...else`, `Option`, `Result`, `Some`, `None`, `Ok`, `Err`, `recv`, `enumerate`, `iter`, closure ইত্যাদি term English-এ।
- ch19-02-refutability.md — refutable/irrefutable concept অনুবাদ; `let`, `let...else`, `if let`, `while let`, `match`, `Some(x)`, `None`, `Option<i32>`, `irrefutable_let_patterns` ইত্যাদি term English-এ; compiler error/warning console output সম্পূর্ণ অপরিবর্তিত; ৩টি `<Listing>` directive preserve করা হয়েছে।
- ch19-03-pattern-syntax.md — Matching Literals, Matching Named Variables, Matching Multiple Patterns, Range `..=`, Destructuring (Struct/Enum/Nested/Struct+Tuple), Ignoring Values (`_`, nested `_`, `_` prefix, `..`), Match Guards, `@` Bindings, Summary সব section অনুবাদ; shadow/shadowing, match guard, range pattern, struct field shorthand, `@` operator, destructuring, wildcard, ownership/move ইত্যাদি term English-এ; ১৯টি `<Listing>` directive (caption English-এ), ১১টি `<a id="...">` anchor (Old headings), ১১টি HTML comment, ২টি `<!-- ignore -->`, ২টি `<pre><code>` বা কোড ব্লক, সব rust/console/text code block ও compiler error output সম্পূর্ণ অপরিবর্তিত; struct/enum/tuple pattern syntax, `Some(x)`, `Message::Quit`, `Message::Move`, `Message::Write`, `Message::ChangeColor`, `Color::Rgb`, `Color::Hsv`, `Point`, `id @ 3..=7`, `1 | 2`, `_`, `..` সব code- level element English-এ।
- Structure verification (final): ৪টি file-এর জন্যই code fence count, `<Listing>` count, `<!--` count, `<a id>` count, heading count source-এর সাথে exact match করে। প্রথমে ch19-01-এ একটি `<!-- ignore -->` directive ছুটে গিয়েছিল — fix করেছি।

Stage Summary:
- Files translated: ch19-00-patterns.md, ch19-01-all-the-places-for-patterns.md, ch19-02-refutability.md, ch19-03-pattern-syntax.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: সব mdBook directive (`<Listing>`, `<pre><code>`, `<a id="...">`, `<!-- ignore -->`, `<!-- Manually formatted ... -->`, `<!-- Old headings ... -->`) ও HTML comment অপরিবর্তিত রাখা হয়েছে। Listing caption গুলো ch02-এর convention অনুসরণ করে English-এ রাখা হয়েছে যাতে rendered output-এ formatting issue না হয়। Technical term (pattern, match, refutable, irrefutable, binding, destructuring, match guard, shadowing, wildcard, range pattern, struct/enum/tuple pattern, `@` binding, `..`, `_`, `..=`) সব English-এ রাখা হয়েছে। Section heading গুলো Bangla-য় অনুবাদ করা হয়েছে কিন্তু heading-এ থাকা code/keyword (যেমন `match`, `let`, `if let`, `while let`, `for`, `..=`, `@`, `_`) English-এ। চলিত ভাষা ও দাঁড়ি ব্যবহার করা হয়েছে। কোনো special issue নেই — সব structural element source-এর সাথে exact match করে।

---
Task ID: 10
Agent: general-purpose (sonnet)
Task: Chapter 9 (Error Handling) অনুবাদ

Work Log:
- worklog.md read করলাম — Task 1 (Front matter), 4 (Ch03), 2 (Ch01), 3 (Ch02) আগেই complete হয়েছে।
- _TRANSLATION_GUIDE.md read করে সব নিয়ম (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive ও Markdown structure preserve, দাঁড়ি ব্যবহার) মেনে নিলাম।
- ৪টি source file read করলাম preprocessed source থেকে: ch09-00-error-handling.md, ch09-01-unrecoverable-errors-with-panic.md, ch09-02-recoverable-errors-with-result.md (663 lines, দুই ভাগে read করা হয়েছে), ch09-03-to-panic-or-not-to-panic.md।
- ch09-00-error-handling.md — chapter intro অনুবাদ; recoverable/unrecoverable error, panic, Result, exception, `Result<T, E>`, `panic!` macro ইত্যাদি technical term English-ে রাখা হয়েছে।
- ch09-01-unrecoverable-errors-with-panic.md — panic/unwind/abort/backtrace/buffer overread/panic = 'abort' ইত্যাদি term English-ে; "Unwinding the Stack or Aborting in Response to a Panic" blockquote (heading + content + `toml` code block) সম্পূর্ণ preserve; `cargo run`, `RUST_BACKTRACE=1`, `target/debug/panic`, file path সব অপরিবর্তিত; ৩টি `<Listing>` directive (Listing 9-1, 9-2 ও একটি no-number), `<a id="using-a-panic-backtrace">` anchor, `<!-- Old headings. Do not remove or links may break. -->` comment, manual-regeneration comment block, `rust,should_panic,panics` ও `console` code block সব অপরিবর্তিত; `[to-panic-or-not-to-panic]: ...` link reference অপরিবর্তিত; backtrace-এর ভেতরের পুরো stack trace code block অপরিবর্তিত।
- ch09-02-recoverable-errors-with-result.md — Result/Ok/Err/generic type parameter/io::Error/file handle/match/unwrap/expect/propagate/`?` operator/closure/From trait/FromResidual/Option/Termination trait ইত্যাদি term English-ে; ১২টি `<Listing>` directive (Listing 9-3 থেকে 9-12 পর্যন্ত) সব preserve, caption text English-ে রাখা হয়েছে; ৩টি anchor (`shortcuts-for-panic-on-error-unwrap-and-expect`, `a-shortcut-for-propagating-errors-the--operator`, `where-the--operator-can-be-used`), ৩টি `<!-- Old headings. Do not remove or links may break. -->` comment, ২টি Deliberately-not-using-rustdoc_include comment, manual-regeneration comment (×২), `<!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->` comment, সব `rust,should_panic`/`rust,ignore`/`rust,ignore,does_not_compile`/`console`/`text` code block অপরিবর্তিত; "Alternatives to Using `match` with `Result<T, E>`" nested blockquote-এর ভেতরের `rust,ignore` code block সহ সম্পূর্ণ structure preserve; `[handle_failure]`, `[trait-objects]`, `[termination]` তিনটি link reference অপরিবর্তিত; বাংলা paragraph গুলো ঘন হওয়ায় line count কম কিন্তু content সম্পূর্ণ।
- ch09-03-to-panic-or-not-to-panic.md — bad state/contract/invariant/guarantee/getter ইত্যাদি term English-ে; bad state-এর ৩টি bullet list structure সম্পূর্ণ preserve; ২টি `<Listing>` directive (no-number ও Listing 9-13) preserve; ২টি anchor (`cases-in-which-you-have-more-information-than-the-compiler`, `creating-custom-types-for-validation`), `<!-- Old headings. Do not remove or links may break. -->` comment (×২), `rust,ignore` ও `rust` code block, `IpAddr` example, `Guess` struct example সম্পূর্ণ অপরিবর্তিত; `[encoding]` link reference অপরিবর্তিত; final Summary section অনুবাদ করা হয়েছে।

Stage Summary:
- Files translated: ch09-00-error-handling.md, ch09-01-unrecoverable-errors-with-panic.md, ch09-02-recoverable-errors-with-result.md, ch09-03-to-panic-or-not-to-panic.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: সব mdBook directive (`<Listing>` সহ caption, `<a id="...">` anchor, `<!-- Old headings... -->` ও `<!-- manual-regeneration -->` ও `<!-- CAN'T EXTRACT... -->` ও `<!-- Deliberately not using rustdoc_include... -->` comment), সব code block (rust/rust,should_panic/rust,ignore/rust,ignore,does_not_compile/toml/console/text), সব link reference (`[handle_failure]`, `[trait-objects]`, `[termination]`, `[encoding]`, `[to-panic-or-not-to-panic]`), সব inline code (`panic!`, `Result<T, E>`, `Ok`, `Err`, `Option`, `unwrap`, `expect`, `?`, `match`, `File::open`, `read_to_string`, `unwrap_or_else`, `ErrorKind::NotFound`, `From` trait, `FromResidual`, `Termination`, `Box<dyn Error>`, `i32`, `u32`, `mod guessing_game;` ইত্যাদি) অপরিবর্তিত। Bangla paragraph গুলো ঘন হওয়ায় output line count source-এর চেয়ে কম কিন্তু content সম্পূর্ণ এবং সব structural element source-এর সাথে exact match করে। Heading text গুলো Bangla-য় অনুবাদ করা হয়েছে কিন্তু heading-এ থাকা code/keyword (`panic!`, `Result`, `?` operator) English-এ রাখা হয়েছে। "Unwinding the Stack" ও "Aborting" ও "buffer overread" ও "backtrace" ও "bad state" ও "contract" ও "invariant" ও "getter" ইত্যাদি term technical হিসেবে English-এ রাখা হয়েছে। Listing caption text গুলো English-এ রাখা হয়েছে যাতে rendered output-এ কোনো formatting issue না হয় (পূর্ববর্তী chapter-গুলোর convention অনুসরণ করে)।

---
Task ID: 8
Agent: general-purpose (sonnet)
Task: Chapter 7 (Packages, Crates, Modules) অনুবাদ

Work Log:
- worklog.md read করলাম — Task 1 (Front matter), Task 2 (Ch01), Task 3 (Ch02), Task 4 (Ch03) আগেই complete হয়েছে।
- _TRANSLATION_GUIDE.md read করে সব নিয়ম (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive ও Markdown structure preserve, দাঁড়ি ব্যবহার, inline code ও code block অপরিবর্তিত) মেনে নিলাম।
- ৬টি preprocessed source file read করলাম: ch07-00 (chapter intro), ch07-01 (packages/crates), ch07-02 (modules cheat sheet + grouping), ch07-03 (paths + pub + super + struct/enum), ch07-04 (use keyword, as, pub use, external packages, nested paths, glob), ch07-05 (separating modules into files + summary)।
- ch07-00 — chapter intro অনুবাদ; module system feature list-এ package/crate/module/path সব term English-এ; `[workspaces]` reference link ও `<!-- ignore -->` directive অপরিবর্তিত; `<a id="managing-growing-projects-with-packages-crates-and-modules"></a>` anchor ও `<!-- Old headings... -->` comment preserve।
- ch07-01 — packages ও crates concept অনুবাদ; binary crate/library crate/crate root/package/Cargo.toml/Cargo.lock সব term English-এ; `cargo new my-project`, `ls my-project` console output অপরিবর্তিত; _src/main.rs_, _src/lib.rs_, _src/bin_ সব path অপরিবর্তিত; `[basics]`, `[modules]`, `[rand]` reflink সব preserve।
- ch07-02 — Modules Cheat Sheet এর সব ৫টি rule অনুবাদ (Start from crate root, Declaring modules, Declaring submodules, Paths to code, Private vs public, use keyword); `backyard` উদাহরণ-এর text tree, _src/garden.rs_, _src/garden/vegetables.rs_ সব path অপরিবর্তিত; ৩টি rust code block (`use crate::garden::vegetables::Asparagus;` ইত্যাদি) সম্পূর্ণ অপরিবর্তিত; ৪টি `<Listing>` directive preserve; restaurant metaphor (front of house/back of house) চলিত ভাষায়; module tree ASCII diagram অপরিবর্তিত।
- ch07-03 — absolute path/relative path অনুবাদ; Listing 7-3 থেকে 7-10 পর্যন্ত সব rust code block (privacy rule example, `pub mod hosting`, `super::deliver_order`, `pub struct Breakfast`, `pub enum Appetizer`) অপরিবর্তিত; `cargo build` console error output দুটি (Listing 7-4 ও 7-6) সম্পূর্ণ অপরিবর্তিত; "Best Practices for Packages with a Binary and a Library" blockquote অনুবাদ কিন্তু structure preserve; `// -- snip --` comment code block-এর ভেতরে অপরিবর্তিত; `[pub]`, `[api-guidelines]`, `[ch12]` reflink preserve।
- ch07-04 — `use` keyword, `as`, `pub use`, external package, nested path, glob operator সব section অনুবাদ; Listing 7-11 থেকে 7-20 পর্যন্ত সব rust code block অপরিবর্তিত; `cargo build` error console output অপরিবর্তিত; ANCHOR comment যুক্ত rust code block (`use rand::prelude::*;` ইত্যাদি) সম্পূর্ণ অপরিবর্তিত; `<a id="using-nested-paths-to-clean-up-large-use-lists">`, `<a id="the-glob-operator">` anchor ও `<!-- Old headings... -->` comment সব preserve; Cargo.toml code block (`rand = "0.10.1"`) অপরিবর্তিত; `[ch14-pub-use]`, `[rand]`, `[writing-tests]` reflink preserve।
- ch07-05 — module আলাদা file-এ ভাগ করা অনুবাদ; Listing 7-21 ও 7-22 সহ সব rust code block অপরিবর্তিত; _src/lib.rs_, _src/front_of_house.rs_, _src/front_of_house/hosting.rs_ সব path অপরিবর্তিত; "Alternate File Paths" blockquote অনুবাদ কিন্তু structure preserve; `[paths]` reflink preserve; Summary section অনুবাদ।
- Verification: সব ৬টি file-এ code fence count source-এর সাথে exact match (0/2/12/16/32/8), সব `<Listing>` tag count match, সব reflink definition ও inline reference link present।

Stage Summary:
- Files translated: ch07-00-managing-growing-projects-with-packages-crates-and-modules.md, ch07-01-packages-and-crates.md, ch07-02-defining-modules-to-control-scope-and-privacy.md, ch07-03-paths-for-referring-to-an-item-in-the-module-tree.md, ch07-04-bringing-paths-into-scope-with-the-use-keyword.md, ch07-05-separating-modules-into-different-files.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: সব technical term (package, crate, binary crate, library crate, crate root, module, path, absolute path, relative path, privacy, visibility, scope, use, pub, mod, crate, super, self, re-export, re-exporting, glob operator, prelude, sibling, parent, child, ancestor) English-এ রাখা হয়েছে। সব module path ও file path (`crate::front_of_house::hosting::add_to_waitlist`, `crate::garden::vegetables::Asparagus`, `std::collections::HashMap`, `std::fmt::Result`, `std::io::Result`, `std::io::Write`, `restaurant::front_of_house::hosting::add_to_waitlist`, ইত্যাদি) অপরিবর্তিত। কোনো special issue নেই; সব structural element source-এর সাথে exact match করে। Code block-এর ভেতরের comment (`// Absolute path`, `// Relative path`, `// -- snip --`, `// --snip--`, `// ANCHOR: ...`, `// ANCHOR_END: ...`) এবং ANCHOR marker সব অপরিবর্তিত রাখা হয়েছে।

---
Task ID: 6
Agent: general-purpose (sonnet)
Task: Chapter 5 (Using Structs) অনুবাদ

Work Log:
- worklog.md read করলাম — Task 1 (Front matter), Task 2 (Ch01), Task 3 (Ch02), Task 4 (Ch03) আগেই complete হয়েছে।
- _TRANSLATION_GUIDE.md read করে সব নিয়ম (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive ও Markdown structure preserve, দাঁড়ি ব্যবহার) মেনে নিলাম।
- ৪টি source file read করলাম (preprocessed source থেকে): ch05-00, ch05-01, ch05-02, ch05-03।
- ch05-00-structs.md — chapter intro অনুবাদ; struct/structure/custom data type/associated function/method/enum/compile-time type checking ইত্যাদি technical term English-এ রাখা হয়েছে।
- ch05-01-defining-structs.md — struct define/instantiate, field, instance, dot notation, mutable, field init shorthand, struct update syntax, tuple struct, unit-like struct, lifetime, owned type/String/&str/Move/Copy trait ইত্যাদি technical term English-এ; সব `<Listing>` directive (caption Bangla-য়), code block, `<!-- Old headings -->` HTML comment, `<a id="...">` anchor, manual-regeneration comment block, link reference (`[tuples]`, `[move]`, `[copy]`) সব অপরিবর্তিত; Ownership of Struct Data blockquote-সহ `rust,ignore,does_not_compile` code block, console output ও compiler error message সম্পূর্ণ অপরিবর্তিত।
- ch05-02-example-structs.md — Rectangle area calculation tutorial, tuple refactor, struct refactor, immutable borrow, `Debug` trait, `#[derive(Debug)]` attribute, `{:?}`/`{:#?}`/`{}` formatter, `dbg!` macro, stderr/stdout ইত্যাদি technical term English-এ; সব `<Listing>` directive, console/text code block, `rust,ignore,does_not_compile` code block, compiler error output অপরিবর্তিত; `> Note:` blockquote syntax preserve; link reference (`[the-tuple-type]`, `[app-c]`, `[println]`, `[dbg]`, `[err]`, `[attributes]`) সব অপরিবর্তিত।
- ch05-03-method-syntax.md — method syntax, `impl` block, `self`/`&self`/`&mut self`/`Self`, method syntax, automatic referencing and dereferencing, getter, public/private API, associated function, `::` syntax, multiple `impl` block ইত্যাদি technical term English-এ; C/C++ `->` operator blockquote, `CAN'T EXTRACT` HTML comment, hidden `# ` attribute lines in rust code block সম্পূর্ণ অপরিবর্তিত; `<span class="filename">` অপরিবর্তিত; সব `<Listing>` directive ও link reference (`[enums]`, `[trait-objects]`, `[public]`, `[modules]`) অপরিবর্তিত; final Summary section অনুবাদ।
- Structure verification (Python দিয়ে): code fences, `<Listing>`/`</Listing>` count, anchor count, link definition count, heading count — সব source-এর সাথে exact match করে (ch05-01: 22/22 fences, 10/10 Listings, 4/4 anchors, 3/3 linkdefs, 5/5 headings; ch05-02: 30/30 fences, 5/5 Listings, 2/2 anchors, 6/6 linkdefs, 4/4 headings; ch05-03: 16/16 fences, 5/5 Listings, 1/1 anchor, 4/4 linkdefs, 6/6 headings)।

Stage Summary:
- Files translated: ch05-00-structs.md, ch05-01-defining-structs.md, ch05-02-example-structs.md, ch05-03-method-syntax.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: কোনো special issue নেই। সব code block (rust, console, text, rust,ignore,does_not_compile), inline code, `<Listing>` directive, anchor, HTML comment (Old headings / manual-regeneration / CAN'T EXTRACT), link reference ও link definition source-এর সাথে exact match করে। Listing caption গুলো Bangla-য় অনুবাদ করা হয়েছে (ভেতরের inline code English-এ)। Ownership of Struct Data ও `->` Operator blockquote-সহ `> ` prefix syntax preserve করা হয়েছে। Heading গুলো mixed Bangla+English (যেমন "## Struct Define এবং Instantiate করা", "### Field Init Shorthand ব্যবহার করা", "### Tuple Struct দিয়ে ভিন্ন Type তৈরি করা", "### Associated Function", "### Multiple `impl` Block", "## Method") — guide-এর নিয়ম অনুযায়ী heading-এ থাকা Rust keyword/code English-এ রাখা হয়েছে। Reader-কে "তুমি" হিসেবে address করা হয়েছে, সব বাক্যে দাঁড়ি ব্যবহার করা হয়েছে।

---
Task ID: 5
Agent: general-purpose (opus)
Task: Chapter 4 (Understanding Ownership) অনুবাদ

Work Log:
- worklog.md read করলাম — Task 1 (Front matter), Task 2 (Ch01), Task 3 (Ch02), Task 4 (Ch03) আগেই complete হয়েছে।
- _TRANSLATION_GUIDE.md read করে সব নিয়ম (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive ও Markdown structure preserve, দাঁড়ি ব্যবহার, inline code ও code block অপরিবর্তিত) মেনে নিলাম।
- ৪টি source file read করলাম: ch04-00 (intro), ch04-01 (what-is-ownership, ৬৩১ lines), ch04-02 (references-and-borrowing, ৪০০ lines), ch04-03 (slices, ৪১৬ lines)।
- ch04-00-understanding-ownership.md — short chapter intro; "# Understanding Ownership" heading "Ownership বোঝা" (SUMMARY.md-এর সাথে consistent) রাখলাম; ownership/borrowing/slice/memory safety/garbage collector সব term English-এ।
- ch04-01-what-is-ownership.md — Ownership concept, Stack/Heap blockquote, Ownership Rules, Variable Scope, `String` type, Memory and Allocation, Move, Scope and Assignment, Clone, Copy, Ownership and Functions, Return Values and Scope section অনুবাদ; ৫টি `<Listing>` directive ও ভেতরের rust code block, ৫টি `<img>` (Figure 4-1 থেকে 4-5), ৫টি `<span class="caption">`, RAII Note blockquote, `<a id="ways-variables-and-data-interact-move">` ও `<a id="ways-variables-and-data-interact-clone">` anchor, `<!-- Old headings... -->` HTML comment, ৫টি `<!-- ignore -->` directive, `[data-types]`/`[ch8]`/`[traits]`/`[derivable-traits]`/`[methods]`/`[paths-module-tree]` link reference, সব console output (E0382, E0596 ইত্যাদি error) সম্পূর্ণ অপরিবর্তিত; technical term (ownership, move, copy, clone, shallow copy, deep copy, drop, double free, scope, stack, heap, allocate, free, pointer, RAII, garbage collector, Copy trait, Drop trait) English-এ রাখা।
- ch04-02-references-and-borrowing.md — References, Borrowing, Mutable References, Dangling References, The Rules of References section অনুবাদ; ৬টি `<Listing>` directive ও ভেতরের rust code, Figure 4-6 (`<img>` ও `<span class="caption">`), dereferencing Note blockquote, সব console output (E0596, E0499, E0502, E0106 error), `&`/`&mut`/`*` operator সম্পূর্ণ অপরিবর্তিত; technical term (reference, borrowing, mutable reference, immutable reference, dereferencing, dereference operator, dangling reference, data race, scope, lifetime, `'static` lifetime, move) English-এ।
- ch04-03-slices.md — Slice Type, String Slices, String Literals as Slices, String Slices as Parameters, Other Slices, Summary section অনুবাদ; ৬টি `<Listing>` directive ও ভেতরের rust code, Figure 4-7 (`<img>` ও `<span class="caption">`), ASCII Note blockquote, String slice range indices Note blockquote, `<a id="string-literals-are-slices">` anchor, `<!-- Old headings... -->` HTML comment, ৫টি `<!-- ignore -->` directive (সোর্সে একটি line-wrap করা ছিল আমি single-line-এ করেছি), `[collection]`/`[strings]`/`[ch13]`/`[ch6]`/`[deref-coercions]` link reference, সব console output (E0502 error) সম্পূর্ণ অপরিবর্তিত; technical term (slice, string slice, reference, ownership, iterator, deref coercions, UTF-8, ASCII, byte, range, tuple, pattern, destructure, collection) English-ে।
- Structure verification: ch04-01 (৩০ code fences, ৫ Listings, ৫ img, ৫ caption, ৬ link refs, ৫ ignore — source-এর সাথে exact match), ch04-02 (৩৪ code fences, ৬ Listings, ১ img, ১ caption — exact match), ch04-03 (৪২ code fences, ৬ Listings, ১ img, ১ caption, ৫ ignore — content match; source-এর একটি `<!-- ignore -->` line-wrap হওয়ায় grep count আলাদা, content একই), ch04-00 (intro paragraph, ০ directive)।
- Listing caption গুলো Task 2 ও Task 4-এর নিয়ম অনুসরণ করে English-এ রাখা হয়েছে (rendered output-এ formatting issue এড়াতে); ভেতরের inline code (`fn first_word`, `&str`, `usize`, `String`, `first_word` ইত্যাদি) English-এ।

Stage Summary:
- Files translated: ch04-00-understanding-ownership.md, ch04-01-what-is-ownership.md, ch04-02-references-and-borrowing.md, ch04-03-slices.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: সব code block (rust, console, text), inline code, `<Listing>` directive, `<img>` tag, `<span class="caption">`, HTML comment (`<!-- Old headings -->`), `<a id="...">` anchor, `<!-- ignore -->` directive, সব reference link definition ও সব console error output অপরিবর্তিত। Heading গুলো Bangla-তে অনুবাদ করা হয়েছে কিন্তু heading-এর ভেতরের code/keyword (`String`, `Copy` trait) English-এ রাখা হয়েছে। Technical term (ownership, borrowing, move, copy, clone, drop, reference, mutable reference, immutable reference, slice, dangling reference, data race, scope, stack, heap, lifetime, deref coercions, iterator ইত্যাদি) সব English-এ। Listing caption Task 2/4 consistency-র জন্য English-এ রাখা হয়েছে। ch04-03 source-এ `[deref-coercions]<!-- ignore -->` এর `<!-- ignore -->` অংশটি line-wrap করা ছিল; আমি single-line-এ রেখেছি — content অভিন্ন। কোনো special issue নেই।

---
Task ID: 11
Agent: general-purpose (opus)
Task: Chapter 10 (Generic Types, Traits, and Lifetimes) অনুবাদ

Work Log:
- worklog.md read করলাম — Task 1, 2, 3, 4 আগেই complete হয়েছে।
- _TRANSLATION_GUIDE.md read করে সব নিয়ম (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive ও Markdown structure preserve, দাঁড়ি ব্যবহার) মেনে নিলাম।
- ৪টি source file read করলাম preprocessed source থেকে: ch10-00-generics.md, ch10-01-syntax.md, ch10-02-traits.md, ch10-03-lifetime-syntax.md।
- ch10-00-generics.md — chapter intro অনুবাদ; সব code block, Listing directive, inline code (`Option<T>`, `Vec<T>`, `HashMap<K, V>`, `Result<T, E>`, `largest`, `i32`, `char`) অপরিবর্তিত; generics, monomorphization, generic, trait, trait bound, lifetime ইত্যাদি technical term English-এ; দাঁড়ি ব্যবহার।
- ch10-01-syntax.md — In Function/Struct/Enum/Method Definitions ও Performance section অনুবাদ; সব rust code block (rust,ignore / does_not_compile সহ), console error output, Listing directive (10-4 থেকে 10-11), inline code অপরিবর্তিত; monomorphization, generic, trait, PartialOrd, blanket implementation, impl block ইত্যাদি term English-এ।
- ch10-02-traits.md — Defining/Implementing Trait, Default Implementation, Trait Bound Syntax, `+` Syntax, `where` Clause, Returning Trait, Conditional Method Implementation সব section অনুবাদ; ৫টি `<!-- Old headings... -->` HTML comment, ৫টি `<a id="...">` anchor, ২টি link reference (`[trait-objects]`, `[methods]`) সব অপরিবর্তিত; সব `impl`, `trait`, `pub`, `for`, `impl Trait`, `Display`, `PartialOrd`, `ToString` keyword ও standard library name English-এ।
- ch10-03-lifetime-syntax.md — Dangling References, Borrow Checker, Generic Lifetimes, Lifetime Annotation Syntax, In Function Signatures, In Struct Definitions, Lifetime Elision (৩টি rule), In Method Definitions, Static Lifetime ও final Generic Type Parameters/Trait Bounds/Lifetimes section সব অনুবাদ; সব rust code block (lifetime `'a`/`'b` annotation সহ ASCII art টীকা অপরিবর্তিত), console error output, Listing directive (10-16 থেকে 10-25 সহ ১টি no-number Listing), ৬টি `<!-- Old headings... -->` HTML comment, ৬টি `<a id="...">` anchor, ৩টি link reference (`[references-and-borrowing]`, `[string-slices-as-parameters]`, `[reference]`) সম্পূর্ণ অপরিবর্তিত; `'a`, `'b`, `'static` সব lifetime syntax English-এ; borrow checker, dangling reference, lifetime, lifetime annotation, lifetime elision rule, input/output lifetime, blanket implementation ইত্যাদি technical term English-এ।
- Structure verification: ৪টি file-এ code fence count (৬, ৩০, ৪২, ৫৪), Listing tag count (৩, ৯, ৪, ১২), anchor count (০, ০, ৫, ৬), HTML comment count (০, ০, ৭, ৮), link reference count (০, ০, ২, ৩) — সব source-এর সাথে exact match।

Stage Summary:
- Files translated: ch10-00-generics.md, ch10-01-syntax.md, ch10-02-traits.md, ch10-03-lifetime-syntax.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: Chapter title "Generic Types, Traits, এবং Lifetimes" রাখা হয়েছে (সব technical term English-এ, শুধু "এবং" Bangla conjunction)। Listing caption text English-এ অপরিবর্তিত রাখা হয়েছে যাতে rendered output-এ কোনো formatting issue না হয় (Task 3-এর convention অনুসরণ করে)। Console error output গুলো (cargo run error) সম্পূর্ণ অপরিবর্তিত কারণ সেগুলো compiler-generated text। Borrow checker diagram-এর ASCII art (Listing 10-17, 10-18) সম্পূর্ণ preserve করা হয়েছে। Lifetime syntax (`'a`, `'b`, `'static`) এবং generic syntax (`<T>`, `<T, U>`) সব অপরিবর্তিত। কোনো special issue নেই।

---
Task ID: 13
Agent: general-purpose (sonnet)
Task: Chapter 12 (An I/O Project: Building a Command Line Program) অনুবাদ

Work Log:
- worklog.md read করলাম — Task 1 (Front matter), Task 4 (Ch03), Task 2 (Ch01), Task 3 (Ch02) আগেই complete হয়েছে।
- _TRANSLATION_GUIDE.md read করে সব নিয়ম (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive ও Markdown structure preserve, দাঁড়ি ব্যবহার, inline code ও code block অপরিবর্তিত) মেনে নিলাম।
- ৭টি source file read করলাম (preprocessed source থেকে): ch12-00 থেকে ch12-06 পর্যন্ত।
- ch12-00-an-io-project.md — chapter intro অনুবাদ; `grep`, `ripgrep`, `stderr`, `stdout`, environment variable ইত্যাদি technical term English-এ; সব `<!-- ignore -->` directive ও `[ch7]`...`[ch18]` link reference অপরিবর্তিত।
- ch12-01-accepting-command-line-arguments.md — `cargo new minigrep`, `std::env::args`, iterator, `collect`, `dbg!`, vector, `args`/`args_os`, `OsString` ইত্যাদি technical term English-এ; সব code block (rust/console) অপরিবর্তিত; `<Listing number="12-1/12-2" ...>` directive ও caption text Bangla-য়; Unicode blockquote preserve; `[ch13]`, `[ch7-idiomatic-use]` link reference অপরিবর্তিত।
- ch12-02-reading-a-file.md — `std::fs`, `fs::read_to_string`, `std::io::Result<String>` ইত্যাদি technical term English-এ; সব code block (rust/text/console) ও Listing directive অপরিবর্তিত; Emily Dickinson poem content text block সম্পূর্ণ অপরিবর্তিত।
- ch12-03-improving-error-handling-and-modularity.md (সবচেয়ে বড় file, 696 line) — refactor/TDD/`Config` struct/`parse_config`/`Config::new`/`Config::build`/`unwrap_or_else`/`process::exit`/`Box<dyn Error>`/`?` operator/trait object/`run` function/library crate/`pub`/`unimplemented!` ইত্যাদি technical term English-এ; ৪টি `<!-- Old headings. Do not remove or links may break. -->` comment ও ৫টি `<a id="...">` anchor (`separation-of-concerns-for-binary-projects`, `returning-a-result-from-new-instead-of-calling-panic`, `calling-confignew-and-handling-errors`, `extracting-logic-from-the-main-function`, `returning-errors-from-the-run-function`) সম্পূর্ণ অপরিবর্তিত; ১০টি Listing directive, ১টি `<span class="filename">` ও সব code block (rust/console) preserve; সব link reference অপরিবর্তিত; internal cross-ref `[#separation-of-concerns-for-binary-projects]` English anchor-এ preserve করা হয়েছে যাতে anchor link কাজ করে।
- ch12-04-testing-the-librarys-functionality.md — TDD/`#[cfg(test)]`/`mod tests`/`use super::*`/`assert_eq!`/`vec!`/lifetime `'a`/`unimplemented!`/`lines` method/`contains` method/`push`/`for` loop ইত্যাদি technical term English-এ; সব code block (rust/console) ও Listing directive অপরিবর্তিত; `<a id="developing-the-librarys-functionality-with-test-driven-development">` anchor preserve; `[ch11-anatomy]`, `[ch10-lifetimes]`, `[ch3-iter]`, `[ch13-iterators]`, `[validating-references-with-lifetimes]` link reference অপরিবর্তিত; `cargo test`, `cargo run` সব command ও terminal output অপরিবর্তিত।
- ch12-05-working-with-environment-variables.md — environment variable/case-insensitive/`search_case_insensitive`/`to_lowercase`/`contains`/shadowing/`String` vs string slice/`Config` struct/`ignore_case` field/`env::var`/`is_ok`/`unwrap`/`expect`/`Result`/`IGNORE_CASE` ইত্যাদি technical term English-এ; সব code block (rust/console) ও Listing directive অপরিবর্তিত; `<a id="writing-a-failing-test-for-the-case-insensitive-search-function">` anchor preserve; `<!-- manual-regeneration ... -->` HTML comment block সম্পূর্ণ অপরিবর্তিত; PowerShell instruction (`$Env:IGNORE_CASE`, `Remove-Item Env:IGNORE_CASE`) ও Linux shell instruction (`IGNORE_CASE=1 cargo run ...`) অপরিবর্তিত।
- ch12-06-writing-to-stderr-instead-of-stdout.md — standard output (`stdout`)/standard error (`stderr`)/`println!`/`eprintln!`/`unwrap_or_else`/`process::exit`/`if let`/redirect ইত্যাদি technical term English-এ; সব code block (rust/text/console) ও Listing directive অপরিবর্তিত; `<a id="writing-error-messages-to-standard-error-instead-of-standard-output">` anchor ও `<!-- Old headings. Do not remove or links may break. -->` comment preserve; `> output.txt` shell redirect syntax অপরিবর্তিত; `<span class="filename">Filename: output.txt</span>` preserve; Summary section অনুবাদ।
- Structure verification: সব ৭টি file-এ code fence count, Listing tag count, anchor count source-এর সাথে exact match করে; সব link reference definition (যেগুলো লাইনের শুরু থেকে শুরু হয় `[id]:`) source-এর সাথে exact match করে; inline `[Chapter N][id]` reference গুলো অপরিবর্তিত।

Stage Summary:
- Files translated: ch12-00-an-io-project.md, ch12-01-accepting-command-line-arguments.md, ch12-02-reading-a-file.md, ch12-03-improving-error-handling-and-modularity.md, ch12-04-testing-the-librarys-functionality.md, ch12-05-working-with-environment-variables.md, ch12-06-writing-to-stderr-instead-of-stdout.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: সব mdBook directive (`<Listing>`, `<span class="filename">`, `<!-- ignore -->`, `<!-- Old headings. Do not remove or links may break. -->`, `<!-- manual-regeneration ... -->`), সব `<a id="...">` explicit anchor, সব code block ও inline code, সব link reference definition source-এর সাথে exact match করে। ch12-03-এ একটি internal cross-reference (`[“Separating Concerns in Binary Projects”](#separation-of-concerns-for-binary-projects)`) এর anchor text টি Bangla-য় অনুবাদ করা হয়েছে (ভেতরের quote text), কিন্তু `(url)` অংশে ASCII anchor `#separation-of-concerns-for-binary-projects` অপরিবর্তিত রাখা হয়েছে যাতে link কাজ করে। সব Chapter reference (`[Chapter 7][ch7]` ইত্যাদি) ও technical term (cargo command, panic message, error message, function/type/method নাম) English-এ রাখা হয়েছে। কোনো special issue নেই।

---
Task ID: 22
Agent: general-purpose (sonnet)
Task: Chapter 21 (Final Project: Web Server) অনুবাদ

Work Log:
- worklog.md read করলাম — Task 1, 2, 3, 4 আগেই complete।
- _TRANSLATION_GUIDE.md read করে সব নিয়ম (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive ও Markdown structure preserve, দাঁড়ি ব্যবহার) মেনে নিলাম।
- ৪টি preprocessed source file read করলাম: ch21-00, ch21-01 (single-threaded), ch21-02 (multithreaded — 1034 lines, দুই ভাগে read), ch21-03 (graceful shutdown)।
- ch21-00-final-project-a-web-server.md — chapter intro, project plan (TCP/HTTP listen, parse, response, thread pool), Figure 21-1 ও `<img>` tag অপরিবর্তিত, `<span class="caption">` text Bangla-য়, async/await/crates.io/systems programming language ইত্যাদি term English-এ।
- ch21-01-single-threaded.md — TCP/HTTP/HTTP request-response/CRLF/URI/URL/status line/headers/body ইত্যাদি technical term English-এ; সব code block (rust, console, text, html), `<Listing>` directive (caption গুলো English-এ রাখা হয়েছে যাতে rendered output-এ formatting নষ্ট না হয়), `<span class="filename">`, `<kbd>ctrl</kbd>-<kbd>C</kbd>` tag, manual-regeneration comment block, `<!-- Old headings -->` comment ও `<a id="...">` anchor সব preserve; `cargo new`/`cargo run`/`cargo check` command ও Cargo output অপরিবর্তিত।
- ch21-02-multithreaded.md — `thread::spawn`/`JoinHandle`/`ThreadPool`/`Worker`/`mpsc`/`channel`/`Arc`/`Mutex`/`FnOnce`/`Send`/`'static`/`Option::take`/`Vec::drain`/`BufReader`/poisoned mutex ইত্যাদি term English-এ; সব 16টি `<Listing>` directive, 7টি anchor, 6টি Old-headings comment, 1টি manual-regeneration comment, 3টি `> Note:` blockquote, console output (compile error সহ) সব অপরিবর্তিত; reference link definition (`[type-aliases]`, `[integer-types]`, `[moving-out-of-closures]`, `[builder]`, `[builder-spawn]`) সব অপরিবর্তিত — source-এ থাকা একটি pre-existing broken markdown link (`]oving-out-of-closures]` যেটাতে `[m` missing) source-এর মতোই preserve করা হয়েছে, কোনো fix করা হয়নি যাতে source fidelity থাকে।
- ch21-03-graceful-shutdown-and-cleanup.md — graceful shutdown/`Drop`/`join`/`Option<thread::JoinHandle<()>>`/poisoned mutex/double panic/`Iterator::take` ইত্যাদি term English-এ; সব 7টি `<Listing>` directive, manual-regeneration comment, console output সব অপরিবর্তিত; final complete code listing (main.rs ও lib.rs) সম্পূর্ণ অপরিবর্তিত; "Well done! You've made it to the end of the book!" summary অনুবাদ করা হয়েছে।
- Structure verification: code fence count, Listing count, anchor count, img count, manual-regen count, Old-headings comment count — সব source-এর সাথে exact match করে (0/30/50/18 fences; 0/9/16/7 Listings; 0/3/7/0 anchors; 1/0/0/0 img; 0/1/1/1 manual-regen; 0/2/6/0 Old-headings)।

Stage Summary:
- Files translated: ch21-00-final-project-a-web-server.md, ch21-01-single-threaded.md, ch21-02-multithreaded.md, ch21-03-graceful-shutdown-and-cleanup.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: সব Listing caption গুলো English-এ রাখা হয়েছে (ch02 task-এর সিদ্ধান্তের সাথে consistency), কারণ caption-এ Bangla থাকলে rendered mdBook output-এ formatting issue হতে পারে। heading গুলোর মধ্যে technical term (যেমন "Drop", "ThreadPool", "Worker") English-এ রাখা হয়েছে। বেশিরভাগ heading Bangla-য় (যেমন "TCP Connection শোনা", "Request পড়া", "একটি Response লেখা")। `<img>` tag-এর `alt` attribute source-এর সাথে exact অপরিবর্তিত রাখা হয়েছে। ch21-02 source-এ একটি pre-existing broken markdown link reference ছিল (`[“...”]oving-out-of-closures]`) যেটা source-এর মতোই preserve করা হয়েছে — source-এর pre-existing bug fix করা হয়নি যাতে source fidelity থাকে। Chapter title গুলো mixed English+Bangla: "Final Project: একটি Multithreaded Web Server তৈরি করা", "একটি Single-Threaded Web Server তৈরি করা", "Single-Threaded থেকে Multithreaded Server-এ", "Graceful Shutdown এবং Cleanup"। কোনো নতুন explicit anchor যোগ করার দরকার হয়নি কারণ সব `<a id="...">` source-এ থাকা anchor ই অপরিবর্তিত preserve করা হয়েছে।

---
Task ID: 16
Agent: general-purpose (opus)
Task: Chapter 15 (Smart Pointers) অনুবাদ

Work Log:
- worklog.md ও _TRANSLATION_GUIDE.md read করা হয়েছে — Tasks 1, 2, 3, 4 ইতিমধ্যে complete।
- ৭টি source file read করা হয়েছে preprocessed source থেকে: ch15-00 (intro), ch15-01 (Box), ch15-02 (Deref), ch15-03 (Drop), ch15-04 (Rc), ch15-05 (RefCell/interior mutability), ch15-06 (reference cycles/Weak)।
- সব file চলিত ভাষায় অনুবাদ করা হয়েছে — smart pointer chapter এর tutorial-tone maintain করে দাঁড়ি ব্যবহার।
- সব code block (rust, rust,ignore,does_not_compile, rust,ignore,panics, rust,noplayground, console, text), inline code, Rust keyword, std-lib type/macro নাম অপরিবর্তিত রাখা হয়েছে।
- Technical term গুলো English-এ রাখা হয়েছে: smart pointer, Box, Box<T>, dereference, dereference operator, Deref, DerefMut, Drop, drop, Rc, Rc<T>, RefCell, RefCell<T>, Ref, RefMut, RefMut<T>, Ref<T>, interior mutability, reference cycle, weak reference, Weak<T>, strong_count, weak_count, trait object, ownership, borrowing, borrow checker, heap, stack, recursive type, cons list, prelude, mock object, test double, destructor, constructor, deep copy, multithreaded, single-threaded, memory leak, Mutex — ইত্যাদি।
- সব Markdown structure (heading, list, table, blockquote), সব `<Listing number="15-XX" ...>` directive, `<a id="...">` anchor (Old headings comment সহ), `<!-- manual-regeneration ... -->` comment block, `<!-- ignore -->` directive, `<span class="filename">`, `<span class="caption">`, `<img ...>` tag সম্পূর্ণ preserve করা হয়েছে।
- সব reference link definition (`[trait-objects]:`, `[impl-trait]:`, `[tuple-structs]:`, `[preventing-ref-cycles]:`, `[wheres-the---operator]:`, `[nomicon]:`) অপরিবর্তিত রাখা হয়েছে।
- Figure 15-1 থেকে 15-4 পর্যন্ত সব diagram ও caption Bangla-য় অনুবাদ করা হয়েছে, image src ও alt attribute অপরিবর্তিত (যেমন Figure 15-1-এর alt text-এর "infinity symbol" ইত্যাদি বর্ণনামূলক অংশ English-এই রাখা হয়েছে যাতে accessibility/SEO-তে পরিবর্তন না হয়)।
- Structure verification: code fence count, Listing tag count, anchor tag count সব file-এর জন্য source-এর সাথে exact match করে (ch15-00: 0/0/0, ch15-01: 16/5/3, ch15-02: 22/8/8, ch15-03: 12/3/1, ch15-04: 10/3/2, ch15-05: 20/5/6, ch15-06: 20/5/2)।
- Listing caption text-গুলো English-এই রাখা হয়েছে (Task 3 এর convention অনুসরণ করে) যাতে rendered output-এ কোনো formatting issue না হয়।
- Heading গুলো Bangla-তে অনুবাদ করা হয়েছে, কিন্তু heading-এ থাকা code/keyword (`Box<T>`, `Drop`, `Deref`, `Rc<T>`, `RefCell<T>`, `Weak<T>`, `strong_count`, `weak_count`) English-এ রাখা হয়েছে।

Stage Summary:
- Files translated: ch15-00-smart-pointers.md, ch15-01-box.md, ch15-02-deref.md, ch15-03-drop.md, ch15-04-rc.md, ch15-05-interior-mutability.md, ch15-06-reference-cycles.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: কোনো special issue নেই। সব structural element (code fence, Listing tag, anchor tag, mdBook directive, HTML comment block) source-এর সাথে exact match করে। Smart pointer chapter-এর technical term গুলো (Box, Rc, RefCell, Deref, DerefMut, Drop, Weak, interior mutability, reference cycle ইত্যাদি) guide-এর glossary অনুযায়ী English-এ রাখা হয়েছে। "cons list" ও "trait object" জাতীয় technical term ও English-এ রাখা হয়েছে। Chapter title গুলো heading-এ Bangla+English mixed ভাবে রাখা হয়েছে (যেমন "## `Box<T>` ব্যবহার করে Heap-এ Data Point করা", "## `Rc<T>`, Reference-Counted Smart Pointer", "### `Weak<T>` ব্যবহার করে Reference Cycle প্রতিরোধ করা")।

---
Task ID: 12
Agent: general-purpose (sonnet)
Task: Chapter 11 (Writing Automated Tests) অনুবাদ

Work Log:
- worklog.md read করলাম — Task 1, 2, 3, 4 আগেই complete হয়েছে।
- _TRANSLATION_GUIDE.md read করে সব নিয়ম (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive ও Markdown structure preserve, দাঁড়ি ব্যবহার) মেনে নিলাম।
- ৪টি source file read করলাম preprocessed source থেকে: ch11-00-testing.md (34 lines), ch11-01-writing-tests.md (1014 lines), ch11-02-running-tests.md (371 lines), ch11-03-test-organization.md (370 lines)।
- ch11-00-testing.md — chapter intro অনুবাদ; Dijkstra quote-এর program testing/bug term English-এ; correctness/type system/borrow checking/assert/test/parameter ইত্যাদি technical term English-এ রাখা হয়েছে; একমাত্র H1 heading "Writing Automated Tests" English-এ রাখা হয়েছে।
- ch11-01-writing-tests.md — Test function structure, `#[test]` attribute, `assert!`/`assert_eq!`/`assert_ne!` macro, custom failure message, `should_panic` attribute (with `expected` parameter), `Result<T, E>` test সব অনুবাদ; সব `rust`/`console`/`text` code block (62 fence pair) সম্পূর্ণ অপরিবর্তিত; সব `<Listing number="11-X" ...>` directive (9টি), `<!-- Old headings. Do not remove or links may break. -->` HTML comment (3টি), `<a id="...">` anchor (3টি), `<!-- manual-regeneration ... -->` comment (2টি), `<span class="filename">` tag, `<!-- ignore -->` directive (6টি) ও ৮টি link reference definition (`[concatenating]`, `[bench]`, `[ignoring]`, `[subset]`, `[controlling-how-tests-are-run]`, `[derivable-traits]`, `[doc-comments]`, `[paths-for-referring-to-an-item-in-the-module-tree]`) অপরিবর্তিত রাখা হয়েছে। Heading text Bangla-তে, কিন্তু heading-এ থাকা code/keyword (`assert!`, `assert_eq!`, `assert_ne!`, `should_panic`, `Result<T, E>`) English-এ। শুরুতে একটি typo "finishing" → "finished" সব 14টি test output লাইনে fix করা হয়েছে (replace_all দিয়ে) যাতে code block source-এর সাথে exact match করে।
- ch11-02-running-tests.md — `cargo test` কমান্ড, `--test-threads`, `--show-output`, `--ignored`, `--include-ignored` flag সব English-এ; parallel/consecutive test, function output capture, subset test, ignoring test সব অনুবাদ; সব code block (24 fence pair), H3 heading (4), H4 heading (2), `<a id="ignoring-some-tests-unless-specifically-requested">` anchor, 2টি `<Listing>` directive, 1টি `[tests]` link reference, `<!-- Old headings ... -->` HTML comment সব preserve।
- ch11-03-test-organization.md — Unit test ও Integration test-এর পার্থক্য, `#[cfg(test)]` annotation, `cfg`/`test` configuration, private function test, _tests_ ডিরেক্টরি, integration test submodule (_tests/common/mod.rs_ convention), binary crate integration test সব অনুবাদ; সব code block (20 fence pair), H3 (2), H4 (5), `<a id="testing-private-functions">` anchor, 2টি `<Listing>` directive, 3টি link reference definition (`[paths]`, `[separating-modules-into-files]`, `[alt-paths]`), `<!-- Old headings ... -->` HTML comment সব preserve। Listing caption ও `<!-- ignore -->` directive অপরিবর্তিত। একটি test output লাইনে "finishing" → "finished" typo fix করা হয়েছে।
- Structure verification: সব ৪টি file-এর জন্য code fence pair count, heading count (H2/H3/H4), `<a id=>` count, `<Listing>` count, link reference count, `<!-- Old headings -->` count, `<!-- manual-regeneration -->` count, `<!-- ignore -->` count source-এর সাথে exact match করে।

Stage Summary:
- Files translated: ch11-00-testing.md, ch11-01-writing-tests.md, ch11-02-running-tests.md, ch11-03-test-organization.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: Heading text Bangla-তে অনুবাদ করা হয়েছে কিন্তু heading-এ থাকা code/keyword English-এ রাখা হয়েছে (যেমন "### `assert!` দিয়ে Result যাচাই করা")। Chapter H1 "Writing Automated Tests" ও প্রতিটি file-এর H2 section heading-এর English title অপরিবর্তিত রাখা হয়েছে canonical chapter name ও cross-reference consistency-র জন্য। Test, unit test, integration test, attribute, module, crate, library, binary crate, public API, private function, panic, thread, scope, compile, run, pass, fail, ignored, filtered, measured, configuration ইত্যাদি technical term English-এ রাখা হয়েছে। সব cargo command (`cargo test`, `cargo test -- --test-threads=1`, `cargo test -- --show-output`, `cargo test one_hundred`, `cargo test add`, `cargo test -- --ignored`, `cargo test -- --include-ignored`, `cargo test --test integration_test`, `cargo new adder --lib`) অপরিবর্তিত। কোনো special issue নেই।

---
Task ID: 21
Agent: general-purpose (opus)
Task: Chapter 20 (Advanced Features) অনুবাদ

Work Log:
- worklog.md ও _TRANSLATION_GUIDE.md read করলাম — Task 1, 2, 3, 4 আগেই complete হয়েছে।
- Preprocessed source folder `/home/z/my-project/rust-book-source-preprocessed/src/` থেকে assigned ৬টি file read করলাম: ch20-00 (intro, 22 lines), ch20-01-unsafe-rust (717 lines), ch20-02-advanced-traits (691 lines), ch20-03-advanced-types (368 lines), ch20-04-advanced-functions-and-closures (240 lines), ch20-05-macros (591 lines)।
- সব file চলিত ভাষায় অনুবাদ করলাম — tutorial tone, দাঁড়ি ব্যবহার, reader-কে "তুমি" হিসেবে address।
- সব code block (rust, rust,noplayground, rust,ignore, rust,ignore,does_not_compile, console, text, toml), inline code, Rust keyword, standard library type/macro name অপরিবর্তিত রাখা হয়েছে।
- সব mdBook directive ও structural element preserve করা হয়েছে: `<Listing ...>` tag (caption attribute অপরিবর্তিত রাখা হয়েছে যাতে rendered output formatting consistent থাকে), `<a id="...">` anchor, `<!-- Old headings. Do not remove or links may break. -->` HTML comment, `<!-- ignore -->` inline directive, blockquote `> Note:` syntax, এবং bottom-এর reference link definition-গুলো।
- Technical terms English-এ রাখা হয়েছে: unsafe, raw pointer, dereference, dereference operator, borrow checker, memory safety, static analysis, unsafe superpower, dangling pointer, data race, undefined behavior, trait, associated type, default type parameter, fully qualified syntax, supertrait, newtype pattern, type alias, never type, empty type, diverging function, dynamically sized type (DST), Sized trait, function pointer, closure trait, opaque type, trait object, declarative macro, procedural macro, macro_rules!, derive, attribute-like macro, function-like macro, metaprogramming, TokenStream, Mangling, FFI, ABI, Miri, Send, Sync, ইত্যাদি। Macro syntax (`macro_rules!`, `$x:expr`, `$()`, `*`, `$( $x:expr ),*`) সম্পূর্ণ অপরিবর্তিত।
- ch20-01-unsafe-rust: ৫টি unsafe superpower (Dereference raw pointer, Call unsafe function/method, Access/modify mutable static variable, Implement unsafe trait, Access fields of union), safe abstraction (`split_at_mut`), `extern`/FFI/ABI, mutable static `COUNTER`, SAFETY comment convention, Miri dynamic analysis tool সব cover করা হয়েছে; `&raw const`/`&raw mut` raw borrow operator, `safe` keyword in `unsafe extern`, `#[unsafe(no_mangle)]` সব English-এ।
- ch20-02-advanced-traits: Associated type (`Iterator` trait-এর `Item`), default generic type parameter (`Add<Rhs=Self>`), operator overloading, fully qualified syntax (`<Dog as Animal>::baby_name()`), supertrait (`OutlinePrint: fmt::Display`), newtype pattern (`Wrapper(Vec<String>)`) সব cover; orphan rule, trait bound, `Deref` reference সব preserve।
- ch20-03-advanced-types: newtype pattern, type alias (`type Kilometers = i32`, `type Thunk`, `std::io::Result<T>`), never type `!` (diverging function, `continue`, `panic!`, `loop`), dynamically sized type (`str`, DST), `Sized` trait ও `?Sized` syntax সব cover।
- ch20-04-advanced-functions-and-closures: function pointer `fn` type vs `Fn` trait, `impl Fn` syntax, `Box<dyn Fn>` trait object, opaque type error (`E0308`) সব cover।
- ch20-05-macros: declarative macro (`macro_rules! vec { ... }`), `#[macro_export]`, pattern syntax ব্যাখ্যা (`$x:expr`, `$()*`), procedural macro (custom `#[derive]`, attribute-like `#[proc_macro_attribute]`, function-like `#[proc_macro]`), `hello_macro`/`hello_macro_derive` crate structure, `syn`/`quote`/`proc_macro` crate, `DeriveInput`, `quote!`/`stringify!` macro সব cover।
- Structure verification করা হয়েছে — code block fence count source-এর সাথে exact match (ch20-01: 34, ch20-02: 46, ch20-03: 34, ch20-04: 16, ch20-05: 36); Listing tag count match (12/15/3/7/9); anchor count match (2/8/2/0/2); `<!-- ignore -->` occurrence count match (6 in ch20-05); reference link definition count match (10/5/5/5/7)।

Stage Summary:
- Files translated: ch20-00-advanced-features.md, ch20-01-unsafe-rust.md, ch20-02-advanced-traits.md, ch20-03-advanced-types.md, ch20-04-advanced-functions-and-closures.md, ch20-05-macros.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: সব code block, Listing tag (caption সহ), anchor, HTML comment (`<!-- Old headings -->` ও `<!-- ignore -->`), reference link definition source-এর সাথে exact match করে। Heading-গুলো চলিত ভাষায় অনুবাদ করা হয়েছে কিন্তু heading-এর ভেতরের code/keyword (`## Unsafe Rust`, `## Advanced Traits`, `## Advanced Types`, `## Advanced Functions and Closures`, `## Macros`, `## Summary`, `### Calling an Unsafe Function or Method`, `### Implementing an Unsafe Trait`, `### Accessing Fields of a Union`, `### Using Miri to Check Unsafe Code`, `### Defining Traits with Associated Types`, `### Using Default Generic Parameters and Operator Overloading`, `### Custom \`derive\` Macros`, ইত্যাদি) English-এ রাখা হয়েছে। Listing caption attribute-এর text অপরিবর্তিত রাখা হয়েছে rendered output-এ formatting consistency-র জন্য। ch20-05-macros-এ একটি paragraph-এ দুটি `<!-- ignore -->` directive একই লাইনে merge হওয়ায় HTML comment line-count ছোট দেখাচ্ছে কিন্তু occurrence সংখ্যা source-এর সাথে exact match করে (৬টা)। কোনো special issue নেই।

---
Task ID: 18
Agent: general-purpose (opus)
Task: Chapter 17 (Async and Await) অনুবাদ

Work Log:
- worklog.md read করলাম — Task 1, 2, 3, 4 আগেই complete হয়েছে।
- _TRANSLATION_GUIDE.md read করে সব নিয়ম (চলিত ভাষা, code/keyword/technical term English-এ, mdBook directive ও Markdown structure preserve, দাঁড়ি ব্যবহার) মেনে নিলাম।
- PREPROCESSED source folder থেকে ৭টি file read করলাম: ch17-00 (intro/parallelism vs concurrency), ch17-01 (futures/async syntax/first program/page_title), ch17-02 (spawn_task/join/message passing/join! macro/move), ch17-03 (yield_now/timeout/building abstractions), ch17-04 (streams/StreamExt), ch17-05 (Future trait/Pin/Unpin/Stream trait deep dive), ch17-06 (futures vs tasks vs threads + Summary)।
- সব Heading text চলিত ভাষায় অনুবাদ করলাম; heading-এ থাকা code/keyword (`Future`, `Stream`, `Pin`, `Unpin`, `spawn_task`, `join!` macro) English-এ রাখলাম।
- Technical term সব English-এ: future, Future, async, await, poll, polling, runtime, executor, task, spawn, spawn_task, stream, Stream, StreamExt, Pin, Unpin, !Unpin, pin, pin!, Waker (implied via Context), Context, Poll, Ready, Pending, Either, Left, Right, lazy, blocking, non-blocking, CPU-bound, I/O-bound, compute-bound, parallelism, concurrency, cooperative multitasking, work stealing, self-referential, trait object, marker trait, etc.
- সব code block (rust, console, text), inline code, mdBook include directive (নেই — preprocessed source এ embedded), manual-regeneration comment, `<Listing>` tag ও attribute (number/file-name/caption সম্পূর্ণ অপরিবর্তিত), `<span class="filename">`, `<a id="...">` anchor, `<figure>`/`<img>`/`<figcaption>` tag ও ভেতরের alt text, `<kbd>` tag, `<!-- ignore -->` directive, `<!-- Old headings. Do not remove or links may break. -->` comment, `<!-- should_panic,noplayground ... -->` comment, `<!-- We cannot test ... -->` comment, `<!-- Not extracting output ... -->` multiline comment, `<!-- TODO: ... -->` comment, `<!-- The inline <code> in the next block ... -->` comment, সব reference link definition `[name]: path` — সম্পূর্ণ অপরিবর্তিত রাখা হয়েছে।
- Figure caption (Figure 17-1 থেকে 17-9) ও Listing caption গুলো English-এ রাখা হয়েছে যাতে rendered output-এ কোনো formatting issue না হয় (Task 3-এর decision অনুসারে)।
- "Note:" blockquote syntax `> Note:` হিসেবে preserve করা হয়েছে, ভেতরের text চলিত ভাষায়।
- Structure verification প্রতিটি file-এর জন্য: code fence count, Listing tag count, anchor count, figure count, manual-regeneration count — সব source-এর সাথে exact match করে (চেক করা হয়েছে)।
- দুটি ছোট typo/encoding glitch ঠিক করা হয়েছে: ch17-01-এ "পারতাম" শব্দে একটি broken Unicode char ছিল, ch17-06-এ "বাস্তবsituation" accidentally English+Bangla mix ছিল — দুটোই ঠিক করেছি।

Stage Summary:
- Files translated: ch17-00-async-await.md, ch17-01-futures-and-syntax.md, ch17-02-concurrency-with-async.md, ch17-03-more-futures.md, ch17-04-streams.md, ch17-05-traits-for-async.md, ch17-06-futures-tasks-threads.md
- Output path: /home/z/my-project/rust-book-bn/
- Notes: Chapter-এর heading গুলো চলিত ভাষায় অনুবাদ করা হয়েছে কিন্তু heading-এ থাকা সব code/keyword/trait নাম English-এ রাখা হয়েছে। Figure caption (17-1 থেকে 17-9) ও Listing caption গুলো English-এ রাখা হয়েছে rendered output consistency-র জন্য (Task 3-এর decision অনুসারে)। Listing caption-এ বর্ণিত file-name "src/main.rs" অপরিবর্তিত। ch17-05-এ `Pin` ও `Unpin` নিয়ে ব্যাখ্যার সময় "self-referential", "marker trait", "trait object" ইত্যাদি term English-ে রাখা হয়েছে। ch17-04-এ "Streams: Futures in Sequence" heading-এর অনুবাদ "Streams: Sequence-এ Future" করা হয়েছে যাতে Stream ও Future term English-এ থাকে। Section-এর পুরোনো anchor সব অপরিবর্তিত (concurrency-with-async, counting, message-passing, counting-up-on-two-tasks-using-message-passing, streams, yielding, digging-into-the-traits-for-async, future, pinning-and-the-pin-and-unpin-traits, the-pin-and-unpin-traits)। কোনো নতুন anchor যোগ করার প্রয়োজন হয়নি কারণ সব cross-reference হুবহু preserve করা হয়েছে।

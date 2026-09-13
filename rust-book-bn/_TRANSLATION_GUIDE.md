# Rust Book Bangla Translation — Shared Guide

সব translation agent **অবশ্যই** এই guide মেনে চলবেন।

## ১. উদ্দেশ্য
Rust Programming Language Book (rust-lang/book) এর English `.md` files গুলো Bangla (চলিত ভাষা) তে অনুবাদ করা।

## ২. Source ও Output
- **Source (PREPROCESSED — code embedded):** `/home/z/my-project/rust-book-source-preprocessed/src/<filename>.md`
  - ⚠️ এই folder-টা ব্যবহার করবে। এতে `{{#include ...}}` directive গুলো ইতিমধ্যে actual code দিয়ে replace করা আছে।
  - **`/home/z/my-project/rust-book-source/src/` ব্যবহার করবে না** — ওই folder-এ directive unresolved আছে।
- **Output:** `/home/z/my-project/rust-book-bn/<filename>.md` (একই filename, শুধু ভিন্ন folder)

## ৩. Translation নিয়মাবলী (STRICT)

### ৩.১ ভাষা
- **চলিত ভাষা** ব্যবহার করো (আমি/তুমি/সে রূপ)। সাধু ভাষা নয়।
- বাক্য স্বাভাবিক ও সাবলীল হবে — word-by-word অনুবাদ নয়, meaning-based।
- Tutorial-style address থাকলে (যেমন "we will build...") — "আমরা বানাবো..." এভাবে করো।
- Reader-কে address করলে "তুমি" ব্যবহার করো (informal, tutorial-friendly)।

### ৩.২ যা অপরিবর্তিত থাকবে (কখনো translate করবে না)
1. **সব code block** (```rust ... ``` সহ যেকোনো language) — ভেতরের code, comments, strings কিছুই translate করবে না।
2. **Inline code** (`code`) — যেমন `fn main()`, `String`, `Vec<T>`।
3. **Rust keywords** — fn, let, mut, struct, enum, impl, trait, pub, use, mod, match, if, else, loop, while, for, return, async, await, move, ref, self, Self, crate, super, where, dyn, unsafe, const, static, type, ইত্যাদি।
4. **Standard library type ও macro নাম** — Vec, String, HashMap, Option, Result, Box, Rc, Arc, RefCell, Mutex, println!, vec!, dbg!, assert!, ইত্যাদি।
5. **Rust-specific technical terms** (নিচের glossary দেখো)।
6. **URL, link, file path, command** — যেমন `cargo build`, `rustup`, `https://...`।
7. **mdBook-specific syntax** — `{{#rustdoc_include ...}}`, `{{#include ...}}`, `{{#rustdoc_include ...}}`, anchor links।
8. **Markdown structure** — heading level, list, table, blockquote — সব preserve করো।
9. **Image/figure reference** — `![alt](path)` অপরিবর্তিত রাখো, শুধু alt text translate করতে পারো।
10. **Ferris diagram reference** ও অন্যান্য include directive।

### ৩.৩ Glossary — এই terms গুলো English-এ রাখবে (translate করবে না)
ownership, borrowing, borrow, borrow checker, lifetime, trait, struct, enum, variant, module, crate, package, workspace, generic, generics, monomorphization, closure, iterator, adaptor, consumer, smart pointer, reference, move, copy, clone, deref, dereference, drop, panic, unwrap, expect, slice, pattern, pattern matching, refutability, refutable, irrefutable, shadowing, shadow, mutable, immutable, mutability, scope, ownership, heap, stack, data race, thread, concurrency, async, await, future, stream, task, executor, macro, declarative macro, procedural macro, trait object, dynamically sized type (DST), object safe, associated type, associated function, method, field, implementation, visibility, privacy, prelude, lint, edition, cargo, rustc, rustup, crates.io, dispatch, static dispatch, dynamic dispatch, vtable, interior mutability, reference cycle, Send, Sync, unsafe, raw pointer, dangling pointer, null, overflow, arithmetic overflow, ইত্যাদি।

**নিয়ম:** যদি কোনো term নিয়ে confusion থাকে, English-ই রাখো। বাংলা অর্থ শুধু প্রথমবার bracket-এ দিতে পারো যেমন: "ownership (মালিকানা)" — কিন্তু এটাও optional।

### ৩.৪ যা Bangla-তে হবে
- সব বর্ণনামূলক লেখা (paragraph)।
- Heading text — কিন্তু heading-এ কোনো code/keyword থাকলে সেটা English-এ থাকবে (যেমন: "## References এবং Borrowing")।
- Table-এর text cell (code cell অপরিবর্তিত)।
- Blockquote-এর explanation text।
- "Note", "Tip", "Warning" label — "নোট", "টিপস", "সতর্কতা" তে পারো, কিন্তু mdBook এর `> Note:` syntax preserve করো।

### ৩.৫ যতিচিহ্ন
- বাক্যের শেষে দাঁড়ি (।) ব্যবহার করো।
- কমা (,) ব্যবহার করো।
- Quote-এর ভেতর English থাকলে English punctuation রাখো, Bangla থাকলে Bangla punctuation।
- কোনো ASCII art বা diagram থাকলে সেটা অপরিবর্তিত রাখো।

## ৪. কাজের প্রবাহ
1. `/home/z/my-project/worklog.md` read করো (previous agents কী করেছে জানতে)।
2. `/home/z/my-project/rust-book-bn/_TRANSLATION_GUIDE.md` (এই file) read করো।
3. Assigned source `.md` file(s) read করো `/home/z/my-project/rust-book-source/src/` থেকে।
4. অনুবাদ করো ও `/home/z/my-project/rust-book-bn/` এ same filename দিয়ে save করো।
5. `/home/z/my-project/worklog.md` এ নিজের work log append করো (template নিচে)।

## ৫. Worklog entry template
```markdown
---
Task ID: <তোমার Task ID>
Agent: general-purpose (<model alias>)
Task: <কোন chapter/files translate করেছ>

Work Log:
- <step 1>
- <step 2>

Stage Summary:
- Files translated: <list>
- Output path: <path>
- Notes: <যদি কোনো সমস্যা বা special decision থাকে>
```

## ৬. Quality checklist (save করার আগে যাচাই করো)
- [ ] সব code block অপরিবর্তিত?
- [ ] সব inline code অপরিবর্তিত?
- [ ] সব Markdown structure (heading, list, table) preserve করা?
- [ ] mdBook include directive (`{{#...}}`) অপরিবর্তিত?
- [ ] Technical terms English-এ আছে?
- [ ] চলিত ভাষা ব্যবহৃত?
- [ ] দাঁড়ি (।) ব্যবহৃত?
- [ ] কোনো heading বা section missing নেই?

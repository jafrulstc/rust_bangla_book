# The Rust Programming Language — বাংলা অনুবাদ

[Rust Book][rust-book] (rust-lang/book) এর সম্পূর্ণ বাংলা অনুবাদ।

## অনুবাদের বৈশিষ্ট্য

- **ভাষা:** চলিত ভাষা (আমি/তুমি রূপ)
- **Technical terms:** English-এ রাখা হয়েছে (ownership, trait, struct, lifetime, ইত্যাদি)
- **Code block:** সম্পূর্ণ অপরিবর্তিত (Rust keyword, comment, string সব ইংরেজিতে)
- **Markdown structure:** preserve করা হয়েছে (heading, list, table, mdBook directive)
- **mdBook directive:** `<Listing>`, `<a id="...">`, `<!-- ignore -->` ইত্যাদি অপরিবর্তিত

## Project structure

```
rust_bangla_book/
├── rust-book-bn/          # চূড়ান্ত বাংলা অনুবাদ (১১২টা .md file)
│   ├── _TRANSLATION_GUIDE.md   # translation guide ও glossary
│   ├── SUMMARY.md
│   ├── title-page.md, foreword.md
│   ├── ch00-00-introduction.md  → ch21-03-...md  (২১টা chapter)
│   └── appendix-00.md → appendix-07.md           (৮টা appendix)
├── preprocess.py          # mdBook {{#include}} directive resolve করার script
├── fix_directives.py      # আগের অনুবাদে বাকি directive fix করার script
└── worklog.md             # প্রতিটা translation agent-এর work log
```

## কীভাবে তৈরি হয়েছে

১. **Source clone:** `rust-lang/book` repository clone করা হয়েছে।
২. **Preprocessing:** mdBook-এর `{{#include ../listings/...}}` directive গুলো actual code content দিয়ে replace করা হয়েছে (`preprocess.py`)। মোট ৭০৭টা directive resolve হয়েছে।
৩. **Translation:** ২৩টা subagent parallel-এ ১১২টা `.md` file অনুবাদ করেছে। প্রতিটা agent `_TRANSLATION_GUIDE.md` মেনে চলেছে যাতে terminology consistency বজায় থাকে।
৪. **Verification:** প্রতিটা agent নিজে code fence count, Listing tag count, anchor count source-এর সাথে match করে verify করেছে।

## mdBook দিয়ে build করা (ঐচ্ছিক)

এই অনুবাদ যেকোনো mdBook-compatible reader দিয়ে পড়া যাবে।

```bash
# mdBook ইনস্টল করুন (যদি না থাকে)
cargo install mdbook

# rust-book-bn/ ফোল্ডারে একটা book.toml যোগ করুন, তারপর:
cd rust-book-bn
mdbook build      # HTML output book/ ফোল্ডারে তৈরি হবে
mdbook serve      # http://localhost:3000 এ live preview
```

## Source

- Original English book: https://github.com/rust-lang/book
- Licensed under MIT (see upstream repo for details)

## Translation status

| অংশ | স্ট্যাটাস |
|------|----------|
| Front matter (title, foreword, intro, SUMMARY) | ✅ সম্পূর্ণ |
| Chapter 1–21 (সব chapter ও subsection) | ✅ সম্পূর্ণ |
| Appendices A–G | ✅ সম্পূর্ণ |
| মোট `.md` file | **১১২/১১২** |

[rust-book]: https://github.com/rust-lang/book

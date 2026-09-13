# Introduction

> নোট: বইটির এই editionটি [No Starch Press][nsp] থেকে print ও ebook ফরম্যাটে পাওয়া
> [The Rust Programming Language][nsprust]-এর মতোই।

[nsprust]: https://nostarch.com/rust-programming-language-3rd-edition
[nsp]: https://nostarch.com/

_The Rust Programming Language_-এ তোমাকে স্বাগতম, Rust সম্পর্কে একটি পরিচিতিমূলক
বই। Rust programming language তোমাকে দ্রুততর, আরও reliable software লিখতে সাহায্য
করে। Programming language design-এ high-level ergonomics এবং low-level control
প্রায়ই একে অপরের বিপরীত; Rust সেই দ্বন্দ্বকে চ্যালেঞ্জ করে। powerful technical
capacity ও দারুণ developer experience-এর মধ্যে ভারসাম্য রক্ষার মাধ্যমে, Rust তোমাকে
low-level বিস্তারিত বিষয়ে (যেমন memory usage) নিয়ন্ত্রণ দেয়, কিন্তু এই নিয়ন্ত্রণের
সাথে প্রথাগতভাবে যুক্ত ঝামেলাগুলো ছাড়াই।

## Rust কাদের জন্য

নানা কারণে Rust অনেক মানুষের কাছেই আদর্শ। চলো সবচেয়ে গুরুত্বপূর্ণ কয়েকটি দলের কথা
দেখি।

### Developer দল

বিভিন্ন মাত্রার systems programming জ্ঞানসম্পন্ন developer-দের বড় দলের মধ্যে
collaborate করতে Rust একটি productive tool হিসেবে প্রমাণিত হচ্ছে। Low-level code-এ
প্রায়ই নানা সূক্ষ্ম bug থাকে, যা অন্য বেশিরভাগ ভাষায় শুধু ব্যাপক testing ও অভিজ্ঞ
developer-দের সূক্ষ্ম code review-এর মাধ্যমেই ধরা যায়। Rust-এ compiler একটি
gatekeeper-এর ভূমিকা পালন করে—এই ধরনের এড়িয়ে যাওয়া bug, এমনকি concurrency bug-সহ,
থাকলে সেই code compile করতে অস্বীকার করে। compiler-এর পাশাপাশি কাজ করে দলটি
program-এর logic-এ focus করতে পারে, bug-এর পেছনে ছুটতে নয়।

Rust systems programming দুনিয়ায় আধুনিক developer tools-ও নিয়ে আসে:

- Cargo, বিল্ট-in dependency manager ও build tool, Rust ecosystem-জুড়ে dependencies
  যোগ করা, compile করা ও পরিচালনা করাকে painless এবং consistent করে তোলে।
- `rustfmt` formatting tool developer-দের মধ্যে একটি consistent coding style নিশ্চিত
  করে।
- Rust Language Server integrated development environment (IDE) integration-কে power
  দেয় code completion ও inline error message-এর জন্য।

Rust ecosystem-এর এই ও অন্যান্য tools ব্যবহার করে developer-রা systems-level code
লেখার সময়ও productive থাকতে পারে।

### Students

Rust students এবং যারা systems concepts সম্পর্কে জানতে আগ্রহী তাদের জন্য। Rust
ব্যবহার করে অনেকেই operating systems development-এর মতো topic শিখেছে। community
খুবই welcoming এবং students-দের প্রশ্নের উত্তর দিতে আনন্দিত। এই বইয়ের মতো
প্রচেষ্টার মাধ্যমে Rust teams systems concepts-কে আরও বেশি মানুষের কাছে—বিশেষ করে
যারা programming-এ নতুন—তাদের কাছে accessible করতে চায়।

### Companies

বড় ও ছোট শত শত company বিভিন্ন কাজের জন্য production-এ Rust ব্যবহার করে, যার মধ্যে
পড়ে command line tools, web services, DevOps tooling, embedded devices, audio ও
video analysis এবং transcoding, cryptocurrencies, bioinformatics, search engines,
Internet of Things applications, machine learning, এবং এমনকি Firefox web browser-এর
বড় অংশ।

### Open Source Developer

Rust তাদের জন্য যারা Rust programming language, community, developer tools ও
library গুলো বানাতে চায়। আমরা আনন্দের সাথে তোমাকে Rust language-এ contribute করতে
আমন্ত্রণ জানাই।

### যারা Speed ও Stability-কে গুরুত্ব দেয়

Rust তাদের জন্য যারা একটি ভাষায় speed ও stability চায়। speed বলতে আমরা বুঝি Rust
code কত দ্রুত চলতে পারে, এবং Rust তোমাকে কত দ্রুত program লেখাতে দেয়। Rust
compiler-এর check গুলো feature addition ও refactoring-এর মধ্য দিয়ে stability নিশ্চিত
করে। এটি এমন সেই brittle legacy code-এর বিপরীত, যা এই check গুলো ছাড়া ভাষায় লেখা
এবং যা modify করতে developer-রা প্রায়ই ভয় পায়। zero-cost abstractions—এমন
higher-level features যা manually লেখা code-এর মতো fast lower-level code-এ compile
হয়—সেই লক্ষ্যে Rust চেষ্টা করে যেন safe code একই সাথে fast code-ও হয়।

Rust language আরও অনেক user-কে support করার আশা করে; এখানে উল্লেখিত গুলো শুধু
কয়েকটি বৃহত্তম stakeholder। সব মিলিয়ে, Rust-এর সবচেয়ে বড় ambition হলো সেই
trade-offs দূর করা, যা programmer-রা কয় দশক ধরে মেনে নিয়েছে—safety _ও_
productivity, speed _ও_ ergonomics—একসাথে দেওয়ার মাধ্যমে। Rust একবার ট্রাই করে দেখো,
এবং দেখো এর পছন্দগুলো তোমার কাছে কাজ করে কিনা।

## এই বইটি কাদের জন্য

এই বইটি ধরে নেয় যে তুমি অন্য কোনো programming language-এ code লিখেছ, কিন্তু কোনটিতে
তা নিয়ে কোনো assumption করে না। আমরা বিভিন্ন programming background থেকে আসা
পাঠকদের জন্য material গুলো ব্যাপকভাবে accessible করার চেষ্টা করেছি। programming
কী _তা_ নিয়ে বা কীভাবে তার কথা ভাবতে হয়—এ নিয়ে আমরা বেশি সময় নষ্ট করি না। যদি
তুমি programming-এ সম্পূর্ণ নতুন হও, তাহলে programming-এর পরিচিতি দেয় এমন একটি
বই পড়ে তোমার বেশি উপকার হবে।

## এই বইটি কীভাবে ব্যবহার করবে

সাধারণভাবে, এই বইটি ধরে নেয় যে তুমি পুরোটা সামনে থেকে পেছনের দিকে sequence-এ পড়ছ।
পরের chapter গুলো আগের chapter গুলোর concept-এর ওপর তৈরি, এবং আগের chapter গুলো
হয়তো কোনো নির্দিষ্ট topic-এ বিস্তারিত যাবে না কিন্তু পরের কোনো chapter-এ সেই
topic-এ ফিরে আসবে।

এই বইয়ে তুমি দুই ধরনের chapter পাবে: concept chapter এবং project chapter। concept
chapter গুলোতে তুমি Rust-এর একটি দিক সম্পর্কে শিখবে। project chapter গুলোতে আমরা
একসাথে ছোট ছোট program বানাবো, তোমার এ পর্যন্ত যা শেখা হয়েছে তা apply করে। Chapter
2, Chapter 12 এবং Chapter 21 হলো project chapter; বাকি গুলো concept chapter।

**Chapter 1**-এ ব্যাখ্যা করা হয়েছে কীভাবে Rust install করতে হয়, কীভাবে একটি "Hello,
world!" program লিখতে হয়, এবং কীভাবে Cargo—Rust-এর package manager ও build
tool—ব্যবহার করতে হয়। **Chapter 2** হলো Rust-এ program লেখার একটি hands-on পরিচিতি,
যেখানে তুমি একটি number-guessing game বানাবে। এখানে আমরা concept গুলো উঁচু স্তরে
cover করবো, এবং পরের chapter গুলো বিস্তারিত জানাবে। যদি তুমি সাথে সাথে হাত নোংরা
করতে চাও, Chapter 2-ই সেই জায়গা। যদি তুমি এমন একজন পরিশ্রমী learner হও যে পরের
ধাপে যাওয়ার আগে সব detail শিখতে পছন্দ করে, তাহলে তুমি হয়তো Chapter 2 skip করে
সরাসরি **Chapter 3**-এ যেতে পারো, যেখানে অন্যান্য programming language-এর মতো Rust
features cover করা হয়েছে; তারপর তুমি যখন তোমার শেখা detail গুলো apply করে একটি
project করতে চাইবে তখন Chapter 2-এ ফিরে আসতে পারো।

**Chapter 4**-এ তুমি Rust-এর ownership system সম্পর্কে শিখবে। **Chapter 5**-এ structs
ও methods নিয়ে আলোচনা করা হয়েছে। **Chapter 6**-এ enums, `match` expressions, এবং
`if let` ও `let...else` control flow constructs cover করা হয়েছে। তুমি custom type
বানাতে structs ও enums ব্যবহার করবে।

**Chapter 7**-এ তুমি Rust-এর module system সম্পর্কে শিখবে এবং তোমার code ও তার
public application programming interface (API) organize করার privacy rule গুলো সম্পর্কে
জানবে। **Chapter 8**-এ standard library-র দেওয়া কিছু common collection data
structure নিয়ে আলোচনা করা হয়েছে: vectors, strings এবং hash maps। **Chapter 9**
Rust-এর error-handling philosophy ও technique গুলো explore করে।

**Chapter 10**-এ generics, traits এবং lifetimes নিয়ে খোঁড়া হয়েছে, যা তোমাকে এমন
code define করার ক্ষমতা দেয় যা একাধিক type-এ apply হয়। **Chapter 11** সম্পূর্ণ
testing সম্পর্কে, যা Rust-এর safety guarantee থাকা সত্ত্বেও প্রয়োজন তোমার program-এর
logic সঠিক কিনা তা নিশ্চিত করতে। **Chapter 12**-এ আমরা আমাদের নিজস্ব `grep` command
line tool-এর একটি subset functionality implement করবো, যা file-এর ভেতর text খোঁজে।
এর জন্য আমরা আগের chapter গুলোতে আলোচিত অনেক concept ব্যবহার করবো।

**Chapter 13** closures এবং iterators explore করে: Rust-এর সেই features যা functional
programming language থেকে এসেছে। **Chapter 14**-এ আমরা Cargo-কে আরও গভীরভাবে দেখবো
এবং তোমার library গুলো অন্যদের সাথে share করার best practice নিয়ে কথা বলবো।
**Chapter 15** standard library-র দেওয়া smart pointer ও সেগুলোর functionality enable
করে এমন trait গুলো নিয়ে আলোচনা করে।

**Chapter 16**-এ আমরা বিভিন্ন concurrent programming model দিয়ে হাঁটবো এবং কথা বলবো
কীভাবে Rust তোমাকে fearlessভাবে একাধিক thread-এ program করতে সাহায্য করে। **Chapter
17**-এ আমরা তার ওপর ভর করে Rust-এর async ও await syntax, সাথে tasks, futures এবং
streams, এবং সেগুলো যে lightweight concurrency model enable করে তা explore করবো।

**Chapter 18** দেখে কীভাবে Rust idiom গুলো তোমার পরিচিত object-oriented programming
principle-এর সাথে তুলনা করা যায়। **Chapter 19** patterns এবং pattern matching-এর ওপর
একটি reference, যা Rust program জুড়ে idea প্রকাশের powerful উপায়। **Chapter 20**-তে
আগ্রহের বিভিন্ন advanced topic-এর একটি সমাহার আছে, যার মধ্যে unsafe Rust, macros,
এবং lifetimes, traits, types, functions ও closures সম্পর্কে আরও অনেক কিছু।

**Chapter 21**-এ আমরা একটি project সম্পূর্ণ করবো যেখানে আমরা একটি low-level
multithreaded web server implement করবো!

সবশেষে, কিছু appendix-এ reference-এর মতো ফরম্যাটে ভাষাটি সম্পর্কে কার্যকর তথ্য
দেওয়া আছে। **Appendix A**-তে Rust-এর keywords, **Appendix B**-তে Rust-এর operators
ও symbols, **Appendix C**-তে standard library-র দেওয়া derivable traits,
**Appendix D**-তে কিছু useful development tool, এবং **Appendix E**-তে Rust editions
ব্যাখ্যা করা হয়েছে। **Appendix F**-এ তুমি বইটির translation পাবে, এবং **Appendix
G**-তে আমরা cover করবো Rust কীভাবে তৈরি হয় এবং nightly Rust কী।

এই বইটি পড়ার কোনো ভুল উপায় নেই: যদি সামনে যেতে চাও, যাও! কোনো confusion হলে
তোমাকে হয়তো আগের chapter গুলোতে ফিরে যেতে হবে। কিন্তু তোমার যা কাজে আসে তাই করো।

<span id="ferris"></span>

Rust শেখার process-এর একটি গুরুত্বপূর্ণ অংশ হলো শেখা compiler যে error message
দেখায় তা কীভাবে পড়তে হয়: এগুলো তোমাকে কাজ করা code-এর দিকে গাইড করবে। সেই কারণে,
আমরা অনেক এমন example দেবো যা compile হয় না, সাথে প্রতিটি পরিস্থিতিতে compiler যে
error message দেখাবে তাও দেবো। জেনে রেখো, তুমি যদি একটি র‍্যান্ডম example লিখে চালাও,
তবে তা হয়তো compile হবে না! তুমি যে example চালাতে চাইছ সেটি error দেওয়ার জন্যই কিনা
তা দেখতে চারপাশের লেখাটি পড়ে নিশ্চিত হয়ে নাও। বেশিরভাগ ক্ষেত্রেই, যে code compile
হয় না সেটির সঠিক version-এ আমরা তোমাকে নিয়ে যাবো। Ferris তোমাকে এমন code চেনাতেও
সাহায্য করবে যা কাজ করার কথা নয়:

| Ferris                                                                                                           | Meaning                                          |
| ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| <img src="img/ferris/does_not_compile.svg" class="ferris-explain" alt="Ferris with a question mark"/>            | এই code compile হয় না!                          |
| <img src="img/ferris/panics.svg" class="ferris-explain" alt="Ferris throwing up their hands"/>                   | এই code panic করে!                              |
| <img src="img/ferris/not_desired_behavior.svg" class="ferris-explain" alt="Ferris with one claw up, shrugging"/> | এই code কাঙ্ক্ষিত behavior দেয় না। |

বেশিরভাগ ক্ষেত্রেই, যে code compile হয় না সেটির সঠিক version-এ আমরা তোমাকে নিয়ে যাবো।

## Source Code

এই বই তৈরি করার source file গুলো [GitHub][book]-এ পাওয়া যায়।

[book]: https://github.com/rust-lang/book/tree/main/src

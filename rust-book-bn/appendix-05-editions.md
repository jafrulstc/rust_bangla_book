## Appendix E: Editions

Chapter 1-এ তুমি দেখেছ যে `cargo new` তোমার _Cargo.toml_ file-এ একটি edition সম্পর্কিত কিছু metadata যোগ করে। এই appendix-এ আলোচনা করা হবে সেটি কী অর্থ বোঝায়!

Rust language ও compiler-এর একটি six-week release cycle আছে, যার মানে user-রা নতুন feature-এর একটি ধারাবাহিক স্রোত পান। অন্যান্য programming language বড় পরিবর্তন কম ঘন ঘন release করে; Rust ছোট ছোট update বেশি ঘন ঘন release করে। কিছুক্ষণ পরে এই ছোট ছোট পরিবর্তনগুলো জমে যায়। কিন্তু release থেকে release-এ এমনটা বলা কঠিন যে, “অবিশ্বাস্য! Rust 1.10 থেকে Rust 1.31-এ Rust অনেক বদলে গেছে!”

প্রায় তিন বছর অন্তর Rust team একটি নতুন Rust _edition_ প্রকাশ করে। প্রতিটি edition সম্পূর্ণ হালনাগাদ করা documentation ও tooling সহ একটি পরিষ্কার package-এ সেই সব feature একত্রিত করে আনে যেগুলো ইতিমধ্যে যুক্ত হয়েছে। নতুন edition স্বাভাবিক six-week release process-এর অংশ হিসেবেই ship হয়।

Edition বিভিন্ন মানুষের জন্য বিভিন্ন উদ্দেশ্য পূরণ করে:

- সক্রিয় Rust user-দের জন্য, একটি নতুন edition incremental পরিবর্তনগুলোকে একটি বোঝা সহজ package-এ নিয়ে আসে।
- Non-user-দের জন্য, একটি নতুন edition signal দেয় যে কিছু বড় অগ্রগতি হয়েছে, যা Rust-কে আবার একবার দেখার মতো করে তুলতে পারে।
- Rust develop করেন এমনদের জন্য, একটি নতুন edition পুরো project-এর জন্য একটি ঐক্যবদ্ধ কেন্দ্র হিসেবে কাজ করে।

লেখার সময় অনুযায়ী, চারটি Rust edition পাওয়া যায়: Rust 2015, Rust 2018, Rust 2021 এবং Rust 2024। এই বইটি Rust 2024 edition-এর idiom ব্যবহার করে লেখা।

_Cargo.toml_-এর `edition` key নির্দেশ করে তোমার code-এর জন্য compiler কোন edition ব্যবহার করবে। এই key না থাকলে, backward compatibility-র জন্য Rust `2015`-কে edition value হিসেবে ব্যবহার করে।

প্রতিটি project ডিফল্ট 2015 edition ছাড়া অন্য কোনো edition-এ opt-in করতে পারে। Edition-এ incompatible পরিবর্তন থাকতে পারে, যেমন এমন একটি নতুন keyword যোগ করা যা code-এর identifier-এর সাথে সংঘাত করে। তবে তুমি সেই পরিবর্তনগুলোতে opt-in না করলে, তুমি যে Rust compiler version ব্যবহার করছ তা upgrade করলেও তোমার code compile হতে থাকবে।

সব Rust compiler version তার release-এর আগে বিদ্যমান যেকোনো edition support করে, এবং সেগুলো যেকোনো supported edition-এর crate একসাথে link করতে পারে। Edition-এর পরিবর্তন শুধুমাত্র compiler code যেভাবে প্রাথমিকভাবে parse করে তাকে প্রভাবিত করে। তাই তুমি যদি Rust 2015 ব্যবহার করো এবং তোমার কোনো dependency Rust 2018 ব্যবহার করে, তবু তোমার project compile হবে এবং সেই dependency ব্যবহার করতে পারবে। উল্টো ক্ষেত্রেও একই—তোমার project Rust 2018 ব্যবহার করে এবং কোনো dependency Rust 2015 ব্যবহার করে—এটাও কাজ করে।

পরিষ্কার করে বলতে: বেশিরভাগ feature-ই সব edition-এ available থাকবে। যেকোনো Rust edition ব্যবহার করা developer-রা নতুন stable release হওয়ার সাথে সাথে improvement দেখতে থাকবেন। তবে কিছু ক্ষেত্রে, মূলত নতুন keyword যোগ করার সময়, কিছু নতুন feature শুধু পরবর্তী edition-এই available হতে পারে। এমন feature থেকে উপকৃত হতে চাইলে তোমাকে edition পরিবর্তন করতে হবে।

আরও বিস্তারিতের জন্য [_The Rust Edition Guide_][edition-guide] দেখো। এটি একটি সম্পূর্ণ বই যা edition-গুলোর মধ্যে পার্থক্য তালিকাভুক্ত করে এবং ব্যাখ্যা করে যে `cargo fix` এর মাধ্যমে কীভাবে তোমার code-কে স্বয়ংক্রিয়ভাবে নতুন edition-এ upgrade করতে হয়।

[edition-guide]: https://doc.rust-lang.org/stable/edition-guide

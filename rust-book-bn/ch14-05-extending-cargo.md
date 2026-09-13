## Custom Command দিয়ে Cargo-কে Extend করা

Cargo এমনভাবে design করা হয়েছে যাতে তুমি এটিকে modify না করেই নতুন subcommand দিয়ে extend করতে পারো। তোমার `$PATH`-এ যদি এমন কোনো binary থাকে যার নাম `cargo-something`, তুমি `cargo something` run করে সেটিকে Cargo subcommand-এর মতো run করতে পারবে। এ ধরনের custom command `cargo --list` run করলেও তালিকাভুক্ত হবে। `cargo install` দিয়ে extension install করে সেগুলোকে built-in Cargo tool-এর মতোই run করতে পারা — Cargo-র design-এর এক অত্যন্ত সুবিধাজনক সুবিধা!

## Summary

Cargo এবং [crates.io](https://crates.io/)<!-- ignore --> দিয়ে code share করাটাই Rust ecosystem-কে বিভিন্ন কাজের জন্য কার্যকর করে তোলার অংশ। Rust-এর standard library ছোট এবং stable, কিন্তু crate গুলো share করা, ব্যবহার করা ও উন্নত করা সহজ, এবং ভাষা থেকে আলাদা সময়সূচিতে সেগুলো এগিয়ে যায়। তোমার কাছে যা code useful মনে হয় তা [crates.io](https://crates.io/)<!-- ignore -->-তে share করতে দ্বিধা কোরো না; সম্ভবত অন্য কারও কাছেও সেটি useful হবে!

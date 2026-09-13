# Patterns and Matching

Rust-এ patterns হলো এক বিশেষ syntax, যা দিয়ে—সরল বা জটিল যেকোনো—type-এর structure-এর সাথে matching করা যায়। `match` expression ও অন্যান্য construct-এর সাথে pattern ব্যবহার করলে একটি program-এর control flow-এর ওপর তোমার নিয়ন্ত্রণ আরও বাড়ে। একটি pattern মূলত নিচের উপাদানগুলোর কোনো সমন্বয় হতে পারে:

- Literals
- Destructured arrays, enums, structs, বা tuples
- Variables
- Wildcards
- Placeholders

কিছু উদাহরণ pattern হলো `x`, `(a, 3)`, এবং `Some(Color::Red)`। Pattern valid এমন context-এ এই উপাদানগুলো data-এর shape বর্ণনা করে। এরপর আমাদের program value-গুলোকে pattern-এর সাথে match করে দেখে সেটির data shape সঠিক কি না—অর্থাৎ নির্দিষ্ট কোনো code চালানো চলবে কি না।

কোনো pattern ব্যবহার করতে হলে আমরা সেটিকে কোনো value-এর সাথে তুলনা করি। Pattern টি value-এর সাথে match করলে আমরা value-এর সেই অংশগুলো নিজের code-এ ব্যবহার করি। Chapter 6-এ `match` expression-এ pattern ব্যবহারের কথা মনে করো, যেমন কয়েন বাছাইয়ের মেশিনের উদাহরণ। value pattern-এর shape-এ ফিট হলে আমরা named অংশগুলো ব্যবহার করতে পারি। না হলে pattern-এর সাথে যুক্ত code টি run হবে না।

এই chapter-টি pattern-সংক্রান্ত সব বিষয়ের একটি reference। আমরা pattern ব্যবহারের valid জায়গাগুলো, refutable ও irrefutable pattern-এর পার্থক্য, এবং তুমি যে বিভিন্ন ধরনের pattern syntax দেখতে পারো সেগুলো নিয়ে আলোচনা করব। Chapter শেষে তুমি জানবে কীভাবে অনেক concept pattern দিয়ে পরিষ্কারভাবে প্রকাশ করা যায়।

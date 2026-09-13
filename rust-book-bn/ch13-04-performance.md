<!-- Old headings. Do not remove or links may break. -->

<a id="comparing-performance-loops-vs-iterators"></a>

## Performance in Loops vs. Iterators

Loop নাকি iterator ব্যবহার করবে তা নির্ধারণ করতে হলে, তোমার জানা দরকার কোন implementation দ্রুত: `search` function-এর explicit `for` loop সহ সংস্করণ নাকি iterator সহ সংস্করণ।

আমরা একটি benchmark run করেছি—_The Adventures of Sherlock Holmes_ by Sir Arthur Conan Doyle-এর পুরো content একটি `String`-এ load করে এবং content-এর মধ্যে _the_ শব্দটি খুঁজে। এখানে `for` loop ব্যবহার করা `search`-এর সংস্করণ ও iterator ব্যবহার করা সংস্করণের benchmark-এর ফলাফল দেওয়া হলো:

```text
test bench_search_for  ... bench:  19,620,300 ns/iter (+/- 915,700)
test bench_search_iter ... bench:  19,234,900 ns/iter (+/- 657,200)
```

দুটি implementation-এর performance প্রায় একই! আমরা এখানে benchmark code ব্যাখ্যা করব না, কারণ উদ্দেশ্য প্রমাণ করা নয় যে দুটি সংস্করণ equivalent, বরং এই দুটি implementation performance-এর দিক থেকে কীভাবে compare করে তার একটি সাধারণ ধারণা পাওয়া।

আরও comprehensive benchmark করতে চাইলে তোমার উচিত বিভিন্ন size-এর বিভিন্ন text-কে `contents` হিসেবে, বিভিন্ন শব্দ ও বিভিন্ন length-এর শব্দকে `query` হিসেবে এবং আরও নানা variation check করা। মূল কথা হলো: Iterator, যদিও একটি high-level abstraction, প্রায় সেই একই code-এ compile হয় যেন তুমি নিজে lower-level code লিখেছ। Iterator হলো Rust-এর _zero-cost abstraction_-গুলোর একটি, যার অর্থ হলো abstraction ব্যবহার করলে কোনো additional runtime overhead চাপায় না। এটি অনেকটা সেইভাবে, যেভাবে Bjarne Stroustrup, C++-এর মূল designer ও implementor, তাঁর 2012 ETAPS keynote presentation “Foundations of C++”-এ zero-overhead define করেছেন:

> In general, C++ implementations obey the zero-overhead principle: What you
> don’t use, you don’t pay for. And further: What you do use, you couldn’t hand
> code any better.

অনেক ক্ষেত্রে, iterator ব্যবহার করা Rust code ঠিক সেই assembly-এ compile হয় যেটি তুমি নিজে হাতে লিখতে। Loop unrolling এবং array access-এ bounds checking eliminate করার মতো optimization apply হয় এবং ফলাফল code-টিকে অত্যন্ত efficient করে তোলে। এখন যখন তুমি এটা জানো, তুমি ভয় ছাড়াই iterator এবং closure ব্যবহার করতে পারো! এগুলো code-কে উচ্চতর স্তরের মনে হতে দেয়, কিন্তু এটা করার জন্য কোনো runtime performance penalty চাপায় না।

## Summary

Closure ও iterator Rust-এর এমন feature যা functional programming language-এর ধারণা থেকে অনুপ্রাণিত। এগুলো low-level performance-এ high-level idea স্পষ্টভাবে প্রকাশ করার Rust-এর ক্ষমতায় অবদান রাখে। Closure ও iterator-এর implementation এমন যে runtime performance প্রভাবিত হয় না। এটি Rust-এর zero-cost abstraction provide করার লক্ষ্যের অংশ।

এখন যেহেতু আমরা আমাদের I/O project-এর expressiveness উন্নত করেছি, চলো `cargo`-র আরও কিছু feature দেখি যা আমাদের project দুনিয়ার সাথে share করতে সাহায্য করবে।

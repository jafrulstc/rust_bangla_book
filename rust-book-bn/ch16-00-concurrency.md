# Fearless Concurrency

নিরাপদ ও efficient ভাবে concurrent programming সামলানো Rust-এর অন্যতম প্রধান লক্ষ্য। _Concurrent programming_, যেখানে একটা program-এর বিভিন্ন অংশ স্বাধীনভাবে execute হয়, আর _parallel programming_, যেখানে একটা program-এর বিভিন্ন অংশ একই সময়ে execute হয় — দুটোই ক্রমশ গুরুত্বপূর্ণ হয়ে উঠছে কারণ বেশিরভাগ কম্পিউটার এখন তাদের একাধিক processor কাজে লাগায়। ইতিহাসগতভাবে, এসব পরিস্থিতিতে programming করা বেশ কঠিন আর error-prone ছিল। Rust চায় এটা বদলাতে।

শুরুতে Rust team ভেবেছিল যে memory safety নিশ্চিত করা আর concurrency সমস্যা প্রতিরোধ করা — এই দুটো আলাদা challenge, দুটোকেই আলাদা পদ্ধতিতে সমাধান করতে হবে। সময়ের সাথে সাথে team আবিষ্কার করল যে ownership আর type system হলো এমন এক শক্তিশালী tool সেট, যা memory safety _এবং_ concurrency উভয় সমস্যা সামলাতে সাহায্য করে! ownership আর type checking কাজে লাগিয়ে, Rust-ে অনেক concurrency error হলো runtime error নয় বরং compile-time error। ফলে তোমাকে ঘণ্টার পর ঘণ্টা সময় নষ্ট করে ঠিক সেই পরিস্থিতি recreate করতে হয় না যেখানে একটা runtime concurrency bug ঘটে — বরং ভুল code compile হতে চায় না আর সমস্যাটা ব্যাখ্যা করে একটা error দেখায়। ফলে তুমি code লেখার সময়েই সেটা ঠিক করতে পারো, production-এ যাওয়ার পরে নয়। Rust-এর এই দিকটাকে আমরা _fearless concurrency_ নাম দিয়েছি। Fearless concurrency তোমাকে এমন code লেখার সুযোগ দেয় যা subtle bug-মুক্ত আর সহজে refactor করা যায় নতুন bug ছাড়াই।

> Note: সরলতার জন্য, আমরা অনেক সমস্যাকে _concurrent_ বলে উল্লেখ করব, সবসময় _concurrent and/or parallel_ বলে সুনির্দিষ্ট না হয়ে। এই chapter-তে, যখনই আমরা _concurrent_ ব্যবহার করব, মাথায় _concurrent and/or parallel_ বসিয়ে নেবে। পরের chapter-এ, যেখানে পার্থক্যটা বেশি গুরুত্বপূর্ণ, সেখানে আমরা আরও নির্দিষ্ট থাকব।

অনেক language concurrency সমস্যা সামলানোর জন্য যেসব সমাধান দেয়, সে ব্যাপারে বেশ কট্টর। যেমন Erlang-এর message-passing concurrency-র জন্য চমৎকার functionality আছে, কিন্তু thread-এর মধ্যে state share করার উপায় খুবই সীমিত। শুধু কয়েকটি সম্ভাব্য সমাধান support করা higher-level language-গুলোর জন্য যুক্তিযুক্ত কৌশল, কারণ একটা higher-level language কিছু control ছেড়ে দিয়ে abstraction পাওয়ার সুবিধা দেয়। কিন্তু lower-level language থেকে আশা করা যায় যে যেকোনো পরিস্থিতিতে সবচেয়ে ভালো performance দেবে আর hardware-এর উপর abstraction কম থাকবে। তাই Rust বিভিন্ন tool দেয় যাতে তুমি তোমার পরিস্থিতি ও প্রয়োজন অনুযায়ী যেভাবে সবচেয়ে মানানসই হয়, সেভাবে সমস্যা model করতে পারো।

এই chapter-এ আমরা নিচের topic-গুলো cover করব:

- একই সময়ে code-এর একাধিক অংশ run করার জন্য thread তৈরি করা
- _Message-passing_ concurrency, যেখানে channel thread-এর মধ্যে message পাঠায়
- _Shared-state_ concurrency, যেখানে একাধিক thread কোনো একটা data-এ access পায়
- `Sync` এবং `Send` trait, যা Rust-এর concurrency guarantee user-defined type আর standard library-র দেওয়া type-এও প্রসারিত করে

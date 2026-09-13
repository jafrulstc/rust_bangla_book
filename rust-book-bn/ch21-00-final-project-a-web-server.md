# Final Project: একটি Multithreaded Web Server তৈরি করা

বেশ দীর্ঘ একটা যাত্রা পেরিয়ে আমরা বইয়ের শেষ পর্যায়ে পৌঁছেছি। এই chapter-এ আমরা শেষবারের মতো আরেকটি project একসাথে বানাবো, যেন শেষ কয়েকটা chapter-এ যেসব concept আলোচনা করেছি সেগুলো একবার প্রয়োগ করে দেখা যায় এবং আগের কিছু পাঠও একটু পুনরাবৃত্তি হয়।

আমাদের final project হিসেবে আমরা এমন একটি web server বানাবো যেটি “Hello!” লেখাটি দেখাবে এবং web browser-এ Figure 21-1-এর মতো দেখাবে।

Web server টি বানানোর জন্য আমাদের পরিকল্পনা হলো:

1. TCP আর HTTP সম্পর্কে সামান্য জানা।
2. একটি socket-এ TCP connection শোনা।
3. কয়েক ধরনের ছোট HTTP request parse করা।
4. সঠিক একটি HTTP response তৈরি করা।
5. একটি thread pool ব্যবহার করে আমাদের server-এর throughput বাড়ানো।

<img alt="Screenshot of a web browser visiting the address 127.0.0.1:8080 displaying a webpage with the text content “Hello! Hi from Rust”" src="img/trpl21-01.png" class="center" style="width: 50%;" />

<span class="caption">Figure 21-1: আমাদের শেষ shared project</span>

শুরু করার আগেই দুটো বিষয় উল্লেখ করে নিই। প্রথমত, আমরা যে পদ্ধতিতে কাজ করবো সেটা Rust-এ web server বানানোর সবচেয়ে ভালো উপায় নয়। Community-র সদস্যরা [crates.io](https://crates.io/)-এ বেশ কিছু production-ready crate প্রকাশ করেছেন যেগুলো আমরা যা বানাবো তার চেয়ে অনেক বেশি পূর্ণাঙ্গ web server এবং thread pool implementation দেয়। তবে এই chapter-এ আমাদের উদ্দেশ্য হলো তোমাকে শেখানো, সহজ পথে না চলা। Rust একটি systems programming language হওয়ায় আমরা যে পর্যায়ের abstraction নিয়ে কাজ করতে চাই সেটা নির্বাচন করতে পারি এবং অন্যান্য ভাষায় যা সম্ভব বা বাস্তবসম্মত নয় তার চেয়ে নিচু স্তরে নেমে কাজ করতে পারি।

দ্বিতীয়ত, আমরা এখানে async আর await ব্যবহার করবো না। একটি thread pool নিজেই বেশ বড় একটা চ্যালেঞ্জ, তার ওপর আবার async runtime বানানোর ঝামেলা যোগ করতে চাই না! তবে এই chapter-এ আমরা যেসব সমস্যা দেখবো সেগুলোর ক্ষেত্রে async আর await কীভাবে প্রযোজ্য হতে পারে সেটা আলোচনা করবো। সবশেষে, Chapter 17-এ যেমন বলেছিলাম, অনেক async runtime নিজেদের কাজ পরিচালনা করতে thread pool ব্যবহার করে।

তাই আমরা মূল HTTP server এবং thread pool টি নিজের হাতে লিখবো, যাতে ভবিষ্যতে তুমি যেসব crate ব্যবহার করবে সেগুলোর পেছনের মূল ধারণা আর প্রযুক্তি সম্পর্কে তোমার জ্ঞান হয়।

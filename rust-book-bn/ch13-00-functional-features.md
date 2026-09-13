# Functional Language Features: Iterators এবং Closures

Rust-এর design অনেক existing language ও technique থেকে অনুপ্রেরণা নিয়েছে, আর তার মধ্যে একটি বড় প্রভাব হলো _functional programming_। Functional style-এ programming করতে গেলে প্রায়ই function-কে value হিসেবে ব্যবহার করা হয়—যেমন সেগুলোকে argument হিসেবে pass করা, অন্য function থেকে return করা, পরে ব্যবহারের জন্য variable-এ assign করা ইত্যাদি।

এই chapter-এ আমরা functional programming আসলে কী সেটা নিয়ে debate করব না, বরং Rust-এর কিছু feature নিয়ে আলোচনা করব যেগুলো functional হিসেবে পরিচিত অনেক language-এর feature-এর সাথে মিলে যায়।

আরও নির্দিষ্ট করে বললে, আমরা যা cover করব:

- _Closures_, একটি function-এর মতো construct যাকে তুমি variable-এ সংরক্ষণ করতে পারো
- _Iterators_, ধারাবাহিক element-এর একটি series process করার একটি উপায়
- Chapter 12-এর I/O project-এ closure ও iterator ব্যবহার করে কীভাবে উন্নতি করা যায়
- Closure ও iterator-এর performance (spoiler alert: তোমার ধারণার চেয়ে এরা দ্রুত!)

আমরা ইতিমধ্যে আরও কিছু Rust feature cover করেছি, যেমন pattern matching এবং enum, যেগুলো functional style দ্বারা প্রভাবিত। Closure ও iterator-এ দক্ষতা অর্জন করা দ্রুত, idiomatic Rust code লেখার একটি গুরুত্বপূর্ণ অংশ, তাই আমরা পুরো chapter জুড়ে এগুলো নিয়ে আলোচনা করব।

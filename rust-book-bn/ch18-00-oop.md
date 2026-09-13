# Object-Oriented Programming Features

<!-- Old headings. Do not remove or links may break. -->

<a id="object-oriented-programming-features-of-rust"></a>

Object-oriented programming (OOP) হলো program-কে model করার একটি উপায়। Object নামের প্রোগ্রামিং ধারণাটি প্রথম ১৯৬০-এর দশকে Simula প্রোগ্রামিং ভাষায় চালু হয়েছিল। সেই object গুলো Alan Kay-এর প্রোগ্রামিং architecture-কে প্রভাবিত করে, যেখানে object গুলো একে অপরকে message পাঠায়। এই architecture বর্ণনা করতে গিয়ে ১৯৬৭ সালে তিনি _object-oriented programming_ শব্দটি তৈরি করেন। OOP আসলে কী, তার অনেকগুলো প্রতিদ্বন্দ্বী সংজ্ঞা আছে; কয়েকটা সংজ্ঞা অনুসারে Rust object-oriented, আবার আর কয়েকটা সংজ্ঞা অনুসারে নয়। এই chapter-এ আমরা সেইসব বৈশিষ্ট্য খুঁটিয়ে দেখবো যেগুলোকে সাধারণত object-oriented বলে ধরা হয় এবং সেই বৈশিষ্ট্য গুলো idiomatic Rust-এ কীভাবে উপস্থাপন করা যায়। এরপর আমরা দেখাবো কীভাবে Rust-এ একটা object-oriented design pattern implement করা যায় এবং আলোচনা করবো এই পথে চলার trade-off কী, Rust-এর নিজস্ব শক্তি ব্যবহার করে একটা সমাধান বানানোর সাথে তুলনা করে।

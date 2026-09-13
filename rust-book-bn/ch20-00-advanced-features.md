# Advanced Features

এখন পর্যন্ত তুমি Rust programming language-এর সবচেয়ে বেশি ব্যবহৃত অংশগুলো শিখে ফেলেছ। Chapter 21-এ আরেকটি project করার আগে, আমরা language-এর কিছু দিক দেখবো যা তুমি মাঝে মাঝে encounter করতে পারো কিন্তু প্রতিদিন ব্যবহার নাও করতে পারো। কোনো unknown বিষয় encounter করলে তুমি এই chapter-টিকে reference হিসেবে ব্যবহার করতে পারো। এখানে আলোচনা করা feature-গুলো খুব নির্দিষ্ট situation-এ কাজে লাগে। যদিও তুমি এগুলো প্রায়ই ব্যবহার নাও করো, আমরা চাই যে Rust-এর সব feature সম্পর্কে তোমার ধারণা থাকুক।

এই chapter-এ আমরা cover করবো:

- Unsafe Rust: Rust-এর কিছু guarantee থেকে বেরিয়ে এসে সেই guarantee-গুলো নিজে ম্যানুয়ালি uphold করার দায়িত্ব নেওয়ার পদ্ধতি
- Advanced traits: Associated type, default type parameter, fully qualified syntax, supertrait এবং trait-এর সাথে সম্পর্কিত newtype pattern
- Advanced type: Newtype pattern সম্পর্কে আরও, type alias, never type এবং dynamically sized type
- Advanced function এবং closure: Function pointer এবং closure return করা
- Macro: Compile time-এ আরও বেশি code সৃষ্টি করে এমন code লেখার উপায়

এটি Rust feature-এর একটি বিশাল সংগ্রহ, সবার জন্যই কিছু না কিছু আছে! চলো শুরু করি!

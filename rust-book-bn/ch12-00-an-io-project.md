# একটি I/O Project: Command Line Program তৈরি করা

এই chapter-এ আমরা এ পর্যন্ত যে অনেক দক্ষতা অর্জন করেছ, সেগুলোর একটি পুনরাবৃত্তি করব এবং আরও কিছু standard library feature নিয়ে আলোচনা করব। আমরা এমন একটি command line tool বানাবো যেটা file ও command line input/output এর সাথে কাজ করে, যাতে তুমি এ পর্যন্ত শেখা Rust-এর বেশ কিছু concept ব্যবহার করার অনুশীলন করতে পারো।

Rust-এর speed, safety, single binary output এবং cross-platform support এটিকে command line tool তৈরির জন্য একটি আদর্শ ভাষা বানায়। তাই আমাদের project হিসেবে আমরা বানাবো classic command line search tool `grep`-এর আমাদের নিজস্ব সংস্করণ (**g**lobally search a **r**egular **e**xpression and **p**rint)। সবচেয়ে সাধারণ ব্যবহারে, `grep` একটি নির্দিষ্ট file-এ একটি নির্দিষ্ট string খোঁজে। এই কাজটি করার জন্য `grep` argument হিসেবে একটি file path ও একটি string নেয়। তারপর সেই file-টি পড়ে, সেই file-এর এমন সব line খুঁজে বের করে যেগুলোতে ওই string argument-টি আছে, এবং সেই line গুলো print করে।

এই পথ ধরে আমরা দেখাবো কীভাবে আমাদের command line tool-কে এমন সব terminal feature ব্যবহার করানো যায় যেগুলো অন্য অনেক command line tool ব্যবহার করে। আমরা একটি environment variable-এর মান পড়ব, যাতে user আমাদের tool-এর আচরণ configure করতে পারে। আমরা error message গুলো standard output (`stdout`) এর বদলে standard error console stream (`stderr`)-এ print করব, যাতে—উদাহরণ স্বরূপ—user সফল output একটি file-এ পাঠাতে পারে কিন্তু সেই সাথে error message গুলো screen-এ দেখতে পারে।

Rust community-র একজন সদস্য, Andrew Gallant, ইতিমধ্যেই `grep`-এর একটি সম্পূর্ণ feature সমৃদ্ধ ও অত্যন্ত দ্রুত সংস্করণ বানিয়েছেন, যার নাম `ripgrep`। তার তুলনায় আমাদের সংস্করণটি বেশ সাধারণ হবে, কিন্তু এই chapter তোমাকে এমন কিছু পটভূমি জ্ঞান দেবে যা `ripgrep`-এর মতো একটি real-world project বুঝতে তোমার দরকার হবে।

আমাদের `grep` project তুমি এ পর্যন্ত যা যা শিখেছ তার অনেকগুলো concept একসাথে যুক্ত করবে:

- Code organize করা ([Chapter 7][ch7]<!-- ignore -->)
- Vector ও string ব্যবহার করা ([Chapter 8][ch8]<!-- ignore -->)
- Error handle করা ([Chapter 9][ch9]<!-- ignore -->)
- প্রয়োজনমতো trait ও lifetime ব্যবহার করা ([Chapter 10][ch10]<!-- ignore -->)
- Test লেখা ([Chapter 11][ch11]<!-- ignore -->)

আমরা closure, iterator ও trait object সম্পর্কেও সংক্ষেপে পরিচয় করাব, যেগুলো [Chapter 13][ch13]<!-- ignore --> এবং [Chapter 18][ch18]<!-- ignore --> বিস্তারিতভাবে আলোচনা করবে।

[ch7]: ch07-00-managing-growing-projects-with-packages-crates-and-modules.html
[ch8]: ch08-00-common-collections.html
[ch9]: ch09-00-error-handling.html
[ch10]: ch10-00-generics.html
[ch11]: ch11-00-testing.html
[ch13]: ch13-00-functional-features.html
[ch18]: ch18-00-oop.html

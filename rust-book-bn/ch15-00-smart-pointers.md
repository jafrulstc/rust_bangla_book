# Smart Pointers

pointer হলো এমন একটা সাধারণ ধারণা যেখানে একটা variable-এর ভেতরে memory-র একটা address থাকে। এই address অন্য কোনো data-কে refer করে, অর্থাৎ “point” করে। Rust-এ সবচেয়ে সাধারণ ধরনের pointer হলো reference, যেটা নিয়ে তুমি Chapter 4-এ শিখেছ। reference-কে `&` চিহ্ন দিয়ে বোঝানো হয় এবং এগুলো যে value-কে point করে সেটাকে borrow করে। data-কে refer করার বাইরে এগুলোর কোনো বিশেষ ক্ষমতা নেই, এবং এগুলোর কোনো overhead নেই।

অন্যদিকে _smart pointer_ গুলো এমন data structure যেগুলো pointer-এর মতো আচরণ করে কিন্তু সাথে অতিরিক্ত metadata এবং ক্ষমতাও থাকে। smart pointer-এর ধারণা Rust-এর একক সম্পত্তি নয়: smart pointer-এর উৎপত্তি C++-এ হয়েছিল এবং অন্যান্য language-তেও এগুলো বিদ্যমান। Rust-এর standard library-তে বিভিন্ন ধরনের smart pointer define করা আছে যেগুলো reference-এর চেয়ে বেশি functionality দেয়। সাধারণ ধারণাটা বোঝার জন্য আমরা কয়েকটা ভিন্ন smart pointer-এর উদাহরণ দেখব, যার মধ্যে একটা হবে _reference counting_ smart pointer type। এই pointer তোমাকে data-এর একাধিক owner রাখার সুবিধা দেয় owner-দের সংখ্যা track করে এবং কোনো owner না থাকলে data পরিষ্কার করে।

Rust-এ ownership এবং borrowing-এর ধারণার কারণে reference এবং smart pointer-এর মধ্যে আরেকটা পার্থক্য আছে: reference শুধু data borrow করে, কিন্তু অনেক ক্ষেত্রে smart pointer তার point করা data-কে _own_ করে।

smart pointer সাধারণত struct ব্যবহার করে implement করা হয়। সাধারণ struct-এর থেকে আলাদাভাবে smart pointer `Deref` এবং `Drop` trait implement করে। `Deref` trait একটা smart pointer struct-এর instance-কে reference-এর মতো আচরণ করতে দেয়, যাতে তুমি এমন code লিখতে পারো যা reference অথবা smart pointer উভয়ের সাথেই কাজ করবে। `Drop` trait তোমাকে সেই code কাস্টমাইজ করতে দেয় যা smart pointer-এর instance scope ছেড়ে যাওয়ার সময় চলে। এই chapter-এ আমরা এই দুটো trait-ই আলোচনা করব এবং দেখাব কেন সেগুলো smart pointer-এর কাছে গুরুত্বপূর্ণ।

যেহেতু smart pointer pattern Rust-এ প্রায়ই ব্যবহৃত একটা সাধারণ design pattern, তাই এই chapter-এ প্রতিটি existing smart pointer cover করা হবে না। অনেক library-এর নিজস্ব smart pointer আছে, এবং তুমি চাইলে নিজেরটাও লিখতে পারো। আমরা standard library-র সবচেয়ে সাধারণ কয়েকটা smart pointer নিয়ে আলোচনা করব:

- `Box<T>`, heap-এ value allocate করার জন্য
- `Rc<T>`, একটা reference counting type যা multiple ownership সক্ষম করে
- `Ref<T>` এবং `RefMut<T>`, `RefCell<T>`-এর মাধ্যমে access করা যায়, এমন একটা type যা borrowing rule গুলো compile time-এর বদলে runtime-এ enforce করে

এছাড়া আমরা _interior mutability_ pattern নিয়ে আলোচনা করব যেখানে একটা immutable type তার ভেতরের value mutate করার জন্য API expose করে। আমরা reference cycle নিয়েও আলোচনা করব: কীভাবে সেগুলো memory leak করতে পারে এবং কীভাবে সেগুলো প্রতিরোধ করা যায়।

চলো শুরু করি!

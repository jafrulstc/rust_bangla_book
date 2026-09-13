# Common Collections

Rust-এর standard library-তে কিছু খুব কাজের data structure আছে যাদের _collection_ বলা হয়। অন্যান্য বেশিরভাগ data type একটি নির্দিষ্ট value represent করে, কিন্তু collection-এ একাধিক value রাখা যায়। Built-in array ও tuple type-এর মতো নয়, এই collection-গুলো যে data-কে point করে তা heap-এ store করা হয়, অর্থাৎ compile time-এ data-এর পরিমাণ জানা থাকার দরকার নেই এবং program চলাকালীন সেটা বড় বা ছোট হতে পারে। প্রতিটি ধরনের collection-এর ভিন্ন ভিন্ন capability ও cost আছে, এবং তোমার বর্তমান প্রয়োজনে কোনটা সবচেয়ে মানানসই সেটা বেছে নেওয়ার দক্ষতা সময়ের সাথে গড়ে উঠবে। এই chapter-এ আমরা Rust program-এ বহুল ব্যবহৃত তিনটি collection নিয়ে আলোচনা করব:

- একটি _vector_ তোমাকে পরিবর্তনশীল সংখ্যক value পাশাপাশি store করতে দেয়।
- একটি _string_ হলো character-এর একটি collection। আগে আমরা `String` type নিয়ে কথা বলেছি, কিন্তু এই chapter-এ আমরা এটি বিস্তারিতভাবে আলোচনা করব।
- একটি _hash map_ তোমাকে একটি নির্দিষ্ট key-এর সাথে একটি value যুক্ত করতে দেয়। এটি _map_ নামের অপেক্ষাকৃত সাধারণ data structure-এর একটি নির্দিষ্ট implementation।

Standard library-তে দেওয়া অন্যান্য ধরনের collection সম্পর্কে জানতে [documentation][collections] দেখো।

আমরা আলোচনা করব কীভাবে vector, string ও hash map তৈরি ও আপডেট করতে হয়, এবং প্রতিটি কী কারণে বিশেষ।

[collections]: ../std/collections/index.html

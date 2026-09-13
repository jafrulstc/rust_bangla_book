# Common Programming Concepts

এই chapter-এ এমন কিছু concept নিয়ে আলোচনা করা হবে যেগুলো প্রায় প্রতিটি programming language-এই দেখা যায় এবং Rust-এ সেগুলো কীভাবে কাজ করে। অনেক programming language-এর core-এ অনেক কিছুই মিল থাকে। এই chapter-এ তোলা কোনো concept-ই Rust-specific নয়, কিন্তু আমরা সেগুলো Rust-এর প্রেক্ষাপটে আলোচনা করব এবং সেগুলো ব্যবহারের সময় মেনে চলা conventions ব্যাখ্যা করব।

বিশেষ করে, তুমি variables, basic types, functions, comments এবং control flow সম্পর্কে জানতে পারবে। এই ভিত্তিগুলো প্রতিটি Rust program-এ থাকবে, এবং শুরুতেই এগুলো শেখা তোমাকে একটা শক্ত ভিত্তি দেবে যার ওপর ভর করে এগোতে পারবে।

> #### Keywords
>
> Rust language-এ একসেট _keywords_ আছে যেগুলো শুধু language-এর নিজস্ব ব্যবহারের জন্যই reserved, অন্যান্য language-এর মতোই। মনে রাখবে যে তুমি এই শব্দগুলো variable বা function-এর নাম হিসেবে ব্যবহার করতে পারবে না। বেশিরভাগ keyword-এরই বিশেষ অর্থ আছে, এবং Rust program-এ নানা কাজ করতে তুমি সেগুলো ব্যবহার করবে; কয়েকটির বর্তমানে কোনো কার্যকারিতা নেই কিন্তু ভবিষ্যতে Rust-এ যোগ হতে পারে এমন কার্যকারিতার জন্য reserved রাখা হয়েছে। keyword-গুলোর তালিকা তুমি [Appendix A][appendix_a]<!-- ignore -->-এ পাবে।

[appendix_a]: appendix-01-keywords.md

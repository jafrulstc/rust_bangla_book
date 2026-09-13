# Ownership বোঝা

Ownership Rust-এর সবচেয়ে unique feature এবং ভাষার বাকি অংশের ওপর এর গভীর প্রভাব রয়েছে। এটি Rust-কে কোনো garbage collector ছাড়াই memory safety guarantee দেওয়ার সুযোগ করে দেয়, তাই ownership কীভাবে কাজ করে সেটা বোঝা জরুরি। এই chapter-এ আমরা ownership নিয়ে কথা বলব, সেই সাথে আলোচনা করব কয়েকটি সম্পর্কিত feature নিয়ে: borrowing, slices এবং Rust কীভাবে memory-তে data সাজায়।

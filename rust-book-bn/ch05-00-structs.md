# Struct ব্যবহার করে সম্পর্কিত Data গোছানো

_struct_, বা _structure_, হলো এমন একটি custom data type যা তোমাকে একসাথে একাধিক সম্পর্কিত value গোছাতে ও নাম দিতে দেয়, যেগুলো মিলে একটি অর্থপূর্ণ দল তৈরি করে। তুমি যদি কোনো object-oriented language-এর সাথে পরিচিত থাকো, তাহলে struct হলো object-এর data attribute-এর মতো। এই chapter-এ আমরা tuple আর struct-এর তুলনা করব, যাতে তোমার জানা জিনিসগুলোর ওপর ভিত্তি করে বোঝানো যায় কখন data গোছাতে struct বেশি মানানসই।

আমরা দেখাবো কীভাবে struct define ও instantiate করতে হয়। তারপর আলোচনা করব কীভাবে associated function define করতে হয়—বিশেষ করে সেই ধরনের associated function যাদের _method_ বলা হয়—যাতে একটি struct type-এর সাথে সম্পর্কিত behavior উল্লেখ করা যায়। Struct আর enum (যেটা Chapter 6-এ আলোচনা করা হবে) হলো তোমার program-এর domain-এ নতুন type তৈরি করার মূল উপাদান, যাতে Rust-এর compile-time type checking-এর সম্পূর্ণ সুবিধা পাওয়া যায়।

<!-- Old headings. Do not remove or links may break. -->

<a id="managing-growing-projects-with-packages-crates-and-modules"></a>

# Packages, Crates, এবং Modules

যত বড় প্রোগ্রাম তুমি লিখবে, তত বেশি গুরুত্বপূর্ণ হয়ে উঠবে তোমার code-কে সুশৃঙ্খলভাবে সাজানো। সম্পর্কিত functionality গুলো একসাথে গ্রুপ করা এবং আলাদা feature-এর code আলাদা করে রাখলে দ্রুত বোঝা যায় যে কোনো নির্দিষ্ট feature implement করা code কোথায় পাওয়া যাবে, এবং কোনো feature-এর আচরণ পরিবর্তন করতে হলে কোথায় যেতে হবে।

আমরা এ পর্যন্ত যে প্রোগ্রাম গুলো লিখেছি সেগুলো একটি মাত্র file-এ একটি মাত্র module-এ ছিল। কিন্তু project বড় হতে থাকলে তোমার code-কে কয়েকটি module-এ এবং তারপর কয়েকটি file-এ ভাগ করে সাজানো উচিত। একটি package-এ একাধিক binary crate থাকতে পারে এবং optionally একটি library crate থাকতে পারে। Package বড় হলে তুমি কিছু অংশ আলাদা crate হিসেবে বের করে আনতে পারো, যেগুলো তখন external dependency হিসেবে কাজ করবে। এই chapter-এ আমরা এই সব কৌশল নিয়ে আলোচনা করব। খুব বড় বড় project-এ যেখানে একসাথে evolve হওয়া কয়েকটি interrelated package থাকে, সেক্ষেত্রে Cargo যোগায় workspaces — যা নিয়ে আমরা Chapter 14-এ [“Cargo Workspaces”][workspaces]<!-- ignore --> section-এ আলোচনা করব।

আমরা implementation detail কীভাবে encapsulate করতে হয় সেটাও আলোচনা করব, যা code-কে উচ্চতর স্তরে reuse করতে সাহায্য করে: একবার কোনো operation implement করা হলে, অন্য code তোমার code-কে তার public interface দিয়ে call করতে পারবে, implementation কীভাবে কাজ করে সেটা না জেনেও। তুমি যেভাবে code লেখো সেটা ঠিক করে দেয় কোন অংশগুলো অন্যদের ব্যবহারের জন্য public এবং কোনগুলো private implementation detail যা তুমি পরে পরিবর্তন করার অধিকার রাখো। এটা একভাবে মাথায় রাখতে হবে এমন বিস্তারিত পরিমাণ কমানোর উপায়।

সম্পর্কিত একটি concept হলো scope: code যে nested context-এ লেখা হয় সেখানে একসেট নাম “in scope” হিসেবে define থাকে। Code পড়া, লেখা এবং compile করার সময় programmer ও compiler-কে জানতে হয় যে কোনো নির্দিষ্ট জায়গায় কোনো নাম একটি variable, function, struct, enum, module, constant বা অন্য কোনো item-কে নির্দেশ করছে এবং সেই item-টির অর্থ কী। তুমি নিজে scope তৈরি করতে পারো এবং কোন নামগুলো in বা out of scope থাকবে সেটা পরিবর্তন করতে পারো। একই scope-এ দুটি item একই নামে থাকতে পারে না; নামের দ্বন্দ্ব মেটানোর জন্য বেশ কিছু tool আছে।

Rust-এ বেশ কিছু feature আছে যা তোমার code-এর organization ম্যানেজ করতে সাহায্য করে — কোন detail গুলো exposed থাকবে, কোনগুলো private থাকবে, এবং তোমার প্রোগ্রামের প্রতিটি scope-এ কোন নামগুলো থাকবে। এই feature-গুলোকে একসাথে কখনো _module system_ বলা হয়, যার মধ্যে আছে:

* **Packages**: একটি Cargo feature যা crate build, test এবং share করতে দেয়
* **Crates**: module-গুলোর একটি tree যা একটি library বা executable তৈরি করে
* **Modules এবং `use`**: path-গুলোর organization, scope এবং privacy নিয়ন্ত্রণ করতে দেয়
* **Paths**: কোনো item (যেমন struct, function, বা module)-কে নাম দেওয়ার উপায়

এই chapter-ে আমরা সব feature-গুলো cover করব, আলোচনা করব কীভাবে এগুলো একে অপরের সাথে যুক্ত হয়, এবং ব্যাখ্যা করব কীভাবে scope ম্যানেজ করতে এগুলো ব্যবহার করতে হয়। শেষে তুমি module system সম্পর্কে দৃঢ় ধারণা লাভ করবে এবং পেশাদারের মতো scope নিয়ে কাজ করতে সক্ষম হবে!

[workspaces]: ch14-03-cargo-workspaces.html

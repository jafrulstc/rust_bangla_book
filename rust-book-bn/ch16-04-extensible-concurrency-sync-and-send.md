<!-- Old headings. Do not remove or links may break. -->

<a id="extensible-concurrency-with-the-sync-and-send-traits"></a>
<a id="extensible-concurrency-with-the-send-and-sync-traits"></a>

## `Send` এবং `Sync` দিয়ে Extensible Concurrency

মজার ব্যাপার হলো, এই chapter-এ আমরা যে concurrency feature গুলো নিয়ে এ পর্যন্ত কথা বলেছি তার প্রায় সবটাই standard library-র অংশ, language-এর নয়। concurrency handle করার তোমার option শুধু language বা standard library-তে সীমাবদ্ধ নয়; তুমি নিজের concurrency feature লিখতে পারো বা অন্যদের লেখা feature ব্যবহার করতে পারো।

তবে, language-এ embedded এমন key concurrency concept-গুলোর মধ্যে আছে `std::marker` trait `Send` আর `Sync`।

<!-- Old headings. Do not remove or links may break. -->

<a id="allowing-transference-of-ownership-between-threads-with-send"></a>

### Thread-এর মধ্যে Ownership Transfer করা

`Send` marker trait নির্দেশ করে যে `Send` implement করা type-এর value-এর ownership thread-এর মধ্যে transfer করা যেতে পারে। প্রায় প্রতিটি Rust type `Send` implement করে, কিন্তু কিছু exception আছে, যার মধ্যে `Rc<T>` অন্যতম: এটি `Send` implement করতে পারে না কারণ তুমি যদি একটা `Rc<T>` value clone করো আর সেই clone-এর ownership অন্য thread-এ transfer করার চেষ্টা করো, তবে দুটো thread-ই একই সময়ে reference count update করতে পারে। এই কারণে, `Rc<T>` single-threaded পরিস্থিতির জন্য implement করা, যেখানে তুমি thread-safe performance penalty pay করতে চাও না।

তাই Rust-এর type system আর trait bound নিশ্চিত করে যে তুমি কখনো accidentally একটা `Rc<T>` value thread-এর মধ্যে unsafe ভাবে send করতে পারবে না। Listing 16-14-তে আমরা যখন এটা করার চেষ্টা করেছিলাম, আমরা error পেয়েছিলাম `` the trait `Send` is not implemented for `Rc<Mutex<i32>>` ``। যখন আমরা `Arc<T>`-এ চলে গেছি, যেটা `Send` implement করে, code compile হয়েছিল।

পুরোপুরি `Send` type দিয়ে গঠিত যেকোনো type স্বয়ংক্রিয়ভাবে `Send` হিসেবে চিহ্নিত হয়। raw pointer ছাড়া প্রায় সব primitive type-ই `Send`, যা নিয়ে আমরা Chapter 20-এ আলোচনা করব।

<!-- Old headings. Do not remove or links may break. -->

<a id="allowing-access-from-multiple-threads-with-sync"></a>

### একাধিক Thread থেকে Access করা

`Sync` marker trait নির্দেশ করে যে `Sync` implement করা type-কে একাধিক thread থেকে reference করা safe। অন্য কথায়, যেকোনো type `T` `Sync` implement করে যদি `&T` (`T`-এর একটা immutable reference) `Send` implement করে, যার মানে reference টা safely অন্য thread-এ send করা যায়। `Send`-এর মতো, primitive type গুলো সবই `Sync` implement করে, আর পুরোপুরি `Sync` implement করা type দিয়ে গঠিত type গুলোও `Sync` implement করে।

smart pointer `Rc<T>`-ও `Sync` implement করে না একই কারণে যে কারণে `Send` implement করে না। `RefCell<T>` type (যা নিয়ে Chapter 15-এ আলোচনা করেছি) এবং related `Cell<T>` family-র গোটা family `Sync` implement করে না। `RefCell<T>` যে borrow checking runtime-এ করে সেটা thread-safe নয়। smart pointer `Mutex<T>` `Sync` implement করে আর একাধিক thread-এর সাথে share করে access দিতে ব্যবহার করা যায়, যেমন তুমি দেখেছো [“Shared Access to `Mutex<T>`”][shared-access]<!-- ignore --> section-এ।

### `Send` এবং `Sync` Manually Implement করা Unsafe

কারণ `Send` আর `Sync` trait implement করা অন্যান্য type দিয়ে পুরোপুরি গঠিত type গুলোও স্বয়ংক্রিয়ভাবে `Send` আর `Sync` implement করে, তাই আমাদের সেই trait গুলো manually implement করতে হয় না। Marker trait হিসেবে এদের implement করার মতো কোনো method-ও নেই। এগুলো শুধু concurrency সম্পর্কিত invariant enforce করতেই useful।

এই trait গুলো manually implement করতে হলে unsafe Rust code implement করতে হয়। আমরা Chapter 20-এ unsafe Rust code ব্যবহার নিয়ে আলোচনা করব; আপাতত, গুরুত্বপূর্ণ তথ্য হলো `Send` আর `Sync` part দিয়ে তৈরি নয় এমন নতুন concurrent type তৈরি করতে হলে safety guarantee uphold করতে সতর্ক চিন্তা দরকার। [“The Rustonomicon”][nomicon]-এ এই guarantee আর কীভাবে সেগুলো uphold করতে হয় তার আরও তথ্য আছে।

## Summary

এই book-এ তুমি concurrency নিয়ে এটাই শেষ দেখছো না: পরের chapter-টি async programming-এ কেন্দ্র করে আর Chapter 21-এর project এই chapter-এর concept গুলো এখানে আলোচিত ছোট উদাহরণ গুলোর চেয়ে অপেক্ষাকৃত realistic পরিস্থিতিতে ব্যবহার করবে।

আগেই বলা হয়েছে, Rust যেভাবে concurrency handle করে তার খুব অল্প অংশই language-এর অংশ, তাই অনেক concurrency solution crate হিসেবে implement করা। এগুলো standard library-র চেয়ে দ্রুত evolve হয়, তাই multithreaded পরিস্থিতির জন্য current, state-of-the-art crate খুঁজে নিতে অবশ্যই online-এ search করবে।

Rust standard library message passing-এর জন্য channel দেয় আর এমন smart pointer type, যেমন `Mutex<T>` আর `Arc<T>`, যা concurrent context-এ safe। Type system আর borrow checker নিশ্চিত করে যে এই solution গুলো ব্যবহার করা code data race বা invalid reference দিয়ে শেষ হবে না। একবার তোমার code compile হয়ে গেলে, তুমি নিশ্চিন্ত থাকতে পারো যে সেটা একাধিক thread-এ নির্ভুলভাবে run হবে, অন্যান্য language-এ প্রচলিত track করা কঠিন bug ছাড়াই। Concurrent programming এখন আর ভয়ের বিষয় নয়: এগিয়ে যাও আর তোমার program গুলো fearless ভাবে concurrent করে ফেলো!

[shared-access]: ch16-03-shared-state.html#shared-access-to-mutext
[nomicon]: ../nomicon/index.html

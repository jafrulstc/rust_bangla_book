## Appendix C: Derivable Traits

বইটির বিভিন্ন জায়গায় আমরা `derive` attribute নিয়ে আলোচনা করেছি, যেটি তুমি একটি struct বা enum definition-এ প্রয়োগ করতে পারো। `derive` attribute এমন code তৈরি করে যা তোমার `derive` syntax দিয়ে annotate করা type-এ trait-এর নিজস্ব default implementation বাস্তবায়ন করে।

এই appendix-এ আমরা standard library-র সেই সব trait-এর রেফারেন্স দিচ্ছি, যেগুলো তুমি `derive`-এর সাথে ব্যবহার করতে পারো। প্রতিটি section-এ আলোচনা করা হবে:

- এই trait derive করলে কোন কোন operator ও method enable হবে
- `derive` যে trait implementation দেয় সেটি কী করে
- trait implement করা থাকলে type সম্পর্কে তা কী নির্দেশ করে
- যে শর্তে তুমি এই trait implement করতে পারবে বা পারবে না
- এমন কিছু operation-এর উদাহরণ যেগুলোর জন্য এই trait প্রয়োজন

যদি `derive` attribute যা দেয় তার থেকে ভিন্ন behavior তুমি চাও, তাহলে প্রতিটি trait-কে কীভাবে manually implement করতে হয় তার বিস্তারিতের জন্য [standard library documentation](../std/index.html)<!-- ignore --> দেখো।

এখানে তালিকাভুক্ত trait গুলো হলো standard library-র দ্বারা define করা একমাত্র trait, যেগুলো তোমার type-এ `derive` ব্যবহার করে implement করা যায়। Standard library-তে define করা অন্যান্য trait-এর কোনো সঙ্গতিপূর্ণ default behavior নেই, তাই তোমার কাজের উদ্দেশ্য অনুযায়ী সেগুলো নিজের মতো করে implement করা তোমার দায়িত্ব।

এমন একটি trait যেটি derive করা যায় না তার উদাহরণ হলো `Display`, যা end user-এর জন্য formatting handle করে। তোমার সবসময় ভাবতে হবে একটি type-কে end user-এর কাছে উপস্থাপনের সবচেয়ে উপযুক্ত উপায় কোনটি। type-এর কোন অংশগুলো end user দেখতে পারবে? কোন অংশগুলো তাদের কাছে relevant? data-র কোন format তাদের কাছে সবচেয়ে relevant? Rust compiler-এর কাছে এই অন্তর্দৃষ্টি নেই, তাই সে তোমার জন্য সঠিক default behavior দিতে পারে না।

এই appendix-এ দেওয়া derivable trait-এর তালিকাটি সম্পূর্ণ নয়: library-গুলো নিজেদের trait-এর জন্য `derive` implement করতে পারে, ফলে `derive` যে সব trait-এর সাথে ব্যবহার করতে পারো সেই তালিকা সত্যিকার অর্থে উন্মুক্ত। `derive` implement করতে procedural macro ব্যবহার করা হয়, যা Chapter 20-র [“Custom `derive`
Macros”][custom-derive-macros]<!-- ignore --> section-এ আলোচনা করা হয়েছে।

### `Debug` — Programmer-এর Output-এর জন্য

`Debug` trait format string-এ debug formatting enable করে, যা তুমি `{}` placeholder-এর ভেতরে `:?` যোগ করে নির্দেশ করো।

`Debug` trait তোমাকে debugging উদ্দেশ্যে কোনো type-এর instance print করতে দেয়, যাতে তুমি এবং তোমার type ব্যবহার করছেন এমন অন্যান্য programmer একটি program execution-এর নির্দিষ্ট বিন্দুতে instance inspect করতে পারেন।

`Debug` trait প্রয়োজন, উদাহরণস্বরূপ, `assert_eq!` macro ব্যবহারের সময়। equality assertion fail করলে এই macro argument হিসেবে দেওয়া instance-গুলোর value print করে, যাতে programmer-রা বুঝতে পারেন কেন দুটি instance সমান নয়।

### `PartialEq` এবং `Eq` — Equality Comparison-এর জন্য

`PartialEq` trait তোমাকে কোনো type-এর instance তুলনা করে equality যাচাই করতে দেয় এবং `==` ও `!=` operator ব্যবহার করতে সক্ষম করে।

`PartialEq` derive করলে `eq` method implement হয়। struct-এ `PartialEq` derive করা হলে শুধুমাত্র তখনই দুটি instance সমান হবে যখন _সব_ field সমান, এবং _যেকোনো_ field সমান না হলে instance দুটি সমান নয়। enum-এ derive করা হলে প্রতিটি variant নিজের সাথে সমান এবং অন্যান্য variant-এর সাথে সমান নয়।

`PartialEq` trait প্রয়োজন, উদাহরণস্বরূপ, `assert_eq!` macro ব্যবহারের সময়, যার কোনো type-এর দুটি instance-এর equality তুলনা করতে সক্ষম হওয়া প্রয়োজন।

`Eq` trait-এর কোনো method নেই। এর উদ্দেশ্য হলো নির্দেশ করা যে annotate করা type-এর প্রতিটি value নিজের সাথে সমান। `Eq` trait শুধুমাত্র এমন type-এ প্রয়োগ করা যায় যেগুলো `PartialEq`-ও implement করে, যদিও `PartialEq` implement করে এমন সব type `Eq` implement করতে পারে না। এর একটি উদাহরণ হলো floating-point number type: floating-point number-এর implementation বলে যে not-a-number (`NaN`) value-এর দুটি instance একে অপরের সমান নয়।

`Eq` যেখানে প্রয়োজন তার একটি উদাহরণ হলো `HashMap<K, V>`-তে key হিসেবে, যাতে `HashMap<K, V>` বুঝতে পারে দুটি key একই কি না।

### `PartialOrd` এবং `Ord` — Ordering Comparison-এর জন্য

`PartialOrd` trait তোমাকে sorting উদ্দেশ্যে কোনো type-ের instance তুলনা করতে দেয়। `PartialOrd` implement করে এমন একটি type `<`, `>`, `<=`, এবং `>=` operator সহ ব্যবহার করা যায়। তুমি শুধুমাত্র এমন type-এ `PartialOrd` trait প্রয়োগ করতে পারো যেগুলো `PartialEq`-ও implement করে।

`PartialOrd` derive করলে `partial_cmp` method implement হয়, যা একটি `Option<Ordering>` return করে—দেওয়া value-গুলো থেকে কোনো ordering না পাওয়া গেলে সেটি `None` হবে। এমন একটি value-র উদাহরণ যা ordering তৈরি করে না, যদিও সেই type-ের বেশিরভাগ value তুলনা করা যায়, সেটি হলো `NaN` floating point value। যেকোনো floating-point number এবং `NaN` floating-point value দিয়ে `partial_cmp` call করলে `None` return করবে।

struct-এ derive করা হলে `PartialOrd` field-গুলোকে struct definition-এ যে ক্রমে আছে সেই ক্রমে প্রতিটি field-এর value তুলনা করে দুটি instance তুলনা করে। enum-এ derive করা হলে enum definition-এ আগে declare করা variant-গুলোকে পরে তালিকাভুক্ত variant-গুলোর চেয়ে ছোট বলে ধরা হয়।

`PartialOrd` trait প্রয়োজন, উদাহরণস্বরূপ, `rand` crate-এর `gen_range` method-এর জন্য, যা একটি range expression দ্বারা উল্লেখিত range-এ একটি random value তৈরি করে।

`Ord` trait তোমাকে জানায় যে annotate করা type-এর যেকোনো দুটি value-র জন্য একটি valid ordering থাকবে। `Ord` trait `cmp` method implement করে, যা একটি `Ordering` return করে—`Option<Ordering>` নয়—কারণ সর্বদা একটি valid ordering সম্ভব। তুমি শুধুমাত্র এমন type-ে `Ord` trait প্রয়োগ করতে পারো যেগুলো `PartialOrd` ও `Eq`-ও implement করে (এবং `Eq`-র জন্য `PartialEq` প্রয়োজন)। struct ও enum-এ derive করা হলে `cmp`-এর behavior `PartialOrd`-এর derive করা `partial_cmp` implementation-এর মতোই।

`Ord` যেখানে প্রয়োজন তার একটি উদাহরণ হলো `BTreeSet<T>`-তে value store করার সময়, যা value-গুলোর sort order অনুযায়ী data store করে এমন একটি data structure।

### `Clone` এবং `Copy` — Value Duplicate করার জন্য

`Clone` trait তোমাকে একটি value-র explicit deep copy তৈরি করতে দেয়, এবং এই duplication process-এ arbitrary code run এবং heap data copy জড়িত থাকতে পারে। `Clone` সম্পর্কে আরও তথ্যের জন্য Chapter 4-র [“Variables and Data Interacting with
Clone”][variables-and-data-interacting-with-clone]<!-- ignore --> section দেখো।

`Clone` derive করলে `clone` method implement হয়, যা সম্পূর্ণ type-এর জন্য implement করা হলে type-এর প্রতিটি অংশে `clone` call করে। এর মানে হলো `Clone` derive করতে হলে type-এর সব field বা value-কেও `Clone` implement করতে হবে।

`Clone` যেখানে প্রয়োজন তার একটি উদাহরণ হলো একটি slice-এ `to_vec` method call করার সময়। slice তার ভেতরে থাকা type instance-গুলোর owner নয়, কিন্তু `to_vec` থেকে পাওয়া vector-কে তার instance-গুলোর owner হতে হবে, তাই `to_vec` প্রতিটি item-এ `clone` call করে। ফলে slice-এ store করা type-কে অবশ্যই `Clone` implement করতে হবে।

`Copy` trait তোমাকে শুধু stack-এ থাকা bit copy করে একটি value duplicate করতে দেয়; কোনো arbitrary code প্রয়োজন নেই। `Copy` সম্পর্কে আরও তথ্যের জন্য Chapter 4-র [“Stack-Only Data:
Copy”][stack-only-data-copy]<!-- ignore --> section দেখো।

`Copy` trait কোনো method define করে না, যাতে programmer-রা সেই method-গুলো overload করে কোনো arbitrary code run হচ্ছে না এই assumption ভঙ্গ করতে না পারেন। এভাবে সব programmer ধরে নিতে পারেন যে কোনো value copy করা খুব দ্রুত হবে।

তুমি এমন যেকোনো type-এ `Copy` derive করতে পারো যার সব অংশই `Copy` implement করে। `Copy` implement করে এমন একটি type-কে অবশ্যই `Clone`-ও implement করতে হবে, কারণ `Copy` implement করে এমন type-এর `Clone`-এর একটি trivial implementation থাকে যা `Copy`-র মতোই কাজ করে।

`Copy` trait খুব কমই প্রয়োজন হয়; `Copy` implement করে এমন type-গুলোতে optimization সম্ভব, অর্থাৎ তোমাকে `clone` call করতে হয় না, যা code-কে আরও সংক্ষিপ্ত করে।

`Copy` দিয়ে যা করা যায় তা তুমি `Clone` দিয়েও করতে পারো, কিন্তু code ধীর হতে পারে বা কিছু জায়গায় `clone` ব্যবহার করতে হতে পারে।

### `Hash` — Value-কে Fixed Size-এর Value-তে Map করার জন্য

`Hash` trait তোমাকে arbitrary size-এর কোনো type-ের instance নিয়ে একটি hash function ব্যবহার করে সেই instance-কে fixed size-ের একটি value-তে map করতে দেয়। `Hash` derive করলে `hash` method implement হয়। `hash` method-এর derived implementation type-ের প্রতিটি অংশে `hash` call করার ফলাফল একত্রিত করে, যার মানে হলো `Hash` derive করতে হলে সব field বা value-কেও `Hash` implement করতে হবে।

`Hash` যেখানে প্রয়োজন তার একটি উদাহরণ হলো `HashMap<K, V>`-তে key store করা, যাতে data দক্ষতার সাথে store করা যায়।

### `Default` — Default Value-এর জন্য

`Default` trait তোমাকে একটি type-ের জন্য default value তৈরি করতে দেয়। `Default` derive করলে `default` function implement হয়। `default` function-এর derived implementation type-ের প্রতিটি অংশে `default` function call করে, যার মানে হলো `Default` derive করতে হলে type-ের সব field বা value-কেও `Default` implement করতে হবে।

`Default::default` function সাধারণত Chapter 5-র [“Creating Instances from Other Instances with
Struct Update
Syntax”][creating-instances-from-other-instances-with-struct-update-syntax]<!--
ignore --> section-এ আলোচিত struct update syntax-এর সাথে মিলে ব্যবহৃত হয়। তুমি একটি struct-ের কয়েকটি field customize করতে পারো এবং তারপর `..Default::default()` ব্যবহার করে বাকি field-গুলোর জন্য একটি default value set করতে পারো।

`Default` trait প্রয়োজন হয়, উদাহরণস্বরূপ, তুমি যখন `Option<T>` instance-এ `unwrap_or_default` method ব্যবহার করো। `Option<T>` যদি `None` হয়, তাহলে `unwrap_or_default` method `Option<T>`-তে store করা `T` type-এর জন্য `Default::default`-এর ফলাফল return করবে।

[creating-instances-from-other-instances-with-struct-update-syntax]: ch05-01-defining-structs.html#creating-instances-from-other-instances-with-struct-update-syntax
[stack-only-data-copy]: ch04-01-what-is-ownership.html#stack-only-data-copy
[variables-and-data-interacting-with-clone]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-clone
[custom-derive-macros]: ch20-05-macros.html#custom-derive-macros

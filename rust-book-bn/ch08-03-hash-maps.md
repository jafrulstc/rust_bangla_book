## Hash Map-এ Key সহ সম্পর্কিত Value Store করা

আমাদের common collection-গুলোর মধ্যে শেষ হলো hash map। `HashMap<K, V>` type একটি _hashing function_ ব্যবহার করে `K` type-এর key থেকে `V` type-এর value-তে mapping store করে, যে function নির্ধারণ করে এই key ও value গুলোকে মেমরিতে কীভাবে রাখা হবে। অনেক programming language এ ধরনের data structure support করে, কিন্তু তারা প্রায়ই ভিন্ন নাম ব্যবহার করে, যেমন _hash_, _map_, _object_, _hash table_, _dictionary_, বা _associative array_—এছাড়াও আরও অনেক।

Hash map তখন কাজে লাগে যখন তুমি data-কে vector-এর মতো index দিয়ে নয়, বরং যেকোনো type-এর হতে পারে এমন একটি key দিয়ে খুঁজতে চাও। যেমন, একটি game-তে তুমি প্রতিটি দলের score একটি hash map-এ রাখতে পারো যেখানে প্রতিটি key হবে দলের নাম এবং value হবে দলের score। একটি দলের নাম দিলেই তুমি তার score বের করতে পারবে।

এই section-এ আমরা hash map-এর basic API দেখব, কিন্তু standard library দ্বারা `HashMap<K, V>`-তে define করা function-গুলোতে আরও অনেক সুবিধা লুকিয়ে আছে। সবসময়ের মতো আরও তথ্যের জন্য standard library documentation দেখো।

### নতুন Hash Map তৈরি করা

খালি একটি hash map তৈরি করার একটি উপায় হলো `new` ব্যবহার করা এবং `insert` দিয়ে element যোগ করা। Listing 8-20-তে আমরা দুটি দলের score ট্র্যাক করছি যাদের নাম _Blue_ ও _Yellow_। Blue দলের শুরুর score 10 এবং Yellow দলের শুরুর score 50।

<Listing number="8-20" caption="নতুন একটি hash map তৈরি করে কিছু key ও value insert করা">

```rust
    use std::collections::HashMap;

    let mut scores = HashMap::new();

    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Yellow"), 50);
```

</Listing>

খেয়াল করো যে আমাদের প্রথমে standard library-এর collections অংশ থেকে `HashMap`-কে `use` করতে হয়। আমাদের তিনটি common collection-এর মধ্যে এটিই সবচেয়ে কম ব্যবহৃত, তাই prelude-এ স্বয়ংক্রিয়ভাবে scope-এ আনা feature-গুলোর মধ্যে এটি নেই। Hash map-গুলো standard library থেকে কম সাপোর্ট পায়; যেমন এগুলো তৈরি করার জন্য কোনো built-in macro নেই।

Vector-এর মতোই hash map তাদের data heap-এ store করে। এই `HashMap`-এর key গুলো `String` type-এর এবং value গুলো `i32` type-এর। Vector-এর মতোই, hash map ও homogeneous: সব key-এর একই type হতে হবে এবং সব value-এর একই type হতে হবে।

### Hash Map-এ Value Access করা

আমরা `get` method-এ একটি key দিয়ে hash map থেকে একটি value বের করতে পারি, Listing 8-21-তে যেমন দেখানো হয়েছে।

<Listing number="8-21" caption="Hash map-এ store করা Blue দলের score access করা">

```rust
    use std::collections::HashMap;

    let mut scores = HashMap::new();

    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Yellow"), 50);

    let team_name = String::from("Blue");
    let score = scores.get(&team_name).copied().unwrap_or(0);
```

</Listing>

এখানে `score`-এ Blue দলের সাথে যুক্ত value থাকবে এবং result হবে `10`। `get` method একটি `Option<&V>` ফেরত দেয়; যদি সেই key-এর জন্য hash map-এ কোনো value না থাকে, তাহলে `get` `None` ফেরত দেবে। এই program `Option`-টিকে `copied` কল করে `Option<&i32>`-এর বদলে একটি `Option<i32>` পেতে handle করে, তারপর `unwrap_or` দিয়ে `scores`-এ সেই key-এর জন্য entry না থাকলে `score`-এর মান শূন্য করতে হ্যান্ডল করে।

আমরা vector-এর মতোই একটি `for` loop ব্যবহার করে একটি hash map-এর প্রতিটি key-value pair-এর উপর iterate করতে পারি:

```rust
    use std::collections::HashMap;

    let mut scores = HashMap::new();

    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Yellow"), 50);

    for (key, value) in &scores {
        println!("{key}: {value}");
    }
```

এই code প্রতিটি pair একটি অনির্দিষ্ট ক্রমে print করবে:

```text
Yellow: 50
Blue: 10
```

<!-- Old headings. Do not remove or links may break. -->

<a id="hash-maps-and-ownership"></a>

### Hash Map-এ Ownership Manage করা

`i32`-এর মতো `Copy` trait implement করা type-এর জন্য value গুলো hash map-এ copy হয়। `String`-এর মতো owned value-এর জন্য value গুলো move হবে এবং hash map সেই value-গুলোর owner হবে, Listing 8-22-তে যেমন দেখানো হয়েছে।

<Listing number="8-22" caption="Key ও value insert হওয়ার পর hash map-এর মালিকানাধীন হয়ে যাওয়া দেখানো হচ্ছে">

```rust
    use std::collections::HashMap;

    let field_name = String::from("Favorite color");
    let field_value = String::from("Blue");

    let mut map = HashMap::new();
    map.insert(field_name, field_value);
    // field_name and field_value are invalid at this point, try using them and
    // see what compiler error you get!
```

</Listing>

`insert` কলের মাধ্যমে hash map-এ move হওয়ার পর আমরা `field_name` ও `field_value` variable গুলো আর ব্যবহার করতে পারি না।

যদি আমরা value-গুলোর reference গুলো hash map-এ insert করি, তাহলে value গুলো hash map-এ move হবে না। Reference গুলো যে value-কে point করে সেগুলো অন্তত ততটা সময় বৈধ থাকতে হবে যতটা সময় hash map বৈধ। আমরা এই বিষয়গুলো নিয়ে Chapter 10-এর [“Validating References with
Lifetimes”][validating-references-with-lifetimes]<!-- ignore -->-এ আরও কথা বলব।

### Hash Map আপডেট করা

যদিও key ও value pair-গুলোর সংখ্যা grow করতে পারে, প্রতিটি unique key-এর সাথে একই সময়ে শুধু একটিই value যুক্ত থাকতে পারে (কিন্তু উল্টোটা সত্য নয়: যেমন, Blue ও Yellow দুটি দলের সাথেই `scores` hash map-এ `10` value store থাকতে পারে)।

যখন তুমি একটি hash map-এর data পরিবর্তন করতে চাইবে, তখন তোমাকে স্থির করতে হবে যে কোনো key-এর সাথে ইতিমধ্যে value assign করা থাকলে সেটা কীভাবে handle করবে। তুমি পুরোনো value-কে নতুন value দিয়ে replace করতে পারো, পুরোনো value সম্পূর্ণ উপেক্ষা করে। তুমি পুরোনো value রেখে নতুন value উপেক্ষা করতে পারো, যেন নতুন value শুধু তখনই যোগ হয় যখন key-এর সাথে আগে কোনো value _নেই_। অথবা তুমি পুরোনো ও নতুন value একত্র করতে পারো। চলো দেখি প্রতিটি কীভাবে করতে হয়!

#### একটি Value Overwrite করা

আমরা যদি একটি hash map-এ একটি key ও value insert করি এবং তারপর একই key-এর সাথে ভিন্ন value insert করি, তাহলে সেই key-এর সাথে যুক্ত value replace হয়ে যাবে। Listing 8-23-এর code যদিও `insert` দুবার কল করে, hash map-এ একটিমাত্র key-value pair থাকবে কারণ আমরা উভয় বারই Blue দলের key-এর জন্য value insert করছি।

<Listing number="8-23" caption="একটি নির্দিষ্ট key-এর সাথে store করা value replace করা">

```rust
    use std::collections::HashMap;

    let mut scores = HashMap::new();

    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Blue"), 25);

    println!("{scores:?}");
```

</Listing>

এই code `{"Blue": 25}` print করবে। পুরোনো `10` value-টি overwrite হয়ে গেছে।

<!-- Old headings. Do not remove or links may break. -->

<a id="only-inserting-a-value-if-the-key-has-no-value"></a>

#### শুধুমাত্র Key বিদ্যমান না থাকলে Key ও Value যোগ করা

প্রায়শই দেখা যায় যে কোনো নির্দিষ্ট key-এর সাথে ইতিমধ্যে value আছে কিনা তা check করা এবং তারপর নিচের কাজগুলো করা: যদি hash map-এ সেই key থাকে, তাহলে বিদ্যমান value যেমন আছে তেমনই থাকবে; যদি key না থাকে, তাহলে সেটি ও তার জন্য একটি value insert করা।

Hash map-এ এই কাজের জন্য একটি special API আছে যাকে `entry` বলা হয়, যা তোমার check করতে চাওয়া key-টিকে parameter হিসেবে নেয়। `entry` method-এর return value হলো `Entry` নামের একটি enum, যা এমন একটি value represent করে যা থাকতেও পারে আবার নাও থাকতে পারে। ধরো আমরা check করতে চাই যে Yellow দলের key-এর সাথে কোনো value যুক্ত আছে কিনা। যদি না থাকে, আমরা value `50` insert করতে চাই, এবং Blue দলের জন্যও একই। `entry` API ব্যবহার করলে code-টা দেখতে Listing 8-24-এর মতো।

<Listing number="8-24" caption="`entry` method ব্যবহার করে শুধু তখনই insert করা যখন key-এর আগে থেকে কোনো value নেই">

```rust
    use std::collections::HashMap;

    let mut scores = HashMap::new();
    scores.insert(String::from("Blue"), 10);

    scores.entry(String::from("Yellow")).or_insert(50);
    scores.entry(String::from("Blue")).or_insert(50);

    println!("{scores:?}");
```

</Listing>

`Entry`-তে `or_insert` method-টি এমনভাবে define করা যে এটি সংশ্লিষ্ট `Entry` key-এর জন্য value-তে একটি mutable reference ফেরত দেয় যদি সেই key বিদ্যমান থাকে, আর যদি না থাকে তাহলে parameter-টিকে এই key-এর জন্য নতুন value হিসেবে insert করে নতুন value-তে একটি mutable reference ফেরত দেয়। এই technique নিজে আমরা logic লেখার চেয়ে অনেক পরিষ্কার, এবং এছাড়া এটি borrow checker-এর সাথেও ভালোভাবে কাজ করে।

Listing 8-24-এর code run করলে `{"Yellow": 50, "Blue": 10}` print করবে। `entry`-তে প্রথম কলটি Yellow দলের key-টিকে value `50` সহ insert করবে কারণ Yellow দলের আগে থেকে কোনো value নেই। `entry`-তে দ্বিতীয় কলটি hash map-কে পরিবর্তন করবে না, কারণ Blue দলের আগে থেকেই value `10` আছে।

#### পুরোনো Value-এর ভিত্তিতে Value আপডেট করা

Hash map-এর আরেকটি সাধারণ use case হলো একটি key-এর value খুঁজে বের করা এবং পুরোনো value-এর ভিত্তিতে সেটি আপডেট করা। যেমন, Listing 8-25 এমন code দেখায় যা কোনো text-এ প্রতিটি শব্দ কতবার এসেছে তা count করে। আমরা শব্দগুলোকে key হিসেবে রেখে একটি hash map ব্যবহার করি এবং একটি শব্দ কতবার দেখা গেছে তা ট্র্যাক করতে value increment করি। যদি কোনো শব্দ আমরা প্রথমবার দেখি, তাহলে আমরা আগে value `0` insert করব।

<Listing number="8-25" caption="শব্দ ও count store করে এমন একটি hash map ব্যবহার করে শব্দের occurrence count করা">

```rust
    use std::collections::HashMap;

    let text = "hello world wonderful world";

    let mut map = HashMap::new();

    for word in text.split_whitespace() {
        let count = map.entry(word).or_insert(0);
        *count += 1;
    }

    println!("{map:?}");
```

</Listing>

এই code `{"world": 2, "hello": 1, "wonderful": 1}` print করবে। তুমি হয়তো একই key-value pair ভিন্ন ক্রমে print হতে দেখবে: [“Accessing
Values in a Hash Map”][access]<!-- ignore -->-এ বলা হয়েছে যে একটি hash map-এর উপর iterate হয় অনির্দিষ্ট ক্রমে।

`split_whitespace` method `text`-এর value-এর whitespace দিয়ে আলাদা করা subslice-গুলোর উপর একটি iterator ফেরত দেয়। `or_insert` method নির্দিষ্ট key-এর জন্য value-তে একটি mutable reference (`&mut V`) ফেরত দেয়। এখানে আমরা সেই mutable reference-টি `count` variable-এ রাখি, তাই সেই value-তে assign করতে হলে আমাদের প্রথমে asterisk (`*`) দিয়ে `count`-কে dereference করতে হবে। Mutable reference-টি `for` loop শেষে scope ছেড়ে দেয়, তাই এই পরিবর্তনগুলো safe এবং borrowing rule-এর অধীনে allowed।

### Hashing Function

By default, `HashMap` _SipHash_ নামের একটি hashing function ব্যবহার করে যা hash table জড়িত denial-of-service (DoS) attack প্রতিরোধে সাহায্য করে[^siphash]<!-- ignore -->। এটি available সবচেয়ে দ্রুত hashing algorithm নয়, কিন্তু কম performance-এর বিনিময়ে যে উন্নত security পাওয়া যায় সেটা এর মূল্যবান। তুমি যদি তোমার code profile করে দেখো যে default hash function তোমার কাজের জন্য খুব ধীর, তাহলে একটি ভিন্ন hasher specify করে অন্য function-এ পরিবর্তন করতে পারো। একটি _hasher_ হলো এমন একটি type যা `BuildHasher` trait implement করে। Trait এবং সেগুলো কীভাবে implement করতে হয় সে সম্পর্কে আমরা [Chapter 10][traits]<!-- ignore -->-তে কথা বলব। তোমার নিজের hasher শুরু থেকে implement করার দরকার নেই; [crates.io](https://crates.io/)<!-- ignore -->-তে অন্যান্য Rust user-দের share করা library আছে যেগুলো অনেক সাধারণ hashing algorithm implement করা hasher দেয়।

[^siphash]: [https://en.wikipedia.org/wiki/SipHash](https://en.wikipedia.org/wiki/SipHash)

## Summary

Vector, string এবং hash map data store করতে, access করতে ও modify করতে program-এ প্রয়োজনীয় অনেক বড় অংশের functionality দেয়। এখানে কিছু exercise দেওয়া হলো যা তুমি এখন সমাধান করতে পারবে:

1. একটি integer list দেওয়া আছে, একটি vector ব্যবহার করে list-এর median (sort করা অবস্থায় মাঝখানের position-এর value) এবং mode (যে value-টি সবচেয়ে বেশি বার আসে; এখানে একটি hash map কাজে লাগবে) ফেরত দাও।
1. String-গুলোকে Pig Latin-এ convert করো। প্রতিটি শব্দের প্রথম consonant-টি শব্দের শেষে সরিয়ে _ay_ যোগ করো, যাতে _first_ হয়ে যায় _irst-fay_। Vowel দিয়ে শুরু হওয়া শব্দের শেষে এর বদলে _hay_ যোগ করো (_apple_ হয়ে যায় _apple-hay_)। UTF-8 encoding সম্পর্কে বিস্তারিত মনে রেখো!
1. একটি hash map ও vector ব্যবহার করে এমন একটি text interface তৈরি করো যা একজন user-কে একটি company-র কোনো department-এ employee নাম যোগ করতে দেয়; যেমন “Add Sally to
   Engineering” বা “Add Amir to Sales.” তারপর user-কে একটি department-এর সব মানুষের list বা পুরো company-র সব মানুষের list department অনুযায়ী alphabet-এর ক্রমে সাজানো অবস্থায় দেখতে দাও।

Standard library API documentation-এ vector, string এবং hash map-এর সেইসব method বর্ণনা করা আছে যা এই exercise-গুলোতে কাজে লাগবে!

আমরা এখন এমন সব জটিল program-এ প্রবেশ করছি যেখানে operation fail করতে পারে, তাই error handling নিয়ে আলোচনা করার এটাই উপযুক্ত সময়। পরেরে আমরা সেটাই করব!

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[access]: #accessing-values-in-a-hash-map
[traits]: ch10-02-traits.html

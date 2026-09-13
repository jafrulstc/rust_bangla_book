## Object-Oriented Language গুলোর বৈশিষ্ট্য

একটা ভাষাকে object-oriented হিসেবে গণ্য করার জন্য কোন কোন feature থাকা আবশ্যক—প্রোগ্রামিং community-তে এ নিয়ে কোনো ঐকমত্য নেই। Rust অনেক প্রোগ্রামিং paradigm দ্বারা প্রভাবিত, যার মধ্যে OOP-ও আছে; যেমন Chapter 13-এ আমরা functional programming থেকে আসা feature গুলো নিয়ে আলোচনা করেছি। যুক্তি দেওয়া যায় যে OOP ভাষাগুলো কিছু সাধারণ বৈশিষ্ট্য ভাগ করে নেয়—যেমন object, encapsulation এবং inheritance। চলো দেখি প্রতিটি বৈশিষ্ট্যের অর্থ কী এবং Rust সেটা সমর্থন করে কি না।

### Object গুলো Data এবং Behavior ধারণ করে

Erich Gamma, Richard Helm, Ralph Johnson এবং John Vlissides-এর লেখা (Addison-Wesley, 1994) _Design Patterns: Elements of Reusable Object-Oriented Software_ বইটি—যাকে colloquially _The Gang of Four_ বলা হয়—হলো object-oriented design pattern গুলোর একটি তালিকা। সেই বই OOP-কে এভাবে সংজ্ঞায়িত করেছে:

> Object-oriented program গুলো object দিয়ে তৈরি হয়। একটি **object** তার data এবং সেই data-এর ওপর কাজ করা procedure গুলোকে একসাথে package করে। সেই procedure গুলোকে সাধারণত **method** বা **operation** বলা হয়।

এই সংজ্ঞা ব্যবহার করলে, Rust object-oriented: struct এবং enum-এর data থাকে, এবং `impl` block-এর মাধ্যমে struct ও enum-এ method যোগ করা যায়। যদিও method সহ struct এবং enum-কে _object_ বলা হয় না, Gang of Four-এর object-এর সংজ্ঞা অনুসারে এগুলো একই functionality দেয়।

### Implementation Detail লুকানোর জন্য Encapsulation

OOP-এর সাথে সাধারণত যে বিষয়টি যুক্ত থাকে তা হলো _encapsulation_-এর ধারণা, যার মানে হলো—একটি object-এর implementation detail সেই object ব্যবহার করা code-এর কাছে অ্যাক্সেসযোগ্য নয়। তাই একটি object-এর সাথে ইন্টারঅ্যাক্ট করার একমাত্র উপায় হলো তার public API; object ব্যবহার করা code সরাসরি object-এর ভেতরের অংশে হাত দিয়ে data বা behavior পরিবর্তন করতে পারবে না। এতে programmer একটি object-এর ভেতরের অংশ change বা refactor করতে পারেন, কিন্তু সেই object ব্যবহার করা code পরিবর্তন করতে হয় না।

Chapter 7-এ আমরা আলোচনা করেছি কীভাবে encapsulation নিয়ন্ত্রণ করা যায়: আমরা `pub` keyword ব্যবহার করে ঠিক করতে পারি আমাদের code-এর কোন module, type, function এবং method public থাকবে, আর default হিসেবে বাকি সবকিছু private থাকবে। উদাহরণ হিসেবে ধরো আমরা একটি `AveragedCollection` struct define করতে চাই যার একটি field-এ `i32` value-গুলোর একটি vector থাকবে। সেই struct-এ আরও একটি field থাকতে পারে যেখানে vector-এর সব value-গুলোর average রাখা থাকবে, যাতে কেউ প্রয়োজন করলেই সেটা বারবার হিসাব করতে না হয়। অর্থাৎ `AveragedCollection` আমাদের জন্য হিসাব করা average টা cache করে রাখবে। Listing 18-1-এ `AveragedCollection` struct-টির definition দেওয়া আছে।

<Listing number="18-1" file-name="src/lib.rs" caption="একটি `AveragedCollection` struct যা integer-গুলোর একটি list এবং collection-এর item-গুলোর average রাখে">

```rust,noplayground
pub struct AveragedCollection {
    list: Vec<i32>,
    average: f64,
}
```

</Listing>

struct-টিকে `pub` করে দেওয়া হয়েছে যাতে অন্য code সেটি ব্যবহার করতে পারে, কিন্তু struct-এর ভেতরের field গুলো private থাকে। এটা এখানে জরুরি কারণ আমরা নিশ্চিত করতে চাই যেখানেই list-এ কোনো value যোগ বা বাদ দেওয়া হবে, সেখানেই average-ও আপডেট হবে। এটা আমরা করি struct-এর ওপর `add`, `remove` এবং `average` method implement করার মাধ্যমে, যেমনটা Listing 18-2-তে দেখানো হয়েছে।

<Listing number="18-2" file-name="src/lib.rs" caption="`AveragedCollection`-এর ওপর public method `add`, `remove` এবং `average`-এর implementation">

```rust,noplayground
impl AveragedCollection {
    pub fn add(&mut self, value: i32) {
        self.list.push(value);
        self.update_average();
    }

    pub fn remove(&mut self) -> Option<i32> {
        let result = self.list.pop();
        match result {
            Some(value) => {
                self.update_average();
                Some(value)
            }
            None => None,
        }
    }

    pub fn average(&self) -> f64 {
        self.average
    }

    fn update_average(&mut self) {
        let total: i32 = self.list.iter().sum();
        self.average = total as f64 / self.list.len() as f64;
    }
}
```

</Listing>

Public method `add`, `remove` এবং `average`-ই হলো `AveragedCollection`-এর কোনো instance-এর data-তে অ্যাক্সেস বা পরিবর্তন করার একমাত্র উপায়। যখন `add` method দিয়ে `list`-এ কোনো item যোগ করা হয় বা `remove` method দিয়ে সরানো হয়, তখন প্রতিটি implementation private `update_average` method-কে call করে, যা `average` field আপডেট করার কাজও সামলায়।

আমরা `list` এবং `average` field গুলো private রেখেছি, যাতে external code সরাসরি `list` field-এ item যোগ বা অপসারণ করতে না পারে; তা না হলে `list` পরিবর্তনের সময় `average` field সিঙ্কের বাইরে চলে যেতে পারে। `average` methodটি `average` field-এর value return করে, ফলে external code `average` পড়তে পারে কিন্তু পরিবর্তন করতে পারে না।

যেহেতু আমরা `AveragedCollection` struct-এর implementation detail encapsulate করে রেখেছি, তাই ভবিষ্যতে আমরা সহজেই কিছু দিক পরিবর্তন করতে পারবো, যেমন data structure। উদাহরণ হিসেবে `list` field-এর জন্য `Vec<i32>`-এর বদলে আমরা `HashSet<i32>` ব্যবহার করতে পারি। যতক্ষণ `add`, `remove` এবং `average` public method-গুলোর signature একই থাকবে, `AveragedCollection` ব্যবহার করা code পরিবর্তন করতে হবে না। যদি আমরা `list`-কে public করতাম, তাহলে ব্যাপারটা এরকম হতো না: `HashSet<i32>` এবং `Vec<i32>`-এর item যোগ-অপসারণের method আলাদা, তাই external code সরাসরি `list` modify করলে সম্ভবত সেটাও পরিবর্তন করতে হতো।

যদি কোনো ভাষাকে object-oriented ধরার জন্য encapsulation একটি আবশ্যকীয় বৈশিষ্ট্য হয়, তাহলে Rust সেই শর্ত পূরণ করে। code-এর বিভিন্ন অংশে `pub` ব্যবহার করা যাবে কি না—এই option-ই implementation detail-এর encapsulation সক্ষম করে।

### Inheritance: Type System এবং Code Sharing হিসেবে

_Inheritance_ হলো এমন একটি mechanism যার মাধ্যমে একটি object অন্য একটি object-এর definition থেকে element inherit করতে পারে, ফলে parent object-এর data এবং behavior সেটি পেয়ে যায়, আর তোমাকে সেগুলো আবার define করতে হয় না।

যদি কোনো ভাষার object-oriented হওয়ার জন্য inheritance থাকা জরুরি হয়, তাহলে Rust সেই রকম ভাষা নয়। কোনো macro ছাড়া এমন কোনো struct define করার উপায় নেই যা parent struct-এর field এবং method implementation inherit করবে।

তবে তোমার প্রোগ্রামিং toolbox-এ যদি inheritance থাকার অভ্যাস থাকে, তাহলে Rust-এ অন্যান্য সমাধান ব্যবহার করতে পারো—কোন সমাধানটা মানানসই হবে তা নির্ভর করে তুমি মূলত কেন inheritance ব্যবহার করতে চেয়েছিলে তার ওপর।

তুমি মূলত দুটি কারণে inheritance বেছে নিতে পারো। একটি হলো code reuse: তুমি একটি type-এর জন্য কোনো নির্দিষ্ট behavior implement করলে, inheritance সেই implementation অন্য type-এর জন্য আবার ব্যবহার করার সুযোগ দেয়। Rust-এ এটা সীমিত আকারে করা যায় default trait method implementation ব্যবহার করে, যেটা তুমি Listing 10-14-এ দেখেছিলে যখন আমরা `Summary` trait-এ `summarize` method-এর একটি default implementation যোগ করেছিলাম। যেকোনো type যেটা `Summary` trait implement করবে, সেটার ওপর কোনো বাড়তি code ছাড়াই `summarize` method পাওয়া যাবে। এটা অনেকটা সেই ব্যাপারের মতো যেখানে parent class-এ একটি method-এর implementation থাকে এবং inherit করা child class-এও সেই method-এর implementation থাকে। আমরা `Summary` trait implement করার সময় `summarize` method-এর default implementation-কে override করতে পারি, যেটা child class দিয়ে parent class থেকে inherit করা method-এর implementation override করার মতো।

Inheritance ব্যবহারের আরেকটি কারণ হলো type system-সংক্রান্ত: child type-কে parent type-এর জায়গায় ব্যবহার করতে দেওয়া। একে _polymorphism_-ও বলা হয়, যার মানে হলো—তুমি runtime-এ একাধিক object-কে একে অপরের বিকল্প হিসেবে ব্যবহার করতে পারবে যদি তারা কিছু বৈশিষ্ট্য ভাগ করে নেয়।

> ### Polymorphism
>
> অনেকের কাছে polymorphism মানেই inheritance। কিন্তু বাস্তবে এটি আরও ব্যাপক একটি ধারণা, যা এমন code-কে বোঝায় যা একাধিক type-এর data-এর সাথে কাজ করতে পারে। Inheritance-এর ক্ষেত্রে সেই type গুলো সাধারণত subclass হয়।
>
> Rust এর বদলে generic ব্যবহার করে বিভিন্ন সম্ভাব্য type-এর ওপর abstraction করে এবং trait bound ব্যবহার করে সেই type গুলোর কী কী থাকতে হবে তার constraint দেয়। একে মাঝে মাঝে _bounded parametric polymorphism_ বলা হয়।

Rust inheritance না দিয়ে এক ভিন্ন সেটের trade-off বেছে নিয়েছে। Inheritance প্রায়ই প্রয়োজনের তুলনায় বেশি code share করার ঝুঁকিতে থাকে। Subclass-কে সব সময় parent class-এর সব বৈশিষ্ট্য share করা উচিত নয়, কিন্তু inheritance থাকলে সে করবেই। এতে একটি program-এর design কম flexible হতে পারে। এছাড়াও এমন সম্ভাবনা তৈরি হয় যে subclass-এর ওপর এমন কোনো method call করা হবে যা অর্থহীন, কারণ সেই method সেই subclass-এর ক্ষেত্রে খায় না—ফলে error হতে পারে। তাছাড়া কিছু ভাষা শুধুমাত্র _single inheritance_ দেয় (অর্থাৎ একটি subclass শুধুমাত্র একটি class থেকে inherit করতে পারে), যা program-এর design-কে আরও বেশি সীমাবদ্ধ করে।

এই কারণেই Rust ভিন্ন পথে হেঁটেছে—inheritance-এর বদলে trait object ব্যবহার করে runtime-এ polymorphism অর্জন করে। চলো দেখি trait object গুলো কীভাবে কাজ করে।

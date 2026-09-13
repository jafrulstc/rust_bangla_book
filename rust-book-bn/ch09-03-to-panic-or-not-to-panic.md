## `panic!` করবে নাকি করবে না?

তাহলে, তুমি কীভাবে সিদ্ধান্ত নেবে কখন `panic!` call করবে আর কখন `Result` return করবে? যখন code panic করে, তখন recover করার কোনো উপায় থাকে না। তুমি যেকোনো error পরিস্থিতিতে `panic!` call করতে পারো, সেখানে recover করার উপায় থাকুক বা না থাকুক, কিন্তু তাহলে তুমি calling code-এর হয়ে সিদ্ধান্ত নিচ্ছ যে একটি পরিস্থিতি unrecoverable। তুমি যখন একটি `Result` value return করার সিদ্ধান্ত নাও, তুমি calling code-কে বিকল্প দাও। Calling code তার পরিস্থিতি অনুযায়ী উপযুক্ত উপায়ে recover করার চেষ্টা করতে পারে, অথবা সে সিদ্ধান্ত নিতে পারে যে এই ক্ষেত্রে একটি `Err` value unrecoverable, তাই সে `panic!` call করে তোমার recoverable error-কে একটি unrecoverable-এ পরিণত করতে পারে। সুতরাং, এমন একটি function define করার সময় যা ব্যর্থ হতে পারে, `Result` return করা একটি ভালো ডিফল্ট পছন্দ।

যেমন উদাহরণ, prototype code, এবং test-এর মতো পরিস্থিতিতে, `Result` return করার বদলে এমন code লেখা বেশি উপযুক্ত যা panic করে। চলো কেন তা দেখি, তারপর এমন পরিস্থিতি নিয়ে আলোচনা করি যেখানে compiler বুঝতে পারে না যে failure অসম্ভব, কিন্তু তুমি একজন মানুষ হিসেবে বুঝতে পারো। অধ্যায়টি library code-এ কখন panic করা উচিত তা নিয়ে কিছু সাধারণ নির্দেশিকা দিয়ে শেষ হবে।

### উদাহরণ, Prototype Code, এবং Test

তুমি যখন কোনো concept বোঝানোর জন্য একটি উদাহরণ লিখছ, সাথে শক্তিশালী error-handling code যোগ করলে উদাহরণটি কম পরিষ্কার হতে পারে। উদাহরণে, এটি বোঝানো হয় যে `unwrap`-এর মতো এমন একটি method-এ করা call যা panic করতে পারে তা একটি placeholder হিসেবে ব্যবহৃত হচ্ছে যা নির্দেশ করে তুমি তোমার application-এ error কীভাবে handle করতে চাও, যা তোমার code-এর বাকি অংশ কী করছে তার উপর ভিত্তি করে ভিন্ন হতে পারে।

একইভাবে, তুমি যখন prototype করো এবং error কীভাবে handle করবে তা এখনও সিদ্ধান্ত নেওয়ার জন্য প্রস্তুত নও, তখন `unwrap` এবং `expect` method খুবই কাজে লাগে। এগুলো তোমার code-এ স্পষ্ট marker রেখে যায় যখন তুমি তোমার program-কে আরও শক্তিশালী করতে প্রস্তুত হবে।

একটি test-এ কোনো method call ব্যর্থ হলে, তুমি চাইবে পুরো test-টি ব্যর্থ হোক, যদিও সেই method-টি test-এর অধীন functionality নাও হতে পারে। যেহেতু `panic!`-ই হলো সেই উপায় যাতে একটি test-কে failure হিসেবে চিহ্নিত করা হয়, `unwrap` বা `expect` call করাটাই হলো ঠিক যা ঘটা উচিত।

<!-- Old headings. Do not remove or links may break. -->

<a id="cases-in-which-you-have-more-information-than-the-compiler"></a>

### যখন তোমার কাছে Compiler-এর চেয়ে বেশি তথ্য থাকে

যখন তোমার কাছে এমন কোনো অন্য logic থাকে যা নিশ্চিত করে যে `Result`-এ একটি `Ok` value থাকবে, কিন্তু সেই logic এমন কিছু নয় যা compiler বোঝে, তখনও `expect` call করা উপযুক্ত। তোমার হাতে এখনও এমন একটি `Result` value থাকবে যা তোমাকে handle করতে হবে: তুমি যে operation-ই call করো না কেন সাধারণভাবে তা ব্যর্থ হওয়ার সম্ভাবনা থাকে, যদিও তোমার নির্দিষ্ট পরিস্থিতিতে এটি logically অসম্ভব। তুমি যদি code নিজে পরীক্ষা করে নিশ্চিত করতে পারো যে তুমি কখনো `Err` variant পাবে না, তবে `expect` call করা এবং argument text-এ তুমি কেন কখনো `Err` variant পাবে না বলে মনে করো তার কারণ লেখা সম্পূর্ণ গ্রহণযোগ্য। এর একটি উদাহরণ নিচে দেওয়া হলো:

```rust
    use std::net::IpAddr;

    let home: IpAddr = "127.0.0.1"
        .parse()
        .expect("Hardcoded IP address should be valid");
```

আমরা একটি hardcoded string parse করে একটি `IpAddr` instance তৈরি করছি। আমরা দেখতে পাই যে `127.0.0.1` একটি বৈধ IP address, তাই এখানে `expect` ব্যবহার করা গ্রহণযোগ্য। তবে, একটি hardcoded, বৈধ string থাকার কারণে `parse` method-এর return type পরিবর্তন হয় না: আমরা এখনও একটি `Result` value পাই, এবং compiler এখনও আমাদের `Result`-কে এমনভাবে handle করতে বাধ্য করবে যেন `Err` variant একটি সম্ভাবনা, কারণ compiler এতটা বুদ্ধিমান নয় যে দেখতে পারে এই string সবসময় একটি বৈধ IP address। যদি IP address string-টি program-এ hardcoded না হয়ে কোনো user-এর কাছ থেকে আসত এবং তাই failure-এর সম্ভাবনা _থাকত_, তবে আমরা অবশ্যই `Result`-কে আরও শক্তিশালী উপায়ে handle করতে চাইতাম। এই IP address-টি hardcoded এই assumption-টি উল্লেখ করা আমাদেরকে স্মরণ করিয়ে দেবে যে ভবিষ্যতে যদি আমাদের এই IP address অন্য কোনো source থেকে নিতে হয়, তখল `expect`-কে আরও ভালো error-handling code-এ পরিবর্তন করতে হবে।

### Error Handling-এর নির্দেশিকা

তোমার code-এ এমন পরিস্থিতি হতে পারে যেখানে সে একটি খারাপ অবস্থায় পৌঁছাতে পারে, সে ক্ষেত্রে code-কে panic করানো পরামর্শযোগ্য। এই context-এ, একটি _bad state_ হলো যখন কোনো assumption, guarantee, contract, বা invariant ভেঙে যায়, যেমন তোমার code-কে invalid value, contradictory value, বা missing value পাস করা হয়—তার সাথে নিচের এক বা তার বেশি শর্ত প্রযোজ্য:

- এই bad state-টি এমন কিছু যা অপ্রত্যাশিত, যেমন একজন user-এর ভুল format-এ data লেখার বিপরীতে যা মাঝে মাঝে ঘটার সম্ভাবনা থাকে।
- এর পরের তোমার code-কে এই bad state-এ না থাকার উপর নির্ভর করতে হবে, প্রতি ধাপে সমস্যাটি যাচাই করার বদলে।
- এই তথ্য তুমি যে type ব্যবহার করো তাতে encode করার কোনো ভালো উপায় নেই। আমরা Chapter 18-এর [“Encoding States and Behavior as
  Types”][encoding]<!-- ignore --> section-এ এর একটি উদাহরণ নিয়ে কাজ করব।

কেউ যদি তোমার code call করে এবং এমন value পাস করে যা অর্থহীন, তবে যদি পারো একটি error return করাটা সবচেয়ে ভালো যাতে library-টির user সেই ক্ষেত্রে কী করতে চায় তা সিদ্ধান্ত নিতে পারে। তবে, এমন ক্ষেত্রে যেখানে চালিয়ে যাওয়া insecure বা ক্ষতিকর হতে পারে, সেরা পছন্দ হতে পারে `panic!` call করা এবং তোমার library ব্যবহারকারী ব্যক্তিকে তার code-এর bug সম্পর্কে সতর্ক করা যাতে সে development-এর সময় সেটি ঠিক করতে পারে। একইভাবে, তুমি যদি এমন কোনো external code call করো যা তোমার নিয়ন্ত্রণের বাইরে এবং যা এমন একটি invalid state return করে যা তোমার ঠিক করার কোনো উপায় নেই, সেক্ষেত্রেও `panic!` প্রায়ই উপযুক্ত।

তবে, যখন failure প্রত্যাশিত, তখন একটি `panic!` call করার চেয়ে একটি `Result` return করা বেশি উপযুক্ত। উদাহরণ হিসেবে একটি parser-কে বিকৃত data দেওয়া অথবা একটি HTTP request এমন একটি status return করা যা নির্দেশ করে যে তুমি একটি rate limit-এ পৌঁছেছ। এই ক্ষেত্রে, একটি `Result` return করা নির্দেশ করে যে failure একটি প্রত্যাশিত সম্ভাবনা যা calling code-কে সিদ্ধান্ত নিতে হবে কীভাবে handle করতে হবে।

যখন তোমার code এমন একটি operation সম্পাদন করে যা invalid value দিয়ে call করা হলে user-কে risk-এ ফেলতে পারে, তখন তোমার code-কে প্রথমে value গুলো বৈধ কিনা তা যাচাই করা উচিত এবং value বৈধ না হলে panic করা উচিত। এটি মূলত safety-এর কারণে: invalid data-এর উপর operation চালানো তোমার code-কে vulnerability-এর সম্মুখীন করতে পারে। এটিই মূল কারণ যে standard library তুমি একটি out-of-bounds memory access চেষ্টা করলে `panic!` call করবে: এমন memory-কে অ্যাক্সেস করার চেষ্টা করা যা current data structure-এর নয় সেটি একটি সাধারণ security সমস্যা। Function-এর প্রায়ই _contract_ থাকে: তাদের behavior তখনই guaranteed যখন input গুলো নির্দিষ্ট requirement পূরণ করে। contract ভাঙা হলে panic করাটা যুক্তিযুক্ত, কারণ একটি contract violation সবসময় caller-পক্ষের একটি bug নির্দেশ করে, এবং এটি এমন ধরনের error নয় যা তুমি চাইবে calling code-কে স্পষ্টভাবে handle করতে হবে। প্রকৃতপক্ষে, calling code-এর জন্য recover করার কোনো যুক্তিযুক্ত উপায় নেই; calling _programmer_-দের code ঠিক করতে হবে। একটি function-এর contract, বিশেষ করে যখন একটি violation panic ঘটাবে, তা function-টির API documentation-এ ব্যাখ্যা করা উচিত।

তবে, তোমার সব function-এ অনেক error check থাকলে তা verbose এবং বিরক্তিকর হবে। ভাগ্যক্রমে, তুমি Rust-এর type system (এবং ফলে compiler দ্বারা করা type checking) ব্যবহার করে অনেক check তোমার হয়ে করিয়ে নিতে পারো। তোমার function-এর যদি একটি নির্দিষ্ট type parameter হিসেবে থাকে, তুমি তোমার code-এর logic চালিয়ে যেতে পারো জেনে যে compiler ইতিমধ্যে নিশ্চিত করেছে যে তোমার কাছে একটি বৈধ value আছে। যেমন, তোমার যদি `Option`-এর বদলে একটি type থাকে, তোমার program প্রত্যাশা করে _nothing_ এর বদলে _something_ থাকবে। তখন তোমার code-কে `Some` এবং `None` variant-এর জন্য দুটি case handle করতে হবে না: এর শুধু একটি case থাকবে যেখানে নিশ্চিতভাবে একটি value আছে। তোমার function-কে কিছু না পাস করার চেষ্টা করা code এমনকি compile-ও হবে না, তাই তোমার function-কে সেই case-টি runtime-এ check করতে হবে না। আরেকটি উদাহরণ হলো `u32`-এর মতো একটি unsigned integer type ব্যবহার করা, যা নিশ্চিত করে যে parameter কখনো negative হবে না।

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-custom-types-for-validation"></a>

### Validation-এর জন্য Custom Type

চলো Rust-এর type system ব্যবহার করে একটি বৈধ value নিশ্চিত করার ধারণাটিকে এক ধাপ এগিয়ে নিয়ে যাই এবং validation-এর জন্য একটি custom type তৈরি করা দেখি। Chapter 2-এর guessing game-টি মনে করো যেখানে আমাদের code user-কে ১ থেকে ১০০-এর মধ্যে একটি সংখ্যা guess করতে বলত। আমরা কখনো যাচাই করিনি যে user-এর guess আমাদের secret number-এর সাথে মেলানোর আগে সেই সংখ্যা গুলোর মধ্যে আছে কি না; আমরা শুধু যাচাই করেছিলাম যে guess-টি positive। এই ক্ষেত্রে, পরিণতি খুব ভয়াবহ ছিল না: আমাদের “Too high” বা “Too low” output এখনও সঠিক থাকত। কিন্তু এটি একটি কার্যকর উন্নতি হতো যাতে user-কে বৈধ guess-এর দিকে পরিচালিত করা যায় এবং যখন user সীমার বাইরের একটি সংখ্যা guess করে তখন ভিন্ন behavior দেখানো যায়, যেমন যখন user অক্ষর লেখে।

এটি করার একটি উপায় হলো guess-টিকে শুধু `u32` না করে সম্ভাব্য negative সংখ্যা অনুমোদন করতে একটি `i32` হিসেবে parse করা, এবং তারপর সংখ্যাটি সীমার মধ্যে আছে কি না তার একটি check যোগ করা, এভাবে:

<Listing file-name="src/main.rs">

```rust,ignore
    loop {
        // --snip--

        let guess: i32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };

        if guess < 1 || guess > 100 {
            println!("The secret number will be between 1 and 100.");
            continue;
        }

        match guess.cmp(&secret_number) {
            // --snip--
    }
```

</Listing>

`if` expression-টি যাচাই করে যে আমাদের value সীমার বাইরে আছে কি না, user-কে সমস্যাটি জানায়, এবং loop-এর পরবর্তী iteration শুরু করতে এবং আরেকটি guess চাইতে `continue` call করে। `if` expression-টির পরে, আমরা জেনে নিয়ে `guess` এবং secret number-এর মধ্যে comparison চালিয়ে যেতে পারি যে `guess` ১ থেকে ১০০-এর মধ্যে আছে।

তবে, এটি আদর্শ সমাধান নয়: যদি এটি অত্যন্ত গুরুত্বপূর্ণ হতো যে program শুধু ১ থেকে ১০০-এর মধ্যে value নিয়ে কাজ করবে, এবং এর অনেক function-এ এই requirement থাকত, তবে প্রতিটি function-এ এমন একটি check থাকাটা ক্লান্তিকর হতো (এবং সম্ভবত performance-এ প্রভাব ফেলত)।

এর বদলে, আমরা একটি dedicated module-এ একটি নতুন type বানাতে পারি এবং validation গুলোকে সর্বত্র না মিলিয়ে সেই type-এর একটি instance তৈরি করার function-এ রাখতে পারি। এভাবে, function-গুলোর জন্য তাদের signature-এ নতুন type ব্যবহার করা নিরাপদ এবং তারা যে value গুলো পায় তা নিশ্চিন্তভাবে ব্যবহার করতে পারে। Listing 9-13 একটি `Guess` type define করার একটি উপায় দেখায় যা শুধুমাত্র তখনই `Guess`-এর একটি instance তৈরি করবে যখন `new` function ১ থেকে ১০০-এর মধ্যে একটি value পাবে।

<Listing number="9-13" caption="A `Guess` type that will only continue with values between 1 and 100" file-name="src/guessing_game.rs">

```rust
pub struct Guess {
    value: i32,
}

impl Guess {
    pub fn new(value: i32) -> Guess {
        if value < 1 || value > 100 {
            panic!("Guess value must be between 1 and 100, got {value}.");
        }

        Guess { value }
    }

    pub fn value(&self) -> i32 {
        self.value
    }
}
```

</Listing>

লক্ষ্য করো যে *src/guessing_game.rs*-এর এই code-টি *src/lib.rs*-এ একটি `mod guessing_game;` module declaration যোগ করার উপর নির্ভর করে, যা আমরা এখানে দেখাইনি। এই নতুন module-এর file-এর ভেতরে, আমরা `Guess` নামের একটি struct define করি যার `value` নামে একটি field আছে যা একটি `i32` ধারণ করে। এখানেই সংখ্যাটি সংরক্ষিত হবে।

তারপর, আমরা `Guess`-এর উপর একটি associated function `new` implement করি যা `Guess` value-এর instance তৈরি করে। `new` function-টিকে `value` নামে একটি parameter সহ define করা হয়েছে যার type `i32` এবং এটি একটি `Guess` return করে। `new` function-এর body-তের code `value` পরীক্ষা করে নিশ্চিত করে যে এটি ১ থেকে ১০০-এর মধ্যে। যদি `value` এই test-এ উত্তীর্ণ না হয়, আমরা একটি `panic!` call করি, যা calling code লেখা programmer-কে সতর্ক করবে যে তার একটি bug আছে যা তাকে ঠিক করতে হবে, কারণ এই সীমার বাইরের একটি `value` দিয়ে একটি `Guess` তৈরি করা `Guess::new` যে contract-এর উপর নির্ভর করছে তা ভঙ্গ করবে। কোন শর্তে `Guess::new` panic করতে পারে তা তার public-facing API documentation-এ আলোচনা করা উচিত; আমরা Chapter 14-তে তুমি যে API documentation তৈরি করবে তাতে `panic!`-এর সম্ভাবনা নির্দেশ করে এমন documentation convention নিয়ে আলোচনা করব। যদি `value` test-এ উত্তীর্ণ হয়, আমরা এর `value` field প্যারামিটার `value`-এ সেট করে একটি নতুন `Guess` তৈরি করি এবং সেই `Guess` return করি।

এরপর, আমরা `value` নামের একটি method implement করি যা `self`-কে borrow করে, অন্য কোনো parameter নেই, এবং একটি `i32` return করে। এই ধরনের method-কে মাঝে মাঝে _getter_ বলা হয় কারণ এর উদ্দেশ্য হলো তার field থেকে কিছু data নেওয়া এবং তা return করা। এই public method-টি প্রয়োজন কারণ `Guess` struct-এর `value` field private। `value` field-টি private থাকা গুরুত্বপূর্ণ যাতে `Guess` struct ব্যবহার করা code-কে `value` সরাসরি সেট করার অনুমতি না দেওয়া হয়: `guessing_game` module-এর বাইরের code-কে অবশ্যই একটি `Guess` instance তৈরি করতে `Guess::new` function ব্যবহার করতে হবে, যার ফলে নিশ্চিত হয় যে `Guess::new` function-এর শর্ত গুলো দ্বারা যাচাই না করা কোনো `value` সহ `Guess` থাকার কোনো উপায় নেই।

এমন একটি function যার parameter বা return শুধু ১ থেকে ১০০-এর মধ্যে সংখ্যা, সে তারপর তার signature-এ ঘোষণা করতে পারে যে সে একটি `i32`-এর বদলে একটি `Guess` নেয় বা return করে এবং তার body-তে কোনো অতিরিক্ত check করতে হবে না।

## Summary

Rust-এর error-handling feature গুলো তোমাকে আরও শক্তিশালী code লিখতে সাহায্য করার জন্য ডিজাইন করা। `panic!` macro সংকেত দেয় যে তোমার program এমন একটি অবস্থায় আছে যা সে handle করতে পারে না এবং তোমাকে invalid বা ভুল value নিয়ে এগোনোর চেষ্টার বদলে process-কে থামিয়ে দিতে দেয়। `Result` enum Rust-এর type system ব্যবহার করে নির্দেশ করে যে operation এমনভাবে ব্যর্থ হতে পারে যা থেকে তোমার code recover করতে পারে। তুমি `Result` ব্যবহার করে তোমার code-কে call করা code-কে বলতে পারো যে তাকে সম্ভাব্য success বা failure handle করতে হবে। উপযুক্ত পরিস্থিতিতে `panic!` এবং `Result` ব্যবহার করলে অনিবার্য সমস্যার মুখে তোমার code আরও নির্ভরযোগ্য হবে।

এখন তুমি দেখেছ কীভাবে standard library `Option` এবং `Result` enum-এর সাথে generics ব্যবহার করে, চলো আলোচনা করি generics কীভাবে কাজ করে এবং তুমি কীভাবে তোমার code-এ সেগুলো ব্যবহার করতে পারো।

[encoding]: ch18-03-oo-design-patterns.html#encoding-states-and-behavior-as-types

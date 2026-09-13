## Modularity এবং Error Handling উন্নত করতে Refactoring

আমাদের program উন্নত করতে আমরা চারটি সমস্যা ঠিক করব, যেগুলো program-টির structure এবং সম্ভাব্য error handle করার পদ্ধতির সাথে সম্পর্কিত। প্রথমত, আমাদের `main` function এখন দুটি কাজ করে: এটি argument parse করে এবং file পড়ে। আমাদের program যত বড় হবে, `main` function যতগুলো আলাদা কাজ handle করবে তত বাড়বে। একটি function যত বেশি responsibility পায়, সেটি তত বুঝতে কঠিন হয়, test করা কঠিন হয়, এবং এর কোনো অংশ না ভেঙে পরিবর্তন করা তত কঠিন হয়। সবচেয়ে ভালো হয় functionality আলাদা করে দেওয়া, যাতে প্রতিটি function শুধু একটি কাজের জন্য দায়ী থাকে।

এই সমস্যাটির সাথে জড়িত দ্বিতীয় সমস্যাটি: যদিও `query` এবং `file_path` আমাদের program-এর configuration variable, `contents`-এর মতো variable গুলো ব্যবহার করা হয় program-টির logic সম্পাদনের জন্য। `main` যত বড় হবে, আমাদের তত বেশি variable scope-এ আনতে হবে; scope-এ যত বেশি variable থাকবে, প্রতিটির উদ্দেশ্য মনে রাখা তত কঠিন হবে। Configuration variable গুলোকে একটি structure-এ একত্রিত করা সবচেয়ে ভালো, যাতে সেগুলোর উদ্দেশ্য পরিষ্কার হয়।

তৃতীয় সমস্যাটি হলো আমরা file পড়তে ব্যর্থ হলে error message print করতে `expect` ব্যবহার করেছি, কিন্তু error message-টি শুধু `Should have been able to read the file` print করে। File পড়া কয়েকভাবে ব্যর্থ হতে পারে: যেমন, file-টি নাও থাকতে পারে, বা আমাদের সেটি খোলার permission নাও থাকতে পারে। এই মুহূর্তে, পরিস্থিতি যাই হোক না কেন, আমরা সবকিছুর জন্য একই error message print করব, যা user-কে কোনো তথ্যই দেবে না!

চতুর্থত, আমরা error handle করতে `expect` ব্যবহার করি, এবং যদি user পর্যাপ্ত argument উল্লেখ না করেই আমাদের program চালায়, তবে তারা Rust থেকে একটি `index out of bounds` error পাবে যা সমস্যাটি পরিষ্কারভাবে ব্যাখ্যা করে না। সব error-handling code যদি এক জায়গায় থাকে তবে সবচেয়ে ভালো হয়, যাতে ভবিষ্যত maintainer-দের error-handling logic পরিবর্তন করতে হলে শুধু এক জায়গাতেই তাকা হয়। সব error-handling code এক জায়গায় রাখলে এটাও নিশ্চিত হবে যে আমরা এমন message print করছি যা আমাদের end user-দের কাছে অর্থপূর্ণ।

চলো আমাদের project refactor করে এই চারটি সমস্যার সমাধান করি।

<!-- Old headings. Do not remove or links may break. -->

<a id="separation-of-concerns-for-binary-projects"></a>

### Binary Project-এ Concern আলাদা করা

`main` function-কে একাধিক কাজের দায়িত্ব দেওয়ার সাংগঠনিক সমস্যাটি অনেক binary project-এর ক্ষেত্রেই সাধারণ। ফলস্বরূপ, অনেক Rust programmer-এর কাছেই এটি কাজে লাগে যে—`main` function বড় হতে শুরু করলে একটি binary program-এর আলাদা concern গুলোকে ভাগ করা। এই process-টির ধাপগুলো নিচে দেওয়া:

- তোমার program-টিকে একটি _main.rs_ file এবং একটি _lib.rs_ file-এ ভাগ করো এবং তোমার program-এর logic _lib.rs_-এ সরিয়ে নাও।
- যতক্ষণ তোমার command line parsing logic ছোট, সেটি `main` function-এই থাকতে পারে।
- যখন command line parsing logic জটিল হতে শুরু করে, সেটি `main` function থেকে বের করে অন্যান্য function বা type-এ নিয়ে যাও।

এই process-টির পরে `main` function-এ অবশিষ্ট responsibility গুলো শুধু নিচেরগুলোতে সীমাবদ্ধ থাকা উচিত:

- Argument value গুলো দিয়ে command line parsing logic call করা
- অন্য কোনো configuration setup করা
- _lib.rs_-এ একটি `run` function call করা
- `run` যদি error return করে সেটি handle করা

এই pattern-টি হলো concern আলাদা করার বিষয়ে: _main.rs_ program চালানো handle করে এবং _lib.rs_ হাতে-কলমে কাজটির সম্পূর্ণ logic handle করে। যেহেতু `main` function-কে সরাসরি test করা যায় না, এই structure তোমাকে তোমার program-এর সম্পূর্ণ logic `main` function থেকে সরিয়ে test করতে দেয়। `main` function-এ অবশিষ্ট code-টি পড়েই যাচাই করার মতো ছোট হবে। চলো এই process অনুসরণ করে আমাদের program-টি পুনরায় তৈরি করি।

#### Argument Parser আলাদা করা

আমরা argument parse করার functionality-টিকে এমন একটি function-এ আলাদা করব যাকে `main` call করবে। Listing 12-5-তে `main` function-টির নতুন শুরু দেখানো হয়েছে যেটি একটি নতুন function `parse_config`-কে call করে, যেটি আমরা _src/main.rs_-এ define করব।

<Listing number="12-5" file-name="src/main.rs" caption="`main` থেকে একটি `parse_config` function আলাদা করা">

```rust,ignore
fn main() {
    let args: Vec<String> = env::args().collect();

    let (query, file_path) = parse_config(&args);

    // --snip--
}

fn parse_config(args: &[String]) -> (&str, &str) {
    let query = &args[1];
    let file_path = &args[2];

    (query, file_path)
}
```

</Listing>

আমরা এখনো command line argument গুলোকে একটি vector-এ সংগ্রহ করছি, কিন্তু `main` function-এর ভেতর index 1-এর argument value-টিকে `query` variable-এ এবং index 2-এর argument value-টিকে `file_path` variable-এ assign করার বদলে আমরা পুরো vector-টিকে `parse_config` function-এ পাঠাই। তারপর `parse_config` function-টি সেই logic ধারণ করে যা নির্ধারণ করে কোন argument কোন variable-এ যাবে এবং value গুলো `main`-এ ফেরত পাঠায়। আমরা এখনো `main`-এ `query` ও `file_path` variable তৈরি করি, কিন্তু `main`-এর কাছে আর নির্ধারণের দায়িত্ব নেই যে command line argument গুলো এবং variable গুলো কীভাবে সম্পর্কিত।

আমাদের ছোট program-টির জন্য এই পরিবর্তনটি হয়তো অতিরিক্ত মনে হতে পারে, কিন্তু আমরা ছোট ছোট incremental ধাপে refactor করছি। এই পরিবর্তনটি করার পর program-টি আবার চালাও যাতে যাচাই হয় argument parsing এখনো কাজ করছে। প্রায়ই তোমার progress যাচাই করা ভালো, যাতে সমস্যা দেখা দিলে কারণ চিহ্নিত করা সহজ হয়।

#### Configuration Value গুলো একত্রিত করা

আমরা `parse_config` function-টিকে আরও উন্নত করতে আরেকটি ছোট ধাপ নিতে পারি। এই মুহূর্তে আমরা একটি tuple return করছি, কিন্তু তারপর সেই tuple-টিকে আবার সাথে সাথে আলাদা অংশে ভাঙছি। এটি একটি ইঙ্গিত যে হয়তো আমাদের কাছে এখনো সঠিক abstraction নেই।

উন্নতির সুযোগ আছে তার আরেকটি ইঙ্গিত হলো `parse_config`-এর `config` অংশটি, যা ইঙ্গিত করে যে আমরা যে দুটি value return করছি সেগুলো সম্পর্কিত এবং দুটিই একটি configuration value-এর অংশ। আমরা বর্তমানে এই অর্থটি data-এর structure-এ প্রকাশ করছি না, শুধু দুটি value-কে একটি tuple-এ একত্রিত করার মাধ্যমে দিচ্ছি; এর বদলে আমরা দুটি value-কে একটি struct-এ রাখব এবং struct-এর প্রতিটি field-কে একটি অর্থপূর্ণ নাম দেব। এতে এই code-এর ভবিষ্যৎ maintainer-দের জন্য বিভিন্ন value কীভাবে একে অপরের সাথে সম্পর্কিত এবং তাদের উদ্দেশ্য কী—তা বোঝা সহজ হবে।

Listing 12-6-তে `parse_config` function-এর উন্নতি দেখানো হয়েছে।

<Listing number="12-6" file-name="src/main.rs" caption="`parse_config`-কে একটি `Config` struct-এর instance return করতে refactor করা">

```rust,should_panic,noplayground
fn main() {
    let args: Vec<String> = env::args().collect();

    let config = parse_config(&args);

    println!("Searching for {}", config.query);
    println!("In file {}", config.file_path);

    let contents = fs::read_to_string(config.file_path)
        .expect("Should have been able to read the file");

    // --snip--
}

struct Config {
    query: String,
    file_path: String,
}

fn parse_config(args: &[String]) -> Config {
    let query = args[1].clone();
    let file_path = args[2].clone();

    Config { query, file_path }
}
```

</Listing>

আমরা `Config` নামের একটি struct যোগ করেছি যার `query` এবং `file_path` নামে field আছে। `parse_config`-এর signature এখন নির্দেশ করে যে এটি একটি `Config` value return করে। `parse_config`-এর body-তে, যেখানে আগে আমরা `args`-এ `String` value-কে reference করে string slice return করতাম, সেখানে এখন আমরা `Config`-কে define করেছি owned `String` value ধারণ করার জন্য। `main`-এর `args` variable-টি argument value-গুলোর owner এবং সে শুধু `parse_config` function-কে সেগুলো borrow করতে দিচ্ছে, যার মানে `Config` যদি `args`-এর value-গুলোর ownership নিতে চাইত তবে আমরা Rust-এর borrowing rule লঙ্ঘন করতাম।

`String` data manage করার বেশ কয়েকটি উপায় আছে; সবচেয়ে সহজ, যদিও কিছুটা inefficient, পথ হলো value গুলোর উপর `clone` method call করা। এতে `Config` instance-টি own করার জন্য data-এর একটি সম্পূর্ণ copy তৈরি হবে, যেটি string data-এর reference সংরক্ষণ করার চেয়ে বেশি সময় ও মেমরি নেয়। তবে, data clone করা আমাদের code-কে অনেক সোজা করে দেয় কারণ আমাদের reference-গুলোর lifetime manage করতে হয় না; এই পরিস্থিতিতে সামান্য performance ছেড়ে সরলতা অর্জন করা একটি গ্রহণযোগ্য trade-off।

> ### `clone` ব্যবহারের Trade-Off
>
> অনেক Rustacean-এর মধ্যে ownership সমস্যা সমাধানে `clone` ব্যবহার এড়িয়ে চলার প্রবণতা আছে, কারণ এর runtime cost আছে। [Chapter 13][ch13]<!-- ignore -->-এ তুমি শিখবে এই ধরনের পরিস্থিতিতে কীভাবে আরও efficient পদ্ধতি ব্যবহার করতে হয়। কিন্তু আপাতত, কয়েকটি string copy করে এগিয়ে যাওয়া ক্ষতিকর নয়, কারণ তুমি এই copy গুলো শুধু একবারই করবে এবং তোমার file path ও query string খুবই ছোট। প্রথম চেষ্টাতেই কিছুটা inefficient হলেও একটি কাজ করা program থাকাটা ভালো, কোনো code hyperoptimize করার চেষ্টা করার চেয়ে। Rust-এ তুমি যত বেশি অভিজ্ঞ হবে, সবচেয়ে efficient solution দিয়ে শুরু করা তত সহজ হবে, কিন্তু আপাতত `clone` call করা সম্পূর্ণ গ্রহণযোগ্য।

আমরা `main`-কে update করেছি যাতে এটি `parse_config` থেকে return হওয়া `Config` instance-টিকে `config` নামের একটি variable-এ রাখে, এবং আমরা যে code আগে আলাদা `query` ও `file_path` variable ব্যবহার করত সেটি update করেছি যাতে এখন সেটি `Config` struct-এর field ব্যবহার করে।

এখন আমাদের code আরও পরিষ্কারভাবে প্রকাশ করে যে `query` ও `file_path` সম্পর্কিত এবং তাদের উদ্দেশ্য হলো program যেভাবে কাজ করবে তা configure করা। এই value গুলো ব্যবহার করে এমন যেকোনো code জানে সেগুলো `config` instance-এ তাদের উদ্দেশ্য অনুসারে নামকরণ করা field-গুলোতে খুঁজে পাবে।

#### `Config`-এর জন্য একটি Constructor তৈরি

এ পর্যন্ত আমরা command line argument parse করার logic-টিকে `main` থেকে আলাদা করে `parse_config` function-এ রেখেছি। এতে আমাদের সাহায্য হলো—আমরা দেখতে পেলাম যে `query` ও `file_path` value দুটি সম্পর্কিত, এবং সেই সম্পর্কটি আমাদের code-এ প্রকাশ পাওয়া উচিত। তারপর আমরা একটি `Config` struct যোগ করি `query` ও `file_path`-এর সম্পর্কিত উদ্দেশ্য নাম দেওয়ার জন্য এবং `parse_config` function থেকে value গুলোর নাম struct field নাম হিসেবে return করার জন্য।

সুতরাং, যেহেতু `parse_config` function-টির এখন উদ্দেশ্য হলো একটি `Config` instance তৈরি করা, আমরা `parse_config`-কে একটি সাধারণ function থেকে এমন একটি function-এ পরিবর্তন করতে পারি যার নাম `new` এবং যেটি `Config` struct-এর সাথে associated। এই পরিবর্তনটি করলে code আরও idiomatic হবে। আমরা standard library-এর যেমন `String`-এর মতো type-এর instance `String::new` call করে তৈরি করতে পারি। একইভাবে, `parse_config`-কে `Config`-এর সাথে associated একটি `new` function-এ পরিবর্তন করলে, আমরা `Config::new` call করে `Config`-এর instance তৈরি করতে পারব। Listing 12-7 আমাদের যে পরিবর্তনগুলো করতে হবে তা দেখায়।

<Listing number="12-7" file-name="src/main.rs" caption="`parse_config`-কে `Config::new`-এ পরিবর্তন">

```rust,should_panic,noplayground
fn main() {
    let args: Vec<String> = env::args().collect();

    let config = Config::new(&args);

    // --snip--
}

// --snip--

impl Config {
    fn new(args: &[String]) -> Config {
        let query = args[1].clone();
        let file_path = args[2].clone();

        Config { query, file_path }
    }
}
```

</Listing>

আমরা `main`-কে update করেছি যেখানে আমরা `parse_config` call করতাম সেখানে এখন `Config::new` call করতে। আমরা `parse_config`-এর নাম পরিবর্তন করে `new` করেছি এবং একে একটি `impl` block-এর ভেতরে সরিয়েছি, যা `new` function-টিকে `Config`-এর সাথে associate করে। এই code আবার compile করে দেখো যাতে নিশ্চিত হয় সব ঠিকঠাক চলছে।

### Error Handling ঠিক করা

এখন আমরা আমাদের error handling ঠিক করার কাজে নামব। মনে করো, `args` vector-এর index 1 বা index 2-এর value-তে access করার চেষ্টা করলে, যদি vector-এ তিনটির কম item থাকে, তবে program-টি panic করবে। কোনো argument ছাড়াই program চালানোর চেষ্টা করো; এটি এমন দেখাবে:

```console
$ cargo run
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.0s
     Running `target/debug/minigrep`

thread 'main' (6023615) panicked at src/main.rs:27:21:
index out of bounds: the len is 1 but the index is 1
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

`index out of bounds: the len is 1 but the index is 1` লাইনটি হলো programmer-দের জন্য একটি error message। এটি আমাদের end user-দের বুঝতে সাহায্য করবে না যে তাদের কী করা উচিত। চলো সেটি এখন ঠিক করি।

#### Error Message উন্নত করা

Listing 12-8-তে, আমরা `new` function-এ একটি check যোগ করি যা index 1 ও index 2-এ access করার আগে verify করবে যে slice-টি যথেষ্ট দীর্ঘ। যদি slice-টি যথেষ্ট দীর্ঘ না হয়, program panic করবে এবং একটি ভালো error message দেখাবে।

<Listing number="12-8" file-name="src/main.rs" caption="Argument সংখ্যার জন্য একটি check যোগ করা">

```rust,ignore
    // --snip--
    fn new(args: &[String]) -> Config {
        if args.len() < 3 {
            panic!("not enough arguments");
        }
        // --snip--
```

</Listing>

এই code-টি [Listing 9-13-এ লেখা `Guess::new` function-এর][ch9-custom-types]<!-- ignore --> মতো, যেখানে আমরা `value` argument বৈধ value-এর range-এর বাইরে গেলে `panic!` call করেছিলাম। এখানে value-এর একটি range check করার বদলে আমরা check করছি যে `args`-এর length অন্তত `3` কিনা, এবং এই condition পূরণ হয়েছে এই assumption-এর অধীনে function-টির বাকি অংশ কাজ করবে। যদি `args`-এ তিনটির কম item থাকে, এই condition-টি `true` হবে, এবং আমরা `panic!` macro call করে program-টি সাথে সাথে শেষ করব।

`new`-তে এই কয়েক লাইন extra code যোগ করার পর, চলো আবার কোনো argument ছাড়াই program চালাই দেখি এখন error-টি দেখতে কেমন:

```console
$ cargo run
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.0s
     Running `target/debug/minigrep`

thread 'main' (6023776) panicked at src/main.rs:26:13:
not enough arguments
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

এই output-টি ভালো: এখন আমাদের একটি যুক্তিসঙ্গত error message আছে। তবে, এতে এমন কিছু অতিরিক্ত তথ্যও আছে যা আমরা আমাদের user-দের দিতে চাই না। হয়তো Listing 9-13-এ আমরা যে technique ব্যবহার করেছিলাম সেটি এখানে ব্যবহারের জন্য সবচেয়ে ভালো নয়: `panic!`-এর একটি call programming সমস্যার চেয়ে usage সমস্যার জন্য বেশি উপযুক্ত, [যেমন Chapter 9-এ আলোচনা করা হয়েছে][ch9-error-guidelines]<!-- ignore -->। এর বদলে, আমরা Chapter 9-এ তোমার শেখা অন্য technique ব্যবহার করব—[একটি `Result` return করা][ch9-result]<!-- ignore --> যা হয় success অথবা error নির্দেশ করে।

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-a-result-from-new-instead-of-calling-panic"></a>

#### `panic!` Call করার বদলে একটি `Result` Return করা

এর বদলে আমরা এমন একটি `Result` value return করতে পারি যা success-এর ক্ষেত্রে একটি `Config` instance ধারণ করবে এবং error-এর ক্ষেত্রে সমস্যাটি বর্ণনা করবে। আমরা function-টির নামও `new` থেকে পরিবর্তন করে `build` করব, কারণ অনেক programmer আশা করেন যে `new` function কখনো fail করবে না। যখন `Config::build` `main`-এর সাথে যোগাযোগ করবে, আমরা `Result` type ব্যবহার করে signal দিতে পারব যে একটি সমস্যা হয়েছে। তারপর, আমরা `main`-কে পরিবর্তন করে একটি `Err` variant-কে আমাদের user-দের জন্য অধিক ব্যবহারিক error-এ রূপান্তর করতে পারব, `panic!` call-এর ফলে আসা `thread 'main'` এবং `RUST_BACKTRACE` সংক্রান্ত অতিরিক্ত text ছাড়া।

Listing 12-9 দেখায় আমাদের এখন `Config::build` নামে যে function-টিকে call করছি তার return value-তে এবং একটি `Result` return করার জন্য function-টির body-তে যে পরিবর্তন করতে হবে। মনে রাখো, এটি ততক্ষণ পর্যন্ত compile হবে না যতক্ষণ না আমরা `main`-কেও update করি, যা আমরা পরের listing-এ করব।

<Listing number="12-9" file-name="src/main.rs" caption="`Config::build` থেকে একটি `Result` return করা">

```rust,ignore,does_not_compile
impl Config {
    fn build(args: &[String]) -> Result<Config, &'static str> {
        if args.len() < 3 {
            return Err("not enough arguments");
        }

        let query = args[1].clone();
        let file_path = args[2].clone();

        Ok(Config { query, file_path })
    }
}
```

</Listing>

আমাদের `build` function একটি `Result` return করে যাতে success-এর ক্ষেত্রে একটি `Config` instance এবং error-এর ক্ষেত্রে একটি string literal থাকে। আমাদের error value গুলো সবসময় এমন string literal হবে যাদের `'static` lifetime আছে।

আমরা function-টির body-তে দুটি পরিবর্তন করেছি: user পর্যাপ্ত argument না পাঠালে `panic!` call করার বদলে আমরা এখন একটি `Err` value return করি, এবং `Config` return value-টিকে আমরা একটি `Ok`-এ wrap করেছি। এই পরিবর্তনগুলো function-টিকে তার নতুন type signature মেনে চলতে দেয়।

`Config::build` থেকে একটি `Err` value return করার সুবিধা হলো `main` function-টি `build` function থেকে return হওয়া `Result` value handle করতে পারে এবং error-এর ক্ষেত্রে process-টিকে আরও পরিষ্কারভাবে শেষ করতে পারে।

<!-- Old headings. Do not remove or links may break. -->

<a id="calling-confignew-and-handling-errors"></a>

#### `Config::build` Call করা এবং Error Handle করা

Error case-টি handle করতে এবং একটি user-friendly message print করতে, আমাদের `main`-কে update করতে হবে যাতে এটি `Config::build` থেকে return হওয়া `Result` handle করে, যেমন Listing 12-10-তে দেখানো হয়েছে। আমরা `panic!` থেকে nonzero error code দিয়ে command line tool শেষ করার দায়িত্বটিও সরিয়ে নিজে নিজে implement করব। Nonzero exit status হলো একটি convention, যা আমাদের program-টিকে call করা process-কে signal দেয় যে program-টি error state-এ exit করেছে।

<Listing number="12-10" file-name="src/main.rs" caption="`Config` build করা ব্যর্থ হলে একটি error code দিয়ে শেষ করা">

```rust,ignore
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();

    let config = Config::build(&args).unwrap_or_else(|err| {
        println!("Problem parsing arguments: {err}");
        process::exit(1);
    });

    // --snip--
```

</Listing>

এই listing-টিতে আমরা এমন একটি method ব্যবহার করেছি যা আমরা এখনো বিস্তারিত আলোচনা করিনি: `unwrap_or_else`, যা standard library দ্বারা `Result<T, E>`-তে define করা। `unwrap_or_else` ব্যবহার করলে আমরা কিছু custom, non-`panic!` error handling define করতে পারি। যদি `Result`-টি একটি `Ok` value হয়, এই method-টির আচরণ `unwrap`-এর মতোই: এটি `Ok` যে value-টি wrap করে রাখে সেটি return করে। তবে, যদি value-টি একটি `Err` value হয়, এই method-টি closure-এর code-টিকে call করে, যেটি এমন একটি anonymous function যা আমরা define করি এবং `unwrap_or_else`-এ argument হিসেবে pass করি। Closure সম্পর্কে আমরা [Chapter 13][ch13]<!-- ignore -->-এ আরও বিস্তারিত আলোচনা করব। আপাতত, তোমার শুধু এটুকু জানা দরকার যে `unwrap_or_else` `Err`-এর inner value-টিকে—যা এই ক্ষেত্রে Listing 12-9-এ আমরা যোগ করা static string `"not enough arguments"`—আমাদের closure-এ vertical pipe-গুলোর মাঝে থাকা `err` argument-এ pass করবে। তারপর closure-এর code-টি চালানোর সময় `err` value ব্যবহার করতে পারে।

আমরা একটি নতুন `use` line যোগ করেছি standard library থেকে `process`-কে scope-এ আনার জন্য। Error case-এ যে closure-টি চলবে তার code-টি শুধু দুই line: আমরা `err` value print করি এবং তারপর `process::exit` call করি। `process::exit` function-টি program-টিকে সাথে সাথে থামিয়ে দেবে এবং exit status code হিসেবে যে number-টি pass করা হয়েছিল তা return করবে। এটি Listing 12-8-এ আমরা যে `panic!`-ভিত্তিক handling ব্যবহার করেছিলাম তার মতোই, কিন্তু আর সেই অতিরিক্ত output পাব না। চলো এটি চেষ্টা করি:

```console
$ cargo run
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.48s
     Running `target/debug/minigrep`
Problem parsing arguments: not enough arguments
```

দারুণ! এই output-টি আমাদের user-দের জন্য অনেক বেশি friendly।

<!-- Old headings. Do not remove or links may break. -->

<a id="extracting-logic-from-the-main-function"></a>

### `main` থেকে Logic আলাদা করা

এখন যেহেতু আমরা configuration parsing refactor করা শেষ করেছি, চলো এবার program-টির logic-এ ফিরে যাই। যেমন আমরা [“Binary Project-এ Concern আলাদা করা”](#separation-of-concerns-for-binary-projects)<!-- ignore -->-এ বলেছি, আমরা একটি `run` নামের function আলাদা করব যা `main` function-এ বর্তমানে থাকা সমস্ত logic—যা configuration setup বা error handle করার সাথে জড়িত নয়—ধারণ করবে। আমরা শেষ করলে, `main` function-টি সংক্ষিপ্ত হবে এবং পরিদর্শন দ্বারা যাচাই করা সহজ হবে, এবং আমরা বাকি সমস্ত logic-এর জন্য test লিখতে পারব।

Listing 12-11 একটি `run` function আলাদা করার ছোট, incremental উন্নতি দেখায়।

<Listing number="12-11" file-name="src/main.rs" caption="Program-টির বাকি logic ধারণ করে এমন একটি `run` function আলাদা করা">

```rust,ignore
fn main() {
    // --snip--

    println!("Searching for {}", config.query);
    println!("In file {}", config.file_path);

    run(config);
}

fn run(config: Config) {
    let contents = fs::read_to_string(config.file_path)
        .expect("Should have been able to read the file");

    println!("With text:\n{contents}");
}

// --snip--
```

</Listing>

`run` function-টি এখন `main`-এর সমস্ত অবশিষ্ট logic ধারণ করে, file পড়া থেকে শুরু করে। `run` function-টি `Config` instance-টিকে argument হিসেবে নেয়।

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-errors-from-the-run-function"></a>

#### `run` থেকে Error Return করা

বাকি program logic `run` function-এ আলাদা হওয়ার পর, আমরা Listing 12-9-এ `Config::build`-এর ক্ষেত্রে যেমন করেছি তেমনি error handling উন্নত করতে পারি। `expect` call করে program-টিকে panic করতে দেওয়ার বদলে, `run` function-টি কিছু গণ্ডগোল হলে একটি `Result<T, E>` return করবে। এতে আমরা error handle করার logic কে `main`-এ একটি user-friendly উপায়ে আরও একত্রিত করতে পারব। Listing 12-12 `run`-এর signature এবং body-তে আমাদের যে পরিবর্তনগুলো করতে হবে তা দেখায়।

<Listing number="12-12" file-name="src/main.rs" caption="`run` function-টিকে `Result` return করতে পরিবর্তন">

```rust,ignore
use std::error::Error;

// --snip--

fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let contents = fs::read_to_string(config.file_path)?;

    println!("With text:\n{contents}");

    Ok(())
}
```

</Listing>

আমরা এখানে তিনটি গুরুত্বপূর্ণ পরিবর্তন করেছি। প্রথমত, আমরা `run` function-টির return type `Result<(), Box<dyn Error>>`-এ পরিবর্তন করেছি। এই function-টি আগে unit type, `()`, return করত, এবং আমরা সেটিকেই `Ok` case-এ return হওয়া value হিসেবে রাখব।

Error type-টির জন্য, আমরা trait object `Box<dyn Error>` ব্যবহার করেছি (এবং উপরে একটি `use` statement দিয়ে `std::error::Error`-কে scope-এ এনেছি)। Trait object সম্পর্কে আমরা [Chapter 18][ch18]<!-- ignore -->-এ আলোচনা করব। আপাতত শুধু এটুকু জেনো যে `Box<dyn Error>` মানে function-টি এমন একটি type return করবে যা `Error` trait implement করে, কিন্তু আমাদের return value-টি ঠিক কোন particular type হবে তা specify করতে হবে না। এতে আমরা বিভিন্ন error case-এ বিভিন্ন type-এর error value return করার flexibility পাই। `dyn` keyword-টি _dynamic_-এর সংক্ষিপ্ত রূপ।

দ্বিতীয়ত, আমরা `expect`-এর call সরিয়ে `?` operator-এর ব্যবহার করেছি, যেমনটা [Chapter 9][ch9-question-mark]<!-- ignore -->-এ আলোচনা করেছি। `panic!`-এর বদলে, `?` বর্তমান function থেকে error value-টিকে caller-এর handle করার জন্য return করবে।

তৃতীয়ত, `run` function-টি এখন success-এর ক্ষেত্রে একটি `Ok` value return করে। আমরা signature-এ `run` function-টির success type `()` হিসেবে declare করেছি, যার মানে আমাদের unit type value-টিকে `Ok` value-তে wrap করতে হবে। এই `Ok(())` syntax প্রথমে কিছুটা অদ্ভুত মনে হতে পারে। কিন্তু এভাবে `()` ব্যবহার করাটাই idiomatic উপায় যখন নির্দেশ করতে চাই যে আমরা `run`-কে শুধু তার side effect-এর জন্য call করছি; এটি আমাদের কোনো value return করে না যা আমাদের দরকার।

তুমি যখন এই code চালাবে, এটি compile হবে কিন্তু একটি warning দেখাবে:

```console
$ cargo run -- the poem.txt
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
warning: unused `Result` that must be used
  --> src/main.rs:19:5
   |
19 |     run(config);
   |     ^^^^^^^^^^^
   |
   = note: this `Result` may be an `Err` variant, which should be handled
   = note: `#[warn(unused_must_use)]` (part of `#[warn(unused)]`) on by default
help: use `let _ = ...` to ignore the resulting value
   |
19 |     let _ = run(config);
   |     +++++++

warning: `minigrep` (bin "minigrep") generated 1 warning
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.71s
     Running `target/debug/minigrep the poem.txt`
Searching for the
In file poem.txt
With text:
I'm nobody! Who are you?
Are you nobody, too?
Then there's a pair of us - don't tell!
They'd banish us, you know.

How dreary to be somebody!
How public, like a frog
To tell your name the livelong day
To an admiring bog!
```

Rust আমাদের বলছে যে আমাদের code `Result` value-টিকে উপেক্ষা করেছে এবং সেই `Result` value-টি হয়তো নির্দেশ করছে যে একটি error ঘটেছে। কিন্তু আমরা check করছি না যে কোনো error হয়েছে কিনা, এবং compiler আমাদের মনে করিয়ে দিচ্ছে যে হয়তো আমরা এখানে কিছু error-handling code রাখতে চেয়েছিলাম! চলো এখন সেই সমস্যাটি সমাধান করি।

#### `main`-এ `run` থেকে Return হওয়া Error Handle করা

আমরা error check করব এবং সেগুলো handle করব Listing 12-10-এ `Config::build`-এর সাথে যে আমরা যে technique ব্যবহার করেছি তার অনুরূপ একটি technique ব্যবহার করে, কিন্তু সামান্য একটি পার্থক্য সহ:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore
fn main() {
    // --snip--

    println!("Searching for {}", config.query);
    println!("In file {}", config.file_path);

    if let Err(e) = run(config) {
        println!("Application error: {e}");
        process::exit(1);
    }
}
```

আমরা `run` কোনো `Err` value return করেছে কিনা তা check করতে এবং যদি করে থাকে তবে `process::exit(1)` call করতে `unwrap_or_else`-এর বদলে `if let` ব্যবহার করি। `run` function-টি এমন কোনো value return করে না যা আমরা `Config::build` `Config` instance return করার যেভাবে সেভাবে `unwrap` করতে চাই। যেহেতু `run` success-এর ক্ষেত্রে `()` return করে, আমরা শুধু error detect করতে চাই, তাই আমাদের `unwrap_or_else`-এর unwrap করা value return করার দরকার নেই, যা শুধু `()`-ই হতো।

`if let` এবং `unwrap_or_else` function-গুলোর body দুই ক্ষেত্রেই একই: আমরা error print করি এবং exit করি।

### Code একটি Library Crate-এ ভাগ করা

আমাদের `minigrep` project এ পর্যন্ত বেশ ভালো দেখাচ্ছে! এখন আমরা _src/main.rs_ file-টি ভাগ করে কিছু code _src/lib.rs_ file-এ রাখব। এতে আমরা code test করতে পারব এবং এমন একটি _src/main.rs_ file পাব যার responsibility কম।

চলো text search করার দায়িত্বপূর্ণ code _src/main.rs_-এর বদলে _src/lib.rs_-এ define করি, যাতে আমরা (বা আমাদের `minigrep` library ব্যবহার করে এমন অন্য কেউ) আমাদের `minigrep` binary-এর চেয়ে বেশি context থেকে search function-টিকে call করতে পারি।

প্রথমে, চলো Listing 12-13-এ দেখানোর মতো `search` function-টির signature _src/lib.rs_-এ define করি, যার body `unimplemented!` macro-কে call করে। আমরা implementation পূরণ করার সময় signature-টি আরও বিস্তারিত ব্যাখ্যা করব।

<Listing number="12-13" file-name="src/lib.rs" caption="*src/lib.rs*-এ `search` function define করা">

```rust,ignore,does_not_compile
pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    unimplemented!();
}
```

</Listing>

আমরা function definition-এ `pub` keyword ব্যবহার করে `search`-কে আমাদের library crate-এর public API-এর অংশ হিসেবে চিহ্নিত করেছি। এখন আমাদের এমন একটি library crate আছে যা আমরা আমাদের binary crate থেকে ব্যবহার করতে পারি এবং যা আমরা test করতে পারি!

এখন আমাদের _src/lib.rs_-এ define করা code-টিকে _src/main.rs_-এর binary crate-এর scope-এ আনতে হবে এবং সেটি call করতে হবে, যেমন Listing 12-14-তে দেখানো হয়েছে।

<Listing number="12-14" file-name="src/main.rs" caption="*src/main.rs*-এ `minigrep` library crate-এর `search` function ব্যবহার">

```rust,ignore
// --snip--
use minigrep::search;

fn main() {
    // --snip--
}

// --snip--

fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let contents = fs::read_to_string(config.file_path)?;

    for line in search(&config.query, &contents) {
        println!("{line}");
    }

    Ok(())
}
```

</Listing>

আমরা একটি `use minigrep::search` line যোগ করে library crate থেকে `search` function-টিকে binary crate-এর scope-এ আনি। তারপর, `run` function-এ, file-এর content print করার বদলে আমরা `search` function-টিকে call করি এবং `config.query` value ও `contents`-কে argument হিসেবে pass করি। তারপর, `run` একটি `for` loop ব্যবহার করে `search` থেকে return হওয়া প্রতিটি line যেগুলো query-এর সাথে match করেছে সেগুলো print করবে। এটিও একটি ভালো সময় `main` function-এ থাকা `println!` call গুলো সরিয়ে ফেলার, যেগুলো query এবং file path দেখাচ্ছিল, যাতে আমাদের program শুধু search result গুলোই print করে (যদি কোনো error না ঘটে)।

খেয়াল করো যে search function-টি সমস্ত result গুলোকে একটি vector-এ সংগ্রহ করবে যেটি সে return করবে যেকোনো print হওয়ার আগে। এই implementation বড় file search করার সময় result দেখাতে ধীর হতে পারে, কারণ result গুলো পাওয়ার সাথে সাথে print হয় না; Chapter 13-এ আমরা iterator ব্যবহার করে এটি ঠিক করার একটি সম্ভাব্য উপায় নিয়ে আলোচনা করব।

বাহ! এটা অনেক কাজ ছিল, কিন্তু আমরা ভবিষ্যতের success-এর জন্য নিজেদের প্রস্তুত করেছি। এখন error handle করা অনেক সহজ, এবং আমরা code-কে আরও modular করেছি। এখান থেকে আমাদের প্রায় সমস্ত কাজ _src/lib.rs_-এ হবে।

চলো এই নতুন modularity-র সুযোগ নিই এমন কিছু করে যা পুরোনো code দিয়ে করা কঠিন ছিল কিন্তু নতুন code দিয়ে সহজ: আমরা কিছু test লিখব!

[ch13]: ch13-00-functional-features.html
[ch9-custom-types]: ch09-03-to-panic-or-not-to-panic.html#creating-custom-types-for-validation
[ch9-error-guidelines]: ch09-03-to-panic-or-not-to-panic.html#guidelines-for-error-handling
[ch9-result]: ch09-02-recoverable-errors-with-result.html
[ch18]: ch18-00-oop.html
[ch9-question-mark]: ch09-02-recoverable-errors-with-result.html#a-shortcut-for-propagating-errors-the--operator

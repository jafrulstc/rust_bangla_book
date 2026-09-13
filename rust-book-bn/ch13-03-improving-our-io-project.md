## Improving Our I/O Project

Iterator সম্পর্কে এই নতুন জ্ঞান নিয়ে আমরা Chapter 12-এর I/O project-এ iterator ব্যবহার করে code-এর কিছু জায়গাকে আরও স্পষ্ট ও concise করতে পারি। চলো দেখি কীভাবে iterator আমাদের `Config::build` function এবং `search` function-এর implementation উন্নত করতে পারে।

### Removing a `clone` Using an Iterator

Listing 12-6-তে আমরা এমন code যোগ করেছিলাম যা `String` value-গুলোর একটি slice নিত এবং slice-এ index করে value গুলোকে clone করে `Config` struct-এর একটি instance তৈরি করত, যাতে `Config` struct সেই value-গুলোর ownership রাখতে পারে। Listing 13-17-তে আমরা Listing 12-23-এর `Config::build` function-এর implementation টি আবার দেখাচ্ছি।

<Listing number="13-17" file-name="src/main.rs" caption="Reproduction of the `Config::build` function from Listing 12-23">

```rust,ignore
impl Config {
    fn build(args: &[String]) -> Result<Config, &'static str> {
        if args.len() < 3 {
            return Err("not enough arguments");
        }

        let query = args[1].clone();
        let file_path = args[2].clone();

        let ignore_case = env::var("IGNORE_CASE").is_ok();

        Ok(Config {
            query,
            file_path,
            ignore_case,
        })
    }
}
```

</Listing>

তখন আমরা বলেছিলাম inefficient `clone` call গুলো নিয়ে চিন্তা করতে না, কারণ ভবিষ্যতে আমরা সেগুলো সরিয়ে ফেলব। সেই সময় এখন এসেছে!

এখানে `clone` প্রয়োজন ছিল কারণ `args` parameter-এ `String` element-গুলোর একটি slice আছে, কিন্তু `build` function `args`-এর ownership নেয় না। একটি `Config` instance-এর ownership return করতে হলে আমাদের `Config`-এর `query` ও `file_path` field থেকে value গুলো clone করতে হতো যাতে `Config` instance তার নিজের value-গুলোর ownership রাখতে পারে।

Iterator সম্পর্কে নতুন জ্ঞান নিয়ে আমরা `build` function-কে এমনভাবে পরিবর্তন করতে পারি যাতে এটি একটি slice borrow করার বদলে একটি iterator-এর ownership নিজের argument হিসেবে নেয়। আমরা slice-এর length check করে নির্দিষ্ট জায়গায় index করার code-টির বদলে iterator functionality ব্যবহার করব। এতে `Config::build` function যা করছে সেটি আরও স্পষ্ট হবে, কারণ value-গুলো access করবে iterator।

একবার `Config::build` iterator-এর ownership নিলে এবং borrow করে index করা operation বন্ধ করলে, আমরা `clone` call করে নতুন allocation করার বদলে `String` value গুলোকে iterator থেকে `Config`-এ move করতে পারব।

#### Using the Returned Iterator Directly

তোমার I/O project-এর _src/main.rs_ file টি খোলো, যা দেখতে এরকম হওয়ার কথা:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore
fn main() {
    let args: Vec<String> = env::args().collect();

    let config = Config::build(&args).unwrap_or_else(|err| {
        eprintln!("Problem parsing arguments: {err}");
        process::exit(1);
    });

    // --snip--
}
```

আমরা প্রথমে Listing 12-24-এ যে `main` function এর শুরুটা ছিল সেটিকে Listing 13-18-এর code-এ পরিবর্তন করব, যা এবার একটি iterator ব্যবহার করে। আমরা `Config::build`-ও update না করা পর্যন্ত এটি compile হবে না।

<Listing number="13-18" file-name="src/main.rs" caption="Passing the return value of `env::args` to `Config::build`">

```rust,ignore,does_not_compile
fn main() {
    let config = Config::build(env::args()).unwrap_or_else(|err| {
        eprintln!("Problem parsing arguments: {err}");
        process::exit(1);
    });

    // --snip--
}
```

</Listing>

`env::args` function একটি iterator return করে! Iterator-এর value গুলোকে একটি vector-এ collect করে তারপর একটি slice `Config::build`-এ pass করার বদলে, এখন আমরা `env::args` থেকে return হওয়া iterator-এর ownership সরাসরি `Config::build`-এ pass করছি।

এরপর আমাদের `Config::build`-এর definition update করতে হবে। চলো `Config::build`-এর signature টিকে Listing 13-19-এর মতো করি। এটি এখনও compile হবে না, কারণ function body-ও update করতে হবে।

<Listing number="13-19" file-name="src/main.rs" caption="Updating the signature of `Config::build` to expect an iterator">

```rust,ignore,does_not_compile
impl Config {
    fn build(
        mut args: impl Iterator<Item = String>,
    ) -> Result<Config, &'static str> {
        // --snip--
```

</Listing>

`env::args` function-এর standard library documentation দেখায় যে এটি যে iterator return করে তার type হলো `std::env::Args`, এবং সেই type `Iterator` trait implement করে এবং `String` value return করে।

আমরা `Config::build` function-এর signature update করেছি যাতে `args` parameter-এর জন্য একটি generic type থাকে যার trait bound হলো `impl Iterator<Item = String>`, `&[String]` নয়। Chapter 10-এর [“Using Traits as Parameters”][impl-trait]<!-- ignore --> section-এ আলোচিত `impl Trait` syntax-এর এই ব্যবহারের অর্থ হলো `args` যেকোনো type হতে পারে যা `Iterator` trait implement করে এবং `String` item return করে।

যেহেতু আমরা `args`-এর ownership নিচ্ছি এবং এর উপর iterate করে এটিকে mutate করব, তাই `args` parameter-এর specification-এ `mut` keyword যোগ করে এটিকে mutable করতে পারি।

<!-- Old headings. Do not remove or links may break. -->

<a id="using-iterator-trait-methods-instead-of-indexing"></a>

#### Using `Iterator` Trait Methods

এরপর আমরা `Config::build`-এর body ঠিক করব। যেহেতু `args` `Iterator` trait implement করে, তাই আমরা জানি এর উপর `next` method call করতে পারি! Listing 13-20 Listing 12-23-এর code টিকে `next` method ব্যবহার করতে update করে।

<Listing number="13-20" file-name="src/main.rs" caption="Changing the body of `Config::build` to use iterator methods">

```rust,ignore,noplayground
impl Config {
    fn build(
        mut args: impl Iterator<Item = String>,
    ) -> Result<Config, &'static str> {
        args.next();

        let query = match args.next() {
            Some(arg) => arg,
            None => return Err("Didn't get a query string"),
        };

        let file_path = match args.next() {
            Some(arg) => arg,
            None => return Err("Didn't get a file path"),
        };

        let ignore_case = env::var("IGNORE_CASE").is_ok();

        Ok(Config {
            query,
            file_path,
            ignore_case,
        })
    }
}
```

</Listing>

মনে রাখো যে `env::args`-এর return value-এর প্রথম value টি হলো program-এর নাম। আমরা সেটি ignore করে পরের value-তে যেতে চাই, তাই প্রথমে আমরা `next` call করি এবং তার return value-এর সাথে কিছু করি না। তারপর আমরা `Config`-এর `query` field-এ রাখার জন্য যে value চাই সেটি পেতে আবার `next` call করি। যদি `next` টি `Some` return করে, তাহলে আমরা value টি extract করতে একটি `match` ব্যবহার করি। আর যদি সেটি `None` return করে, তার মানে পর্যাপ্ত argument দেওয়া হয়নি, এবং আমরা একটি `Err` value দিয়ে আগেই return করি। `file_path` value-টির জন্য আমরা একই কাজ করি।

<!-- Old headings. Do not remove or links may break. -->

<a id="making-code-clearer-with-iterator-adapters"></a>

### Clarifying Code with Iterator Adapters

আমরা আমাদের I/O project-এর `search` function-তেও iterator-এর সুবিধা নিতে পারি, যা Listing 12-19-এর মতো এখানে Listing 13-21-তে আবার দেখানো হয়েছে।

<Listing number="13-21" file-name="src/lib.rs" caption="The implementation of the `search` function from Listing 12-19">

```rust,ignore
pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    let mut results = Vec::new();

    for line in contents.lines() {
        if line.contains(query) {
            results.push(line);
        }
    }

    results
}
```

</Listing>

আমরা এই code টিকে iterator adapter method ব্যবহার করে আরও concise ভাবে লিখতে পারি। এতে আমরা একটি mutable intermediate `results` vector রাখা থেকেও মুক্তি পাই। Functional programming style বাড়তে mutable state-এর পরিমাণ কমাতে চায় যাতে code আরও স্পষ্ট হয়। Mutable state সরিয়ে ফেললে হয়তো ভবিষ্যতে এমন একটি enhancement সম্ভব হবে যেখানে search parallel-এ ঘটবে, কারণ `results` vector-এ concurrent access manage করতে হবে না। Listing 13-22 এই পরিবর্তন দেখায়।

<Listing number="13-22" file-name="src/lib.rs" caption="Using iterator adapter methods in the implementation of the `search` function">

```rust,ignore
pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    contents
        .lines()
        .filter(|line| line.contains(query))
        .collect()
}
```

</Listing>

স্মরণ করো যে `search` function-এর উদ্দেশ্য হলো `contents`-এর সব সেই line return করা যেগুলো `query` ধারণ করে। Listing 13-16-এর `filter` example-টির মতোই, এই code `filter` adapter ব্যবহার করে শুধু সেই line গুলোই রাখে যেগুলোর জন্য `line.contains(query)` টি `true` return করে। তারপর আমরা মেলা line গুলোকে `collect` দিয়ে আরেকটি vector-এ একত্রিত করি। অনেক সহজ! `search_case_insensitive` function-এও একই পরিবর্তন করে iterator method ব্যবহার করতে পারো।

আরও একটি improvement হিসেবে, `search` function থেকে `collect` call সরিয়ে দিয়ে এবং return type `impl Iterator<Item = &'a str>`-এ পরিবর্তন করে একটি iterator return করতে পারো, যাতে function-টি একটি iterator adapter হয়ে যায়। মনে রাখবে তোমাকে test গুলোও update করতে হবে! এই পরিবর্তনের আগে ও পরে তোমার `minigrep` tool দিয়ে একটি বড় file-এ search করে behavior-এর পার্থক্য দেখো। পরিবর্তনের আগে প্রোগ্রামটি সব ফলাফল collect না করা পর্যন্ত কোনো ফলাফল print করবে না, কিন্তু পরিবর্তনের পর প্রতিটি মেলা line পাওয়ার সাথে সাথেই ফলাফল print হবে, কারণ `run` function-এর `for` loop টি iterator-এর laziness-এর সুবিধা নিতে পারবে।

<!-- Old headings. Do not remove or links may break. -->

<a id="choosing-between-loops-or-iterators"></a>

### Choosing Between Loops এবং Iterators

পরবর্তী logical প্রশ্ন হলো তোমার নিজের code-এ তোমার কোন style বেছে নেওয়া উচিত এবং কেন: Listing 13-21-এর মূল implementation নাকি Listing 13-22-এর iterator ব্যবহার করা সংস্করণ (ধরে নিচ্ছি আমরা iterator return না করে সব ফলাফল আগেই collect করে নিচ্ছি)। বেশিরভাগ Rust programmer-ই iterator style ব্যবহার করতে পছন্দ করেন। প্রথমে এটা আয়ত্ব করা একটু কঠিন, কিন্তু একবার তুমি বিভিন্ন iterator adapter এবং সেগুলো কী করে সে সম্পর্কে ধারণা পেলে, iterator বুঝতে সহজ হয়। Loop-এর বিভিন্ন ছোট অংশ আর নতুন vector তৈরি করা নিয়ে ঘাঁটাঘাঁটির বদলে, code loop-টির high-level objective-এ focus করে। এতে কিছু commonplace code abstract হয়ে যায়, যাতে এই code-টির জন্য unique concept গুলো দেখা সহজ হয়, যেমন iterator-এর প্রতিটি element-কে অতিক্রম করতে হবে এমন filtering condition।

কিন্তু এই দুটি implementation কি সত্যিই equivalent? Intuitive ধারণা হতে পারে যে lower-level loop দ্রুত হবে। চলো performance নিয়ে কথা বলি।

[impl-trait]: ch10-02-traits.html#traits-as-parameters

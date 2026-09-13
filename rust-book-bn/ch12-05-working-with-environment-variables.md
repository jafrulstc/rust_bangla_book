## Environment Variable নিয়ে কাজ করা

আমরা `minigrep` binary-টিকে একটি extra feature যোগ করে উন্নত করব: একটি case-insensitive search option, যা user একটি environment variable-এর মাধ্যমে চালু করতে পারবে। আমরা এই feature-টিকে একটি command line option বানাতে পারতাম এবং প্রতিবার apply করতে চাইলে user-কে সেটি লিখতে বাধ্য করতে পারতাম, কিন্তু এর বদলে এটিকে একটি environment variable বানালে আমরা আমাদের user-দের একবার environment variable-টি set করতে দিই এবং সেই terminal session-এ তাদের সমস্ত search case insensitive হবে।

<!-- Old headings. Do not remove or links may break. -->
<a id="writing-a-failing-test-for-the-case-insensitive-search-function"></a>

### Case-Insensitive Search-এর জন্য একটি Failing Test লেখা

আমরা প্রথমে `minigrep` library-তে একটি নতুন `search_case_insensitive` function যোগ করব যা environment variable-এর কোনো value থাকলে call করা হবে। আমরা TDD process অনুসরণ করতে থাকব, তাই প্রথম ধাপ আবার একটি failing test লেখা। আমরা নতুন `search_case_insensitive` function-টির জন্য একটি নতুন test যোগ করব এবং দুটি test-এর মধ্যে পার্থক্য পরিষ্কার করতে আমাদের পুরোনো test-টির নাম `one_result` থেকে পরিবর্তন করে `case_sensitive` করব, যেমন Listing 12-20-তে দেখানো হয়েছে।

<Listing number="12-20" file-name="src/lib.rs" caption="আমরা যে case-insensitive function যোগ করতে চলেছি তার জন্য একটি নতুন failing test যোগ করা">

```rust,ignore,does_not_compile
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn case_sensitive() {
        let query = "duct";
        let contents = "\
Rust:
safe, fast, productive.
Pick three.
Duct tape.";

        assert_eq!(vec!["safe, fast, productive."], search(query, contents));
    }

    #[test]
    fn case_insensitive() {
        let query = "rUsT";
        let contents = "\
Rust:
safe, fast, productive.
Pick three.
Trust me.";

        assert_eq!(
            vec!["Rust:", "Trust me."],
            search_case_insensitive(query, contents)
        );
    }
}
```

</Listing>

খেয়াল করো যে আমরা পুরোনো test-এর `contents`-ও edit করেছি। আমরা একটি নতুন line যোগ করেছি যাতে text হলো `"Duct tape."`—বড় হাতের _D_ সহ—যা case-sensitive ভাবে খোঁজার সময় `"duct"` query-এর সাথে match করা উচিত নয়। পুরোনো test এভাবে পরিবর্তন করা নিশ্চিত করে যে আমরা accidental-ভাবে আগে থেকে implement করা case-sensitive search functionality-টি ভেঙে ফেলছি না। এই test-টি এখন pass করা উচিত এবং case-insensitive search নিয়ে কাজ করার সময়ও pass করতে থাকা উচিত।

Case-_insensitive_ search-এর নতুন test-টি তার query হিসেবে `"rUsT"` ব্যবহার করে। আমরা যে `search_case_insensitive` function যোগ করতে চলেছি সেখানে, `"rUsT"` query-টির বড় হাতের _R_ সহ `"Rust:"` line-টির সাথে match করা উচিত এবং `"Trust me."` line-টির সাথেও match করা উচিত, যদিও দুটোর case-ই query-এর থেকে আলাদা। এটি আমাদের failing test, এবং এটি compile করতে fail করবে কারণ আমরা এখনো `search_case_insensitive` function-টি define করিনি। তুমি চাইলে একটি skeleton implementation যোগ করতে পারো যা সবসময় একটি empty vector return করে, Listing 12-16-এ `search` function-এর জন্য যেভাবে আমরা করেছিলাম, যাতে test-টি compile হয়ে fail করে দেখা যায়।

### `search_case_insensitive` Function Implement করা

`search_case_insensitive` function-টি, যেমন Listing 12-21-তে দেখানো হয়েছে, `search` function-টির প্রায় একই হবে। একমাত্র পার্থক্য হলো আমরা `query` এবং প্রতিটি `line`-কে lowercase করে দেব, যাতে input argument গুলোর case যেমনই হোক না কেন, আমরা যখন check করব যে line-এ query আছে কিনা, তখন তারা একই case-এ থাকবে।

<Listing number="12-21" file-name="src/lib.rs" caption="তুলনা করার আগে query এবং line lowercase করতে `search_case_insensitive` function define করা">

```rust,noplayground
pub fn search_case_insensitive<'a>(
    query: &str,
    contents: &'a str,
) -> Vec<&'a str> {
    let query = query.to_lowercase();
    let mut results = Vec::new();

    for line in contents.lines() {
        if line.to_lowercase().contains(&query) {
            results.push(line);
        }
    }

    results
}
```

</Listing>

প্রথমে, আমরা `query` string-টিকে lowercase করি এবং একই নামের একটি নতুন variable-এ সংরক্ষণ করি, যা আসল `query`-কে shadow করে। Query-তে `to_lowercase` call করা প্রয়োজন যাতে user-এর query `"rust"`, `"RUST"`, `"Rust"`, বা `"rUsT"` যা-ই হোক না কেন, আমরা query-টিকে `"rust"` হিসেবে ধরে নেব এবং case-এর ব্যাপারে অসংবেদনশীল হব। যদিও `to_lowercase` basic Unicode handle করবে, এটি ১০০ শতাংশ নির্ভুল হবে না। আমরা যদি একটি আসল application লিখতাম, তবে আমরা এখানে আরও কিছু কাজ করতে চাইতাম, কিন্তু এই section-টি environment variable নিয়ে, Unicode নিয়ে নয়, তাই আমরা এখানেই সেটি রেখে দেব।

খেয়াল করো যে `query` এখন একটি string slice-এর বদলে একটি `String`, কারণ `to_lowercase` call করলে existing data-কে reference করার বদলে নতুন data তৈরি করে। উদাহরণ হিসেবে ধরো query টি হলো `"rUsT"`: সেই string slice-এ আমাদের ব্যবহারের জন্য কোনো lowercase `u` বা `t` নেই, তাই আমাদের `"rust"` ধারণ করে এমন একটি নতুন `String` allocate করতে হবে। যখন আমরা এখন `query`-কে `contains` method-এ argument হিসেবে pass করি, আমাদের একটি ampersand যোগ করতে হবে, কারণ `contains`-এর signature একটি string slice নেওয়ার জন্য define করা।

এরপর, আমরা সব character lowercase করতে প্রতিটি `line`-এ একটি `to_lowercase` call যোগ করি। এখন যেহেতু আমরা `line` এবং `query` দুটোকেই lowercase-এ রূপান্তর করেছি, query-এর case যেমনই হোক না কেন আমরা match খুঁজে পাব।

চলো দেখি এই implementation test গুলো pass করে কিনা:

```console
$ cargo test
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 1.33s
     Running unittests src/lib.rs (target/debug/deps/minigrep-9cd200e5fac0fc94)

running 2 tests
test tests::case_insensitive ... ok
test tests::case_sensitive ... ok

test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/debug/deps/minigrep-9cd200e5fac0fc94)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests minigrep

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

দারুণ! সব পাস করেছে। এখন চলো `run` function থেকে নতুন `search_case_insensitive` function-টিকে call করি। প্রথমে, আমরা `Config` struct-এ একটি configuration option যোগ করব যা case-sensitive এবং case-insensitive search-এর মধ্যে switch করবে। এই field যোগ করলে compiler error হবে কারণ আমরা এখনো এই field-টিকে কোথাও initialize করছি না:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
pub struct Config {
    pub query: String,
    pub file_path: String,
    pub ignore_case: bool,
}
```

আমরা `ignore_case` নামের field যোগ করেছি যা একটি Boolean ধারণ করে। এরপর, আমাদের `run` function-কে দরকার যেন সে `ignore_case` field-এর value check করে এবং সেটি ব্যবহার করে সিদ্ধান্ত নেয় যে `search` function call করবে নাকি `search_case_insensitive` function, যেমন Listing 12-22-তে দেখানো হয়েছে। এটি এখনো compile হবে না।

<Listing number="12-22" file-name="src/main.rs" caption="`config.ignore_case`-এর value-এর ওপর ভিত্তি করে `search` অথবা `search_case_insensitive` call করা">

```rust,ignore,does_not_compile
use minigrep::{search, search_case_insensitive};

// --snip--

fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let contents = fs::read_to_string(config.file_path)?;

    let results = if config.ignore_case {
        search_case_insensitive(&config.query, &contents)
    } else {
        search(&config.query, &contents)
    };

    for line in results {
        println!("{line}");
    }

    Ok(())
}
```

</Listing>

সবশেষে, আমাদের environment variable-টির জন্য check করতে হবে। Environment variable নিয়ে কাজ করার function গুলো standard library-এর `env` module-এ আছে, যেটি ইতিমধ্যে _src/main.rs_-এর উপরে scope-এ আছে। আমরা `env` module থেকে `var` function ব্যবহার করে check করব যে `IGNORE_CASE` নামের একটি environment variable-এর কোনো value set করা আছে কিনা, যেমন Listing 12-23-তে দেখানো হয়েছে।

<Listing number="12-23" file-name="src/main.rs" caption="`IGNORE_CASE` নামের একটি environment variable-এ কোনো value আছে কিনা তা check করা">

```rust,ignore,noplayground
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

এখানে, আমরা একটি নতুন variable, `ignore_case` তৈরি করি। এর value set করতে, আমরা `env::var` function call করি এবং একে `IGNORE_CASE` environment variable-টির নাম pass করি। `env::var` function একটি `Result` return করে যা সফল `Ok` variant হবে—যা environment variable-এর value ধারণ করে—যদি environment variable-টি কোনো value-তে set করা থাকে। এটি `Err` variant return করবে যদি environment variable-টি set না করা থাকে।

আমরা `Result`-এর উপর `is_ok` method ব্যবহার করে check করছি environment variable-টি set করা আছে কিনা, যার মানে program-টির case-insensitive search করা উচিত। যদি `IGNORE_CASE` environment variable-টি কোনো কিছুতেই set করা না থাকে, `is_ok` `false` return করবে এবং program-টি case-sensitive search করবে। আমরা environment variable-টির _value_-এ আগ্রহী নই, শুধু সেটি set করা আছে কিনা unset করা আছে তাতেই আগ্রহী, তাই আমরা `unwrap`, `expect` বা `Result`-এ আমরা যে অন্যান্য method দেখেছি সেগুলো ব্যবহার না করে `is_ok` check করছি।

আমরা `ignore_case` variable-এর value `Config` instance-এ pass করি, যাতে `run` function-টি সেই value পড়তে পারে এবং সিদ্ধান্ত নিতে পারে যে `search_case_insensitive` call করবে নাকি `search`, যেমন আমরা Listing 12-22-তে implement করেছি।

চলো এটি একবার চেষ্টা করি! প্রথমে, আমরা আমাদের program-টি environment variable set না করেই চালাব এবং query `to` দিয়ে, যা সমস্ত ছোট হাতের _to_ word ধারণ করে এমন সব line-এর সাথে match করা উচিত:

```console
$ cargo run -- to poem.txt
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.0s
     Running `target/debug/minigrep to poem.txt`
Are you nobody, too?
How dreary to be somebody!
```

মনে হচ্ছে এটি এখনো কাজ করছে! এখন চলো program-টি `IGNORE_CASE` কে `1` তে set করে চালাই, কিন্তু একই query `to` দিয়ে:

```console
$ IGNORE_CASE=1 cargo run -- to poem.txt
```

তুমি যদি PowerShell ব্যবহার করো, তবে environment variable-টি set করতে এবং program-টি চালাতে আলাদা command হিসেবে করতে হবে:

```console
PS> $Env:IGNORE_CASE=1; cargo run -- to poem.txt
```

এতে তোমার বাকি shell session-এর জন্য `IGNORE_CASE` persist হবে। এটি `Remove-Item` cmdlet দিয়ে unset করা যাবে:

```console
PS> Remove-Item Env:IGNORE_CASE
```

আমাদের এমন সব line পাওয়া উচিত যেগুলোতে _to_ আছে এবং সম্ভবত বড় হাতের অক্ষর সহ:

<!-- manual-regeneration
cd listings/ch12-an-io-project/listing-12-23
IGNORE_CASE=1 cargo run -- to poem.txt
can't extract because of the environment variable
-->

```console
Are you nobody, too?
How dreary to be somebody!
To tell your name the livelong day
To an admiring bog!
```

চমৎকার, আমরা _To_ ধারণ করে এমন line গুলোও পেয়েছি! আমাদের `minigrep` program এখন একটি environment variable দ্বারা নিয়ন্ত্রিত case-insensitive search করতে পারে। এখন তুমি জানো কীভাবে command line argument অথবা environment variable ব্যবহার করে set করা option manage করতে হয়।

কিছু program একই configuration-এর জন্য argument _এবং_ environment variable উভয়ই allow করে। সেই ক্ষেত্রে, program গুলো সিদ্ধান্ত নেয় যে কোনটি priority পাবে। তোমার নিজের অনুশীলনের জন্য আরেকটি কাজ হিসেবে, চেষ্টা করো case sensitivity একটি command line argument অথবা একটি environment variable দিয়ে নিয়ন্ত্রণ করতে। সিদ্ধান্ত নাও যদি program-টি এমনভাবে চালানো হয় যে একটি case sensitive-এ এবং অন্যটি ignore case-এ set করা থাকে তবে command line argument নাকি environment variable priority পাবে।

`std::env` module-এ environment variable নিয়ে কাজ করার জন্য আরও অনেক useful feature আছে: কী কী available তা দেখতে এর documentation দেখে নাও।

<!-- Old headings. Do not remove or links may break. -->
<a id="developing-the-librarys-functionality-with-test-driven-development"></a>

## Test-Driven Development দিয়ে Functionality যোগ করা

এখন যেহেতু search logic `main` function থেকে আলাদা করে _src/lib.rs_-এ রাখা হয়েছে, আমাদের code-এর core functionality-এর জন্য test লেখা অনেক সহজ। আমরা বিভিন্ন argument দিয়ে সরাসরি function call করতে পারি এবং command line থেকে আমাদের binary call না করেই return value check করতে পারি।

এই section-এ আমরা `minigrep` program-এ search করার logic যোগ করব test-driven development (TDD) process ব্যবহার করে, যার ধাপগুলো নিচে দেওয়া:

1. এমন একটি test লেখো যেটি fail করে এবং সেটি চালিয়ে নিশ্চিত করো যে সেটি তোমার প্রত্যাশিত কারণেই fail করেছে।
2. নতুন test-টি pass করার জন্য ঠিক যতটুকু দরকার ততটুকু code লেখো বা পরিবর্তন করো।
3. তুমি এইমাত্র যোগ করা বা পরিবর্তন করা code-টি refactor করো এবং নিশ্চিত করো যে test গুলো pass করতেই থাকে।
4. ধাপ 1 থেকে আবার শুরু করো!

যদিও এটি software লেখার অনেক উপায়ের মধ্যে একটি মাত্র, TDD code design drive করতে সাহায্য করে। Code লেখার আগে test লেখা সম্পূর্ণ process জুড়ে high test coverage বজায় রাখতে সাহায্য করে।

আমরা সেই functionality-টির implementation-এ test-driven approach নেব যা আসলে file content-এ query string খুঁজবে এবং query-এর সাথে match করা line-গুলোর একটি তালিকা তৈরি করব। আমরা এই functionality একটি `search` নামের function-এ যোগ করব।

### একটি Failing Test লেখা

_src/lib.rs_-এ, আমরা [Chapter 11][ch11-anatomy]<!-- ignore -->-এ যেমন করেছি তেমনি একটি `tests` module এবং একটি test function যোগ করব। Test function-টি নির্দিষ্ট করে দেয় আমরা `search` function-টির কী আচরণ চাই: এটি একটি query এবং search করার জন্য text নেবে, এবং text থেকে শুধু সেই line গুলোই return করবে যেগুলোতে query-টি আছে। Listing 12-15 এই test-টি দেখায়।

<Listing number="12-15" file-name="src/lib.rs" caption="আমাদের কাঙ্ক্ষিত functionality-র জন্য `search` function-টির একটি failing test তৈরি করা">

```rust,ignore,does_not_compile
// --snip--

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn one_result() {
        let query = "duct";
        let contents = "\
Rust:
safe, fast, productive.
Pick three.";

        assert_eq!(vec!["safe, fast, productive."], search(query, contents));
    }
}
```

</Listing>

এই test-টি `"duct"` string খোঁজে। আমরা যে text খুঁজছি সেটি তিনটি line, যার মধ্যে শুধু একটিতেই `"duct"` আছে (খেয়াল করো যে opening double quote-এর পরের backslash টি Rust-কে বলে এই string literal-এর content-এর শুরুতে কোনো newline character না রাখতে)। আমরা assert করি যে `search` function থেকে return হওয়া value-তে শুধু আমরা যে line আশা করি সেটিই আছে।

আমরা যদি এই test চালাই, এটি বর্তমানে fail করবে কারণ `unimplemented!` macro “not implemented” message দিয়ে panic করে। TDD-র নীতি অনুসারে, আমরা ছোট একটি ধাপ নেব—`search` function-টিকে সবসময় একটি empty vector return করতে define করে function-টিকে call করার সময় panic না করার জন্য যতটুকু দরকার ততটুকু code যোগ করব—যেমন Listing 12-16-তে দেখানো হয়েছে। তারপর, test-টি compile হবে এবং fail করবে, কারণ একটি empty vector `"safe, fast, productive."` line ধারণকারী vector-এর সাথে match করে না।

<Listing number="12-16" file-name="src/lib.rs" caption="`search` function-টির ঠিক ততটুকু define করা যাতে এটি call করলে panic না করে">

```rust,noplayground
pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    vec![]
}
```

</Listing>

এখন চলো আলোচনা করি কেন `search`-এর signature-এ আমরা একটি স্পষ্ট lifetime `'a` define করতে হবে এবং সেই lifetime-টি `contents` argument এবং return value-এর সাথে ব্যবহার করতে হবে। [Chapter 10][ch10-lifetimes]<!-- ignore -->-তে মনে করো, lifetime parameter গুলো নির্দিষ্ট করে দেয় কোন argument-এর lifetime return value-এর lifetime-এর সাথে সংযুক্ত। এই ক্ষেত্রে, আমরা নির্দেশ করছি যে return হওয়া vector-টিতে এমন string slice থাকবে যেগুলো `contents` argument-এর slice-কে reference করে (argument `query`-কে নয়)।

অর্থাৎ, আমরা Rust-কে বলছি যে `search` function দ্বারা return করা data `search` function-এ `contents` argument হিসেবে pass করা data-এর সমান দীর্ঘ থাকবে। এটি গুরুত্বপূর্ণ! একটি slice _দ্বারা_ reference করা data-টি reference বৈধ হওয়ার জন্য বৈধ থাকা প্রয়োজন; যদি compiler ধরে নেয় যে আমরা `contents`-এর বদলে `query`-এর string slice বানাচ্ছি, তবে এটি তার safety checking ভুলভাবে করবে।

আমরা যদি lifetime annotation ভুলে যাই এবং এই function-টি compile করার চেষ্টা করি, আমরা এই error পাব:

```console
$ cargo build
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
error[E0106]: missing lifetime specifier
 --> src/lib.rs:1:51
  |
1 | pub fn search(query: &str, contents: &str) -> Vec<&str> {
  |                      ----            ----         ^ expected named lifetime parameter
  |
  = help: this function's return type contains a borrowed value, but the signature does not say whether it is borrowed from `query` or `contents`
help: consider introducing a named lifetime parameter
  |
1 | pub fn search<'a>(query: &'a str, contents: &'a str) -> Vec<&'a str> {
  |              ++++         ++                 ++              ++

For more information about this error, try `rustc --explain E0106`.
error: could not compile `minigrep` (lib) due to 1 previous error
```

Rust জানতে পারে না আমাদের output-এর জন্য দুটি parameter-এর কোনটি দরকার, তাই আমাদের সেটি স্পষ্টভাবে বলতে হবে। খেয়াল করো যে help text-টি সব parameter এবং output type-এর জন্য একই lifetime parameter specify করার পরামর্শ দেয়, যা ভুল! যেহেতু `contents`-ই সেই parameter যা আমাদের সমস্ত text ধারণ করে এবং আমরা সেই text-এর যে অংশগুলো match করে সেগুলো return করতে চাই, আমরা জানি `contents`-ই একমাত্র parameter যেটির সাথে lifetime syntax ব্যবহার করে return value-টিকে সংযুক্ত করা উচিত।

অন্যান্য programming language-এ argument গুলোকে signature-এ return value-এর সাথে সংযুক্ত করতে বাধ্য করে না, কিন্তু এই অভ্যাস সময়ের সাথে সাথে সহজ হবে। তুমি হয়তো এই উদাহরণটির সাথে Chapter 10-এর [“Validating References with Lifetimes”][validating-references-with-lifetimes]<!-- ignore --> section-এর উদাহরণগুলো তুলনা করতে চাইতে পারো।

### Test Pass করার জন্য Code লেখা

বর্তমানে আমাদের test fail করছে কারণ আমরা সবসময় একটি empty vector return করি। সেটি ঠিক করতে এবং `search` implement করতে, আমাদের program-কে নিচের ধাপগুলো অনুসরণ করতে হবে:

1. contents-এর প্রতিটি line এর মধ্য দিয়ে iterate করো।
2. Check করো যে line-টিতে আমাদের query string আছে কিনা।
3. থাকলে, সেটিকে আমরা যে return করছি সেই value-গুলোর তালিকায় যোগ করো।
4. না থাকলে, কিছু করো না।
5. Match করা result গুলোর তালিকা return করো।

চলো প্রতিটি ধাপ নিয়ে কাজ করি, line গুলোর মধ্য দিয়ে iterate করা থেকে শুরু করে।

#### `lines` Method দিয়ে Line গুলোর মধ্য দিয়ে Iterate করা

Rust-এ string-এর line-by-line iteration handle করার জন্য একটি সহায়ক method আছে, সুবিধাজনকভাবে যার নাম `lines`, যেটি Listing 12-17-এ দেখানোর মতো কাজ করে। খেয়াল রাখো এটি এখনো compile হবে না।

<Listing number="12-17" file-name="src/lib.rs" caption="`contents`-এর প্রতিটি line-এর মধ্য দিয়ে iterate করা">

```rust,ignore,does_not_compile
pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    for line in contents.lines() {
        // do something with line
    }
}
```

</Listing>

`lines` method একটি iterator return করে। Iterator সম্পর্কে আমরা [Chapter 13][ch13-iterators]<!-- ignore -->-এ গভীরভাবে আলোচনা করব। কিন্তু মনে করো, তুমি [Listing 3-5][ch3-iter]<!-- ignore -->-এ একটি iterator ব্যবহারের এই উপায় দেখেছিলে, যেখানে আমরা একটি collection-এর প্রতিটি item-এ কিছু code চালানোর জন্য iterator সহ একটি `for` loop ব্যবহার করেছিলাম।

#### প্রতিটি Line-এ Query খোঁজা

এরপর, আমরা check করব যে বর্তমান line-টিতে আমাদের query string আছে কিনা। সৌভাগ্যক্রমে, string-এ এমন একটি সহায়ক method আছে যার নাম `contains` যা এই কাজটি আমাদের জন্য করে! `search` function-এ Listing 12-18-এ দেখানোর মতো `contains` method-এ একটি call যোগ করো। খেয়াল রাখো এটিও এখনো compile হবে না।

<Listing number="12-18" file-name="src/lib.rs" caption="Line-টিতে `query`-এর string আছে কিনা তা দেখার জন্য functionality যোগ করা">

```rust,ignore,does_not_compile
pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    for line in contents.lines() {
        if line.contains(query) {
            // do something with line
        }
    }
}
```

</Listing>

এই মুহূর্তে, আমরা functionality তৈরি করছি। Code-টি compile করাতে, আমাদের function signature-তে যেমন নির্দেশ করেছিলাম তেমন body থেকে একটি value return করতে হবে।

#### Match করা Line সংরক্ষণ করা

এই function-টি শেষ করতে, আমাদের return করতে চাওয়া match করা line গুলো সংরক্ষণ করার একটি উপায় দরকার। সেটির জন্য, আমরা `for` loop-এর আগে একটি mutable vector বানাতে পারি এবং vector-এ একটি `line` সংরক্ষণ করতে `push` method call করতে পারি। `for` loop-এর পরে, আমরা vector-টি return করি, যেমন Listing 12-19-তে দেখানো হয়েছে।

<Listing number="12-19" file-name="src/lib.rs" caption="Match করা line গুলো সংরক্ষণ করা যাতে সেগুলো return করা যায়">

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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn one_result() {
        let query = "duct";
        let contents = "\
Rust:
safe, fast, productive.
Pick three.";

        assert_eq!(vec!["safe, fast, productive."], search(query, contents));
    }
}
```

</Listing>

এখন `search` function-টি শুধু সেই line গুলোই return করবে যেগুলোতে `query` আছে, এবং আমাদের test pass করা উচিত। চলো test চালাই:

```console
$ cargo test
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 1.22s
     Running unittests src/lib.rs (target/debug/deps/minigrep-9cd200e5fac0fc94)

running 1 test
test tests::one_result ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/debug/deps/minigrep-9cd200e5fac0fc94)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests minigrep

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

আমাদের test pass করেছে, তাই আমরা জানি এটি কাজ করে!

এই মুহূর্তে, আমরা ভাবতে পারি search function-টির implementation refactor করার সুযোগ নিয়ে, যাতে একই functionality বজায় রেখে test গুলো pass করে। search function-এর code-টি খুব খারাপ নয়, কিন্তু এটি iterator-এর কিছু কার্যকর feature ব্যবহার করে না। আমরা এই উদাহরণে [Chapter 13][ch13-iterators]<!-- ignore -->-এ ফিরে যাব, যেখানে আমরা iterator বিস্তারিতভাবে আলোচনা করব, এবং এটিকে কীভাবে উন্নত করা যায় দেখব।

এখন সম্পূর্ণ program-টি কাজ করা উচিত! চলো এটি চেষ্টা করি, প্রথমে এমন একটি word দিয়ে যা Emily Dickinson-এর poem থেকে ঠিক একটি line return করবে: _frog_।

```console
$ cargo run -- frog poem.txt
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.38s
     Running `target/debug/minigrep frog poem.txt`
How public, like a frog
```

দারুণ! এখন চলো এমন একটি word দিয়ে চেষ্টা করি যা একাধিক line-এর সাথে match করবে, যেমন _body_:

```console
$ cargo run -- body poem.txt
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.0s
     Running `target/debug/minigrep body poem.txt`
I'm nobody! Who are you?
Are you nobody, too?
How dreary to be somebody!
```

এবং সবশেষে, চলো নিশ্চিত করি যে আমরা poem-এ এমন কোনো word খুঁজলে কোনো line পাব না যা কোথাও নেই, যেমন _monomorphization_:

```console
$ cargo run -- monomorphization poem.txt
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.0s
     Running `target/debug/minigrep monomorphization poem.txt`
```

চমৎকার! আমরা একটি classic tool-এর নিজস্ব mini সংস্করণ বানিয়েছি এবং application কীভাবে structure করতে হয় তা নিয়ে অনেক কিছু শিখেছি। আমরা file input এবং output, lifetime, testing এবং command line parsing সম্পর্কেও কিছু শিখেছি।

এই project সম্পূর্ণ করতে, আমরা সংক্ষেপে দেখাবো কীভাবে environment variable নিয়ে কাজ করতে হয় এবং কীভাবে standard error-এ print করতে হয়—দুটোই command line program লেখার সময় কাজে লাগে।

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[ch11-anatomy]: ch11-01-writing-tests.html#the-anatomy-of-a-test-function
[ch10-lifetimes]: ch10-03-lifetime-syntax.html
[ch3-iter]: ch03-05-control-flow.html#looping-through-a-collection-with-for
[ch13-iterators]: ch13-02-iterators.html

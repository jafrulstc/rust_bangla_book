## Appendix A: Keywords

নিচের তালিকাগুলোতে এমন সব keyword রয়েছে, যেগুলো Rust language বর্তমান বা ভবিষ্যতে ব্যবহারের জন্য reserve করে রেখেছে। তাই এগুলোকে identifier হিসেবে ব্যবহার করা যায় না (শুধু raw identifier হিসেবে ব্যবহার করা ছাড়া, যেটা আমরা [“Raw Identifiers”][raw-identifiers]<!-- ignore --> section-এ আলোচনা করব)। _Identifier_ হলো function, variable, parameter, struct field, module, crate, constant, macro, static value, attribute, type, trait বা lifetime-এর নাম।

[raw-identifiers]: #raw-identifiers

### বর্তমানে ব্যবহৃত Keywords

নিচে বর্তমানে ব্যবহৃত সব keyword-এর তালিকা ও তাদের কার্যকারিতা দেওয়া হলো।

- **`as`**: primitive casting করতে, কোনো item ধারণ করে এমন নির্দিষ্ট trait disambiguate করতে, অথবা `use` statement-এ item rename করতে।
- **`async`**: বর্তমান thread block না করে একটি `Future` return করতে।
- **`await`**: একটি `Future`-এর result প্রস্তুত না হওয়া পর্যন্ত execution স্থগিত রাখতে।
- **`break`**: loop থেকে সঙ্গে সঙ্গে বেরিয়ে আসতে।
- **`const`**: constant item বা constant raw pointer define করতে।
- **`continue`**: পরবর্তী loop iteration-এ চলতে।
- **`crate`**: module path-এ crate root-কে নির্দেশ করতে।
- **`dyn`**: trait object-এ dynamic dispatch করতে।
- **`else`**: `if` এবং `if let` control flow construct-এর বিকল্প হিসেবে।
- **`enum`**: একটি enumeration define করতে।
- **`extern`**: external function বা variable link করতে।
- **`false`**: Boolean false literal।
- **`fn`**: function বা function pointer type define করতে।
- **`for`**: একটি iterator থেকে item-এ loop করতে, trait implement করতে, অথবা higher ranked lifetime উল্লেখ করতে।
- **`if`**: conditional expression-এর ফলাফলের ভিত্তিতে branch তৈরি করতে।
- **`impl`**: inherent বা trait functionality implement করতে।
- **`in`**: `for` loop syntax-এর অংশ।
- **`let`**: variable bind করতে।
- **`loop`**: শর্তহীনভাবে loop করতে।
- **`match`**: একটি value-কে pattern-এর সাথে match করতে।
- **`mod`**: একটি module define করতে।
- **`move`**: একটি closure-কে তার সব capture-এর ownership নিতে বাধ্য করতে।
- **`mut`**: reference, raw pointer বা pattern binding-এ mutability নির্দেশ করতে।
- **`pub`**: struct field, `impl` block বা module-এ public visibility নির্দেশ করতে।
- **`ref`**: reference দ্বারা bind করতে।
- **`return`**: function থেকে return করতে।
- **`Self`**: যে type আমরা define বা implement করছি তার জন্য একটি type alias।
- **`self`**: method-এর subject বা বর্তমান module।
- **`static`**: পুরো program execution জুড়ে থাকা global variable বা lifetime।
- **`struct`**: একটি structure define করতে।
- **`super`**: বর্তমান module-এর parent module।
- **`trait`**: একটি trait define করতে।
- **`true`**: Boolean true literal।
- **`type`**: type alias বা associated type define করতে।
- **`union`**: একটি [union][union]<!-- ignore --> define করতে; শুধু union declaration-এ ব্যবহৃত হলেই keyword।
- **`unsafe`**: unsafe code, function, trait বা implementation নির্দেশ করতে।
- **`use`**: symbol-কে scope-এ আনতে।
- **`where`**: type constrain করে এমন clause নির্দেশ করতে।
- **`while`**: একটি expression-এর ফলাফলের ভিত্তিতে শর্তসাপেক্ষ loop করতে।

[union]: ../reference/items/unions.html

### ভবিষ্যতে ব্যবহারের জন্য Reserved Keywords

নিচের keyword-গুলোর বর্তমানে কোনো কার্যকারিতা নেই, কিন্তু Rust সম্ভাব্য ভবিষ্যৎ ব্যবহারের জন্য সেগুলো reserve করে রেখেছে:

- `abstract`
- `become`
- `box`
- `do`
- `final`
- `gen`
- `macro`
- `override`
- `priv`
- `try`
- `typeof`
- `unsized`
- `virtual`
- `yield`

### Raw Identifiers

_Raw identifier_ হলো এমন একটি syntax যা তোমাকে keyword-কে এমন জায়গায় ব্যবহার করতে দেয় যেখানে সাধারণত এটা অনুমোদিত নয়। কোনো keyword-এর আগে `r#` যোগ করে তুমি একটি raw identifier ব্যবহার করতে পারো।

উদাহরণস্বরূপ, `match` একটি keyword। যদি তুমি নিচের function-টি compile করার চেষ্টা করো যেটি `match`-কে নিজের নাম হিসেবে ব্যবহার করে:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
fn match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}
```

তাহলে এই error-টি পাবে:

```text
error: expected identifier, found keyword `match`
 --> src/main.rs:4:4
  |
4 | fn match(needle: &str, haystack: &str) -> bool {
  |    ^^^^^ expected identifier, found keyword
```

এই error থেকে বোঝা যাচ্ছে যে তুমি `match` keyword-টিকে function identifier হিসেবে ব্যবহার করতে পারবে না। `match`-কে function নাম হিসেবে ব্যবহার করতে হলে তোমাকে raw identifier syntax ব্যবহার করতে হবে, এভাবে:

<span class="filename">Filename: src/main.rs</span>

```rust
fn r#match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}

fn main() {
    assert!(r#match("foo", "foobar"));
}
```

এই code-টি কোনো error ছাড়াই compile হবে। লক্ষ্য করো function definition-এ এবং `main`-এ function call করার সময় উভয় জায়গায় function নামে `r#` prefix ব্যবহৃত হয়েছে।

Raw identifier তোমাকে যেকোনো শব্দকে identifier হিসেবে ব্যবহার করতে দেয়, এমনকি সেই শব্দটি যদি একটি reserved keyword-ও হয়। এটি identifier নাম বাছাইয়ে আরও বেশি স্বাধীনতা দেয়, এবং এমন ভাষায় লেখা program-এর সাথে integrate করতে সাহায্য করে যেখানে এই শব্দগুলো keyword নয়। এছাড়াও, raw identifier তোমাকে এমন library ব্যবহার করতে দেয় যা তোমার crate-এ ব্যবহৃত Rust edition থেকে ভিন্ন একটি edition-এ লেখা। উদাহরণস্বরূপ, `try` 2015 edition-এ keyword নয়, কিন্তু 2018, 2021 এবং 2024 edition-এ এটি keyword। যদি তুমি এমন একটি library-র উপর নির্ভর করো যা 2015 edition-এ লেখা এবং যার একটি `try` function আছে, তাহলে পরবর্তী edition-গুলো থেকে সেই function-কে call করতে তোমাকে raw identifier syntax—এই ক্ষেত্রে `r#try`—ব্যবহার করতে হবে। edition সম্পর্কে আরও তথ্যের জন্য [Appendix E][appendix-e]<!-- ignore --> দেখো।

[appendix-e]: appendix-05-editions.html

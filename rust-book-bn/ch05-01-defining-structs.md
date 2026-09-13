## Struct Define এবং Instantiate করা

Struct, tuple-এর সাথে মিল রাখে (tuple নিয়ে [“The Tuple Type”][tuples]<!-- ignore --> section-এ আলোচনা করা হয়েছে)—এই অর্থে যে দুটোই একাধিক সম্পর্কিত value ধরে রাখে। Tuple-এর মতোই struct-এর প্রতিটি অংশ ভিন্ন ভিন্ন type-এর হতে পারে। কিন্তু tuple-এর থেকে পার্থক্য হলো, struct-এ তুমি প্রতিটি data-এর নাম দাও, ফলে value-গুলোর অর্থ কী তা স্পষ্ট হয়ে যায়। এই নাম যোগ করার কারণে struct, tuple-এর চেয়ে বেশি flexible: একটি instance-এর value উল্লেখ বা access করতে তোমাকে data-এর ক্রমের ওপর নির্ভর করতে হয় না।

একটি struct define করতে আমরা `struct` keyword লিখি এবং পুরো struct-এর একটি নাম দিই। Struct-এর নামটি এমন হওয়া উচিত যেটা একসাথে গোছানো data অংশগুলোর তাৎপর্য বর্ণনা করে। তারপর, curly brackets-এর ভেতরে আমরা data অংশগুলোর নাম ও type define করি, যাদের আমরা _field_ বলি। যেমন, Listing 5-1-এ এমন একটি struct দেখানো হয়েছে যেটা একটি user account সম্পর্কিত তথ্য সংরক্ষণ করে।

<Listing number="5-1" file-name="src/main.rs" caption="একটি `User` struct definition">

```rust
struct User {
    active: bool,
    username: String,
    email: String,
    sign_in_count: u64,
}
```

</Listing>

Struct define করার পর সেটা ব্যবহার করতে হলে, আমরা প্রতিটি field-এর জন্য concrete value দিয়ে সেই struct-এর একটি _instance_ তৈরি করি। আমরা struct-এর নাম লিখে তারপর curly brackets যোগ করে instance তৈরি করি, যেখানে _`key: value`_ pair থাকে—key হলো field-গুলোর নাম আর value হলো সেই field-এ যে data রাখতে চাই। field-গুলো struct-এ যে ক্রমে declare করা ছিল, instance তৈরির সময় ঠিক সেই ক্রমে উল্লেখ করতে হবে এমন কোনো বাধ্যবাধকতা নেই। অর্থাৎ, struct definition হলো সেই type-এর একটি সাধারণ template, আর instance গুলো সেই template-এ নির্দিষ্ট data বসিয়ে সেই type-এর value তৈরি করে। যেমন, Listing 5-2-তে আমরা একজন নির্দিষ্ট user-কে দেখানোর মতো declare করতে পারি।

<Listing number="5-2" file-name="src/main.rs" caption="`User` struct-এর একটি instance তৈরি করা">

```rust
fn main() {
    let user1 = User {
        active: true,
        username: String::from("someusername123"),
        email: String::from("someone@example.com"),
        sign_in_count: 1,
    };
}
```

</Listing>

Struct থেকে কোনো নির্দিষ্ট value পেতে আমরা dot notation ব্যবহার করি। যেমন, এই user-এর email address access করতে আমরা `user1.email` ব্যবহার করি। যদি instance-টি mutable হয়, তাহলে dot notation ব্যবহার করে নির্দিষ্ট কোনো field-এ value assign করে সেটা পরিবর্তন করতে পারি। Listing 5-3-এ দেখানো হয়েছে কীভাবে একটি mutable `User` instance-এর `email` field-এর value পরিবর্তন করা যায়।

<Listing number="5-3" file-name="src/main.rs" caption="একটি `User` instance-এর `email` field-এর value পরিবর্তন করা">

```rust
fn main() {
    let mut user1 = User {
        active: true,
        username: String::from("someusername123"),
        email: String::from("someone@example.com"),
        sign_in_count: 1,
    };

    user1.email = String::from("anotheremail@example.com");
}
```

</Listing>

খেয়াল করো যে পুরো instance-টিকেই mutable হতে হবে; Rust আমাদের শুধু কিছু field-কে mutable হিসেবে চিহ্নিত করতে দেয় না। যেকোনো expression-এর মতো, আমরা function body-র শেষ expression হিসেবে struct-এর একটি নতুন instance construct করতে পারি, যাতে সেই নতুন instance-টি implicitly return হয়।

Listing 5-4-এ একটি `build_user` function দেখানো হয়েছে যেটা দেওয়া email ও username সহ একটি `User` instance return করে। `active` field-এর value হয় `true`, আর `sign_in_count`-এর value হয় `1`।

<Listing number="5-4" file-name="src/main.rs" caption="একটি `build_user` function যেটা email ও username নেয় এবং একটি `User` instance return করে">

```rust
fn build_user(email: String, username: String) -> User {
    User {
        active: true,
        username: username,
        email: email,
        sign_in_count: 1,
    }
}
```

</Listing>

Function parameter-এর নাম struct field-এর নামের সাথে মিলিয়ে রাখাটা যৌক্তিক, কিন্তু `email` ও `username` field-এর নাম আর variable বারবার লিখতে হয়—এটা কিছুটা ক্লান্তিকর। যদি struct-এ আরও বেশি field থাকত, তাহলে প্রতিটির নাম বারবার লিখতে গিয়ে আরও বিরক্তিকর হয়ে যেত। সৌভাগ্যক্রমে, এর জন্য একটি সুবিধাজনক shorthand আছে!

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-field-init-shorthand-when-variables-and-fields-have-the-same-name"></a>

### Field Init Shorthand ব্যবহার করা

যেহেতু Listing 5-4-এ parameter-এর নাম আর struct field-এর নাম হুবহু এক, আমরা _field init shorthand_ syntax ব্যবহার করে `build_user` আবার লিখতে পারি। এতে function-টি ঠিক আগের মতোই কাজ করবে, কিন্তু `username` ও `email` বারবার লিখতে হবে না, যেমনটা Listing 5-5-তে দেখানো হয়েছে।

<Listing number="5-5" file-name="src/main.rs" caption="একটি `build_user` function যেটা field init shorthand ব্যবহার করে কারণ `username` ও `email` parameter-এর নাম struct field-এর নামের সমান">

```rust
fn build_user(email: String, username: String) -> User {
    User {
        active: true,
        username,
        email,
        sign_in_count: 1,
    }
}
```

</Listing>

এখানে আমরা `User` struct-এর একটি নতুন instance তৈরি করছি, যেটার `email` নামে একটি field আছে। আমরা চাই `email` field-এর value হোক `build_user` function-এর `email` parameter-এ থাকা value। যেহেতু `email` field আর `email` parameter-এর নাম এক, তাই `email: email` না লিখে শুধু `email` লিখলেই চলবে।

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-instances-from-other-instances-with-struct-update-syntax"></a>

### Struct Update Syntax দিয়ে Instance তৈরি করা

প্রায়ই দরকার হয় এমন একটি নতুন struct instance তৈরি করা, যেটা একই type-এর অন্য কোনো instance-এর বেশিরভাগ value নেয়, কিন্তু কিছু value পরিবর্তন করে। তুমি এটা struct update syntax দিয়ে করতে পারো।

প্রথমে, Listing 5-6-তে দেখানো হলো কীভাবে নিয়মিত উপায়ে—update syntax ছাড়া—`user2`-তে একটি নতুন `User` instance তৈরি করা যায়। আমরা `email`-এর জন্য নতুন value সেট করছি, কিন্তু বাকি field-গুলোর জন্য Listing 5-2-তে তৈরি করা `user1`-এর একই value ব্যবহার করছি।

<Listing number="5-6" file-name="src/main.rs" caption="`user1`-এর সব value একটা ছাড়া ব্যবহার করে নতুন একটি `User` instance তৈরি করা">

```rust
fn main() {
    // --snip--

    let user2 = User {
        active: user1.active,
        username: user1.username,
        email: String::from("another@example.com"),
        sign_in_count: user1.sign_in_count,
    };
}
```

</Listing>

Struct update syntax ব্যবহার করলে আমরা কম কোডে একই ফল পেতে পারি, যেমন Listing 5-7-তে দেখানো হয়েছে। `..` syntax নির্দেশ করে যে বাকি field-গুলো—যেগুলো স্পষ্টভাবে set করা হয়নি—সেগুলো দেওয়া instance-এর field-এর একই value পাবে।

<Listing number="5-7" file-name="src/main.rs" caption="Struct update syntax ব্যবহার করে একটি `User` instance-এর জন্য নতুন `email` value সেট করা হলেও বাকি value-গুলো `user1` থেকে নেওয়া">

```rust
fn main() {
    // --snip--

    let user2 = User {
        email: String::from("another@example.com"),
        ..user1
    };
}
```

</Listing>

Listing 5-7-এর কোডও `user2`-তে এমন একটি instance তৈরি করে যার `email` value ভিন্ন, কিন্তু `username`, `active` ও `sign_in_count` field-এর value `user1`-এর মতোই। বাকি field-গুলো যেন `user1`-এর সংশ্লিষ্ট field থেকে value পায়, তা বোঝাতে `..user1` সবার শেষে থাকতে হবে। তবে struct definition-এ যে ক্রমে field থাকুক, আমরা যত খুশি তত field-এর value যেকোনো ক্রমে উল্লেখ করতে পারি।

খেয়াল রাখো, struct update syntax assignment-এর মতো `=` ব্যবহার করে; কারণ এটি data-কে move করে, ঠিক যেমনটা আমরা [“Variables and Data Interacting with Move”][move]<!-- ignore --> section-এ দেখেছি। এই উদাহরণে, `user2` তৈরির পর আমরা আর `user1` ব্যবহার করতে পারব না, কারণ `user1`-এর `username` field-এর `String` value-টি `user2`-তে move হয়ে গেছে। যদি আমরা `user2`-এর `email` ও `username` দুটোর জন্যই নতুন `String` value দিতাম, তাহলে `user1` থেকে শুধু `active` ও `sign_in_count` value ব্যবহার করা হতো, আর তখন `user2` তৈরির পরও `user1` valid থাকত। `active` ও `sign_in_count` উভয়ই এমন type যেগুলো `Copy` trait implement করে, তাই [“Stack-Only Data: Copy”][copy]<!-- ignore --> section-এ আলোচিত behavior প্রযোজ্য হবে। এই উদাহরণে আমরা `user1.email`-ও ব্যবহার করতে পারব, কারণ এর value `user1` থেকে move করা হয়নি।

<!-- Old headings. Do not remove or links may break. -->

<a id="using-tuple-structs-without-named-fields-to-create-different-types"></a>

### Tuple Struct দিয়ে ভিন্ন Type তৈরি করা

Rust এমন struct-ও সমর্থন করে যেগুলো tuple-এর মতো দেখতে—এগুলোকে _tuple struct_ বলা হয়। Tuple struct-এ struct-এর নাম যে অর্থ বহন করে তা থাকে, কিন্তু field-এর সাথে নাম যুক্ত থাকে না; বরং শুধু field-গুলোর type থাকে। Tuple struct তখন কাজে লাগে যখন তুমি পুরো tuple-কে একটি নাম দিতে চাও এবং অন্যান্য tuple থেকে একে আলাদা type বানাতে চাও, আর যখন সাধারণ struct-এর মতো প্রতিটি field-এ নাম দেওয়া দীর্ঘ বা অপ্রয়োজনীয় হয়ে যায়।

একটি tuple struct define করতে, `struct` keyword ও struct-এর নাম দিয়ে শুরু করো, তারপর tuple-এর type-গুলো দাও। যেমন, এখানে আমরা `Color` ও `Point` নামে দুটি tuple struct define ও ব্যবহার করছি:

<Listing file-name="src/main.rs">

```rust
struct Color(i32, i32, i32);
struct Point(i32, i32, i32);

fn main() {
    let black = Color(0, 0, 0);
    let origin = Point(0, 0, 0);
}
```

</Listing>

খেয়াল করো যে `black` আর `origin` value ভিন্ন type-এর, কারণ এগুলো ভিন্ন tuple struct-এর instance। তুমি যেটা define করো প্রতিটি struct নিজেই একটি আলাদা type, এমনকি struct-এর ভেতরের field-গুলোর type একই হলেও। যেমন, এমন একটি function যেটা `Color` type-এর parameter নেয়, সেটা `Point` কে argument হিসেবে নিতে পারবে না, যদিও দুটো type-ই তিনটি `i32` value নিয়ে গঠিত। অন্যদিকে, tuple struct instance-গুলো tuple-এর মতোই—এগুলোকে আলাদা অংশে destructure করা যায়, আর `.` ও index ব্যবহার করে কোনো একক value access করা যায়। কিন্তু tuple-এর থেকে পার্থক্য হলো, tuple struct-কে destructure করার সময় struct-এর type-এর নাম উল্লেখ করতে হয়। যেমন, `origin` point-এর value-গুলোকে `x`, `y`, ও `z` নামের variable-এ destructure করতে আমরা `let Point(x, y, z) = origin;` লিখব।

<!-- Old headings. Do not remove or links may break. -->

<a id="unit-like-structs-without-any-fields"></a>

### Unit-Like Struct Define করা

তুমি এমন struct-ও define করতে পারো যেগুলোর কোনো field নেই! এগুলোকে _unit-like struct_ বলা হয় কারণ এগুলো `()`-এর মতো আচরণ করে—`()` হলো সেই unit type যেটার কথা [“The Tuple Type”][tuples]<!-- ignore --> section-এ বলা হয়েছিল। Unit-like struct তখন কাজে দেয় যখন তোমাকে কোনো type-এ একটি trait implement করতে হবে কিন্তু type-এর ভেতরে নিজে কোনো data সংরক্ষণ করতে হবে না। Trait নিয়ে আমরা Chapter 10-এ আলোচনা করব। এইখানে `AlwaysEqual` নামে একটি unit struct declare ও instantiate করার উদাহরণ দেখানো হলো:

<Listing file-name="src/main.rs">

```rust
struct AlwaysEqual;

fn main() {
    let subject = AlwaysEqual;
}
```

</Listing>

`AlwaysEqual` define করতে আমরা `struct` keyword, যে নামটা চাই, আর তারপর একটি semicolon ব্যবহার করি। কোনো curly brackets বা parentheses-এর দরকার নেই! তারপর, আমরা প্রায় একইভাবে `subject` variable-এ `AlwaysEqual`-এর একটি instance পেতে পারি: যে নাম define করেছি সেটা ব্যবহার করে, কোনো curly brackets বা parentheses ছাড়াই। কল্পনা করো যে পরে আমরা এই type-এর জন্য এমন behavior implement করব যেন `AlwaysEqual`-এর প্রতিটি instance যেকোনো অন্য type-ের প্রতিটি instance-এর সাথে সবসময় equal হয়—হয়ত testing-এর প্রয়োজনে একটি জানা ফল পাওয়ার জন্য। সেই behavior implement করতে আমাদের কোনো data-এর দরকার হবে না! Chapter 10-তে তুমি দেখবে কীভাবে trait define করতে হয় আর সেগুলো যেকোনো type-এ—unit-like struct সহ—implement করতে হয়।

> ### Struct Data-এর Ownership
>
> Listing 5-1-এর `User` struct definition-ে আমরা `&str` string slice type-এর বদলে owned `String` type ব্যবহার করেছি। এটা ইচ্ছাকৃত পছন্দ, কারণ আমরা চাই এই struct-এর প্রতিটি instance নিজের সব data-এর owner হোক আর সেই data ততক্ষণ valid থাকুক যতক্ষণ পুরো struct valid থাকে।
>
> Struct-এর অন্য কিছুর মালিকানাধীন data-এর reference সংরক্ষণ করাও সম্ভব, কিন্তু তার জন্য _lifetime_ ব্যবহার করতে হয়—Rust-এর এমন একটি feature যেটা আমরা Chapter 10-এ আলোচনা করব। Lifetime নিশ্চিত করে যে struct যে data-কে reference করে তা ততক্ষণ valid থাকবে যতক্ষণ struct নিজে valid থাকে। ধরো তুমি lifetime উল্লেখ না করেই কোনো struct-এ reference সংরক্ষণ করতে চাইলে, *src/main.rs*-এ নিচের মতো লিখলে; এটা কাজ করবে না:
>
> <Listing file-name="src/main.rs">
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore,does_not_compile
> struct User {
>     active: bool,
>     username: &str,
>     email: &str,
>     sign_in_count: u64,
> }
>
> fn main() {
>     let user1 = User {
>         active: true,
>         username: "someusername123",
>         email: "someone@example.com",
>         sign_in_count: 1,
>     };
> }
> ```
>
> </Listing>
>
> Compiler অভিযোগ করবে যে এটি lifetime specifier চায়:
>
> ```console
> $ cargo run
>    Compiling structs v0.1.0 (file:///projects/structs)
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:3:15
>   |
> 3 |     username: &str,
>   |               ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 ~     username: &'a str,
>   |
>
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:4:12
>   |
> 4 |     email: &str,
>   |            ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 |     username: &str,
> 4 ~     email: &'a str,
>   |
>
> For more information about this error, try `rustc --explain E0106`.
> error: could not compile `structs` (bin "structs") due to 2 previous errors
> ```
>
> Chapter 10-এ আমরা আলোচনা করব কীভাবে এই error-গুলো ঠিক করতে হয় যাতে struct-এ reference সংরক্ষণ করা যায়, কিন্তু আপাতত আমরা `&str`-এর মতো reference-এর বদলে `String`-এর মতো owned type ব্যবহার করে এ ধরনের error এড়াব।

<!-- manual-regeneration
for the error above
after running update-rustc.sh:
pbcopy < listings/ch05-using-structs-to-structure-related-data/no-listing-02-reference-in-struct/output.txt
paste above
add `> ` before every line -->

[tuples]: ch03-02-data-types.html#the-tuple-type
[move]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-move
[copy]: ch04-01-what-is-ownership.html#stack-only-data-copy

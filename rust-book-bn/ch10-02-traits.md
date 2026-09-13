<!-- Old headings. Do not remove or links may break. -->

<a id="traits-defining-shared-behavior"></a>

## Traits দিয়ে Shared Behavior Define করা

একটি _trait_ কোনো নির্দিষ্ট type-এর functionality define করে যা সে অন্যান্য type-এর সাথে share করতে পারে। আমরা traits ব্যবহার করে বিমূর্তভাবে shared behavior define করতে পারি। আমরা _trait bounds_ ব্যবহার করে specify করতে পারি যে কোনো generic type এমন যেকোনো type হতে পারে যার নির্দিষ্ট behavior আছে।

> নোট: Traits অন্যান্য language-এ প্রায়শই _interfaces_ নামে পরিচিত একটি feature-এর অনুরূপ, যদিও কিছু পার্থক্য আছে।

### একটি Trait Define করা

একটি type-এর behavior গঠিত হয় সেই method-গুলো দিয়ে যেগুলো আমরা সেই type-এর উপর call করতে পারি। ভিন্ন ভিন্ন type একই behavior share করে যদি আমরা সেই সব type-এর উপর একই method call করতে পারি। Trait definition হলো এমন একটি উপায় যা কোনো একটি উদ্দেশ্য সাধনের জন্য প্রয়োজনীয় behavior-এর একটি set define করতে method signature-গুলোকে একসাথে গ্রুপ করে।

উদাহরণস্বরূপ, ধরো আমাদের একাধিক struct আছে যেগুলো বিভিন্ন ধরনের ও পরিমাণের text ধারণ করে: একটি `NewsArticle` struct যা কোনো এক নির্দিষ্ট location থেকে প্রকাশিত একটি news story ধারণ করে এবং একটি `SocialPost` যা সর্বোচ্চ 280 character ধারণ করতে পারে সাথে metadata যা নির্দেশ করে সেটি নতুন post, repost, নাকি অন্য কোনো post-এর reply।

আমরা একটি media aggregator library crate বানাতে চাই যার নাম `aggregator`, যা `NewsArticle` বা `SocialPost` instance-এ সংরক্ষিত data-র summary দেখাতে পারে। এটি করতে, আমাদের প্রতিটি type থেকে একটি summary প্রয়োজন, এবং আমরা সেই summary একটি instance-এর উপর `summarize` method call করে চাইবো। Listing 10-12 একটি public `Summary` trait-এর definition দেখায় যা এই behavior প্রকাশ করে।

<Listing number="10-12" file-name="src/lib.rs" caption="A `Summary` trait that consists of the behavior provided by a `summarize` method">

```rust,noplayground
pub trait Summary {
    fn summarize(&self) -> String;
}
```

</Listing>

এখানে, আমরা `trait` keyword এবং তারপর trait-এর নাম ব্যবহার করে একটি trait declare করি, যা এই ক্ষেত্রে `Summary`। আমরা trait-টিকে `pub` হিসেবেও declare করি যাতে এই crate-এর উপর নির্ভরশীল crate-গুলোও এই trait ব্যবহার করতে পারে, যেমন আমরা কয়েকটি উদাহরণে দেখবো। Curly bracket-এর ভেতর, আমরা method signature-গুলো declare করি যা এই trait implement করে এমন type-গুলোর behavior বর্ণনা করে, যা এই ক্ষেত্রে `fn summarize(&self) -> String`।

Method signature-এর পরে, curcly bracket-এর ভেতর implementation দেওয়ার বদলে আমরা একটি semicolon ব্যবহার করি। এই trait implement করে এমন প্রতিটি type-কে অবশ্যই method-টির body-এর জন্য নিজস্ব custom behavior দিতে হবে। Compiler enforce করবে যে `Summary` trait আছে এমন যেকোনো type-এ `summarize` method ঠিক এই signature দিয়ে define করা থাকবে।

একটি trait-এর body-এ একাধিক method থাকতে পারে: Method signature-গুলো এক লাইনে একটি করে তালিকাবদ্ধ থাকে, এবং প্রতিটি লাইন শেষ হয় একটি semicolon দিয়ে।

### একটি Type-এর উপর Trait Implement করা

যেহেতু আমরা `Summary` trait-এর method-গুলোর কাঙ্ক্ষিত signature define করেছি, এখন আমরা এটি আমাদের media aggregator-এর type-গুলোর উপর implement করতে পারি। Listing 10-13 দেখায় `NewsArticle` struct-এর উপর `Summary` trait-এর একটি implementation যা `summarize`-এর return value তৈরি করতে headline, author, এবং location ব্যবহার করে। `SocialPost` struct-এর জন্য, আমরা `summarize`-কে এমনভাবে define করি যেন সেটি username-এর পরে post-এর সম্পূর্ণ text দেখায়, এই অনুমানে যে post content ইতিমধ্যে 280 character-এ সীমাবদ্ধ।

<Listing number="10-13" file-name="src/lib.rs" caption="Implementing the `Summary` trait on the `NewsArticle` and `SocialPost` types">

```rust,noplayground
pub struct NewsArticle {
    pub headline: String,
    pub location: String,
    pub author: String,
    pub content: String,
}

impl Summary for NewsArticle {
    fn summarize(&self) -> String {
        format!("{}, by {} ({})", self.headline, self.author, self.location)
    }
}

pub struct SocialPost {
    pub username: String,
    pub content: String,
    pub reply: bool,
    pub repost: bool,
}

impl Summary for SocialPost {
    fn summarize(&self) -> String {
        format!("{}: {}", self.username, self.content)
    }
}
```

</Listing>

কোনো type-এর উপর trait implement করা নিয়মিত method implement করার মতোই। পার্থক্য হলো `impl`-এর পরে আমরা যে trait-টি implement করতে চাই তার নাম রাখি, তারপর `for` keyword ব্যবহার করি, এবং তারপর যে type-এর জন্য trait implement করতে চাই তার নাম specify করি। `impl` block-এর ভেতরে, আমরা trait definition-এ define করা method signature-গুলো রাখি। প্রতিটি signature-এর পরে semicolon যোগ করার বদলে আমরা curly bracket ব্যবহার করি এবং method body-তে সেই specific behavior পূরণ করি যা আমরা চাই trait-টির method-গুলো যেন নির্দিষ্ট type-এর জন্য রাখে।

যেহেতু library-তে `NewsArticle` ও `SocialPost`-এর উপর `Summary` trait implement করা হয়েছে, তাই crate-এর user-রা নিয়মিত method call করার মতোই `NewsArticle` ও `SocialPost`-র instance-এ trait method-গুলো call করতে পারে। শুধুমাত্র পার্থক্য হলো user-কে type-গুলোর পাশাপাশি trait-টিকেও scope-এ আনতে হবে। এখানে একটি উদাহরণ দেওয়া হলো কীভাবে একটি binary crate আমাদের `aggregator` library crate ব্যবহার করতে পারে:

```rust,ignore
use aggregator::{SocialPost, Summary};

fn main() {
    let post = SocialPost {
        username: String::from("horse_ebooks"),
        content: String::from(
            "of course, as you probably already know, people",
        ),
        reply: false,
        repost: false,
    };

    println!("1 new post: {}", post.summarize());
}
```

এই code টি `1 new post: horse_ebooks: of course, as you probably already know, people` print করে।

`aggregator` crate-এর উপর নির্ভরশীল অন্যান্য crate-ও তাদের নিজেদের type-এর উপর `Summary` implement করতে `Summary` trait-কে scope-এ আনতে পারে। একটি গুরুত্বপূর্ণ restriction হলো একটি type-এর উপর trait implement করতে পারবো শুধুমাত্র তখনই যখন trait অথবা type, অথবা উভয়ই, আমাদের crate-এ local। উদাহরণস্বরূপ, আমরা আমাদের `aggregator` crate-এর functionality-র অংশ হিসেবে `SocialPost`-এর মতো custom type-এর উপর `Display`-এর মতো standard library trait implement করতে পারি, কারণ `SocialPost` type-টি আমাদের `aggregator` crate-এ local। আমরা আমাদের `aggregator` crate-এ `Vec<T>`-র উপরও `Summary` implement করতে পারি, কারণ `Summary` trait-টি আমাদের `aggregator` crate-এ local।

কিন্তু আমরা external type-এর উপর external trait implement করতে পারবো না। উদাহরণস্বরূপ, আমরা আমাদের `aggregator` crate-এ `Vec<T>`-র উপর `Display` trait implement করতে পারবো না, কারণ `Display` এবং `Vec<T>` দুটোই standard library-তে define করা এবং আমাদের `aggregator` crate-এ local নয়। এই restriction _coherence_ নামক একটি property-র অংশ, আরও নির্দিষ্টভাবে _orphan rule_, এই নামে কারণ parent type উপস্থিত থাকে না। এই rule নিশ্চিত করে যে অন্য মানুষের code তোমার code ভাঙতে পারবে না এবং এর উল্টোটাও। এই rule না থাকলে, দুটি crate একই type-এর জন্য একই trait implement করতে পারতো, আর Rust বুঝতে পারতো না কোন implementation ব্যবহার করবে।

<!-- Old headings. Do not remove or links may break. -->

<a id="default-implementations"></a>

### Default Implementation ব্যবহার করা

কখনো কখনো একটি trait-এর সব বা কিছু method-এর জন্য default behavior থাকাটা কার্যকর, যেখানে প্রতিটি type-এ সব method-এর implementation দাবি করার বদলে সেই default দেওয়া থাকে। তারপর, যখন আমরা কোনো নির্দিষ্ট type-এ trait implement করি, তখন আমরা প্রতিটি method-এর default behavior রাখতে বা override করতে পারি।

Listing 10-14-তে, আমরা Listing 10-12-তে যেমন শুধু method signature define করেছিলাম তার বদলে `Summary` trait-এর `summarize` method-এর জন্য একটি default string specify করি।

<Listing number="10-14" file-name="src/lib.rs" caption="Defining a `Summary` trait with a default implementation of the `summarize` method">

```rust,noplayground
pub trait Summary {
    fn summarize(&self) -> String {
        String::from("(Read more...)")
    }
}
```

</Listing>

`NewsArticle`-এর instance সারাংশিত করতে default implementation ব্যবহার করতে, আমরা `impl Summary for NewsArticle {}` দিয়ে একটি খালি `impl` block specify করি।

যদিও আমরা আর `NewsArticle`-এ সরাসরি `summarize` method define করছি না, আমরা একটি default implementation দিয়েছি এবং specify করেছি যে `NewsArticle` `Summary` trait implement করে। ফলস্বরূপ, আমরা এখনও একটি `NewsArticle` instance-এর উপর `summarize` method call করতে পারি, এভাবে:

```rust,ignore
    let article = NewsArticle {
        headline: String::from("Penguins win the Stanley Cup Championship!"),
        location: String::from("Pittsburgh, PA, USA"),
        author: String::from("Iceburgh"),
        content: String::from(
            "The Pittsburgh Penguins once again are the best \
             hockey team in the NHL.",
        ),
    };

    println!("New article available! {}", article.summarize());
```

এই code টি `New article available! (Read more...)` print করে।

Default implementation তৈরি করার জন্য Listing 10-13-তে `SocialPost`-এ `Summary`-র implementation সম্পর্কে কিছু পরিবর্তন করতে হয় না। কারণ একটি default implementation কে override করার syntax আর এমন trait method যার default implementation নেই সেটি implement করার syntax একই।

Default implementation-গুলো একই trait-এর অন্যান্য method-কে call করতে পারে, যদিও সেই অন্যান্য method-গুলোর default implementation নাও থাকতে পারে। এইভাবে, একটি trait প্রচুর useful functionality দিতে পারে এবং শুধু implementor-কে তার একটি ছোট অংশ specify করতে বলতে পারে। উদাহরণস্বরূপ, আমরা `Summary` trait-টিকে এমনভাবে define করতে পারি যাতে এর একটি `summarize_author` method থাকে যার implementation প্রয়োজনীয়, এবং তারপর একটি `summarize` method define করি যার default implementation `summarize_author` method-কে call করে:

```rust,noplayground
pub trait Summary {
    fn summarize_author(&self) -> String;

    fn summarize(&self) -> String {
        format!("(Read more from {}...)", self.summarize_author())
    }
}
```

এই version-এর `Summary` ব্যবহার করতে, আমাদের একটি type-এ trait implement করার সময় শুধু `summarize_author` define করলেই হবে:

```rust,ignore
impl Summary for SocialPost {
    fn summarize_author(&self) -> String {
        format!("@{}", self.username)
    }
}
```

`summarize_author` define করার পর, আমরা `SocialPost` struct-এর instance-গুলোর উপর `summarize` call করতে পারি, এবং `summarize`-এর default implementation আমরা যে `summarize_author` definition দিয়েছি তাকে call করবে। যেহেতু আমরা `summarize_author` implement করেছি, তাই `Summary` trait আমাদের আর কোনো code না লিখতে হয়েই `summarize` method-টির behavior দিয়েছে। এটি দেখতে এরকম:

```rust,ignore
    let post = SocialPost {
        username: String::from("horse_ebooks"),
        content: String::from(
            "of course, as you probably already know, people",
        ),
        reply: false,
        repost: false,
    };

    println!("1 new post: {}", post.summarize());
```

এই code টি `1 new post: (Read more from @horse_ebooks...)` print করে।

মনে রেখো, কোনো method-এর overriding implementation থেকে সেই একই method-এর default implementation-কে call করা সম্ভব নয়।

<!-- Old headings. Do not remove or links may break. -->

<a id="traits-as-parameters"></a>

### Traits কে Parameter হিসেবে ব্যবহার করা

এখন যেহেতু তুমি জানো কীভাবে trait define ও implement করতে হয়, আমরা দেখতে পারি কীভাবে traits ব্যবহার করে এমন function define করা যায় যা অনেক ভিন্ন ভিন্ন type গ্রহণ করে। আমরা Listing 10-13-এ `NewsArticle` ও `SocialPost` type-এর উপর যে `Summary` trait implement করেছি তা ব্যবহার করে একটি `notify` function define করবো যা তার `item` parameter-এর উপর `summarize` method call করে, যেখানে `item` এমন কোনো type যা `Summary` trait implement করে। এটি করতে, আমরা `impl Trait` syntax ব্যবহার করি, এভাবে:

```rust,ignore
pub fn notify(item: &impl Summary) {
    println!("Breaking news! {}", item.summarize());
}
```

`item` parameter-এর জন্য কোনো concrete type-এর বদলে, আমরা `impl` keyword এবং trait-এর নাম specify করি। এই parameter এমন যেকোনো type গ্রহণ করে যা specify করা trait implement করে। `notify`-এর body-তে, আমরা `item`-এর উপর এমন যেকোনো method call করতে পারি যা `Summary` trait থেকে এসেছে, যেমন `summarize`। আমরা `notify` call করে `NewsArticle` বা `SocialPost`-র যেকোনো instance পাস করতে পারি। অন্য কোনো type, যেমন `String` বা `i32` দিয়ে function-টি call করলে সেটি compile হবে না, কারণ সেই type-গুলো `Summary` implement করে না।

<!-- Old headings. Do not remove or links may break. -->

<a id="fixing-the-largest-function-with-trait-bounds"></a>

#### Trait Bound Syntax

`impl Trait` syntax সরল ক্ষেত্রে কাজ করে কিন্তু আসলে এটি _trait bound_ নামে পরিচিত একটি দীর্ঘতর রূপের syntax sugar; সেটি দেখতে এমন:

```rust,ignore
pub fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}
```

এই দীর্ঘতর রূপটি আগের section-এর উদাহরণের সমতুল্য কিন্তু বেশি verbose। আমরা generic type parameter-এর declaration-এর পরে একটি colon এবং angle bracket-এর ভেতর trait bound স্থাপন করি।

`impl Trait` syntax সুবিধাজনক এবং সহজ ক্ষেত্রে আরও concise code তৈরি করে, অন্যদিকে পূর্ণ trait bound syntax অন্যান্য ক্ষেত্রে আরও বেশি complexity প্রকাশ করতে পারে। উদাহরণস্বরূপ, আমরা দুটি parameter রাখতে পারি যাদের উভয়ই `Summary` implement করে। `impl Trait` syntax দিয়ে এটি করলে দেখতে এমন:

```rust,ignore
pub fn notify(item1: &impl Summary, item2: &impl Summary) {
```

যদি আমরা চাই এই function-টি `item1` ও `item2`-কে ভিন্ন type হতে দিক (যতক্ষণ না উভয় typeই `Summary` implement করে), তখন `impl Trait` ব্যবহার করা উপযুক্ত। কিন্তু যদি আমরা উভয় parameter-কে একই type হতে বাধ্য করতে চাই, তখন আমাদের অবশ্যই একটি trait bound ব্যবহার করতে হবে, এভাবে:

```rust,ignore
pub fn notify<T: Summary>(item1: &T, item2: &T) {
```

`item1` ও `item2` parameter-এর type হিসেবে specify করা generic type `T` function-টিকে এমনভাবে constrain করে যে `item1` ও `item2`-এর জন্য argument হিসেবে পাস করা value-র concrete type অবশ্যই একই হতে হবে।

<!-- Old headings. Do not remove or links may break. -->

<a id="specifying-multiple-trait-bounds-with-the--syntax"></a>

#### `+` Syntax দিয়ে একাধিক Trait Bound

আমরা একাধিক trait bound-ও specify করতে পারি। বলো আমরা চাই `notify`-তে `summarize`-এর পাশাপাশি `item`-এর উপর display formatting-ও ব্যবহার করতে: আমরা `notify` definition-এ specify করি যে `item`-কে অবশ্যই `Display` এবং `Summary` উভয় trait-ই implement করতে হবে। আমরা `+` syntax ব্যবহার করে এটি করতে পারি:

```rust,ignore
pub fn notify(item: &(impl Summary + Display)) {
```

`+` syntax এছাড়াও generic type-এর উপর trait bound-এর সাথেও valid:

```rust,ignore
pub fn notify<T: Summary + Display>(item: &T) {
```

দুটি trait bound specify করার সাথে সাথে, `notify`-এর body এখন `summarize` call করতে পারবে এবং `item`-কে format করতে `{}` ব্যবহার করতে পারবে।

#### `where` Clause দিয়ে আরও পরিষ্কার Trait Bound

অনেক বেশি trait bound ব্যবহার করার নেতিবাচক দিক আছে। প্রতিটি generic-এর নিজস্ব trait bound আছে, তাই একাধিক generic type parameter সহ function-এ function-এর নাম এবং তার parameter list-এর মাঝে প্রচুর trait bound তথ্য থাকতে পারে, যা function signature-কে পড়তে কঠিন করে তোলে। এই কারণে, Rust-এ function signature-এর পরে একটি `where` clause-এর ভেতরে trait bound specify করার জন্য alternate syntax আছে। তাই, এটি না লিখে:

```rust,ignore
fn some_function<T: Display + Clone, U: Clone + Debug>(t: &T, u: &U) -> i32 {
```

আমরা একটি `where` clause ব্যবহার করতে পারি, এভাবে:

```rust,ignore
fn some_function<T, U>(t: &T, u: &U) -> i32
where
    T: Display + Clone,
    U: Clone + Debug,
{
```

এই function-এর signature কম cluttered: Function-এর নাম, parameter list, এবং return type একসাথে আছে, ঠিক যেমন একটি সাধারণ অনেক trait bound ছাড়া function-এ থাকে।

### Trait Implement করে এমন Type Return করা

আমরা `impl Trait` syntax-কে return position-এও ব্যবহার করতে পারি যাতে কোনো এক trait implement করে এমন কোনো type-এর value return করা যায়, যেমন এখানে দেখানো হয়েছে:

```rust,ignore
fn returns_summarizable() -> impl Summary {
    SocialPost {
        username: String::from("horse_ebooks"),
        content: String::from(
            "of course, as you probably already know, people",
        ),
        reply: false,
        repost: false,
    }
}
```

Return type-এর জন্য `impl Summary` ব্যবহার করে, আমরা specify করি যে `returns_summarizable` function এমন কোনো type return করে যা `Summary` trait implement করে, কোনো concrete type-এর নাম না দিয়েই। এই ক্ষেত্রে, `returns_summarizable` একটি `SocialPost` return করে, কিন্তু এই function-টি call করা code-এর সেটি জানার প্রয়োজন নেই।

শুধুমাত্র সেই trait দিয়েই return type specify করার ক্ষমতা closure এবং iterator-এর context-এ বিশেষভাবে useful, যা আমরা Chapter 13-এ cover করবো। Closure এবং iterator এমন type তৈরি করে যা শুধু compiler জানে অথবা যা specify করতে খুব দীর্ঘ। `impl Trait` syntax তোমাকে সংক্ষেপে specify করতে দেয় যে একটি function এমন কোনো type return করে যা `Iterator` trait implement করে, একটি খুব দীর্ঘ type লেখার প্রয়োজন না হয়েই।

তবে, তুমি শুধুমাত্র তখনই `impl Trait` ব্যবহার করতে পারবে যখন তুমি একটি single type return করছো। উদাহরণস্বরূপ, এই code টি যেটি `impl Summary` হিসেবে return type specify করে এবং একটি `NewsArticle` অথবা `SocialPost` return করে, সেটি কাজ করবে না:

```rust,ignore,does_not_compile
fn returns_summarizable(switch: bool) -> impl Summary {
    if switch {
        NewsArticle {
            headline: String::from(
                "Penguins win the Stanley Cup Championship!",
            ),
            location: String::from("Pittsburgh, PA, USA"),
            author: String::from("Iceburgh"),
            content: String::from(
                "The Pittsburgh Penguins once again are the best \
                 hockey team in the NHL.",
            ),
        }
    } else {
        SocialPost {
            username: String::from("horse_ebooks"),
            content: String::from(
                "of course, as you probably already know, people",
            ),
            reply: false,
            repost: false,
        }
    }
}
```

একটি `NewsArticle` অথবা `SocialPost` return করা allowed নয়, কারণ `impl Trait` syntax compiler-এ কীভাবে implement করা হয়েছে তার উপর নির্ভর করে কিছু restriction আছে। আমরা Chapter 18-এর [“Using Trait Objects to Abstract over Shared Behavior”][trait-objects]<!-- ignore --> section-এ এই behavior সহ কীভাবে function লিখতে হয় তা cover করবো।

### Trait Bound দিয়ে Conditional Method Implementation

Generic type parameter ব্যবহার করে একটি `impl` block-এর সাথে trait bound ব্যবহার করে, আমরা যেসব type specify করা trait implement করে সেগুলোর জন্য conditionally method implement করতে পারি। উদাহরণস্বরূপ, Listing 10-15-তে `Pair<T>` type সবসময় `new` function implement করে যা `Pair<T>`-র একটি নতুন instance return করে (Chapter 5-এর [“Method Syntax”][methods]<!-- ignore --> section থেকে মনে করো যে `Self` হলো `impl` block-এর type-এর একটি type alias, যা এই ক্ষেত্রে `Pair<T>`)। কিন্তু পরের `impl` block-এ, `Pair<T>` শুধুমাত্র তখনই `cmp_display` method implement করে যখন এর ভেতরের type `T` comparison enable করে এমন `PartialOrd` trait _এবং_ printing enable করে এমন `Display` trait implement করে।

<Listing number="10-15" file-name="src/lib.rs" caption="Conditionally implementing methods on a generic type depending on trait bounds">

```rust,noplayground
use std::fmt::Display;

struct Pair<T> {
    x: T,
    y: T,
}

impl<T> Pair<T> {
    fn new(x: T, y: T) -> Self {
        Self { x, y }
    }
}

impl<T: Display + PartialOrd> Pair<T> {
    fn cmp_display(&self) {
        if self.x >= self.y {
            println!("The largest member is x = {}", self.x);
        } else {
            println!("The largest member is y = {}", self.y);
        }
    }
}
```

</Listing>

আমরা এছাড়াও অন্য কোনো trait implement করে এমন যেকোনো type-এর জন্য conditionally একটি trait implement করতে পারি। trait bound পূরণ করে এমন যেকোনো type-এ একটি trait-এর implementation-কে _blanket implementation_ বলা হয় এবং এটি Rust standard library-তে ব্যাপকভাবে ব্যবহৃত হয়। উদাহরণস্বরূপ, standard library যেকোনো type-এ যা `Display` trait implement করে তার উপর `ToString` trait implement করে। Standard library-তে `impl` block-টি এই code-এর মতো:

```rust,ignore
impl<T: Display> ToString for T {
    // --snip--
}
```

যেহেতু standard library-তে এই blanket implementation আছে, তাই আমরা `Display` trait implement করে এমন যেকোনো type-এর উপর `ToString` trait দ্বারা define করা `to_string` method call করতে পারি। উদাহরণস্বরূপ, আমরা পূর্ণসংখ্যাকে তার সংশ্লিষ্ট `String` value-তে এভাবে রূপান্তর করতে পারি কারণ পূর্ণসংখ্যা `Display` implement করে:

```rust
let s = 3.to_string();
```

Blanket implementation-গুলো trait-এর documentation-এ “Implementors” section-এ দেখা যায়।

Trait এবং trait bound আমাদের code duplication কমাতে generic type parameter ব্যবহার করে code লেখার সুযোগ দেয়, কিন্তু আবার compiler-কেও specify করে যে আমরা চাই generic type-এর নির্দিষ্ট behavior থাকুক। Compiler তারপর trait bound তথ্য ব্যবহার করে check করতে পারে যে আমাদের code-এর সাথে ব্যবহৃত সব concrete type সঠিক behavior দেয় কিনা। Dynamically typed language-এ, আমরা এমন কোনো type-এর উপর method call করলে যে type সেই method define করে না, তখন runtime-এ error পেতাম। কিন্তু Rust সেই error-গুলোকে compile time-এ নিয়ে আসে, যাতে আমাদের code চালানোর আগেই সমস্যাগুলো ঠিক করতে বাধ্য করে। এছাড়াও, আমাদের runtime-এ behavior check করে এমন code লেখার দরকার নেই, কারণ আমরা ইতিমধ্যে compile time-এ check করে নিয়েছি। এটি করলে generics-এর flexibility ছাড়াই performance উন্নত হয়।

[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[methods]: ch05-03-method-syntax.html#method-syntax

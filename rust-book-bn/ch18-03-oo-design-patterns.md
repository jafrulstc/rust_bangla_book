## Object-Oriented Design Pattern Implement করা

_State pattern_ হলো একটি object-oriented design pattern। এই pattern-এর মূল কথা হলো—আমরা এমন কিছু state define করি যেগুলো একটি value ভেতরে ভেতরে ধারণ করতে পারে। state গুলো _state object_ নামের একটি সেট দিয়ে represent করা হয়, এবং value-র behavior তার state-এর ওপর ভিত্তি করে বদলায়। আমরা একটি blog post struct-এর উদাহরণ ধাপে ধাপে দেখবো, যার একটি field তার state ধরে রাখবে—যে state object টি "draft," "review," অথবা "published" সেট থেকে আসবে।

State object গুলো functionality ভাগ করে নেয়: Rust-এ অবশ্যই আমরা object এবং inheritance-এর বদলে struct এবং trait ব্যবহার করি। প্রতিটি state object নিজের behavior-এর জন্য এবং কখন সে অন্য state-এ পরিবর্তিত হবে তা নিয়ন্ত্রণের জন্য দায়ী। যে value state object ধরে রাখে সে state-গুলোর ভিন্ন behavior সম্পর্কে বা কখন state-এর মধ্যে transition হবে সে সম্পর্কে কিছুই জানে না।

State pattern ব্যবহারের সুবিধা হলো—program-এর business requirement পরিবর্তিত হলে আমাদের state ধরে রাখা value-র code বা সেই value ব্যবহার করা code পরিবর্তন করতে হবে না। আমাদের শুধু state object-গুলোর একটির ভেতরের code update করতে হবে তার নিয়ম পরিবর্তন করতে, অথবা হয়তো আরও কিছু state object যোগ করতে হবে।

প্রথমে আমরা state pattern-টিকে অপেক্ষাকৃত traditional object-oriented পদ্ধতিতে implement করবো। এরপর এমন একটি approach ব্যবহার করবো যা Rust-এ বেশি natural। চলো state pattern ব্যবহার করে incrementally একটি blog post workflow implement করি।

শেষে functionality-টি এমন দেখাবে:

1. একটি blog post খালি draft হিসেবে শুরু হয়।
1. Draft শেষ হলে post-এর review request করা হয়।
1. Post approve হলে তা publish হয়।
1. শুধুমাত্র published blog post গুলো print করার জন্য content return করবে, যাতে unapproved post ভুলে প্রকাশিত না হয়ে যায়।

Post-এর ওপর করা অন্য কোনো change-এর কোনো প্রভাব থাকা উচিত নয়। যেমন, review request করার আগেই যদি আমরা একটি draft blog post approve করার চেষ্টা করি, তাহলে post-টি unpublished draft-ই থাকবে।

<!-- Old headings. Do not remove or links may break. -->

<a id="a-traditional-object-oriented-attempt"></a>

### Traditional Object-Oriented Style-এ চেষ্টা করা

একই সমস্যা সমাধানের জন্য code structure করার অসংখ্য উপায় আছে, প্রতিটির ভিন্ন trade-off আছে। এই section-এর implementation টি অপেক্ষাকৃত traditional object-oriented style-এর, যেটি Rust-এ লেখা সম্ভব, কিন্তু কিছু ক্ষেত্রে Rust-এর শক্তি কাজে লাগায় না। পরে আমরা একটি ভিন্ন সমাধান দেখাবো যা এখনও object-oriented design pattern ব্যবহার করে কিন্তু এমনভাবে structure করা যা object-oriented অভিজ্ঞতা সম্পন্ন programmer-দের কাছে কম পরিচিত মনে হতে পারে। আমরা দুটি সমাধান তুলনা করবো যাতে অন্য ভাষার code থেকে আলাদাভাবে Rust code design করার trade-off বোঝা যায়।

Listing 18-11 এই workflow-কে code আকারে দেখায়: এটি `blog` নামের একটি library crate-এ আমরা যে API implement করবো তার ব্যবহারের একটি উদাহরণ। এটি এখনও compile হবে না কারণ আমরা এখনও `blog` crate implement করিনি।

<Listing number="18-11" file-name="src/main.rs" caption="Code যা আমাদের `blog` crate-এর কাছে কাঙ্ক্ষিত behavior প্রদর্শন করে">

```rust,ignore,does_not_compile
use blog::Post;

fn main() {
    let mut post = Post::new();

    post.add_text("I ate a salad for lunch today");
    assert_eq!("", post.content());

    post.request_review();
    assert_eq!("", post.content());

    post.approve();
    assert_eq!("I ate a salad for lunch today", post.content());
}
```

</Listing>

আমরা চাই user `Post::new` দিয়ে একটি নতুন draft blog post তৈরি করতে পারে। আমরা চাই blog post-এ text যোগ করা যায়। যদি approve হওয়ার আগেই আমরা post-এর content পেতে চাই, তবে আমাদের কোনো text পাওয়া উচিত নয়, কারণ post-টি তখনও draft। প্রদর্শনের জন্য আমরা code-এ `assert_eq!` যোগ করেছি। এর জন্য একটি চমৎকার unit test হতো—draft blog post-টি `content` method থেকে empty string return করে কিনা তা assert করা, কিন্তু আমরা এই উদাহরণে test লিখবো না।

এরপর আমরা চাই post-টির review request করার সুযোগ থাকুক, এবং review-এর অপেক্ষায় থাকা অবস্থায় `content` empty string return করুক। যখন post approve হবে তখন তা publish হবে, অর্থাৎ `content` call করলে post-এর text return করবে।

লক্ষ্য করো যে crate থেকে আমরা যে type-টি ব্যবহার করছি সেটি হলো `Post`। এই type-টি state pattern ব্যবহার করবে এবং এমন একটি value ধরে রাখবে যা তিনটি state object-এর একটি—যা একটি post-এর বিভিন্ন state (draft, review, বা published) represent করে। এক state থেকে অন্য state-এ পরিবর্তন `Post` type-এর ভেতরেই internally manage হবে। আমাদের library-র user-রা `Post` instance-এর ওপর যে method গুলো call করবে তার সাড়ায় state গুলো বদলাবে, কিন্তু তাদের state change সরাসরি manage করতে হবে না। তাছাড়া user-রা state নিয়ে ভুল করতে পারবে না, যেমন review হওয়ার আগেই post publish করা।

<!-- Old headings. Do not remove or links may break. -->

<a id="defining-post-and-creating-a-new-instance-in-the-draft-state"></a>

#### `Post` Define করা এবং নতুন Instance তৈরি করা

চলো library-র implementation শুরু করি! আমরা জানি যে একটি public `Post` struct দরকার যা কিছু content ধরে রাখবে, তাই আমরা struct-এর definition এবং `Post`-এর একটি instance তৈরি করার জন্য একটি associated public `new` function দিয়ে শুরু করবো, যেমন Listing 18-12-তে দেখানো হয়েছে। আমরা একটি private `State` trait-ও বানাবো যা `Post`-এর জন্য সব state object-এর থাকা আবশ্যক behavior define করবে।

তারপর `Post` একটি private `state` নামের field-এ `Option<T>`-এর ভেতরে `Box<dyn State>` trait object ধরে রাখবে যা state object টিকে hold করবে। কেন `Option<T>` জরুরি তা তুমি একটু পরেই বুঝবে।

<Listing number="18-12" file-name="src/lib.rs" caption="একটি `Post` struct ও নতুন `Post` instance তৈরি করার একটি `new` function, একটি `State` trait, এবং একটি `Draft` struct-এর definition">

```rust,noplayground
pub struct Post {
    state: Option<Box<dyn State>>,
    content: String,
}

impl Post {
    pub fn new() -> Post {
        Post {
            state: Some(Box::new(Draft {})),
            content: String::new(),
        }
    }
}

trait State {}

struct Draft {}

impl State for Draft {}
```

</Listing>

`State` trait-টি বিভিন্ন post state-এর ভাগ করে নেওয়া behavior define করে। state object গুলো হলো `Draft`, `PendingReview` এবং `Published`, এবং সবাই `State` trait implement করবে। আপাতত trait-টির কোনো method নেই, এবং আমরা শুধু `Draft` state define করে শুরু করবো কারণ আমরা চাই একটি post শুরু হয় এই state-এ।

যখন আমরা একটি নতুন `Post` তৈরি করি, তখন আমরা তার `state` field-কে একটি `Some` value-তে set করি যা একটি `Box` ধরে রাখে। এই `Box` একটি নতুন `Draft` struct instance-কে point করে। এতে নিশ্চিত হয় যে আমরা যখনই নতুন `Post` instance তৈরি করবো সেটি draft হিসেবে শুরু হবে। যেহেতু `Post`-এর `state` field-টি private, তাই অন্য কোনো state-এ কোনো `Post` তৈরি করার উপায় নেই! `Post::new` function-এ আমরা `content` field-টিকে একটি নতুন, empty `String`-এ set করি।

#### Post Content-এর Text Store করা

Listing 18-11-তে আমরা দেখেছি যে আমরা `add_text` নামের একটি method call করতে চাই এবং সেটিতে একটি `&str` পাস করবো যা তারপর blog post-এর text content হিসেবে যোগ হবে। আমরা এটি একটি method হিসেবে implement করছি, `content` field-কে `pub` হিসেবে expose না করে, যাতে পরে আমরা এমন একটি method implement করতে পারি যা `content` field-এর data কীভাবে পড়া হবে তা নিয়ন্ত্রণ করবে। `add_text` method-টি বেশ সোজা, তাই চলো Listing 18-13-এর implementation-টি `impl Post` block-এ যোগ করি।

<Listing number="18-13" file-name="src/lib.rs" caption="`add_text` method implement করা যা post-এর `content`-এ text যোগ করে">

```rust,noplayground
impl Post {
    // --snip--
    pub fn add_text(&mut self, text: &str) {
        self.content.push_str(text);
    }
}
```

</Listing>

`add_text` method টি `self`-এর একটি mutable reference নেয় কারণ আমরা যে `Post` instance-এর ওপর `add_text` call করছি সেটি পরিবর্তন করছি। তারপর আমরা `content`-এর `String`-এর ওপর `push_str` call করি এবং save করা `content`-এ যোগ করার জন্য `text` argument-টি পাস করি। এই behavior post-টি যে state-এ আছে তার ওপর নির্ভর করে না, তাই এটি state pattern-এর অংশ নয়। `add_text` method কোনোভাবেই `state` field-এর সাথে ইন্টারঅ্যাক্ট করে না, কিন্তু এটি আমরা যে behavior support করতে চাই তার অংশ।

<!-- Old headings. Do not remove or links may break. -->

<a id="ensuring-the-content-of-a-draft-post-is-empty"></a>

#### নিশ্চিত করা যে Draft Post-এর Content খালি

`add_text` call করে আমাদের post-এ কিছু content যোগ করার পরও আমরা চাই `content` method empty string slice return করুক, কারণ post-টি তখনও draft state-এ আছে, যেমনটা Listing 18-11-এর প্রথম `assert_eq!` দেখায়। আপাতত আমরা `content` method-টিকে সবচেয়ে সহজ যেভাবে এই requirement পূরণ করবে সেভাবে implement করবো: সব সময় empty string slice return করা। পরে আমরা post-এর state পরিবর্তন করে তাকে publish করার সক্ষমতা যোগ করার পর এটি বদলাবো। এখন পর্যন্ত post গুলো শুধু draft state-এই থাকতে পারে, তাই post content সব সময় খালি হওয়া উচিত। Listing 18-14 এই placeholder implementation দেখায়।

<Listing number="18-14" file-name="src/lib.rs" caption="`Post`-এর ওপর `content` method-এর জন্য একটি placeholder implementation যোগ করা যা সব সময় empty string slice return করে">

```rust,noplayground
impl Post {
    // --snip--
    pub fn content(&self) -> &str {
        ""
    }
}
```

</Listing>

এই `content` method যোগ করায় Listing 18-11-এর প্রথম `assert_eq!` পর্যন্ত সব কিছু ঠিকমতো কাজ করে।

<!-- Old headings. Do not remove or links may break. -->

<a id="requesting-a-review-of-the-post-changes-its-state"></a>
<a id="requesting-a-review-changes-the-posts-state"></a>

#### Review Request করা, যা Post-এর State পরিবর্তন করে

এরপর আমাদের post-এর জন্য review request করার functionality যোগ করতে হবে, যা তার state `Draft` থেকে `PendingReview`-এ পরিবর্তন করবে। Listing 18-15 এই code দেখায়।

<Listing number="18-15" file-name="src/lib.rs" caption="`Post` এবং `State` trait-এর ওপর `request_review` method implement করা">

```rust,noplayground
impl Post {
    // --snip--
    pub fn request_review(&mut self) {
        if let Some(s) = self.state.take() {
            self.state = Some(s.request_review())
        }
    }
}

trait State {
    fn request_review(self: Box<Self>) -> Box<dyn State>;
}

struct Draft {}

impl State for Draft {
    fn request_review(self: Box<Self>) -> Box<dyn State> {
        Box::new(PendingReview {})
    }
}

struct PendingReview {}

impl State for PendingReview {
    fn request_review(self: Box<Self>) -> Box<dyn State> {
        self
    }
}
```

</Listing>

আমরা `Post`-কে একটি public `request_review` method দিচ্ছি যা `self`-এর একটি mutable reference নেবে। তারপর আমরা `Post`-এর বর্তমান state-এর ওপর একটি internal `request_review` method call করি, এবং এই দ্বিতীয় `request_review` method বর্তমান state-কে consume করে নতুন state return করে।

আমরা `State` trait-এ `request_review` method যোগ করি; এখন trait-টি implement করা সব type-কে `request_review` method implement করতে হবে। মনে রাখো, method-এর প্রথম parameter হিসেবে `self`, `&self` বা `&mut self` না থেকে আমরা `self: Box<Self>` ব্যবহার করেছি। এই syntax-এর মানে হলো—method-টি শুধুমাত্র তখনই valid যখন সেটি type-টিকে ধরে রাখা একটি `Box`-এর ওপর call করা হয়। এই syntax `Box<Self>`-এর ownership নেয়, পুরোনো state-টিকে invalidate করে, যাতে `Post`-এর state value একটি নতুন state-এ রূপান্তরিত হতে পারে।

পুরোনো state-কে consume করতে `request_review` method-কে state value-র ownership নিতে হবে। এখানেই `Post`-এর `state` field-এ `Option` থাকা কাজে লাগে: আমরা `take` method call করে `state` field থেকে `Some` value-টি বের করে আনি এবং তার জায়গায় একটি `None` রেখে দিই, কারণ Rust struct-এ unpopulated field রাখতে দেয় না। এতে আমরা `state` value-কে `Post` থেকে borrow না করে move করতে পারি। তারপর আমরা post-এর `state` value-টিকে এই operation-এর ফলাফলে set করবো।

`state`-কে সরাসরি `self.state = self.state.request_review();` code-এর মতো করে set না করে সাময়িকভাবে `None` set করতে হয়, কারণ `state` value-র ownership পেতে হবে। এতে নিশ্চিত হয় যে নতুন state-ে রূপান্তরের পর `Post` পুরোনো `state` value ব্যবহার করতে পারবে না।

`Draft`-এর `request_review` method একটি নতুন, boxed instance of `PendingReview` struct return করে, যা এমন state-কে represent করে যখন একটি post review-এর অপেক্ষায় থাকে। `PendingReview` struct-ও `request_review` method implement করে কিন্তু কোনো transformation করে না। বরং সে নিজেই return করে, কারণ যখন একটি post ইতিমধ্যেই `PendingReview` state-এ থাকে তখন তার ওপর review request করা হলে সেটি `PendingReview` state-েই থাকা উচিত।

এখন আমরা state pattern-এর সুবিধা দেখতে পাচ্ছি: `Post`-এর `request_review` method `state` value যেমনই হোক না কেন একই থাকে। প্রতিটি state নিজের নিয়মের জন্য দায়ী।

`Post`-এর `content` method-টি যেমন আছে তেমনই রেখে দেবো, empty string slice return করবে। এখন আমাদের `Post` `Draft` state ছাড়াও `PendingReview` state-এ থাকতে পারবে, কিন্তু আমরা `PendingReview` state-এও একই behavior চাই। Listing 18-11 এখন দ্বিতীয় `assert_eq!` call পর্যন্ত কাজ করে!

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-the-approve-method-that-changes-the-behavior-of-content"></a>
<a id="adding-approve-to-change-the-behavior-of-content"></a>

#### `content`-এর Behavior পরিবর্তন করতে `approve` যোগ করা

`approve` method-টি `request_review` method-এর মতোই হবে: এটি `state`-কে সেই value-তে set করবে যা বর্তমান state অনুযায়ী approve করা হলে থাকা উচিত, যেমন Listing 18-16 দেখায়।

<Listing number="18-16" file-name="src/lib.rs" caption="`Post` এবং `State` trait-এর ওপর `approve` method implement করা">

```rust,noplayground
impl Post {
    // --snip--
    pub fn approve(&mut self) {
        if let Some(s) = self.state.take() {
            self.state = Some(s.approve())
        }
    }
}

trait State {
    fn request_review(self: Box<Self>) -> Box<dyn State>;
    fn approve(self: Box<Self>) -> Box<dyn State>;
}

struct Draft {}

impl State for Draft {
    // --snip--
    fn approve(self: Box<Self>) -> Box<dyn State> {
        self
    }
}

struct PendingReview {}

impl State for PendingReview {
    // --snip--
    fn approve(self: Box<Self>) -> Box<dyn State> {
        Box::new(Published {})
    }
}

struct Published {}

impl State for Published {
    fn request_review(self: Box<Self>) -> Box<dyn State> {
        self
    }

    fn approve(self: Box<Self>) -> Box<dyn State> {
        self
    }
}
```

</Listing>

আমরা `State` trait-এ `approve` method যোগ করি এবং `State` implement করা একটি নতুন struct যোগ করি—`Published` state।

`PendingReview`-এর `request_review` যেভাবে কাজ করে তার মতোই, যদি আমরা `Draft`-এর ওপর `approve` method call করি, তবে এর কোনো প্রভাব হবে না কারণ `approve` `self` return করবে। যখন আমরা `PendingReview`-এর ওপর `approve` call করি, তখন সে `Published` struct-এর একটি নতুন, boxed instance return করে। `Published` struct `State` trait implement করে, এবং `request_review` ও `approve` উভয় method-এর জন্যই নিজেকে return করে, কারণ এই ক্ষেত্রে post-টি `Published` state-েই থাকা উচিত।

এখন `Post`-এর `content` method update করতে হবে। আমরা চাই `content` থেকে return হওয়া value `Post`-এর বর্তমান state-এর ওপর নির্ভর করুক, তাই আমরা `Post`-কে তার `state`-এর ওপর define করা একটি `content` method-কে delegate করাবো, যেমন Listing 18-17 দেখায়।

<Listing number="18-17" file-name="src/lib.rs" caption="`Post`-এর `content` method-কে `State`-এর একটি `content` method-এ delegate করতে update করা">

```rust,ignore,does_not_compile
impl Post {
    // --snip--
    pub fn content(&self) -> &str {
        self.state.as_ref().unwrap().content(self)
    }
    // --snip--
}
```

</Listing>

যেহেতু লক্ষ্য হলো এই সব নিয়ম `State` implement করা struct-গুলোর ভেতরেই রাখা, তাই আমরা `state`-এর value-র ওপর একটি `content` method call করি এবং post instance-টিকে (অর্থাৎ `self`) argument হিসেবে পাস করি। তারপর `state` value-র ওপর `content` method ব্যবহার করে যে value return হয় সেটি return করি।

আমরা `Option`-এর ওপর `as_ref` method call করি কারণ আমরা `Option`-এর ভেতরের value-র ownership না নিয়ে তার একটি reference চাই। যেহেতু `state` একটি `Option<Box<dyn State>>`, তাই `as_ref` call করলে একটি `Option<&Box<dyn State>>` return করে। যদি `as_ref` call না করতাম, তাহলে error পেতাম কারণ function parameter-এর borrowed `&self` থেকে আমরা `state`-কে move করতে পারি না।

তারপর আমরা `unwrap` method call করি, যা আমরা জানি কখনো panic করবে না কারণ আমরা জানি `Post`-এর method গুলো নিশ্চিত করে যে সেসব method শেষ হওয়ার পর `state` সব সময় একটি `Some` value ধারণ করবে। এটি এমন একটি case যা আমরা Chapter 9-এর [“When You Have More Information Than the Compiler”][more-info-than-rustc]<!-- ignore --> section-এ আলোচনা করেছি—যেখানে আমরা জানি যে `None` value কখনোই সম্ভব নয়, যদিও compiler সেটা বুঝতে পারে না।

এই মুহূর্তে যখন আমরা `&Box<dyn State>`-এর ওপর `content` call করি, তখন deref coercion `&` এবং `Box`-এর ওপর কাজ করবে, যাতে `content` method সবশেষে `State` trait implement করা type-টির ওপরই call হয়। এর মানে আমাদের `content`-কে `State` trait definition-এ যোগ করতে হবে, এবং সেখানেই আমরা কোন state আছে তার ওপর ভিত্তি করে কী content return হবে তার logic রাখবো, যেমন Listing 18-18-তে দেখানো হয়েছে।

<Listing number="18-18" file-name="src/lib.rs" caption="`State` trait-এ `content` method যোগ করা">

```rust,noplayground
trait State {
    // --snip--
    fn content<'a>(&self, post: &'a Post) -> &'a str {
        ""
    }
}

// --snip--
struct Published {}

impl State for Published {
    // --snip--
    fn content<'a>(&self, post: &'a Post) -> &'a str {
        &post.content
    }
}
```

</Listing>

আমরা `content` method-এর জন্য একটি default implementation যোগ করি যা empty string slice return করে। এর মানে `Draft` এবং `PendingReview` struct-গুলোতে আমাদের `content` implement করতে হবে না। `Published` struct `content` method-কে override করবে এবং `post.content`-এর value return করবে। সুবিধাজনক হলেও, `State`-এর ওপর `content` method থাকা যা `Post`-এর content নির্ধারণ করছে, সেটি `State`-এর দায়িত্ব এবং `Post`-এর দায়িত্বের মধ্যে সীমারেখা ঘোলাটে করছে।

মনে রাখো, এই method-এ আমাদের lifetime annotation দরকার, যেমনটা Chapter 10-এ আলোচনা করেছি। আমরা একটি `post`-এর reference argument হিসেবে নিচ্ছি এবং সেই `post`-এর কোনো অংশের reference return করছি, তাই return হওয়া reference-এর lifetime `post` argument-এর lifetime-এর সাথে সম্পর্কিত।

এবং আমাদের কাজ শেষ—সম্পূর্ণ Listing 18-11 এখন কাজ করে! আমরা blog post workflow-এর নিয়ম অনুসারে state pattern implement করেছি। নিয়ম সম্পর্কিত logic `Post`-এর সর্বত্র ছড়িয়ে না থেকে state object-গুলোর ভেতরেই থাকে।

> ### Why Not An Enum?
>
> তুমি হয়তো ভাবছো কেন আমরা বিভিন্ন সম্ভাব্য post state-গুলোকে variant হিসেবে রেখে একটি enum ব্যবহার করলাম না। সেটিও অবশ্যই একটি সম্ভাব্য সমাধান; চেষ্টা করে দেখো এবং শেষ ফলাফল তুলনা করো কোনটা তোমার বেশি পছন্দ হয়! Enum ব্যবহারের একটি অসুবিধা হলো—enum-এর value যেখানে যেখানে check করা হবে, সেখানে প্রতিটি সম্ভাব্য variant handle করার জন্য একটি `match` expression বা অনুরূপ কিছু লাগবে। এটি এই trait object সমাধানের তুলনায় বেশি repetitive হতে পারে।

<!-- Old headings. Do not remove or links may break. -->

<a id="trade-offs-of-the-state-pattern"></a>

#### State Pattern মূল্যায়ন করা

আমরা দেখিয়েছি যে Rust object-oriented state pattern implement করতে সক্ষম, যাতে একটি post-এর প্রতিটি state-এ যেমন behavior থাকা উচিত তা encapsulate করা যায়। `Post`-এর method গুলো বিভিন্ন behavior সম্পর্কে কিছুই জানে না। আমরা যেভাবে code organize করেছি তার ফলে একটি published post যেসব ভাবে behave করতে পারে তা জানতে আমাদের মাত্র এক জায়গায় তাকাতে হবে: `Published` struct-এর ওপর `State` trait-এর implementation।

যদি আমরা state pattern ব্যবহার না করে এমন একটি alternative implementation বানাতাম, তাহলে হয়তো `Post`-এর method গুলোতে বা এমনকি `main` code-এ `match` expression ব্যবহার করতাম যা post-এর state check করে সেই জায়গাগুলোতে behavior পরিবর্তন করতো। তার মানে একটি post published state-এ থাকার সব প্রভাব বুঝতে আমাদের কয়েক জায়গায় তাকাতে হতো।

State pattern ব্যবহার করলে `Post` method গুলো এবং আমরা যেখানে `Post` ব্যবহার করি সেখানে `match` expression লাগে না, এবং নতুন state যোগ করতে হলে আমাদের শুধু এক জায়গায় একটি নতুন struct যোগ করে সেই struct-এর ওপর trait method implement করতে হবে।

State pattern ব্যবহার করা implementation কে আরও functionality যোগ করতে expand করা সহজ। state pattern ব্যবহার করা code maintain করার সরলতা দেখতে নিচের কয়েকটি পরামর্শ চেষ্টা করে দেখো:

- একটি `reject` method যোগ করো যা post-এর state `PendingReview` থেকে আবার `Draft`-এ পরিবর্তন করবে।
- `Published` state-ে পরিবর্তনের আগে দুবার `approve` call করা আবশ্যক করো।
- user-দের শুধুমাত্র `Draft` state-এ থাকা post-এ text content যোগ করতে দাও। ইঙ্গিত: state object-কে content-এ কী পরিবর্তন হতে পারে তার দায়িত্ব দাও, কিন্তু `Post` modify করার দায়িত্ব দিও না।

State pattern-এর একটি অসুবিধা হলো—যেহেতু state গুলো state-গুলোর মধ্যে transition implement করে, কিছু state একে অপরের সাথে coupled। যদি আমরা `PendingReview` এবং `Published`-এর মধ্যে আরেকটি state যোগ করি, যেমন `Scheduled`, তাহলে আমাদের `PendingReview`-এর code পরিবর্তন করতে হবে যাতে সে `Published`-এর বদলে `Scheduled`-এ transition করে। যদি `PendingReview`-কে নতুন state যোগ করার সাথে পরিবর্তন করতে না হতো, তাহলে কাজ কম হতো, কিন্তু তখন অন্য design pattern-এ চলে যেতে হতো।

আরেকটি অসুবিধা হলো আমরা কিছু logic duplicate করেছি। কিছু duplication দূর করতে আমরা হয়তো `State` trait-এ `request_review` এবং `approve` method-এর জন্য `self` return করা default implementation বানানোর চেষ্টা করতে পারি। তবে এটি কাজ করবে না: `State` কে trait object হিসেবে ব্যবহার করলে trait-টি জানে না concrete `self` ঠিক কী হবে, তাই return type compile time-এ জানা যায় না। (এটি আগে উল্লেখিত dyn compatibility নিয়মগুলোর একটি।)

আরও duplication রয়েছে—`Post`-এর `request_review` এবং `approve` method-গুলোর অনুরূপ implementation। উভয় method-ই `Post`-এর `state` field-এর সাথে `Option::take` ব্যবহার করে, এবং `state` যদি `Some` হয় তবে wrapped value-র একই method-এর implementation-কে delegate করে এবং `state` field-এর নতুন value সেই ফলাফলে set করে। যদি `Post`-এ এই pattern অনুসরণ করা আরও অনেক method থাকতো, তবে আমরা একটি macro define করে repetition দূর করার কথা ভাবতে পারতাম (Chapter 20-এর [“Macros”][macros]<!-- ignore --> section দেখো)।

Object-oriented language-গুলোর জন্য যেভাবে state pattern define করা আছে ঠিক সেভাবে সেটি implement করলে আমরা Rust-এর শক্তির পূর্ণ সুযোগ নিতে পারছি না। চলো দেখি `blog` crate-এ আমরা কী কী পরিবর্তন করতে পারি যাতে invalid state এবং transition-কে compile-time error-এ পরিণত করা যায়।

### State এবং Behavior-কে Type হিসেবে Encode করা

আমরা দেখাবো কীভাবে state pattern-কে নতুন করে ভেবে এক ভিন্ন সেটের trade-off পাওয়া যায়। state এবং transition-কে সম্পূর্ণভাবে encapsulate করে রাখার বদলে যাতে বাইরের code-এর কাছে সেগুলো সম্পর্কে কোনো জ্ঞান না থাকে, আমরা state গুলোকে ভিন্ন ভিন্ন type-এ encode করবো। ফলে Rust-এর type-checking system শুধুমাত্র published post-allowed জায়গায় draft post ব্যবহার করার চেষ্টা করলে compiler error দিয়ে তা আটকে দেবে।

চলো Listing 18-11-এর `main`-এর প্রথম অংশটি বিবেচনা করি:

<Listing file-name="src/main.rs">

```rust,ignore
fn main() {
    let mut post = Post::new();

    post.add_text("I ate a salad for lunch today");
    assert_eq!("", post.content());
}
```

</Listing>

আমরা এখনও `Post::new` দিয়ে draft state-এ নতুন post তৈরির সুযোগ রাখবো এবং post-এর content-এ text যোগ করার সক্ষমতা রাখবো। কিন্তু draft post-এ এমন একটি `content` method থাকার বদলে যা empty string return করে, আমরা এমনভাবে করবো যেন draft post-গুলোর কোনো `content` method-ই না থাকে। এতে যদি আমরা কোনো draft post-এর content পেতে চেষ্টা করি, তবে compiler error পাবো যে method-টি নেই। ফলে production-এ আমরা ভুলে draft post-এর content প্রদর্শন করতে পারবো না, কারণ সেই code-ই compile হবে না। Listing 18-19 একটি `Post` struct এবং একটি `DraftPost` struct-এর definition, এবং প্রতিটির ওপর method দেখায়।

<Listing number="18-19" file-name="src/lib.rs" caption="একটি `Post` যার `content` method আছে, এবং একটি `DraftPost` যার `content` method নেই">

```rust,noplayground
pub struct Post {
    content: String,
}

pub struct DraftPost {
    content: String,
}

impl Post {
    pub fn new() -> DraftPost {
        DraftPost {
            content: String::new(),
        }
    }

    pub fn content(&self) -> &str {
        &self.content
    }
}

impl DraftPost {
    pub fn add_text(&mut self, text: &str) {
        self.content.push_str(text);
    }
}
```

</Listing>

`Post` এবং `DraftPost` উভয় struct-এরই একটি private `content` field আছে যা blog post text store করে। struct-গুলোর আর `state` field নেই কারণ আমরা state-এর encoding struct-গুলোর type-এ সরিয়ে নিচ্ছি। `Post` struct একটি published post-কে represent করবে, এবং তার `content` method আছে যা `content` return করে।

আমাদের এখনও একটি `Post::new` function আছে, কিন্তু সেটি `Post`-এর instance না ফেরত দিয়ে একটি `DraftPost`-এর instance return করে। যেহেতু `content` private এবং `Post` return করা কোনো function নেই, তাই এখন কোনো `Post` instance তৈরি করার উপায় নেই।

`DraftPost` struct-এ একটি `add_text` method আছে, তাই আমরা আগের মতো `content`-এ text যোগ করতে পারি, কিন্তু মনে রাখো `DraftPost`-এ কোনো `content` method define করা নেই! তাই এখন program নিশ্চিত করে যে সব post draft post হিসেবে শুরু হয়, এবং draft post-গুলোর content প্রদর্শনের জন্য available নয়। এই constraint গুলো এড়ানোর কোনো চেষ্টা compiler error করবে।

<!-- Old headings. Do not remove or links may break. -->

<a id="implementing-transitions-as-transformations-into-different-types"></a>

তাহলে, আমরা একটি published post কীভাবে পাবো? আমরা এই নিয়মটি enforce করতে চাই যে একটি draft post publish হওয়ার আগে তাকে review এবং approve হতে হবে। Pending review state-এ থাকা একটি post-এরও কোনো content প্রদর্শন করা উচিত নয়। চলো এই constraint গুলো আরেকটি struct `PendingReviewPost` যোগ করে, `DraftPost`-এর ওপর `request_review` method define করে যা একটি `PendingReviewPost` return করবে এবং `PendingReviewPost`-এর ওপর একটি `approve` method define করে যা একটি `Post` return করবে—implement করি, যেমন Listing 18-20-তে দেখানো হয়েছে।

<Listing number="18-20" file-name="src/lib.rs" caption="একটি `PendingReviewPost` যা `DraftPost`-এর ওপর `request_review` call করে তৈরি হয়, এবং একটি `approve` method যা `PendingReviewPost`-কে একটি published `Post`-এ রূপান্তর করে">

```rust,noplayground
impl DraftPost {
    // --snip--
    pub fn request_review(self) -> PendingReviewPost {
        PendingReviewPost {
            content: self.content,
        }
    }
}

pub struct PendingReviewPost {
    content: String,
}

impl PendingReviewPost {
    pub fn approve(self) -> Post {
        Post {
            content: self.content,
        }
    }
}
```

</Listing>

`request_review` এবং `approve` method-গুলো `self`-এর ownership নেয়, ফলে `DraftPost` এবং `PendingReviewPost` instance গুলোকে consume করে যথাক্রমে একটি `PendingReviewPost` এবং একটি published `Post`-এ রূপান্তর করে। এতে `request_review` call করার পর কোনো পিছনে পড়ে থাকা `DraftPost` instance থাকবে না, এভাবেই বাকি গুলো। `PendingReviewPost` struct-এর ওপর কোনো `content` method define করা নেই, তাই তার content পড়ার চেষ্টা করলে `DraftPost`-এর মতো compiler error হবে। যেহেতু `content` method define করা একটি published `Post` instance পাওয়ার একমাত্র উপায় হলো একটি `PendingReviewPost`-এর ওপর `approve` method call করা, এবং একটি `PendingReviewPost` পাওয়ার একমাত্র উপায় হলো একটি `DraftPost`-এর ওপর `request_review` method call করা, তাই আমরা এখন blog post workflow-টি type system-এ encode করে ফেলেছি।

তবে আমাদের `main`-এও কিছু ছোটখাটো পরিবর্তন করতে হবে। `request_review` এবং `approve` method গুলো যেই struct-এর ওপর call করা হয় তাকে modify না করে নতুন instance return করে, তাই আমাদের return হওয়া instance গুলো save করতে আরও কিছু `let post =` shadowing assignment যোগ করতে হবে। তাছাড়া draft এবং pending review post-গুলোর content empty string—এমন assertion-ও আর রাখতে পারবো না, তার দরকারও নেই: সেই state-গুলোতে থাকা post-গুলোর content ব্যবহার করার চেষ্টা করা code আর compile-ই হবে না। `main`-এর আপডেট করা code Listing 18-21-এ দেখানো হয়েছে।

<Listing number="18-21" file-name="src/main.rs" caption="blog post workflow-এর নতুন implementation ব্যবহার করতে `main`-এ পরিবর্তন">

```rust,ignore
use blog::Post;

fn main() {
    let mut post = Post::new();

    post.add_text("I ate a salad for lunch today");

    let post = post.request_review();

    let post = post.approve();

    assert_eq!("I ate a salad for lunch today", post.content());
}
```

</Listing>

`post` পুনরায় assign করতে আমাদের `main`-এ যে পরিবর্তন করতে হয়েছে তার মানে হলো—এই implementation আর সম্পূর্ণভাবে object-oriented state pattern অনুসরণ করছে না: state গুলোর মধ্যে transformation গুলো আর পুরোপুরি `Post` implementation-এ encapsulate করা নেই। তবে যা অর্জন করলাম তা হলো—type system এবং compile time-এ হওয়া type checking-এর কারণে invalid state এখন অসম্ভব! এতে নিশ্চিত হয় যে কিছু bug, যেমন একটি unpublished post-এর content প্রদর্শন—production-ে যাওয়ার আগেই ধরা পড়বে।

Listing 18-21-এর পরের state-এ `blog` crate-এর ওপর এই section-এর শুরুতে প্রস্তাবিত কাজগুলো চেষ্টা করো এবং দেখো এই সংস্করণের code design সম্পর্কে তোমার মতামত কী। মনে রাখো, কিছু কাজ হয়তো এই design-এ আগেই সম্পন্ন হয়ে গেছে।

আমরা দেখেছি যে Rust object-oriented design pattern implement করতে সক্ষম হলেও, অন্যান্য pattern যেমন type system-এ state encode করা—ও Rust-এ available। এই pattern গুলোর trade-off আলাদা। তুমি হয়তো object-oriented pattern-এ খুব পরিচিত, কিন্তু সমস্যাটিকে নতুন করে ভেবে Rust-এর feature গুলো কাজে লাগালে সুবিধা পাওয়া যেতে পারে, যেমন compile time-এ কিছু bug prevent করা। Object-oriented pattern সব সময় Rust-এ সেরা সমাধান হবে না, কারণ কিছু feature, যেমন ownership, object-oriented language-গুলোর নেই।

## Summary

এই chapter পড়ে তুমি Rust-কে object-oriented ভাষা মনে করো কি না, তা যেই হোক—তুমি এখন জানো যে Rust-এ trait object ব্যবহার করে কিছু object-oriented feature পাওয়া যায়। Dynamic dispatch কিছুটা runtime performance-এর বিনিময়ে code-কে flexibility দেয়। এই flexibility ব্যবহার করে তুমি object-oriented pattern implement করতে পারো যা code-এর maintainability-এ সাহায্য করবে। Rust-এ আরও feature আছে, যেমন ownership, যা object-oriented language-গুলোর নেই। Object-oriented pattern সব সময় Rust-এর শক্তি কাজে লাগানোর সেরা উপায় হবে না, তবে এটি একটি available option।

এরপর আমরা pattern নিয়ে আলোচনা করবো, যা Rust-এর আরেকটি feature যা প্রচুর flexibility দেয়। আমরা পুরো book জুড়ে সংক্ষেপে এগুলো দেখেছি কিন্তু তাদের সম্পূর্ণ সক্ষমতা এখনও দেখিনি। চলো এগোই!

[more-info-than-rustc]: ch09-03-to-panic-or-not-to-panic.html#cases-in-which-you-have-more-information-than-the-compiler
[macros]: ch20-05-macros.html#macros

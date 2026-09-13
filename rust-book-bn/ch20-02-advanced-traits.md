## Advanced Traits

আমরা প্রথমে Chapter 10-এর [“Defining Shared Behavior with
Traits”][traits]<!-- ignore --> section-এ trait নিয়ে আলোচনা করেছি, কিন্তু আমরা আরও advanced detail-গুলো নিয়ে আলোচনা করিনি। যেহেতু তুমি এখন Rust সম্পর্কে আরও বেশি জানো, আমরা এবার গভীরে যেতে পারি।

<!-- Old headings. Do not remove or links may break. -->

<a id="specifying-placeholder-types-in-trait-definitions-with-associated-types"></a>
<a id="associated-types"></a>

### Defining Traits with Associated Types

_Associated type_ একটি type placeholder-কে একটি trait-এর সাথে যুক্ত করে, যাতে trait method definition-গুলো তাদের signature-এ এই placeholder type ব্যবহার করতে পারে। একটি trait-এর implementor নির্দিষ্ট implementation-এর জন্য placeholder type-এর পরিবর্তে কোন concrete type ব্যবহার করা হবে তা specify করবে। এভাবে, আমরা এমন একটি trait define করতে পারি যা কিছু type ব্যবহার করে কিন্তু trait implement না হওয়া পর্যন্ত সেই type-গুলো ঠিক কী তা জানার প্রয়োজন নেই।

আমরা এই chapter-এ বেশিরভাগ advanced feature-কে খুব কম প্রয়োজন হয় এমন হিসেবে describe করেছি। Associated type-গুলো মাঝামাঝি জায়গায়: এগুলো book-এর বাকি অংশে ব্যাখ্যা করা feature-গুলোর চেয়ে কম ব্যবহৃত হয় কিন্তু এই chapter-এ আলোচিত অন্যান্য অনেক feature-এর চেয়ে বেশি common।

Associated type সহ একটি trait-এর একটি উদাহরণ হলো standard library দ্বারা provide করা `Iterator` trait। Associated type-টির নাম `Item` এবং এটি `Iterator` trait implement করা type যার উপর iterate করা হচ্ছে তার value-র type-এর জন্য দাঁড়ায়। `Iterator` trait-এর definition Listing 20-13-এ দেখানো হয়েছে।

<Listing number="20-13" caption="The definition of the `Iterator` trait that has an associated type `Item`">

```rust,noplayground
pub trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;
}
```

</Listing>

`Item` type-টি একটি placeholder, এবং `next` method-এর definition দেখায় যে এটি `Option<Self::Item>` type-এর value return করবে। `Iterator` trait-এর implementor-রা `Item`-এর জন্য concrete type specify করবে, এবং `next` method সেই concrete type-এর একটি value ধারণকারী একটি `Option` return করবে।

Associated type-গুলো generics-এর সাথে অনুরূপ একটি concept মনে হতে পারে, কারণ পরেরটি আমাদের এমন একটি function define করতে দেয় যা কোন type handle করে তা না বলেই। দুটি concept-এর মধ্যে পার্থক্য পরীক্ষা করতে, আমরা `Counter` নামের একটি type-এ `Iterator` trait-এর একটি implementation দেখব যেখানে `Item` type হিসেবে `u32` specify করা:

<Listing file-name="src/lib.rs">

```rust,ignore
impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {
        // --snip--
```

</Listing>

এই syntax generics-এর syntax-এর সাথে comparable মনে হয়। তাহলে, কেন `Iterator` trait-কে Listing 20-14-এ দেখানোর মতো generics দিয়ে define করছি না?

<Listing number="20-14" caption="A hypothetical definition of the `Iterator` trait using generics">

```rust,noplayground
pub trait Iterator<T> {
    fn next(&mut self) -> Option<T>;
}
```

</Listing>

পার্থক্য হলো, Listing 20-14-এর মতো generics ব্যবহার করলে, আমাদের প্রতিটি implementation-এ type annotate করতে হবে; যেহেতু আমরা `Iterator<String> for Counter` বা অন্য যেকোনো type-ও implement করতে পারি, আমাদের কাছে `Counter`-এর জন্য `Iterator`-এর একাধিক implementation থাকতে পারে। অন্য কথায়, যখন একটি trait-এ একটি generic parameter থাকে, তখন এটি একটি type-এর জন্য একাধিকবার implement করা যেতে পারে, প্রতিবার generic type parameter-গুলোর concrete type পরিবর্তন করে। যখন আমরা `Counter`-এর উপর `next` method ব্যবহার করব, তখন আমাদের আমরা কোন `Iterator`-এর implementation ব্যবহার করতে চাই তা নির্দেশ করতে type annotation দিতে হবে।

Associated type-এর সাথে, আমাদের type annotate করার প্রয়োজন নেই, কারণ আমরা একটি type-এ একটি trait একাধিকবার implement করতে পারি না। Listing 20-13-এ associated type ব্যবহার করা definition-এর সাথে, আমরা `Item`-এর type কী হবে তা শুধু একবার choose করতে পারি কারণ শুধুমাত্র একটি `impl Iterator for Counter` থাকতে পারে। `Counter`-এ আমরা যেখানেই `next` কল করি না কেন, সব জায়গায় আমাদের এটি specify করতে হবে না যে আমরা `u32` value-র iterator চাই।

Associated type-গুলো trait-এর contract-এরও অংশ হয়ে যায়: trait-এর implementor-কে অবশ্যই associated type placeholder-এর জায়গায় দাঁড়ানোর জন্য একটি type provide করতে হবে। Associated type-গুলোর প্রায়ই এমন একটি নাম থাকে যা describe করে যে type-টি কীভাবে ব্যবহৃত হবে, এবং API documentation-এ associated type document করা একটি ভালো practice।

<!-- Old headings. Do not remove or links may break. -->

<a id="default-generic-type-parameters-and-operator-overloading"></a>

### Using Default Generic Parameters and Operator Overloading

আমরা যখন generic type parameter ব্যবহার করি, তখন আমরা generic type-এর জন্য একটি default concrete type specify করতে পারি। এতে trait-এর implementor-কে যদি default type কাজ করে তবে concrete type specify করার প্রয়োজন নেই। তুমি `<PlaceholderType=ConcreteType>` syntax দিয়ে একটি generic type declare করার সময় একটি default type specify করো।

এমন একটি situation-এ এই technique যেখানে useful সেটির একটি দুর্দান্ত উদাহরণ হলো _operator overloading_, যেখানে তুমি নির্দিষ্ট situation-এ একটি operator (যেমন `+`)-এর behavior customize করো।

Rust তোমাকে নিজের operator তৈরি করতে বা arbitrary operator overload করতে দেয় না। কিন্তু তুমি `std::ops`-এ তালিকাভুক্ত operation এবং সংশ্লিষ্ট trait-গুলো overload করতে পারো, operator-এর সাথে যুক্ত trait implement করার মাধ্যমে। উদাহরণস্বরূপ, Listing 20-15-এ, আমরা দুটি `Point` instance একসাথে যোগ করতে `+` operator overload করি। আমরা এটি একটি `Point` struct-এর উপর `Add` trait implement করে করি।

<Listing number="20-15" file-name="src/main.rs" caption="Implementing the `Add` trait to overload the `+` operator for `Point` instances">

```rust
use std::ops::Add;

#[derive(Debug, Copy, Clone, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

impl Add for Point {
    type Output = Point;

    fn add(self, other: Point) -> Point {
        Point {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

fn main() {
    assert_eq!(
        Point { x: 1, y: 0 } + Point { x: 2, y: 3 },
        Point { x: 3, y: 3 }
    );
}
```

</Listing>

`add` method দুটি `Point` instance-এর `x` value এবং দুটি `Point` instance-এর `y` value যোগ করে একটি নতুন `Point` তৈরি করে। `Add` trait-এ একটি associated type আছে যার নাম `Output` যা `add` method থেকে return হওয়া type নির্ধারণ করে।

এই code-এ default generic type-টি `Add` trait-এর ভেতরে আছে। এর definition নিচে দেওয়া হলো:

```rust
trait Add<Rhs=Self> {
    type Output;

    fn add(self, rhs: Rhs) -> Self::Output;
}
```

এই code-টি সাধারণত পরিচিত মনে হওয়া উচিত: একটি method এবং একটি associated type সহ একটি trait। নতুন অংশ হলো `Rhs=Self`: এই syntax-কে _default type parameter_ বলা হয়। `Rhs` generic type parameter ("right-hand side"-এর সংক্ষিপ্ত) `add` method-এর `rhs` parameter-এর type define করে। যদি আমরা `Add` trait implement করার সময় `Rhs`-এর জন্য কোনো concrete type specify না করি, তবে `Rhs`-এর type ডিফল্টরূপে `Self` হবে, যা সেই type হবে যেখানে আমরা `Add` implement করছি।

যখন আমরা `Point`-এর জন্য `Add` implement করেছি, তখন আমরা `Rhs`-এর জন্য default ব্যবহার করেছি কারণ আমরা দুটি `Point` instance যোগ করতে চেয়েছিলাম। চলো এমন একটি উদাহরণ দেখি যেখানে আমরা default ব্যবহার না করে `Rhs` type customize করতে চাই `Add` trait implement করে।

আমাদের কাছে দুটি struct আছে, `Millimeters` এবং `Meters`, ভিন্ন ভিন্ন unit-এ value ধারণ করে। একটি বিদ্যমান type-কে অন্য struct-এ এভাবে thin wrap করাকে _newtype pattern_ বলা হয়, যা আমরা [“Implementing
External Traits with the Newtype Pattern”][newtype]<!-- ignore --> section-এ আরও বিস্তারিত বর্ণনা করি। আমরা millimeter-এর value-র সাথে meter-এর value যোগ করতে চাই এবং `Add`-এর implementation যাতে সঠিকভাবে conversion করে তা চাই। আমরা `Meters`-কে `Rhs` হিসেবে নিয়ে `Millimeters`-এর জন্য `Add` implement করতে পারি, যেমন Listing 20-16-তে দেখানো হয়েছে।

<Listing number="20-16" file-name="src/lib.rs" caption="Implementing the `Add` trait on `Millimeters` to add `Millimeters` and `Meters`">

```rust,noplayground
use std::ops::Add;

struct Millimeters(u32);
struct Meters(u32);

impl Add<Meters> for Millimeters {
    type Output = Millimeters;

    fn add(self, other: Meters) -> Millimeters {
        Millimeters(self.0 + (other.0 * 1000))
    }
}
```

</Listing>

`Millimeters` এবং `Meters` যোগ করতে, আমরা `impl Add<Meters>` specify করি যাতে `Self` default ব্যবহার না করে `Rhs` type parameter-এর value সেট করা যায়।

তুমি দুটি প্রধান উপায়ে default type parameter ব্যবহার করবে:

1. একটি type-কে existing code না ভেঙে extend করতে
2. বেশিরভাগ user-এর প্রয়োজন হবে না এমন নির্দিষ্ট ক্ষেত্রে customization allow করতে

Standard library-র `Add` trait দ্বিতীয় উদ্দেশ্যের একটি উদাহরণ: সাধারণত, তুমি দুটি সদৃশ type যোগ করবে, কিন্তু `Add` trait এর বাইরে customize করার ক্ষমতা provide করে। `Add` trait definition-এ একটি default type parameter ব্যবহার করার মানে হলো তোমাকে বেশিরভাগ সময় অতিরিক্ত parameter specify করতে হবে না। অন্য কথায়, কিছু implementation boilerplate-এর প্রয়োজন নেই, যাতে trait-টি ব্যবহার করা সহজ হয়।

প্রথম উদ্দেশ্যটি দ্বিতীয়টির মতো কিন্তু উল্টো: যদি তুমি একটি existing trait-এ একটি type parameter যোগ করতে চাও, তুমি এটিকে একটি default দিতে পারো যাতে existing implementation code না ভেঙে trait-টির functionality extend করা যায়।

<!-- Old headings. Do not remove or links may break. -->

<a id="fully-qualified-syntax-for-disambiguation-calling-methods-with-the-same-name"></a>
<a id="disambiguating-between-methods-with-the-same-name"></a>

### Disambiguating Between Identically Named Methods

Rust-এ এমন কিছু নেই যা একটি trait-কে অন্য trait-এর method-এর মতো একই নামের একটি method রাখতে বাধা দেয়, এবং Rust তোমাকে একটি type-এ দুটি trait-ই implement করতেও বাধা দেয় না। এটি সম্ভব যে তুমি trait-থেকে আসা method-গুলোর সাথে একই নামের একটি method সরাসরি type-এ implement করো।

একই নামের method কল করার সময়, তোমাকে Rust-কে বলতে হবে তুমি কোনটি ব্যবহার করতে চাও। Listing 20-17-তে code-টি বিবেচনা করো যেখানে আমরা দুটি trait define করেছি, `Pilot` এবং `Wizard`, যাদের উভয়ের একটি `fly` নামের method আছে। তারপর আমরা একটি `Human` type-এ উভয় trait implement করি যার উপর ইতিমধ্যে একটি `fly` নামের method implement করা আছে। প্রতিটি `fly` method ভিন্ন কিছু করে।

<Listing number="20-17" file-name="src/main.rs" caption="Two traits are defined to have a `fly` method and are implemented on the `Human` type, and a `fly` method is implemented on `Human` directly.">

```rust
trait Pilot {
    fn fly(&self);
}

trait Wizard {
    fn fly(&self);
}

struct Human;

impl Pilot for Human {
    fn fly(&self) {
        println!("This is your captain speaking.");
    }
}

impl Wizard for Human {
    fn fly(&self) {
        println!("Up!");
    }
}

impl Human {
    fn fly(&self) {
        println!("*waving arms furiously*");
    }
}
```

</Listing>

যখন আমরা একটি `Human` instance-এর উপর `fly` কল করি, compiler ডিফল্টরূপে সরাসরি type-এর উপর implement করা method-টিকে কল করে, যেমন Listing 20-18-তে দেখানো হয়েছে।

<Listing number="20-18" file-name="src/main.rs" caption="Calling `fly` on an instance of `Human`">

```rust
fn main() {
    let person = Human;
    person.fly();
}
```

</Listing>

এই code run করলে `*waving arms furiously*` print করবে, যা দেখায় যে Rust সরাসরি `Human`-এর উপর implement করা `fly` method-কে কল করেছে।

`Pilot` trait বা `Wizard` trait-এর `fly` method-গুলো কল করতে, আমাদের আরও explicit syntax ব্যবহার করতে হবে যাতে specify করা যায় আমরা কোন `fly` method বোঝাতে চাই। Listing 20-19 এই syntax প্রদর্শন করে।

<Listing number="20-19" file-name="src/main.rs" caption="Specifying which trait’s `fly` method we want to call">

```rust
fn main() {
    let person = Human;
    Pilot::fly(&person);
    Wizard::fly(&person);
    person.fly();
}
```

</Listing>

Method-এর নামের আগে trait-এর নাম specify করা Rust-কে ব্যাখ্যা করে যে আমরা `fly`-এর কোন implementation কল করতে চাই। আমরা `Human::fly(&person)` ও লিখতে পারতাম, যা Listing 20-19-এ আমরা যে `person.fly()` ব্যবহার করেছি তার সমতুল্য, কিন্তু আমাদের disambiguate করার প্রয়োজন না থাকলে এটি লিখতে একটু বেশি বড়।

এই code run করলে নিম্নলিখিত print করে:

```console
$ cargo run
   Compiling traits-example v0.1.0 (file:///projects/traits-example)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.46s
     Running `target/debug/traits-example`
This is your captain speaking.
Up!
*waving arms furiously*
```

যেহেতু `fly` method একটি `self` parameter নেয়, যদি আমাদের দুটি _type_ থাকতো যাদের উভয়ই একটি _trait_ implement করে, তবে Rust `self`-এর type-এর উপর ভিত্তি করে বুঝতে পারতো যে কোন trait-এর implementation ব্যবহার করতে হবে।

তবে, যেসব associated function method নয় সেগুলোর `self` parameter নেই। যখন একই function নাম সহ non-method function define করে এমন একাধিক type বা trait থাকে, Rust সবসময় জানে না তুমি কোন type বোঝাতে চাইছো, যদি না তুমি fully qualified syntax ব্যবহার করো। উদাহরণস্বরূপ, Listing 20-20-তে, আমরা একটি animal shelter-এর জন্য একটি trait তৈরি করি যারা সব baby dog-এর নাম Spot রাখতে চায়। আমরা একটি `Animal` trait তৈরি করি যার একটি associated non-method function `baby_name` আছে। `Animal` trait-টি `Dog` struct-এর জন্য implement করা হয়েছে, যার উপর আমরা সরাসরি একটি associated non-method function `baby_name`-ও provide করি।

<Listing number="20-20" file-name="src/main.rs" caption="A trait with an associated function and a type with an associated function of the same name that also implements the trait">

```rust
trait Animal {
    fn baby_name() -> String;
}

struct Dog;

impl Dog {
    fn baby_name() -> String {
        String::from("Spot")
    }
}

impl Animal for Dog {
    fn baby_name() -> String {
        String::from("puppy")
    }
}

fn main() {
    println!("A baby dog is called a {}", Dog::baby_name());
}
```

</Listing>

আমরা সব puppy-এর নাম Spot রাখার জন্য code `Dog`-এর উপর define করা `baby_name` associated function-এ implement করি। `Dog` type `Animal` trait-ও implement করে, যা সব প্রাণীর বৈশিষ্ট্য বর্ণনা করে। Baby dog-কে puppy বলা হয়, এবং তা `Dog`-এর উপর `Animal` trait-এর implementation-এ `Animal` trait-এর সাথে যুক্ত `baby_name` function-এ প্রকাশ করা হয়েছে।

`main`-এ, আমরা `Dog::baby_name` function কল করি, যা সরাসরি `Dog`-এর উপর define করা associated function-কে কল করে। এই code নিম্নলিখিত print করে:

```console
$ cargo run
   Compiling traits-example v0.1.0 (file:///projects/traits-example)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.54s
     Running `target/debug/traits-example`
A baby dog is called a Spot
```

এই output আমরা যা চেয়েছিলাম তা নয়। আমরা `Dog`-এর উপর implement করা `Animal` trait-এর অংশ `baby_name` function-টি কল করতে চাই যাতে code-টি `A baby dog is called a puppy` print করে। Listing 20-19-এ আমরা যে technique টি trait-এর নাম specify করতে ব্যবহার করেছি সেটি এখানে সাহায্য করে না; যদি আমরা `main`-কে Listing 20-21-এর code-এ পরিবর্তন করি, তবে আমরা একটি compilation error পাবো।

<Listing number="20-21" file-name="src/main.rs" caption="Attempting to call the `baby_name` function from the `Animal` trait, but Rust doesn’t know which implementation to use">

```rust,ignore,does_not_compile
fn main() {
    println!("A baby dog is called a {}", Animal::baby_name());
}
```

</Listing>

যেহেতু `Animal::baby_name`-এর কোনো `self` parameter নেই, এবং অন্যান্য type যারা `Animal` trait implement করে তা থাকতে পারে, Rust বুঝতে পারে না আমরা `Animal::baby_name`-এর কোন implementation চাই। আমরা এই compiler error পাবো:

```console
$ cargo run
   Compiling traits-example v0.1.0 (file:///projects/traits-example)
error[E0790]: cannot call associated function on trait without specifying the corresponding `impl` type
  --> src/main.rs:20:43
   |
 2 |     fn baby_name() -> String;
   |     ------------------------- `Animal::baby_name` defined here
...
20 |     println!("A baby dog is called a {}", Animal::baby_name());
   |                                           ^^^^^^^^^^^^^^^^^^^ cannot call associated function of trait
   |
help: use the fully-qualified path to the only available implementation
   |
20 |     println!("A baby dog is called a {}", <Dog as Animal>::baby_name());
   |                                           +++++++       +

For more information about this error, try `rustc --explain E0790`.
error: could not compile `traits-example` (bin "traits-example") due to 1 previous error
```

Disambiguate করতে এবং Rust-কে বলতে যে আমরা অন্য কোনো type-এর জন্য `Animal`-এর implementation-এর বদলে `Dog`-এর জন্য `Animal`-এর implementation ব্যবহার করতে চাই, আমাদের fully qualified syntax ব্যবহার করতে হবে। Listing 20-22 দেখায় কীভাবে fully qualified syntax ব্যবহার করতে হয়।

<Listing number="20-22" file-name="src/main.rs" caption="Using fully qualified syntax to specify that we want to call the `baby_name` function from the `Animal` trait as implemented on `Dog`">

```rust
fn main() {
    println!("A baby dog is called a {}", <Dog as Animal>::baby_name());
}
```

</Listing>

আমরা Rust-কে angle bracket-এর ভেতরে একটি type annotation দিচ্ছি, যা নির্দেশ করে যে আমরা `Dog` type-কে এই function call-এর জন্য একটি `Animal` হিসেবে treat করতে চাই বলে `Dog`-এর উপর implement করা `Animal` trait-এর `baby_name` method কল করতে চাই। এই code এখন আমরা যা চাই তা print করবে:

```console
$ cargo run
   Compiling traits-example v0.1.0 (file:///projects/traits-example)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.48s
     Running `target/debug/traits-example`
A baby dog is called a puppy
```

সাধারণভাবে, fully qualified syntax নিচের মতো define করা:

```rust,ignore
<Type as Trait>::function(receiver_if_method, next_arg, ...);
```

Method নয় এমন associated function-এর জন্য, কোনো `receiver` থাকবে না: শুধু অন্যান্য argument-গুলোর list থাকবে। তুমি যেখানে function বা method কল করো সব জায়গায় fully qualified syntax ব্যবহার করতে পারো। তবে, তুমি এই syntax-এর যেকোনো অংশ omit করতে পারো যা Rust program-এর অন্যান্য information থেকে বের করতে পারে। তোমাকে শুধু এই আরও verbose syntax সেই ক্ষেত্রে ব্যবহার করতে হবে যেখানে একই নাম ব্যবহার করে এমন একাধিক implementation থাকে এবং Rust-কে তুমি কোন implementation কল করতে চাইছো তা identify করতে সাহায্য প্রয়োজন।

<!-- Old headings. Do not remove or links may break. -->

<a id="using-supertraits-to-require-one-traits-functionality-within-another-trait"></a>

### Using Supertraits

মাঝে মাঝে তুমি এমন একটি trait definition লিখতে পারো যা অন্য একটি trait-এর উপর নির্ভর করে: একটি type-এর প্রথম trait implement করার জন্য, তুমি চাইবে সেই type-টিকে দ্বিতীয় trait-ও implement করতে হবে। তুমি এটি এই কারণে করবে যাতে তোমার trait definition দ্বিতীয় trait-এর associated item-গুলো ব্যবহার করতে পারে। যে trait-এর উপর তোমার trait definition নির্ভর করছে তাকে তোমার trait-এর একটি _supertrait_ বলা হয়।

উদাহরণস্বরূপ, ধরা যাক আমরা একটি `OutlinePrint` trait তৈরি করতে চাই যার একটি `outline_print` method আছে যা একটি দেওয়া value-কে asterisk-এ framed হিসেবে format করে print করবে। অর্থাৎ, একটি `Point` struct যা standard library trait `Display` implement করে যার ফলাফল `(x, y)`, যখন আমরা একটি `Point` instance-এর উপর `outline_print` কল করবো যার `x`-এর জন্য `1` এবং `y`-এর জন্য `3`, এটি নিম্নলিখিত print করবে:

```text
**********
*        *
* (1, 3) *
*        *
**********
```

`outline_print` method-এর implementation-এ, আমরা `Display` trait-এর functionality ব্যবহার করতে চাই। সুতরাং, আমাদের specify করতে হবে যে `OutlinePrint` trait শুধুমাত্র সেই type-গুলোর জন্য কাজ করবে যা `Display`-ও implement করে এবং `OutlinePrint`-এর প্রয়োজনীয় functionality provide করে। আমরা সেটি trait definition-এ `OutlinePrint: Display` specify করে করতে পারি। এই technique একটি trait-এ trait bound যোগ করার মতো। Listing 20-23 `OutlinePrint` trait-এর একটি implementation দেখায়।

<Listing number="20-23" file-name="src/main.rs" caption="Implementing the `OutlinePrint` trait that requires the functionality from `Display`">

```rust
use std::fmt;

trait OutlinePrint: fmt::Display {
    fn outline_print(&self) {
        let output = self.to_string();
        let len = output.len();
        println!("{}", "*".repeat(len + 4));
        println!("*{}*", " ".repeat(len + 2));
        println!("* {output} *");
        println!("*{}*", " ".repeat(len + 2));
        println!("{}", "*".repeat(len + 4));
    }
}
```

</Listing>

যেহেতু আমরা specify করেছি যে `OutlinePrint`-এর `Display` trait প্রয়োজন, আমরা `to_string` function ব্যবহার করতে পারি যা `Display` implement করে এমন যেকোনো type-এর জন্য স্বয়ংক্রিয়ভাবে implement করা। যদি আমরা trait-এর নামের পরে colon এবং `Display` trait specify না করে `to_string` ব্যবহার করার চেষ্টা করতাম, তবে আমরা এমন একটি error পেতাম যে বর্তমান scope-এ `&Self` type-এর জন্য `to_string` নামে কোনো method পাওয়া যায়নি।

চলো দেখি কী হয় যখন আমরা এমন একটি type-এর উপর `OutlinePrint` implement করার চেষ্টা করি যা `Display` implement করে না, যেমন `Point` struct:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
struct Point {
    x: i32,
    y: i32,
}

impl OutlinePrint for Point {}
```

</Listing>

আমরা এমন একটি error পাই যে `Display` প্রয়োজন কিন্তু implement করা নেই:

```console
$ cargo run
   Compiling traits-example v0.1.0 (file:///projects/traits-example)
error[E0277]: `Point` doesn't implement `std::fmt::Display`
  --> src/main.rs:20:23
   |
20 | impl OutlinePrint for Point {}
   |                       ^^^^^ unsatisfied trait bound
   |
help: the trait `std::fmt::Display` is not implemented for `Point`
  --> src/main.rs:15:1
   |
15 | struct Point {
   | ^^^^^^^^^^^^
note: required by a bound in `OutlinePrint`
  --> src/main.rs:3:21
   |
 3 | trait OutlinePrint: fmt::Display {
   |                     ^^^^^^^^^^^^ required by this bound in `OutlinePrint`

error[E0277]: `Point` doesn't implement `std::fmt::Display`
  --> src/main.rs:24:7
   |
24 |     p.outline_print();
   |       ^^^^^^^^^^^^^ unsatisfied trait bound
   |
help: the trait `std::fmt::Display` is not implemented for `Point`
  --> src/main.rs:15:1
   |
15 | struct Point {
   | ^^^^^^^^^^^^
note: required by a bound in `OutlinePrint::outline_print`
  --> src/main.rs:3:21
   |
 3 | trait OutlinePrint: fmt::Display {
   |                     ^^^^^^^^^^^^ required by this bound in `OutlinePrint::outline_print`
 4 |     fn outline_print(&self) {
   |        ------------- required by a bound in this associated function

For more information about this error, try `rustc --explain E0277`.
error: could not compile `traits-example` (bin "traits-example") due to 2 previous errors
```

এটি fix করতে, আমরা `Point`-এর উপর `Display` implement করি এবং `OutlinePrint` যে constraint প্রয়োজন তা satisfy করি, যেমন:

<Listing file-name="src/main.rs">

```rust
use std::fmt;

impl fmt::Display for Point {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}
```

</Listing>

তারপর, `Point`-এর উপর `OutlinePrint` trait implement করা successfully compile হবে, এবং আমরা একটি `Point` instance-এর উপর `outline_print` কল করে এটিকে asterisk-এর outline-এর ভেতরে display করতে পারব।

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-newtype-pattern-to-implement-external-traits-on-external-types"></a>
<a id="using-the-newtype-pattern-to-implement-external-traits"></a>

### Implementing External Traits with the Newtype Pattern

Chapter 10-এর [“Implementing a Trait on a Type”][implementing-a-trait-on-a-type]<!--
ignore --> section-এ, আমরা orphan rule উল্লেখ করেছি যা বলে যে আমরা শুধুমাত্র তখনই একটি type-এর উপর একটি trait implement করতে পারি যদি trait বা type, অথবা উভয়ই, আমাদের crate-এ local হয়। Newtype pattern ব্যবহার করে এই restriction এড়ানো সম্ভব, যা একটি tuple struct-এ একটি নতুন type তৈরি করে। (আমরা Chapter 5-এর [“Creating Different Types with
Tuple Structs”][tuple-structs]<!-- ignore --> section-এ tuple struct cover করেছি।) Tuple struct-টির একটি field থাকবে এবং যে type-এর জন্য আমরা trait implement করতে চাই তার চারপাশে একটি thin wrapper হবে। তারপর, wrapper type-টি আমাদের crate-এ local, এবং আমরা wrapper-এর উপর trait implement করতে পারি। _Newtype_ এমন একটি term যা Haskell programming language থেকে এসেছে। এই pattern ব্যবহার করার জন্য কোনো runtime performance penalty নেই, এবং wrapper type compile time-এ elide করা হয়।

একটি উদাহরণ হিসেবে, ধরা যাক আমরা `Vec<T>`-এর উপর `Display` implement করতে চাই, যা orphan rule আমাদের সরাসরি করতে বাধা দেয় কারণ `Display` trait এবং `Vec<T>` type আমাদের crate-এর বাইরে define করা। আমরা একটি `Wrapper` struct তৈরি করতে পারি যা একটি `Vec<T>` instance ধারণ করে; তারপর, আমরা `Wrapper`-এর উপর `Display` implement করতে পারি এবং `Vec<T>` value ব্যবহার করতে পারি, যেমন Listing 20-24-তে দেখানো হয়েছে।

<Listing number="20-24" file-name="src/main.rs" caption="Creating a `Wrapper` type around `Vec<String>` to implement `Display`">

```rust
use std::fmt;

struct Wrapper(Vec<String>);

impl fmt::Display for Wrapper {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "[{}]", self.0.join(", "))
    }
}

fn main() {
    let w = Wrapper(vec![String::from("hello"), String::from("world")]);
    println!("w = {w}");
}
```

</Listing>

`Display`-এর implementation-এ `self.0` ব্যবহার করে ভেতরের `Vec<T>` access করা হয় কারণ `Wrapper` একটি tuple struct এবং `Vec<T>` tuple-এর index 0-এর item। তারপর, আমরা `Wrapper`-এর উপর `Display` trait-এর functionality ব্যবহার করতে পারি।

এই technique ব্যবহারের downside হলো `Wrapper` একটি নতুন type, তাই এর যে value ধারণ করে তার method-গুলো নেই। আমাদের `Wrapper`-এ সরাসরি `Vec<T>`-এর সব method implement করতে হবে যাতে method-গুলো `self.0`-এ delegate করে, যা আমাদেরকে `Wrapper`-কে ঠিক `Vec<T>`-এর মতো treat করতে দেবে। যদি আমরা চাই নতুন type-টির কাছে inner type-এর প্রতিটি method থাকুক, তবে `Wrapper`-এর উপর `Deref` trait implement করে inner type return করা একটি solution হবে (আমরা Chapter 15-এর [“Treating
Smart Pointers Like Regular References”][smart-pointer-deref]<!-- ignore --> section-এ `Deref` trait implement করা আলোচনা করেছি)। যদি আমরা না চাই যে `Wrapper` type-টির কাছে inner type-এর সব method থাকুক—উদাহরণস্বরূপ, `Wrapper` type-এর behavior restrict করতে—তবে আমাদের শুধু আমরা যে method-গুলো চাই সেগুলো ম্যানুয়ালি implement করতে হবে।

এই newtype pattern trait জড়িত না থাকলেও useful। চলো focus পরিবর্তন করি এবং Rust-এর type system-এর সাথে interact করার কিছু advanced উপায় দেখি।

[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern
[implementing-a-trait-on-a-type]: ch10-02-traits.html#implementing-a-trait-on-a-type
[traits]: ch10-02-traits.html
[smart-pointer-deref]: ch15-02-deref.html#treating-smart-pointers-like-regular-references
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs

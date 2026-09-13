## Advanced Types

Rust type system-এর কিছু feature আছে যা আমরা এখন পর্যন্ত উল্লেখ করেছি কিন্তু আলোচনা করিনি। আমরা প্রথমে newtype-কে সাধারণভাবে আলোচনা করবো কেন সেগুলো type হিসেবে useful তা দেখে। তারপর, আমরা type alias-এ চলে যাব, যা newtype-এর মতো কিন্তু সামান্য ভিন্ন semantics সহ। আমরা `!` type এবং dynamically sized type নিয়েও আলোচনা করব।

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-newtype-pattern-for-type-safety-and-abstraction"></a>

### Type Safety and Abstraction with the Newtype Pattern

এই section ধরে নেয় যে তুমি পূর্ববর্তী section [“Implementing External
Traits with the Newtype Pattern”][newtype]<!-- ignore --> পড়েছ। Newtype pattern এখন পর্যন্ত আলোচিত কাজের বাইরেও কিছু task-এর জন্য useful, যার মধ্যে statically enforce করা যে value-গুলো কখনো confused হবে না এবং একটি value-র unit নির্দেশ করা। তুমি unit indicate করতে newtype ব্যবহারের একটি উদাহরণ Listing 20-16-তে দেখেছ: মনে করো যে `Millimeters` এবং `Meters` struct একটি newtype-এ `u32` value wrap করেছিল। যদি আমরা `Millimeters` type-এর একটি parameter সহ একটি function লিখতাম, তবে আমরা এমন একটি program compile করতে পারতাম না যা accidentally সেই function-কে `Meters` type-এর বা একটি plain `u32` value দিয়ে কল করার চেষ্টা করে।

আমরা newtype pattern ব্যবহার করে একটি type-এর কিছু implementation detail abstract করতেও পারি: নতুন type-টি private inner type-এর API থেকে ভিন্ন একটি public API expose করতে পারে।

Newtype গুলো internal implementation ও লুকাতে পারে। উদাহরণস্বরূপ, আমরা একটি `People` type provide করতে পারি যা `HashMap<i32, String>`-কে wrap করে যা একজন ব্যক্তির ID তাদের নামের সাথে store করে। `People` ব্যবহার করা code শুধুমাত্র আমরা যে public API provide করি তার সাথে interact করবে, যেমন `People` collection-এ একটি name string যোগ করার একটি method; সেই code-কে জানতে হবে না যে আমরা নামের সাথে একটি `i32` ID অভ্যন্তরীণভাবে assign করি। Newtype pattern encapsulation অর্জনের একটি lightweight উপায় যা implementation detail লুকায়, যা আমরা Chapter 18-এর [“Encapsulation that
Hides Implementation
Details”][encapsulation-that-hides-implementation-details]<!-- ignore --> section-এ আলোচনা করেছি।

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-type-synonyms-with-type-aliases"></a>

### Type Synonyms and Type Aliases

Rust একটি বিদ্যমান type-কে অন্য নাম দেওয়ার জন্য একটি _type alias_ declare করার ক্ষমতা provide করে। এর জন্য আমরা `type` keyword ব্যবহার করি। উদাহরণস্বরূপ, আমরা এভাবে `i32`-এর alias `Kilometers` তৈরি করতে পারি:

```rust
    type Kilometers = i32;
```

এখন alias `Kilometers` হলো `i32`-এর একটি _synonym_; Listing 20-16-তে আমরা যে `Millimeters` এবং `Meters` type তৈরি করেছিলাম তার বিপরীতে, `Kilometers` একটি পৃথক, নতুন type নয়। `Kilometers` type-এর value-গুলো `i32` type-এর value-এর মতোই treat করা হবে:

```rust
    type Kilometers = i32;

    let x: i32 = 5;
    let y: Kilometers = 5;

    println!("x + y = {}", x + y);
}
```

যেহেতু `Kilometers` এবং `i32` একই type, আমরা উভয় type-এর value যোগ করতে পারি এবং `i32` parameter নেয় এমন function-গুলোতে `Kilometers` value pass করতে পারি। তবে, এই method ব্যবহার করে, আমরা পূর্বে আলোচিত newtype pattern থেকে যে type-checking benefit পাই তা পাই না। অন্য কথায়, যদি আমরা কোথাও `Kilometers` এবং `i32` value mix করে ফেলি, তবে compiler আমাদের কোনো error দেবে না।

Type synonym-গুলোর প্রধান use case হলো repetition কমানো। উদাহরণস্বরূপ, আমাদের হয়তো এমন একটি দীর্ঘ type থাকতে পারে:

```rust,ignore
Box<dyn Fn() + Send + 'static>
```

এই দীর্ঘ type-টি function signature-এ এবং সারা code-এ type annotation হিসেবে লেখা ক্লান্তিকর এবং error-prone। ভাবো Listing 20-25-এর মতো এমন code-এ পূর্ণ একটি project থাকার কথা।

<Listing number="20-25" caption="Using a long type in many places">

```rust
    let f: Box<dyn Fn() + Send + 'static> = Box::new(|| println!("hi"));

    fn takes_long_type(f: Box<dyn Fn() + Send + 'static>) {
        // --snip--
    }

    fn returns_long_type() -> Box<dyn Fn() + Send + 'static> {
        // --snip--
    }
```

</Listing>

একটি type alias এই code-টিকে আরও manageable করে repetition কমিয়ে। Listing 20-26-তে, আমরা verbose type-টির জন্য `Thunk` নামে একটি alias introduce করেছি এবং type-টির সব ব্যবহার ছোট alias `Thunk` দিয়ে replace করতে পারি।

<Listing number="20-26" caption="Introducing a type alias, `Thunk`, to reduce repetition">

```rust
    type Thunk = Box<dyn Fn() + Send + 'static>;

    let f: Thunk = Box::new(|| println!("hi"));

    fn takes_long_type(f: Thunk) {
        // --snip--
    }

    fn returns_long_type() -> Thunk {
        // --snip--
    }
```

</Listing>

এই code পড়তে এবং লিখতে অনেক সহজ! একটি type alias-এর জন্য অর্থপূর্ণ নাম choose করা তোমার intent communicate করতেও সাহায্য করে (_thunk_ হলো এমন একটি শব্দ যা পরে evaluate করা হবে এমন code-কে বোঝায়, তাই এটি store করা একটি closure-এর জন্য একটি উপযুক্ত নাম)।

Type alias-গুলো `Result<T, E>` type-এর সাথেও repetition কমানোর জন্য commonly ব্যবহৃত হয়। Standard library-এর `std::io` module-টি বিবেচনা করো। I/O operation-গুলো প্রায়ই একটি `Result<T, E>` return করে যখন operation কাজ করতে ব্যর্থ হয় সেই situation handle করতে। এই library-তে একটি `std::io::Error` struct আছে যা সব সম্ভাব্য I/O error represent করে। `std::io`-র অনেক function `Result<T, E>` return করবে যেখানে `E` হলো `std::io::Error`, যেমন `Write` trait-এর এই function-গুলো:

```rust,noplayground
use std::fmt;
use std::io::Error;

pub trait Write {
    fn write(&mut self, buf: &[u8]) -> Result<usize, Error>;
    fn flush(&mut self) -> Result<(), Error>;

    fn write_all(&mut self, buf: &[u8]) -> Result<(), Error>;
    fn write_fmt(&mut self, fmt: fmt::Arguments) -> Result<(), Error>;
}
```

`Result<..., Error>` অনেকবার repeat হয়েছে। যেহেতু, `std::io`-তে এই type alias declaration আছে:

```rust,noplayground
type Result<T> = std::result::Result<T, std::io::Error>;
```

যেহেতু এই declaration-টি `std::io` module-এ আছে, আমরা fully qualified alias `std::io::Result<T>` ব্যবহার করতে পারি; অর্থাৎ, একটি `Result<T, E>` যার `E`-তে `std::io::Error` fill করা। `Write` trait-এর function signature-গুলো শেষে এমন দেখাবে:

```rust,noplayground
pub trait Write {
    fn write(&mut self, buf: &[u8]) -> Result<usize>;
    fn flush(&mut self) -> Result<()>;

    fn write_all(&mut self, buf: &[u8]) -> Result<()>;
    fn write_fmt(&mut self, fmt: fmt::Arguments) -> Result<()>;
}
```

Type alias দুটি উপায়ে সাহায্য করে: এটি code লিখতে সহজ করে _এবং_ এটি সম্পূর্ণ `std::io` জুড়ে একটি consistent interface দেয়। যেহেতু এটি একটি alias, এটি শুধু আরেকটি `Result<T, E>`, যার মানে আমরা `Result<T, E>`-এর উপর কাজ করে এমন যেকোনো method, এবং `?` operator-এর মতো special syntax এর সাথে ব্যবহার করতে পারি।

### The Never Type That Never Returns

Rust-এ `!` নামের একটি special type আছে যাকে type theory-এর ভাষায় _empty type_ বলা হয় কারণ এর কোনো value নেই। আমরা একে _never type_ বলতে পছন্দ করি কারণ এটি এমন একটি function-এর return type-এর জায়গায় দাঁড়ায় যা কখনো return করবে না। এর একটি উদাহরণ নিচে দেওয়া হলো:

```rust,noplayground
fn bar() -> ! {
    // --snip--
}
```

এই code-টি পড়া হয় "function `bar` returns never।" যে function গুলো never return করে তাদের _diverging function_ বলা হয়। আমরা `!` type-এর value তৈরি করতে পারি না, তাই `bar` কখনো return করতে পারে না।

কিন্তু এমন একটি type-এর কী ব্যবহার যার value তুমি কখনো তৈরি করতে পারবে না? Listing 2-5-এর code মনে করো, যা number-guessing game-এর অংশ; আমরা এর একটি অংশ এখানে Listing 20-27-তে পুনরায় দিয়েছি।

<Listing number="20-27" caption="A `match` with an arm that ends in `continue`">

```rust,ignore
        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };
```

</Listing>

সে সময়ে, আমরা এই code-টির কিছু detail এড়িয়ে গিয়েছিলাম। Chapter 6-এর [“The `match`
Control Flow Construct”][the-match-control-flow-construct]<!-- ignore --> section-এ আমরা আলোচনা করেছি যে `match` arm-গুলো সবাই একই type return করতে হবে। সুতরাং, উদাহরণস্বরূপ, নিচের code কাজ করে না:

```rust,ignore,does_not_compile
    let guess = match guess.trim().parse() {
        Ok(_) => 5,
        Err(_) => "hello",
    };
```

এই code-এ `guess`-এর type একটি integer _এবং_ একটি string হতে হবে, এবং Rust চায় যে `guess`-এর শুধুমাত্র একটি type থাকুক। তাহলে, `continue` কী return করে? Listing 20-27-তে কীভাবে আমরা একটি arm থেকে `u32` return করতে পারলাম এবং অন্য একটি arm `continue`-তে শেষ হলো?

তুমি হয়তো অনুমান করেছো, `continue`-এর একটি `!` value আছে। অর্থাৎ, যখন Rust `guess`-এর type compute করে, এটি উভয় match arm দেখে, প্রথমটিতে `u32` value এবং পরেরটিতে `!` value। যেহেতু `!`-এর কখনো value থাকতে পারে না, Rust সিদ্ধান্ত নেয় যে `guess`-এর type `u32`।

এই behavior বর্ণনা করার formal উপায় হলো যে `!` type-এর expression-গুলো অন্য যেকোনো type-এ coerce করা যেতে পারে। আমাদের এই `match` arm `continue` দিয়ে শেষ করার অনুমতি দেওয়া হয়েছে কারণ `continue` কোনো value return করে না; এর বদলে, এটি control loop-এর শীর্ষে ফিরিয়ে দেয়, তাই `Err` case-এ, আমরা কখনো `guess`-এ কোনো value assign করি না।

Never type `panic!` macro-এর সাথেও useful। `Option<T>` value-এর উপর আমরা যে `unwrap` function কল করি তা মনে করো যা একটি value produce করে বা এই definition সহ panic করে:

```rust,ignore
impl<T> Option<T> {
    pub fn unwrap(self) -> T {
        match self {
            Some(val) => val,
            None => panic!("called `Option::unwrap()` on a `None` value"),
        }
    }
}
```

এই code-এ, Listing 20-27-এর `match`-এর মতো একই ঘটনা ঘটে: Rust দেখে যে `val`-এর type `T` এবং `panic!`-এর type `!`, তাই সম্পূর্ণ `match` expression-এর result `T`। এই code কাজ করে কারণ `panic!` কোনো value produce করে না; এটি program শেষ করে। `None` case-এ, আমরা `unwrap` থেকে কোনো value return করব না, তাই এই code valid।

`!` type এর একটি শেষ expression হলো একটি loop:

```rust,ignore
    print!("forever ");

    loop {
        print!("and ever ");
    }
```

এখানে, loop কখনো শেষ হয় না, তাই `!` হলো expression-টির value। তবে, যদি আমরা একটি `break` include করতাম তবে এটি সত্য হতো না, কারণ loop `break`-এ পৌঁছালে terminate হয়ে যেত।

### Dynamically Sized Types and the `Sized` Trait

Rust-কে তার type সম্পর্কে কিছু detail জানতে হবে, যেমন একটি নির্দিষ্ট type-এর value-এর জন্য কতটা space allocate করতে হবে। এটি তার type system-এর একটি কোণকে প্রথমে কিছুটা confusing করে তোলে: _dynamically sized type_-এর concept। কখনো এগুলোকে _DST_ বা _unsized type_ বলা হয়, এই type-গুলো আমাদের এমন value ব্যবহার করে code লিখতে দেয় যার size আমরা শুধুমাত্র runtime-এ জানতে পারি।

চলো `str` নামক একটি dynamically sized type-এর detail-এ ঢুকি, যা আমরা সারা book জুড়ে ব্যবহার করেছি। ঠিক তাই, `&str` নয়, বরং `str` নিজেই একটি DST। অনেক ক্ষেত্রে, যেমন user দ্বারা প্রবেশ করা text store করার সময়, আমরা runtime না হলে string-টি কত দীর্ঘ তা জানতে পারি না। তার মানে আমরা `str` type-এর একটি variable তৈরি করতে পারি না, এবং `str` type-এর একটি argument নিতে পারি না। নিচের code বিবেচনা করো, যা কাজ করে না:

```rust,ignore,does_not_compile
    let s1: str = "Hello there!";
    let s2: str = "How's it going?";
```

Rust-কে জানতে হবে একটি নির্দিষ্ট type-এর যেকোনো value-এর জন্য কতটা memory allocate করতে হবে, এবং একটি type-এর সব value-কে একই পরিমাণ memory ব্যবহার করতে হবে। যদি Rust আমাদের এই code লিখতে allow করতো, তবে এই দুটি `str` value-র একই পরিমাণ space নেওয়া প্রয়োজন হতো। কিন্তু তাদের length ভিন্ন: `s1`-এর 12 byte storage প্রয়োজন এবং `s2`-এর 15। এটিই কারণ যে একটি dynamically sized type ধারণকারী variable তৈরি করা সম্ভব নয়।

তাহলে, আমরা কী করব? এই ক্ষেত্রে, তুমি ইতিমধ্যে উত্তর জানো: আমরা `s1` এবং `s2`-এর type `str`-এর পরিবর্তে string slice (`&str`) করি। Chapter 4-এর [“String Slices”][string-slices]<!-- ignore --> section থেকে মনে করো যে slice data structure শুধু slice-এর starting position এবং length store করে। সুতরাং, যদিও `&T` একটি single value যা `T` যেখানে locate আছে তার memory address store করে, একটি string slice হলো _দুটি_ value: `str`-এর address এবং এর length। যেহেতু, আমরা compile time-এ একটি string slice value-র size জানতে পারি: এটি একটি `usize`-এর length-এর দ্বিগুণ। অর্থাৎ, আমরা সবসময় একটি string slice-এর size জানি, যে string-টি এটি refer করছে তা যত দীর্ঘই হোক না কেন। সাধারণভাবে, এটিই সেই উপায় যাতে Rust-এ dynamically sized type ব্যবহৃত হয়: এদের একটি অতিরিক্ত metadata থাকে যা dynamic information-এর size store করে। Dynamically sized type-এর golden rule হলো আমাদের সবসময় dynamically sized type-এর value-গুলোকে কোনো ধরনের pointer-এর পেছনে রাখতে হবে।

আমরা `str`-কে সব ধরনের pointer-এর সাথে combine করতে পারি: উদাহরণস্বরূপ, `Box<str>` বা `Rc<str>`। আসলে, তুমি এটি আগে দেখেছো কিন্তু একটি ভিন্ন dynamically sized type সহ: trait। প্রতিটি trait একটি dynamically sized type যাকে আমরা trait-টির নাম ব্যবহার করে refer করতে পারি। Chapter 18-এর [“Using Trait Objects to Abstract over
Shared Behavior”][using-trait-objects-to-abstract-over-shared-behavior]<!--
ignore --> section-এ আমরা উল্লেখ করেছি যে trait-গুলোকে trait object হিসেবে ব্যবহার করতে, আমাদের সেগুলোকে একটি pointer-এর পেছনে রাখতে হবে, যেমন `&dyn Trait` বা `Box<dyn
Trait>` (`Rc<dyn Trait>`-ও কাজ করবে)।

DST-গুলোর সাথে কাজ করতে, Rust `Sized` trait provide করে যা নির্ধারণ করে যে একটি type-এর size compile time-এ known কি না। এই trait স্বয়ংক্রিয়ভাবে সব কিছুর জন্য implement করা যার size compile time-এ known। এছাড়াও, Rust implicitly প্রতিটি generic function-এ `Sized`-এ একটি bound যোগ করে। অর্থাৎ, এমন একটি generic function definition:

```rust,ignore
fn generic<T>(t: T) {
    // --snip--
}
```

আসলে এমনভাবে treat করা হয় যেন আমরা এটি লিখেছি:

```rust,ignore
fn generic<T: Sized>(t: T) {
    // --snip--
}
```

ডিফল্টরূপে, generic function গুলো শুধুমাত্র সেই type-গুলোতে কাজ করবে যাদের size compile time-এ known। তবে, তুমি নিম্নলিখিত special syntax ব্যবহার করে এই restriction কমাতে পারো:

```rust,ignore
fn generic<T: ?Sized>(t: &T) {
    // --snip--
}
```

`?Sized`-এ একটি trait bound-এর মানে "`T` হয়তো `Sized` বা নাও হতে পারে," এবং এই notation generic type-গুলোর compile time-এ known size থাকতে হবে এই default-কে override করে। এই অর্থে `?Trait` syntax শুধুমাত্র `Sized`-এর জন্য available, অন্য কোনো trait-এর জন্য নয়।

এটাও খেয়াল করো যে আমরা `t` parameter-এর type `T` থেকে `&T`-তে পরিবর্তন করেছি। যেহেতু type-টি হয়তো `Sized` নয়, আমাদের এটি কোনো ধরনের pointer-এর পেছনে ব্যবহার করতে হবে। এই ক্ষেত্রে, আমরা একটি reference choose করেছি।

এরপর, আমরা function এবং closure নিয়ে কথা বলব!

[encapsulation-that-hides-implementation-details]: ch18-01-what-is-oo.html#encapsulation-that-hides-implementation-details
[string-slices]: ch04-03-slices.html#string-slices
[the-match-control-flow-construct]: ch06-02-match.html#the-match-control-flow-construct
[using-trait-objects-to-abstract-over-shared-behavior]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern

## Method

Method, function-এর মতোই: আমরা এগুলো `fn` keyword আর একটি নাম দিয়ে declare করি, এগুলোর parameter ও return value থাকতে পারে, এবং অন্য কোথাও থেকে method-টি call করলে কিছু কোড চলে। কিন্তু function-এর বিপরীতে, method একটি struct (অথবা enum বা trait object—যেগুলো আমরা যথাক্রমে [Chapter 6][enums]<!-- ignore --> ও [Chapter 18][trait-objects]<!-- ignore -->-এ দেখব)-এর context-এর ভেতরে define করা হয়, আর এদের প্রথম parameter সবসময় `self` থাকে, যা সেই struct-এর instance-কে নির্দেশ করে যার ওপর method-টি call করা হয়েছে।

<!-- Old headings. Do not remove or links may break. -->

<a id="defining-methods"></a>

### Method Syntax

চলো `Rectangle` instance-কে parameter হিসেবে নেওয়া `area` function-টি বদলে সরাসরি `Rectangle` struct-এ define করা একটি `area` method বানাই, যেমন Listing 5-13-তে দেখানো হয়েছে।

<Listing number="5-13" file-name="src/main.rs" caption="`Rectangle` struct-এ একটি `area` method define করা">

```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}

fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };

    println!(
        "The area of the rectangle is {} square pixels.",
        rect1.area()
    );
}
```

</Listing>

`Rectangle`-এর context-এ function-টি define করতে আমরা `Rectangle`-এর জন্য একটি `impl` (implementation) block শুরু করি। এই `impl` block-এর ভেতরের সবকিছু `Rectangle` type-এর সাথে associated হবে। তারপর আমরা `area` function-টিকে `impl`-এর curly brackets-এর ভেতরে নিয়ে যাই এবং signature-এ ও body-তে সর্বত্র প্রথম (এই ক্ষেত্রে একমাত্র) parameter-টিকে `self` করে দিই। `main`-এ আমরা আগে `area` function call করে `rect1` argument পাঠাতাম, এখন তার বদলে আমরা _method syntax_ ব্যবহার করে আমাদের `Rectangle` instance-এ `area` method call করতে পারি। Method syntax একটি instance-এর পরে আসে: আমরা একটি dot, তারপর method-এর নাম, parentheses, এবং প্রয়োজনীয় argument যোগ করি।

`area`-র signature-এ আমরা `rectangle: &Rectangle`-এর বদলে `&self` ব্যবহার করেছি। আসলে `&self` হলো `self: &Self`-এর সংক্ষিপ্ত রূপ। একটি `impl` block-এর ভেতরে `Self` type-টি হলো সেই type-এর alias যার জন্য `impl` block লেখা হয়েছে। Method-এর প্রথম parameter হিসেবে `Self` type-এর একটি `self` নামের parameter থাকতেই হবে, তাই Rust তোমাকে প্রথম parameter-এর জায়গায় শুধু `self` নামটা দিয়েই সংক্ষেপে লেখার সুবিধা দেয়। খেয়াল রাখো, এই method যেন `Self` instance-কে borrow করে সেটা বোঝাতে আমাদের `self` shorthand-এর আগে `&` ব্যবহার করতেই হবে—ঠিক যেমন `rectangle: &Rectangle`-এ করেছিলাম। Method, অন্য যেকোনো parameter-এর মতোই, `self`-এর ownership নিতে পারে, `self`-কে immutably borrow করতে পারে (যেমন এখানে করেছি), অথবা `self`-কে mutably borrow করতে পারে।

এখানে আমরা `&self` ব্যবহার করেছি সেই একই কারণে যে কারণে function version-এ `&Rectangle` ব্যবহার করেছিলাম: আমরা ownership নিতে চাই না, শুধু struct-এর data পড়তে চাই, লিখতে নয়। যদি আমরা চাইতাম যে method call করা instance-টিকে method-এর কাজের অংশ হিসেবে পরিবর্তন করব, তাহলে প্রথম parameter হিসেবে `&mut self` ব্যবহার করতাম। শুধু `self` ব্যবহার করে instance-এর ownership নেওয়া এমন method খুবই কম দেখা যায়; এই কৌশল সাধারণত তখন ব্যবহার করা হয় যখন method `self`-কে অন্য কিছুতে রূপান্তর করে এবং তুমি চাও যে transformation-এর পর caller যেন আর original instance ব্যবহার করতে না পারে।

Function-এর বদলে method ব্যবহারের প্রধান কারণ—method syntax-এর সুবিধা দেওয়া এবং প্রতিটি method-এর signature-এ `self`-এর type বারবার না লিখতে হওয়া ছাড়া—হলো organization। আমরা একটি type-এর instance দিয়ে কী কী করা যায় তা একই `impl` block-এ রাখি, যাতে আমাদের কোড ব্যবহার করবে এমন future user-দের আমাদের লাইব্রেরির বিভিন্ন জায়গায় `Rectangle`-এর ক্ষমতা খুঁজে বের করতে না হয়।

খেয়াল করো যে আমরা চাইলে একটি method-কে struct-এর কোনো field-এর নামের সমান নাম দিতে পারি। যেমন, আমরা `Rectangle`-এ এমন একটি method define করতে পারি যার নামও `width`:

<Listing file-name="src/main.rs">

```rust
impl Rectangle {
    fn width(&self) -> bool {
        self.width > 0
    }
}

fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };

    if rect1.width() {
        println!("The rectangle has a nonzero width; it is {}", rect1.width);
    }
}
```

</Listing>

এখানে আমরা সিদ্ধান্ত নিয়েছি যে `width` method, instance-এর `width` field-এর value `0`-এর বেশি হলে `true` এবং value `0` হলে `false` return করবে: আমরা একই নামের একটি field-কে যেকোনো কাজে একটি method-এর ভেতর ব্যবহার করতে পারি। `main`-এ, যখন আমরা `rect1.width`-এর পরে parentheses যোগ করি, Rust বোঝে যে আমরা `width` method বোঝাচ্ছি। যখন parentheses ব্যবহার করি না, Rust বোঝে যে আমরা `width` field বোঝাচ্ছি।

প্রায়ই—কিন্তু সবসময় নয়—যখন আমরা কোনো method-কে কোনো field-এর নামের সমান নাম দেই, তখন তা শুধু ঐ field-এর value return করে, আর কিছু করে না। এ ধরনের method-কে _getter_ বলা হয়, এবং Rust অন্য কিছু language-এর মতো struct field-এর জন্য স্বয়ংক্রিয়ভাবে getter implement করে না। Getter কাজে লাগে কারণ তুমি field-কে private রেখে method-কে public করতে পারো, ফলে type-এর public API-এর অংশ হিসেবে ঐ field-এ read-only access দেওয়া যায়। আমরা [Chapter 7][public]<!-- ignore -->-এ আলোচনা করব public ও private কী এবং কোনো field বা method-কে কীভাবে public বা private হিসেবে চিহ্নিত করতে হয়।

> ### `->` Operator কোথায়?
>
> C ও C++-এ method call করার জন্য দুটি ভিন্ন operator ব্যবহার করা হয়: তুমি `.` ব্যবহার করো যদি সরাসরি object-এর ওপর method call করো, আর `->` ব্যবহার করো যদি object-এর pointer-এর ওপর method call করো এবং আগে pointer-টি dereference করতে হয়। অর্থাৎ, যদি `object` একটি pointer হয়, `object->something()` হলো `(*object).something()`-এর মতো।
>
> Rust-এ `->` operator-এর কোনো সমতুল্য নেই; বরং Rust-এ _automatic referencing and dereferencing_ নামে একটি feature আছে। Method call করা Rust-এর সেই কয়েকটি জায়গার একটি যেখানে এই behavior দেখা যায়।
>
> এটা কীভাবে কাজ করে: তুমি যখন `object.something()` দিয়ে method call করো, Rust স্বয়ংক্রিয়ভাবে `&`, `&mut`, বা `*` যোগ করে দেয় যাতে `object` method-এর signature-এর সাথে মিলে যায়। অর্থাৎ, নিচের দুটি এক:
>
> <!-- CAN'T EXTRACT SEE BUG https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust
> # #[derive(Debug,Copy,Clone)]
> # struct Point {
> #     x: f64,
> #     y: f64,
> # }
> #
> # impl Point {
> #    fn distance(&self, other: &Point) -> f64 {
> #        let x_squared = f64::powi(other.x - self.x, 2);
> #        let y_squared = f64::powi(other.y - self.y, 2);
> #
> #        f64::sqrt(x_squared + y_squared)
> #    }
> # }
> # let p1 = Point { x: 0.0, y: 0.0 };
> # let p2 = Point { x: 5.0, y: 6.5 };
> p1.distance(&p2);
> (&p1).distance(&p2);
> ```
>
> প্রথমটি অনেক বেশি পরিষ্কার দেখায়। এই automatic referencing behavior কাজ করে কারণ method-এর একটি স্পষ্ট receiver থাকে—`self`-এর type। Receiver ও method-এর নাম দেওয়া থাকলে Rust নিশ্চিতভাবে বুঝতে পারে method-টি read (`&self`), mutate (`&mut self`), নাকি consume (`self`) করছে। Rust method receiver-এর ক্ষেত্রে borrowing implicit করে দেয়—এটিই ownership-কে practice-এ ergonomic করার একটি বড় অংশ।

### আরও Parameter সহ Method

চলো `Rectangle` struct-এ দ্বিতীয় আরেকটি method implement করে method ব্যবহারের অনুশীলন করি। এবার আমরা চাই `Rectangle`-এর একটি instance অন্য একটি `Rectangle` instance নেবে এবং দ্বিতীয় `Rectangle`-টি যদি পুরোপুরি `self`-এর (প্রথম `Rectangle`-এর) ভেতরে ধরে যায় তাহলে `true` return করবে; নাহলে `false` return করবে। অর্থাৎ, `can_hold` method define করার পর আমরা চাই Listing 5-14-তে দেখানো program লিখতে পারি।

<Listing number="5-14" file-name="src/main.rs" caption="এখনও লেখা হয়নি এমন `can_hold` method ব্যবহার করা">

```rust,ignore
fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };
    let rect2 = Rectangle {
        width: 10,
        height: 40,
    };
    let rect3 = Rectangle {
        width: 60,
        height: 45,
    };

    println!("Can rect1 hold rect2? {}", rect1.can_hold(&rect2));
    println!("Can rect1 hold rect3? {}", rect1.can_hold(&rect3));
}
```

</Listing>

প্রত্যাশিত output নিচের মতো হবে, কারণ `rect2`-এর উভয় dimension `rect1`-এর dimension-এর চেয়ে ছোট, কিন্তু `rect3` `rect1`-এর চেয়ে চওড়া:

```text
Can rect1 hold rect2? true
Can rect1 hold rect3? false
```

আমরা জানি একটি method define করতে চাই, তাই সেটি `impl Rectangle` block-এ থাকবে। Method-এর নাম হবে `can_hold`, এবং এটি অন্য একটি `Rectangle`-এর immutable borrow parameter হিসেবে নেবে। Method call করা কোড দেখে আমরা বুঝতে পারি parameter-এর type কী হবে: `rect1.can_hold(&rect2)` যা পাঠায় `&rect2`—অর্থাৎ `rect2`-এর immutable borrow, যেটি একটি `Rectangle` instance। এটা যৌক্তিক, কারণ আমাদের শুধু `rect2` পড়তে হবে (লিখতে নয়—লিখতে হলে mutable borrow লাগত), আর আমরা চাই `main` যেন `rect2`-এর ownership ধরে রাখে যাতে `can_hold` method call করার পরও আমরা `rect2` আবার ব্যবহার করতে পারি। `can_hold`-এর return value হবে Boolean, আর implementation-এ পরীক্ষা করা হবে `self`-এর width ও height যথাক্রমে অন্য `Rectangle`-এর width ও height-এর চেয়ে বড় কিনা। চলো Listing 5-13-এর `impl` block-এ নতুন `can_hold` method যোগ করি, যেমন Listing 5-15-তে দেখানো হয়েছে।

<Listing number="5-15" file-name="src/main.rs" caption="`Rectangle`-এ `can_hold` method implement করা যেটি অন্য একটি `Rectangle` instance কে parameter হিসেবে নেয়">

```rust
impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }

    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }
}
```

</Listing>

Listing 5-14-এর `main` function-এর সাথে এই কোড চালালে আমরা কাঙ্ক্ষিত output পাব। Method `self` parameter-এর পর আরও একাধিক parameter নিতে পারে, এবং সেই parameter-গুলো function-এর parameter-এর মতোই কাজ করে।

### Associated Function

`impl` block-এর ভেতরে define করা সব function-কে _associated function_ বলা হয়, কারণ এগুলো `impl`-এর পরে যে type-এর নাম থাকে তার সাথে associated। আমরা এমন associated function define করতে পারি যাদের প্রথম parameter `self` নয় (ফলে সেগুলো method নয়), কারণ এগুলোর কাজ করার জন্য ঐ type-ের কোনো instance দরকার নেই। আমরা আগে থেকেই এমন একটি function ব্যবহার করেছি: `String::from` function, যেটা `String` type-এ define করা।

Method নয় এমন associated function প্রায়ই constructor হিসেবে ব্যবহার করা হয়, যেগুলো struct-এর একটি নতুন instance return করে। এগুলোর নাম প্রায়ই `new` দেওয়া হয়, কিন্তু `new` কোনো বিশেষ নাম নয় এবং এটি language-এ built-in নয়। যেমন, আমরা `square` নামে একটি associated function দিতে পারি যেটার একটি dimension parameter থাকবে এবং সেটি প্রস্থ ও উচ্চতা উভয় ক্ষেত্রেই ব্যবহার করবে, ফলে একটি বর্গাকার `Rectangle` তৈরি করা সহজ হবে—একই value দুবার উল্লেখ করতে হবে না:

<span class="filename">Filename: src/main.rs</span>

```rust
impl Rectangle {
    fn square(size: u32) -> Self {
        Self {
            width: size,
            height: size,
        }
    }
}
```

Return type-এ ও function body-তে থাকা `Self` keyword-গুলো হলো `impl` keyword-এর পরে থাকা type-টির alias—এই ক্ষেত্রে `Rectangle`।

এই associated function call করতে আমরা struct-এর নামের সাথে `::` syntax ব্যবহার করি; উদাহরণ হিসেবে `let sq = Rectangle::square(3);`। এই function-টি struct দ্বারা namespaced: `::` syntax associated function আর module দ্বারা তৈরি namespace—উভয়ের জন্যই ব্যবহৃত হয়। Module নিয়ে আমরা আলোচনা করব [Chapter 7][modules]<!-- ignore -->-এ।

### Multiple `impl` Block

প্রতিটি struct-এর জন্য একাধিক `impl` block থাকতে পারে। যেমন, Listing 5-15-এর সাথে Listing 5-16-এর কোড সমতুল্য, যেখানে প্রতিটি method আলাদা `impl` block-এ আছে।

<Listing number="5-16" caption="Listing 5-15-কে একাধিক `impl` block ব্যবহার করে পুনরায় লেখা">

```rust
impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}

impl Rectangle {
    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }
}
```

</Listing>

এখানে এই method-গুলোকে একাধিক `impl` block-এ ভাগ করার কোনো কারণ নেই, কিন্তু এটি valid syntax। Chapter 10-তে, যেখানে আমরা generic type ও trait নিয়ে আলোচনা করব, সেখানে এমন একটি ক্ষেত্রে দেখব যেখানে একাধিক `impl` block কাজে লাগে।

## Summary

Struct তোমাকে এমন custom type তৈরি করতে দেয় যা তোমার domain-এর জন্য অর্থবহ। Struct ব্যবহার করে তুমি সম্পর্কিত data-এর অংশগুলোকে একসাথে যুক্ত রাখতে পারো এবং প্রতিটি অংশের নাম দিয়ে কোড পরিষ্কার করতে পারো। `impl` block-এ তুমি তোমার type-এর সাথে associated function define করতে পারো, আর method হলো এমন এক ধরনের associated function যা তোমার struct-এর instance-এর behavior নির্দিষ্ট করতে দেয়।

কিন্তু custom type তৈরি করার একমাত্র উপায় struct নয়: চলো এবার Rust-এর enum feature-এ ফিরে যাই, যাতে তোমার toolbox-এ আরেকটি tool যোগ হয়।

[enums]: ch06-00-enums.html
[trait-objects]: ch18-02-trait-objects.md
[public]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html

<!-- Old headings. Do not remove or links may break. -->

<a id="using-trait-objects-that-allow-for-values-of-different-types"></a>

## Trait Object ব্যবহার করে Shared Behavior-এর ওপর Abstraction

Chapter 8-এ আমরা উল্লেখ করেছিলাম যে vector-গুলোর একটি limitation হলো—এরা শুধুমাত্র এক ধরনের element store করতে পারে। Listing 8-9-এ আমরা একটি workaround তৈরি করেছিলাম যেখানে আমরা `SpreadsheetCell` enum define করেছিলাম যার variant-এ integer, float এবং text রাখা যেত। এর ফলে প্রতিটি cell-এ ভিন্ন ধরনের data রাখা সত্ত্বেও আমরা একটি vector পেতাম যা একটি সারির cell-কে represent করত। যখন আমাদের interchangeable item গুলো একটি fixed set of type হবে, যা আমরা code compile-এর সময় জানি—তখন এটি একদম মোটা মোটা একটি ভালো সমাধান।

তবে মাঝে মাঝে আমরা চাই আমাদের library ব্যবহারকারী নির্দিষ্ট পরিস্থিতিতে valid type-গুলোর set-কে বাড়াতে পারে। কীভাবে এটা করা যেতে পারে তা দেখাতে আমরা একটি graphical user interface (GUI) tool-এর উদাহরণ তৈরি করবো, যা item-গুলোর একটি list-এর ওপর iterate করবে এবং প্রতিটির ওপর `draw` method call করে সেটিকে screen-এ draw করবে—GUI tool-গুলোর জন্য একটি সাধারণ পদ্ধতি। আমরা `gui` নামের একটি library crate তৈরি করবো যেখানে একটি GUI library-এর structure থাকবে। এই crate-এ মানুষের ব্যবহারের জন্য কিছু type থাকতে পারে, যেমন `Button` বা `TextField`। তাছাড়া `gui` ব্যবহারকারীরা নিজেদের type তৈরি করতে চাইবে যেগুলো draw করা যাবে: যেমন একজন programmer একটি `Image` যোগ করতে পারেন, অন্যজন একটি `SelectBox` যোগ করতে পারেন।

library লেখার সময় আমরা জানি না এবং define করতে পারি না অন্যান্য programmer-রা কী কী type তৈরি করতে চাইবেন। কিন্তু এটা জানি যে `gui`-কে ভিন্ন ভিন্ন type-এর অনেকগুলো value track করে রাখতে হবে এবং সেই ভিন্ন type-এর প্রতিটি value-র ওপর `draw` method call করতে হবে। এটার দরকার নেই যে `draw` method call করলে ঠিক কী হবে তা জানবে—শুধু জানলেই চলবে যে ঐ value-তে সেই method আমরা call করার জন্য পাবো।

inheritance সম্বলিত কোনো ভাষায় এটা করতে হলে আমরা একটি `Component` নামের class define করতে পারতাম যার ওপর `draw` নামের একটি method থাকবে। অন্যান্য class, যেমন `Button`, `Image` এবং `SelectBox`, সেই `Component` থেকে inherit করবে এবং এভাবে `draw` method-ও inherit করবে। তারা প্রত্যেকে নিজ নিজ custom behavior define করার জন্য `draw` method-কে override করতে পারতো, কিন্তু framework সব type-কে `Component` instance-এর মতো করে দেখে তাদের ওপর `draw` call করতে পারবে। কিন্তু যেহেতু Rust-এ inheritance নেই, তাই user-দের নতুন type তৈরি করে সেগুলো library-র সাথে compatible করার জন্য আমাদের `gui` library-কে অন্যভাবে structure করতে হবে।

### Common Behavior-এর জন্য একটি Trait Define করা

যে behavior আমরা `gui`-তে চাই তা implement করতে আমরা `Draw` নামের একটি trait define করবো যার একটি `draw` নামের method থাকবে। এরপর আমরা এমন একটি vector define করতে পারবো যা একটি trait object নেয়। একটি _trait object_ দুটি জিনিসকে point করে—আমাদের নির্দিষ্ট করা trait implement করা একটি type-এর instance, এবং runtime-এ সেই type-এর trait method lookup করার জন্য ব্যবহৃত একটি table। আমরা একটি trait object তৈরি করি কোনো pointer (যেমন একটি reference বা `Box<T>` smart pointer) উল্লেখ করে, তারপর `dyn` keyword এবং তারপর প্রাসঙ্গিক trait উল্লেখ করে। (কেন trait object-কে অবশ্যই pointer ব্যবহার করতে হয় তা আমরা Chapter 20-এর [“Dynamically Sized Types and the `Sized` Trait”][dynamically-sized]<!-- ignore --> section-এ আলোচনা করবো।) আমরা trait object কে কোনো generic বা concrete type-এর জায়গায় ব্যবহার করতে পারি। যেখানেই trait object ব্যবহার করবো, Rust-এর type system compile time-এ নিশ্চিত করবে যে সেই context-এ ব্যবহৃত যেকোনো value trait object-এর trait implement করেছে। ফলে আমাদের compile time-এ সব সম্ভাব্য type জানার দরকার নেই।

আমরা উল্লেখ করেছি যে Rust-এ আমরা struct এবং enum-কে অন্যান্য ভাষার object থেকে আলাদা করার জন্য "object" বলি না। একটি struct বা enum-এ struct field-এর data এবং `impl` block-এর behavior আলাদা থাকে, অন্যদিকে অন্য ভাষায় data এবং behavior একত্রে একটি ধারণায় থাকলে তাকে প্রায়ই object বলা হয়। Trait object অন্য ভাষার object থেকে এই দিক দিয়ে আলাদা যে trait object-এ আমরা data যোগ করতে পারি না। Trait object অন্য ভাষার object-এর মতো সাধারণ কাজে ততটা কাজে লাগে না: এদের নির্দিষ্ট উদ্দেশ্য হলো common behavior-এর ওপর abstraction-এর সুযোগ দেওয়া।

Listing 18-3-এ দেখানো হয়েছে কীভাবে `Draw` নামের একটি trait define করতে হয় যার একটি `draw` নামের method আছে।

<Listing number="18-3" file-name="src/lib.rs" caption="`Draw` trait-এর definition">

```rust,noplayground
pub trait Draw {
    fn draw(&self);
}
```

</Listing>

এই syntax তোমার পরিচিত মনে হওয়ার কথা, কারণ Chapter 10-এ trait define করার সময় এটা নিয়ে আলোচনা করেছি। এরপর আসে কিছু নতুন syntax: Listing 18-4 `Screen` নামের একটি struct define করে যা `components` নামের একটি vector রাখে। এই vector-টি `Box<dyn Draw>` type-এর, যা একটি trait object; এটি `Box`-এর ভেতরে থাকা যেকোনো type-এর জায়গায় বসে যা `Draw` trait implement করে।

<Listing number="18-4" file-name="src/lib.rs" caption="`Screen` struct-এর definition, যার `components` field-এ `Draw` trait implement করা trait object-গুলোর একটি vector থাকে">

```rust,noplayground
pub struct Screen {
    pub components: Vec<Box<dyn Draw>>,
}
```

</Listing>

`Screen` struct-এর ওপর আমরা `run` নামের একটি method define করবো যা তার প্রতিটি `components`-এর ওপর `draw` method call করবে, যেমনটা Listing 18-5-তে দেখানো হয়েছে।

<Listing number="18-5" file-name="src/lib.rs" caption="`Screen`-এর ওপর একটি `run` method যা প্রতিটি component-এর ওপর `draw` method call করে">

```rust,noplayground
impl Screen {
    pub fn run(&self) {
        for component in self.components.iter() {
            component.draw();
        }
    }
}
```

</Listing>

এটি এমন একটি struct define করার থেকে ভিন্নভাবে কাজ করে যা trait bound সহ একটি generic type parameter ব্যবহার করে। Generic type parameter একই সময়ে শুধুমাত্র একটি concrete type দিয়ে substitute করা যায়, অন্যদিকে trait object runtime-এ একাধিক concrete type-কে trait object-এর জায়গায় বসতে দেয়। উদাহরণ হিসেবে আমরা `Screen` struct define করতে পারতাম generic type এবং trait bound দিয়ে, যেমন Listing 18-6-তে দেখানো হয়েছে।

<Listing number="18-6" file-name="src/lib.rs" caption="Generics এবং trait bound ব্যবহার করে `Screen` struct ও তার `run` method-এর বিকল্প implementation">

```rust,noplayground
pub struct Screen<T: Draw> {
    pub components: Vec<T>,
}

impl<T> Screen<T>
where
    T: Draw,
{
    pub fn run(&self) {
        for component in self.components.iter() {
            component.draw();
        }
    }
}
```

</Listing>

এটি আমাদের এমন একটি `Screen` instance পর্যন্ত সীমাবদ্ধ রাখবে যেখানে component-গুলোর list সবাই `Button` type-এর হবে বা সবাই `TextField` type-এর হবে। যদি তোমার শুধু homogeneous collection থাকে, তাহলে generic এবং trait bound ব্যবহার করা ভালো, কারণ definition গুলো compile time-এ concrete type ব্যবহার করার জন্য monomorphize হবে।

অন্যদিকে trait object ব্যবহার করা method-এ একটি `Screen` instance `Vec<T>` ধারণ করতে পারে যার ভেতরে একটি `Box<Button>` ও একটি `Box<TextField>` একসাথে থাকতে পারে। চলো দেখি এটি কীভাবে কাজ করে, এরপর আলোচনা করবো runtime performance-এ এর প্রভাব কী।

### Trait Implement করা

এখন আমরা কিছু type যোগ করবো যেগুলো `Draw` trait implement করবে। আমরা `Button` type দেবো। আবারও বলছি—একটি সম্পূর্ণ GUI library implement করা এই book-এর scope-এর বাইরে, তাই `draw` method-এর body-তে কোনো কাজের implementation থাকবে না। এমন হতে পারে তা কল্পনা করতে একটি `Button` struct-এর field হিসেবে `width`, `height` এবং `label` থাকতে পারে, যেমনটা Listing 18-7-তে দেখানো হয়েছে।

<Listing number="18-7" file-name="src/lib.rs" caption="একটি `Button` struct যা `Draw` trait implement করে">

```rust,noplayground
pub struct Button {
    pub width: u32,
    pub height: u32,
    pub label: String,
}

impl Draw for Button {
    fn draw(&self) {
        // code to actually draw a button
    }
}
```

</Listing>

`Button`-এর `width`, `height` এবং `label` field গুলো অন্যান্য component-এর field থেকে আলাদা হবে; যেমন একটি `TextField` type-এ এই field গুলোর সাথে একটি `placeholder` field-ও থাকতে পারে। screen-এ যেসব type আমরা draw করতে চাই প্রত্যেকটি `Draw` trait implement করবে কিন্তু `draw` method-এ ভিন্ন code ব্যবহার করে নির্ধারণ করবে কীভাবে সেই নির্দিষ্ট type-কে draw করা হবে, যেমন `Button` করেছে এখানে (আগে যেমন বলা হয়েছে তা ছাড়া আসল GUI code নেই)। `Button` type-এর হয়তো আরও একটি `impl` block থাকতে পারে যেখানে user যখন button-এ click করে তখন কী হবে তার সাথে সম্পর্কিত method থাকবে। এ ধরনের method `TextField`-এর মতো type-এর ক্ষেত্রে খাটবে না।

আমাদের library ব্যবহার করে কেউ যদি `width`, `height` এবং `options` field বিশিষ্ট একটি `SelectBox` struct implement করতে চায়, তবে তাকে `SelectBox` type-এর ওপরও `Draw` trait implement করতে হবে, যেমন Listing 18-8-তে দেখানো হয়েছে।

<Listing number="18-8" file-name="src/main.rs" caption="অন্য একটি crate `gui` ব্যবহার করছে এবং একটি `SelectBox` struct-এর ওপর `Draw` trait implement করছে">

```rust,ignore
use gui::Draw;

struct SelectBox {
    width: u32,
    height: u32,
    options: Vec<String>,
}

impl Draw for SelectBox {
    fn draw(&self) {
        // code to actually draw a select box
    }
}
```

</Listing>

এখন আমাদের library-র user তার `main` function লিখতে পারে একটি `Screen` instance তৈরি করতে। সেই `Screen` instance-এ সে একটি `SelectBox` এবং একটি `Button` যোগ করতে পারে—প্রতিটিকে একটি `Box<T>`-এ রেখে trait object বানিয়ে। তারপর সে `Screen` instance-এর ওপর `run` method call করতে পারে, যা প্রতিটি component-এর ওপর `draw` call করবে। Listing 18-9 এই implementation দেখায়।

<Listing number="18-9" file-name="src/main.rs" caption="Trait object ব্যবহার করে একই trait implement করা ভিন্ন type-এর value store করা">

```rust,ignore
use gui::{Button, Screen};

fn main() {
    let screen = Screen {
        components: vec![
            Box::new(SelectBox {
                width: 75,
                height: 10,
                options: vec![
                    String::from("Yes"),
                    String::from("Maybe"),
                    String::from("No"),
                ],
            }),
            Box::new(Button {
                width: 50,
                height: 10,
                label: String::from("OK"),
            }),
        ],
    };

    screen.run();
}
```

</Listing>

আমরা যখন library লিখেছিলাম তখন জানতাম না যে কেউ `SelectBox` type যোগ করতে পারে, কিন্তু আমাদের `Screen` implementation সেই নতুন type-এর ওপর কাজ করতে পেরে সেটিকে draw করেছে—কারণ `SelectBox` যেহেতু `Draw` trait implement করেছে, তাই সে `draw` method implement করেছে।

একটি value-র প্রতি সে কোন message-এ সাড়া দেয় সেদিকে নজর দেওয়া, কিন্তু value-টির concrete type-কে নয়—এই ধারণাটি dynamically typed language-গুলোর _duck typing_ ধারণার মতো: যদি হাঁটাচলা হাঁসের মতো হয় এবং ডাক ডাকছে হাঁসের মতো, তাহলে সেটি অবশ্যই হাঁস! Listing 18-5-তে `Screen`-এর ওপর `run`-এর implementation-এ, `run`-কে জানতে হয় না প্রতিটি component-এর concrete type কী। সে check করে না যে কোনো component `Button` নাকি `SelectBox`-এর instance, সে শুধু component-টির ওপর `draw` method call করে। `components` vector-এর value-গুলোর type হিসেবে `Box<dyn Draw>` উল্লেখ করার মাধ্যমে আমরা `Screen`-কে এমনভাবে define করেছি যেন সে এমন value চায় যার ওপর আমরা `draw` method call করতে পারি।

duck typing ব্যবহার করা code-এর মতো করে code লেখার জন্য trait object এবং Rust-এর type system ব্যবহার করার সুবিধা হলো—আমাদের কখনো runtime-এ check করতে হয় না যে কোনো value নির্দিষ্ট method implement করেছে কি না, বা value যদি method implement না করে থাকে তবু আমরা call করে ফেলি আর error পাবো এই চিন্তা করতে হয় না। value গুলো trait object-এর প্রয়োজনীয় trait implement না করলে Rust আমাদের code compile-ই করবে না।

যেমন Listing 18-10 দেখায় যদি আমরা একটি `String`-কে component হিসেবে দিয়ে `Screen` তৈরি করার চেষ্টা করি তখন কী হয়।

<Listing number="18-10" file-name="src/main.rs" caption="এমন একটি type ব্যবহার করার চেষ্টা যা trait object-এর trait implement করে না">

```rust,ignore,does_not_compile
use gui::Screen;

fn main() {
    let screen = Screen {
        components: vec![Box::new(String::from("Hi"))],
    };

    screen.run();
}
```

</Listing>

যেহেতু `String` `Draw` trait implement করে না, তাই আমরা এই error পাবো:

```console
$ cargo run
   Compiling gui v0.1.0 (file:///projects/gui)
error[E0277]: the trait bound `String: Draw` is not satisfied
  --> src/main.rs:5:26
   |
 5 |         components: vec![Box::new(String::from("Hi"))],
   |                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ the trait `Draw` is not implemented for `String`
   |
help: the trait `Draw` is implemented for `Button`
  --> src/lib.rs:23:1
   |
23 | impl Draw for Button {
   | ^^^^^^^^^^^^^^^^^^^^
   = note: required for the cast from `Box<String>` to `Box<dyn Draw>`

For more information about this error, try `rustc --explain E0277`.
error: could not compile `gui` (bin "gui") due to 1 previous error
```

এই error থেকে আমরা জানতে পারি—হয় আমরা `Screen`-কে এমন কিছু পাস করছি যা পাস করার ইচ্ছা ছিল না, তাই অন্য type পাস করা উচিত; অথবা আমাদের `String`-এর ওপর `Draw` implement করা উচিত যাতে `Screen` তার ওপর `draw` call করতে পারে।

<!-- Old headings. Do not remove or links may break. -->

<a id="trait-objects-perform-dynamic-dispatch"></a>

### Dynamic Dispatch সম্পাদন

Chapter 10-এর [“Performance of Code Using Generics”][performance-of-code-using-generics]<!-- ignore --> section-এ আমরা যে আলোচনা করেছিলাম তা মনে করো—compiler generic-গুলোর ওপর যে monomorphization process সম্পাদন করে: compiler generic type parameter-এর জায়গায় আমরা যে প্রতিটি concrete type ব্যবহার করি তার জন্য function এবং method-এর nongeneric implementation তৈরি করে। Monomorphization-এর ফলে যে code পাওয়া যায় তা _static dispatch_ সম্পাদন করে, যেখানে compiler compile time-ই জানে তুমি কোন method call করছো। এর বিপরীতে হলো _dynamic dispatch_, যেখানে compiler compile time-এ বলতে পারে না তুমি কোন method call করছো। Dynamic dispatch-এর ক্ষেত্রে compiler এমন code তৈরি করে যা runtime-এ জানতে পারবে কোন method-কে call করতে হবে।

Trait object ব্যবহার করলে Rust-কে অবশ্যই dynamic dispatch ব্যবহার করতে হবে। Compiler জানে না trait object ব্যবহার করা code-টির সাথে কোন কোন type ব্যবহার হতে পারে, তাই সে জানে না কোন type-এর ওপর implement করা কোন method-কে call করতে হবে। তার বদলে runtime-এ Rust trait object-এর ভেতরের pointer গুলো ব্যবহার করে জানে কোন method-কে call করতে হবে। এই lookup-এর একটি runtime cost আছে যা static dispatch-এ থাকে না। Dynamic dispatch compiler-কে কোনো method-এর code inline করতে বারণ করে, যার ফলে কিছু optimization বাধাগ্রস্ত হয়, এবং Rust-এর কিছু নিয়ম আছে কোথায় dynamic dispatch ব্যবহার করা যাবে আর কোথায় নয়, যাকে _dyn compatibility_ বলা হয়। সেই নিয়ম গুলো এই আলোচনার scope-এর বাইরে, তবে তুমি সেগুলো সম্পর্কে [reference-এ][dyn-compatibility]<!-- ignore --> আরও পড়তে পারো। তবে আমরা Listing 18-5-এ লেখা code-এ অতিরিক্ত flexibility পেয়েছি এবং Listing 18-9-এ যে support পেয়েছি, তাই এটি একটি বিবেচনা করতে হবে এমন trade-off।

[performance-of-code-using-generics]: ch10-01-syntax.html#performance-of-code-using-generics
[dynamically-sized]: ch20-03-advanced-types.html#dynamically-sized-types-and-the-sized-trait
[dyn-compatibility]: https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility

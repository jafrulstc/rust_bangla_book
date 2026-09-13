## `RefCell<T>` এবং Interior Mutability Pattern

_interior mutability_ হলো Rust-এর একটি design pattern যা তোমাকে data mutate করতে দেয় এমনকি যখন সেই data-এর immutable reference থাকে; সাধারণত, borrowing rule অনুযায়ী এই কাজটি disallowed। data mutate করতে এই pattern একটি data structure-এর ভেতরে `unsafe` code ব্যবহার করে যাতে mutation এবং borrowing নিয়ন্ত্রণকারী Rust-এর স্বাভাবিক rule গুলো এড়ানো যায়। unsafe code compiler-কে ইঙ্গিত করে যে আমরা rule গুলো manually যাচাই করছি compiler-এর উপর নির্ভর না করে; আমরা unsafe code সম্পর্কে Chapter 20-তে আরও আলোচনা করব।

আমরা interior mutability pattern ব্যবহার করে এমন type ব্যবহার করতে পারি শুধুমাত্র যখন আমরা নিশ্চিত করতে পারি যে borrowing rule গুলো runtime-এ অনুসরণ করা হবে, যদিও compiler সেটা guarantee করতে পারে না। জড়িত `unsafe` code-টিকে তারপর একটি safe API-তে wrap করা হয়, এবং বাইরের type-টি এখনো immutable।

চলো interior mutability pattern অনুসরণ করে এমন `RefCell<T>` type দেখে এই ধারণাটি বোঝা যাক।

<!-- Old headings. Do not remove or links may break. -->

<a id="enforcing-borrowing-rules-at-runtime-with-refcellt"></a>

### Runtime-এ Borrowing Rule Enforce করা

`Rc<T>`-এর বিপরীতে, `RefCell<T>` type তার ধারণ করা data-এর single ownership বোঝায়। তাহলে, `Box<T>`-এর মতো type থেকে `RefCell<T>` আলাদা কী করে? Chapter 4-এ তুমি যে borrowing rule গুলো শিখেছ সেগুলো মনে করো:

- যেকোনো সময়, তোমার কাছে _হয়_ একটি mutable reference অথবা যেকোনো সংখ্যক immutable reference থাকতে পারে (কিন্তু দুটোই নয়)।
- Reference সবসময় valid হতে হবে।

reference এবং `Box<T>` এর সাথে, borrowing rule-গুলোর invariant compile time-এ enforce করা হয়। `RefCell<T>`-এর সাথে, এই invariant-গুলো _runtime-এ_ enforce করা হয়। reference-এর সাথে, তুমি এই rule গুলো ভাঙলে একটি compiler error পাবে। `RefCell<T>`-এর সাথে, তুমি এই rule গুলো ভাঙলে তোমার program panic করবে এবং বেরিয়ে যাবে।

compile time-এ borrowing rule যাচাই করার সুবিধা হলো error গুলো development process-এ তাড়াতাড়ি ধরা পড়বে, এবং runtime performance-এ কোনো প্রভাব পড়বে না কারণ সব analysis আগেই সম্পন্ন হয়ে যায়। সেই কারণে, বেশিরভাগ ক্ষেত্রে compile time-এ borrowing rule যাচাই করাই সেরা পছন্দ, যে কারণে এটি Rust-এর default।

এর বদলে runtime-এ borrowing rule যাচাই করার সুবিধা হলো তখন কিছু memory-safe scenario allowed হয়, যেগুলো compile-time check দ্বারা disallowed হতো। Static analysis, যেমন Rust compiler, স্বভাবতই conservative। Code-এর কিছু property code analyze করে শনাক্ত করা অসম্ভব: সবচেয়ে বিখ্যাত উদাহরণ হলো Halting Problem, যা এই book-এর scope-এর বাইরে কিন্তু research করার মতো একটি interesting topic।

যেহেতু কিছু analysis অসম্ভব, যদি Rust compiler নিশ্চিত হতে না পারে যে code ownership rule মেনে চলে, তবে এটি হয়তো একটি সঠিক program reject করবে; এইভাবে এটি conservative। যদি Rust একটি ভুল program accept করে, user-রা Rust-এর দেওয়া guarantee-এ বিশ্বাস করতে পারত না। তবে, যদি Rust একটি সঠিক program reject করে, programmer অসুবিধায় পড়বে, কিন্তু কোনো বিপর্যয় ঘটবে না। `RefCell<T>` type তখন কাজে লাগে যখন তুমি নিশ্চিত যে তোমার code borrowing rule মেনে চলে কিন্তু compiler সেটা বুঝতে পারছে না এবং guarantee করতে পারছে না।

`Rc<T>`-এর মতো, `RefCell<T>` শুধুমাত্র single-threaded scenario-তে ব্যবহারের জন্য এবং তুমি multithreaded context-এ এটি ব্যবহার করার চেষ্টা করলে একটি compile-time error দেবে। আমরা Chapter 16-তে কীভাবে একটি multithreaded program-এ `RefCell<T>`-এর functionality পেতে হয় তা নিয়ে আলোচনা করব।

এখানে `Box<T>`, `Rc<T>`, অথবা `RefCell<T>` বেছে নেওয়ার কারণ গুলোর একটি recap দেওয়া হলো:

- `Rc<T>` একই data-এর একাধিক owner সক্ষম করে; `Box<T>` এবং `RefCell<T>`-এর single owner থাকে।
- `Box<T>` immutable অথবা mutable borrow করতে দেয় যা compile time-এ check করা হয়; `Rc<T>` শুধুমাত্র immutable borrow করতে দেয় যা compile time-এ check করা হয়; `RefCell<T>` immutable অথবা mutable borrow করতে দেয় যা runtime-এ check করা হয়।
- যেহেতু `RefCell<T>` mutable borrow করতে দেয় যা runtime-এ check করা হয়, তুমি `RefCell<T>` immutable হলেও এর ভেতরের value mutate করতে পারো।

একটি immutable value-এর ভেতরের value mutate করাই হলো interior mutability pattern। চলো এমন একটি পরিস্থিতি দেখি যেখানে interior mutability কাজে লাগে এবং কীভাবে এটি সম্ভব তা পরীক্ষা করি।

<!-- Old headings. Do not remove or links may break. -->

<a id="interior-mutability-a-mutable-borrow-to-an-immutable-value"></a>

### Interior Mutability ব্যবহার করা

borrowing rule-গুলোর একটি পরিণতি হলো যখন তোমার কাছে একটি immutable value থাকে, তুমি সেটিকে mutably borrow করতে পারো না। উদাহরণস্বরূপ, এই code compile হবে না:

```rust,ignore,does_not_compile
fn main() {
    let x = 5;
    let y = &mut x;
}
```

এই code compile করার চেষ্টা করলে তুমি নিচের error পাবে:

```console
$ cargo run
   Compiling borrowing v0.1.0 (file:///projects/borrowing)
error[E0596]: cannot borrow `x` as mutable, as it is not declared as mutable
 --> src/main.rs:3:13
  |
3 |     let y = &mut x;
  |             ^^^^^^ cannot borrow as mutable
  |
help: consider changing this to be mutable
  |
2 |     let mut x = 5;
  |         +++

For more information about this error, try `rustc --explain E0596`.
error: could not compile `borrowing` (bin "borrowing") due to 1 previous error
```

তবে, এমন পরিস্থিতি আছে যেখানে একটি value-এর নিজের method-এ নিজেকে mutate করা কাজের হবে কিন্তু অন্য code-এর কাছে immutable মনে হবে। value-টির method-এর বাইরের code সেই value-টিকে mutate করতে পারবে না। `RefCell<T>` ব্যবহার করা হলো interior mutability পাওয়ার একটি উপায়, কিন্তু `RefCell<T>` borrowing rule গুলো সম্পূর্ণভাবে এড়ায় না: compiler-এর borrow checker এই interior mutability কে allow করে, এবং borrowing rule-গুলো এর বদলে runtime-এ check করা হয়। তুমি rule গুলো লঙ্ঘন করলে, তুমি compiler error-এর বদলে একটি `panic!` পাবে।

চলো এমন একটি practical উদাহরণ দেখি যেখানে আমরা `RefCell<T>` ব্যবহার করে একটি immutable value mutate করতে পারি এবং দেখি কেন সেটি কাজের।

<!-- Old headings. Do not remove or links may break. -->

<a id="a-use-case-for-interior-mutability-mock-objects"></a>

#### Mock Object দিয়ে Testing

কখনো কখনো testing-এর সময় একজন programmer অন্য একটি type-এর জায়গায় একটি type ব্যবহার করবে, নির্দিষ্ট behavior পর্যবেক্ষণ করতে এবং assert করতে যে এটি সঠিকভাবে implement করা হয়েছে। এই placeholder type-টিকে _test double_ বলা হয়। চলচ্চ্রিত্র নির্মাণে stunt double-এর মতো ভাবতে পারো, যেখানে একজন ব্যক্তি এসে একজন actor-এর স্থান নেয় বিশেষ কঠিন দৃশ্য করতে। test double গুলো অন্য type-এর স্থান নেয় যখন আমরা test চালাই। _Mock object_ হলো test double-এর নির্দিষ্ট ধরন যা test-এর সময় কী ঘটে তা record করে যাতে তুমি assert করতে পারো যে সঠিক action গুলো ঘটেছে।

Rust-এ অন্যান্য language-এর মতো object নেই, এবং Rust-এ standard library-তে অন্যান্য কিছু language-এর মতো built-in mock object functionality নেই। তবে, তুমি অবশ্যই এমন একটি struct তৈরি করতে পারো যা একটি mock object-এর উদ্দেশ্য পূরণ করবে।

এখানে এমন পরিস্থিতি যা আমরা test করব: আমরা এমন একটি library তৈরি করব যা একটি value-কে একটি maximum value-এর সাপেক্ষে track করে এবং current value maximum value-এর কতটা কাছাকাছি তার উপর ভিত্তি করে message পাঠায়। এই library ব্যবহার করা যেতে পারে একজন user-কে কতগুলো API call allow করা হয় তার quota track রাখতে, উদাহরণস্বরূপ।

আমাদের library শুধু maximum-এর কাছাকাছি একটি value কতটা কাছাকাছি তা track করার functionality এবং কোন সময়ে কী message হওয়া উচিত তা provide করবে। আমাদের library ব্যবহার করা application-গুলো থেকে message পাঠানোর mechanism provide করা আশা করা হবে: application টি message-টি সরাসরি user-কে দেখাতে পারে, একটি email পাঠাতে পারে, একটি text message পাঠাতে পারে, অথবা অন্য কিছু করতে পারে। library-কে সেই detail জানতে হবে না। তার যা দরকার তা হলো এমন কিছু যা আমরা provide করা একটি trait implement করে, যার নাম `Messenger`। Listing 15-20 library code দেখায়।

<Listing number="15-20" file-name="src/lib.rs" caption="A library to keep track of how close a value is to a maximum value and warn when the value is at certain levels">

```rust,noplayground
pub trait Messenger {
    fn send(&self, msg: &str);
}

pub struct LimitTracker<'a, T: Messenger> {
    messenger: &'a T,
    value: usize,
    max: usize,
}

impl<'a, T> LimitTracker<'a, T>
where
    T: Messenger,
{
    pub fn new(messenger: &'a T, max: usize) -> LimitTracker<'a, T> {
        LimitTracker {
            messenger,
            value: 0,
            max,
        }
    }

    pub fn set_value(&mut self, value: usize) {
        self.value = value;

        let percentage_of_max = self.value as f64 / self.max as f64;

        if percentage_of_max >= 1.0 {
            self.messenger.send("Error: You are over your quota!");
        } else if percentage_of_max >= 0.9 {
            self.messenger
                .send("Urgent warning: You've used up over 90% of your quota!");
        } else if percentage_of_max >= 0.75 {
            self.messenger
                .send("Warning: You've used up over 75% of your quota!");
        }
    }
}
```

</Listing>

এই code-এর একটি গুরুত্বপূর্ণ অংশ হলো `Messenger` trait-এ `send` নামের একটি method আছে যা `self`-এর একটি immutable reference এবং message-এর text নেয়। এই trait-টি হলো সেই interface যা আমাদের mock object implement করবে যাতে mock টিকে একটি আসল object-এর মতোই ব্যবহার করা যায়। আরেকটি গুরুত্বপূর্ণ অংশ হলো আমরা `LimitTracker`-এর `set_value` method-এর behavior test করতে চাই। আমরা `value` parameter-এর জন্য যা pass করি তা পরিবর্তন করতে পারি, কিন্তু `set_value` assertion করার জন্য কিছু return করে না। আমরা চাই বলতে পারি যে আমরা যদি `Messenger` trait implement করে এমন কিছু এবং `max`-এর জন্য একটি নির্দিষ্ট value দিয়ে একটি `LimitTracker` তৈরি করি, তাহলে আমরা `value`-এর জন্য ভিন্ন ভিন্ন number pass করলে messenger-কে appropriate message পাঠাতে বলা হয়।

আমাদের এমন একটি mock object দরকার যা আমরা `send` call করলে email বা text message পাঠানোর বদলে শুধু যে message গুলো পাঠাতে বলা হয়েছে সেগুলো track রাখবে। আমরা mock object-এর একটি নতুন instance তৈরি করতে পারি, mock object ব্যবহার করে একটি `LimitTracker` তৈরি করতে পারি, `LimitTracker`-এ `set_value` method call করতে পারি, এবং তারপর check করতে পারি যে mock object-এ আমাদের প্রত্যাশিত message গুলো আছে কি না। Listing 15-21 একটি mock object implement করার একটি চেষ্টা দেখায়, কিন্তু borrow checker এটিকে allow করবে না।

<Listing number="15-21" file-name="src/lib.rs" caption="An attempt to implement a `MockMessenger` that isn’t allowed by the borrow checker">

```rust,ignore,does_not_compile
#[cfg(test)]
mod tests {
    use super::*;

    struct MockMessenger {
        sent_messages: Vec<String>,
    }

    impl MockMessenger {
        fn new() -> MockMessenger {
            MockMessenger {
                sent_messages: vec![],
            }
        }
    }

    impl Messenger for MockMessenger {
        fn send(&self, message: &str) {
            self.sent_messages.push(String::from(message));
        }
    }

    #[test]
    fn it_sends_an_over_75_percent_warning_message() {
        let mock_messenger = MockMessenger::new();
        let mut limit_tracker = LimitTracker::new(&mock_messenger, 100);

        limit_tracker.set_value(80);

        assert_eq!(mock_messenger.sent_messages.len(), 1);
    }
}
```

</Listing>

এই test code একটি `MockMessenger` struct define করে যার একটি `sent_messages` field আছে যা `String` value-এর একটি `Vec` পাঠাতে বলা message গুলো track রাখে। আমরা একটি associated function `new`-ও define করি যাতে নতুন `MockMessenger` value তৈরি করা সুবিধা হয় যা message-এর একটি empty list দিয়ে শুরু হয়। তারপর আমরা `MockMessenger`-এর জন্য `Messenger` trait implement করি যাতে আমরা একটি `MockMessenger`-কে একটি `LimitTracker`-এ দিতে পারি। `send` method-এর definition-এ, আমরা parameter হিসেবে pass করা message-টি নিই এবং সেটি `MockMessenger`-এর `sent_messages` list-এ store করি।

test-এ, আমরা test করছি কী ঘটে যখন `LimitTracker`-কে `value` সেট করতে বলা হয় এমন কিছুতে যা `max` value-এর 75 শতাংশের বেশি। প্রথমে, আমরা একটি নতুন `MockMessenger` তৈরি করি, যা message-এর একটি empty list দিয়ে শুরু হবে। তারপর, আমরা একটি নতুন `LimitTracker` তৈরি করি যা নতুন `MockMessenger`-এর একটি reference এবং `100`-এর একটি `max` value পায়। আমরা `LimitTracker`-এ `set_value` method call করি `80` value দিয়ে, যা 100-এর 75 শতাংশের বেশি। তারপর, আমরা assert করি যে `MockMessenger` যে message গুলো track করছে সেই list-এ এখন একটি message থাকা উচিত।

তবে, এই test-এ একটি সমস্যা আছে, যেমন এখানে দেখানো হয়েছে:

```console
$ cargo test
   Compiling limit-tracker v0.1.0 (file:///projects/limit-tracker)
error[E0596]: cannot borrow `self.sent_messages` as mutable, as it is behind a `&` reference
  --> src/lib.rs:58:13
   |
58 |             self.sent_messages.push(String::from(message));
   |             ^^^^^^^^^^^^^^^^^^ `self` is a `&` reference, so it cannot be borrowed as mutable
   |
help: consider changing this to be a mutable reference in the `impl` method and the `trait` definition
   |
 2 ~     fn send(&mut self, msg: &str);
 3 | }
...
56 |     impl Messenger for MockMessenger {
57 ~         fn send(&mut self, message: &str) {
   |

For more information about this error, try `rustc --explain E0596`.
error: could not compile `limit-tracker` (lib test) due to 1 previous error
```

আমরা `MockMessenger`-কে message গুলো track করার জন্য modify করতে পারি না, কারণ `send` method `self`-এর একটি immutable reference নেয়। আমরা error text-এর পরামর্শ অনুযায়ী `impl` method এবং trait definition উভয় জায়গাতেই `&mut self` ব্যবহারও করতে পারি না। আমরা শুধুমাত্র testing-এর জন্য `Messenger` trait পরিবর্তন করতে চাই না। এর বদলে, আমাদের এমন একটি উপায় খুঁজে বের করতে হবে যাতে আমাদের test code আমাদের existing design-এর সাথে সঠিকভাবে কাজ করে।

এমন একটি পরিস্থিতি যেখানে interior mutability সাহায্য করতে পারে! আমরা `sent_messages`-কে একটি `RefCell<T>`-এর ভেতরে store করব, এবং তাহলে `send` method আমাদের দেখা message গুলো store করতে `sent_messages` modify করতে পারবে। Listing 15-22 দেখায় সেটি কেমন দেখায়।

<Listing number="15-22" file-name="src/lib.rs" caption="Using `RefCell<T>` to mutate an inner value while the outer value is considered immutable">

```rust,noplayground
#[cfg(test)]
mod tests {
    use super::*;
    use std::cell::RefCell;

    struct MockMessenger {
        sent_messages: RefCell<Vec<String>>,
    }

    impl MockMessenger {
        fn new() -> MockMessenger {
            MockMessenger {
                sent_messages: RefCell::new(vec![]),
            }
        }
    }

    impl Messenger for MockMessenger {
        fn send(&self, message: &str) {
            self.sent_messages.borrow_mut().push(String::from(message));
        }
    }

    #[test]
    fn it_sends_an_over_75_percent_warning_message() {
        // --snip--

        assert_eq!(mock_messenger.sent_messages.borrow().len(), 1);
    }
}
```

</Listing>

`sent_messages` field-টি এখন `Vec<String>`-এর বদলে `RefCell<Vec<String>>` type-এর। `new` function-এ, আমরা empty vector-এর চারপাশে একটি নতুন `RefCell<Vec<String>>` instance তৈরি করি।

`send` method-এর implementation-এর জন্য, প্রথম parameter-টি এখনো `self`-এর একটি immutable borrow, যা trait definition-এর সাথে match করে। আমরা `self.sent_messages`-এ থাকা `RefCell<Vec<String>>`-এ `borrow_mut` call করি যাতে `RefCell<Vec<String>>`-এর ভেতরের value-এর একটি mutable reference পাই, যা সেই vector-টি। তারপর, আমরা vector-এর mutable reference-এ `push` call করতে পারি যাতে test-এর সময় পাঠানো message গুলো track রাখা যায়।

আমাদের যে শেষ পরিবর্তনটি করতে হবে তা হলো assertion-এ: ভেতরের vector-এ কতগুলো item আছে তা দেখতে, আমরা `RefCell<Vec<String>>`-এ `borrow` call করি যাতে vector-টির একটি immutable reference পাই।

এখন তুমি দেখেছ কীভাবে `RefCell<T>` ব্যবহার করতে হয়, চলো এটি কীভাবে কাজ করে তা গভীরভাবে দেখি!

<!-- Old headings. Do not remove or links may break. -->

<a id="keeping-track-of-borrows-at-runtime-with-refcellt"></a>

#### Runtime-এ Borrow Track করা

immutable এবং mutable reference তৈরি করার সময়, আমরা যথাক্রমে `&` এবং `&mut` syntax ব্যবহার করি। `RefCell<T>`-এর সাথে, আমরা `borrow` এবং `borrow_mut` method ব্যবহার করি, যা `RefCell<T>`-এর অন্তর্গত safe API-এর অংশ। `borrow` method smart pointer type `Ref<T>` return করে, এবং `borrow_mut` smart pointer type `RefMut<T>` return করে। উভয় type-ই `Deref` implement করে, তাই আমরা এদের regular reference-এর মতো বিবেচনা করতে পারি।

`RefCell<T>` track রাখে বর্তমানে কতগুলো `Ref<T>` এবং `RefMut<T>` smart pointer active আছে। প্রতিবার আমরা `borrow` call করলে, `RefCell<T>` কতগুলো immutable borrow active আছে তার count বাড়ায়। যখন একটি `Ref<T>` value scope ছেড়ে যায়, immutable borrow-এর count 1 কমে যায়। compile-time borrowing rule-এর মতো, `RefCell<T>` আমাদের যেকোনো সময় অনেকগুলো immutable borrow অথবা একটি mutable borrow রাখতে দেয়।

আমরা যদি এই rule গুলো লঙ্ঘন করার চেষ্টা করি, তাহলে reference-এর ক্ষেত্রে যেমন compiler error পেতাম, তার বদলে `RefCell<T>`-এর implementation runtime-এ panic করবে। Listing 15-23 দেখায় Listing 15-22-এর `send`-এর implementation-এর একটি পরিবর্তন। আমরা ইচ্ছাকৃতভাবে একই scope-এ দুটি active mutable borrow তৈরি করার চেষ্টা করছি যাতে দেখানো যায় যে `RefCell<T>` আমাদের এটি runtime-এ করতে বারণ করে।

<Listing number="15-23" file-name="src/lib.rs" caption="Creating two mutable references in the same scope to see that `RefCell<T>` will panic">

```rust,ignore,panics
    impl Messenger for MockMessenger {
        fn send(&self, message: &str) {
            let mut one_borrow = self.sent_messages.borrow_mut();
            let mut two_borrow = self.sent_messages.borrow_mut();

            one_borrow.push(String::from(message));
            two_borrow.push(String::from(message));
        }
    }
```

</Listing>

আমরা `borrow_mut` থেকে return হওয়া `RefMut<T>` smart pointer-এর জন্য `one_borrow` নামে একটি variable তৈরি করি। তারপর, আমরা একইভাবে `two_borrow` variable-এ আরেকটি mutable borrow তৈরি করি। এটি একই scope-এ দুটি mutable reference তৈরি করে, যা allowed নয়। যখন আমরা আমাদের library-এর test গুলো চালাই, Listing 15-23-এর code কোনো error ছাড়াই compile হবে, কিন্তু test ব্যর্থ হবে:

```console
$ cargo test
   Compiling limit-tracker v0.1.0 (file:///projects/limit-tracker)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.91s
     Running unittests src/lib.rs (target/debug/deps/limit_tracker-e599811fa246dbde)

running 1 test
test tests::it_sends_an_over_75_percent_warning_message ... FAILED

failures:

---- tests::it_sends_an_over_75_percent_warning_message stdout ----

thread 'tests::it_sends_an_over_75_percent_warning_message' (6028024) panicked at src/lib.rs:60:53:
RefCell already borrowed
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    tests::it_sends_an_over_75_percent_warning_message

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

লক্ষ্য করো যে code-টি `already borrowed:
BorrowMutError` message দিয়ে panic করেছে। এভাবেই `RefCell<T>` runtime-এ borrowing rule লঙ্ঘন পরিচালনা করে।

compile time-এর বদলে runtime-এ borrowing error ধরা বেছে নেওয়ার অর্থ হলো তুমি সম্ভবত তোমার code-এ ভুল গুলো development process-এ অনেক পরে খুঁজে পাবে: সম্ভবত তোমার code production-এ deploy না হওয়া পর্যন্ত নয়। এছাড়া, compile time-এর বদলে runtime-এ borrow গুলো track রাখার ফলে তোমার code-এ একটি ছোট runtime performance penalty আসবে। তবে, `RefCell<T>` ব্যবহার করলে এমন একটি mock object লেখা সম্ভব যা নিজেকে modify করতে পারে যাতে সে যে message গুলো দেখেছে সেগুলো track রাখে যখন তুমি এটিকে এমন context-এ ব্যবহার করো যেখানে শুধুমাত্র immutable value allow করা হয়। তুমি এর trade-off সত্ত্বেও `RefCell<T>` ব্যবহার করতে পারো যাতে regular reference-এর চেয়ে বেশি functionality পাওয়া যায়।

<!-- Old headings. Do not remove or links may break. -->

<a id="having-multiple-owners-of-mutable-data-by-combining-rc-t-and-ref-cell-t"></a>
<a id="allowing-multiple-owners-of-mutable-data-with-rct-and-refcellt"></a>

### Mutable Data-এর একাধিক Owner Allow করা

`RefCell<T>` ব্যবহারের একটি সাধারণ উপায় হলো `Rc<T>`-এর সাথে combine করা। মনে করো `Rc<T>` তোমাকে কিছু data-এর একাধিক owner রাখতে দেয়, কিন্তু এটি সেই data-তে শুধু immutable access দেয়। তোমার যদি এমন একটি `Rc<T>` থাকে যা একটি `RefCell<T>` ধারণ করে, তুমি এমন একটি value পেতে পারো যার একাধিক owner থাকতে পারে _এবং_ যা তুমি mutate করতে পারো!

উদাহরণস্বরূপ, Listing 15-18-এর cons list উদাহরণটি মনে করো যেখানে আমরা `Rc<T>` ব্যবহার করেছিলাম একাধিক list-কে অন্য একটি list-এর ownership share করতে দিতে। যেহেতু `Rc<T>` শুধুমাত্র immutable value ধারণ করে, আমরা একবার সেগুলো তৈরি করার পর list-গুলোর কোনো value পরিবর্তন করতে পারি না। চলো list-গুলোর value পরিবর্তন করার ক্ষমতার জন্য `RefCell<T>` যোগ করি। Listing 15-24 দেখায় যে `Cons` definition-এ একটি `RefCell<T>` ব্যবহার করে, আমরা সব list-এ store করা value পরিবর্তন করতে পারি।

<Listing number="15-24" file-name="src/main.rs" caption="Using `Rc<RefCell<i32>>` to create a `List` that we can mutate">

```rust
#[derive(Debug)]
enum List {
    Cons(Rc<RefCell<i32>>, Rc<List>),
    Nil,
}

use crate::List::{Cons, Nil};
use std::cell::RefCell;
use std::rc::Rc;

fn main() {
    let value = Rc::new(RefCell::new(5));

    let a = Rc::new(Cons(Rc::clone(&value), Rc::new(Nil)));

    let b = Cons(Rc::new(RefCell::new(3)), Rc::clone(&a));
    let c = Cons(Rc::new(RefCell::new(4)), Rc::clone(&a));

    *value.borrow_mut() += 10;

    println!("a after = {a:?}");
    println!("b after = {b:?}");
    println!("c after = {c:?}");
}
```

</Listing>

আমরা একটি `Rc<RefCell<i32>>` instance তৈরি করি এবং সেটি `value` নামের একটি variable-এ store করি যাতে আমরা পরে সরাসরি এটিতে access করতে পারি। তারপর, আমরা `a`-তে একটি `List` তৈরি করি যার `Cons` variant `value` ধারণ করে। আমাদের `value`-কে clone করতে হবে যাতে `a` এবং `value` উভয়েই ভেতরের `5` value-টির ownership রাখে, `value` থেকে `a`-তে ownership transfer না করে অথবা `a`-কে `value` থেকে borrow না করে।

আমরা list `a`-কে একটি `Rc<T>`-এ wrap করি যাতে আমরা `b` এবং `c` list তৈরি করলে তারা উভয়েই `a`-কে refer করতে পারে, যেটা আমরা Listing 15-18-এ করেছিলাম।

`a`, `b`, এবং `c`-তে list গুলো তৈরি করার পর, আমরা `value`-তে থাকা value-এ 10 যোগ করতে চাই। আমরা এটি `value`-তে `borrow_mut` call করে করি, যা Chapter 5-এর [“Where’s the `->`
Operator?”][wheres-the---operator]<!-- ignore -->-এ আলোচিত automatic dereferencing feature ব্যবহার করে `Rc<T>`-কে ভেতরের `RefCell<T>` value-এ dereference করে। `borrow_mut` method একটি `RefMut<T>` smart pointer return করে, এবং আমরা এটির উপর dereference operator ব্যবহার করি এবং ভেতরের value পরিবর্তন করি।

আমরা `a`, `b`, এবং `c` print করলে, আমরা দেখতে পাই যে তাদের সবার কাছেই `5`-এর বদলে modified `15` value আছে:

```console
$ cargo run
   Compiling cons-list v0.1.0 (file:///projects/cons-list)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.63s
     Running `target/debug/cons-list`
a after = Cons(RefCell { value: 15 }, Nil)
b after = Cons(RefCell { value: 3 }, Cons(RefCell { value: 15 }, Nil))
c after = Cons(RefCell { value: 4 }, Cons(RefCell { value: 15 }, Nil))
```

এই technique বেশ দারুণ! `RefCell<T>` ব্যবহার করে, আমাদের কাছে বাইরের দিকে একটি immutable `List` value আছে। কিন্তু আমরা `RefCell<T>`-এর method গুলো ব্যবহার করতে পারি যা তার interior mutability-তে access দেয় যাতে আমরা প্রয়োজনে আমাদের data modify করতে পারি। borrowing rule-এর runtime check গুলো আমাদের data race থেকে রক্ষা করে, এবং আমাদের data structure-এ এই flexibility-র জন্য একটু speed বিসর্জন দেওয়া মাঝে মাঝে মূল্যবান। মনে রাখবে `RefCell<T>` multithreaded code-এর জন্য কাজ করে না! `Mutex<T>` হলো `RefCell<T>`-এর thread-safe সংস্করণ, এবং আমরা `Mutex<T>` নিয়ে Chapter 16-তে আলোচনা করব।

[wheres-the---operator]: ch05-03-method-syntax.html#wheres-the---operator

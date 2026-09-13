## `Drop` Trait দিয়ে Cleanup-এ Code চালানো

smart pointer pattern-এর জন্য গুরুত্বপূর্ণ দ্বিতীয় trait হলো `Drop`, যা তোমাকে কাস্টমাইজ করতে দেয় কী ঘটবে যখন একটি value scope ছেড়ে যাওয়ার উপক্রমে থাকে। তুমি যেকোনো type-এর জন্য `Drop` trait-এর একটি implementation দিতে পারো, এবং সেই code ব্যবহার করা যেতে পারে file বা network connection-এর মতো resource release করতে।

আমরা `Drop`-কে smart pointer-এর context-এ পরিচয় করাচ্ছি কারণ কোনো smart pointer implement করার সময় `Drop` trait-এর functionality প্রায় সবসময়ই ব্যবহৃত হয়। উদাহরণস্বরূপ, যখন একটি `Box<T>` drop করা হয়, এটি box-টি যে heap space-কে point করছিল সেটি deallocate করবে।

কিছু language-এ, কিছু type-এর জন্য programmer-কে অবশ্যই সেই type-গুলোর একটি instance ব্যবহার শেষ করার প্রতিবার memory বা resource free করার code call করতে হয়। উদাহরণ হলো file handle, socket এবং lock। যদি programmer ভুলে যায়, তাহলে system overload হয়ে crash করতে পারে। Rust-এ, তুমি নির্দিষ্ট করতে পারো যে কোনো value scope ছেড়ে যাওয়ার সময় নির্দিষ্ট কিছু code চলবে, এবং compiler এই code স্বয়ংক্রিয়ভাবে insert করবে। ফলে, তোমার এই বিষয়ে সতর্ক হওয়ার দরকার নেই যে program-এ একটি নির্দিষ্ট type-এর instance যেখানে শেষ হয় সেখানে সব জায়গায় cleanup code রাখা—তবুও তুমি resource leak করবে না!

কোনো value scope ছেড়ে যাওয়ার সময় কোন code চলবে তা তুমি `Drop` trait implement করে নির্দিষ্ট করো। `Drop` trait তোমাকে `drop` নামের একটি method implement করতে বলে যা `self`-এর একটি mutable reference নেয়। Rust কখন `drop` call করে তা দেখতে, আপাতত চলো `println!` statement দিয়ে `drop` implement করি।

Listing 15-14 একটি `CustomSmartPointer` struct দেখায় যার একমাত্র custom functionality হলো এটি instance scope ছেড়ে গেলে `Dropping CustomSmartPointer!` print করবে, যাতে দেখা যায় Rust কখন `drop` method call করে।

<Listing number="15-14" file-name="src/main.rs" caption="A `CustomSmartPointer` struct that implements the `Drop` trait where we would put our cleanup code">

```rust
struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
    fn drop(&mut self) {
        println!("Dropping CustomSmartPointer with data `{}`!", self.data);
    }
}

fn main() {
    let c = CustomSmartPointer {
        data: String::from("my stuff"),
    };
    let d = CustomSmartPointer {
        data: String::from("other stuff"),
    };
    println!("CustomSmartPointers created");
}
```

</Listing>

`Drop` trait prelude-এ আছে, তাই আমাদের এটিকে scope-এ আনার দরকার নেই। আমরা `CustomSmartPointer`-এ `Drop` trait implement করি এবং `drop` method-এর জন্য এমন একটি implementation দিই যা `println!` call করে। `drop` method-এর body-তে তুমি যে logic চালাতে চাও তোমার type-ের একটি instance scope ছেড়ে গেলে, সেটা রাখবে। আমরা এখানে কিছু text print করছি যাতে দৃশ্যত দেখা যায় Rust কখন `drop` call করবে।

`main`-এ আমরা `CustomSmartPointer`-এর দুটি instance তৈরি করি এবং তারপর `CustomSmartPointers created` print করি। `main`-এর শেষে, আমাদের `CustomSmartPointer` instance গুলো scope ছেড়ে দেবে, এবং Rust আমাদের রাখা `drop` method-এর code call করবে, আমাদের শেষ message টি print করবে। মনে রাখবে আমাদের `drop` method-টি explicitly call করার দরকার ছিল না।

এই program চালালে আমরা নিচের output দেখব:

```console
$ cargo run
   Compiling drop-example v0.1.0 (file:///projects/drop-example)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.60s
     Running `target/debug/drop-example`
CustomSmartPointers created
Dropping CustomSmartPointer with data `other stuff`!
Dropping CustomSmartPointer with data `my stuff`!
```

আমাদের instance গুলো scope ছেড়ে যাওয়ার সময় Rust স্বয়ংক্রিয়ভাবে আমাদের জন্য `drop` call করেছে, আমরা যে code নির্দিষ্ট করেছিলাম সেটি call করে। Variable গুলো তৈরির উল্টো ক্রমে drop করা হয়, তাই `d`-কে `c`-এর আগে drop করা হয়েছে। এই উদাহরণের উদ্দেশ্য তোমাকে `drop` method কীভাবে কাজ করে সে বিষয়ে একটি দৃশ্যমান গাইড দেওয়া; সাধারণত তুমি print message-এর বদলে তোমার type-এর চালানো দরকার এমন cleanup code নির্দিষ্ট করবে।

<!-- Old headings. Do not remove or links may break. -->

<a id="dropping-a-value-early-with-std-mem-drop"></a>

দুর্ভাগ্যবশত, স্বয়ংক্রিয় `drop` functionality বন্ধ করা খুব সরল নয়। `drop` বন্ধ করা সাধারণত প্রয়োজন হয় না; `Drop` trait-এর পুরো উদ্দেশ্যই হলো এটি স্বয়ংক্রিয়ভাবে সামলানো হয়। তবে মাঝে মাঝে, তুমি একটি value-কে আগেই পরিষ্কার করতে চাইতে পারো। এর একটি উদাহরণ হলো smart pointer ব্যবহারের সময় যা lock পরিচালনা করে: তুমি হয়তো `drop` method-টি force করে call করতে চাইবে যা lock release করে যাতে একই scope-এর অন্য code সেই lock acquire করতে পারে। Rust তোমাকে `Drop` trait-এর `drop` method-টি manually call করতে দেয় না; এর বদলে, তুমি একটি value-কে তার scope-এর শেষের আগে drop করতে বাধ্য করতে চাইলে standard library-র দেওয়া `std::mem::drop` function call করতে হবে।

Listing 15-14-এর `main` function-টি পরিবর্তন করে `Drop` trait-এর `drop` method-টিকে manually call করার চেষ্টা করলে কাজ করবে না, যেমন Listing 15-15-তে দেখানো হয়েছে।

<Listing number="15-15" file-name="src/main.rs" caption="Attempting to call the `drop` method from the `Drop` trait manually to clean up early">

```rust,ignore,does_not_compile
fn main() {
    let c = CustomSmartPointer {
        data: String::from("some data"),
    };
    println!("CustomSmartPointer created");
    c.drop();
    println!("CustomSmartPointer dropped before the end of main");
}
```

</Listing>

এই code compile করার চেষ্টা করলে আমরা এই error পাব:

```console
$ cargo run
   Compiling drop-example v0.1.0 (file:///projects/drop-example)
error[E0040]: explicit use of destructor method
  --> src/main.rs:16:7
   |
16 |     c.drop();
   |       ^^^^ explicit destructor calls not allowed
   |
help: consider using `drop` function
   |
16 -     c.drop();
16 +     drop(c);
   |

For more information about this error, try `rustc --explain E0040`.
error: could not compile `drop-example` (bin "drop-example") due to 1 previous error
```

এই error message বলছে যে আমরা explicitly `drop` call করতে পারি না। error message-টি _destructor_ শব্দটি ব্যবহার করে, যা এমন একটি function-এর জন্য সাধারণ programming term যা কোনো instance পরিষ্কার করে। _destructor_ হলো _constructor_-এর অনুরূপ, যা একটি instance তৈরি করে। Rust-এর `drop` function হলো একটি নির্দিষ্ট destructor।

Rust আমাদের `drop` explicitly call করতে দেয় না, কারণ Rust এখনো `main`-এর শেষে value-টির উপর স্বয়ংক্রিয়ভাবে `drop` call করবে। এটি একটি double free error ঘটাতে পারে কারণ Rust একই value দু'বার পরিষ্কার করার চেষ্টা করবে।

আমরা কোনো value scope ছেড়ে গেলে `drop`-এর স্বয়ংক্রিয় insertion বন্ধ করতে পারি না, এবং আমরা `drop` method-টি explicitly call করতে পারি না। তাই, যদি আমাদের কোনো value-কে আগেই পরিষ্কার করতে বাধ্য করতে হয়, আমরা `std::mem::drop` function ব্যবহার করি।

`std::mem::drop` function-টি `Drop` trait-এর `drop` method থেকে আলাদা। আমরা এটিকে force-drop করতে চাওয়া value-টিকে argument হিসেবে pass করে call করি। এই function-টি prelude-এ আছে, তাই আমরা Listing 15-15-এর `main`-কে পরিবর্তন করে `drop` function call করতে পারি, যেমন Listing 15-16-তে দেখানো হয়েছে।

<Listing number="15-16" file-name="src/main.rs" caption="Calling `std::mem::drop` to explicitly drop a value before it goes out of scope">

```rust
fn main() {
    let c = CustomSmartPointer {
        data: String::from("some data"),
    };
    println!("CustomSmartPointer created");
    drop(c);
    println!("CustomSmartPointer dropped before the end of main");
}
```

</Listing>

এই code চালালে নিচের output পাওয়া যাবে:

```console
$ cargo run
   Compiling drop-example v0.1.0 (file:///projects/drop-example)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.73s
     Running `target/debug/drop-example`
CustomSmartPointer created
Dropping CustomSmartPointer with data `some data`!
CustomSmartPointer dropped before the end of main
```

``Dropping CustomSmartPointer with data `some data`!`` text-টি `CustomSmartPointer created` এবং `CustomSmartPointer dropped before the end of main` text-এর মাঝে print হয়েছে, যা দেখায় যে সেই মুহূর্তে `c`-কে drop করার জন্য `drop` method-এর code call হয়েছে।

তুমি `Drop` trait implementation-এ নির্দিষ্ট করা code অনেকভাবে ব্যবহার করতে পারো যাতে cleanup সুবিধাজনক এবং safe হয়: উদাহরণস্বরূপ, তুমি এটি ব্যবহার করে তোমার নিজস্ব memory allocator তৈরি করতে পারো! `Drop` trait এবং Rust-এর ownership system-এর সাহায্যে, তোমাকে পরিষ্কার করতে মনে রাখতে হবে না, কারণ Rust সেটা স্বয়ংক্রিয়ভাবে করে।

তোমাকে এই নিয়েও চিন্তা করতে হবে না যে এখনো ব্যবহৃত value দুর্ঘটনাক্রমে পরিষ্কার করার ফলে কোনো সমস্যা হবে কিনা: যে ownership system reference-গুলো সবসময় valid নিশ্চিত করে, সেটি নিশ্চিত করে যে value আর ব্যবহৃত না হলে `drop` শুধুমাত্র একবার call হয়।

এখন আমরা `Box<T>` এবং smart pointer-এর কিছু বৈশিষ্ট্য দেখেছি, চলো standard library-তে define করা আরও কয়েকটি smart pointer দেখি।

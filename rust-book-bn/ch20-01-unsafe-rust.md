## Unsafe Rust

এখন পর্যন্ত আমরা যেসব code নিয়ে আলোচনা করেছি, সবগুলোতেই compile time-এ Rust-এর memory safety guarantee enforced হয়েছে। কিন্তু Rust-এর ভেতরে আরেকটি লুকানো language আছে যা এই memory safety guarantee-গুলো enforce করে না: একে _unsafe Rust_ বলা হয় এবং এটি regular Rust-এর মতোই কাজ করে কিন্তু আমাদের কিছু extra superpower দেয়।

Unsafe Rust এর অস্তিত্ব আছে কারণ, স্বভাবতই, static analysis রক্ষণশীল। যখন compiler চেক করার চেষ্টা করে যে code গুলো guarantee uphold করছে কি না, তখন কিছু valid program reject করা তার জন্য ভালো, অপেক্ষা করে কিছু invalid program accept করার চেয়ে। যদিও code-টি _maybe_ ঠিক থাকতে পারে, যদি Rust compiler-এর কাছে নিশ্চিত হওয়ার মতো পর্যাপ্ত information না থাকে, তবে সেটি code-টি reject করবে। এসব ক্ষেত্রে, তুমি unsafe code ব্যবহার করে compiler-কে বলতে পারো, "আমাকে বিশ্বাস করো, আমি জানি আমি কী করছি।" তবে সতর্ক থেকো, তুমি নিজ দায়িত্বে unsafe Rust ব্যবহার করবে: যদি তুমি unsafe code ভুলভাবে ব্যবহার করো, তবে memory unsafety-র কারণে সমস্যা হতে পারে, যেমন null pointer dereferencing।

Rust-এর একটি unsafe alter ego থাকার আরেকটি কারণ হলো, underlying computer hardware স্বভাবতই unsafe। যদি Rust তোমাকে unsafe operation করতে না দিত, তবে তুমি কিছু নির্দিষ্ট task করতে পারতে না। Rust-কে তোমাকে low-level system programming করার অনুমতি দিতে হবে, যেমন সরাসরি operating system-এর সাথে interact করা বা এমনকি নিজের operating system লেখা। Low-level system programming করা এই language-এর লক্ষ্যগুলোর মধ্যে একটি। চলো দেখি unsafe Rust দিয়ে আমরা কী করতে পারি এবং কীভাবে করতে পারি।

<!-- Old headings. Do not remove or links may break. -->

<a id="unsafe-superpowers"></a>

### Performing Unsafe Superpowers

Unsafe Rust-এ যাওয়ার জন্য, `unsafe` keyword ব্যবহার করো এবং তারপর একটি নতুন block শুরু করো যেখানে unsafe code থাকবে। Unsafe Rust-এ তুমি পাঁচটি action নিতে পারবে যা safe Rust-এ পারবে না, আমরা এগুলোকে _unsafe superpower_ বলি। সেই superpower-গুলোর মধ্যে রয়েছে:

1. একটি raw pointer-কে dereference করা।
1. একটি unsafe function বা method কল করা।
1. একটি mutable static variable-কে access বা modify করা।
1. একটি unsafe trait implement করা।
1. `union`-এর field access করা।

এটি বোঝা গুরুত্বপূর্ণ যে `unsafe` এর মানে borrow checker বন্ধ হয়ে যাওয়া বা Rust-এর অন্যান্য safety check disable হওয়া নয়: যদি তুমি unsafe code-এ reference ব্যবহার করো, সেটি এখনও check করা হবে। `unsafe` keyword শুধুমাত্র তোমাকে এই পাঁচটি feature-এ access দেয় যেগুলো compiler memory safety-র জন্য check করে না। একটি unsafe block-এর ভেতরে তুমি কিছুটা degree-তে safety পাবে।

এছাড়া, `unsafe` এর মানে এই নয় যে block-এর ভেতরের code অবশ্যই dangerous বা এতে অবশ্যই memory safety problem থাকবে: এর intent হলো যে programmer হিসেবে তুমি নিশ্চিত করবে যে একটি `unsafe` block-এর ভেতরের code বৈধভাবে memory access করবে।

মানুষ ভুল করতে পারে এবং ভুল হবেই, কিন্তু এই পাঁচটি unsafe operation-কে `unsafe` দিয়ে annotate করা block-এর ভেতরে রাখার প্রয়োজনীয়তা থাকায়, তুমি জানবে যে memory safety সম্পর্কিত যেকোনো error অবশ্যই একটি `unsafe` block-এর ভেতরে থাকবে। `unsafe` block-গুলো ছোট রাখো; পরে তুমি memory bug investigate করার সময় এর জন্য কৃতজ্ঞ হবে।

Unsafe code-কে যতটা সম্ভব isolate করতে, এটির পরিবেশ একটি safe abstraction-এর ভেতরে রাখা এবং একটি safe API provide করা সবচেয়ে ভালো, যা আমরা পরে এই chapter-এ unsafe function ও method পরীক্ষা করার সময় আলোচনা করব। Standard library-র কিছু অংশ unsafe code-এর উপর safe abstraction হিসেবে implement করা যা audit করা হয়েছে। Unsafe code-কে একটি safe abstraction-এ wrap করলে `unsafe` এর ব্যবহার সব জায়গায় ছড়িয়ে পড়া থেকে আটকায় যেখানে তুমি বা তোমার user-রা `unsafe` code দিয়ে implement করা functionality ব্যবহার করতে চাইতে পারো, কারণ একটি safe abstraction ব্যবহার করা safe।

চলো একে একে পাঁচটি unsafe superpower দেখি। আমরা unsafe code-এর সাথে একটি safe interface provide করে এমন কিছু abstraction-ও দেখব।

### Dereferencing a Raw Pointer

Chapter 4-এর [“Dangling References”][dangling-references]<!-- ignore
--> section-এ আমরা উল্লেখ করেছিলাম যে compiler নিশ্চিত করে যে reference-গুলো সবসময় valid থাকে। Unsafe Rust-এ দুটি নতুন type আছে যাদের _raw pointer_ বলা হয় এবং যা reference-এর মতো। Reference-এর মতো, raw pointer-ও immutable বা mutable হতে পারে এবং যথাক্রমে `*const T` এবং `*mut T` হিসেবে লেখা হয়। এখানে asterisk টি dereference operator নয়; এটি type-এর নামের অংশ। Raw pointer-এর context-এ, _immutable_ মানে হলো pointer-টিকে dereference করার পর সরাসরি assign করা যাবে না।

Reference এবং smart pointer-এর থেকে আলাদা হিসেবে, raw pointer-গুলো:

- একই location-এ একসাথে immutable এবং mutable pointer বা একাধিক mutable pointer থাকতে দিয়ে borrowing rule উপেক্ষা করতে পারে
- valid memory-কে point করছে এমন guarantee নেই
- null হতে পারে
- কোনো automatic cleanup implement করে না

Rust-কে এই guarantee-গুলো enforce করা থেকে বিরত রেখে, তুমি guaranteed safety ছেড়ে দিতে পারো এবং বিনিময়ে বেশি performance বা অন্য কোনো language বা hardware-এর সাথে interface করার ক্ষমতা পেতে পারো যেখানে Rust-এর guarantee প্রযোজ্য নয়।

Listing 20-1 দেখায় কীভাবে একটি immutable এবং একটি mutable raw pointer তৈরি করতে হয়।

<Listing number="20-1" caption="Creating raw pointers with the raw borrow operators">

```rust
    let mut num = 5;

    let r1 = &raw const num;
    let r2 = &raw mut num;
```

</Listing>

খেয়াল করো যে এই code-এ আমরা `unsafe` keyword ব্যবহার করিনি। আমরা safe code-এ raw pointer তৈরি করতে পারি; আমরা শুধু একটি unsafe block-এর বাইরে raw pointer-কে dereference করতে পারি না, যেমন তুমি একটু পরেই দেখবে।

আমরা raw borrow operator ব্যবহার করে raw pointer তৈরি করেছি: `&raw const num` একটি `*const i32` immutable raw pointer তৈরি করে এবং `&raw mut num` একটি `*mut
i32` mutable raw pointer তৈরি করে। যেহেতু আমরা সরাসরি একটি local variable থেকে এগুলো তৈরি করেছি, আমরা জানি যে এই নির্দিষ্ট raw pointer-গুলো valid, কিন্তু যেকোনো raw pointer সম্পর্কে এই assumption করা যাবে না।

এটি প্রদর্শন করতে, এরপর আমরা raw borrow operator ব্যবহার করার পরিবর্তে `as` keyword দিয়ে একটি value-কে cast করে এমন একটি raw pointer তৈরি করব যার validity সম্পর্কে আমরা ততটা নিশ্চিত নই। Listing 20-2 দেখায় কীভাবে memory-র একটি স্বেচ্ছাচারী location-এ একটি raw pointer তৈরি করতে হয়। স্বেচ্ছাচারী memory ব্যবহার করার চেষ্টা undefined: সেই address-এ data থাকতেও পারে বা নাও থাকতে পারে, compiler এমনভাবে code optimize করতে পারে যাতে কোনো memory access না হয়, বা program একটি segmentation fault দিয়ে terminate হতে পারে। সাধারণত, এরকম code লেখার কোনো ভালো কারণ নেই, বিশেষত সেই ক্ষেত্রে যেখানে তুমি raw borrow operator ব্যবহার করতে পারো, কিন্তু এটি সম্ভব।

<Listing number="20-2" caption="Creating a raw pointer to an arbitrary memory address">

```rust
    let address = 0x012345usize;
    let r = address as *const i32;
```

</Listing>

মনে করো যে আমরা safe code-এ raw pointer তৈরি করতে পারি, কিন্তু raw pointer-কে dereference করে point করা data পড়তে পারি না। Listing 20-3-এ, আমরা এমন একটি raw pointer-এর উপর dereference operator `*` ব্যবহার করি যার জন্য একটি `unsafe` block প্রয়োজন।

<Listing number="20-3" caption="Dereferencing raw pointers within an `unsafe` block">

```rust
    let mut num = 5;

    let r1 = &raw const num;
    let r2 = &raw mut num;

    unsafe {
        println!("r1 is: {}", *r1);
        println!("r2 is: {}", *r2);
    }
```

</Listing>

Pointer তৈরি করায় কোনো ক্ষতি নেই; শুধুমাত্র যখন আমরা সেটি যে value-তে point করছে তা access করার চেষ্টা করি, তখনই আমরা হয়তো একটি invalid value নিয়ে কাজ করতে শেষ করি।

এটাও খেয়াল করো যে Listing 20-1 এবং 20-3-এ আমরা `*const i32` এবং `*mut
i32` raw pointer তৈরি করেছি যা দুটোই একই memory location-কে point করে, যেখানে `num` store করা আছে। যদি আমরা পরিবর্তে `num`-এ একটি immutable এবং একটি mutable reference তৈরি করার চেষ্টা করতাম, তবে code compile হতো না কারণ Rust-এর ownership rule কোনো immutable reference-এর সাথে একই সময়ে mutable reference allow করে না। Raw pointer-এর সাথে, আমরা একই location-এ একটি mutable এবং একটি immutable pointer তৈরি করতে পারি এবং mutable pointer দিয়ে data change করতে পারি, যার ফলে potentially একটি data race তৈরি হতে পারে। সাবধান!

এই সব danger থাকা সত্ত্বেও, তুমি কেন raw pointer ব্যবহার করবে? একটি বড় use case হলো C code-এর সাথে interface করার সময়, যেমন তুমি পরবর্তী section-এ দেখবে। আরেকটি ক্ষেত্রে হলো borrow checker যা বোঝে না এমন safe abstraction তৈরির সময়। আমরা unsafe function introduce করব এবং তারপর unsafe code ব্যবহার করে এমন একটি safe abstraction-এর উদাহরণ দেখব।

### Calling an Unsafe Function or Method

একটি unsafe block-এ তুমি যে দ্বিতীয় ধরনের operation করতে পারো তা হলো unsafe function কল করা। Unsafe function এবং method দেখতে ঠিক regular function ও method-এর মতো, কিন্তু এদের definition-এর বাকি অংশের আগে একটি অতিরিক্ত `unsafe` থাকে। এই context-এ `unsafe` keyword indicate করে যে function-এর কিছু requirement আছে যা আমাদের এই function কল করার সময় uphold করতে হবে, কারণ Rust guarantee করতে পারে না যে আমরা এই requirement-গুলো মেনেছি কি না। একটি unsafe function-কে একটি `unsafe` block-এর ভেতরে কল করার মাধ্যমে, আমরা বলছি যে আমরা এই function-এর documentation পড়েছি এবং আমরা function-এর contract uphold করার দায়িত্ব নিচ্ছি।

নিচে একটি unsafe function দেওয়া হলো যার নাম `dangerous` এবং যার body-তে কিছুই করে না:

```rust
    unsafe fn dangerous() {}

    unsafe {
        dangerous();
    }
```

আমাদের একটি পৃথক `unsafe` block-এর ভেতরে `dangerous` function কল করতে হবে। যদি আমরা `unsafe` block ছাড়া `dangerous` কল করার চেষ্টা করি, তবে আমরা একটি error পাবো:

```console
$ cargo run
   Compiling unsafe-example v0.1.0 (file:///projects/unsafe-example)
error[E0133]: call to unsafe function `dangerous` is unsafe and requires unsafe block
 --> src/main.rs:4:5
  |
4 |     dangerous();
  |     ^^^^^^^^^^^ call to unsafe function
  |
  = note: consult the function's documentation for information on how to avoid undefined behavior

For more information about this error, try `rustc --explain E0133`.
error: could not compile `unsafe-example` (bin "unsafe-example") due to 1 previous error
```

`unsafe` block দিয়ে, আমরা Rust-কে assert করছি যে আমরা function-টির documentation পড়েছি, আমরা বুঝি এটি কীভাবে সঠিকভাবে ব্যবহার করতে হয়, এবং আমরা নিশ্চিত করেছি যে আমরা function-টির contract পূরণ করছি।

একটি `unsafe` function-এর body-তে unsafe operation করতে হলে, তোমাকে এখনও একটি `unsafe` block ব্যবহার করতে হবে, ঠিক regular function-এর ভেতরের মতো, এবং তুমি ভুলে গেলে compiler তোমাকে warn করবে। এটি আমাদের `unsafe` block-গুলোকে যতটা সম্ভব ছোট রাখতে সাহায্য করে, কারণ পুরো function body জুড়ে unsafe operation প্রয়োজন নাও হতে পারে।

#### Creating a Safe Abstraction over Unsafe Code

শুধু কারণ একটি function unsafe code contain করে তার মানে এই নয় যে আমাদের পুরো function-টিকে unsafe হিসেবে mark করতে হবে। আসলে, unsafe code-কে একটি safe function-এ wrap করা একটি common abstraction। একটি উদাহরণ হিসেবে, চলো standard library থেকে `split_at_mut` function-টি পড়াশোনা করি, যা কিছু unsafe code প্রয়োজন। আমরা এটি কীভাবে implement করতে পারি তা explore করব। এই safe method-টি mutable slice-এর উপর define করা: এটি একটি slice নেয় এবং argument হিসেবে দেওয়া index-এ slice-টিকে ভাগ করে দুটি slice তৈরি করে। Listing 20-4 দেখায় কীভাবে `split_at_mut` ব্যবহার করতে হয়।

<Listing number="20-4" caption="Using the safe `split_at_mut` function">

```rust
    let mut v = vec![1, 2, 3, 4, 5, 6];

    let r = &mut v[..];

    let (a, b) = r.split_at_mut(3);

    assert_eq!(a, &mut [1, 2, 3]);
    assert_eq!(b, &mut [4, 5, 6]);
```

</Listing>

আমরা শুধুমাত্র safe Rust ব্যবহার করে এই function-টি implement করতে পারি না। এমন একটি attempt Listing 20-5-এর মতো দেখতে হবে, যা compile হবে না। simplicity-র জন্য, আমরা `split_at_mut`-কে method না হিসেবে একটি function হিসেবে implement করব এবং শুধুমাত্র generic type `T`-এর বদলে `i32` value-র slice-এর জন্য।

<Listing number="20-5" caption="An attempted implementation of `split_at_mut` using only safe Rust">

```rust,ignore,does_not_compile
fn split_at_mut(values: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
    let len = values.len();

    assert!(mid <= len);

    (&mut values[..mid], &mut values[mid..])
}
```

</Listing>

এই function প্রথমে slice-টির total length পায়। তারপর, length-এর সাথে তুলনা করে দেখে যে parameter হিসেবে দেওয়া index-টি slice-এর ভেতরে আছে কি না। এই assertion-এর মানে হলো, যদি আমরা slice-কে ভাগ করার জন্য length-এর চেয়ে বড় কোনো index পাস করি, তবে function-টি সেই index ব্যবহার করার চেষ্টা করার আগেই panic করবে।

তারপর, আমরা একটি tuple-এ দুটি mutable slice return করি: একটি original slice-এর শুরু থেকে `mid` index পর্যন্ত এবং অন্যটি `mid` থেকে slice-এর শেষ পর্যন্ত।

যখন আমরা Listing 20-5-এর code compile করার চেষ্টা করি, তখন আমরা একটি error পাবো:

```console
$ cargo run
   Compiling unsafe-example v0.1.0 (file:///projects/unsafe-example)
error[E0499]: cannot borrow `*values` as mutable more than once at a time
 --> src/main.rs:6:31
  |
1 | fn split_at_mut(values: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
  |                         - let's call the lifetime of this reference `'1`
...
6 |     (&mut values[..mid], &mut values[mid..])
  |     --------------------------^^^^^^--------
  |     |     |                   |
  |     |     |                   second mutable borrow occurs here
  |     |     first mutable borrow occurs here
  |     returning this value requires that `*values` is borrowed for `'1`
  |
  = help: use `.split_at_mut(position)` to obtain two mutable non-overlapping sub-slices

For more information about this error, try `rustc --explain E0499`.
error: could not compile `unsafe-example` (bin "unsafe-example") due to 1 previous error
```

Rust-এর borrow checker বুঝতে পারে না যে আমরা slice-এর ভিন্ন ভিন্ন অংশ borrow করছি; এটি শুধু জানে যে আমরা একই slice থেকে দুবার borrow করছি। একটি slice-এর ভিন্ন ভিন্ন অংশ borrow করা fundamentally ঠিক আছে কারণ দুটি slice overlap করছে না, কিন্তু Rust এতটা smart নয় যে এটি বুঝতে পারবে। যখন আমরা জানি code ঠিক আছে, কিন্তু Rust জানে না, তখন unsafe code-এর দিকে যাওয়ার সময়।

Listing 20-6 দেখায় কীভাবে একটি `unsafe` block, একটি raw pointer এবং কিছু unsafe function-এ কল ব্যবহার করে `split_at_mut`-এর implementation কাজ করানো যায়।

<Listing number="20-6" caption="Using unsafe code in the implementation of the `split_at_mut` function">

```rust
use std::slice;

fn split_at_mut(values: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
    let len = values.len();
    let ptr = values.as_mut_ptr();

    assert!(mid <= len);

    unsafe {
        (
            slice::from_raw_parts_mut(ptr, mid),
            slice::from_raw_parts_mut(ptr.add(mid), len - mid),
        )
    }
}
```

</Listing>

Chapter 4-এর [“The Slice Type”][the-slice-type]<!-- ignore --> section থেকে মনে করো যে একটি slice হলো কিছু data-র একটি pointer এবং slice-টির length। আমরা একটি slice-এর length পেতে `len` method ব্যবহার করি এবং একটি slice-এর raw pointer access করতে `as_mut_ptr` method ব্যবহার করি। এই ক্ষেত্রে, যেহেতু আমাদের কাছে `i32` value-র একটি mutable slice আছে, `as_mut_ptr` একটি raw pointer যার type `*mut i32`, যা আমরা `ptr` variable-এ store করেছি।

আমরা এই assertion রেখেছি যে `mid` index-টি slice-এর ভেতরে আছে। তারপর, আমরা unsafe code-এ যাই: `slice::from_raw_parts_mut` function একটি raw pointer এবং একটি length নেয়, এবং একটি slice তৈরি করে। আমরা এই function ব্যবহার করে এমন একটি slice তৈরি করি যা `ptr` থেকে শুরু হয় এবং `mid` সংখ্যক item দীর্ঘ। তারপর, আমরা `ptr`-এর উপর `add` method কল করি `mid` argument দিয়ে এমন একটি raw pointer পেতে যা `mid` থেকে শুরু হয়, এবং আমরা সেই pointer এবং `mid`-এর পরের বাকি item-এর সংখ্যা length হিসেবে ব্যবহার করে একটি slice তৈরি করি।

`slice::from_raw_parts_mut` function unsafe কারণ এটি একটি raw pointer নেয় এবং এই pointer-টি valid তা trust করতে হয়। Raw pointer-এর `add` method-টিও unsafe কারণ এটি trust করতে হয় যে offset location-টিও একটি valid pointer। সুতরাং, আমাদের `slice::from_raw_parts_mut` এবং `add`-এ কল-এর চারপাশে একটি `unsafe` block রাখতে হয়েছিল যাতে আমরা সেগুলো কল করতে পারি। Code-টি দেখে এবং `mid` অবশ্যই `len`-এর সমান বা ছোট তা assert করার মাধ্যমে, আমরা বলতে পারি যে `unsafe` block-এর ভেতরে ব্যবহৃত সব raw pointer slice-এর ভেতরের data-র valid pointer হবে। এটি `unsafe`-এর একটি গ্রহণযোগ্য এবং উপযুক্ত ব্যবহার।

খেয়াল করো যে আমাদের result `split_at_mut` function-টিকে `unsafe` হিসেবে mark করার প্রয়োজন নেই, এবং আমরা এই function কে safe Rust থেকে কল করতে পারি। আমরা একটি safe abstraction তৈরি করেছি unsafe code-এর চারপাশে যেখানে function-টির implementation `unsafe` code ব্যবহার করে safe ভাবে, কারণ এটি শুধুমাত্র এই function-এর access থাকা data থেকে valid pointer তৈরি করে।

এর বিপরীতে, Listing 20-7-এ `slice::from_raw_parts_mut`-এর ব্যবহার সম্ভবত slice ব্যবহারের সময় crash করবে। এই code একটি স্বেচ্ছাচারী memory location নেয় এবং ১০,০০০ item দীর্ঘ একটি slice তৈরি করে।

<Listing number="20-7" caption="Creating a slice from an arbitrary memory location">

```rust
    use std::slice;

    let address = 0x01234usize;
    let r = address as *mut i32;

    let values: &[i32] = unsafe { slice::from_raw_parts_mut(r, 10000) };
```

</Listing>

আমরা এই স্বেচ্ছাচারী location-এর memory-র মালিক নই, এবং এই code যে slice তৈরি করে তাতে valid `i32` value আছে তার কোনো guarantee নেই। `values`-কে একটি valid slice-এর মতো ব্যবহার করার চেষ্টা undefined behavior ঘটায়।

#### Using `extern` Functions to Call External Code

মাঝে মাঝে তোমার Rust code-এর অন্য language-এ লেখা code-এর সাথে interact করা প্রয়োজন হতে পারে। এর জন্য, Rust-এ `extern` keyword আছে যা একটি _Foreign Function Interface (FFI)_ create এবং use করতে সাহায্য করে, যা একটি programming language-কে function define করতে এবং অন্য (foreign) programming language-কে সেই function কল করতে দেয়।

Listing 20-8 দেখায় কীভাবে C standard library থেকে `abs` function-এর সাথে একটি integration set up করতে হয়। `extern` block-এর ভেতরে declared function-গুলো Rust code থেকে কল করা সাধারণত unsafe, তাই `extern` block-গুলোও `unsafe` হিসেবে mark করতে হয়। কারণ হলো অন্যান্য language Rust-এর rule এবং guarantee enforce করে না, এবং Rust সেগুলো check করতে পারে না, তাই safety নিশ্চিত করার দায়িত্ব programmer-এর উপর পড়ে।

<Listing number="20-8" file-name="src/main.rs" caption="Declaring and calling an `extern` function defined in another language">

```rust
unsafe extern "C" {
    fn abs(input: i32) -> i32;
}

fn main() {
    unsafe {
        println!("Absolute value of -3 according to C: {}", abs(-3));
    }
}
```

</Listing>

`unsafe extern "C"` block-এর ভেতরে, আমরা অন্য language থেকে কল করতে চাই এমন external function-গুলোর নাম এবং signature list করি। `"C"` অংশটি define করে যে external function-টি কোন _application binary interface (ABI)_ ব্যবহার করে: ABI define করে কীভাবে assembly level-এ function-টি কল করতে হয়। `"C"` ABI সবচেয়ে common এবং C programming language-এর ABI অনুসরণ করে। Rust যে সব ABI support করে তার সম্পর্কে information [the Rust Reference][ABI]-এ পাওয়া যায়।

একটি `unsafe extern` block-এর ভেতরে declare করা প্রতিটি item implicitly unsafe। যাইহোক, কিছু FFI function call করা *safe*। উদাহরণস্বরূপ, C-এর standard library থেকে `abs` function-এর কোনো memory safety consideration নেই, এবং আমরা জানি এটি যেকোনো `i32` দিয়ে কল করা যেতে পারে। এমন ক্ষেত্রে, আমরা `safe` keyword ব্যবহার করে বলতে পারি যে এই নির্দিষ্ট function-টি safe এটি একটি `unsafe extern` block-এ থাকা সত্ত্বেও। এই change করার পর, এটি কল করার জন্য আর কোনো `unsafe` block-এর প্রয়োজন নেই, যেমন Listing 20-9-এ দেখানো হয়েছে।

<Listing number="20-9" file-name="src/main.rs" caption="Explicitly marking a function as `safe` within an `unsafe extern` block and calling it safely">

```rust
unsafe extern "C" {
    safe fn abs(input: i32) -> i32;
}

fn main() {
    println!("Absolute value of -3 according to C: {}", abs(-3));
}
```

</Listing>

একটি function-কে `safe` হিসেবে mark করা এটিকে inherently safe বানায় না! বরং, এটি এমন একটি promise-এর মতো যা তুমি Rust-কে দিচ্ছো যে এটি safe। এই promise রক্ষা করা তোমার দায়িত্ব!

#### Calling Rust Functions from Other Languages

আমরা `extern` ব্যবহার করে এমন একটি interface তৈরি করতে পারি যা অন্য language-কে Rust function কল করতে দেয়। একটি পুরো `extern` block তৈরি করার পরিবর্তে, আমরা প্রাসঙ্গিক function-টির `fn` keyword-এর ঠিক আগে `extern` keyword যোগ করি এবং কোন ABI ব্যবহার করবে তা specify করি। আমাদের একটি `#[unsafe(no_mangle)]` annotation যোগ করতে হবে যাতে Rust compiler-কে বলা যায় এই function-টির নাম mangle না করতে। _Mangling_ হলো যখন একটি compiler আমরা যে নাম function দিয়েছি তাকে ভিন্ন একটি নামে পরিবর্তন করে যা compilation process-এর অন্যান্য অংশ consume করার জন্য আরও বেশি information ধারণ করে কিন্তু মানুষের পড়ার জন্য কম সহজ। প্রতিটি programming language compiler-ই সামান্য ভিন্নভাবে নাম mangle করে, তাই অন্য কোনো language দ্বারা একটি Rust function-কে nameable করতে, আমাদের Rust compiler-এর name mangling disable করতে হবে। এটি unsafe কারণ built-in mangling ছাড়া library-জুড়ে name collision হতে পারে, তাই যে নাম আমরা choose করি তা mangle না করে export করা safe তা নিশ্চিত করা আমাদের দায়িত্ব।

নিচের উদাহরণে, আমরা `call_from_c` function-টিকে C code থেকে accessible করি, এটিকে একটি shared library-তে compile করে C থেকে link করার পর:

```
#[unsafe(no_mangle)]
pub extern "C" fn call_from_c() {
    println!("Just called a Rust function from C!");
}
```

`extern`-এর এই ব্যবহারে `unsafe` শুধু attribute-এ প্রয়োজন, `extern` block-এ নয়।

### Accessing or Modifying a Mutable Static Variable

এই book-এ আমরা এখনো global variable নিয়ে কথা বলিনি, যা Rust support করে কিন্তু Rust-এর ownership rule-এর সাথে সমস্যা হতে পারে। যদি দুটি thread একই mutable global variable access করে, তবে এটি একটি data race ঘটাতে পারে।

Rust-এ, global variable-কে _static_ variable বলা হয়। Listing 20-10 একটি string slice value-সহ একটি static variable-এর declaration এবং use-এর উদাহরণ দেখায়।

<Listing number="20-10" file-name="src/main.rs" caption="Defining and using an immutable static variable">

```rust
static HELLO_WORLD: &str = "Hello, world!";

fn main() {
    println!("value is: {HELLO_WORLD}");
}
```

</Listing>

Static variable গুলো constant-এর মতো, যা আমরা Chapter 3-এর [“Declaring Constants”][constants]<!-- ignore --> section-এ আলোচনা করেছি। Convention অনুযায়ী static variable-এর নাম `SCREAMING_SNAKE_CASE`-এ হয়। Static variable শুধুমাত্র `'static` lifetime-সহ reference store করতে পারে, যার মানে Rust compiler lifetime বের করতে পারে এবং আমাদের সেটি explicitly annotate করার প্রয়োজন নেই। একটি immutable static variable access করা safe।

Constant এবং immutable static variable-এর মধ্যে একটি সূক্ষ্ম পার্থক্য হলো static variable-এর value-র memory-তে একটি fixed address থাকে। Value ব্যবহার করলে সবসময় একই data access করা হবে। অন্যদিকে, constant-কে তাদের ব্যবহারের সময় data duplicate করার অনুমতি দেওয়া হয়। আরেকটি পার্থক্য হলো static variable mutable হতে পারে। Mutable static variable access এবং modify করা _unsafe_। Listing 20-11 দেখায় কীভাবে `COUNTER` নামের একটি mutable static variable declare, access এবং modify করতে হয়।

<Listing number="20-11" file-name="src/main.rs" caption="Reading from or writing to a mutable static variable is unsafe.">

```rust
static mut COUNTER: u32 = 0;

/// SAFETY: Calling this from more than a single thread at a time is undefined
/// behavior, so you *must* guarantee you only call it from a single thread at
/// a time.
unsafe fn add_to_count(inc: u32) {
    unsafe {
        COUNTER += inc;
    }
}

fn main() {
    unsafe {
        // SAFETY: This is only called from a single thread in `main`.
        add_to_count(3);
        println!("COUNTER: {}", *(&raw const COUNTER));
    }
}
```

</Listing>

Regular variable-এর মতো, আমরা `mut` keyword ব্যবহার করে mutability specify করি। `COUNTER` থেকে read বা write করা যেকোনো code অবশ্যই একটি `unsafe` block-এর ভেতরে থাকতে হবে। Listing 20-11-এর code compile হয় এবং আমরা যেমন আশা করবো তেমনি `COUNTER: 3` print করে কারণ এটি single threaded। একাধিক thread `COUNTER` access করলে সম্ভবত data race হবে, তাই এটি undefined behavior। সুতরাং, আমাদের পুরো function-টিকে `unsafe` হিসেবে mark করতে হবে এবং safety limitation document করতে হবে যাতে function-টি কল করা যে কেউ জানে তারা কী করতে পারে এবং কী করতে পারে না।

যখনই আমরা একটি unsafe function লিখি, একটি `SAFETY` দিয়ে শুরু হওয়া comment লেখা এবং ব্যাখ্যা করা যে caller-কে function-টি safely কল করতে কী করতে হবে তা idiomatic। একইভাবে, যখনই আমরা একটি unsafe operation সম্পাদন করি, একটি `SAFETY` দিয়ে শুরু হওয়া comment লেখা যাতে ব্যাখ্যা করা হয় যে safety rule-গুলো কীভাবে uphold করা হচ্ছে তা idiomatic।

এছাড়াও, compiler ডিফল্টরূপে একটি compiler lint-এর মাধ্যমে mutable static variable-এ reference তৈরি করার যেকোনো attempt deny করবে। তোমাকে হয় একটি `#[allow(static_mut_refs)]` annotation যোগ করে সেই lint-এর protection থেকে explicitly বেরিয়ে আসতে হবে অথবা raw borrow operator-এর একটি দিয়ে তৈরি একটি raw pointer-এর মাধ্যমে mutable static variable access করতে হবে। এর মধ্যে এমন ক্ষেত্রও রয়েছে যেখানে reference অদৃশ্যভাবে তৈরি হয়, যেমন এই code listing-এ `println!`-এ ব্যবহৃত হলে। Static mutable variable-এর reference-গুলো raw pointer দিয়ে তৈরি করা প্রয়োজন তাদের ব্যবহারের safety requirement-গুলো আরও স্পষ্ট করে তোলে।

Globally accessible mutable data-র সাথে, এটি নিশ্চিত করা কঠিন যে কোনো data race নেই, যে কারণে Rust mutable static variable-কে unsafe বিবেচনা করে। যেখানে সম্ভব, Chapter 16-এ আলোচনা করা concurrency technique এবং thread-safe smart pointer ব্যবহার করা অধিক পছন্দনীয় যাতে compiler check করে যে বিভিন্ন thread থেকে data access নিরাপদে করা হচ্ছে।

### Implementing an Unsafe Trait

আমরা `unsafe` ব্যবহার করে একটি unsafe trait implement করতে পারি। একটি trait unsafe হয় যখন এর অন্তত একটি method-এর এমন কোনো invariant থাকে যা compiler verify করতে পারে না। আমরা একটি trait-কে `unsafe` declare করি `trait`-এর আগে `unsafe` keyword যোগ করে এবং trait-এর implementation-কেও `unsafe` হিসেবে mark করে, যেমন Listing 20-12-তে দেখানো হয়েছে।

<Listing number="20-12" caption="Defining and implementing an unsafe trait">

```rust
unsafe trait Foo {
    // methods go here
}

unsafe impl Foo for i32 {
    // method implementations go here
}
```

</Listing>

`unsafe impl` ব্যবহার করে, আমরা promise করছি যে আমরা compiler যে invariant-গুলো verify করতে পারে না সেগুলো uphold করব।

একটি উদাহরণ হিসেবে, Chapter 16-এর [“Extensible Concurrency with `Send` and `Sync`”][send-and-sync]<!-- ignore --> section-এ আলোচিত `Send` এবং `Sync` marker trait-গুলো মনে করো: আমাদের type-গুলো যদি সম্পূর্ণভাবে এমন অন্যান্য type দিয়ে গঠিত যেগুলো `Send` এবং `Sync` implement করে, তবে compiler স্বয়ংক্রিয়ভাবে এই trait-গুলো implement করে। যদি আমরা এমন একটি type implement করি যা `Send` বা `Sync` implement না করে এমন কোনো type contain করে, যেমন raw pointer, এবং আমরা সেই type-টিকে `Send` বা `Sync` হিসেবে mark করতে চাই, তবে আমাদের `unsafe` ব্যবহার করতে হবে। Rust verify করতে পারে না যে আমাদের type এই guarantee-গুলো uphold করে যে এটি thread জুড়ে safely send করা যায় বা একাধিক thread থেকে access করা যায়; সুতরাং, আমাদের এই check-গুলো ম্যানুয়ালি করতে হবে এবং `unsafe` দিয়ে তা নির্দেশ করতে হবে।

### Accessing Fields of a Union

শুধুমাত্র `unsafe` দিয়ে কাজ করে এমন শেষ action হলো union-এর field access করা। একটি *union* একটি `struct`-এর মতো, কিন্তু একটি নির্দিষ্ট instance-এ একসময়ে শুধুমাত্র একটি declared field ব্যবহৃত হয়। Union-গুলো প্রধানত C code-এর union-গুলোর সাথে interface করতে ব্যবহৃত হয়। Union field access করা unsafe কারণ Rust guarantee করতে পারে না যে union instance-এ বর্তমানে store করা data-র type কী। Union সম্পর্কে আরও তুমি [the Rust Reference][unions]-এ শিখতে পারো।

### Using Miri to Check Unsafe Code

Unsafe code লেখার সময়, তুমি হয়তো check করতে চাইবে যে তুমি যা লিখেছ তা আসলেই safe এবং correct। এটি করার অন্যতম সেরা উপায় হলো Miri ব্যবহার করা, যা undefined behavior detect করার জন্য একটি official Rust tool। যেখানে borrow checker একটি _static_ tool যা compile time-এ কাজ করে, Miri হলো একটি _dynamic_ tool যা runtime-এ কাজ করে। এটি তোমার program বা এর test suite run করে এবং Rust-এর কাজ করার নিয়ম সম্পর্কে যা সে বোঝে তা ভঙ্গ করলে detect করে তোমার code check করে।

Miri ব্যবহার করতে Rust-এর একটি nightly build প্রয়োজন (যা সম্পর্কে আমরা [Appendix G: How Rust is Made and “Nightly Rust”][nightly]<!-- ignore -->-এ আরও কথা বলেছি)। তুমি `rustup
+nightly component add miri` টাইপ করে Rust-এর একটি nightly version এবং Miri tool দুটোই install করতে পারো। এটি তোমার project কোন version-এর Rust ব্যবহার করে তা পরিবর্তন করে না; এটি শুধু তোমার system-এ tool-টি যোগ করে যাতে তুমি চাইলে এটি ব্যবহার করতে পারো। তুমি একটি project-এ Miri `cargo +nightly miri run` বা `cargo +nightly miri test` টাইপ করে run করতে পারো।

এটি কতটা helpful হতে পারে তার একটি উদাহরণের জন্য, ভাবো যখন আমরা এটি Listing 20-7-এর বিরুদ্ধে run করি তখন কী হয়।

```console
$ cargo +nightly miri run
   Compiling unsafe-example v0.1.0 (file:///projects/unsafe-example)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.17s
     Running `file:///home/.rustup/toolchains/nightly/bin/cargo-miri runner target/miri/debug/unsafe-example`
warning: integer-to-pointer cast
 --> src/main.rs:5:13
  |
5 |     let r = address as *mut i32;
  |             ^^^^^^^^^^^^^^^^^^^ integer-to-pointer cast
  |
  = help: this program is using integer-to-pointer casts or (equivalently) `ptr::with_exposed_provenance`, which means that Miri might miss pointer bugs in this program
  = help: see https://doc.rust-lang.org/nightly/std/ptr/fn.with_exposed_provenance.html for more details on that operation
  = help: to ensure that Miri does not miss bugs in your program, use Strict Provenance APIs (https://doc.rust-lang.org/nightly/std/ptr/index.html#strict-provenance, https://crates.io/crates/sptr) instead
  = help: you can then set `MIRIFLAGS=-Zmiri-strict-provenance` to ensure you are not relying on `with_exposed_provenance` semantics
  = help: alternatively, `MIRIFLAGS=-Zmiri-permissive-provenance` disables this warning

error: Undefined Behavior: constructing invalid value of type &mut [i32]: encountered a dangling reference (0x1234[noalloc] has no provenance)
 --> src/main.rs:7:35
  |
7 |     let values: &[i32] = unsafe { slice::from_raw_parts_mut(r, 10000) };
  |                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Undefined Behavior occurred here
  |
  = help: this indicates a bug in the program: it performed an invalid operation, and caused Undefined Behavior
  = help: see https://doc.rust-lang.org/nightly/reference/behavior-considered-undefined.html for further information

note: some details are omitted, run with `MIRIFLAGS=-Zmiri-backtrace=full` for a verbose backtrace

error: aborting due to 1 previous error; 1 warning emitted
```

Miri সঠিকভাবে আমাদের warn করে যে আমরা একটি integer-কে pointer-এ cast করছি, যা একটি সমস্যা হতে পারে, কিন্তু Miri নির্ধারণ করতে পারে না কোনো সমস্যা আছে কি না কারণ সে জানে না pointer-টি কীভাবে তৈরি হয়েছে। তারপর, Miri একটি error return করে যেখানে Listing 20-7-তে undefined behavior আছে কারণ আমাদের একটি dangling pointer আছে। Miri-এর জন্য, আমরা এখন জানি যে undefined behavior-এর ঝুঁকি আছে, এবং আমরা ভাবতে পারি কীভাবে code-টিকে safe করা যায়। কিছু ক্ষেত্রে, Miri এমনকি error fix করার বিষয়ে recommendation-ও দিতে পারে।

Miri unsafe code লেখার সময় তোমার যে সব ভুল হতে পারে সবগুলো catch করে না। Miri একটি dynamic analysis tool, তাই এটি শুধুমাত্র এমন code-এর সমস্যা catch করে যা আসলে run হয়। এর মানে হলো তোমাকে এটি ভালো testing technique-এর সাথে একসাথে ব্যবহার করতে হবে যাতে তুমি যে unsafe code লিখেছ তা সম্পর্কে তোমার confidence বাড়ে। Miri তোমার code-এর unsound হওয়ার প্রতিটি সম্ভাব্য উপায়ও cover করে না।

অন্য কথায়: যদি Miri _একটি সমস্যা_ catch করে, তুমি জানো যে একটি bug আছে, কিন্তু শুধু কারণ Miri একটি bug _catch_ করে না তার মানে এই নয় যে কোনো সমস্যা নেই। যাইহোক, এটি অনেক কিছু catch করতে পারে। এই chapter-এ unsafe code-এর অন্যান্য উদাহরণগুলোতে এটি run করার চেষ্টা করো এবং দেখো এটি কী বলে!

Miri সম্পর্কে তুমি [এর GitHub repository][miri]-তে আরও জানতে পারো।

<!-- Old headings. Do not remove or links may break. -->

<a id="when-to-use-unsafe-code"></a>

### Using Unsafe Code Correctly

আলোচিত পাঁচটি superpower-এর একটি ব্যবহার করতে `unsafe` ব্যবহার করা ভুল নয় বা এটি নিরুৎসাহিতও করা হয় না, কিন্তু `unsafe` code সঠিকভাবে পাওয়া trickier কারণ compiler memory safety uphold করতে সাহায্য করতে পারে না। যখন তোমার `unsafe` code ব্যবহার করার কারণ থাকে, তুমি তা করতে পারো, এবং explicit `unsafe` annotation থাকায় সমস্যা ঘটলে তার source খুঁজে বের করা সহজ হয়। যখনই তুমি unsafe code লেখো, তুমি Miri ব্যবহার করতে পারো যাতে তুমি যা লিখেছ তা Rust-এর rule uphold করে তা নিশ্চিত করতে আরও বেশি confident হতে পারো।

Unsafe Rust-এর সাথে effectively কীভাবে কাজ করতে হয় তার আরও গভীর exploration-এর জন্য, Rust-এর `unsafe`-এর official guide [The Rustonomicon][nomicon] পড়ো।

[dangling-references]: ch04-02-references-and-borrowing.html#dangling-references
[ABI]: ../reference/items/external-blocks.html#abi
[constants]: ch03-01-variables-and-mutability.html#declaring-constants
[send-and-sync]: ch16-04-extensible-concurrency-sync-and-send.html
[the-slice-type]: ch04-03-slices.html#the-slice-type
[unions]: ../reference/items/unions.html
[miri]: https://github.com/rust-lang/miri
[editions]: appendix-05-editions.html
[nightly]: appendix-07-nightly-rust.html
[nomicon]: https://doc.rust-lang.org/nomicon/

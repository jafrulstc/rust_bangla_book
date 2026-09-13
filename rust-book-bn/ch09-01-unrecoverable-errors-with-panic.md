## `panic!` দিয়ে Unrecoverable Error

মাঝে মাঝে তোমার code-এ এমন খারাপ কিছু ঘটে যার কিছুই তুমি করতে পারো না। এই ক্ষেত্রে Rust-এ আছে `panic!` macro। বাস্তবে দুটি উপায়ে panic ঘটানো যায়: এমন কোনো কাজ করা যা আমাদের code-কে panic করে দেয় (যেমন একটি array-এর শেষের বাইরে অ্যাক্সেস করা) অথবা স্পষ্টভাবে `panic!` macro call করা। দুই ক্ষেত্রেই আমরা আমাদের program-এ একটি panic ঘটাচ্ছি। ডিফল্টভাবে, এই panic গুলো একটি failure message প্রিন্ট করে, stack থেকে unwind করে, clean up করে এবং প্রোগ্রাম থেকে বেরিয়ে যায়। একটি environment variable-এর মাধ্যমে তুমি Rust-কে দেখাতে পারো যেন panic ঘটলে call stack দেখায়, যাতে panic-এর উৎস খুঁজে বের করা সহজ হয়।

> ### Unwinding the Stack বা Aborting in Response to a Panic
>
> ডিফল্টভাবে, যখন একটি panic ঘটে, program _unwinding_ শুরু করে, যার অর্থ হল Rust stack ধরে উপরের দিকে ফিরে যায় এবং যেসব function-এর মুখোমুখি হয় তাদের প্রতিটির data clean up করে। কিন্তু পিছনে ফিরে যাওয়া এবং clean up করা বেশ ভারী কাজ। তাই Rust তোমাকে সরাসরি _aborting_-এর বিকল্প বেছে নেওয়ার সুযোগ দেয়, যা clean up না করেই program শেষ করে দেয়।
>
> Program যে memory ব্যবহার করছিল সেটি তারপর operating system-কে clean up করতে হবে। তোমার project-এ যদি তৈরি হওয়া binary-কে যত সম্ভব ছোট করতে হয়, তবে তুমি তোমার _Cargo.toml_ file-এর উপযুক্ত `[profile]` section-এ `panic = 'abort'` যোগ করে একটি panic-এ unwind করার বদলে abort করায় পরিবর্তন করতে পারো। যেমন, যদি release mode-এ panic হলে abort করতে চাও, তবে এটি যোগ করো:
>
> ```toml
> [profile.release]
> panic = 'abort'
> ```

একটি সাধারণ program-এ `panic!` call করে দেখি:

<Listing file-name="src/main.rs">

```rust,should_panic,panics
fn main() {
    panic!("crash and burn");
}
```

</Listing>

Program-টি run করলে তুমি এমন কিছু দেখবে:

```console
$ cargo run
   Compiling panic v0.1.0 (file:///projects/panic)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.25s
     Running `target/debug/panic`

thread 'main' (6018279) panicked at src/main.rs:2:5:
crash and burn
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

`panic!`-এ করা call-ই শেষ দুটি লাইনে থাকা error message-এর কারণ। প্রথম লাইনটি আমাদের panic message এবং আমাদের source code-এর সেই স্থান দেখায় যেখানে panic ঘটেছে: _src/main.rs:2:5_ নির্দেশ করে যে এটি আমাদের _src/main.rs_ file-এর দ্বিতীয় লাইনের পঞ্চম character।

এই ক্ষেত্রে, উল্লেখিত লাইনটি আমাদের code-এর অংশ, আর সেই লাইনে গেলে আমরা `panic!` macro call দেখতে পাব। আরেক ক্ষেত্রে, `panic!` call এমন code-এ থাকতে পারে যা আমাদের code call করে, তখন error message-এ রিপোর্ট করা filename ও লাইন নম্বর হবে অন্য কারো code-এর, যেখানে `panic!` macro call করা হয়েছে—আমাদের code-এর সেই লাইন নয় যা শেষ পর্যন্ত `panic!` call-এর কারণ হয়েছে।

<!-- Old headings. Do not remove or links may break. -->

<a id="using-a-panic-backtrace"></a>

আমরা `panic!` call যেসব function থেকে এসেছে সেগুলোর backtrace ব্যবহার করে বের করতে পারি যে আমাদের code-এর কোন অংশটি সমস্যার কারণ। `panic!` backtrace কীভাবে ব্যবহার করতে হয় তা বোঝার জন্য, চলো আরেকটি উদাহরণ দেখি এবং দেখি কেমন হয় যখন আমাদের code সরাসরি macro call না করে আমাদের code-এর একটি bug-এর কারণে একটি library থেকে `panic!` call আসে। Listing 9-1-এ এমন কিছু code আছে যা একটি vector-এ বৈধ index-এর সীমার বাইরের একটি index অ্যাক্সেস করার চেষ্টা করে।

<Listing number="9-1" file-name="src/main.rs" caption="Attempting to access an element beyond the end of a vector, which will cause a call to `panic!`">

```rust,should_panic,panics
fn main() {
    let v = vec![1, 2, 3];

    v[99];
}
```

</Listing>

এখানে, আমরা আমাদের vector-এর ১০০তম element অ্যাক্সেস করার চেষ্টা করছি (যা index ৯৯-এ আছে কারণ indexing শূন্য থেকে শুরু হয়), কিন্তু vector-এ মাত্র তিনটি element আছে। এই পরিস্থিতিতে, Rust panic করবে। `[]` দিয়ে একটি element return করার কথা, কিন্তু তুমি যদি একটি অবৈধ index পাস করো, তবে এমন কোনো element নেই যা Rust এখানে return করতে পারে যা সঠিক হবে।

C-তে, একটি data structure-এর শেষের বাইরে পড়ার চেষ্টা করা হলো undefined behavior। তুমি memory-তে এমন একটি অবস্থানে যা কিছু আছে তা পেতে পারো যা data structure-এর ওই element-এর সাথে মিলে যায়, যদিও সেই memory-টি ওই structure-এর নয়। একে _buffer overread_ বলা হয় এবং যদি কোনো attacker এমনভাবে index পরিবর্তন করতে পারে যে সে data structure-এর পরে সংরক্ষিত এমন data পড়তে পারে যা সে পড়ার অনুমতি পাওয়ার কথা নয়, তবে এটি security vulnerability তৈরি করতে পারে।

তোমার program-কে এ ধরনের vulnerability থেকে রক্ষা করতে, তুমি যদি এমন কোনো index-এ element পড়ার চেষ্টা করো যা নেই, Rust execution থামিয়ে দেবে এবং চালিয়ে যেতে অস্বীকার করবে। চলো চেষ্টা করে দেখি:

```console
$ cargo run
   Compiling panic v0.1.0 (file:///projects/panic)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.27s
     Running `target/debug/panic`

thread 'main' (6017887) panicked at src/main.rs:4:6:
index out of bounds: the len is 3 but the index is 99
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

এই error-টি আমাদের _main.rs_-এর ৪ নম্বর লাইনটি নির্দেশ করে, যেখানে আমরা `v` vector-এর index ৯৯ অ্যাক্সেস করার চেষ্টা করেছি।

`note:` লাইনটি আমাদের জানায় যে আমরা `RUST_BACKTRACE` environment variable সেট করে ঠিক কী ঘটেছিল যা error-এর কারণ হয়েছিল তার একটি backtrace পেতে পারি। একটি _backtrace_ হল সেই সমস্ত function-এর একটি তালিকা যেগুলো এই পর্যন্ত পৌঁছাতে call করা হয়েছে। Rust-এ backtrace অন্যান্য language-এর মতোই কাজ করে: backtrace পড়ার মূল বিষয় হল উপর থেকে শুরু করে পড়তে থাকা যতক্ষণ না তুমি নিজে লেখা file দেখতে পাও। সেটিই সেই জায়গা যেখানে সমস্যার উৎপত্তি। ওই জায়গার উপরের লাইনগুলো হল সেই code যা তোমার code call করেছে; নিচের লাইনগুলো হল সেই code যা তোমার code-কে call করেছে। এই আগের ও পরের লাইনগুলোতে core Rust code, standard library code, অথবা তুমি যেসব crate ব্যবহার করছ সেগুলো থাকতে পারে। চলো `RUST_BACKTRACE` environment variable-কে `0` ছাড়া অন্য যেকোনো মান সেট করে একটি backtrace পাওয়ার চেষ্টা করি। Listing 9-2 তোমার দেখা output-এর মতো একটি output দেখায়।

<!-- manual-regeneration
cd listings/ch09-error-handling/listing-09-01
RUST_BACKTRACE=1 cargo run
copy the backtrace output below
check the backtrace number mentioned in the text below the listing
-->

<Listing number="9-2" caption="The backtrace generated by a call to `panic!` displayed when the environment variable `RUST_BACKTRACE` is set">

```console
$ RUST_BACKTRACE=1 cargo run
thread 'main' panicked at src/main.rs:4:6:
index out of bounds: the len is 3 but the index is 99
stack backtrace:
   0: rust_begin_unwind
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/std/src/panicking.rs:692:5
   1: core::panicking::panic_fmt
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:75:14
   2: core::panicking::panic_bounds_check
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:273:5
   3: <usize as core::slice::index::SliceIndex<[T]>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:274:10
   4: core::slice::index::<impl core::ops::index::Index<I> for [T]>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:16:9
   5: <alloc::vec::Vec<T,A> as core::ops::index::Index<I>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/alloc/src/vec/mod.rs:3361:9
   6: panic::main
             at ./src/main.rs:4:6
   7: core::ops::function::FnOnce::call_once
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/ops/function.rs:250:5
note: Some details are omitted, run with `RUST_BACKTRACE=full` for a verbose backtrace.
```

</Listing>

বেশ বড় output! তোমার দেখা exact output তোমার operating system এবং Rust version-অনুসারে ভিন্ন হতে পারে। এই তথ্যসহ backtrace পেতে হলে debug symbol enable থাকতে হবে। `--release` flag ছাড়া `cargo build` বা `cargo run` করলে debug symbol ডিফল্টভাবে enable থাকে, যেমন আমরা এখানে করেছি।

Listing 9-2-এর output-এ, backtrace-এর ৬ নম্বর লাইনটি আমাদের project-এর সেই লাইনটি নির্দেশ করে যা সমস্যার কারণ: _src/main.rs_-এর ৪ নম্বর লাইন। যদি আমরা না চাই যে আমাদের program panic করুক, তবে আমাদের তদন্ত শুরু করা উচিত এমন প্রথম লাইন দ্বারা উল্লেখিত স্থান থেকে যেখানে আমরা লেখা একটি file-এর কথা বলা হয়েছে। Listing 9-1-এ, যেখানে আমরা ইচ্ছাকৃতভাবে এমন code লিখেছি যা panic করবে, panic ঠিক করার উপায় হলো vector index-এর সীমার বাইরের কোনো element না চাওয়া। ভবিষ্যতে তোমার code যখন panic করবে, তুমি বের করতে হবে যে code কোন কাজটি করছে এবং কী value-এর সাথে সেটা panic ঘটাচ্ছে এবং code-টির পরিবর্তে কী করা উচিত ছিল।

আমরা এই অধ্যায়ের শেষে [“To `panic!` or Not to
`panic!`”][to-panic-or-not-to-panic]<!-- ignore --> section-এ ফিরে যাব এবং `panic!` কখন error condition handle করতে ব্যবহার করা উচিত আর কখন নয় তা নিয়ে আলোচনা করব। এর পরে, আমরা দেখব কীভাবে `Result` ব্যবহার করে একটি error থেকে recover করা যায়।

[to-panic-or-not-to-panic]: ch09-03-to-panic-or-not-to-panic.html#to-panic-or-not-to-panic

## একটি Enum Define করা

যেখানে struct তোমাকে সম্পর্কিত fields এবং data একসাথে group করার সুযোগ দেয় — যেমন একটি `Rectangle` যার `width` এবং `height` field আছে — সেখানে enum তোমাকে বলার সুযোগ দেয় যে একটি value সম্ভাব্য কয়েকটি value-র মধ্যে একটি। উদাহরণস্বরূপ, আমরা হয়তো বলতে চাই যে `Rectangle` হলো সম্ভাব্য shape-গুলোর একটি সেটের মধ্যে একটি, যে সেটে `Circle` এবং `Triangle`-ও আছে। এটা করার জন্য Rust আমাদের এই সম্ভাবনাগুলোকে একটি enum হিসেবে encode করতে দেয়।

চলো এমন একটি পরিস্থিতি দেখি যেটা আমরা হয়তো code-এ প্রকাশ করতে চাই এবং বুঝি কেন এই ক্ষেত্রে enum গুলো struct-এর চেয়ে বেশি উপযুক্ত ও কাজের। ধরো আমাদের IP address নিয়ে কাজ করতে হবে। বর্তমানে IP address-এর জন্য প্রধানত দুটি standard ব্যবহৃত হয়: version four এবং version six। যেহেতু আমাদের program-এ এই দুটি ছাড়া আর কোনো IP address আসার সম্ভাবনা নেই, তাই আমরা সব সম্ভাব্য variants গুলো _enumerate_ করতে পারি — enumeration নামটা এখান থেকেই এসেছে।

যেকোনো IP address হয় version four নয়তো version six হতে পারে, কিন্তু একই সময়ে দুটোই নয়। IP address-এর এই বৈশিষ্ট্যটির কারণে enum data structure টি উপযুক্ত, কারণ একটি enum value তার যেকোনো একটি variant-ই হতে পারে। Version four এবং version six — দুই ধরনের address-ই মূলত IP address, তাই যেসব ক্ষেত্রে যেকোনো ধরনের IP address-এর জন্য একই বিধান প্রযোজ্য, সেখানে এগুলোকে একই type হিসেবে বিবেচনা করা উচিত।

আমরা এই ধারণাটি code-এ প্রকাশ করতে পারি একটি `IpAddrKind` enumeration define করে এবং এর সম্ভাব্য ধরনগুলো — `V4` এবং `V6` — তালিকাবদ্ধ করে। এগুলোই ঐ enum-এর variants:

```rust
enum IpAddrKind {
    V4,
    V6,
}
```

`IpAddrKind` এখন একটি custom data type যা আমরা আমাদের code-এর অন্যত্র ব্যবহার করতে পারি।

### Enum Values

আমরা `IpAddrKind`-এর দুটি variant-এর প্রতিটির instance এভাবে তৈরি করতে পারি:

```rust
    let four = IpAddrKind::V4;
    let six = IpAddrKind::V6;
```

খেয়াল করো যে enum-এর variants গুলো তার identifier-এর অধীনে namespaced থাকে, এবং আমরা দুটোর মাঝে একটি double colon ব্যবহার করি। এটা কাজের, কারণ এখন `IpAddrKind::V4` এবং `IpAddrKind::V6` — দুটো value-ই একই type: `IpAddrKind`। তারপর আমরা, যেমন, এমন একটি function define করতে পারি যে যেকোনো `IpAddrKind` নেয়:

```rust
fn route(ip_kind: IpAddrKind) {}
```

এবং আমরা যেকোনো একটি variant দিয়ে এই function-টিকে call করতে পারি:

```rust
    route(IpAddrKind::V4);
    route(IpAddrKind::V6);
```

Enum ব্যবহারে আরও কিছু সুবিধা আছে। আমাদের IP address type-টি নিয়ে একটু ভাবলে দেখবো, এই মুহূর্তে আমাদের কাছে প্রকৃত IP address _data_ সংরক্ষণ করার কোনো উপায় নেই; আমরা শুধু জানি এটি কোন _kind_। যেহেতু তুমি Chapter 5-এ struct সম্পর্কে শিখেছো, তাই হয়তো Listing 6-1-এ দেখানোর মতো করে struct দিয়ে এই সমস্যা সমাধানে প্রলুব্ধ হতে পারো।

<Listing number="6-1" caption="একটি `struct` ব্যবহার করে IP address-এর data এবং `IpAddrKind` variant সংরক্ষণ করা">

```rust
    enum IpAddrKind {
        V4,
        V6,
    }

    struct IpAddr {
        kind: IpAddrKind,
        address: String,
    }

    let home = IpAddr {
        kind: IpAddrKind::V4,
        address: String::from("127.0.0.1"),
    };

    let loopback = IpAddr {
        kind: IpAddrKind::V6,
        address: String::from("::1"),
    };
```

</Listing>

এখানে আমরা একটি struct `IpAddr` define করেছি যার দুটি field আছে: একটি `kind` field যার type `IpAddrKind` (আগে যে enum-টি define করেছিলাম), এবং একটি `address` field যার type `String`। এই struct-এর আমাদের দুটি instance আছে। প্রথমটি হলো `home`, যার `kind` value হলো `IpAddrKind::V4` এবং সংশ্লিষ্ট address data হলো `127.0.0.1`। দ্বিতীয় instance-টি হলো `loopback`। এর `kind` value হলো `IpAddrKind`-এর অন্য variant, `V6`, এবং এর সাথে যুক্ত address হলো `::1`। আমরা একটি struct ব্যবহার করে `kind` এবং `address` value গুলো একসাথে bundle করেছি, তাই এখন variant-টি value-র সাথে যুক্ত হয়েছে।

তবে শুধু একটি enum ব্যবহার করেও একই ধারণা প্রকাশ করা যায়, আর সেটা বেশ concise: struct-এর ভেতরে enum রাখার বদলে আমরা সরাসরি প্রতিটি enum variant-এ data রাখতে পারি। `IpAddr` enum-এর এই নতুন definition-টি বলছে যে `V4` এবং `V6` — দুটি variant-ই একটি করে `String` value বহন করবে:

```rust
    enum IpAddr {
        V4(String),
        V6(String),
    }

    let home = IpAddr::V4(String::from("127.0.0.1"));

    let loopback = IpAddr::V6(String::from("::1"));
```

আমরা প্রতিটি enum variant-এর সাথে সরাসরি data যুক্ত করেছি, তাই একটি অতিরিক্ত struct-এর প্রয়োজন নেই। এখানে enum যেভাবে কাজ করে তার আরেকটি বিস্তারিত দিকও সহজে বোঝা যায়: আমরা যে প্রতিটি enum variant-এর নাম define করি, তা একই সাথে একটি function-এ পরিণত হয় যা ঐ enum-এর একটি instance তৈরি করে। অর্থাৎ, `IpAddr::V4()` হলো একটি function call যা একটি `String` argument নেয় এবং `IpAddr` type-এর একটি instance return করে। Enum-টি define করার ফলে আমরা স্বয়ংক্রিয়ভাবে এই constructor function-টি পেয়ে যাই।

Struct-এর বদলে enum ব্যবহারে আরও একটি সুবিধা আছে: প্রতিটি variant ভিন্ন ধরনের ও ভিন্ন পরিমাণে associated data বহন করতে পারে। Version four IP address-এ সবসময় চারটি numeric component থাকে যাদের value 0 থেকে 255 এর মধ্যে হয়। যদি আমরা `V4` address-গুলো চারটি `u8` value হিসেবে সংরক্ষণ করতে চাই কিন্তু `V6` address-গুলো একটি `String` value হিসেবেই প্রকাশ করতে চাই, তবে struct দিয়ে এটা করা সম্ভব হতো না। Enum এই ক্ষেত্রে খুব সহজেই কাজ সামলায়:

```rust
    enum IpAddr {
        V4(u8, u8, u8, u8),
        V6(String),
    }

    let home = IpAddr::V4(127, 0, 0, 1);

    let loopback = IpAddr::V6(String::from("::1"));
```

আমরা version four এবং version six IP address সংরক্ষণের জন্য data structure define করার বেশ কয়েকটি উপায় দেখলাম। তবে দেখা যাচ্ছে, IP address সংরক্ষণ করে তার ধরনও encode করার প্রয়োজন এত সাধারণ যে [standard library-তে এমন একটি definition আছেই যা আমরা ব্যবহার করতে পারি!][IpAddr]<!-- ignore --> চলো দেখি standard library কীভাবে `IpAddr` define করেছে। এতে ঠিক সেই enum এবং variants আছে যা আমরা define ও use করেছি, কিন্তু এটি address data-টি ভেতরে দুটি ভিন্ন struct-এর আকারে embed করে রেখেছে, যে দুটি struct প্রতিটি variant-এর জন্য ভিন্নভাবে define করা:

```rust
struct Ipv4Addr {
    // --snip--
}

struct Ipv6Addr {
    // --snip--
}

enum IpAddr {
    V4(Ipv4Addr),
    V6(Ipv6Addr),
}
```

এই code-টি দেখায় যে তুমি একটি enum variant-এ যেকোনো ধরনের data রাখতে পারো: string, numeric type, বা struct। এমনকি তুমি আরেকটি enum-ও রাখতে পারো! এছাড়া, standard library-র type গুলো প্রায়শই ততটা জটিল নয় যতটা তুমি নিজে ভাবতে পারো।

খেয়াল করো, standard library-তে `IpAddr`-এর একটি definition থাকা সত্ত্বেও আমরা নিজেদের নিজস্ব definition conflict ছাড়াই তৈরি করে use করতে পারি, কারণ আমরা standard library-র definition-টিকে আমাদের scope-এ আনিনি। Scope-এ type আনা নিয়ে আমরা Chapter 7-এ আরও আলোচনা করবো।

চলো Listing 6-2-তে আরেকটি enum-এর উদাহরণ দেখি: এইটির variants-এ বিচিত্র ধরনের type embed করা আছে।

<Listing number="6-2" caption="একটি `Message` enum যার প্রতিটি variant ভিন্ন পরিমাণ ও ধরনের value সংরক্ষণ করে">

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}
```

</Listing>

এই enum-এর চারটি variant ভিন্ন ধরনের:

- `Quit`: এর সাথে কোনো data-ই যুক্ত নেই
- `Move`: এর named field আছে, struct-এর মতো
- `Write`: একটি single `String` বহন করে
- `ChangeColor`: তিনটি `i32` value বহন করে

Listing 6-2-তে দেখানোর মতো variants সহ একটি enum define করা হলো ভিন্ন ধরনের কয়েকটি struct definition define করার মতোই, পার্থক্য শুধু এতটুকু যে enum `struct` keyword ব্যবহার করে না এবং সব variants একসাথে `Message` type-এর অধীনে grouped থাকে। নিচের struct গুলো ঠিক একই data ধরে রাখতে পারতো যা উপরের enum variants গুলো ধরে রাখে:

```rust
struct QuitMessage; // unit struct
struct MoveMessage {
    x: i32,
    y: i32,
}
struct WriteMessage(String); // tuple struct
struct ChangeColorMessage(i32, i32, i32); // tuple struct
```

কিন্তু আমরা যদি এই ভিন্ন ভিন্ন struct গুলো ব্যবহার করতাম, যাদের প্রতিটির নিজস্ব type আছে, তবে Listing 6-2-তে define করা `Message` enum-এর মতো সহজে এমন একটি function define করতে পারতাম না যে এই সব ধরনের message-এর যেকোনো একটিকে নেয় — কারণ `Message` একটি single type।

Enum এবং struct-এর মধ্যে আরও একটি মিল আছে: যেভাবে আমরা `impl` ব্যবহার করে struct-এ method define করতে পারি, ঠিক তেমনি enum-এও method define করতে পারি। এখানে একটি `call` নামের method দেওয়া হলো যা আমরা আমাদের `Message` enum-এ define করতে পারি:

```rust
    impl Message {
        fn call(&self) {
            // method body would be defined here
        }
    }

    let m = Message::Write(String::from("hello"));
    m.call();
```

Method-টির ভেতরের body তে `self` ব্যবহার করে আমরা সেই value-টি পাবো যার উপর আমরা method-টি call করেছি। এই উদাহরণে আমরা একটি variable `m` তৈরি করেছি যার value `Message::Write(String::from("hello"))`, এবং `m.call()` run হওয়ার সময় `call` method-এর body-তে `self`-এর value হবে এটিই।

চলো standard library-র আরেকটি enum দেখি যা খুব সাধারণ ও কাজের: `Option`।

<!-- Old headings. Do not remove or links may break. -->

<a id="the-option-enum-and-its-advantages-over-null-values"></a>

### `Option` Enum

এই section-টি `Option`-এর একটি case study দেখাবে, যা standard library কর্তৃক define করা আরেকটি enum। `Option` type এমন একটি অত্যন্ত সাধারণ পরিস্থিতি encode করে যেখানে একটি value হয় কিছু একটা হতে পারে নয়তো কিছুই না।

উদাহরণস্বরূপ, তুমি যদি একটি non-empty list-এর প্রথম item চাও, তবে একটি value পাবে। কিন্তু যদি খালি list-এর প্রথম item চাও, তবে কিছুই পাবে না। এই ধারণাটি type system-এর মাধ্যমে প্রকাশ করার অর্থ হলো compiler যাচাই করতে পারবে তুমি যেসব case handle করা উচিত সেগুলো কি handle করেছো কিনা; এই feature-টি অন্যান্য programming language-এ যে ধরনের bug খুব সাধারণ, তা প্রতিরোধে সাহায্য করে।

Programming language design সাধারণত এই ভাবে চিন্তা করা হয় যে তুমি কোন কোন feature যোগ করছো, কিন্তু তুমি কোন কোন feature বাদ দিচ্ছো সেটাও গুরুত্বপূর্ণ। Rust-এ অন্যান্য অনেক language-এর মতো null feature নেই। _Null_ হলো এমন একটি value যা বোঝায় সেখানে কোনো value-ই নেই। Null যুক্ত থাকা language-গুলোতে variable সবসময় দুটি state-এর একটিতে থাকতে পারে: null বা not-null।

Tony Hoare, null-এর উদ্ভাবক, তাঁর 2009 সালের "Null References: The Billion Dollar Mistake" নামক উপস্থাপনায় এই বলেছিলেন:

> I call it my billion-dollar mistake. At that time, I was designing the first
> comprehensive type system for references in an object-oriented language. My
> goal was to ensure that all use of references should be absolutely safe, with
> checking performed automatically by the compiler. But I couldn't resist the
> temptation to put in a null reference, simply because it was so easy to
> implement. This has led to innumerable errors, vulnerabilities, and system
> crashes, which have probably caused a billion dollars of pain and damage in
> the last forty years.

Null value-র সমস্যা হলো, তুমি যদি একটি null value-কে not-null value হিসেবে ব্যবহার করতে চাও, তবে কোনো না কোনো ধরনের error পাবে। যেহেতু এই null বা not-null বৈশিষ্ট্যটি সর্বত্র বিদ্যমান, তাই এই ধরনের error করা খুবই সহজ।

তবে null যে ধারণাটি প্রকাশ করতে চায় সেটি এখনও কাজের: একটি null হলো এমন একটি value যা বর্তমানে কোনো কারণে invalid বা absent।

সমস্যাটি আসলে ধারণার মধ্যে নয়, বরং এর নির্দিষ্ট implementation-এ। সেই কারণেই Rust-এ null নেই, কিন্তু এমন একটি enum আছে যা value-র উপস্থিত বা অনুপস্থিত ধারণাটি encode করতে পারে। এই enum-টি হলো `Option<T>`, যা standard library কর্তৃক [এভাবে define করা হয়েছে][option]<!-- ignore -->:

```rust
enum Option<T> {
    None,
    Some(T),
}
```

`Option<T>` enum-টি এতটাই কাজের যে এটি prelude-তেও অন্তর্ভুক্ত; তোমাকে এটিকে স্পষ্টভাবে scope-এ আনতে হয় না। এর variants-ও prelude-তে অন্তর্ভুক্ত: তুমি `Option::` prefix ছাড়াই সরাসরি `Some` এবং `None` ব্যবহার করতে পারো। `Option<T>` enum এখনও একটি সাধারণ enum-ই, এবং `Some(T)` এবং `None` এখনও `Option<T>` type-এর variants।

`<T>` syntax-টি একটি Rust feature যা সম্পর্কে আমরা এখনও কথা বলিনি। এটি একটি generic type parameter, এবং আমরা generics সম্পর্কে Chapter 10-এ বিস্তারিত আলোচনা করবো। আপাতত তোমার শুধু এটুকু জানা দরকার যে `<T>` বোঝায় `Option` enum-এর `Some` variant যেকোনো type-এর একটি data ধরে রাখতে পারে, এবং `T`-এর বদলে যে প্রতিটি concrete type ব্যবহৃত হয় তা পুরো `Option<T>` type-টিকে একটি ভিন্ন type বানিয়ে দেয়। নিচে `Option` value ব্যবহার করে number type এবং char type ধরে রাখার কিছু উদাহরণ দেওয়া হলো:

```rust
    let some_number = Some(5);
    let some_char = Some('e');

    let absent_number: Option<i32> = None;
```

`some_number`-এর type হলো `Option<i32>`। `some_char`-এর type হলো `Option<char>`, যা ভিন্ন একটি type। Rust এই type গুলো infer করতে পারে কারণ আমরা `Some` variant-এর ভেতরে একটি value উল্লেখ করেছি। `absent_number`-এর জন্য Rust আমাদের সামগ্রিক `Option` type-টি annotate করতে বলে: শুধু একটি `None` value দেখে compiler বুঝতে পারে না যে এর সংশ্লিষ্ট `Some` variant কোন type-এর value ধরে রাখবে। এখানে আমরা Rust-কে বলছি যে `absent_number`-এর type আমরা চাই `Option<i32>` হোক।

যখন আমাদের কাছে একটি `Some` value থাকে, তখন আমরা জানি একটি value উপস্থিত আছে, এবং সেই value-টি `Some`-এর ভেতরে আছে। যখন আমাদের কাছে একটি `None` value থাকে, তখন কোনো অর্থে এটি null-এর সমার্থক: আমাদের কাছে কোনো valid value নেই। তাহলে, `Option<T>` থাকা null থাকার চেয়ে ভালো কীসে?

সংক্ষেপে, যেহেতু `Option<T>` এবং `T` (যেখানে `T` যেকোনো type হতে পারে) ভিন্ন type, তাই compiler আমাদেরকে একটি `Option<T>` value-কে সরাসরি একটি valid value-র মতো ব্যবহার করতে দেবে না। উদাহরণস্বরূপ, এই code-টি compile হবে না, কারণ এটি একটি `i8`-এর সাথে একটি `Option<i8>` যোগ করতে চাইছে:

```rust,ignore,does_not_compile
    let x: i8 = 5;
    let y: Option<i8> = Some(5);

    let sum = x + y;
```

আমরা যদি এই code-টি run করি, তবে নিচের মতো একটি error message পাবো:

```console
$ cargo run
   Compiling enums v0.1.0 (file:///projects/enums)
error[E0277]: cannot add `Option<i8>` to `i8`
 --> src/main.rs:5:17
  |
5 |     let sum = x + y;
  |                 ^ no implementation for `i8 + Option<i8>`
  |
  = help: the trait `Add<Option<i8>>` is not implemented for `i8`
help: the following other types implement trait `Add<Rhs>`
 --> /rustc/88d9e12ae178fab0fb5cc050a94da85685d449ea/library/core/src/ops/arith.rs:98:8
  |
  = note: `i8` implements `Add`
 ::: /rustc/88d9e12ae178fab0fb5cc050a94da85685d449ea/library/core/src/ops/arith.rs:113:0
  |
  = note: in this macro invocation
 --> /rustc/88d9e12ae178fab0fb5cc050a94da85685d449ea/library/core/src/internal_macros.rs:22:8
  |
  = note: `&i8` implements `Add<i8>`
 ::: /rustc/88d9e12ae178fab0fb5cc050a94da85685d449ea/library/core/src/internal_macros.rs:33:8
  |
  = note: `i8` implements `Add<&i8>`
 ::: /rustc/88d9e12ae178fab0fb5cc050a94da85685d449ea/library/core/src/internal_macros.rs:44:8
  |
  = note: `&i8` implements `Add`
  = note: this error originates in the macro `add_impl` (in Nightly builds, run with -Z macro-backtrace for more info)

For more information about this error, try `rustc --explain E0277`.
error: could not compile `enums` (bin "enums") due to 1 previous error
```

ভয়ংকর! বাস্তবে, এই error message-টির অর্থ হলো Rust বোঝে না কীভাবে একটি `i8` এবং একটি `Option<i8>` যোগ করতে হয়, কারণ এগুলো ভিন্ন type। Rust-এ আমাদের যখন `i8`-এর মতো কোনো type-এর value থাকে, তখন compiler নিশ্চিত করে যে আমাদের কাছে সবসময় একটি valid value আছে। আমরা নিশ্চিন্তে এগোতে পারি, সেই value ব্যবহারের আগে null আছে কিনা তা যাচাই না করেও। শুধুমাত্র যখন আমাদের কাছে একটি `Option<i8>` (বা আমরা যে ধরনের value নিয়ে কাজ করছি তার সমতুল্য) থাকে, তখনই আমাদের value না-ও থাকতে পারে সেই উদ্বেগ নিতে হয়, এবং compiler নিশ্চিত করে যে value-টি ব্যবহারের আগে আমরা সেই case handle করেছি।

অন্য কথায়, তোমাকে একটি `Option<T>`-কে `T`-এ রূপান্তর করতে হবে তার পরেই তুমি সেটির উপর `T` operation চালাতে পারবে। সাধারণত, এটি null-এর অন্যতম সাধারণ সমস্যা ধরতে সাহায্য করে: ধরে নেওয়া যে কোনো কিছু null নয়, অথচ বাস্তবে তা null।

ভুল করে not-null value ধরে নেওয়ার ঝুঁকি দূর করা তোমাকে code সম্পর্কে আরও আত্মবিশ্বাসী হতে সাহায্য করে। যদি তোমার এমন কোনো value দরকার হয় যা সম্ভবত null হতে পারে, তবে তোমাকে স্পষ্টভাবে ঐ value-র type `Option<T>` করে opt in করতে হবে। তারপর যখন তুমি সেই value ব্যবহার করবে, তখন তোমাকে স্পষ্টভাবে value-টি null হলে সেই case handle করতে হবে। যেখানেই কোনো value-র type `Option<T>` নয়, সেখানে তুমি _নিশ্চিন্তে_ ধরে নিতে পারো যে value-টি null নয়। Rust-এ null-এর ব্যাপকতা সীমিত করে Rust code-এর safety বাড়ানোর জন্য এটি একটি ইচ্ছাকৃত design decision ছিল।

তাহলে তুমি যখন `Option<T>` type-এর কোনো value পাবে, তখন `Some` variant থেকে `T` value-টি কীভাবে বের করবে যাতে সেটি ব্যবহার করতে পারো? `Option<T>` enum-এ প্রচুর method আছে যা বিভিন্ন পরিস্থিতিতে কাজে লাগে; তুমি সেগুলো [এর documentation-এ][docs]<!-- ignore --> দেখতে পারো। `Option<T>`-এর method গুলোর সাথে পরিচিত হওয়া তোমার Rust শেখার পথে খুবই কাজে লাগবে।

সাধারণত, একটি `Option<T>` value ব্যবহার করতে হলে তোমার এমন code লাগবে যা প্রতিটি variant handle করবে। তোমার এমন কিছু code লাগবে যা শুধু তখনই run হবে যখন তোমার কাছে একটি `Some(T)` value থাকবে, এবং এই code-টি ভেতরের `T` ব্যবহার করতে পারবে। তোমার আরও কিছু code লাগবে যা শুধু তখনই run হবে যখন তোমার কাছে একটি `None` value থাকবে, এবং সেই code-এর কাছে কোনো `T` value থাকবে না। `match` expression হলো এমন একটি control flow construct যা enum-এর সাথে ব্যবহার করলে ঠিক এই কাজটিই করে: এটি enum-এর যেকোনো variant-এর ক্ষেত্রে ভিন্ন ভিন্ন code run করবে, এবং সেই code প্রদত্ত value-র ভেতরের data ব্যবহার করতে পারবে।

[IpAddr]: ../std/net/enum.IpAddr.html
[option]: ../std/option/enum.Option.html
[docs]: ../std/option/enum.Option.html

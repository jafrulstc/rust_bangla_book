## একটি File পড়া

এখন আমরা `file_path` argument-এ উল্লেখ করা file-টি পড়ার functionality যোগ করব। প্রথমে, সেটি পরীক্ষা করার জন্য আমাদের একটি sample file দরকার: আমরা এমন একটি file ব্যবহার করব যাতে কয়েকটি line-এ সামান্য পরিমাণ text আছে এবং কিছু word বারবার এসেছে। Listing 12-3-তে Emily Dickinson-এর একটি poem দেওয়া আছে যেটি দারুণ কাজ করবে! তোমার project-এর root level-এ _poem.txt_ নামে একটি file তৈরি করো এবং সেখানে “I’m Nobody! Who are you?” poem-টি লেখো।

<Listing number="12-3" file-name="poem.txt" caption="Emily Dickinson-এর একটি poem একটি ভালো test case।">

```text
I'm nobody! Who are you?
Are you nobody, too?
Then there's a pair of us - don't tell!
They'd banish us, you know.

How dreary to be somebody!
How public, like a frog
To tell your name the livelong day
To an admiring bog!
```

</Listing>

Text ঠিক জায়গায় বসানোর পর, _src/main.rs_ edit করো এবং Listing 12-4-এ দেখানোর মতো করে file পড়ার code যোগ করো।

<Listing number="12-4" file-name="src/main.rs" caption="দ্বিতীয় argument দ্বারা নির্দিষ্ট file-টির content পড়া">

```rust,should_panic,noplayground
use std::env;
use std::fs;

fn main() {
    // --snip--
    println!("In file {file_path}");

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    println!("With text:\n{contents}");
}
```

</Listing>

প্রথমে আমরা একটি `use` statement দিয়ে standard library-এর প্রাসঙ্গিক অংশটি আনি: file handle করার জন্য আমাদের `std::fs` দরকার।

`main`-এ নতুন statement `fs::read_to_string` টি `file_path` নেয়, সেই file-টি খোলে, এবং `std::io::Result<String>` type-এর একটি value return করে যেটি file-টির content ধারণ করে।

এর পরে, আমরা আবার একটি সাময়িক `println!` statement যোগ করি যেটি file পড়ার পর `contents`-এর value print করে, যাতে আমরা যাচাই করতে পারি যে program-টি এ পর্যন্ত ঠিকঠাক কাজ করছে।

চলো প্রথম command line argument হিসেবে যেকোনো একটি string দিয়ে (কারণ আমরা এখনও searching-এর অংশটি implement করিনি) এবং দ্বিতীয় argument হিসেবে _poem.txt_ file দিয়ে এই code-টি চালাই:

```console
$ cargo run -- the poem.txt
   Compiling minigrep v0.1.0 (file:///projects/minigrep)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.0s
     Running `target/debug/minigrep the poem.txt`
Searching for the
In file poem.txt
With text:
I'm nobody! Who are you?
Are you nobody, too?
Then there's a pair of us - don't tell!
They'd banish us, you know.

How dreary to be somebody!
How public, like a frog
To tell your name the livelong day
To an admiring bog!
```

দারুণ! Code-টি file-এর content পড়ল এবং তারপর সেটি print করল। কিন্তু code-টির কিছু ত্রুটি আছে। এই মুহূর্তে, `main` function-টির একাধিক responsibility আছে: সাধারণত, যদি প্রতিটি function শুধু একটি বিষয়ের জন্য দায়ী থাকে তবে function-গুলো বেশি পরিষ্কার ও maintain করা সহজ হয়। অন্য সমস্যাটি হলো আমরা error গুলো যেভাবে পারতাম সেভাবে handle করছি না। Program-টি এখনো ছোট, তাই এই ত্রুটিগুলো বড় সমস্যা নয়, কিন্তু program যত বড় হবে, সেগুলো পরিষ্কারভাবে ঠিক করা তত কঠিন হবে। Program develop করার সময় শুরুতেই refactoring শুরু করা ভালো অভ্যাস, কারণ অল্প পরিমাণ code refactor করা অনেক সহজ। আমরা এখন সেটাই করব।

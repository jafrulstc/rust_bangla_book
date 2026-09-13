<!-- Old headings. Do not remove or links may break. -->

<a id="writing-error-messages-to-standard-error-instead-of-standard-output"></a>

## Standard Error-এ Error Redirect করা

এই মুহূর্তে, আমরা আমাদের সমস্ত output `println!` macro ব্যবহার করে terminal-এ লিখছি। বেশিরভাগ terminal-এ দুই ধরনের output থাকে: সাধারণ তথ্যের জন্য _standard output_ (`stdout`) এবং error message-এর জন্য _standard error_ (`stderr`)। এই পার্থক্য user-দের একটি program-এর সফল output একটি file-এ পাঠাতে দেয় কিন্তু সেই সাথে error message গুলো screen-এই print করতে দেয়।

`println!` macro শুধু standard output-এ print করতে সক্ষম, তাই standard error-এ print করতে আমাদের অন্য কিছু ব্যবহার করতে হবে।

### Error গুলো কোথায় লেখা হচ্ছে তা Check করা

প্রথমে, চলো দেখি বর্তমানে `minigrep`-এর দ্বারা print করা content গুলো কীভাবে standard output-এ লেখা হচ্ছে, সেই সাথে আমরা যে error message গুলো এর বদলে standard error-এ লিখতে চাই সেগুলোও। আমরা সেটি করব standard output stream-কে একটি file-এ redirect করে, সেই সাথে ইচ্ছাকৃতভাবে একটি error ঘটিয়ে। আমরা standard error stream-টিকে redirect করব না, তাই standard error-এ পাঠানো যেকোনো content screen-এ দেখা যাবে।

Command line program-গুলোর কাছ থেকে আশা করা হয় যে তারা error message গুলো standard error stream-এ পাঠাবে, যাতে আমরা standard output stream-কে একটি file-এ redirect করলেও error message গুলো screen-এ দেখতে পাই। আমাদের program-টি বর্তমানে ভালোভাবে আচরণ করছে না: আমরা এখনই দেখতে পাব যে এটি error message output-টিকে একটি file-এ সংরক্ষণ করছে!

এই আচরণটি প্রদর্শন করতে, আমরা program-টিকে `>` এবং সেই file path, _output.txt_, দিয়ে চালাব, যেখানে আমরা standard output stream-টিকে redirect করতে চাই। আমরা কোনো argument pass করব না, যা একটি error ঘটাবে:

```console
$ cargo run > output.txt
```

`>` syntax-টি shell-কে বলে standard output-এর content গুলো screen-এর বদলে _output.txt_-এ লিখতে। আমরা আমরা যে error message-টি আশা করছিলাম তা screen-এ print হতে দেখিনি, তাই মানে সেটি file-এ চলে গেছে। _output.txt_-তে যা আছে তা এইরকম:

```text
Problem parsing arguments: not enough arguments
```

হ্যাঁ, আমাদের error message-টি standard output-এ print হচ্ছে। এই ধরনের error message-গুলো standard error-এ print হলে অনেক বেশি কাজে লাগে, যাতে একটি সফল run থেকে পাওয়া data-ই শুধু file-এ যায়। আমরা সেটি পরিবর্তন করব।

### Error গুলো Standard Error-এ Print করা

আমরা Listing 12-24-এর code ব্যবহার করে error message print করার পদ্ধতি পরিবর্তন করব। এই chapter-এ আগে আমরা যে refactoring করেছি তার জন্য, error message print করা সমস্ত code একটি function-এ আছে, `main`। Standard library `eprintln!` macro provide করে যা standard error stream-এ print করে, তাই চলো error print করতে আমরা যে দুটি জায়গায় `println!` call করছিলাম সেগুলো পরিবর্তন করে `eprintln!` ব্যবহার করি।

<Listing number="12-24" file-name="src/main.rs" caption="`eprintln!` ব্যবহার করে standard output-এর বদলে standard error-এ error message লেখা">

```rust,ignore
fn main() {
    let args: Vec<String> = env::args().collect();

    let config = Config::build(&args).unwrap_or_else(|err| {
        eprintln!("Problem parsing arguments: {err}");
        process::exit(1);
    });

    if let Err(e) = run(config) {
        eprintln!("Application error: {e}");
        process::exit(1);
    }
}
```

</Listing>

চলো এখন program-টি আবার একইভাবে চালাই, কোনো argument ছাড়া এবং standard output-কে `>` দিয়ে redirect করে:

```console
$ cargo run > output.txt
Problem parsing arguments: not enough arguments
```

এখন আমরা error-টি screen-এ দেখতে পাচ্ছি এবং _output.txt_-তে কিছু নেই, যা command line program-গুলোর কাছ থেকে আমরা প্রত্যাশা করি।

চলো program-টি আবার এমন argument দিয়ে চালাই যা error ঘটাবে না কিন্তু standard output-কে একটি file-এ redirect করবে, এভাবে:

```console
$ cargo run -- to poem.txt > output.txt
```

আমরা terminal-এ কোনো output দেখব না, এবং _output.txt_-তে আমাদের result গুলো থাকবে:

<span class="filename">Filename: output.txt</span>

```text
Are you nobody, too?
How dreary to be somebody!
```

এটি প্রদর্শন করে যে আমরা এখন সফল output-এর জন্য standard output এবং error output-এর জন্য standard error ব্যবহার করছি যেমন উচিত।

## Summary

এই chapter-টিতে তুমি এ পর্যন্ত শেখা কিছু প্রধান concept-এর পুনরাবৃত্তি করা হলো এবং দেখানো হলো কীভাবে Rust-এ সাধারণ I/O operation সম্পাদন করতে হয়। Command line argument, file, environment variable, এবং error print করার জন্য `eprintln!` macro ব্যবহার করে তুমি এখন command line application লেখার জন্য প্রস্তুত। আগের chapter-গুলোর concept-গুলোর সাথে মিলিয়ে, তোমার code সুসংগঠিত হবে, সঠিক data structure-এ data effectively সংরক্ষণ করবে, error সুন্দরভাবে handle করবে, এবং ভালোভাবে test করা হবে।

এরপরে, আমরা functional language দ্বারা প্রভাবিত কিছু Rust feature নিয়ে আলোচনা করব: closure এবং iterator।

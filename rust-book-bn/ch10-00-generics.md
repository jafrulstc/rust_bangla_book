# Generic Types, Traits, এবং Lifetimes

প্রতিটি programming language-এই concept-এর duplication কার্যকরভাবে দূর করার জন্য কিছু tool থাকে। Rust-এ এমন একটি tool হলো _generics_: concrete type বা অন্য কোনো property-র বিমূর্ত (abstract) stand-in। Compile ও run করার সময় সেখানে কী থাকবে তা না জেনেই আমরা generics-এর behavior বা অন্যান্য generics-এর সাথে তাদের সম্পর্ক প্রকাশ করতে পারি।

Function, ঠিক যেমন অজানা value-সহ parameter নিয়ে একই code একাধিক concrete value-এর উপর চালায়, তেমনি `i32` বা `String` এর মতো কোনো concrete type-এর বদলে কোনো generic type-এর parameter নিতে পারে। আসলে আমরা ইতিমধ্যে Chapter 6-এ `Option<T>`, Chapter 8-এ `Vec<T>` ও `HashMap<K, V>`, এবং Chapter 9-এ `Result<T, E>` দিয়ে generics ব্যবহার করেছি। এই chapter-এ তুমি নিজের type, function, এবং method-গুলোতে কীভাবে generics define করতে হয় তা শিখবে!

প্রথমে আমরা দেখবো কীভাবে একটি function extract করে code duplication কমানো যায়। এরপর একই প্রক্রিয়া ব্যবহার করে শুধু parameter-এর type-এ পার্থক্য আছে এমন দুটো function থেকে একটি generic function বানাবো। আমরা আরও ব্যাখ্যা করবো কীভাবে struct ও enum definition-এ generic type ব্যবহার করতে হয়।

তারপর তুমি শিখবে কীভাবে traits ব্যবহার করে generic ভাবে behavior define করতে হয়। তুমি traits-কে generic type-এর সাথে যুক্ত করে একটি generic type-কে শুধুমাত্র সেইসব type-এ সীমাবদ্ধ করতে পারবে যাদের একটি নির্দিষ্ট behavior আছে—যেকোনো type নয়।

শেষে, আমরা _lifetimes_ নিয়ে আলোচনা করবো: এটি এক ধরনের generic, যা compiler-কে reference-গুলো কীভাবে একে অপরের সাথে সম্পর্কিত সে সম্পর্কে তথ্য দেয়। Lifetimes-এর মাধ্যমে আমরা compiler-কে borrowed value সম্পর্কে যথেষ্ট তথ্য দিতে পারি, যাতে আমাদের সাহায্য ছাড়া সে যে পরিস্থিতিতে পারত, তার চেয়ে বেশি পরিস্থিতিতে reference-গুলো valid থাকবে কিনা তা নিশ্চিত করতে পারে।

## Function Extract করে Duplication দূর করা

Generics আমাদেরকে নির্দিষ্ট type-গুলোকে একটি placeholder দিয়ে প্রতিস্থাপন করতে দেয়, যা একাধিক type-কে প্রতিনিধিত্ব করে এবং এভাবে code duplication দূর করে। Generics syntax-এ ডুব দেওয়ার আগে, চলো প্রথমে দেখি কীভাবে generic type ব্যবহার না করেই একটি function extract করে নির্দিষ্ট value-গুলোকে একাধিক value-র প্রতিনিধি placeholder দিয়ে প্রতিস্থাপন করে duplication দূর করা যায়। তারপর আমরা একই প্রযুক্তি প্রয়োগ করে একটি generic function extract করবো! Function-এ extract করা যায় এমন duplicated code কীভাবে চিনতে হয় তা দেখলে, তুমি ধীরে ধীরে এমন duplicated code-ও চিনতে পারবে যেগুলোতে generics ব্যবহার করা যায়।

আমরা Listing 10-1-এর ছোট প্রোগ্রাম দিয়ে শুরু করবো, যা একটি list-এর মধ্যে সবচেয়ে বড় সংখ্যাটি খুঁজে বের করে।

<Listing number="10-1" file-name="src/main.rs" caption="Finding the largest number in a list of numbers">

```rust
fn main() {
    let number_list = vec![34, 50, 25, 100, 65];

    let mut largest = &number_list[0];

    for number in &number_list {
        if number > largest {
            largest = number;
        }
    }

    println!("The largest number is {largest}");
}
```

</Listing>

আমরা পূর্ণসংখ্যার একটি list `number_list` variable-এ রাখি এবং list-এর প্রথম সংখ্যার একটি reference `largest` নামের একটি variable-এ রাখি। এরপর আমরা list-এর সব সংখ্যার উপর পুনরাবৃত্তি করি, এবং বর্তমান সংখ্যাটি `largest`-এ সংরক্ষিত সংখ্যার চেয়ে বড় হলে আমরা সেই variable-এর reference প্রতিস্থাপন করি। কিন্তু বর্তমান সংখ্যাটি এ পর্যন্ত দেখা সবচেয়ে বড় সংখ্যার সমান বা তার চেয়ে ছোট হলে variable অপরিবর্তিত থাকে এবং code list-এর পরবর্তী সংখ্যায় চলে যায়। list-এর সব সংখ্যা বিবেচনা করার পর `largest` সবচেয়ে বড় সংখ্যাটিকে refer করবে, যা এই ক্ষেত্রে 100।

এখন আমাদেরকে দুটি ভিন্ন সংখ্যার list থেকে সবচেয়ে বড় সংখ্যাটি খুঁজে বের করার কাজ দেওয়া হয়েছে। এর জন্য, আমরা Listing 10-1-এর code টি duplicate করে প্রোগ্রামের দুটি ভিন্ন স্থানে একই logic ব্যবহার করতে পারি, যেমনটা Listing 10-2-তে দেখানো হয়েছে।

<Listing number="10-2" file-name="src/main.rs" caption="Code to find the largest number in *two* lists of numbers">

```rust
fn main() {
    let number_list = vec![34, 50, 25, 100, 65];

    let mut largest = &number_list[0];

    for number in &number_list {
        if number > largest {
            largest = number;
        }
    }

    println!("The largest number is {largest}");

    let number_list = vec![102, 34, 6000, 89, 54, 2, 43, 8];

    let mut largest = &number_list[0];

    for number in &number_list {
        if number > largest {
            largest = number;
        }
    }

    println!("The largest number is {largest}");
}
```

</Listing>

যদিও এই code কাজ করে, code duplicate করা ক্লান্তিকর এবং ত্রুটি-প্রবণ। এছাড়া আমরা যখন code পরিবর্তন করতে চাই, তখন একাধিক স্থানে সেটি update করতে মনে রাখতে হয়।

এই duplication দূর করতে, আমরা একটি abstraction তৈরি করবো—এমন একটি function define করে যা parameter হিসেবে পাস করা যেকোনো পূর্ণসংখ্যার list-এর উপর কাজ করে। এই সমাধান আমাদের code-কে আরও পরিষ্কার করে এবং একটি list-এ সবচেয়ে বড় সংখ্যা খোঁজার concept-টি বিমূর্তভাবে প্রকাশ করতে দেয়।

Listing 10-3-এ, আমরা সবচেয়ে বড় সংখ্যা খুঁজে বের করার code-টি `largest` নামের একটি function-এ extract করি। তারপর আমরা Listing 10-2-এর দুটি list থেকে সবচেয়ে বড় সংখ্যা খুঁজতে সেই function-টি call করি। ভবিষ্যতে আমাদের যেকোনো `i32` value-র list-এর জন্যও আমরা এই function ব্যবহার করতে পারি।

<Listing number="10-3" file-name="src/main.rs" caption="Abstracted code to find the largest number in two lists">

```rust
fn largest(list: &[i32]) -> &i32 {
    let mut largest = &list[0];

    for item in list {
        if item > largest {
            largest = item;
        }
    }

    largest
}

fn main() {
    let number_list = vec![34, 50, 25, 100, 65];

    let result = largest(&number_list);
    println!("The largest number is {result}");

    let number_list = vec![102, 34, 6000, 89, 54, 2, 43, 8];

    let result = largest(&number_list);
    println!("The largest number is {result}");
}
```

</Listing>

`largest` function-এ `list` নামের একটি parameter আছে, যা আমরা function-এ যেকোনো `i32` value-র concrete slice পাস করতে পারি তাকে প্রতিনিধিত্ব করে। ফলস্বরূপ, যখন আমরা function-টি call করি, code টি আমরা যে নির্দিষ্ট value-গুলো পাস করি তার উপর চলে।

সংক্ষেপে, Listing 10-2 থেকে Listing 10-3-এ আমরা যে ধাপগুলো নিয়েছি:

1. Duplicate code চিনে বের করা।
1. Duplicate code-টি function-এর body-তে extract করা এবং function signature-তে সেই code-এর input ও return value specify করা।
1. Duplicate code-এর দুটি instance-কে সেই function-কে call করায় রূপান্তর করা।

এরপর, আমরা code duplication কমাতে এই একই ধাপগুলো generics-এর সাথে ব্যবহার করবো। ঠিক যেমন function body নির্দিষ্ট value-এর বদলে বিমূর্ত `list`-এর উপর কাজ করতে পারে, generics code-কে বিমূর্ত type-এর উপর কাজ করতে দেয়।

উদাহরণস্বরূপ, ধরো আমাদের দুটি function আছে: একটি `i32` value-র slice-এ সবচেয়ে বড় item খুঁজে বের করে এবং অন্যটি `char` value-র slice-এ সবচেয়ে বড় item খুঁজে বের করে। আমরা কীভাবে সেই duplication দূর করবো? চলো জেনে নিই!

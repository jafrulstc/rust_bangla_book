## Processing a Series of Items with Iterators

Iterator pattern তোমাকে একটি ধারাবাহিক item-এর series-এর প্রতিটির উপর পালাক্রমিক কোনো task সম্পাদন করতে দেয়। একটি iterator প্রতিটি item-এর উপর iterate করার এবং কবে sequence শেষ হয়েছে তা নির্ধারণ করার logic-এর দায়িত্ব নেয়। তুমি যখন iterator ব্যবহার করো, তখন সেই logic নিজে আবার implement করতে হয় না।

Rust-এ iterator গুলো _lazy_, যার মানে তুমি iterator-কে consume করে শেষ করে দেওয়া method না call করা পর্যন্ত এদের কোনো প্রভাব নেই। যেমন, Listing 13-10-এর code `Vec<T>`-তে define করা `iter` method call করে `v1` vector-এর item গুলোর উপর একটি iterator তৈরি করে। শুধু এই code নিজে কোনো কার্যকর কাজ করে না।

<Listing number="13-10" file-name="src/main.rs" caption="Creating an iterator">

```rust
    let v1 = vec![1, 2, 3];

    let v1_iter = v1.iter();
```

</Listing>

Iterator-টি `v1_iter` variable-এ store করা হয়। একবার আমরা iterator তৈরি করলে সেটি বিভিন্নভাবে ব্যবহার করতে পারি। Listing 3-5-এ আমরা একটি array-এর উপর `for` loop ব্যবহার করে প্রতিটি item-এর উপর কিছু code execute করে iterate করেছিলাম। Behind the scenes, এটি implicitly একটি iterator তৈরি করে তারপর consume করেছিল, কিন্তু আমরা এখন পর্যন্ত সেটি ঠিক কীভাবে কাজ করে তা এড়িয়ে গিয়েছিলাম।

Listing 13-11-এর example-এ আমরা iterator তৈরি করা আর `for` loop-এ iterator ব্যবহার করাকে আলাদা করি। যখন `v1_iter`-এর iterator-টি ব্যবহার করে `for` loop call করা হয়, তখন iterator-এর প্রতিটি element loop-এর এক একটি iteration-এ ব্যবহৃত হয়, যা প্রতিটি value print করে।

<Listing number="13-11" file-name="src/main.rs" caption="Using an iterator in a `for` loop">

```rust
    let v1 = vec![1, 2, 3];

    let v1_iter = v1.iter();

    for val in v1_iter {
        println!("Got: {val}");
    }
```

</Listing>

যেসব language-এর standard library-তে iterator provide করা থাকে না, সেখানে তুমি সম্ভবত একই functionality এভাবে লিখতে: একটি variable কে index 0 থেকে শুরু করে, সেই variable দিয়ে vector-এ index করে একটি value নিয়ে, এবং loop-এ variable-এর value increment করে vector-এর মোট item-এর সংখ্যায় না পৌঁছানো পর্যন্ত এটি করতে।

Iterator সব logic তোমার জন্য handle করে, ফলে তুমি সম্ভাব্যভাবে ভুল করতে পারো এমন repetitive code কমায়। Iterator তোমাকে আরও বেশি flexibility দেয় একই logic বিভিন্ন ধরনের series-এ ব্যবহার করতে, শুধুমাত্র vector-এর মতো index-যোগ্য data structure-এ নয়। চলো দেখি iterator গুলো কীভাবে সেটা করে।

### The `Iterator` Trait এবং `next` Method

সব iterator standard library-তে define করা একটি trait যার নাম `Iterator` implement করে। Trait-টির definition দেখতে এরকম:

```rust
pub trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;

    // methods with default implementations elided
}
```

লক্ষ্য করো যে এই definition-এ কিছু নতুন syntax ব্যবহৃত হয়েছে: `type Item` এবং `Self::Item`, যা এই trait-এর সাথে একটি associated type define করছে। Associated type নিয়ে আমরা Chapter 20-তে বিস্তারিত আলোচনা করব। আপাতত তোমার শুধু এটুকু জানা দরকার যে এই code বলছে—`Iterator` trait implement করতে হলে তোমাকে একটি `Item` type-ও define করতে হবে, আর এই `Item` type টি `next` method-এর return type-এ ব্যবহৃত হয়। অর্থাৎ, `Item` type টি হবে iterator থেকে return হওয়া type।

`Iterator` trait implementor-দের কাছে শুধু একটি method define করতে বলে: `next` method, যা একসময়ে একটি করে item return করে যা `Some`-এ wrapped থাকে, এবং iteration শেষ হলে `None` return করে।

আমরা সরাসরি iterator-এর উপর `next` method call করতে পারি; Listing 13-12 দেখায় vector থেকে তৈরি একটি iterator-এ বারবার `next` call করলে কী value গুলো return হয়।

<Listing number="13-12" file-name="src/lib.rs" caption="Calling the `next` method on an iterator">

```rust,noplayground
    #[test]
    fn iterator_demonstration() {
        let v1 = vec![1, 2, 3];

        let mut v1_iter = v1.iter();

        assert_eq!(v1_iter.next(), Some(&1));
        assert_eq!(v1_iter.next(), Some(&2));
        assert_eq!(v1_iter.next(), Some(&3));
        assert_eq!(v1_iter.next(), None);
    }
```

</Listing>

লক্ষ্য করো যে আমাদের `v1_iter` কে mutable করতে হয়েছিল: একটি iterator-এর উপর `next` method call করা মানে iterator-এর সেই internal state change করা যা সে sequence-এ কোথায় আছে তা track করতে ব্যবহার করে। অন্য কথায়, এই code টি iterator-টিকে _consume_ বা ব্যবহার করে শেষ করে দেয়। `next`-এর প্রতিটি call iterator থেকে একটি করে item খেয়ে ফেলে। আমরা `for` loop ব্যবহার করার সময় `v1_iter` কে mutable করতে হয়নি, কারণ loop টি `v1_iter`-এর ownership নিয়ে নেয় এবং behind the scenes সেটিকে mutable করে।

এছাড়া লক্ষ্য করো যে `next` call থেকে আমরা যে value গুলো পাই সেগুলো vector-এর value-এর immutable reference। `iter` method immutable reference-এর উপর একটি iterator তৈরি করে। যদি আমরা এমন একটি iterator তৈরি করতে চাই যা `v1`-এর ownership নেয় এবং owned value return করে, তাহলে আমরা `iter`-এর বদলে `into_iter` call করতে পারি। একইভাবে, যদি mutable reference-এর উপর iterate করতে চাই, তাহলে `iter`-এর বদলে `iter_mut` call করতে পারি।

### Methods That Consume the Iterator

`Iterator` trait-এ বেশ কিছু ভিন্ন ভিন্ন method আছে যেগুলোর default implementation standard library দ্বারা provide করা; এই method গুলো সম্পর্কে জানতে `Iterator` trait-এর standard library API documentation দেখতে পারো। এই method গুলোর কিছু তাদের definition-এ `next` method call করে, যে কারণে `Iterator` trait implement করার সময় তোমাকে `next` method implement করতেই হয়।

যেসব method `next` কে call করে তাদের _consuming adapter_ বলা হয়, কারণ সেগুলোকে call করলে iterator শেষ হয়ে যায়। এর একটি example হলো `sum` method, যা iterator-এর ownership নেয় এবং বারবার `next` call করে item গুলোর উপর iterate করে, ফলে iterator-টিকে consume করে। এটি iterate করার সময় প্রতিটি item একটি running total-এ যোগ করে এবং iteration শেষ হলে সেই total return করে। Listing 13-13-এ একটি test আছে যা `sum` method-এর ব্যবহার দেখায়।

<Listing number="13-13" file-name="src/lib.rs" caption="Calling the `sum` method to get the total of all items in the iterator">

```rust,noplayground
    #[test]
    fn iterator_sum() {
        let v1 = vec![1, 2, 3];

        let v1_iter = v1.iter();

        let total: i32 = v1_iter.sum();

        assert_eq!(total, 6);
    }
```

</Listing>

`sum` call করার পর আমরা `v1_iter` ব্যবহার করতে পারি না, কারণ `sum` যেই iterator-এর উপর call করা হয় তার ownership নিয়ে নেয়।

### Methods That Produce Other Iterators

_Iterator adapter_ হলো `Iterator` trait-এ define করা এমন method যা iterator-কে consume করে না। বরং সেগুলো মূল iterator-এর কোনো এক aspect পরিবর্তন করে ভিন্ন iterator তৈরি করে।

Listing 13-14 দেখায় `map` iterator adapter method call করার একটি example, যা item গুলোর উপর iterate করার সময় প্রতিটি item-এ call করার জন্য একটি closure নেয়। `map` method একটি নতুন iterator return করে যা modified item গুলো produce করে। এখানে closure-টি এমন একটি নতুন iterator তৈরি করে যেখানে vector-এর প্রতিটি item ১ করে বাড়ানো হবে।

<Listing number="13-14" file-name="src/main.rs" caption="Calling the iterator adapter `map` to create a new iterator">

```rust,not_desired_behavior
    let v1: Vec<i32> = vec![1, 2, 3];

    v1.iter().map(|x| x + 1);
```

</Listing>

তবে এই code একটি warning produce করে:

```console
$ cargo run
   Compiling iterators v0.1.0 (file:///projects/iterators)
warning: unused `Map` that must be used
 --> src/main.rs:4:5
  |
4 |     v1.iter().map(|x| x + 1);
  |     ^^^^^^^^^^^^^^^^^^^^^^^^
  |
  = note: iterators are lazy and do nothing unless consumed
  = note: `#[warn(unused_must_use)]` (part of `#[warn(unused)]`) on by default
help: use `let _ = ...` to ignore the resulting value
  |
4 |     let _ = v1.iter().map(|x| x + 1);
  |     +++++++

warning: `iterators` (bin "iterators") generated 1 warning
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.47s
     Running `target/debug/iterators`
```

Listing 13-14-এর code কিছুই করে না; আমরা যে closure specify করেছি সেটি কখনো call হয় না। Warning-টি আমাদের মনে করিয়ে দেয় কেন: Iterator adapter গুলো lazy, আর আমাদের এখানে iterator-টিকে consume করতে হবে।

এই warning থেকে মুক্তি পেয়ে iterator-টিকে consume করতে আমরা `collect` method ব্যবহার করব, যা আমরা Listing 12-1-এ `env::args`-এর সাথে ব্যবহার করেছিলাম। এই method iterator-টিকে consume করে এবং ফলাফল value গুলোকে একটি collection data type-এ একত্রিত করে।

Listing 13-15-এ আমরা `map` call থেকে return হওয়া iterator-এর উপর iterate করার ফলাফল একটি vector-এ collect করি। এই vector-টিতে মূল vector-এর প্রতিটি item ১ করে বাড়ানো অবস্থায় থাকবে।

<Listing number="13-15" file-name="src/main.rs" caption="Calling the `map` method to create a new iterator, and then calling the `collect` method to consume the new iterator and create a vector">

```rust
    let v1: Vec<i32> = vec![1, 2, 3];

    let v2: Vec<_> = v1.iter().map(|x| x + 1).collect();

    assert_eq!(v2, vec![2, 3, 4]);
```

</Listing>

যেহেতু `map` একটি closure নেয়, তাই আমরা প্রতিটি item-এর উপর যেকোনো operation perform করতে চাই তা specify করতে পারি। এটি একটি চমৎকার example যে কীভাবে closure তোমাকে কোনো behavior customize করতে দেয় একই সাথে `Iterator` trait যে iteration behavior provide করে সেটি reuse করে।

তুমি একাধিক iterator adapter call chain করে readable ভাবে জটিল action perform করতে পারো। কিন্তু যেহেতু সব iterator lazy, তাই iterator adapter call থেকে ফলাফল পেতে তোমাকে অবশ্যই একটি consuming adapter method call করতে হবে।

<!-- Old headings. Do not remove or links may break. -->

<a id="using-closures-that-capture-their-environment"></a>

### Closures That Capture Their Environment

অনেক iterator adapter closure কে argument হিসেবে নেয়, এবং সাধারণত iterator adapter-গুলোর argument হিসেবে আমরা যে closure গুলো specify করব সেগুলো এমন closure হবে যা তাদের environment capture করে।

এই example-টির জন্য আমরা `filter` method ব্যবহার করব যা একটি closure নেয়। Closure-টি iterator থেকে একটি item পায় এবং একটি `bool` return করে। যদি closure `true` return করে, তাহলে সেই value টি `filter`-এর produce করা iterator-এ include থাকবে। আর যদি closure `false` return করে, তাহলে সেই value include হবে না।

Listing 13-16-তে আমরা `filter` কে এমন একটি closure-এর সাথে ব্যবহার করি যা তার environment থেকে `shoe_size` variable capture করে `Shoe` struct instance-গুলোর একটি collection-এর উপর iterate করে। এটি শুধু সেই shoe গুলোই return করবে যেগুলোর size specify করা সাইজের সমান।

<Listing number="13-16" file-name="src/lib.rs" caption="Using the `filter` method with a closure that captures `shoe_size`">

```rust,noplayground
#[derive(PartialEq, Debug)]
struct Shoe {
    size: u32,
    style: String,
}

fn shoes_in_size(shoes: Vec<Shoe>, shoe_size: u32) -> Vec<Shoe> {
    shoes.into_iter().filter(|s| s.size == shoe_size).collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn filters_by_size() {
        let shoes = vec![
            Shoe {
                size: 10,
                style: String::from("sneaker"),
            },
            Shoe {
                size: 13,
                style: String::from("sandal"),
            },
            Shoe {
                size: 10,
                style: String::from("boot"),
            },
        ];

        let in_my_size = shoes_in_size(shoes, 10);

        assert_eq!(
            in_my_size,
            vec![
                Shoe {
                    size: 10,
                    style: String::from("sneaker")
                },
                Shoe {
                    size: 10,
                    style: String::from("boot")
                },
            ]
        );
    }
}
```

</Listing>

`shoes_in_size` function shoe-গুলোর একটি vector এবং একটি shoe size parameter হিসেবে নেয়। এটি শুধুমাত্র specify করা size-এর shoe গুলো ধারণ করে এমন একটি vector return করে।

`shoes_in_size`-এর body-তে আমরা `into_iter` call করি যাতে vector-এর ownership নেওয়া একটি iterator তৈরি হয়। তারপর আমরা `filter` call করে সেই iterator-কে একটি নতুন iterator-এ adapt করি যা শুধু সেই element গুলোই ধারণ করে যাদের জন্য closure `true` return করে।

Closure-টি environment থেকে `shoe_size` parameter capture করে এবং সেই value টি প্রতিটি shoe-এর size-এর সাথে compare করে, শুধু specify করা size-এর shoe গুলোই রাখে। সবশেষে, `collect` call করলে adapted iterator থেকে return হওয়া value গুলো একটি vector-এ একত্রিত হয় যা function-টি return করে।

Test-টি দেখায় যে আমরা `shoes_in_size` call করলে আমরা শুধু সেই shoe গুলোই ফিরে পাই যাদের size আমরা যে value specify করেছি তার সমান।

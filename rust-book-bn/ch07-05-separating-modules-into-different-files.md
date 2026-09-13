## Module-কে আলাদা File-এ ভাগ করা

এই chapter-এর সব example এ পর্যন্ত একই file-এ একাধিক module define করা হয়েছে। Module যখন বড় হয়, তখন তুমি হয়তো তাদের definition আলাদা file-এ move করতে চাইবে যাতে code navigate করা সহজ হয়।

যেমন, চলো Listing 7-17-এর code থেকে শুরু করি যেখানে একাধিক restaurant module ছিল। আমরা module-গুলোকে crate root file-এ define করা রাখার বদলে আলাদা file-এ extract করব। এই ক্ষেত্রে crate root file হলো _src/lib.rs_, কিন্তু এই প্রক্রিয়া binary crate-এর ক্ষেত্রেও কাজ করে যাদের crate root file _src/main.rs_।

প্রথমে আমরা `front_of_house` module-টিকে তার নিজের file-এ extract করব। `front_of_house` module-এর curly bracket-এর ভেতরের code সরিয়ে দাও, শুধু `mod front_of_house;` declaration রেখে দাও, যাতে _src/lib.rs_-এ Listing 7-21-এর code থাকে। খেয়াল করো Listing 7-22-তে _src/front_of_house.rs_ file তৈরি না করা পর্যন্ত এটি compile হবে না।

<Listing number="7-21" file-name="src/lib.rs" caption="`front_of_house` module declare করা যার body *src/front_of_house.rs*-এ থাকবে">

```rust,ignore,does_not_compile
mod front_of_house;

pub use crate::front_of_house::hosting;

pub fn eat_at_restaurant() {
    hosting::add_to_waitlist();
}
```

</Listing>

এরপর, curly bracket-এ থাকা code-টি _src/front_of_house.rs_ নামের একটি নতুন file-এ রাখো, যেমন Listing 7-22-তে দেখানো হয়েছে। Compiler এই file-এ খুঁজতে জানে কারণ সে crate root-এ `front_of_house` নামের একটি module declaration পেয়েছে।

<Listing number="7-22" file-name="src/front_of_house.rs" caption="*src/front_of_house.rs*-এ `front_of_house` module-এর ভেতরের definition">

```rust,ignore
pub mod hosting {
    pub fn add_to_waitlist() {}
}
```

</Listing>

খেয়াল রাখো, তোমার module tree-তে কোনো file `mod` declaration দিয়ে load করতে হবে মাত্র _একবার_। একবার compiler জেনে গেলে যে এই file-টি project-এর অংশ (এবং যেহেতু `mod` statement তুমি কোথায় রেখেছ তার উপর ভিত্তি করে compiler জানে module tree-তে code-টি কোথায় আছে), তোমার project-এর অন্যান্য file-এর সেই loaded file-এর code-কে refer করতে হবে যেখানে সেটি declare করা হয়েছিল সেই path দিয়ে, যেমন [“Paths for Referring to an Item in the Module Tree”][paths]<!-- ignore --> section-এ আলোচনা করা হয়েছে। অন্য কথায়, `mod` কোনো “include” operation নয় যা তুমি হয়তো অন্য কোনো programming language-এ দেখেছ।

এরপর আমরা `hosting` module-টিকে তার নিজের file-ে extract করব। প্রক্রিয়াটি একটু ভিন্ন, কারণ `hosting` হলো root module-এর নয়, `front_of_house`-এর child module। আমরা `hosting`-এর file-টি একটি নতুন directory-তে রাখব যার নাম হবে module tree-তে তার ancestor-দের নাম অনুসারে, এই ক্ষেত্রে _src/front_of_house_।

`hosting` move করা শুরু করতে আমরা _src/front_of_house.rs_-কে পরিবর্তন করে শুধু `hosting` module-এর declaration রাখি:

<Listing file-name="src/front_of_house.rs">

```rust,ignore
pub mod hosting;
```

</Listing>

তারপর, আমরা একটি _src/front_of_house_ directory এবং একটি _hosting.rs_ file তৈরি করি `hosting` module-এ করা definition-গুলো রাখার জন্য:

<Listing file-name="src/front_of_house/hosting.rs">

```rust,ignore
pub fn add_to_waitlist() {}
```

</Listing>

যদি আমরা তার বদলে _hosting.rs_-কে _src_ directory-তে রাখতাম, তবে compiler _hosting.rs_-এর code-টিকে crate root-এ declare করা একটি `hosting` module হিসেবে আশা করত, `front_of_house` module-এর child হিসেবে declare করা হয়নি এমন একটি module হিসেবে নয়। কোন module-এর code কোন file-এ থাকবে তা নির্ধারণের compiler-এর নিয়মের কারণে directory ও file-গুলো module tree-এর সাথে কাছাকাছি মেলে।

> ### Alternate File Path
>
> এ পর্যন্ত আমরা Rust compiler-এর সবচেয়ে idiomatic file path cover করেছি, কিন্তু Rust একটি পুরোনো style-এর file path-ও support করে। Crate root-এ declare করা `front_of_house` নামের একটি module-এর জন্য compiler নিচের জায়গাগুলোতে module-এর code খুঁজবে:
>
> - _src/front_of_house.rs_ (যা আমরা cover করেছি)
> - _src/front_of_house/mod.rs_ (পুরোনো style, এখনও supported path)
>
> `front_of_house`-এর submodule `hosting`-এর জন্য compiler নিচের জায়গাগুলোতে module-এর code খুঁজবে:
>
> - _src/front_of_house/hosting.rs_ (যা আমরা cover করেছি)
> - _src/front_of_house/hosting/mod.rs_ (পুরোনো style, এখনও supported path)
>
> একই module-এর জন্য তুমি যদি দুটি style-ই ব্যবহার করো, তবে একটি compiler error পাবে। একই project-এ ভিন্ন ভিন্ন module-এর জন্য দুই style-এর mix ব্যবহার allowed, কিন্তু তোমার project navigate করা মানুষের জন্য এটি confusing হতে পারে।
>
> _mod.rs_ নামের file ব্যবহার করে এমন style-এর প্রধান অসুবিধা হলো তোমার project-এ অনেকগুলো _mod.rs_ file চলে আসতে পারে, যা তোমার editor-এ একসাথে open থাকলে বিভ্রান্তিকর হতে পারে।

আমরা প্রতিটি module-এর code আলাদা file-এ move করেছি, কিন্তু module tree একই রয়ে গেছে। `eat_at_restaurant`-এর function call-গুলো কোনো পরিবর্তন ছাড়াই কাজ করবে, যদিও definition গুলো এখন ভিন্ন ভিন্ন file-ে আছে। এই technique তোমাকে module বড় হলে সেগুলোকে নতুন file-এ move করার সুযোগ দেয়।

খেয়াল করো _src/lib.rs_-এর `pub use crate::front_of_house::hosting` statement-টিও পরিবর্তন হয়নি, এবং `use`-এর crate-এর অংশ হিসেবে কোন file compile হবে তার উপর কোনো প্রভাব নেই। `mod` keyword module declare করে, এবং Rust সেই module-এর code খোঁজে এমন একটি file-ে যার নাম module-টির নামের সাথে একই।

## Summary

Rust তোমাকে একটি package-কে একাধিক crate-এ এবং একটি crate-কে একাধিক module-ে ভাগ করতে দেয়, যাতে তুমি এক module-এ define করা item-কে অন্য module থেকে refer করতে পারো। এটি তুমি absolute বা relative path specify করে করতে পারো। এই path-গুলোকে `use` statement দিয়ে scope-ে আনা যায়, যাতে সেই scope-এ item-টি একাধিকবার ব্যবহারের সময় একটি ছোট path ব্যবহার করা যায়। Module-এর code ডিফল্টভাবে private, কিন্তু `pub` keyword যোগ করে definition-কে public করা যায়।

পরের chapter-এ আমরা standard library-র কিছু collection data structure দেখব যা তুমি তোমার সুসংগঠিত code-এ ব্যবহার করতে পারো।

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html

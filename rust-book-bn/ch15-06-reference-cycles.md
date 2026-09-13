## Reference Cycle Memory Leak করতে পারে

Rust-এর memory safety guarantee এটিকে কঠিন করে তোলে, কিন্তু অসম্ভব নয়, দুর্ঘটনাক্রমে এমন memory তৈরি করতে যা কখনো পরিষ্কার করা হয় না (যাকে _memory leak_ বলা হয়)। Memory leak সম্পূর্ণভাবে প্রতিরোধ করা Rust-এর কোনো guarantee নয়, যার অর্থ Rust-এ memory leak memory safe। আমরা দেখতে পাই যে Rust `Rc<T>` এবং `RefCell<T>` ব্যবহার করে memory leak allow করে: এমন reference তৈরি করা সম্ভব যেখানে item গুলো একে অপরকে একটি cycle-এ refer করে। এটি memory leak তৈরি করে কারণ cycle-এর প্রতিটি item-এর reference count কখনো 0-এ পৌঁছাবে না, এবং value গুলো কখনো drop হবে না।

### একটি Reference Cycle তৈরি করা

চলো দেখি একটি reference cycle কীভাবে ঘটতে পারে এবং কীভাবে তা প্রতিরোধ করা যায়, Listing 15-25-এ `List` enum-এর definition এবং একটি `tail` method দিয়ে শুরু করে।

<Listing number="15-25" file-name="src/main.rs" caption="A cons list definition that holds a `RefCell<T>` so that we can modify what a `Cons` variant is referring to">

```rust
use crate::List::{Cons, Nil};
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Debug)]
enum List {
    Cons(i32, RefCell<Rc<List>>),
    Nil,
}

impl List {
    fn tail(&self) -> Option<&RefCell<Rc<List>>> {
        match self {
            Cons(_, item) => Some(item),
            Nil => None,
        }
    }
}
```

</Listing>

আমরা Listing 15-5 থেকে `List` definition-এর আরেকটি variation ব্যবহার করছি। `Cons` variant-এর দ্বিতীয় element এখন `RefCell<Rc<List>>`, যার অর্থ হলো Listing 15-24-এ যেমন আমরা `i32` value modify করার ক্ষমতা পেয়েছিলাম, তার বদলে আমরা একটি `Cons` variant যে `List` value-টিকে point করছে সেটিকে modify করতে চাই। আমরা একটি `tail` method-ও যোগ করছি যাতে আমাদের কাছে একটি `Cons` variant থাকলে দ্বিতীয় item-এ access করা সুবিধা হয়।

Listing 15-26-তে, আমরা একটি `main` function যোগ করছি যা Listing 15-25-এর definition গুলো ব্যবহার করে। এই code `a`-তে একটি list এবং `b`-তে এমন একটি list তৈরি করে যা `a`-তে থাকা list-কে point করে। তারপর, এটি `a`-তে থাকা list-টিকে `b`-কে point করতে modify করে, একটি reference cycle তৈরি করে। এই প্রক্রিয়ার বিভিন্ন পর্যায়ে reference count গুলো কতটা তা দেখাতে পথে পথে `println!` statement আছে।

<Listing number="15-26" file-name="src/main.rs" caption="Creating a reference cycle of two `List` values pointing to each other">

```rust
fn main() {
    let a = Rc::new(Cons(5, RefCell::new(Rc::new(Nil))));

    println!("a initial rc count = {}", Rc::strong_count(&a));
    println!("a next item = {:?}", a.tail());

    let b = Rc::new(Cons(10, RefCell::new(Rc::clone(&a))));

    println!("a rc count after b creation = {}", Rc::strong_count(&a));
    println!("b initial rc count = {}", Rc::strong_count(&b));
    println!("b next item = {:?}", b.tail());

    if let Some(link) = a.tail() {
        *link.borrow_mut() = Rc::clone(&b);
    }

    println!("b rc count after changing a = {}", Rc::strong_count(&b));
    println!("a rc count after changing a = {}", Rc::strong_count(&a));

    // Uncomment the next line to see that we have a cycle;
    // it will overflow the stack.
    // println!("a next item = {:?}", a.tail());
}
```

</Listing>

আমরা `a` variable-এ `5, Nil` initial list সহ একটি `Rc<List>` instance তৈরি করি। তারপর আমরা `b` variable-এ একটি `Rc<List>` instance তৈরি করি যা আরেকটি `List` value ধারণ করে যাতে `10` value আছে এবং যা `a`-তে থাকা list-কে point করে।

আমরা `a`-কে modify করি যাতে সে `Nil`-এর বদলে `b`-কে point করে, একটি cycle তৈরি করে। আমরা সেটি `tail` method ব্যবহার করে `a`-তে থাকা `RefCell<Rc<List>>`-এর একটি reference পেয়ে করি, যা আমরা `link` variable-এ রাখি। তারপর, আমরা `RefCell<Rc<List>>`-এ `borrow_mut` method ব্যবহার করে ভেতরের value-টি একটি `Rc<List>` থেকে যা একটি `Nil` value ধারণ করে সেটিকে `b`-তে থাকা `Rc<List>`-এ পরিবর্তন করি।

এই code চালালে, শেষ `println!`-টি আপাতত comment করে রাখলে, আমরা এই output পাব:

```console
$ cargo run
   Compiling cons-list v0.1.0 (file:///projects/cons-list)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.53s
     Running `target/debug/cons-list
a initial rc count = 1
a next item = Some(RefCell { value: Nil })
a rc count after b creation = 2
b initial rc count = 1
b next item = Some(RefCell { value: Cons(5, RefCell { value: Nil }) })
b rc count after changing a = 2
a rc count after changing a = 2
```

`a` এবং `b`-তে `Rc<List>` instance-গুলোর reference count আমরা `a`-তে থাকা list-টিকে `b`-কে point করতে modify করার পর 2। `main`-এর শেষে, Rust `b` variable-টিকে drop করে, যা `b` `Rc<List>` instance-এর reference count 2 থেকে 1 কমায়। এই মুহূর্তে `Rc<List>`-এর heap-এ যে memory আছে তা drop হবে না কারণ এর reference count 1, 0 নয়। তারপর, Rust `a`-কে drop করে, যা `a` `Rc<List>` instance-এর reference count-ও 2 থেকে 1 কমায়। এই instance-এর memory-ও drop হতে পারে না, কারণ অন্য `Rc<List>` instance এখনো এটিকে refer করে। list-এ allocate করা memory চিরকাল uncollected থাকবে। এই reference cycle ভিজুয়ালাইজ করতে, আমরা Figure 15-4-তে diagram তৈরি করেছি।

<img alt="A rectangle labeled 'a' that points to a rectangle containing the integer 5. A rectangle labeled 'b' that points to a rectangle containing the integer 10. The rectangle containing 5 points to the rectangle containing 10, and the rectangle containing 10 points back to the rectangle containing 5, creating a cycle." src="img/trpl15-04.svg" class="center" />

<span class="caption">Figure 15-4: `a` এবং `b` list গুলো একে অপরকে point করে একটি reference cycle</span>

তুমি যদি শেষ `println!`-টি uncomment করে program চালাও, Rust এই cycle-টি `a` থেকে `b` থেকে `a` ইত্যাদি ভাবে print করার চেষ্টা করবে যতক্ষণ না stack overflow হয়।

বাস্তব world-এর program-এর তুলনায়, এই উদাহরণে একটি reference cycle তৈরি করার ফলাফল খুব ভয়াবহ নয়: আমরা reference cycle তৈরি করার ঠিক পরেই program শেষ হয়ে যায়। তবে, যদি একটি অধিক জটিল program একটি cycle-এ প্রচুর memory allocate করে এবং দীর্ঘক্ষণ ধরে রাখে, তাহলে program প্রয়োজনের চেয়ে বেশি memory ব্যবহার করবে এবং হয়তো system-কে overwhelm করবে, যার ফলে system-এ available memory শেষ হয়ে যাবে।

Reference cycle তৈরি করা খুব সহজে করা যায় না, কিন্তু অসম্ভবও নয়। তোমার কাছে যদি এমন `RefCell<T>` value থাকে যা `Rc<T>` value ধারণ করে অথবা interior mutability এবং reference counting সহ অন্যান্য nested combination of type থাকে, তোমাকে অবশ্যই নিশ্চিত করতে হবে যে তুমি cycle তৈরি করছ না; তুমি cycle গুলো ধরতে Rust-এর উপর নির্ভর করতে পারো না। একটি reference cycle তৈরি করা তোমার program-এর একটি logic bug হবে যা তোমার minimize করা উচিত automated test, code review এবং অন্যান্য software development practice ব্যবহার করে।

Reference cycle এড়ানোর আরেকটি সমাধান হলো তোমার data structure পুনর্গঠন করা যাতে কিছু reference ownership প্রকাশ করে এবং কিছু reference না করে। ফলে, তোমার কাছে কিছু ownership relationship এবং কিছু non-ownership relationship দিয়ে গঠিত cycle থাকতে পারে, এবং শুধুমাত্র ownership relationship গুলো প্রভাব ফেলবে একটি value drop করা যাবে কি না তাতে। Listing 15-25-এ, আমরা সবসময় চাই `Cons` variant গুলো যেন তাদের list-কে own করে, তাই data structure পুনর্গঠন করা সম্ভব নয়। চলো parent node এবং child node দিয়ে গঠিত graph ব্যবহার করে একটি উদাহরণ দেখি যেখানে non-ownership relationship গুলো reference cycle প্রতিরোধের একটি উপযুক্ত উপায়।

<!-- Old headings. Do not remove or links may break. -->

<a id="preventing-reference-cycles-turning-an-rct-into-a-weakt"></a>

### `Weak<T>` ব্যবহার করে Reference Cycle প্রতিরোধ করা

এ পর্যন্ত, আমরা দেখিয়েছি যে `Rc::clone` call করলে একটি `Rc<T>` instance-এর `strong_count` বাড়ে, এবং একটি `Rc<T>` instance শুধুমাত্র তখনই পরিষ্কার করা হয় যদি এর `strong_count` 0 হয়। তুমি `Rc::downgrade` call করে এবং `Rc<T>`-এর একটি reference pass করে একটি `Rc<T>` instance-এর ভেতরের value-এর একটি weak reference তৈরি করতে পারো। *Strong reference* গুলো হলো তুমি কীভাবে একটি `Rc<T>` instance-এর ownership share করতে পারো। *Weak reference* গুলো ownership relationship প্রকাশ করে না, এবং তাদের count একটি `Rc<T>` instance কখন পরিষ্কার করা হবে তা প্রভাবিত করে না। এগুলো reference cycle সৃষ্টি করবে না, কারণ কিছু weak reference জড়িত যেকোনো cycle একবার জড়িত value গুলোর strong reference count 0 হলে ভেঙে যাবে।

তুমি `Rc::downgrade` call করলে, তুমি `Weak<T>` type-এর একটি smart pointer পাবে। `Rc<T>` instance-এ `strong_count` 1 করে বাড়ানোর বদলে, `Rc::downgrade` call করলে `weak_count` 1 করে বাড়ে। `Rc<T>` type `weak_count` ব্যবহার করে কতগুলো `Weak<T>` reference বিদ্যমান তা track করে, `strong_count`-এর মতো। পার্থক্য হলো `weak_count`-এর 0 হওয়া প্রয়োজন নেই `Rc<T>` instance পরিষ্কার করার জন্য।

যেহেতু `Weak<T>` যে value-কে reference করে তা ইতিমধ্যে drop হয়ে থাকতে পারে, একটি `Weak<T>` যে value-কে point করছে তার সাথে কিছু করতে হলে তোমাকে অবশ্যই নিশ্চিত করতে হবে যে value-টি এখনো বিদ্যমান। এটি একটি `Weak<T>` instance-এ `upgrade` method call করে করতে হয়, যা একটি `Option<Rc<T>>` return করবে। তুমি `Some` ফলাফল পাবে যদি `Rc<T>` value-টি এখনো drop না হয়ে থাকে এবং `None` ফলাফল পাবে যদি `Rc<T>` value-টি drop হয়ে গিয়ে থাকে। যেহেতু `upgrade` একটি `Option<Rc<T>>` return করে, Rust নিশ্চিত করবে যে `Some` case এবং `None` case handle করা হয়েছে, এবং কোনো invalid pointer থাকবে না।

একটি উদাহরণ হিসেবে, এমন একটি list ব্যবহার করার বদলে যার item গুলো শুধুমাত্র পরবর্তী item সম্পর্কে জানে, আমরা এমন একটি tree তৈরি করব যার item গুলো তাদের child item সম্পর্কে _এবং_ তাদের parent item সম্পর্কে জানে।

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-a-tree-data-structure-a-node-with-child-nodes"></a>

#### একটি Tree Data Structure তৈরি করা

শুরু করতে, আমরা এমন একটি tree বানাবো যার node গুলো তাদের child node সম্পর্কে জানে। আমরা `Node` নামে একটি struct তৈরি করব যা তার নিজের `i32` value এবং তার child `Node` value-এর reference ধারণ করবে:

<span class="filename">Filename: src/main.rs</span>

```rust
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Debug)]
struct Node {
    value: i32,
    children: RefCell<Vec<Rc<Node>>>,
}
```

আমরা চাই একটি `Node` তার children-কে own করুক, এবং আমরা সেই ownership variable গুলোর সাথে share করতে চাই যাতে আমরা tree-তে প্রতিটি `Node`-এ সরাসরি access করতে পারি। এটি করতে, আমরা `Vec<T>` item গুলোকে `Rc<Node>` type-এর value হিসেবে define করি। আমরা চাই কোন node গুলো অন্য একটি node-এর child তা modify করতে, তাই `children`-এ `Vec<Rc<Node>>`-এর চারপাশে একটি `RefCell<T>` আছে।

এরপর, আমরা আমাদের struct definition ব্যবহার করে `3` value সহ এবং কোনো child ছাড়া `leaf` নামের একটি `Node` instance এবং `5` value সহ এবং `leaf` তার একটি child হিসেবে থাকা `branch` নামের আরেকটি instance তৈরি করব, যেমন Listing 15-27-তে দেখানো হয়েছে।

<Listing number="15-27" file-name="src/main.rs" caption="Creating a `leaf` node with no children and a `branch` node with `leaf` as one of its children">

```rust
fn main() {
    let leaf = Rc::new(Node {
        value: 3,
        children: RefCell::new(vec![]),
    });

    let branch = Rc::new(Node {
        value: 5,
        children: RefCell::new(vec![Rc::clone(&leaf)]),
    });
}
```

</Listing>

আমরা `leaf`-এ থাকা `Rc<Node>`-কে clone করি এবং সেটি `branch`-এ store করি, যার অর্থ `leaf`-এ থাকা `Node`-এর এখন দুটি owner আছে: `leaf` এবং `branch`। আমরা `branch.children` এর মাধ্যমে `branch` থেকে `leaf`-এ যেতে পারি, কিন্তু `leaf` থেকে `branch`-এ যাওয়ার কোনো উপায় নেই। কারণ হলো `leaf`-এর `branch`-এর কোনো reference নেই এবং সে জানে না যে তারা related। আমরা চাই `leaf` জানুক যে `branch` তার parent। আমরা সেটি এরপর করব।

#### একটি Child থেকে তার Parent-এ Reference যোগ করা

Child node-কে তার parent সম্পর্কে সচেতন করতে, আমাদের `Node` struct definition-এ একটি `parent` field যোগ করতে হবে। সমস্যা হলো সিদ্ধান্ত নেওয়া যে `parent`-এর type কী হবে। আমরা জানি এটিতে একটি `Rc<T>` থাকতে পারে না, কারণ তাহলে `leaf.parent` যা `branch`-কে point করবে এবং `branch.children` যা `leaf`-কে point করবে তাদের সাথে একটি reference cycle তৈরি হবে, যার ফলে তাদের `strong_count` value গুলো কখনো 0 হবে না।

relationship গুলো অন্যভাবে ভাবলে, একটি parent node তার children-কে own করা উচিত: যদি একটি parent node drop করা হয়, তার child node গুলোও drop করা হওয়া উচিত। তবে, একটি child তার parent-কে own করা উচিত নয়: যদি আমরা একটি child node drop করি, parent এখনো বিদ্যমান থাকা উচিত। এটি weak reference-এর একটি ক্ষেত্র!

তাই, `Rc<T>`-এর বদলে, আমরা `parent`-এর type-টিকে `Weak<T>` ব্যবহার করতে হবে, বিশেষত একটি `RefCell<Weak<Node>>`। এখন আমাদের `Node` struct definition এরকম দেখায়:

<span class="filename">Filename: src/main.rs</span>

```rust
use std::cell::RefCell;
use std::rc::{Rc, Weak};

#[derive(Debug)]
struct Node {
    value: i32,
    parent: RefCell<Weak<Node>>,
    children: RefCell<Vec<Rc<Node>>>,
}
```

একটি node তার parent node-কে refer করতে পারবে কিন্তু তার parent-কে own করবে না। Listing 15-28-এ, আমরা `main`-কে এই নতুন definition ব্যবহার করতে update করি যাতে `leaf` node-এর তার parent `branch`-কে refer করার একটি উপায় থাকে।

<Listing number="15-28" file-name="src/main.rs" caption="A `leaf` node with a weak reference to its parent node, `branch`">

```rust
fn main() {
    let leaf = Rc::new(Node {
        value: 3,
        parent: RefCell::new(Weak::new()),
        children: RefCell::new(vec![]),
    });

    println!("leaf parent = {:?}", leaf.parent.borrow().upgrade());

    let branch = Rc::new(Node {
        value: 5,
        parent: RefCell::new(Weak::new()),
        children: RefCell::new(vec![Rc::clone(&leaf)]),
    });

    *leaf.parent.borrow_mut() = Rc::downgrade(&branch);

    println!("leaf parent = {:?}", leaf.parent.borrow().upgrade());
}
```

</Listing>

`leaf` node তৈরি করা Listing 15-27-এর মতোই, শুধু `parent` field ছাড়া: `leaf` এর শুরুতে কোনো parent নেই, তাই আমরা একটি নতুন, খালি `Weak<Node>` reference instance তৈরি করি।

এই মুহূর্তে, আমরা `upgrade` method ব্যবহার করে `leaf`-এর parent-এর একটি reference পাওয়ার চেষ্টা করলে, আমরা একটি `None` value পাই। আমরা এটি প্রথম `println!` statement-এর output-এ দেখি:

```text
leaf parent = None
```

যখন আমরা `branch` node তৈরি করি, এর `parent` field-এ একটি নতুন `Weak<Node>` reference থাকবে কারণ `branch`-এর কোনো parent node নেই। আমাদের কাছে এখনো `leaf` হিসেবে `branch`-এর একটি child আছে। একবার আমাদের কাছে `branch`-এ `Node` instance হয়ে গেলে, আমরা `leaf`-কে modify করে তাকে তার parent-এর একটি `Weak<Node>` reference দিতে পারি। আমরা `leaf`-এর `parent` field-এ থাকা `RefCell<Weak<Node>>`-এ `borrow_mut` method ব্যবহার করি, এবং তারপর আমরা `Rc::downgrade` function ব্যবহার করে `branch`-এ থাকা `Rc<Node>` থেকে `branch`-এর একটি `Weak<Node>` reference তৈরি করি।

যখন আমরা আবার `leaf`-এর parent print করি, এবার আমরা একটি `Some` variant পাব যা `branch` ধারণ করে: এখন `leaf` তার parent-এ access করতে পারে! যখন আমরা `leaf` print করি, আমরা সেই cycle-এর থেকেও বাঁচি যা Listing 15-26-এ যেমন stack overflow হয়েছিল; `Weak<Node>` reference-গুলো `(Weak)` হিসেবে print হয়:

```text
leaf parent = Some(Node { value: 5, parent: RefCell { value: (Weak) },
children: RefCell { value: [Node { value: 3, parent: RefCell { value: (Weak) },
children: RefCell { value: [] } }] } })
```

অসীম output না থাকা ইঙ্গিত করে যে এই code-এ কোনো reference cycle তৈরি হয়নি। আমরা `Rc::strong_count` এবং `Rc::weak_count` থেকে পাওয়া value গুলো দেখেও এটি বলতে পারি।

#### `strong_count` এবং `weak_count`-এর পরিবর্তন Visualize করা

চলো দেখি `Rc<Node>` instance-গুলোর `strong_count` এবং `weak_count` value গুলো কীভাবে পরিবর্তিত হয় — একটি নতুন inner scope তৈরি করে এবং `branch` তৈরি করা সেই scope-এ সরিয়ে। এটি করার ফলে, আমরা দেখতে পারি কী ঘটে যখন `branch` তৈরি করা হয় এবং তারপর যখন সেটি scope ছেড়ে যাওয়ার সময় drop হয়। পরিবর্তন গুলো Listing 15-29-তে দেখানো হয়েছে।

<Listing number="15-29" file-name="src/main.rs" caption="Creating `branch` in an inner scope and examining strong and weak reference counts">

```rust
fn main() {
    let leaf = Rc::new(Node {
        value: 3,
        parent: RefCell::new(Weak::new()),
        children: RefCell::new(vec![]),
    });

    println!(
        "leaf strong = {}, weak = {}",
        Rc::strong_count(&leaf),
        Rc::weak_count(&leaf),
    );

    {
        let branch = Rc::new(Node {
            value: 5,
            parent: RefCell::new(Weak::new()),
            children: RefCell::new(vec![Rc::clone(&leaf)]),
        });

        *leaf.parent.borrow_mut() = Rc::downgrade(&branch);

        println!(
            "branch strong = {}, weak = {}",
            Rc::strong_count(&branch),
            Rc::weak_count(&branch),
        );

        println!(
            "leaf strong = {}, weak = {}",
            Rc::strong_count(&leaf),
            Rc::weak_count(&leaf),
        );
    }

    println!("leaf parent = {:?}", leaf.parent.borrow().upgrade());
    println!(
        "leaf strong = {}, weak = {}",
        Rc::strong_count(&leaf),
        Rc::weak_count(&leaf),
    );
}
```

</Listing>

`leaf` তৈরির পর, এর `Rc<Node>`-এর strong count 1 এবং weak count 0। inner scope-এ, আমরা `branch` তৈরি করি এবং সেটিকে `leaf`-এর সাথে associate করি, যে মুহূর্তে আমরা count গুলো print করি, `branch`-এ থাকা `Rc<Node>`-এর strong count 1 এবং weak count 1 (কারণ `leaf.parent` একটি `Weak<Node>` দিয়ে `branch`-কে point করছে)। যখন আমরা `leaf`-এ count গুলো print করি, আমরা দেখব এর strong count 2 হবে কারণ `branch`-এ এখন `leaf`-এর `Rc<Node>`-এর একটি clone `branch.children`-এ store করা আছে কিন্তু এর weak count এখনো 0 থাকবে।

যখন inner scope শেষ হয়, `branch` scope ছেড়ে যায় এবং `Rc<Node>`-এর strong count 0-এ নেমে যায়, তাই এর `Node` drop হয়। `leaf.parent` থেকে weak count 1-এর কোনো প্রভাব নেই যে `Node` drop হবে কি না, তাই আমরা কোনো memory leak পাই না!

scope-এর শেষে আমরা `leaf`-এর parent access করার চেষ্টা করলে, আমরা আবার `None` পাব। program-এর শেষে, `leaf`-এ থাকা `Rc<Node>`-এর strong count 1 এবং weak count 0 কারণ variable `leaf` এখন আবার `Rc<Node>`-এর একমাত্র reference।

Count এবং value drop করা পরিচালনা করে এমন সব logic `Rc<T>` এবং `Weak<T>` এবং তাদের `Drop` trait implementation-এ built in। `Node`-এর definition-এ child থেকে তার parent-এ relationship একটি `Weak<T>` reference হওয়া উচিত বলে নির্দিষ্ট করে, তুমি parent node-গুলোকে child node-গুলোকে point করতে এবং উল্টোটাও করতে পারো কোনো reference cycle বা memory leak তৈরি না করে।

## Summary

এই chapter-এ আলোচনা করা হয়েছে কীভাবে smart pointer ব্যবহার করে Rust যে default guarantee এবং trade-off করে regular reference দিয়ে তার থেকে ভিন্ন guarantee এবং trade-off করা যায়। `Box<T>` type-এর একটি known size আছে এবং এটি heap-এ allocate করা data-কে point করে। `Rc<T>` type heap-এ থাকা data-এর reference সংখ্যা track রাখে যাতে data-এর একাধিক owner থাকতে পারে। interior mutability সহ `RefCell<T>` type আমাদের এমন একটি type দেয় যা আমরা তখন ব্যবহার করতে পারি যখন আমার একটি immutable type দরকার কিন্তু সেই type-এর একটি inner value পরিবর্তন করতে হবে; এটি borrowing rule গুলো compile time-এর বদলে runtime-এ enforce করে।

এছাড়াও আলোচনা করা হয়েছে `Deref` এবং `Drop` trait, যা smart pointer-এর অনেক functionality সক্ষম করে। আমরা reference cycle নিয়ে আলোচনা করেছি যা memory leak ঘটাতে পারে এবং কীভাবে `Weak<T>` ব্যবহার করে সেগুলো প্রতিরোধ করা যায়।

যদি এই chapter তোমার আগ্রহ জাগিয়ে থাকে এবং তুমি নিজের smart pointer implement করতে চাও, [“The Rustonomicon”][nomicon] দেখো আরও useful information-এর জন্য।

এরপর, আমরা Rust-এ concurrency নিয়ে আলোচনা করব। তুমি এমনকি আরও কয়েকটি নতুন smart pointer সম্পর্কেও জানবে।

[nomicon]: ../nomicon/index.html

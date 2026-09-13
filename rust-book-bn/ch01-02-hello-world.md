## Hello, World!

তুমি Rust install করে ফেলেছো, এখন সময় তোমার প্রথম Rust program লেখার। নতুন কোনো language শেখার সময় screen-এ `Hello, world!` text print করে এমন একটা ছোট program লেখাটা tradition — আমরাও এখানে সেটাই করবো!

> নোট: এই book ধরে নেয় তোমার command line-এর সাথে পরিচিতি আছে। Rust তোমার editing, tooling নিয়ে বা তোমার code কোথায় থাকবে নিয়ে কোনো specific দাবি করে না, তাই তুমি command line-এর বদলে IDE ব্যবহার করতে চাইলে তোমার পছন্দের IDE ব্যবহার করতে পারো। এখন অনেক IDE-এ কম-বেশি Rust support থাকে; বিস্তারিত জানতে সেই IDE-এর documentation দেখো। Rust team বর্তমানে `rust-analyzer`-এর মাধ্যমে চমৎকার IDE support নিশ্চিত করার দিকে মন দিচ্ছে। আরও বিস্তারিত জানতে [Appendix D][devtools]<!-- ignore --> দেখো।

<!-- Old headings. Do not remove or links may break. -->
<a id="creating-a-project-directory"></a>

### Project Directory তৈরি করা

তুমি প্রথমে একটা directory বানাবে তোমার Rust code রাখার জন্য। Rust-এর কাছে তোমার code কোথায় আছে সেটা গুরুত্বপূর্ণ নয়, কিন্তু এই book-এর exercise এবং project-গুলোর জন্য আমরা সাজেস্ট করছি তোমার home directory-তে একটা _projects_ directory বানাও এবং সব project সেখানেই রাখো।

একটা terminal খোলো এবং নিচের command-গুলো লিখে _projects_ directory এবং তার ভেতরে "Hello, world!" project-এর জন্য আরেকটা directory বানাও।

Linux, macOS এবং Windows-এর PowerShell-এর জন্য লেখো:

```console
$ mkdir ~/projects
$ cd ~/projects
$ mkdir hello_world
$ cd hello_world
```

Windows CMD-এর জন্য লেখো:

```cmd
> mkdir "%USERPROFILE%\projects"
> cd /d "%USERPROFILE%\projects"
> mkdir hello_world
> cd hello_world
```

<!-- Old headings. Do not remove or links may break. -->
<a id="writing-and-running-a-rust-program"></a>

### Rust Program-এর মৌলিক ধারণা

এরপর একটা নতুন source file বানাও এবং নাম দাও _main.rs_। Rust file-এর নাম সবসময় _.rs_ extension-এ শেষ হয়। তুমি যদি filename-এ একের বেশি word ব্যবহার করো, তাহলে convention হলো সেগুলোর মাঝে underscore ব্যবহার করা। যেমন, _helloworld.rs_ এর বদলে _hello_world.rs_ ব্যবহার করো।

এখন তুমি যে _main.rs_ file বানালে সেটা খোলো এবং Listing 1-1-এর code লেখো।

<Listing number="1-1" file-name="main.rs" caption="এমন একটা program যেটা `Hello, world!` print করে">

```rust
fn main() {
    println!("Hello, world!");
}
```

</Listing>

File-টা save করো এবং তোমার terminal window-এ _~/projects/hello_world_ directory-তে ফিরে যাও। Linux বা macOS-এ file-টা compile এবং run করতে নিচের command লেখো:

```console
$ rustc main.rs
$ ./main
Hello, world!
```

Windows-এ `./main` এর বদলে `.\main` command ব্যবহার করো:

```powershell
> rustc main.rs
> .\main
Hello, world!
```

তোমার operating system যেটাই হোক না কেন, terminal-এ `Hello, world!` string print হওয়ার কথা। এই output না দেখলে Installation section-এর ["Troubleshooting"][troubleshooting]<!-- ignore --> অংশে ফিরে যাও, সেখানে সাহায্য পাওয়ার উপায় লেখা আছে।

`Hello, world!` print হলে অভিনন্দন! তুমি অফিসিয়ালি একটা Rust program লিখেছো। এতে তুমি এখন একজন Rust programmer — স্বাগতম!

<!-- Old headings. Do not remove or links may break. -->

<a id="anatomy-of-a-rust-program"></a>

### একটা Rust Program-এর Anatomy

চলো এই "Hello, world!" program-টা বিস্তারিত দেখি। এই ছবির প্রথম অংশটা হলো:

```rust
fn main() {

}
```

এই line-গুলো `main` নামে একটা function define করে। `main` function-টা বিশেষ: প্রতিটা executable Rust program-এ সবার আগে এই function-টার code-ই run হয়। এখানে প্রথম line-এ `main` নামে এমন একটা function declare করা হয়েছে যার কোনো parameter নেই এবং যেটা কিছু return করে না। যদি parameter থাকতো, সেগুলো parentheses-এর (`()`) ভেতরে থাকতো।

Function body `{}` দিয়ে ঘেরা। Rust-এ সব function body-র চারপাশে curly bracket থাকতে হবে। ভালো style হলো opening curly bracket function declaration-এর একই line-এ রাখা, মাঝখানে একটা space দিয়ে।

> নোট: তুমি যদি Rust project-গুলোতে একটা standard style মেনে চলতে চাও, তাহলে `rustfmt` নামের একটা automatic formatter tool ব্যবহার করতে পারো, যেটা তোমার code-কে একটা specific style-এ ফরম্যাট করে দেয় (`rustfmt` নিয়ে বিস্তারিত [Appendix D][devtools]<!-- ignore -->-এ আছে)। Rust team এই tool-টা standard Rust distribution-এর সাথে দেয়, ঠিক যেমন `rustc` দেয়, তাই এটা সম্ভবত তোমার কম্পিউটারে আগেই install হয়ে আছে!

`main` function-এর body-তে নিচের code আছে:

```rust
println!("Hello, world!");
```

এই ছোট program-এ সব কাজ এই line-টাই করে: screen-এ text print করে। এখানে তিনটা জিনিস খেয়াল করার আছে।

প্রথমত, `println!` একটা Rust macro call করে। যদি এটা function call করতো, তাহলে এটা লেখা হতো `println` (`!` ছাড়া)। Rust macro হলো এমন একটা উপায় যেখানে code লিখলে সেটা আরও code generate করে Rust syntax-কে expand করে; [Chapter 20][ch20-macros]<!-- ignore -->-এ এটা নিয়ে বিস্তারিত আলোচনা করা হয়েছে। আপাতত তোমার শুধু এটা জানা দরকার যে `!` ব্যবহার করলে বোঝায় তুমি function নয়, macro call করছো, এবং macro সবসময় function-এর মতো একই rule মানে না।

দ্বিতীয়ত, তুমি `"Hello, world!"` string দেখতে পাচ্ছো। আমরা এই string-টা `println!`-এ argument হিসেবে pass করি, আর এই string-টা screen-এ print হয়।

তৃতীয়ত, line-টা একটা semicolon (`;`) দিয়ে শেষ হয়েছে, যেটা বোঝায় এই expression-টা শেষ এবং পরেরটা শুরু হতে প্রস্তুত। Rust code-এর বেশিরভাগ line semicolon দিয়ে শেষ হয়।

<!-- Old headings. Do not remove or links may break. -->
<a id="compiling-and-running-are-separate-steps"></a>

### Compilation এবং Execution

তুমি এইমাত্র একটা নতুন বানানো program run করলে, চলো এখন process-টার প্রতিটা step বুঝে নিই।

Rust program run করার আগে তোমাকে অবশ্যই Rust compiler দিয়ে সেটা compile করতে হবে — `rustc` command লিখে তোমার source file-এর নাম pass করো, এমনভাবে:

```console
$ rustc main.rs
```

তোমার যদি C বা C++ background থাকে, তুমি খেয়াল করবে এটা `gcc` বা `clang`-এর মতো। সফলভাবে compile হওয়ার পর Rust একটা binary executable output দেয়।

Linux, macOS এবং Windows-ের PowerShell-এ shell-এ `ls` command দিয়ে executable দেখতে পাবে:

```console
$ ls
main  main.rs
```

Linux এবং macOS-এ তুমি দুটো file দেখতে পাবে। Windows-ের PowerShell-ে তুমি সেই তিনটো file দেখতে পাবে যেগুলো CMD ব্যবহার করলে দেখা যায়। Windows-ের CMD-তে তুমি নিচের command লেখো:

```cmd
> dir /B %= the /B option says to only show the file names =%
main.exe
main.pdb
main.rs
```

এখানে দেখা যাচ্ছে _.rs_ extension সহ source code file, executable file (Windows-ে _main.exe_, কিন্তু অন্য সব platform-ে _main_), এবং Windows ব্যবহার করলে debugging information সহ _.pdb_ extension-এর একটা file। এখান থেকে তুমি _main_ বা _main.exe_ file run করো, এভাবে:

```console
$ ./main # or .\main on Windows
```

তোমার _main.rs_ যদি "Hello, world!" program হয়, এই line তোমার terminal-ে `Hello, world!` print করবে।

তুমি যদি Ruby, Python বা JavaScript-এর মতো dynamic language-এর সাথে বেশি পরিচিত থাকো, তাহলে compile এবং run করাকে আলাদা step হিসেবে না ভাবতে অভ্যস্ত নাও হতে পারো। Rust একটা _ahead-of-time compiled_ language, অর্থাৎ তুমি একটা program compile করে executable অন্য কাউকে দিতে পারো, আর তার কম্পিউটারে Rust install না থাকলেও সে সেটা run করতে পারবে। কিন্তু তুমি কাউকে _.rb_, _.py_ বা _.js_ file দিলে তার কাছে Ruby, Python বা JavaScript implementation install থাকতে হবে (যথাক্রমে)। কিন্তু সেই language-গুলোতে একটাই command-এ compile এবং run করা যায়। Language design-এ সবকিছুই এক ধরনের trade-off।

শুধু `rustc` দিয়ে compile করা ছোট program-ের জন্য চলে, কিন্তু তোমার project বড় হলে সব option manage করতে এবং code share করা সহজ করতে চাইবে। এরপরে আমরা তোমাকে Cargo tool-এর সাথে পরিচয় করিয়ে দেবো, যেটা real-world Rust program লেখায় সাহায্য করবে।

[troubleshooting]: ch01-01-installation.html#troubleshooting
[devtools]: appendix-04-useful-development-tools.html
[ch20-macros]: ch20-05-macros.html

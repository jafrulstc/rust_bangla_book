## Graceful Shutdown এবং Cleanup

Listing 21-20-এর code একটি thread pool ব্যবহারের মাধ্যমে আমাদের ইচ্ছানুযায়ী request গুলোকে asynchronously সাড়া দিচ্ছে। আমরা কিছু warning পাই `workers`, `id` এবং `thread` field গুলো সম্পর্কে যেগুলো আমরা সরাসরি ব্যবহার করছি না—এটি আমাদের মনে করিয়ে দেয় যে আমরা কিছুই cleanup করছি না। যখন আমরা কম সুন্দর <kbd>ctrl</kbd>-<kbd>C</kbd> পদ্ধতি ব্যবহার করে main thread কে থামাই, অন্য সব thread-কেও সাথে সাথে থামিয়ে দেওয়া হয়, এমনকি তারা যদি কোনো request serve করার মাঝখানেও থাকে।

তাহলে এরপর, আমরা pool-এর প্রতিটি thread-এ `join` call করতে `Drop` trait implement করবো, যাতে তারা বন্ধ হওয়ার আগে তারা যে কাজ করছে সেটি শেষ করতে পারে। তারপর, আমরা thread গুলোকে জানানোর একটি উপায় implement করবো যে তাদের নতুন request গ্রহণ করা বন্ধ করে shut down করা উচিত। এই code কাজ করতে দেখতে আমরা আমাদের server কে পরিবর্তন করবো যাতে সে শুধুমাত্র দুটি request গ্রহণ করে এবং তারপর তার thread pool কে gracefully shut down করে।

এগিয়ে যাওয়ার সময় একটি বিষয় খেয়াল রাখো: এর কোনোটাই closure execute করার অংশটি handle করে না, তাই এখানে সবকিছু একই থাকতো যদি আমরা একটি async runtime-এর জন্য thread pool ব্যবহার করতাম।

### `ThreadPool`-এ `Drop` Trait Implement করা

চলো আমাদের thread pool-এ `Drop` implement করা থেকে শুরু করি। Pool টি drop হলে আমাদের thread গুলোর সবাই যাতে তাদের কাজ শেষ করে তা নিশ্চিত করতে join করা উচিত। Listing 21-22 একটি `Drop` implementation-এর প্রথম চেষ্টা দেখায়; এই code টি এখনও ঠিকমতো কাজ করবে না।

<Listing number="21-22" file-name="src/lib.rs" caption="Joining each thread when the thread pool goes out of scope">

```rust,ignore,does_not_compile
impl Drop for ThreadPool {
    fn drop(&mut self) {
        for worker in &mut self.workers {
            println!("Shutting down worker {}", worker.id);

            worker.thread.join().unwrap();
        }
    }
}
```

</Listing>

প্রথমে, আমরা thread pool-এর প্রতিটি `workers`-এর মধ্য দিয়ে loop করি। আমরা এর জন্য `&mut` ব্যবহার করি কারণ `self` একটি mutable reference, এবং আমাদের `worker` কে mutate করার ক্ষমতাও দরকার। প্রতিটি `worker`-এর জন্য, আমরা একটি বার্তা প্রিন্ট করি যে এই নির্দিষ্ট `Worker` instance shut down হচ্ছে, এবং তারপর সেই `Worker` instance-এর thread-এ `join` call করি। যদি `join` call ব্যর্থ হয়, আমরা `unwrap` ব্যবহার করি যাতে Rust panic করে এবং একটি ungraceful shutdown-এ চলে যায়।

নিচে এই code compile করার সময় আমরা যে error টি পাই তা দেখানো হলো:

```console
$ cargo check
    Checking hello v0.1.0 (file:///projects/hello)
error[E0507]: cannot move out of `worker.thread` which is behind a mutable reference
  --> src/lib.rs:52:13
   |
52 |             worker.thread.join().unwrap();
   |             ^^^^^^^^^^^^^ ------ `worker.thread` moved due to this method call
   |             |
   |             move occurs because `worker.thread` has type `JoinHandle<()>`, which does not implement the `Copy` trait
   |
note: `JoinHandle::<T>::join` takes ownership of the receiver `self`, which moves `worker.thread`
  --> /rustc/88d9e12ae178fab0fb5cc050a94da85685d449ea/library/std/src/thread/join_handle.rs:149:16

For more information about this error, try `rustc --explain E0507`.
error: could not compile `hello` (lib) due to 1 previous error
```

error টি আমাদের বলছে আমরা `join` call করতে পারি না কারণ প্রতিটি `worker`-এর শুধু একটি mutable borrow আছে এবং `join` তার argument-এর ownership নেয়। এই সমস্যাটি সমাধান করতে আমাদের `thread`-কে `Worker` instance থেকে বের করে আনতে হবে যেটি `thread` এর owner, যাতে `join` thread-টিকে consume করতে পারে। এটি করার একটি উপায় হলো Listing 18-15-এ যে পদ্ধতি নিয়েছিলাম সেটা। যদি `Worker` একটি `Option<thread::JoinHandle<()>>` ধরে রাখতো, আমরা `Option`-এ `take` method call করতে পারতাম মানটিকে `Some` variant থেকে বের করে আনতে এবং তার জায়গায় একটি `None` variant রেখে যেতে। অন্য কথায়, একটি চলমান `Worker`-এর `thread`-এ একটি `Some` variant থাকতো, এবং যখন আমরা একটি `Worker` cleanup করতে চাইতাম, আমরা `Some` কে `None` দিয়ে replace করতাম যাতে `Worker`-এর চালানোর জন্য আর কোনো thread না থাকে।

তবে, এই প্রয়োজন শুধুমাত্র তখনই উঠতো যখন আমরা `Worker` drop করতাম। এর বিনিময়ে, আমাদের `worker.thread` access করা যেখানেই সেখানে একটি `Option<thread::JoinHandle<()>>` নিয়ে কাজ করতে হতো। Idiomatic Rust `Option`-কে অনেক ব্যবহার করে, কিন্তু যখন তুমি নিজেকে এমন কিছু যা সবসময় থাকে জানো তাকে এইরকম workaround হিসেবে `Option`-এ wrap করতে দেখো, তখনই এটি একটি ভালো ধারণা যে তোমার code কে আরও পরিষ্কার এবং কম error-prone করার জন্য alternative approach খুঁজে দেখো।

এই ক্ষেত্রে, একটি উন্নত alternative আছে: `Vec::drain` method। এটি একটি range parameter গ্রহণ করে যা নির্দিষ্ট করে কোন কোন item-কে vector থেকে সরাতে হবে এবং সেই item-গুলোর একটি iterator return করে। `..` range syntax পাস করলে vector থেকে *সব* value সরে যাবে।

সুতরাং, আমাদের `ThreadPool`-এর `drop` implementation টি এভাবে আপডেট করতে হবে:

<Listing file-name="src/lib.rs">

```rust
impl Drop for ThreadPool {
    fn drop(&mut self) {
        for worker in self.workers.drain(..) {
            println!("Shutting down worker {}", worker.id);

            worker.thread.join().unwrap();
        }
    }
}
```

</Listing>

এটি compiler error টি সমাধান করে এবং আমাদের code-এ আর কোনো পরিবর্তনের প্রয়োজন নেই। মনে রেখো, যেহেতু drop কে panicking অবস্থায়ও call করা যেতে পারে, unwrap-ও panic করতে পারে এবং একটি double panic ঘটাতে পারে, যা সাথে সাথে program কে crash করে এবং চলমান যেকোনো cleanup শেষ করে দেয়। একটি example program-এর জন্য এটি ঠিক আছে, কিন্তু production code-এর জন্য এটি প্রস্তাবিত নয়।

### Thread গুলোকে Job শোনা থামিয়ে দেওয়ার সংকেত দেওয়া

আমরা যতগুলো পরিবর্তন করেছি তার সাথে আমাদের code এখন কোনো warning ছাড়াই compile হয়। তবে খারাপ খবর হলো এই code টি এখনও আমরা যেভাবে চাই সেভাবে কাজ করে না। মূল বিষয় হলো `Worker` instance-দের thread দ্বারা চালিত closure গুলোর logic: এই মুহূর্তে, আমরা `join` call করি, কিন্তু সেটি thread গুলোকে shut down করবে না, কারণ তারা job খোঁজার জন্য চিরকাল `loop` করে। যদি আমরা আমাদের বর্তমান `drop` implementation সহ আমাদের `ThreadPool` drop করার চেষ্টা করি, main thread চিরকাল block করবে, প্রথম thread শেষ হওয়ার জন্য অপেক্ষা করবে।

এই সমস্যাটি ঠিক করতে আমাদের `ThreadPool`-এর `drop` implementation-এ একটি পরিবর্তন এবং তারপর `Worker` loop-এ আরেকটি পরিবর্তন দরকার।

প্রথমে, আমরা `ThreadPool`-এর `drop` implementation কে পরিবর্তন করবো যাতে thread গুলো শেষ হওয়ার জন্য অপেক্ষা করার আগে স্পষ্টভাবে `sender` drop করে। Listing 21-23 `ThreadPool`-এ `sender` স্পষ্টভাবে drop করার পরিবর্তন গুলো দেখায়। thread-এর ক্ষেত্রে যার বিপরীত ছিল, এখানে আমরা _সত্যিই_ `ThreadPool` থেকে `sender` কে `Option::take` দিয়ে বের করে আনতে একটি `Option` ব্যবহার করতে বাধ্য।

<Listing number="21-23" file-name="src/lib.rs" caption="Explicitly dropping `sender` before joining the `Worker` threads">

```rust,noplayground,not_desired_behavior
pub struct ThreadPool {
    workers: Vec<Worker>,
    sender: Option<mpsc::Sender<Job>>,
}
// --snip--
impl ThreadPool {
    pub fn new(size: usize) -> ThreadPool {
        // --snip--

        ThreadPool {
            workers,
            sender: Some(sender),
        }
    }

    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);

        self.sender.as_ref().unwrap().send(job).unwrap();
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        drop(self.sender.take());

        for worker in self.workers.drain(..) {
            println!("Shutting down worker {}", worker.id);

            worker.thread.join().unwrap();
        }
    }
}
```

</Listing>

`sender` drop করা channel কে বন্ধ করে দেয়, যা নির্দেশ করে যে আর কোনো message পাঠানো হবে না। যখন এমন হয়, `Worker` instance গুলো infinite loop-এ যে `recv` call গুলো করে তা সবই একটি error return করবে। Listing 21-24-এ, আমরা `Worker` loop কে পরিবর্তন করি যাতে সেই case-এ gracefully loop থেকে বেরিয়ে আসে, যার মানে `ThreadPool`-এর `drop` implementation যখন তাদের ওপর `join` call করবে তখন thread গুলো শেষ হবে।

<Listing number="21-24" file-name="src/lib.rs" caption="Explicitly breaking out of the loop when `recv` returns an error">

```rust,noplayground
impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        let thread = thread::spawn(move || {
            loop {
                let message = receiver.lock().unwrap().recv();

                match message {
                    Ok(job) => {
                        println!("Worker {id} got a job; executing.");

                        job();
                    }
                    Err(_) => {
                        println!("Worker {id} disconnected; shutting down.");
                        break;
                    }
                }
            }
        });

        Worker { id, thread }
    }
}
```

</Listing>

এই code কাজ করতে দেখতে আমরা `main` কে পরিবর্তন করবো যাতে সে server কে gracefully shut down করার আগে শুধু দুটি request গ্রহণ করে, যেমন Listing 21-25-তে দেখানো হয়েছে।

<Listing number="21-25" file-name="src/main.rs" caption="Shutting down the server after serving two requests by exiting the loop">

```rust,ignore
fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    let pool = ThreadPool::new(4);

    for stream in listener.incoming().take(2) {
        let stream = stream.unwrap();

        pool.execute(|| {
            handle_connection(stream);
        });
    }

    println!("Shutting down.");
}
```

</Listing>

বাস্তব কোনো web server কে শুধু দুটি request serve করে shut down করতে তুমি চাইবে না। এই code টি শুধু demonstrate করে যে graceful shutdown এবং cleanup কাজ করছে।

`take` method টি `Iterator` trait-এ define করা এবং iteration কে সর্বোচ্চ প্রথম দুটি item-এ সীমিত করে। `ThreadPool` `main`-এর শেষে scope-এর বাইরে যাবে, এবং `drop` implementation চলবে।

`cargo run` দিয়ে server শুরু করো এবং তিনটি request করো। তৃতীয় request-টি error করবে, এবং তোমার terminal-এ তুমি নিচের মতো output দেখতে পাবে:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-25
cargo run
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
third request will error because server will have shut down
copy output below
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.41s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Shutting down.
Shutting down worker 0
Worker 3 got a job; executing.
Worker 1 disconnected; shutting down.
Worker 2 disconnected; shutting down.
Worker 3 disconnected; shutting down.
Worker 0 disconnected; shutting down.
Shutting down worker 1
Shutting down worker 2
Shutting down worker 3
```

তুমি হয়তো `Worker` ID এবং প্রিন্ট হওয়া message-গুলোর ভিন্ন ক্রম দেখতে পাবে। এই message গুলো থেকে আমরা বুঝতে পারি এই code কীভাবে কাজ করে: `Worker` instance 0 এবং 3 প্রথম দুটি request পেয়েছে। দ্বিতীয় connection-এর পর server connection গ্রহণ করা বন্ধ করে দিয়েছে, এবং `ThreadPool`-এর `Drop` implementation `Worker 3`-এর কাজ শুরু হওয়ার আগেই execute হতে শুরু করেছে। `sender` drop করায় সব `Worker` instance disconnect হয়ে যায় এবং তাদের shut down করতে বলা হয়। প্রতিটি `Worker` instance disconnect হলে একটি বার্তা প্রিন্ট করে, এবং তারপর thread pool প্রতিটি `Worker` thread শেষ হওয়ার জন্য অপেক্ষা করতে `join` call করে।

এই নির্দিষ্ট সম্পাদনের একটি আকর্ষণীয় দিক খেয়াল করো: `ThreadPool` `sender` drop করেছে, এবং যেকোনো `Worker` error পাওয়ার আগেই আমরা `Worker 0`-এ join করার চেষ্টা করেছি। `Worker 0` এখনও `recv` থেকে error পায়নি, তাই main thread block করে, `Worker 0`-এর শেষ হওয়ার জন্য অপেক্ষা করছে। ইতিমধ্যে, `Worker 3` একটি job গ্রহণ করেছে এবং তারপর সব thread-ই error পেয়েছে। `Worker 0` যখন শেষ হয়, main thread বাকি `Worker` instance গুলো শেষ হওয়ার জন্য অপেক্ষা করেছে। সেই মুহূর্তে, তারা সবাই তাদের loop থেকে বেরিয়ে এসে থেমে গিয়েছিল।

অভিনন্দন! আমরা এখন আমাদের project সম্পন্ন করেছি; আমাদের একটি মৌলিক web server আছে যেটি asynchronously সাড়া দিতে একটি thread pool ব্যবহার করে। আমরা server এর একটি graceful shutdown করতে পারি, যা pool-এর সব thread-কে cleanup করে।

রেফারেন্সের জন্য সম্পূর্ণ code এখানে দেওয়া হলো:

<Listing file-name="src/main.rs">

```rust,ignore
use hello::ThreadPool;
use std::{
    fs,
    io::{BufReader, prelude::*},
    net::{TcpListener, TcpStream},
    thread,
    time::Duration,
};

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    let pool = ThreadPool::new(4);

    for stream in listener.incoming().take(2) {
        let stream = stream.unwrap();

        pool.execute(|| {
            handle_connection(stream);
        });
    }

    println!("Shutting down.");
}

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let request_line = buf_reader.lines().next().unwrap().unwrap();

    let (status_line, filename) = match &request_line[..] {
        "GET / HTTP/1.1" => ("HTTP/1.1 200 OK", "hello.html"),
        "GET /sleep HTTP/1.1" => {
            thread::sleep(Duration::from_secs(5));
            ("HTTP/1.1 200 OK", "hello.html")
        }
        _ => ("HTTP/1.1 404 NOT FOUND", "404.html"),
    };

    let contents = fs::read_to_string(filename).unwrap();
    let length = contents.len();

    let response =
        format!("{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}");

    stream.write_all(response.as_bytes()).unwrap();
}
```

</Listing>

<Listing file-name="src/lib.rs">

```rust,noplayground
use std::{
    sync::{Arc, Mutex, mpsc},
    thread,
};

pub struct ThreadPool {
    workers: Vec<Worker>,
    sender: Option<mpsc::Sender<Job>>,
}

type Job = Box<dyn FnOnce() + Send + 'static>;

impl ThreadPool {
    /// Create a new ThreadPool.
    ///
    /// The size is the number of threads in the pool.
    ///
    /// # Panics
    ///
    /// The `new` function will panic if the size is zero.
    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        let (sender, receiver) = mpsc::channel();

        let receiver = Arc::new(Mutex::new(receiver));

        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            workers.push(Worker::new(id, Arc::clone(&receiver)));
        }

        ThreadPool {
            workers,
            sender: Some(sender),
        }
    }

    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);

        self.sender.as_ref().unwrap().send(job).unwrap();
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        drop(self.sender.take());

        for worker in &mut self.workers {
            println!("Shutting down worker {}", worker.id);

            if let Some(thread) = worker.thread.take() {
                thread.join().unwrap();
            }
        }
    }
}

struct Worker {
    id: usize,
    thread: Option<thread::JoinHandle<()>>,
}

impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        let thread = thread::spawn(move || {
            loop {
                let message = receiver.lock().unwrap().recv();

                match message {
                    Ok(job) => {
                        println!("Worker {id} got a job; executing.");

                        job();
                    }
                    Err(_) => {
                        println!("Worker {id} disconnected; shutting down.");
                        break;
                    }
                }
            }
        });

        Worker {
            id,
            thread: Some(thread),
        }
    }
}
```

</Listing>

আমরা এখানে আরও অনেক কিছু করতে পারি! তুমি যদি এই project আরও উন্নত করতে চাও, এখানে কিছু ধারণা দেওয়া হলো:

- `ThreadPool` এবং তার public method-গুলোর জন্য আরও documentation যোগ করো।
- library-র কার্যকারিতার test যোগ করো।
- `unwrap` call গুলোকে আরও robust error handling-এ পরিবর্তন করো।
- `ThreadPool` ব্যবহার করে web request serve করা ছাড়া অন্য কোনো task সম্পাদন করো।
- [crates.io](https://crates.io/)-এ কোনো thread pool crate খুঁজে বের করো এবং সেই crate ব্যবহার করে একই রকম একটি web server implement করো। তারপর, এর API এবং robustness আমরা যে thread pool implement করেছি তার সাথে তুলনা করো।

## Summary

দারুণ করেছো! তুমি বইয়ের শেষ পর্যন্ত পৌঁছে গেছো! এই Rust ভ্রমণে আমাদের সাথে থাকার জন্য তোমাকে ধন্যবাদ। তুমি এখন নিজের Rust project implement করতে এবং অন্যদের project-এ সাহায্য করতে প্রস্তুত। মনে রাখবে, Rustacean-দের একটি স্বাগত জানানো community আছে যারা তোমার Rust যাত্রায় যেকোনো চ্যালেঞ্জে তোমাকে সাহায্য করতে আগ্রহী।

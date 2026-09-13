## একটি Single-Threaded Web Server তৈরি করা

আমরা শুরুতে একটি single-threaded web server কাজ করা অবস্থায় নিয়ে আসবো। কাজে নামার আগে web server তৈরির সাথে যুক্ত protocol গুলো সম্পর্কে একটা সংক্ষিপ্ত ধারণা নিয়ে নিই। এই protocol গুলোর বিস্তারিত আলোচনা এই বইয়ের আওতার বাইরে, কিন্তু একটা ছোট overview তোমাকে প্রয়োজনীয় তথ্য দেবে।

Web server-এর সাথে যুক্ত দুটি প্রধান protocol হলো _Hypertext Transfer Protocol_ _(HTTP)_ এবং _Transmission Control Protocol_ _(TCP)_। দুটোই _request-response_ protocol, অর্থাৎ একজন _client_ request শুরু করে এবং একজন _server_ সেই request গুলো শোনে ও client-কে response দেয়। এই request আর response গুলোর ভেতরে কী থাকবে সেটা protocol গুলোই নির্ধারণ করে।

TCP হলো নিচু স্তরের একটি protocol যেটি বর্ণনা করে যে তথ্য একটি server থেকে অন্যটিতে কীভাবে পৌঁছায়, কিন্তু সেই তথ্য আসলে কী সেটা নির্দিষ্ট করে না। HTTP, TCP-এর ওপর ভর করেই দাঁড়িয়ে আছে—request আর response-এর ভেতরের বিষয়বস্তু নির্ধারণ করে। প্রযুক্তিগতভাবে অন্যান্য protocol-এর সাথেও HTTP ব্যবহার করা সম্ভব, কিন্তু বেশিরভাগ ক্ষেত্রেই HTTP তার ডেটা TCP-এর মাধ্যমে পাঠায়। আমরা TCP আর HTTP request ও response-এর কাঁচা byte নিয়ে কাজ করবো।

### TCP Connection শোনা

আমাদের web server-কে একটি TCP connection শুনতে হবে, তাই এটিই আমরা প্রথমে তৈরি করবো। Standard library একটি `std::net` module দেয় যেটি আমাদের এই কাজ করতে সাহায্য করে। স্বাভাবিক পদ্ধতিতে একটি নতুন project তৈরি করি:

```console
$ cargo new hello
     Created binary (application) `hello` project
$ cd hello
```

এবার শুরু করার জন্য _src/main.rs_-এ Listing 21-1-এর code টি লেখো। এই code টি ইনকামিং TCP stream-এর জন্য লোকাল ঠিকানা `127.0.0.1:7878`-এ শুনবে। যখনই কোনো incoming stream পাবে, সে `Connection established!` প্রিন্ট করবে।

<Listing number="21-1" file-name="src/main.rs" caption="Listening for incoming streams and printing a message when we receive a stream">

```rust,no_run
use std::net::TcpListener;

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        println!("Connection established!");
    }
}
```

</Listing>

`TcpListener` ব্যবহার করে আমরা `127.0.0.1:7878` ঠিকানায় TCP connection শুনতে পারি। এই ঠিকানায় colon-এর আগের অংশটি হলো IP address যেটা তোমার কম্পিউটারকে নির্দেশ করে (এটা প্রতিটি কম্পিউটারে একই এবং বিশেষভাবে লেখকদের কম্পিউটারকে নির্দেশ করে না), আর `7878` হলো port। দুটি কারণে এই port বেছে নিয়েছি: HTTP সাধারণত এই port-এ গ্রহণ করা হয় না, তাই তোমার মেশিনে চলা অন্য কোনো web server-এর সাথে আমাদের server-এর সংঘাত হওয়ার সম্ভাবনা কম, আর 7878 হলো টেলিফোনে টাইপ করা _rust_ শব্দটি।

এই পরিস্থিতিতে `bind` function টি `new` function-এর মতোই কাজ করে—এটি একটি নতুন `TcpListener` instance return করে। এই function-এর নাম `bind` কারণ networking-এ কোনো port-এ শোনার জন্য সংযুক্ত হওয়াকে “binding to a port” বলা হয়।

`bind` function একটি `Result<T, E>` return করে, যা থেকে বোঝানো যায় যে binding ব্যর্থ হওয়ার সম্ভাবনা আছে—যেমন আমরা যদি আমাদের program-এর দুটি instance চালাই, ফলে দুটো program একই port-এ শুনতে চায়। যেহেতু আমরা শেখার জন্য মাত্র একটি সাধারণ server লিখছি, তাই এ ধরনের error handle করা নিয়ে মাথা ঘামাবো না; বরং error হলে program থামাতে আমরা `unwrap` ব্যবহার করবো।

`TcpListener`-এর `incoming` method একটি iterator return করে যা আমাদের stream-এর একটি sequence দেয় (আরও নির্দিষ্টভাবে বললে `TcpStream` type-এর stream)। একটি _stream_ হলো client আর server-এর মধ্যে খোলা একটি connection। _Connection_ হলো সম্পূর্ণ request ও response process-টির নাম—যেখানে client server-এর সাথে সংযুক্ত হয়, server একটি response তৈরি করে, তারপর server connection বন্ধ করে দেয়। সুতরাং, আমরা `TcpStream` থেকে পড়বো যাতে client কী পাঠিয়েছে তা দেখতে পাই এবং তারপর আমাদের response সেই stream-এ লিখবো যাতে client-কে ডেটা ফেরত পাঠানো যায়। সব মিলিয়ে, এই `for` loop টি প্রতিটি connection পর্যায়ক্রমে process করবে এবং আমাদের সামলানোর জন্য stream-এর একটি সিরিজ তৈরি করবে।

আপাতত, stream handle করার কাজটা শুধু `unwrap` করে রাখা—stream-এ কোনো error থাকলে program terminate হয়ে যাবে; আর error না থাকলে program একটি বার্তা প্রিন্ট করবে। পরের listing-এ আমরা success case-এর জন্য আরও কার্যকারিতা যোগ করবো। `incoming` method থেকে আমরা error পেতে পারি, কারণ আমরা আসলে connection-এর ওপর iterate করছি না; বরং আমরা _connection attempt_ গুলোর ওপর iterate করছি। নানা কারণে connection সফল নাও হতে পারে, যার অনেকগুলো operating system নির্ভর। যেমন, অনেক operating system-এ একসাথে খোলা রাখা যায় এমন connection-এর সংখ্যার একটা সীমা থাকে; সেই সীমার চেয়ে বেশি নতুন connection attempt এলে কিছু খোলা connection বন্ধ না হওয়া পর্যন্ত সেগুলো error তৈরি করবে।

চলো এই code টি চালিয়ে দেখি! terminal-এ `cargo run` চালাও এবং তারপর একটি web browser-এ _127.0.0.1:7878_ লোড করো। Browser-এ “Connection reset” এর মতো একটা error বার্তা দেখাবে, কারণ server এই মুহূর্তে কোনো ডেটা ফেরত পাঠাচ্ছে না। কিন্তু terminal-এ তাকালে দেখবে বেশ কিছু বার্তা প্রিন্ট হয়েছে যখন browser সেই server-এর সাথে সংযুক্ত হয়েছিল!

```text
     Running `target/debug/hello`
Connection established!
Connection established!
Connection established!
```

মাঝে মাঝে একটি browser request-এর জন্য একাধিক বার্তা প্রিন্ট হতে দেখবে; এর কারণ হতে পারে browser পেজের জন্য একটি request পাঠাচ্ছে এবং সাথে সাথে browser tab-এ দেখা _favicon.ico_ icon-এর মতো অন্যান্য resource-এর জন্যও request পাঠাচ্ছে।

আরও হতে পারে যে browser একাধিকবার server-এর সাথে সংযুক্ত হওয়ার চেষ্টা করছে, কারণ server কোনো ডেটা দিয়ে সাড়া দিচ্ছে না। loop-এর শেষে `stream` scope-এর বাইরে গিয়ে drop হলে connection `drop` implementation-এর অংশ হিসেবে বন্ধ হয়ে যায়। Browser গুলো মাঝে মাঝে বন্ধ হয়ে যাওয়া connection আবার retry করে, কারণ সমস্যাটা সাময়িক হতে পারে।

Browser গুলো কখনো কখনো কোনো request না পাঠিয়েই server-এর সাথে একাধিক connection খোলে, যাতে পরে যদি *তারা* request পাঠায়, সেগুলো দ্রুত সম্পন্ন হতে পারে। যখন এমন হয়, আমাদের server প্রতিটি connection-ই দেখতে পাবে, সেই connection-এ কোনো request আছে কি না তা গুরুত্ব না দিয়েই। Chrome-based browser-এর অনেক version এমন আচরণ করে; তুমি private browsing mode ব্যবহার করে বা অন্য কোনো browser দিয়ে সেই optimization বন্ধ করতে পারবে।

গুরুত্বপূর্ণ বিষয় হলো, আমরা সফলভাবে একটি TCP connection-এর handle পেয়ে গেছি!

কোনো একটি নির্দিষ্ট version-এর code চালানো শেষ হলে <kbd>ctrl</kbd>-<kbd>C</kbd> চেপে program থামাতে মনে রেখো। তারপর প্রতিবার code-এ পরিবর্তন করার পর নতুন code চালাও বলে নিশ্চিত করতে `cargo run` কমান্ড দিয়ে আবার program চালাও।

### Request পড়া

Browser থেকে request পড়ার কার্যকারিতা implement করি! প্রথমে connection পাওয়ার কাজটা আর সেই connection নিয়ে কোনো কাজ করার কাজটা আলাদা রাখতে, আমরা connection process করার জন্য একটি নতুন function শুরু করবো। এই নতুন `handle_connection` function-এ আমরা TCP stream থেকে ডেটা পড়বো এবং সেটি প্রিন্ট করবো, যাতে browser থেকে পাঠানো ডেটা আমরা দেখতে পাই। code টি পরিবর্তন করে Listing 21-2-এর মতো করে নাও।

<Listing number="21-2" file-name="src/main.rs" caption="Reading from the `TcpStream` and printing the data">

```rust,no_run
use std::{
    io::{BufReader, prelude::*},
    net::{TcpListener, TcpStream},
};

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        handle_connection(stream);
    }
}

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let http_request: Vec<_> = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    println!("Request: {http_request:#?}");
}
```

</Listing>

আমরা `std::io::BufReader` এবং `std::io::prelude` কে scope-এ আনলাম, যাতে stream-এ পড়া ও লেখার সুবিধা দেয় এমন trait ও type গুলোতে প্রবেশাধিকার পাই। `main` function-এর `for` loop-এ আগের মতো connection হওয়ার বার্তা প্রিন্ট করার বদলে এখন আমরা নতুন `handle_connection` function টি call করি এবং সেটিতে `stream` পাস করি।

`handle_connection` function-এ আমরা একটি নতুন `BufReader` instance তৈরি করি যেটি `stream`-এর একটি reference কে wrap করে। `BufReader` আমাদের জন্য `std::io::Read` trait-এর method call গুলো পরিচালনা করে buffering যোগ করে।

আমরা `http_request` নামে একটি variable তৈরি করি, যাতে browser আমাদের server-কে যে request গুলো পাঠায় তার line গুলো জড়ো করি। `Vec<_>` type annotation যোগ করে আমরা বোঝাই যে এই line গুলো একটি vector-এ জমা করতে চাই।

`BufReader`, `std::io::BufRead` trait implement করে, যা `lines` method দেয়। `lines` method একটি নতুন line byte দেখলেই ডেটার stream কে split করে `Result<String, std::io::Error>`-এর একটি iterator return করে। প্রতিটি `String` পেতে আমরা প্রতিটি `Result` কে `map` আর `unwrap` করি। যদি ডেটা বৈধ UTF-8 না হয় বা stream থেকে পড়তে সমস্যা হয় তবে `Result` একটি error হতে পারে। আবারও বলছি, একটি production program-কে এই error গুলো আরও সুন্দরভাবে handle করা উচিত, কিন্তু সরলতার জন্য আমরা error case-এ program থামিয়ে দেওয়ার পক্ষে বেছে নিচ্ছি।

Browser একটি HTTP request-এর শেষ নির্দেশ করতে পরপর দুটি newline character পাঠায়, তাই stream থেকে একটি request পেতে আমরা ততটা line নিই যতটা না একটি empty string line পাই। line গুলো vector-এ জমা করার পর, আমরা সেগুলো pretty debug formatting দিয়ে প্রিন্ট করছি যাতে web browser আমাদের server-কে যে নির্দেশ গুলো পাঠাচ্ছে সেগুলো একটু দেখা যায়।

চলো এই code টি চালাই! program টি শুরু করো এবং আবার একটি web browser-এ request পাঠাও। মনে রেখো browser-এ আমরা এখনও একটি error পেজ পাবো, কিন্তু terminal-এ আমাদের program-এর output এরকম দেখাবে:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-02
cargo run
make a request to 127.0.0.1:7878
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.42s
     Running `target/debug/hello`
Request: [
    "GET / HTTP/1.1",
    "Host: 127.0.0.1:7878",
    "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language: en-US,en;q=0.5",
    "Accept-Encoding: gzip, deflate, br",
    "DNT: 1",
    "Connection: keep-alive",
    "Upgrade-Insecure-Requests: 1",
    "Sec-Fetch-Dest: document",
    "Sec-Fetch-Mode: navigate",
    "Sec-Fetch-Site: none",
    "Sec-Fetch-User: ?1",
    "Cache-Control: max-age=0",
]
```

তোমার browser অনুযায়ী output সামান্য ভিন্ন হতে পারে। এখন আমরা request ডেটা প্রিন্ট করছি, তাই request-এর প্রথম line-এ `GET`-এর পরের path-টিতে তাকালে বুঝতে পারি কেন একটি browser request থেকে আমরা একাধিক connection পাই। যদি পুনরাবৃত্ত সব connection-ই _/_ চায়, তাহলে আমরা বুঝবো browser _/_ কে বারবার fetch করার চেষ্টা করছে, কারণ সে আমাদের program থেকে কোনো response পাচ্ছে না।

browser আমাদের program-এর কাছে আসলে কী চায় তা বুঝতে চলো এই request ডেটা একটু খুলে দেখি।

<!-- Old headings. Do not remove or links may break. -->

<a id="a-closer-look-at-an-http-request"></a>
<a id="looking-closer-at-an-http-request"></a>

### একটি HTTP Request-কে আরও কাছ থেকে দেখা

HTTP একটি text-based protocol, এবং এর request এই ফরম্যাটে থাকে:

```text
Method Request-URI HTTP-Version CRLF
headers CRLF
message-body
```

প্রথম line-টি হলো _request line_ যেটিতে client কী চাইছে তার তথ্য থাকে। request line-এর প্রথম অংশটি নির্দেশ করে কোন method ব্যবহার করা হচ্ছে, যেমন `GET` বা `POST`, যা client কীভাবে এই request করছে তা বর্ণনা করে। আমাদের client একটি `GET` request ব্যবহার করেছে, যার মানে সে শুধু তথ্য চাইছে।

request line-এর পরের অংশটি _/_, যা client যে _uniform resource identifier_ _(URI)_ চাইছে তা নির্দেশ করে: URI প্রায়, কিন্তু সম্পূর্ণভাবে নয়, _uniform resource locator_ _(URL)_-এর মতোই। URI আর URL-এর পার্থক্য এই chapter-এর প্রয়োজনের জন্য গুরুত্বপূর্ণ নয়, কিন্তু HTTP spec _URI_ শব্দটি ব্যবহার করে, তাই আমরা মনে মনে এখানে _URI_-এর বদলে _URL_ বসিয়ে নিতে পারি।

শেষ অংশটি হলো client যে HTTP version ব্যবহার করছে, এবং তারপর request line-টি একটি CRLF sequence-এ শেষ হয়। (_CRLF_ মানে _carriage return_ আর _line feed_, যা টাইপরাইটারের যুগের শব্দ!) CRLF sequence-কে `\r\n` হিসেবেও লেখা যায়, যেখানে `\r` হলো carriage return এবং `\n` হলো line feed। _CRLF sequence_ request line-কে request-এর বাকি ডেটা থেকে আলাদা করে। মনে রেখো, CRLF প্রিন্ট করলে আমরা `\r\n` না দেখে একটি নতুন line শুরু হতে দেখি।

এখন পর্যন্ত আমাদের program চালিয়ে যে request line ডেটা পেয়েছি সেটি দেখলে বোঝা যায় `GET` হলো method, _/_ হলো request URI, এবং `HTTP/1.1` হলো version।

request line-এর পরে `Host:` থেকে শুরু হওয়া বাকি line গুলো হলো headers। `GET` request-এর কোনো body থাকে না।

অন্য কোনো browser থেকে request করে দেখো বা ভিন্ন ঠিকানা চাও, যেমন _127.0.0.1:7878/test_, যাতে request ডেটা কীভাবে বদলায় তা দেখতে পারো।

এখন যেহেতু আমরা জানি browser কী চাইছে, চলো কিছু ডেটা ফেরত পাঠাই!

### একটি Response লেখা

আমরা client request-এর প্রতিক্রিয়ায় ডেটা পাঠানোর কাজটি implement করবো। Response গুলোর ফরম্যাট নিচের মতো:

```text
HTTP-Version Status-Code Reason-Phrase CRLF
headers CRLF
message-body
```

প্রথম line-টি হলো _status line_, যেখানে response-এ ব্যবহৃত HTTP version, request-এর ফলাফল সংক্ষেপে জানাতে একটি সাংখ্যিক status code এবং সেই status code-এর একটি text description হিসেবে reason phrase থাকে। CRLF sequence-এর পরে থাকে যেকোনো headers, আরেকটি CRLF sequence, এবং response-এর body।

নিচের উদাহরণটিতে HTTP version 1.1 ব্যবহার করা হয়েছে, status code 200, reason phrase হিসেবে OK, কোনো headers নেই, এবং body-ও নেই:

```text
HTTP/1.1 200 OK\r\n\r\n
```

Status code 200 হলো সাধারণ success response। এই text টি একটি ছোট্ট সফল HTTP response। চলো একটি সফল request-এ আমাদের response হিসেবে এটিকে stream-এ লিখি! `handle_connection` function থেকে request ডেটা প্রিন্ট করা `println!` টি সরিয়ে তার বদলে Listing 21-3-এর code বসাও।

<Listing number="21-3" file-name="src/main.rs" caption="Writing a tiny successful HTTP response to the stream">

```rust,no_run
fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let http_request: Vec<_> = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    let response = "HTTP/1.1 200 OK\r\n\r\n";

    stream.write_all(response.as_bytes()).unwrap();
}
```

</Listing>

প্রথম নতুন line-টি `response` variable define করে যা success বার্তার ডেটা ধরে রাখে। তারপর, আমরা আমাদের `response`-এ `as_bytes` call করি string ডেটাকে byte-এ রূপান্তর করতে। `stream`-এর `write_all` method একটি `&[u8]` নেয় এবং সেই byte গুলো সরাসরি connection বরাবর পাঠায়। যেহেতু `write_all` অপারেশন ব্যর্থ হতে পারে, তাই আগের মতোই যেকোনো error result-এ আমরা `unwrap` ব্যবহার করি। আবারও বলছি, একটি আসল অ্যাপ্লিকেশনে তোমাকে এখানে error handling যোগ করতে হবে।

এই পরিবর্তন গুলো করে আমরা আমাদের code চালাই এবং একটি request পাঠাই। আমরা এখন আর terminal-এ কোনো ডেটা প্রিন্ট করছি না, তাই Cargo-র output ছাড়া আর কোনো output দেখবে না। যখন তুমি একটি web browser-এ _127.0.0.1:7878_ লোড করবে, error-এর বদলে তুমি একটি ফাঁকা পেজ পাবে। তুমি এইমাত্র নিজের হাতে একটি HTTP request গ্রহণ এবং একটি response পাঠানোর code লিখলে!

### আসল HTML ফেরত দেওয়া

একটি ফাঁকা পেজের চেয়ে বেশি কিছু ফেরত দেওয়ার কার্যকারিতা implement করি। তোমার project directory-র root-এ, _src_ directory-তে নয়, নতুন _hello.html_ file টি তৈরি করো। তুমি যেকোনো HTML লিখতে পারো; Listing 21-4-এ একটি সম্ভাব্য উদাহরণ দেওয়া হলো।

<Listing number="21-4" file-name="hello.html" caption="A sample HTML file to return in a response">

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Hello!</title>
  </head>
  <body>
    <h1>Hello!</h1>
    <p>Hi from Rust</p>
  </body>
</html>
```

</Listing>

এটি একটি ছোট HTML5 document, যাতে একটি heading আর কিছু text আছে। কোনো request পেলে এটিকে server থেকে ফেরত দিতে, আমরা Listing 21-5-এ দেখানো অনুযায়ী `handle_connection` কে পরিবর্তন করবো HTML file টি পড়তে, সেটিকে response-এ body হিসেবে যোগ করতে, এবং পাঠাতে।

<Listing number="21-5" file-name="src/main.rs" caption="Sending the contents of *hello.html* as the body of the response">

```rust,no_run
use std::{
    fs,
    io::{BufReader, prelude::*},
    net::{TcpListener, TcpStream},
};
// --snip--

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let http_request: Vec<_> = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    let status_line = "HTTP/1.1 200 OK";
    let contents = fs::read_to_string("hello.html").unwrap();
    let length = contents.len();

    let response =
        format!("{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}");

    stream.write_all(response.as_bytes()).unwrap();
}
```

</Listing>

আমরা `use` statement-এ `fs` যোগ করেছি, যাতে standard library-র filesystem module scope-এ আসে। একটি file-এর contents কে string হিসেবে পড়ার code টি তোমার চেনা চেনা মনে হওয়া উচিত; আমরা এটি Listing 12-4-এ I/O project-তে একটি file-এর contents পড়ার সময় ব্যবহার করেছিলাম।

এরপর, আমরা `format!` ব্যবহার করি success response-এর body হিসেবে file-টির contents যোগ করতে। একটি বৈধ HTTP response নিশ্চিত করতে, আমরা `Content-Length` header যোগ করি, যা আমাদের response body-এর সাইজে সেট করা—এই ক্ষেত্রে `hello.html`-এর সাইজ।

এই code টি `cargo run` দিয়ে চালাও এবং তোমার browser-এ _127.0.0.1:7878_ লোড করো; তোমার HTML render হতে দেখতে পাবে!

বর্তমানে আমরা `http_request`-এর request ডেটা উপেক্ষা করে শর্তহীনভাবে HTML file-এর contents ফেরত পাঠাচ্ছি। এর মানে হলো তুমি browser-এ _127.0.0.1:7878/something-else_ চাইলেও একই HTML response পাবে। এই মুহূর্তে আমাদের server খুবই সীমিত এবং বেশিরভাগ web server যা করে সেটা করে না। আমরা চাই request অনুযায়ী আমাদের response customize করতে এবং শুধুমাত্র _/_-এর জন্য একটি well-formed request হলে HTML file টি ফেরত পাঠাতে।

### Request যাচাই করা এবং নির্বাচিতভাবে সাড়া দেওয়া

এখন আমাদের web server client যাই চাক না কেন, file-টির HTML ফেরত দেবে। চলো এমন কার্যকারিতা যোগ করি যেটি HTML file ফেরত দেওয়ার আগে যাচাই করবে browser আসলে _/_ চাইছে কি না এবং অন্য কিছু চাইলে একটি error ফেরত দেবে। এর জন্য আমাদের Listing 21-6-এ দেখানো অনুযায়ী `handle_connection` কে পরিবর্তন করতে হবে। এই নতুন code টি প্রাপ্ত request-এর content কে একটি _/_ request কেমন হয় তার সাথে তুলনা করে এবং request গুলোকে আলাদাভাবে সামলাতে `if` আর `else` block যোগ করে।

<Listing number="21-6" file-name="src/main.rs" caption="Handling requests to */* differently from other requests">

```rust,no_run
// --snip--

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let request_line = buf_reader.lines().next().unwrap().unwrap();

    if request_line == "GET / HTTP/1.1" {
        let status_line = "HTTP/1.1 200 OK";
        let contents = fs::read_to_string("hello.html").unwrap();
        let length = contents.len();

        let response = format!(
            "{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}"
        );

        stream.write_all(response.as_bytes()).unwrap();
    } else {
        // some other request
    }
}
```

</Listing>

আমরা শুধু HTTP request-এর প্রথম line-টি দেখবো, তাই সম্পূর্ণ request কে একটি vector-এ পড়ার বদলে আমরা iterator থেকে প্রথম item পেতে `next` call করছি। প্রথম `unwrap` টি `Option` সামলায় এবং iterator-এ কোনো item না থাকলে program থামিয়ে দেয়। দ্বিতীয় `unwrap` টি `Result` handle করে এবং Listing 21-2-তে যে `map` যোগ করা হয়েছিল তার `unwrap`-এর মতো একই কাজ করে।

এরপর, আমরা `request_line` check করি দেখতে এটি _/_ path-এ একটি GET request-এর request line-এর সমান কি না। যদি সমান হয়, `if` block আমাদের HTML file-এর contents ফেরত দেয়।

`request_line` যদি _/_ path-এ GET request-এর সমান না হয়, তার মানে আমরা অন্য কোনো request পেয়েছি। আমরা একটু পরেই অন্য সব request-এ সাড়া দিতে `else` block-এ code যোগ করবো।

এখন এই code টি চালাও এবং _127.0.0.1:7878_ request করো; তোমার _hello.html_-এর HTML পাওয়া উচিত। তুমি অন্য কোনো request করলে, যেমন _127.0.0.1:7878/something-else_, তাহলে Listing 21-1 আর Listing 21-2-তে code চালানোর সময় যেমন connection error দেখেছিলে তেমন একটি connection error পাবে।

এখন Listing 21-7-এর code টি `else` block-এ যোগ করি, যেটি status code 404 সহ একটি response ফেরত দেবে এবং সংকেত দেবে যে request করা content খুঁজে পাওয়া যায়নি। আমরা কিছু HTML ও ফেরত দেবো, যা browser-এ render হবে এবং end user-কে response সম্পর্কে জানাবে।

<Listing number="21-7" file-name="src/main.rs" caption="Responding with status code 404 and an error page if anything other than */* was requested">

```rust,no_run
    // --snip--
    } else {
        let status_line = "HTTP/1.1 404 NOT FOUND";
        let contents = fs::read_to_string("404.html").unwrap();
        let length = contents.len();

        let response = format!(
            "{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}"
        );

        stream.write_all(response.as_bytes()).unwrap();
    }
```

</Listing>

এখানে আমাদের response-এ status code 404 এবং reason phrase `NOT FOUND` সহ একটি status line আছে। response-এর body হবে _404.html_ file-এর HTML। তোমাকে _hello.html_-এর পাশে error পেজের জন্য একটি _404.html_ file তৈরি করতে হবে; আবারও বলছি, তুমি যেকোনো HTML ব্যবহার করতে পারো, অথবা Listing 21-8-এর example HTML ব্যবহার করতে পারো।

<Listing number="21-8" file-name="404.html" caption="Sample content for the page to send back with any 404 response">

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Hello!</title>
  </head>
  <body>
    <h1>Oops!</h1>
    <p>Sorry, I don't know what you're asking for.</p>
  </body>
</html>
```

</Listing>

এই পরিবর্তন গুলো করে তোমার server আবার চালাও। _127.0.0.1:7878_ request করলে _hello.html_-এর contents ফেরত পাবে, এবং অন্য কোনো request, যেমন _127.0.0.1:7878/foo_, করলে _404.html_-থেকে error HTML পাবে।

<!-- Old headings. Do not remove or links may break. -->

<a id="a-touch-of-refactoring"></a>

### একটু Refactor করা

এই মুহূর্তে `if` আর `else` block-এ অনেক repetition আছে: দুটোই file পড়ে এবং file-এর contents কে stream-এ লেখে। শুধুমাত্র status line আর filename-ই আলাদা। চলো code টি আরও সংক্ষিপ্ত করি—এই পার্থক্য গুলোকে আলাদা `if` আর `else` line-এ টেনে আনি, যাতে status line আর filename-এর মান variable-এ assign হয়; তারপর সেই variable গুলো আমরা file পড়া ও response লেখার code-এ শর্তহীনভাবে ব্যবহার করতে পারি। বড় `if` আর `else` block-গুলো প্রতিস্থাপন করার পর সৃষ্ট code টি Listing 21-9-এ দেখানো হলো।

<Listing number="21-9" file-name="src/main.rs" caption="Refactoring the `if` and `else` blocks to contain only the code that differs between the two cases">

```rust,no_run
// --snip--

fn handle_connection(mut stream: TcpStream) {
    // --snip--

    let (status_line, filename) = if request_line == "GET / HTTP/1.1" {
        ("HTTP/1.1 200 OK", "hello.html")
    } else {
        ("HTTP/1.1 404 NOT FOUND", "404.html")
    };

    let contents = fs::read_to_string(filename).unwrap();
    let length = contents.len();

    let response =
        format!("{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}");

    stream.write_all(response.as_bytes()).unwrap();
}
```

</Listing>

এখন `if` আর `else` block শুধুমাত্র status line এবং filename-এর জন্য উপযুক্ত মান একটি tuple-এ return করে; তারপর আমরা Chapter 19-এ যেমন আলোচনা করেছি, `let` statement-এ একটি pattern ব্যবহার করে destructuring করে এই দুটি মানকে `status_line` এবং `filename`-এ assign করি।

আগে যে code টি duplicate ছিল সেটি এখন `if` আর `else` block-এর বাইরে এসে `status_line` এবং `filename` variable ব্যবহার করে। এতে দুটি case-এর পার্থক্য বোঝা সহজ হয়েছে এবং file পড়া ও response লেখার কাজ পরিবর্তন করতে চাইলে আমাদের শুধু এক জায়গাতেই code আপডেট করতে হবে। Listing 21-9-এর code-এর আচরণ Listing 21-7-এর মতোই হবে।

দারুণ! এখন আমাদের কাছে প্রায় 40 line Rust code-এ একটি সরল web server আছে যেটি একটি request-এ content-এর একটি পেজ দিয়ে সাড়া দেয় এবং বাকি সব request-এ 404 response দেয়।

বর্তমানে আমাদের server single thread-এ চলে, যার মানে এক সময়ে এটি শুধু একটি request-ই সামলাতে পারে। চলো কিছু slow request simulate করে দেখি কীভাবে সেটা সমস্যা হতে পারে। তারপর, আমরা এটি ঠিক করবো যাতে আমাদের server একসাথে একাধিক request সামলাতে পারে।

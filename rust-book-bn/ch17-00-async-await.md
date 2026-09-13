# Asynchronous Programming-এর Fundamentals: Async, Await, Futures, এবং Streams

আমরা কম্পিউটারকে যে অনেক কাজ করতে বলি, সেগুলো শেষ হতে বেশ সময় লাগতে পারে। এই দীর্ঘস্থায়ী প্রসেসগুলো শেষ হওয়ার অপেক্ষায় থাকা অবস্থায় যদি আমরা অন্য কিছু করতে পারতাম, তাহলে বেশ ভালো হতো। আধুনিক কম্পিউটারগুলো একই সময়ে একাধিক কাজ করার জন্য দুটি টেকনিক দেয়: parallelism এবং concurrency। তবে আমাদের প্রোগ্রামের logic বেশিরভাগ ক্ষেত্রেই রৈখিক (linear) ভাবে লেখা হয়। আমরা চাইলে প্রোগ্রাম যে কাজগুলো করবে সেটা specify করতে পারি এবং এমন কিছু point চিহ্নিত করতে পারি যেখানে একটি function pause করতে পারে এবং প্রোগ্রামের অন্য কোনো অংশ চলতে পারে—আগে থেকেই প্রতিটি কোডের অংশ ঠিক কী ক্রমে ও কীভাবে চলবে তা নির্দিষ্ট করে দেওয়ার প্রয়োজন ছাড়াই। _Asynchronous programming_ হলো এমন একটি abstraction যা আমাদের কোডকে potential pausing point এবং eventual result-এর ভাষায় প্রকাশ করতে দেয় এবং coordination-এর বিস্তারিত নিজ দায়িত্বে সামলে নেয়।

এই chapter-টি Chapter 16-এ thread ব্যবহার করে parallelism ও concurrency-র যে আলোচনা করেছিল, তার ওপর ভিত্তি করে কোড লেখার একটি বিকল্প পদ্ধতি পরিচয় করিয়ে দেয়: Rust-এর futures, streams এবং `async` ও `await` syntax, যেগুলো কাজগুলো কীভাবে asynchronous হতে পারে তা প্রকাশ করতে সাহায্য করে, এবং third-party crate গুলো যা asynchronous runtime ইমপ্লিমেন্ট করে: এমন code যা asynchronous operation-এর execution পরিচালনা ও coordinate করে।

একটি উদাহরণ দেখা যাক। ধরো তুমি পরিবারের এক উৎসবের ভিডিও এডিট করে একটি ভিডিও export করছ, এমন একটি কাজ যা কয়েক মিনিট থেকে কয়েক ঘণ্টা পর্যন্ত সময় নিতে পারে। ভিডিও export করার সময় সে যতটুকু পারবে CPU ও GPU power ব্যবহার করবে। যদি তোমার কাছে মাত্র একটি CPU core থাকত এবং তোমার অপারেটিং সিস্টেম কাজ শেষ না হওয়া পর্যন্ত সেই export-কে pause না করত—অর্থাৎ সে যদি export-টি _synchronously_ চালাত—তাহলে সেই কাজ চলাকালীন তুমি কম্পিউটারে আর কিছুই করতে পারতে না। সেটা বেশ হতাশাজনক অভিজ্ঞতা হতো। সৌভাগ্যক্রমে, তোমার কম্পিউটারের অপারেটিং সিস্টেম অদৃশ্যভাবে বারবার সেই export-কে interrupt করে, যাতে তুমি একই সময়ে অন্য কাজ করতে পারো।

এখন ধরো অন্য কেউ তোমার সাথে একটি ভিডিও share করেছে যেটা তুমি download করছ, যা সময়ও নিতে পারে কিন্তু খুব বেশি CPU time খায় না। এই ক্ষেত্রে CPU-কে অপেক্ষা করতে হয় যতক্ষণ না নেটওয়ার্ক থেকে data এসে পৌঁছায়। যদিও data আসা শুরু করলেই তুমি সেগুলো পড়তে পারবে, পুরো data এসে পৌঁছাতে কিছুটা সময় লাগতে পারে। সব data এসে গেলেও, ভিডিওটি যদি বেশ বড় হয়, তাহলে পুরোটা load করতে অন্তত এক-দুই সেকেন্ড সময় লাগতে পারে। খুব বেশি শোনায় না, কিন্তু আধুনিক processor-এর কাছে এটি অনেক বড় সময়—সে প্রতি সেকেন্ডে কোটি কোটি operation করতে পারে। আবারও, অপারেটিং সিস্টেম অদৃশ্যভাবে তোমার প্রোগ্রামকে interrupt করবে যাতে নেটওয়ার্ক call শেষ হওয়ার অপেক্ষায় CPU অন্য কাজ করতে পারে।

ভিডিও export-টি একটি _CPU-bound_ বা _compute-bound_ operation-এর উদাহরণ। এটি CPU বা GPU-র সম্ভাব্য data processing গতি এবং সেই কাজে সে কতটা গতি ব্যয় করতে পারে, তার ওপর নির্ভরশীল। আর ভিডিও download করা হলো _I/O-bound_ operation-এর উদাহরণ, কারণ এটি কম্পিউটারের _input এবং output_-এর গতির ওপর নির্ভরশীল; নেটওয়ার্ক জুড়ে data যত দ্রুত পাঠানো যায়, তার বেশি গতিতে এগোতে পারবে না।

এই দুটি উদাহরণেই অপারেটিং সিস্টেমের অদৃশ্য interrupt এক ধরনের concurrency দেয়। তবে সেই concurrency ঘটে পুরো প্রোগ্রামের লেভেলে: অপারেটিং সিস্টেম একটি প্রোগ্রামকে interrupt করে অন্য প্রোগ্রামকে কাজ করতে দেয়। অনেক ক্ষেত্রে, অপারেটিং সিস্টেমের চেয়ে আমরা আমাদের প্রোগ্রামকে অনেক বেশি সূক্ষ্মভাবে বুঝি, তাই আমরা এমন concurrency-র সুযোগ খুঁজে পাই যা অপারেটিং সিস্টেম দেখতে পায় না।

যেমন, যদি আমরা file download পরিচালনার একটি tool বানাই, তাহলে আমাদের প্রোগ্রাম এমনভাবে লেখা উচিত যাতে একটি download শুরু করলে UI lock না হয়, এবং user-রা একই সময়ে একাধিক download শুরু করতে পারে। কিন্তু নেটওয়ার্কের সাথে যোগাযোগ করা বহু operating system API _blocking_ হয়; অর্থাৎ, তারা যে data প্রসেস করছে তা পুরোপুরি ready না হওয়া পর্যন্ত প্রোগ্রামের অগ্রগতি block করে রাখে।

> Note: ভাবলে দেখবে, _বেশিরভাগ_ function call-ই এভাবেই কাজ করে। তবে _blocking_ শব্দটি সাধারণত file, নেটওয়ার্ক বা কম্পিউটারের অন্যান্য resource-এর সাথে যোগাযোগ করে এমন function call-এর জন্যই রাখা হয়, কারণ সেই ক্ষেত্রেই একটি পৃথক প্রোগ্রাম operation-টি _non_-blocking হলে উপকৃত হবে।

আমরা প্রতিটি file download করার জন্য আলাদা thread spawn করে main thread block করা থেকে বাঁচতে পারি। কিন্তু এই thread-গুলো যে system resource ব্যবহার করে, তার overhead একসময় সমস্যা হয়ে দাঁড়াবে। বরং এটাই ভালো হতো যদি call-টি শুরুতেই block না করত, এবং আমরা প্রোগ্রামের সম্পন্ন করার জন্য কিছু task সংজ্ঞায়িত করতে পারতাম, আর runtime-কে সেগুলো চালানোর সবচেয়ে ভালো ক্রম ও পদ্ধতি বেছে নিতে দিতে পারতাম।

আর এটাই ঠিক যা Rust-এর _async_ (_asynchronous_-এর সংক্ষিপ্ত রূপ) abstraction আমাদের দেয়। এই chapter-এ তুমি async সম্পর্কে সব শিখবে, নিচের বিষয়গুলো আলোচনা সহ:

- Rust-এর `async` ও `await` syntax কীভাবে ব্যবহার করবে এবং একটি runtime দিয়ে asynchronous function কীভাবে execute করবে
- Async model ব্যবহার করে Chapter 16-এ দেখা কিছু একই চ্যালেঞ্জ কীভাবে সমাধান করবে
- Multithreading এবং async কীভাবে পরিপূরক সমাধান দেয় যা তুমি অনেক ক্ষেত্রে একসাথে ব্যবহার করতে পারো

তবে async বাস্তবে কীভাবে কাজ করে তা দেখার আগে, আমাদের একটু ঘুরে গিয়ে parallelism ও concurrency-র মধ্যে পার্থক্য নিয়ে আলোচনা করতে হবে।

## Parallelism এবং Concurrency

এতকণ আমরা parallelism ও concurrency-কে বেশ বিনিময়যোগ্য হিসেবে ধরেছি। এখন আমাদের এগুলোর মধ্যে আরও সুনির্দিষ্টভাবে পার্থক্য করতে হবে, কারণ কাজ শুরু করলে এই পার্থক্যগুলো প্রকট হয়ে উঠবে।

একটি software project-এ কাজ ভাগ করার বিভিন্ন উপায়ের কথা ভাবো। তুমি একজন সদস্যকে একাধিক task দিতে পারো, প্রত্যেক সদস্যকে একেকটি task দিতে পারো, অথবা এই দুটি পদ্ধতির মিশ্রণ ব্যবহার করতে পারো।

যখন একজন ব্যক্তি একাধিক ভিন্ন task-এ কাজ করে, যার কোনোটিই এখনো শেষ হয়নি, তখন সেটি _concurrency_। Concurrency ইমপ্লিমেন্ট করার একটি উপায় হলো—তোমার কম্পিউটারে দুটি আলাদা project check out করে রাখা, এবং একটিতে কাজ করতে গিয়ে বোর হলে বা আটকে গেলে অন্যটিতে চলে যাওয়া। তুমি একজন মানুষ, তাই একই সময়ে দুটি task-এ অগ্রগতি করতে পারবে না, কিন্তু তুমি কাজ আলাদা করে multitask করতে পারো—তাদের মধ্যে switch করে একটি সময়ে একটি করে এগিয়ে যেতে পারো (Figure 17-1 দেখো)।

<figure>

<img src="img/trpl17-01.svg" class="center" alt="A diagram with stacked boxes labeled Task A and Task B, with diamonds in them representing subtasks. Arrows point from A1 to B1, B1 to A2, A2 to B2, B2 to A3, A3 to A4, and A4 to B3. The arrows between the subtasks cross the boxes between Task A and Task B." />

<figcaption>Figure 17-1: A concurrent workflow, switching between Task A and Task B</figcaption>

</figure>

যখন দল একগুচ্ছ task এমনভাবে ভাগ করে যে প্রত্যেক সদস্য একটি করে task নেয় ও একা কাজ করে, তখন সেটি _parallelism_। দলের প্রত্যেকে একই সময়ে অগ্রগতি করতে পারে (Figure 17-2 দেখো)।

<figure>

<img src="img/trpl17-02.svg" class="center" alt="A diagram with stacked boxes labeled Task A and Task B, with diamonds in them representing subtasks. Arrows point from A1 to A2, A2 to A3, A3 to A4, B1 to B2, and B2 to B3. No arrows cross between the boxes for Task A and Task B." />

<figcaption>Figure 17-2: A parallel workflow, where work happens on Task A and Task B independently</figcaption>

</figure>

এই দুটি workflow-এই তুমি হয়তো বিভিন্ন task-এর মধ্যে coordinate করতে বাধ্য হবে। হয়তো তুমি ভেবেছিলে একজনের task বাকি সবার কাজ থেকে সম্পূর্ণ স্বাধীন, কিন্তু আসলে দলের আরেকজনকে আগে তার task শেষ করতে হবে। কিছু কাজ parallel-ভাবে করা যেতে পারে, কিন্তু কিছু কাজ আসলে _serial_: সেগুলো শুধু একটার পর একটা, সিরিজে ঘটতে পারে, Figure 17-3-এর মতো।

<figure>

<img src="img/trpl17-03.svg" class="center" alt="A diagram with stacked boxes labeled Task A and Task B, with diamonds in them representing subtasks. In Task A, arrows point from A1 to A2, from A2 to a pair of thick vertical lines like a “pause” symbol, and from that symbol to A3. In task B, arrows point from B1 to B2, from B2 to B3, from B3 to A3, and from B3 to B4." />

<figcaption>Figure 17-3: A partially parallel workflow, where work happens on Task A and Task B independently until Task A3 is blocked on the results of Task B3.</figcaption>

</figure>

একইভাবে, তুমি হয়তো বুঝতে পারবে যে তোমার নিজের একটি task তোমার আরেকটি task-এর ওপর নির্ভরশীল। এখন তোমার concurrent কাজটাও serial হয়ে গেল।

Parallelism এবং concurrency পরস্পরের সাথে intersect করতেও পারে। যদি জানতে পারো একজন সহকর্মী তোমার একটি task শেষ না হওয়া পর্যন্ত আটকে আছে, তুমি সম্ভবত তাকে “unblock” করতে সেই task-এ সমস্ত মনোযোগ দেবে। তুমি আর তোমার সহকর্মী এখন আর parallel-ভাবে কাজ করতে পারবে না, এবং নিজের কাজেও আর concurrently কাজ করতে পারবে না।

একই মৌলিক গতিশীলতা software ও hardware-এর ক্ষেত্রেও প্রযোজ্য। একটি single CPU core সম্পন্ন মেশিনে, CPU একই সময়ে শুধু একটি operation করতে পারে, কিন্তু এখনও concurrently কাজ করতে পারে। Thread, process, এবং async-এর মতো tool ব্যবহার করে কম্পিউটার একটি কাজ pause করে অন্যগুলোতে চলে যেতে পারে, আর পরে আবার প্রথম কাজে ফিরে আসতে পারে। একাধিক CPU core সম্পন্ন মেশিনে সে parallel-ভাবেও কাজ করতে পারে। একটি core একটি task করতে পারে, আরেকটি core একই সময়ে সম্পূর্ণ আলাদা একটি task করতে পারে, আর সেই operation-গুলো আসলেই একই সময়ে ঘটে।

Rust-এ async code সাধারণত concurrently চলে। Hardware, অপারেটিং সিস্টেম ও ব্যবহৃত async runtime-এর ওপর নির্ভর করে (async runtime নিয়ে একটু পরেই বলছি), সেই concurrency পর্দার আড়ালে parallelism-ও ব্যবহার করতে পারে।

এখন, চলো Rust-এ async programming আসলে কীভাবে কাজ করে সেটাতে নামি।

## Appendix G - How Rust is Made এবং “Nightly Rust”

এই appendix-এ আলোচনা করা হবে Rust কীভাবে তৈরি হয় এবং একজন Rust developer হিসেবে তা তোমাকে কীভাবে প্রভাবিত করে।

### Stability Without Stagnation

একটি language হিসেবে Rust তোমার code-এর stability নিয়ে _অনেক_ গুরুত্ব দেয়। আমরা চাই Rust হবে এমন একটি rock-solid foundation যার উপর তুমি নির্মাণ করতে পারো, আর যদি সবকিছু ক্রমাগত বদলাতে থাকে তবে তা অসম্ভব হয়ে যাবে। একই সময়ে, যদি আমরা নতুন feature নিয়ে experiment না করতে পারি, তবে সেগুলো release হওয়ার পরে—যখন আর কিছু পরিবর্তন করা যায় না—আমরা গুরুত্বপূর্ণ ত্রুটি আবিষ্কার নাও করতে পারি।

এই সমস্যার সমাধান আমরা যাকে “stability without stagnation” বলি, এবং আমাদের পরিচালন নীতি হলো: তোমার কখনোই stable Rust-এর একটি নতুন version-এ upgrade করতে ভয় পাওয়া উচিত নয়। প্রতিটি upgrade painless হবে, কিন্তু একই সাথে তোমাকে নতুন feature, কম bug এবং দ্রুত compile time এনে দেবে।

### Choo, Choo! Release Channels এবং Riding the Trains

Rust development একটি _train schedule_-এ পরিচালিত হয়। অর্থাৎ সমস্ত development Rust repository-র main branch-এ হয়। Release গুলো একটি software release train model অনুসরণ করে, যা Cisco IOS এবং অন্যান্য software project ব্যবহার করেছে। Rust-এর তিনটি _release channel_ রয়েছে:

- Nightly
- Beta
- Stable

বেশিরভাগ Rust developer মূলত stable channel ব্যবহার করেন, কিন্তু যারা নতুন experimental feature চেষ্টা করতে চান তারা nightly বা beta ব্যবহার করতে পারেন।

এখানে একটি উদাহরণ দেওয়া হলো কীভাবে development ও release process কাজ করে: ধরে নাও Rust team Rust 1.5 release করার কাজ করছে। সেই release টি 2015 সালের ডিসেম্বরে হয়েছিল, কিন্তু এটি আমাদের বাস্তবসম্মত version number দেবে। একটি নতুন feature Rust-এ যোগ করা হলো: একটি নতুন commit main branch-এ এল। প্রতি রাতে Rust-এর একটি নতুন nightly version তৈরি হয়। প্রতিদিনই একটি release day, এবং এই release গুলো আমাদের release infrastructure স্বয়ংক্রিয়ভাবে তৈরি করে। সুতরাং সময়ের সাথে সাথে আমাদের release গুলো একরাতে একবার করে এভাবে দেখায়:

```text
nightly: * - - * - - *
```

প্রতি ছয় সপ্তাহ অন্তর একটি নতুন release প্রস্তুত করার সময় হয়! Rust repository-র `beta` branch nightly দ্বারা ব্যবহৃত main branch থেকে আলাদা হয়। এখন দুটি release রয়েছে:

```text
nightly: * - - * - - *
                     |
beta:                *
```

বেশিরভাগ Rust user beta release সক্রিয়ভাবে ব্যবহার করেন না, কিন্তু তাদের CI system-এ beta তে পরীক্ষা করেন যাতে Rust সম্ভাব্য regression খুঁজে পায়। এই সময়েও প্রতি রাতে একটি nightly release হয়:

```text
nightly: * - - * - - * - - * - - *
                     |
beta:                *
```

ধরো একটি regression পাওয়া গেল। সেই regression একটি stable release-এ চলে যাওয়ার আগেই আমরা beta release পরীক্ষা করার সুযোগ পেয়েছি—এটা ভালোই! fix-টি main branch-এ apply করা হয়, যাতে nightly fix হয়ে যায়, এবং তারপর fix-টি `beta` branch-এ backport করা হয়, এবং beta-র একটি নতুন release তৈরি করা হয়:

```text
nightly: * - - * - - * - - * - - * - - *
                     |
beta:                * - - - - - - - - *
```

প্রথম beta তৈরি হওয়ার ছয় সপ্তাহ পর একটি stable release-এর সময় এসেছে! `stable` branch `beta` branch থেকে তৈরি হয়:

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |
beta:                * - - - - - - - - *
                                       |
stable:                                *
```

বাহ! Rust 1.5 শেষ! কিন্তু আমরা একটি জিনিস ভুলে গেছি: ছয় সপ্তাহ পার হয়ে যাওয়ায় আমাদের Rust-র _পরবর্তী_ version 1.6-র একটি নতুন beta-ও প্রয়োজন। তাই `stable` `beta` থেকে আলাদা হওয়ার পর, `beta`-র পরবর্তী version আবার `nightly` থেকে আলাদা হয়:

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |                         |
beta:                * - - - - - - - - *       *
                                       |
stable:                                *
```

একে “train model” বলা হয় কারণ প্রতি ছয় সপ্তাহ অন্তর একটি release “station থেকে ছেড়ে যায়”, কিন্তু এটি stable release হিসেবে পৌঁছানোর আগে beta channel দিয়ে একটি যাত্রা করতে হয়।

Rust প্রতি ছয় সপ্তাহ অন্তর, clockwork-এর মতো নিয়মিত release করে। তুমি যদি একটি Rust release-এর তারিখ জানো, তাহলে পরবর্তী release-এর তারিখও জানো: ছয় সপ্তাহ পর। প্রতি ছয় সপ্তাহ অন্তর release schedule থাকার একটি সুন্দর দিক হলো পরবর্তী train শীঘ্রই আসছে। কোনো feature যদি কোনো নির্দিষ্ট release-এ যেতে না পারে, তবে চিন্তার কিছু নেই: আরেকটি অল্প সময়ের মধ্যেই আসছে! এটি release deadline-এর কাছাকাছি সময়ে সম্ভবত অসম্পূর্ণ feature ঢুকিয়ে দেওয়ার চাপ কমাতে সাহায্য করে।

এই process-র জন্য ধন্যবাদ, তুমি সর্বদা Rust-র পরবর্তী build দেখতে পারো এবং নিজে যাচাই করতে পারো যে upgrade করা সহজ: যদি কোনো beta release প্রত্যাশিতভাবে না চলে, তুমি team-কে জানাতে পারো এবং পরবর্তী stable release হওয়ার আগেই fix করে নিতে পারো! Beta release-এ কিছু ভেঙে যাওয়া তুলনামূলক বিরল, কিন্তু `rustc`-ও একটি software, আর bug-ও আছে।

### Maintenance time

Rust project সর্বশেষ stable version-টিকে support করে। নতুন stable version release হলে পুরোনো version তার end of life (EOL)-এ পৌঁছায়। এর মানে প্রতিটি version ছয় সপ্তাহ support করা হয়।

### Unstable Features

এই release model-এর সাথে আরেকটি বিষয় যুক্ত: unstable feature। Rust “feature flag” নামে একটি কৌশল ব্যবহার করে নির্ধারণ করতে যে কোনো নির্দিষ্ট release-এ কোন কোন feature enable থাকবে। কোনো নতুন feature যদি active development-এর অধীনে থাকে, তবে তা main branch-এ আসে, এবং তাই nightly-তেও আসে, কিন্তু একটি _feature flag_-এর পেছনে। তুমি একজন user হিসেবে যদি সেই work-in-progress feature চেষ্টা করতে চাও, তবে পারো, কিন্তু তোমাকে অবশ্যই Rust-র একটি nightly release ব্যবহার করতে হবে এবং তোমার source code-এ উপযুক্ত flag দিয়ে opt-in annotate করতে হবে।

তুমি যদি Rust-র beta বা stable release ব্যবহার করো, তবে কোনো feature flag ব্যবহার করতে পারবে না। এটিই সেই চাবি যা আমাদের নতুন feature-গুলোকে চিরকাল stable ঘোষণা করার আগে ব্যবহারিক প্রয়োগ করতে সাহায্য করে। যারা bleeding edge-এ opt-in করতে চান তারা তা করতে পারেন, আর যারা rock-solid experience চান তারা stable-এ থাকতে পারেন এবং জানতে পারেন যে তাদের code ভাঙবে না। Stability without stagnation।

এই বইতে শুধুমাত্র stable feature সম্পর্কে তথ্য রয়েছে, কারণ in-progress feature এখনও বদলাচ্ছে, এবং বইটি লেখার সময় থেকে সেগুলো stable build-এ enable হওয়ার মধ্যে অবশ্যই পরিবর্তন হবে। Nightly-only feature-এর documentation তুমি অনলাইনে পেয়ে যাবে।

### Rustup এবং Rust Nightly-র ভূমিকা

Rustup তোমাকে global বা per-project ভিত্তিতে Rust-র বিভিন্ন release channel-এর মধ্যে পরিবর্তন করতে সহজ করে। ডিফল্টভাবে তোমার কাছে stable Rust install থাকবে। Nightly install করতে, উদাহরণস্বরূপ:

```console
$ rustup toolchain install nightly
```

তুমি তোমার install করা সব _toolchain_ (Rust-র release ও associated component) `rustup` দিয়েও দেখতে পারো। তোমার একজন লেখকের Windows computer-এ এর একটি উদাহরণ:

```powershell
> rustup toolchain list
stable-x86_64-pc-windows-msvc (default)
beta-x86_64-pc-windows-msvc
nightly-x86_64-pc-windows-msvc
```

দেখতেই পাচ্ছ, stable toolchain-টিই ডিফল্ট। বেশিরভাগ Rust user বেশিরভাগ সময় stable ব্যবহার করেন। তুমিও বেশিরভাগ সময় stable ব্যবহার করতে চাইতে পারো, কিন্তু কোনো নির্দিষ্ট project-এ nightly ব্যবহার করতে পারো, কারণ তুমি একটি cutting-edge feature-এ আগ্রহী। সেটি করতে হলে, সেই project-এর directory-তে `rustup override` ব্যবহার করে nightly toolchain-কে `rustup`-এর জন্য ডিফল্ট হিসেবে set করতে পারো যখন তুমি সেই directory-তে থাকবে:

```console
$ cd ~/projects/needs-nightly
$ rustup override set nightly
```

এখন তুমি যখনই _~/projects/needs-nightly_-র ভেতরে `rustc` বা `cargo` call করবে, `rustup` নিশ্চিত করবে যে তুমি nightly Rust ব্যবহার করছ—stable Rust-র ডিফল্ট নয়। তোমার যখন অনেক Rust project থাকে তখন এটি খুবই কাজে লাগে!

### RFC Process এবং Teams

তাহলে তুমি এই নতুন feature-গুলো সম্পর্কে কীভাবে জানবে? Rust-র development model একটি _Request For Comments (RFC) process_ অনুসরণ করে। তুমি যদি Rust-এ কোনো improvement চাও, তবে তুমি একটি proposal লিখতে পারো, যাকে RFC বলে।

যে কেউ Rust উন্নত করতে RFC লিখতে পারেন, এবং এই proposal-গুলো Rust team দ্বারা review ও আলোচনা করা হয়, যা অনেকগুলি topic subteam নিয়ে গঠিত। Team-গুলোর সম্পূর্ণ তালিকা [Rust-র website-এ](https://www.rust-lang.org/governance) পাওয়া যায়, যেখানে project-এর প্রতিটি ক্ষেত্রের জন্য team রয়েছে: language design, compiler implementation, infrastructure, documentation ইত্যাদি। উপযুক্ত team proposal এবং comment-গুলো পড়ে, নিজেদের কিছু comment লেখে, এবং সবশেষে feature-টি accept বা reject করার ব্যাপারে consensus-এ পৌঁছায়।

feature-টি accept করা হলে, Rust repository-তে একটি issue খোলা হয়, এবং কেউ একজন সেটি implement করতে পারে। যিনি implement করেন তিনি সম্ভবত সেই person-ই নন যিনি প্রথমে feature-টি propose করেছিলেন! implementation প্রস্তুত হলে তা main branch-এ একটি feature gate-এর পেছনে আসে, যেমনটি আমরা [“Unstable Features”](#unstable-features)<!-- ignore --> section-এ আলোচনা করেছি।

কিছুক্ষণ পর, nightly release ব্যবহার করেন এমন Rust developer-রা যখন নতুন feature-টি চেষ্টা করার সুযোগ পান, তখন team member-রা feature-টি, এটি nightly-তে কেমন কাজ করেছে তা নিয়ে আলোচনা করেন এবং সিদ্ধান্ত নেন এটি stable Rust-এ যাবে কি না। সিদ্ধান্ত যদি এগিয়ে যাওয়ার হয়, তবে feature gate সরিয়ে দেওয়া হয়, এবং feature-টি এখন stable বলে গণ্য হয়! এটি train-এ চড়ে Rust-র একটি নতুন stable release-এ যায়।

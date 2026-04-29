# **گزارش جامع و چک‌لیست تحلیلی آزمون‌های CKA و CKAD (کوبرنتیز نسخه ۱.۳۵ – سال ۲۰۲۶)**

## **مقدمه و چشم‌انداز اکوسیستم بومی ابری در سال ۲۰۲۶**

در اکوسیستم بومی ابری (Cloud Native)، گواهینامه‌های ارائه‌شده توسط بنیاد پردازش ابری بومی (CNCF) با همکاری بنیاد لینوکس (Linux Foundation) به‌عنوان استاندارد طلایی و مراجع بی‌بدیل برای ارزیابی مهارت‌های عملی مهندسان در سطح جهانی شناخته می‌شوند.1 با انتشار نسخه ۱.۳۵ کوبرنتیز در سه‌ماهه پایانی سال ۲۰۲۵ و تثبیت آن به‌عنوان نسخه مرجع برای آزمون‌های سال ۲۰۲۶، تغییرات شگرفی در نحوه مدیریت منابع محاسباتی، امنیت مبتنی بر معماری بدون اعتماد (Zero Trust)، سیاست‌گذاری‌های شبکه و یکپارچگی با بارهای کاری هوش مصنوعی (AI/ML) ایجاد شده است.4 این تغییرات بنیادین مستقیماً در برنامه‌درسی (Curriculum) و ساختار سوالات آزمون‌های «مدیر تاییدشده کوبرنتیز» (CKA) و «توسعه‌دهنده تاییدشده برنامه‌های کوبرنتیز» (CKAD) منعکس شده‌اند.7

هر دو آزمون به‌صورت کاملاً عملی (Performance-based) و در محیط خط فرمان سیستم‌عامل اوبونتو لینوکس از طریق مرورگر امنیتی PSI Bridge برگزار می‌شوند.8 در این ارزیابی‌ها هیچ‌گونه سوال چندگزینه‌ای یا تئوریک وجود ندارد؛ در عوض، داوطلبان باید در مدت زمان دقیقاً دو ساعت، مجموعه‌ای از چالش‌ها و مشکلات پیچیده را در خوشه‌های واقعی حل و فصل کنند.8 کسب نمره قبولی ۶۶ درصد در این آزمون‌ها مستلزم درک عمیق از معماری، سرعت بالا در اجرای دستورات امری (Imperative Commands) و تسلط بر مفاهیم جدید نسخه ۱.۳۵ نظیر «تغییر اندازه درجای پادها» (In-place Pod Resize)، «رابط برنامه‌نویسی دروازه» (Gateway API) و «کنترل‌کننده‌های پذیرش تاییدکننده مبتنی بر زبان عبارات مشترک» (CEL ValidatingAdmissionPolicy) است.9

این گزارش تحقیقاتی، با پرهیز کامل از کلی‌گویی و با رویکردی میکروسکوپی، به کالبدشکافی دقیق سرفصل‌ها، تقاطع‌های مهارتی و افتراق‌های بنیادین بین دو آزمون CKA و CKAD در سال ۲۰۲۶ می‌پردازد. هدف، ارائه یک چک‌لیست کاربردی و تحلیلی برای داوطلبانی است که قصد دارند هر دو گواهینامه را با موفقیت دریافت کنند و نیازمند درک دقیقی از حوزه‌های تمرکز هر آزمون هستند.

## **تحلیل ساختار کلان و هویت‌شناسی دو آزمون**

آزمون‌های CKA و CKAD اگرچه هر دو بر بستر فناوری واحدِ کوبرنتیز طراحی شده‌اند، اما دو پرسونا (Persona) و نقش سازمانی کاملاً متمایز را هدف قرار می‌دهند.7 آزمون CKA با تمرکز بر مدیریت زیرساخت خوشه، مهندسان سیستم و مهندسان قابلیت اطمینان سایت (SRE) را ارزیابی می‌کند که وظیفه نصب، نگهداری، ارتقاء، تامین امنیت کلان و عیب‌یابی اجزای هسته (مانند kubelet، etcd و kube-apiserver) را بر عهده دارند.7 در نقطه مقابل، آزمون CKAD برای مهندسان نرم‌افزار و توسعه‌دهندگان برنامه‌های بومی ابری طراحی شده است. این آزمون با این پیش‌فرض آغاز می‌شود که کلاستر از پیش پیکربندی شده است و اکنون تمرکز بر استقرار کدهای برنامه‌نویسی‌شده، مدیریت الگوهای استقرار (Deployment Patterns)، پیکربندی متغیرهای محیطی، تنظیم منابع مصرفی و مانیتورینگ وضعیت سلامت برنامه‌ها در داخل این کلاستر است.7

تحلیل‌ها نشان می‌دهد که استراتژی‌های آماده‌سازی برای این دو ارزیابی باید کاملاً متفاوت باشند، زیرا رویکرد ذهنی (Mindset) مورد نیاز در مواجهه با خطاها با یکدیگر تفاوت ماهوی دارد.7

| شاخصه مقایسه‌ای | آزمون CKA (مدیر تاییدشده کوبرنتیز) | آزمون CKAD (توسعه‌دهنده تاییدشده برنامه‌ها) |
| ----: | ----: | ----: |
| **هویت حرفه‌ای مخاطب** | مدیران سیستم، مهندسان زیرساخت، مهندسان SRE | توسعه‌دهندگان نرم‌افزار، مهندسان DevOps لایه کاربرد |
| **محور تمرکز مهارت‌ها** | مدیریت کلاستر، معماری سیستم، چرخه حیات نودها و اجزای کنترل‌پلین | استقرار مقیاس‌پذیر برنامه‌ها، الگوهای طراحی کانتینری، عیب‌یابی لایه اپلیکیشن |
| **تعداد وظایف (Tasks)** | بین ۱۷ الی ۲۵ سناریو عملی در محیط خط فرمان | بین ۱۵ الی ۲۰ سناریو عملی در محیط خط فرمان |
| **مدت زمان امتحان** | ۱۲۰ دقیقه (۲ ساعت) | ۱۲۰ دقیقه (۲ ساعت) |
| **نمره حد نصاب قبولی** | ۶۶٪ | ۶۶٪ |
| **نسخه کوبرنتیز (سال ۲۰۲۶)** | v1.35 | v1.35 |
| **مبلغ ثبت‌نام (حدودی)** | ۴۴۵ دلار آمریکا (شامل یک بار بازآزمایی رایگان در صورت شکست) | ۴۴۵ دلار آمریکا (شامل یک بار بازآزمایی رایگان در صورت شکست) |
| **مدت زمان اعتبار گواهینامه** | ۲ سال | ۲ سال |
| **میزان سختی نسبی** | پیشرفته (چالش‌های سنگین عیب‌یابی و مدیریت زمان تحت فشار) | متوسط رو به بالا (چالش‌های مفهومی در طراحی مانیفست‌ها و الگوهای ترافیکی) |

## **کالبدشکافی تقاطع مهارت‌ها: چک‌لیست مباحث مشترک (همپوشانی ۴۰ درصدی)**

بررسی‌های متقاطع سیبلس‌های (Syllabuses) منتشر شده توسط بنیاد لینوکس و CNCF نشان می‌دهد که در نسخه ۱.۳۵، حدود ۴۰ درصد از مفاهیم، دستورات و سناریوها بین آزمون‌های CKA و CKAD مشترک هستند.9 این همپوشانی کاملاً منطقی است؛ یک مدیر سیستم باید بداند بارهای کاری چگونه عمل می‌کنند تا بتواند زیرساخت تخصیص‌یافته به آن‌ها را مدیریت کند، و یک توسعه‌دهنده نیز باید حداقل‌های شبکه و ذخیره‌سازی را درک کند تا برنامه خود را به درستی مستقر سازد. تسلط بر این حوزه‌های مشترک، پایه‌ای مستحکم برای موفقیت در هر دو آزمون فراهم می‌آورد.

### **۱. مدیریت بنیادین بارهای کاری (Workloads Management)**

در هر دو آزمون، تسلط بر ایجاد، مدیریت و عیب‌یابی آبجکت‌های پایه‌ای کوبرنتیز نظیر پادها (Pods) و استقرارها (Deployments) قطعی است.9 داوطلبان باید بتوانند با استفاده از دستورات امری (Imperative Commands) بدون نیاز به نوشتن دستی فایل‌های YAML از ابتدا، منابع را خلق کنند. دستوراتی نظیر kubectl run برای ایجاد پادها و kubectl create deployment برای ایجاد استقرارها، ستون فقرات مدیریت زمان در آزمون هستند.

ریزموضوعات مشترک در این بخش شامل الگوهای چندکانتینری (Multi-container Pods) است. درک الگوهای سایدکار (Sidecar) و کانتینرهای مقداردهی اولیه (Init Containers) در هر دو آزمون ارزیابی می‌شود.9 با ارتقاء کوبرنتیز به نسخه ۱.۳۵، کانتینرهای سایدکار بومی (Native Sidecar Containers) به وضعیت پایدار (GA) رسیده‌اند. این بدان معناست که داوطلبان باید بدانند چگونه با افزودن فیلد restartPolicy: Always به یک کانتینر در بخش initContainers، آن را به یک پردازش پس‌زمینه تبدیل کنند که در تمام طول عمر پاد به فعالیت خود ادامه می‌دهد، بدون آنکه مانع اجرای کانتینر اصلی شود.9

### **۲. پیکربندی داده‌ها و مدیریت اسرار (ConfigMaps & Secrets)**

مدیریت متغیرهای محیطی و داده‌های حساس از وظایف روزمره در هر دو نقش است.9 داوطلبان باید بتوانند نقشه‌های پیکربندی (ConfigMaps) و رازها (Secrets) را از طریق خط فرمان (با پرچم‌های \--from-literal یا \--from-file) ایجاد کنند.14 سناریوهای مشترک شامل تزریق این منابع به کانتینرها به عنوان متغیرهای محیطی با استفاده از کلیدهای valueFrom و envFrom، و یا نصب آن‌ها در سیستم‌فایل کانتینر به عنوان حجم‌های داده (Volumes) است.14 علاوه بر این، درک ساختار Base64 برای رمزگشایی و رمزنگاری داده‌های درون Secrets در هر دو آزمون مورد نیاز است.17

### **۳. شبکه‌سازی پایه و سرویس‌ها (Basic Networking)**

درک نحوه برقراری ارتباط شبکه‌ای بین پادها و خارج از کلاستر یک ضرورت مشترک است.9 داوطلبان باید تفاوت بین انواع سرویس‌ها شامل ClusterIP (ارتباطات داخلی کلاستر)، NodePort (باز کردن یک پورت روی تمامی نودها در بازه ۳۰۰۰۰-۳۲۷۶۷ برای دسترسی مستقیم) و LoadBalancer را به وضوح درک کنند.9 مهارت تولید سریع سرویس‌ها با استفاده از دستور kubectl expose و همچنین درک عمیق از مکانیزم انتخاب‌گرها (Selectors) و برچسب‌ها (Labels) برای هدایت صحیح ترافیک به پادهای مقصد در سناریوهای هر دو آزمون حضور دارد.9

### **۴. ذخیره‌سازی داده‌های پایدار (Persistent Storage)**

مفاهیم پایه ذخیره‌سازی در سطح ایجاد و مصرف، نقطه اشتراک دیگری است. هر دو آزمون شامل چالش‌هایی برای مدیریت حجم‌های پایدار (PersistentVolumes \- PV) و درخواست‌های حجم پایدار (PersistentVolumeClaims \- PVC) هستند.9 داوطلب باید قادر باشد یک PVC با حجم و نوع دسترسی مشخص ایجاد کند، وضعیت اتصال (Bound) آن به یک PV موجود را تایید کند و سپس این درخواست را در قالب یک volumeMount در داخل کانتینر پاد مورد استفاده قرار دهد تا پایداری داده‌ها پس از چرخه راه‌اندازی مجدد (Restart) تضمین شود.7

| چک‌لیست مهارت‌های کاملاً مشترک بین CKA و CKAD | کاربرد و دستورات کلیدی ارزیابی‌شونده |
| ----: | ----: |
| **ایجاد سریع پادها و دیپلوی‌منت‌ها** | استفاده از kubectl run nginx \--image=nginx و kubectl create deployment |
| **الگوهای چندکانتینری و سایدکار بومی** | پیکربندی initContainers با restartPolicy: Always (ویژگی نسخه ۱.۳۵) |
| **تزریق تنظیمات و داده‌های حساس** | ساخت ConfigMap و Secret و استفاده از envFrom یا اتصال به‌عنوان Volume |
| **سرویس‌ها و مسیریابی ترافیک داخلی** | شناخت ClusterIP و NodePort و ساخت سریع با kubectl expose |
| **اتصال دیسک‌های پایدار (PV/PVC)** | چرخه حیات اتصال PVC به PV و پیکربندی volumeMounts در پاد |
| **عیب‌یابی پایه کانتینرها** | استفاده از kubectl logs \-c \<container\_name\> و kubectl exec \-it |

## **کالبدشکافی آزمون CKAD: چک‌لیست ریزموضوعات اختصاصی (ویژه توسعه‌دهندگان)**

آزمون CKAD برخلاف CKA، داوطلب را درگیر خطاهای سیستمی پایین‌رده یا مدیریت نودها نمی‌کند؛ بلکه بر نحوه مهندسی نرم‌افزار برای اجرا در محیط کانتینری متمرکز است.7 سرفصل‌های اختصاصی این آزمون در پنج دامنه (Domain) تدوین شده‌اند که جزئیات آن‌ها در نسخه ۱.۳۵ به شرح زیر است.

### **دامنه ۱: محیط برنامه‌ها، پیکربندی و امنیت (۲۵٪ وزن آزمون)**

این دامنه که بیشترین وزن را به خود اختصاص داده است، بر پیکربندی امنیتی و مدیریت منابع از دیدگاه توسعه‌دهنده تمرکز دارد.8

* **مدیریت زمینه‌های امنیتی (SecurityContext):** داوطلبان باید بتوانند سطح دسترسی فرآیندهای درون کانتینر را به شدت محدود کنند. این شامل پیکربندی پارامترهایی نظیر runAsUser، runAsGroup و runAsNonRoot برای جلوگیری از اجرای کانتینر با دسترسی ریشه است.14 همچنین افزودن یا حذف قابلیت‌های هسته لینوکس از طریق بلوک capabilities (مانند افزودن NET\_ADMIN) و تنظیم سیستم‌فایل به‌صورت فقط‌خواندنی (readOnlyRootFilesystem) از سناریوهای رایج است.17  
* **حساب‌های خدماتی (ServiceAccounts):** توسعه‌دهندگان باید نحوه ایجاد حساب‌های خدماتی متمایز و اتصال آن‌ها به پادها را بدانند. سناریوی مهم در این بخش، جلوگیری از نصب خودکار توکن‌های حساب پیش‌فرض از طریق تنظیم automountServiceAccountToken: false و استفاده از تزریق هدفمند توکن‌ها است.13  
* **محدودیت منابع و سهمیه‌ها (Requests, Limits, Quotas):** درک تفاوت بین درخواست‌های پایه منابع (Requests) و سقف مجاز مصرف (Limits) حیاتی است. توسعه‌دهنده باید بتواند این مقادیر را تنظیم کرده و با مفاهیمی چون LimitRange (برای اعمال مقادیر پیش‌فرض به کانتینرها) و ResourceQuota (برای کنترل سقف مصرف کل فضای نام) کار کند و در صورت بروز خطای نقض سهمیه، آن را عیب‌یابی نماید.14  
* **منابع سفارشی (CRDs):** کشف و استفاده از تعاریف منابع سفارشی با استفاده از دستور kubectl get crd و درک نحوه ایجاد منابع سفارشی مبتنی بر اپراتورها (Operators) در سطح پایه سنجیده می‌شود.17

### **دامنه ۲: طراحی و ساخت برنامه‌ها (۲۰٪ وزن آزمون)**

این دامنه مهارت‌های داوطلب در آماده‌سازی کدهای منبع برای اجرا در محیط کوبرنتیز را ارزیابی می‌کند.8

* **مدیریت تصاویر کانتینری (Container Images):** تسلط بر ساخت تصاویر از طریق نوشتن فایل‌های Dockerfile، درک تکنیک‌های ساخت چندمرحله‌ای (Multi-stage builds) برای کاهش حجم نهایی تصویر، و تگ‌گذاری (Tagging) تصاویر برای ارسال به مخازن محلی از وظایف قطعی است.14  
* **وظایف دسته‌ای و زمان‌بندی‌شده (Jobs & CronJobs):** فراتر از استقرارهای دائمی، توسعه‌دهندگان باید بتوانند وظایفی ایجاد کنند که برای اجرای یک پردازش موقت طراحی شده‌اند. سناریوها شامل پیکربندی کرون‌جاب‌ها برای اجرا در بازه‌های زمانی خاص (با فرمت‌های استاندارد لینوکس مانند \*/30 \* \* \* \*)، کنترل موازی‌سازی پردازش‌ها (parallelism)، تعیین مهلت اجرای یک وظیفه ناموفق (activeDeadlineSeconds) و تنظیم محدودیت سابقه نگهداری وظایف موفق و ناموفق است.10  
* **حجم‌های داده موقت (Ephemeral Volumes):** استفاده از حجم‌های غیرپایدار مانند emptyDir برای اشتراک‌گذاری داده‌ها بین دو کانتینر در یک پاد (مثلاً یک کانتینر لاگ تولید می‌کند و کانتینر سایدکار آن را به سرور مرکزی می‌فرستد) و استفاده از hostPath از ریزموضوعات این بخش است.17

### **دامنه ۳: استقرار برنامه‌ها (۲۰٪ وزن آزمون)**

توانایی مدیریت چرخه انتشار نرم‌افزار بدون قطعی سرویس‌دهی، قلب تپنده این دامنه است.8

* **به‌روزرسانی‌های غلتان و استراتژی‌ها (Rolling Updates):** داوطلب باید بتواند یک استقرار را به نسخه جدیدی از تصویر کانتینر ارتقاء دهد. تنظیم دقیق پارامترهای maxSurge (حداکثر تعداد پادهای اضافه‌تر از ظرفیت مجاز در حین به‌روزرسانی) و maxUnavailable (حداکثر تعداد پادهای خارج از سرویس) بسیار مهم است. همچنین توانایی توقف (Pause)، ازسرگیری (Resume) و لغو به‌روزرسانی (kubectl rollout undo) در صورت بروز خطا ارزیابی می‌شود.17  
* **مدیریت بسته‌ها با Helm:** یکی از تفاوت‌های عمده CKAD با CKA، تمرکز ویژه بر ابزار Helm است.15 سناریوها شامل نصب یک بسته (Release)، جستجوی مخازن، بررسی رندرینگ قالب‌ها با helm template، تغییر مقادیر پیش‌فرض در حین نصب با استفاده از فایل‌های ارزش (values.yaml)، و ارتقاء یا لغو ارتقاء نسخه‌های استقراریافته با Helm است.17  
* **مدیریت پیکربندی با Kustomize:** داوطلب باید بتواند یک فایل kustomization.yaml را درک کرده، وصله‌ها (Patches) را ترکیب نماید و پیکربندی‌های مختلف را با دستور kubectl apply \-k بر روی لایه‌های پایه (Bases) و روکش‌ها (Overlays) اعمال کند.17  
* **الگوهای استقرار پیشرفته:** پیاده‌سازی مکانیزم‌های استقرار قناری (Canary Deployments) و استقرار آبی/سبز (Blue/Green) از طریق دستکاری برچسب‌ها (Labels) و انتخاب‌گرهای سرویس در طول آزمون مورد سوال قرار می‌گیرد.14

### **دامنه ۴: سرویس‌ها و شبکه‌سازی (۲۰٪ وزن آزمون)**

در این بخش، شبکه‌سازی لایه کاربرد و مدیریت ترافیک ورودی به شدت ارزیابی می‌شود.17

* **سیاست‌های شبکه (NetworkPolicies):** توسعه‌دهندگان باید بتوانند ترافیک ورودی (Ingress) و خروجی (Egress) به پادهای خود را محدود کنند. این شامل نگارش قوانینی بر اساس podSelector، namespaceSelector و بلوک‌های آدرس IP (ipBlock)، و همچنین ایجاد سیاست‌های «انکار پیش‌فرض» (Default Deny) برای فضاهای نام است.17  
* **مسیریابی پیشرفته با Ingress و Gateway API:** پیکربندی مسیریابی مبتنی بر مسیر (Path-based) و مبتنی بر میزبان (Host-based) با استفاده از منابع سنتی Ingress و خاتمه اتصالات امن (TLS Termination) همچنان در آزمون حضور دارد.14 با این حال، در نسخه ۱.۳۵، تمرکز ویژه‌ای بر روی Gateway API و به‌خصوص ایجاد آبجکت‌های HTTPRoute از سوی توسعه‌دهندگان وجود دارد که نحوه تسهیم ترافیک را کنترل می‌کنند.20 (جزئیات این ویژگی در بخش‌های بعدی تشریح خواهد شد).

### **دامنه ۵: قابلیت مشاهده و نگهداری (۱۵٪ وزن آزمون)**

تضمین پایداری و سلامت اجرای برنامه‌ها هدف این دامنه است.17

* **پروب‌های سلامت (Probes):** پیاده‌سازی دقیق پروب‌های حیات (Liveness Probes) برای راه‌اندازی مجدد کانتینرهای قفل‌شده، پروب‌های آمادگی (Readiness Probes) برای جلوگیری از ارسال ترافیک به پادهای در حال پردازش اولیه، و پروب‌های راه‌اندازی (Startup Probes) برای برنامه‌هایی که بوت شدن آن‌ها زمان‌بر است، کاملاً ضروری است. داوطلب باید بتواند پارامترهایی نظیر initialDelaySeconds و periodSeconds را تنظیم کرده و از متدهای ارزیابی نظیر httpGet یا اجرای دستورات شل با exec بهره ببرد.14  
* **عیب‌یابی لایه کاربرد:** تحلیل خطاهای رایج توسعه‌دهندگان نظیر CrashLoopBackOff و ImagePullBackOff با بررسی لاگ کانتینرها (با پرچم \-c برای پادهای چندکانتینری) و بررسی رویدادهای سیستم (kubectl describe pod). در نسخه ۱.۳۵، استفاده از قابلیت کانتینرهای گذرا (Ephemeral Containers) با استفاده از دستور kubectl debug برای عیب‌یابی پادهایی که فاقد ابزارهای خط فرمان هستند (نظیر تصاویر Distroless) بسیار حیاتی است.10  
* **مدیریت APIهای منسوخ‌شده:** توانایی کشف منابعی که از نسخه‌های قدیمی و منسوخ‌شده API استفاده می‌کنند و به‌روزرسانی آن‌ها به نسخه‌های جدید برای استقرار موفق در کلاستر.17

| چک‌لیست اختصاصی CKAD | حوزه‌های تمرکز دقیق در سناریوهای آزمون |
| ----: | ----: |
| **توسعه امن کانتینرها** | تنظیم runAsNonRoot: true و مدیریت SecurityContext، سهمیه‌بندی فضاها با ResourceQuota |
| **عملیات استقرار غلتان** | درک کامل پارامترهای maxSurge و maxUnavailable در کنترل رفتار به‌روزرسانی‌ها و Rollback |
| **پروب‌های سلامت برنامه‌ها** | تفکیک دقیق سناریوهای کاربرد Liveness، Readiness و Startup و پارامترهای زمانی آن‌ها |
| **مدیریت بسته‌های بومی ابری** | نصب، تغییر پارامتر و رول‌بک پکیج‌های Helm و مدیریت Overlays در Kustomize |
| **وظایف پردازشی دسته‌ای** | ایجاد CronJob با تنظیمات activeDeadlineSeconds و failedJobsHistoryLimit |
| **مسیریابی و محدودسازی شبکه** | پیاده‌سازی NetworkPolicies با استفاده از عملگرهای انتخاب‌گر، ساخت HTTPRoute |

## **کالبدشکافی آزمون CKA: چک‌لیست ریزموضوعات اختصاصی (ویژه مدیران کلاستر)**

آزمون CKA به‌طور بنیادین روی پایداری زیرساخت، بازیابی از فاجعه (Disaster Recovery) و مدیریت دسترسی‌ها در سطح کلان تمرکز دارد.7 این مباحث که ۶۰ درصد از محتوای مختص CKA را شکل می‌دهند، نیازمند تسلط بر سیستم‌عامل لینوکس و معماری داخلی کوبرنتیز هستند. سرفصل‌های این آزمون نیز در پنج دامنه تقسیم‌بندی شده‌اند.

### **دامنه ۱: عیب‌یابی زیرساخت و کنترل‌پلین (۳۰٪ وزن آزمون)**

این دامنه با داشتن بالاترین وزن، سرنوشت‌سازترین بخش آزمون است و سؤالات آن تحت فشار زمانی بسیار "بی‌رحمانه" توصیف شده‌اند.7

* **عیب‌یابی Kubelet و Containerd:** یکی از متداول‌ترین سناریوها، مواجهه با نودی است که در وضعیت NotReady قرار دارد. داوطلب باید به نود لاگین کرده (از طریق SSH) و سرویس‌های سیستمی را بررسی کند. مهارت کار با systemctl status kubelet و بررسی لاگ‌ها با journalctl \-u kubelet حیاتی است.9 خطاهای رایج شامل مسیر اشتباه گواهینامه‌ها در فایل پیکربندی kubeconfig یا از کار افتادن موتور کانتینر است. با توجه به حذف کامل پشتیبانی از cgroup v1 در نسخه ۱.۳۵، داوطلبان باید توانایی بررسی فایل‌های پیکربندی containerd (/etc/containerd/config.toml) را برای اطمینان از تنظیم صحیح SystemdCgroup \= true داشته باشند.9  
* **عیب‌یابی اجزای کنترل‌پلین:** اگر زمان‌بند (Scheduler) یا مدیر کنترل‌کننده (Controller Manager) از کار افتاده باشند، داوطلب باید پادهای ایستای (Static Pods) مربوطه را در مسیر /etc/kubernetes/manifests بررسی کرده و خطاهای املایی یا مقادیر اشتباه پرچم‌ها را در فایل‌های YAML تصحیح کند.9  
* **استفاده از kubectl debug برای عیب‌یابی نودها:** ویژگی پایدارشده kubectl debug node/\<node-name\> به داوطلب اجازه می‌دهد تا کانتینری با ابزارهای کامل لینوکس را در فضای نام میزبان اجرا کند تا مشکلات شبکه یا دیسک نود را بررسی نماید.9

### **دامنه ۲: معماری خوشه، نصب و پیکربندی (۲۵٪ وزن آزمون)**

توانایی مدیریت چرخه حیات خوشه از لحظه تولد تا ارتقاء نسخه‌ها در این دامنه سنجیده می‌شود.7

* **نصب و ارتقاء کلاستر با Kubeadm:** ارتقاء نسخه کوبرنتیز (مثلاً از ۱.۳۴ به ۱.۳۵) یک سناریوی قطعی است. داوطلب باید ترتیب اجرای دستورات را به حافظه بسپارد: ابتدا kubeadm upgrade plan و سپس kubeadm upgrade apply v1.35.x برای کنترل‌پلین. در مرحله بعد، خارج کردن نود از مدار با kubectl drain \<node\> \--ignore-daemonsets، ارتقاء بسته‌های kubelet و kubectl با استفاده از مدیر بسته‌های اوبونتو (apt-get)، بارگیری مجدد دیمن‌ها با systemctl daemon-reload و systemctl restart kubelet، و در نهایت بازگرداندن نود به مدار با kubectl cordon کاملاً ضروری است.9  
* **پشتیبان‌گیری و بازیابی پایگاه داده ETCD:** این عملیات قلب تپنده مدیریت بازیابی از فاجعه است.7 داوطلبان باید بتوانند با ابزار خط فرمان etcdctl کار کنند. تنظیم متغیر ETCDCTL\_API=3 الزامی است. هنگام ثبت تصویر لحظه‌ای (Snapshot) و بازیابی آن، داوطلب باید با پرچم‌های \--endpoints، \--cacert (گواهینامه مرجع)، \--cert (گواهینامه کلاینت) و \--key (کلید خصوصی کلاینت) کار کند. استخراج این مسیرها از داخل مانیفست پاد ایستای ETCD از مهارت‌های کلیدی است که باعث صرفه‌جویی در زمان می‌شود.9  
* **کنترل دسترسی مبتنی بر نقش (RBAC):** معماری امنیت خوشه مبتنی بر RBAC است. داوطلبان باید بتوانند منابع Role و ClusterRole را با جزئیات کامل سطح دسترسی (Verbs و Resources) ایجاد کرده و از طریق RoleBinding و ClusterRoleBinding آن‌ها را به کاربران یا گروه‌ها متصل کنند. همچنین باید تفاوت دامنه اثر نقش‌های محدود به فضای نام و نقش‌های سراسری در سطح کلاستر را درک کنند.7

### **دامنه ۳: تنظیمات پیشرفته شبکه و سرویس‌ها (۲۰٪ وزن آزمون)**

مدیر سیستم باید بتواند ترافیک شبکه را در لایه‌های پایین‌رده مدیریت کند.7

* **عیب‌یابی CNI و CoreDNS:** بررسی مشکلات افزونه‌های شبکه کانتینری (مانند Calico یا Cilium) و اطمینان از عملکرد صحیح رزولوشن نام دامنه درون‌خوشه‌ای با مدیریت پادهای CoreDNS.9 درک عملکرد کامپوننت kube-proxy و نحوه ترجمه آدرس‌های IP نیز بخشی از این سناریوهاست.9  
* **Gateway API در سطح زیرساخت:** در حالی که توسعه‌دهندگان HTTPRoute را می‌نویسند، مدیران سیستم (CKA) باید زیرساخت Gateway API را آماده کنند. این شامل نصب تعاریف منابع سفارشی (CRDs) مربوطه، و استقرار آبجکت‌های GatewayClass (معرفی نوع کنترل‌کننده دروازه) و Gateway (تعریف پورت‌ها و آدرس‌های IP شنونده) است.7

### **دامنه ۴: زمان‌بندی بارهای کاری و دامنه ۵: ذخیره‌سازی پیشرفته (۲۵٪ وزن ترکیبی)**

* **قوانین پیشرفته زمان‌بندی:** مدیران باید بتوانند با استفاده از کثیفی‌ها و تحمل‌پذیری‌ها (Taints and Tolerations) پادها را از اجرای روی نودهای خاص منع کنند یا برای نودهای اختصاصی مجوز صادر کنند. همچنین قوانین وابستگی و دفع نودها (Node Affinity / Anti-Affinity) برای استقرار بارهای کاری حساس به هم‌مکانی (Co-location) در این بخش قرار می‌گیرند.9 مدیریت پادهای ایستا (Static Pods) نیز از وظایف اختصاصی مدیران است.9  
* **معماری ذخیره‌سازی پیشرفته:** فراتر از حجم‌های ساده، مدیران باید معماری تخصیص پویای حجم‌های ذخیره‌سازی (Dynamic Volume Provisioning) را درک کنند. این امر نیازمند ایجاد و پیکربندی StorageClasses و درک نحوه تعامل رابط ذخیره‌سازی کانتینر (CSI) با زیرساخت‌های ابری یا دیسک‌های محلی است.7

| چک‌لیست اختصاصی CKA | حوزه‌های تمرکز دقیق در سناریوهای آزمون |
| ----: | ----: |
| **نگهداری از پایگاه داده ETCD** | تسلط بر دستورات etcdctl snapshot save و restore با پرچم‌های گواهینامه‌ها |
| **عملیات ارتقاء خوشه (Upgrade)** | درک کامل مراحل kubeadm upgrade، به انضمام فرآیندهای drain و ارتقاء بسته kubelet |
| **عیب‌یابی عمیق Kubelet** | استفاده از ابزارهای لینوکس (journalctl, systemctl) برای رفع خطاهای گواهینامه و cgroup |
| **مدیریت دسترسی‌ها (RBAC)** | تسلط بر ساختار Role, ClusterRole, RoleBinding و ClusterRoleBinding |
| **کنترل زمان‌بندی پادها** | تنظیم Taints روی نودها و Tolerations روی پادها برای زمان‌بندی اختصاصی |
| **زیرساخت Gateway API و شبکه** | ساخت منابع GatewayClass و Gateway، و همچنین عیب‌یابی کامپوننت kube-proxy |

## **تغییرات پارادایم در کوبرنتیز نسخه ۱.۳۵ (بسیار مهم برای سال ۲۰۲۶)**

با ارتقاء بستر آزمون‌ها به نسخه ۱.۳۵ در سال ۲۰۲۶، مجموعه‌ای از قابلیت‌های آزمایشی به وضعیت پایدار (Stable/GA) و قابلیت‌های آلفا به وضعیت بتا (Beta) رسیده‌اند. این تغییرات مفاهیم جدیدی را وارد چرخه آزمون‌ها کرده‌اند که عدم آشنایی با آن‌ها، شانس موفقیت را به‌شدت کاهش می‌دهد.4

### **۱. تغییر اندازه درجای منابع پاد (In-place Pod Resource Resize)**

یکی از چالش‌های تاریخی کوبرنتیز، عدم امکان تغییر درخواست‌ها (Requests) و محدودیت‌های (Limits) پردازنده و حافظه بدون از بین بردن و راه‌اندازی مجدد پادها بود. در نسخه ۱.۳۵، قابلیت تغییر اندازه درجای منابع پاد (In-place Pod Vertical Scaling) به‌صورت کامل پایدار شده است.5 این امر مستقیماً بر سناریوهای آزمون CKAD و CKA تأثیر می‌گذارد، زیرا توسعه‌دهندگان و مدیران اکنون باید بتوانند بدون ایجاد قطعی در سرویس (به‌ویژه برای بارهای کاری حساس نظیر هوش مصنوعی)، منابع را در لحظه (On-the-fly) مدیریت کنند.5

در مانیفست پادها، فیلد جدیدی به نام resizePolicy در سطح کانتینر اضافه شده است. این فیلد تعیین می‌کند که آیا تغییرات پردازنده یا حافظه نیازمند راه‌اندازی مجدد است یا خیر. برای مثال، اگر restartPolicy برای cpu روی NotRequired تنظیم شده باشد، داوطلب می‌تواند با استفاده از دستور JSON Patch زیر، منابع را در لحظه افزایش دهد: kubectl patch pod resize-demo \-n qos-example \--subresource resize \--patch '{"spec":{"containers":\[{"name":"pause", "resources":{"requests":{"cpu":"800m"}, "limits":{"cpu":"800m"}}}\]}}'.28 پس از اجرای این دستور، وضعیت کانتینر بررسی می‌شود. اگر منابع نود کافی نباشد، پاد وارد وضعیت PodResizePending می‌شود.30 اگر منابع کافی باشد، تغییرات اعمال شده و فیلد status.containerStatuses\[\*\].resources مقادیر جدید (مثلاً cpu: 800m) را نشان می‌دهد، بدون آنکه restartCount افزایش یابد.11 داوطلبان باید توجه داشته باشند که استفاده از پرچم \--subresource resize نیازمند کلاینت kubectl نسخه ۱.۳۲ به بالا است که در محیط آزمون ۱.۳۵ کاملاً فراهم است.28

### **۲. معماری نوین مسیریابی: رابط برنامه‌نویسی دروازه (Gateway API)**

اگرچه منابع کلاسیک Ingress همچنان پشتیبانی می‌شوند، اما Gateway API به عنوان استاندارد جدید و پایدار در مسیریابی لایه ۴ و ۷ در برنامه‌درسی ۲۰۲۶ قرار گرفته است.7 در آزمون‌ها، داوطلبان با نقش‌های متفاوتی روبرو هستند. در آزمون CKAD، از توسعه‌دهنده خواسته می‌شود تا یک HTTPRoute ایجاد کند. این آبجکت بسیار انعطاف‌پذیرتر از Ingress سنتی است. برای مثال، در سناریوی تسهیم ترافیک (Traffic Splitting) برای استقرار قناری، داوطلب باید بر اساس وزن‌های درخواستی، ترافیک را هدایت کند. سینتکس کلیدی در این سناریو به شرح زیر است 20:

YAML

rules:  
  \- backendRefs:  
    \- name: foo-v1  
      port: 8080  
      weight: 90  
    \- name: foo-v2  
      port: 8080  
      weight: 10

همچنین مسیریابی مبتنی بر هدر (Header-based Routing) از چالش‌های جدید است؛ برای مثال، ارسال درخواست‌هایی که دارای هدر X-API-Version: v2 هستند به یک سرویس خاص، از طریق تطبیق‌گرها (matches.headers) در HTTPRoute انجام می‌پذیرد.21

### **۳. کنترل‌کننده‌های پذیرش تاییدکننده مبتنی بر CEL**

در گذشته، مدیران سیستم برای اعمال محدودیت‌های اعتبارسنجی پیچیده (مانند الزام به داشتن یک برچسب خاص روی تمامی پادها) مجبور به راه‌اندازی و نگهداری سرویس‌های خارجی تحت عنوان وب‌هوک‌های پذیرش (Admission Webhooks) بودند. با معرفی ValidatingAdmissionPolicy به‌عنوان یک قابلیت پایدار در کوبرنتیز ۱.۳۵، اکنون کدهای اعتبارسنجی مستقیماً از طریق زبان مشترک ارزیابی (Common Expression Language \- CEL) درون سرور API اجرا می‌شوند.9 این تغییر پارادایم، وزن زیادی در آزمون CKA سال ۲۰۲۶ دارد. داوطلبان باید بتوانند عبارات منطقی CEL را بنویسند. چند نمونه از عباراتی که در سناریوها ارزیابی می‌شوند عبارتند از 12:

* اعتبارسنجی شروع شدن نام پاد با پیشوندی خاص: object.metadata.name.startsWith(object.prefix)  
* اعتبارسنجی وجود کلید و مقدار خاص در تنظیمات: object.widgets.exists(w, w.key \== 'x' && w.foo \< 10\)  
* اعتبارسنجی وجود پیشوند مشخص برای یک رشته متنی: object.health.startsWith('ok') داوطلبان همچنین باید بتوانند این سیاست‌ها را با استفاده از ValidatingAdmissionPolicyBinding به فضاهای نام هدف متصل کنند و پیش از اعمال نهایی، آن‌ها را در حالت ممیزی (Audit Mode) تست نمایند.12

### **۴. گواهینامه‌های پاد (Pod Certificates) برای معماری بدون اعتماد**

با ترویج معماری شبکه‌های بدون اعتماد (Zero Trust) و استقرار سرویس‌مش‌ها، مدیریت هویت بارهای کاری پیچیده شده است. در نسخه ۱.۳۵، قابلیت بومی کوبرنتیز برای صدور و چرخش خودکار گواهینامه‌های X.509 برای پادها، به وضعیت بتا ارتقاء یافته است.4 در آزمون‌ها، داوطلبان ممکن است نیازمند پیکربندی یک حجم داده پرتابل (Projected Volume) برای کانتینر باشند. آن‌ها باید در مانیفست YAML، منبع حجم را از نوع podCertificate تعریف کنند و فیلدهای signerName (معرفی صادرکننده گواهینامه) و keyType (مانند ED25519 یا RSA3072) را تنظیم نمایند.36 Kubelet وظیفه تولید کلیدها، ثبت درخواست صدور گواهینامه (CSR)، نصب زنجیره گواهینامه‌ها در سیستم‌فایل کانتینر و چرخش دوره‌ای آن‌ها را پیش از انقضا به صورت خودکار بر عهده می‌گیرد.36

### **۵. فضاهای نام کاربر (User Namespaces) در پادها**

یک پیشرفت امنیتی کلیدی دیگر در نسخه ۱.۳۵ که به صورت پیش‌فرض فعال شده است، قابلیت فضاهای نام کاربر برای پادهاست.4 این ویژگی مانع از خطرات امنیتی تشدید سطح دسترسی (Privilege Escalation) می‌شود. مکانیزم کار به این صورت است که کانتینر درون محیط ایزوله خود با دسترسی ریشه (Root) فعالیت می‌کند، اما شناسه‌های کاربری (UID/GID) آن در سطح ماشین میزبان فیزیکی (Host) به کاربران بدون امتیاز (Unprivileged) نگاشت (Map) می‌شوند.4 داوطلبان در پیکربندی‌های امنیتی آزمون‌های CKA و CKAD باید درک روشنی از نحوه پیکربندی نگاشت شناسه میزبان در مانیفست پاد داشته باشند.

## **استراتژی‌های اجرا و مدیریت زمان در محیط آزمون**

موفقیت در آزمون‌های عملی بومی ابری، تنها به دانش فنی محدود نمی‌شود؛ مهارت‌های بقا در محیط ترمینال و مدیریت بی‌رحمانه زمان تحت استرس، نقشی تعیین‌کننده دارند.8 محیط آزمون تحت پلتفرم امنیتی PSI Bridge اجرا می‌شود که محدودیت‌هایی نظیر ممنوعیت استفاده از مانیتور دوم و تاخیرهای (Lag) احتمالی در رابط کاربری را به همراه دارد.8

### **راهبرد حیاتی بررسی دومرحله‌ای (Two-Pass Strategy)**

گزارش‌های مستخرج از تجربیات برتر در آزمون‌های ۲۰۲۶، استراتژی حل سوالات مبتنی بر دو مرحله را قویاً توصیه می‌کنند.9

* **مرحله اول (بانک امتیازات سریع):** هدف این مرحله کسب سریع امتیازات آسان و ایجاد حاشیه امنیت روانی در ۳۰ دقیقه نخست آزمون است. وظایفی نظیر ایجاد پادها، استقرارها، نقشه‌های پیکربندی یا عملیات node drain که با دستورات امری (Imperative) در کمتر از سه دقیقه حل می‌شوند، باید بدون درنگ اجرا شوند.9  
* **قانون ۸ دقیقه:** اگر بررسی اولیه نشان داد که یک سناریو پیچیده است (مانند عیب‌یابی عمیق Kubelet یا ارتقاء کلاستر با Kubeadm) و به نظر می‌رسد بیش از ۸ دقیقه زمان می‌برد، داوطلب باید فوراً آن را در پلتفرم نشانه‌گذاری (Flag) کرده و عبور کند تا در تله زمانی گرفتار نشود.9  
* **مرحله دوم (بازگشت استراتژیک):** پس از اتمام سوالات سریع، داوطلب به سناریوهای نشانه‌گذاری‌شده بازمی‌گردد. در این مرحله، حل سوالات بر اساس وزن درصدی آن‌ها اولویت‌بندی می‌شود. به عنوان مثال، یک سوال عیب‌یابی با وزن ۷ درصد، بر یک سوال ایجاد سیاست شبکه با وزن ۳ درصد ارجحیت دارد.9

### **بهداشت محیط و تغییر فضاهای نام (Context & Namespace Hygiene)**

یکی از دلایل اصلی از دست دادن نمره در این آزمون‌ها، اجرای صحیح دستورات در کلاستر یا فضای نام اشتباه است.9 محیط آزمون از چندین کلاستر مستقل تشکیل شده است. داوطلبان باید قانون طلایی زیر را پیش از لمس کیبورد برای هر سوال رعایت کنند: دستور تنظیم کانتکست (Context) که در ابتدای هر سوال توسط سیستم ارائه شده است، باید فوراً در ترمینال کپی و اجرا شود. علاوه بر این، در آزمون CKAD برای جلوگیری از خطای اجرای دستور در فضای نام پیش‌فرض، توصیه می‌شود دستور تنظیم دائمی فضای نام برای هر کانتکست: kubectl config set-context \--current \--namespace=\<target-namespace\> در یک فایل متنی (Notepad داخلی پلتفرم) ذخیره شده و در ابتدای هر بخش فراخوانی شود.10 این کار باعث صرفه‌جویی در زمان و جلوگیری از نیاز به وارد کردن مداوم پرچم \-n می‌شود.10

### **بهینه‌سازی خط فرمان و اتکا به مستندات رسمی**

۶۰ ثانیه ابتدایی آزمون باید صرف آماده‌سازی محیط لینوکس شود. تنظیم alias k=kubectl و فعال‌سازی تکمیل خودکار کدها (Bash Autocompletion) باعث افزایش چشمگیر سرعت نگارش می‌شود.9 به دلیل محدودیت‌های سیستم امنیتی PSI، استفاده از کلید Ctrl+W باعث بسته شدن زبانه مرورگر شده و فاجعه‌آفرین است؛ داوطلبان باید به کلیدهای میانبر استاندارد کپی و پیست لینوکس درون پایانه تحت وب (Ctrl+Shift+C و Ctrl+Shift+V) عادت کرده باشند.8 داوطلبان برای ویرایش فایل‌های YAML نیازمند مهارت پایه در استفاده از ویرایشگر vim و کلیدهای حرکتی آن برای حذف، کپی و تغییر سریع خطوط کد هستند.9

در طول آزمون، داوطلبان اجازه دسترسی به مستندات رسمی کوبرنتیز (kubernetes.io/docs) و صفحات گیت‌هاب مربوطه را در مرورگر درون‌سازمانی دارند.9 هنر جستجوی سریع در این مستندات باید پیش از آزمون تمرین شده باشد. به‌ویژه در آزمون CKA، صفحات مربوط به وظایف مدیریتی نظیر ارتقاء خوشه با Kubeadm (بخش Tasks/Administer Cluster) و مسیردهی گواهینامه‌های etcdctl نباید حفظ شوند، بلکه باید با سرعت از روی مستندات مرجع کپی شده و ویرایش شوند.9 با این حال، استفاده حداکثری از ابزار راهنمای خط فرمان (مثلاً اجرای kubectl explain cronjob.spec.jobTemplate) برای یافتن نام فیلدهای فراموش‌شده درون مانیفست‌ها، به مراتب از جستجوی متنی در صفحات وب رسمی سریع‌تر و کارآمدتر است.10

پیش از شرکت در آزمون اصلی، داوطلبان دو جلسه رایگان دسترسی به شبیه‌ساز Killer.sh دارند که با ثبت‌نام ارائه می‌شود.8 شبیه‌ساز Killer.sh به‌صورت هدفمند و با طراحی قبلی، چالش‌برانگیزتر و دشوارتر از آزمون واقعی است تا داوطلب را برای بدترین شرایط زمانی و استرس آماده کند.16 کسب نمرات بالای ۶۰ درصد در این شبیه‌ساز، عموماً نویدبخش موفقیت قطعی و کسب نمرات بالای ۸۰ در آزمون اصلی خواهد بود.9

#### **Works cited**

1. Training | Kubernetes, accessed April 28, 2026, [https://kubernetes.io/training/](https://kubernetes.io/training/)  
2. Training & Certification | CNCF, accessed April 28, 2026, [https://www.cncf.io/training/](https://www.cncf.io/training/)  
3. Everything You Need to Know About the CKA and CKAD \- Cloud Native Computing Foundation, accessed April 28, 2026, [https://www.cncf.io/wp-content/uploads/2020/08/rx-m-webinar-everything-you-need-to-know-about-the-cka-ckad.pdf](https://www.cncf.io/wp-content/uploads/2020/08/rx-m-webinar-everything-you-need-to-know-about-the-cka-ckad.pdf)  
4. Kubernetes Security: 2025 Stable Features and 2026 preview | CNCF, accessed April 28, 2026, [https://www.cncf.io/blog/2025/12/15/kubernetes-security-2025-stable-features-and-2026-preview/](https://www.cncf.io/blog/2025/12/15/kubernetes-security-2025-stable-features-and-2026-preview/)  
5. Kubernetes as AI's operating system: 1.35 release signals | CNCF, accessed April 28, 2026, [https://www.cncf.io/blog/2026/02/23/kubernetes-as-ais-operating-system-1-35-release-signals/](https://www.cncf.io/blog/2026/02/23/kubernetes-as-ais-operating-system-1-35-release-signals/)  
6. Kubernetes 1.35 Features Explained: What's New? (Timbernetes Release) \- YouTube, accessed April 28, 2026, [https://www.youtube.com/watch?v=WK4mDhSJKCU](https://www.youtube.com/watch?v=WK4mDhSJKCU)  
7. CKA Exam Guide 2026: Everything You Need to Know \- Sailor.sh Blog, accessed April 28, 2026, [https://sailor.sh/blog/cka-exam-guide-2026/](https://sailor.sh/blog/cka-exam-guide-2026/)  
8. Certified Kubernetes Application Developer (CKAD) | CNCF, accessed April 28, 2026, [https://www.cncf.io/training/certification/ckad/](https://www.cncf.io/training/certification/ckad/)  
9. theplatformlab/CKA-Certified-Kubernetes-Administrator: CKA Certification Exam Guide 2026 — study notes, practice questions, kubectl cheat sheet, exam tips, and full Kubernetes v1.35 syllabus breakdown. Covers etcd backup, RBAC, kubeadm, Gateway API, NetworkPolicy, troubleshooting, and killer.sh prep. Scored 89%. · GitHub, accessed April 28, 2026, [https://github.com/techwithmohamed/CKA-Certified-Kubernetes-Administrator](https://github.com/techwithmohamed/CKA-Certified-Kubernetes-Administrator)  
10. CKAD 2026: What to Expect & How I Passed | by Aravind \- Medium, accessed April 28, 2026, [https://medium.com/@araviku04/ckad-2026-what-to-expect-how-i-passed-448f134ac8b5](https://medium.com/@araviku04/ckad-2026-what-to-expect-how-i-passed-448f134ac8b5)  
11. Kubernetes 1.35: In-Place Pod Resize Graduates to Stable, accessed April 28, 2026, [https://kubernetes.io/blog/2025/12/19/kubernetes-v1-35-in-place-pod-resize-ga/](https://kubernetes.io/blog/2025/12/19/kubernetes-v1-35-in-place-pod-resize-ga/)  
12. How to Use CEL-Based ValidatingAdmissionPolicy for Kubernetes Native Policies, accessed April 28, 2026, [https://oneuptime.com/blog/post/2026-02-09-cel-validating-admission-policy/view](https://oneuptime.com/blog/post/2026-02-09-cel-validating-admission-policy/view)  
13. Kubernetes Certification Guide 2026: CKA, CKAD, CKS \- Which One Should You Choose?, accessed April 28, 2026, [https://kubezilla.io/kubernetes-certification-guide-2026-cka-ckad-cks-which-one-should-you-choose/](https://kubezilla.io/kubernetes-certification-guide-2026-cka-ckad-cks-which-one-should-you-choose/)  
14. CKA vs CKAD vs CKS — which cert first? (2026 guide) | EITT, accessed April 28, 2026, [https://eitt.academy/knowledge-base/cka-vs-ckad-vs-cks-kubernetes-certifications/](https://eitt.academy/knowledge-base/cka-vs-ckad-vs-cks-kubernetes-certifications/)  
15. CKAD vs CKA: Key Differences Every Developer Should Know \- Sailor.sh Blog, accessed April 28, 2026, [https://sailor.sh/blog/ckad-vs-cka](https://sailor.sh/blog/ckad-vs-cka)  
16. CKA vs. CKAD: Which Kubernetes Certification Should You Choose in 2026?, accessed April 28, 2026, [https://www.practical-devsecops.com/cka-vs-ckad/](https://www.practical-devsecops.com/cka-vs-ckad/)  
17. ckad-dojo/docs/ckad-curriculum.md at main · TiPunchLabs/ckad ..., accessed April 28, 2026, [https://github.com/TiPunchLabs/ckad-dojo/blob/main/docs/ckad-curriculum.md](https://github.com/TiPunchLabs/ckad-dojo/blob/main/docs/ckad-curriculum.md)  
18. CKAD is Easier Than CKA: How I Passed with 20 Hours of Study \- DEV Community, accessed April 28, 2026, [https://dev.to/suzuki0430/ckad-is-easier-than-cka-how-i-passed-with-20-hours-of-study-432d](https://dev.to/suzuki0430/ckad-is-easier-than-cka-how-i-passed-with-20-hours-of-study-432d)  
19. Are Helm & Kustomize Included? (Exam on March 23 – Need Clarification) : r/ckad \- Reddit, accessed April 28, 2026, [https://www.reddit.com/r/ckad/comments/1rmbefk/ckad\_exam\_are\_helm\_kustomize\_included\_exam\_on/](https://www.reddit.com/r/ckad/comments/1rmbefk/ckad_exam_are_helm_kustomize_included_exam_on/)  
20. HTTPRoute \- Kubernetes Gateway API, accessed April 28, 2026, [https://gateway-api.sigs.k8s.io/api-types/httproute/](https://gateway-api.sigs.k8s.io/api-types/httproute/)  
21. How to Configure Kubernetes Gateway API with HTTPRoute \- OneUptime, accessed April 28, 2026, [https://oneuptime.com/blog/post/2026-02-20-kubernetes-gateway-api-httproute/view](https://oneuptime.com/blog/post/2026-02-20-kubernetes-gateway-api-httproute/view)  
22. New Features We Find Exciting in the Kubernetes 1.35 Release \- Reddit, accessed April 28, 2026, [https://www.reddit.com/r/kubernetes/comments/1ppj8o3/new\_features\_we\_find\_exciting\_in\_the\_kubernetes/](https://www.reddit.com/r/kubernetes/comments/1ppj8o3/new_features_we_find_exciting_in_the_kubernetes/)  
23. Kubernetes v1.35 Sneak Peek, accessed April 28, 2026, [https://kubernetes.io/blog/2025/11/26/kubernetes-v1-35-sneak-peek/](https://kubernetes.io/blog/2025/11/26/kubernetes-v1-35-sneak-peek/)  
24. CKA Exam Study Guide 2026: Complete, Practical Strategy to Pass on Your First Attempt, accessed April 28, 2026, [https://techwithmohamed.com/blog/cka-exam-study/](https://techwithmohamed.com/blog/cka-exam-study/)  
25. GitHub \- techiescamp/cka-certification-guide: This comprehensive CKA learning path repo equips aspiring Kubernetes administrators with all the knowledge and resources to ace the CKA exam on the first try. Includes in-depth explanations, hands-on labs, and valuable study materials. Pass the CKA and unlock your Kubernetes potential today\!, accessed April 28, 2026, [https://github.com/techiescamp/cka-certification-guide](https://github.com/techiescamp/cka-certification-guide)  
26. Kubernetes v1.35: Timbernetes (The World Tree Release), accessed April 28, 2026, [https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/](https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/)  
27. Why Kubernetes 1.35 is a game-changer for stateful workload scaling \- The New Stack, accessed April 28, 2026, [https://thenewstack.io/kubernetes-vpa-inplace-resize/](https://thenewstack.io/kubernetes-vpa-inplace-resize/)  
28. Resize CPU and Memory Resources assigned to Containers \- Kubernetes, accessed April 28, 2026, [https://kubernetes.io/docs/tasks/configure-pod-container/resize-container-resources/](https://kubernetes.io/docs/tasks/configure-pod-container/resize-container-resources/)  
29. Resize CPU and Memory Resources assigned to Pods \- Kubernetes, accessed April 28, 2026, [https://kubernetes.io/docs/tasks/configure-pod-container/resize-pod-resources/](https://kubernetes.io/docs/tasks/configure-pod-container/resize-pod-resources/)  
30. In-place Pod resizing in Kubernetes: How it works and how to use it | Tech blog \- Palark, accessed April 28, 2026, [https://palark.com/blog/in-place-pod-resizing-kubernetes/](https://palark.com/blog/in-place-pod-resizing-kubernetes/)  
31. Kubernetes Gateway API: Introduction, accessed April 28, 2026, [https://gateway-api.sigs.k8s.io/](https://gateway-api.sigs.k8s.io/)  
32. CKA (Certified Kubernetes Administrator) Exam Report 2026: Don't Rely on Old Guides (Mastering the Post-2025 Revision), accessed April 28, 2026, [https://dev.to/suzuki0430/cka-certified-kubernetes-administrator-exam-report-2026-dont-rely-on-old-guides-mastering-the-534m](https://dev.to/suzuki0430/cka-certified-kubernetes-administrator-exam-report-2026-dont-rely-on-old-guides-mastering-the-534m)  
33. Validating Admission Policy \- Kubernetes, accessed April 28, 2026, [https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/)  
34. A Deep Dive into Kubernetes Validating Admission Policy: The Native Alternative to Webhooks | by Chetan Atole | Medium, accessed April 28, 2026, [https://medium.com/@chetanatole99/a-deep-dive-into-kubernetes-validating-admission-policy-the-native-alternative-to-webhooks-b35df05e6a5b](https://medium.com/@chetanatole99/a-deep-dive-into-kubernetes-validating-admission-policy-the-native-alternative-to-webhooks-b35df05e6a5b)  
35. Kubernetes Validation Admission Policy \- local testing guide and valuable resources \- GitHub, accessed April 28, 2026, [https://github.com/datreeio/validating-admission-policy](https://github.com/datreeio/validating-admission-policy)  
36. Projected Volumes | Kubernetes, accessed April 28, 2026, [https://v1-35.docs.kubernetes.io/docs/concepts/storage/projected-volumes/](https://v1-35.docs.kubernetes.io/docs/concepts/storage/projected-volumes/)  
37. Kubernetes 1.35 \- New security features \- Sysdig, accessed April 28, 2026, [https://www.sysdig.com/blog/kubernetes-1-35-whats-new](https://www.sysdig.com/blog/kubernetes-1-35-whats-new)  
38. New Features We Find Exciting in the Kubernetes 1.35 Release \- MetalBear, accessed April 28, 2026, [https://metalbear.com/blog/kubernetes-1-35/](https://metalbear.com/blog/kubernetes-1-35/)  
39. Certified Kubernetes Administrator CKA Exam Simulator 2026 \- Tutorials Dojo Portal, accessed April 28, 2026, [https://portal.tutorialsdojo.com/courses/certified-kubernetes-administrator-cka-exam-simulator-2026/](https://portal.tutorialsdojo.com/courses/certified-kubernetes-administrator-cka-exam-simulator-2026/)
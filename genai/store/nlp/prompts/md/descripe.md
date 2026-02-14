# Semantic Car Description Generation

## Context

We are building an e-commerce platform. We need to generate a natural, human-like Arabic description for each car. This description is critical for our **semantic search** engine, allowing users to find cars by describing what they *want* (e.g., "a safe car for my family," "a fast car for the weekend") instead of just filtering by technical specs.

## Task

Based on the provided **JSON object** (which matches the `Car` Pydantic model), generate a single, engaging, and **natural Arabic description**. This description must *interpret* the technical features into real-world benefits and lifestyle uses.

### Guiding Principles for Interpretation

1.  **Synthesize Identity:** Combine `brand`, `model`, `year`, and `trim`.
2.  **Define the Use Case:** This is the most important part.
    * `body_type` ("SUV", "Minivan") + `features` (like "7-seater", "Rear-seat entertainment") → "سيارة عائلية بامتياز" (A perfect family car).
    * `body_type` ("Sedan", "Hatchback") + `fuel_type` ("Hybrid", "Electric") → "مثالية للتنقل اليومي داخل المدينة واقتصادية جداً" (Ideal for daily city commuting and very economical).
    * `body_type` ("Coupe", "Convertible") + high `horsepower` → "سيارة رياضية لعشاق السرعة والأداء" (A sports car for speed and performance enthusiasts).
3.  **Describe Performance & Feel:**
    * High `horsepower` (>300) or specific `engine_type` ("V6", "V8") → "توفر أداء قوياً وتسارعاً مثيراً" (Offers strong performance and thrilling acceleration).
    * `fuel_type` ("Hybrid", "Electric") → "تتميز بالهدوء والكفاءة في استهلاك الطاقة" (Characterized by quietness and energy efficiency).
    * `transmission` ("Manual") → "لتجربة قيادة تفاعلية وممتعة" (For an interactive and fun driving experience).
4.  **Assess Condition & Value:**
    * Low `mileage_km` (< 50,000) → "بحالة شبه جديدة" (In almost-new condition) or "ممشاها قليل" (low mileage).
    * High `mileage_km` (> 150,000) → "سيارة مستعملة بحالة جيدة واعتناء" (A used car in good, well-maintained condition).
    * `discount_percent` (> 0) → "فرصة ممتازة بسعر مخفض" (An excellent opportunity at a discounted price).
5.  **Highlight Luxury & Tech:**
    * Parse the `features` string. "Leather seats, Sunroof, Premium audio" → "مقصورة فخمة مع مقاعد جلدية وفتحة سقف" (A luxurious cabin with leather seats and a sunroof).
    * "Navigation, Apple CarPlay" → "مزودة بأحدث أنظمة الترفيه والملاحة" (Equipped with the latest entertainment and navigation systems).

---

## Examples (Input → Output)

Here are examples of how to apply these principles.

### Example 1: Family SUV

**Input (JSON):**
```json
{
    "car_id": "c9a8f7",
    "brand": "Toyota",
    "model": "Highlander",
    "year": 2021,
    "trim": "Limited",
    "body_type": "SUV",
    "engine_type": "V6",
    "engine_size_liters": 3.5,
    "horsepower": 295,
    "transmission": "Automatic",
    "fuel_type": "Gasoline",
    "mileage_km": 45000,
    "features": "Leather seats, Sunroof, Navigation, 7-seater, Blind Spot Monitor"
}
````

**Semantic Description:**
"سيارة عائلية بامتياز وحجمها كبير. هي مثالية للسفر والرحلات الطويلة بفضل محركها القوي V6 ومقاعدها السبعة المريحة. السيارة بحالة شبه جديدة وممشاها قليل. تعتبر فئة ليميتد فخمة، مع مقاعد جلد، فتحة سقف، وأنظمة أمان متقدمة مثل كشف النقطة العمياء. خيار رائع لمن يبحث عن سيارة عائلية متكاملة."

---

### Example 2: Economical Commuter

**Input (JSON):**

```json
{
    "car_id": "h5b1a2",
    "brand": "Hyundai",
    "model": "Elantra",
    "year": 2019,
    "trim": "SEL",
    "body_type": "Sedan",
    "engine_type": "4-Cylinder",
    "engine_size_liters": 2.0,
    "horsepower": 147,
    "transmission": "Automatic",
    "fuel_type": "Gasoline",
    "mileage_km": 110000,
    "features": "Apple CarPlay, Bluetooth, Backup Camera",
    "discount_percent": 5
}
```

**Semantic Description:**
"سيارة سيدان عملية واقتصادية جداً، مثالية للتنقل اليومي داخل المدينة بفضل استهلاكها الممتاز للوقود. السيارة مستعملة بحالة جيدة وممشاها معقول. مجهزة بالميزات الأساسية مثل آبل كاربلاي وكاميرا خلفية. هي خيار رائع كسيارة أولى أو للتوفير في مصاريف التشغيل اليومية، ومتوفرة حالياً بسعر مخفض."

---

### Example 3: Sports Car Enthusiast

**Input (JSON):**

```json
{
    "car_id": "p9r3t4",
    "brand": "Ford",
    "model": "Mustang",
    "year": 2020,
    "trim": "GT",
    "body_type": "Coupe",
    "engine_type": "V8",
    "engine_size_liters": 5.0,
    "horsepower": 460,
    "transmission": "Manual",
    "fuel_type": "Gasoline",
    "mileage_km": 22000,
    "features": "Performance Package, Leather Sport Seats, Premium Audio"
}
```

**Semantic Description:**
"سيارة رياضية بامتياز لعشاق القوة والأداء. تأتي بمحرك V8 جبار وناقل حركة يدوي (مانيوال) لتجربة قيادة تفاعلية وممتعة. السيارة بحالة ممتازة وممشاها قليل جداً. بتصميمها الكوبيه الجذاب ومقاعدها الرياضية، هي ليست مجرد سيارة للتنقل، بل هي مصممة لمن يبحث عن الإثارة ومتعة القيادة في عطلات نهاية الأسبوع."

---

## Car Input (JSON)

{cars_str}

## Semantic Description (The description without extra text)

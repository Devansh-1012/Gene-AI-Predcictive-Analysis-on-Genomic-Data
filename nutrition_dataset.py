# nutrition_dataset.py
# Comprehensive nutrition and supplement database with evidence-based recommendations

NUTRITION_DATABASE = {
    "cardiovascular disease": {
        "general_advice": "Focus on heart-healthy nutrition with emphasis on reducing inflammation and improving cardiovascular function through evidence-based dietary patterns.",
        "foods_to_include": {
            "all": [
                "fatty fish (salmon, mackerel, sardines) - rich in omega-3 EPA/DHA",
                "leafy greens (spinach, kale, Swiss chard) - high in nitrates and antioxidants",
                "berries (blueberries, strawberries, raspberries) - rich in polyphenols",
                "nuts and seeds (almonds, walnuts, chia seeds) - healthy fats and fiber",
                "olive oil (extra virgin) - monounsaturated fats and polyphenols",
                "whole grains (oats, quinoa, brown rice) - fiber and nutrients",
                "legumes (lentils, chickpeas, black beans) - plant protein and fiber",
                "avocado - monounsaturated fats and potassium",
                "dark chocolate (70%+ cocoa) - flavonoids and antioxidants",
                "garlic - allicin and sulfur compounds",
                "tomatoes - lycopene and potassium",
                "pomegranate - polyphenols and antioxidants"
            ],
            "adolescent": [
                "lean proteins (chicken breast, turkey, fish) - growth support",
                "dairy products (low-fat milk, yogurt) - calcium and protein",
                "colorful vegetables (bell peppers, carrots, broccoli) - diverse nutrients"
            ],
            "young_adult": [
                "omega-3 rich foods (salmon, flaxseeds, walnuts) - heart health",
                "antioxidant-rich fruits (citrus, berries, apples) - cellular protection",
                "plant proteins (tofu, tempeh, legumes) - sustainable protein"
            ],
            "middle_aged": [
                "fiber-rich foods (oats, beans, vegetables) - cholesterol management",
                "potassium-rich foods (bananas, sweet potatoes, spinach) - blood pressure",
                "heart-healthy fats (avocado, nuts, olive oil) - lipid profile"
            ],
            "senior": [
                "easily digestible proteins (fish, eggs, yogurt) - muscle maintenance",
                "soft fruits (berries, bananas, peaches) - easy consumption",
                "cooked vegetables (steamed, roasted) - enhanced absorption"
            ]
        },
        "foods_to_avoid": {
            "all": [
                "trans fats (hydrogenated oils, margarine) - increases LDL cholesterol",
                "excessive sodium (processed foods, canned goods) - raises blood pressure",
                "processed meats (bacon, sausage, deli meats) - high in saturated fat and sodium",
                "refined sugars (soda, candy, baked goods) - promotes inflammation",
                "saturated fats (red meat, full-fat dairy) - raises cholesterol",
                "excessive alcohol (more than 1-2 drinks/day) - can raise blood pressure"
            ],
            "adolescent": [
                "sugary beverages (soda, energy drinks) - empty calories and sugar spikes",
                "fast food (burgers, fries, pizza) - high in unhealthy fats and sodium",
                "processed snacks (chips, crackers) - high in sodium and unhealthy fats"
            ],
            "young_adult": [
                "excessive alcohol (more than 2 drinks/day) - cardiovascular stress",
                "ultra-processed foods (frozen meals, instant foods) - poor nutrient density",
                "high-sodium meals (restaurant food, takeout) - blood pressure impact"
            ],
            "middle_aged": [
                "red meat (beef, pork, lamb) - high in saturated fat",
                "full-fat dairy (whole milk, cheese) - saturated fat content",
                "refined carbohydrates (white bread, pasta) - blood sugar spikes"
            ],
            "senior": [
                "high-sodium foods (canned soups, processed meats) - blood pressure risk",
                "difficult-to-chew items (tough meats, raw vegetables) - swallowing issues",
                "excessive portions (large meals) - digestive stress"
            ]
        },
        "supplements": {
            "all": [
                "omega-3 (EPA/DHA) - 1000-2000 mg daily for heart health",
                "vitamin d - 1000-2000 IU daily for cardiovascular function",
                "magnesium - 300-400 mg daily for blood pressure regulation",
                "coenzyme q10 - 100-300 mg daily for heart muscle function",
                "garlic extract - 600-1200 mg daily for blood pressure support",
                "hawthorn berry - 300-600 mg daily for heart function"
            ],
            "adolescent": [
                "multivitamin - comprehensive nutrient support",
                "calcium - 1000-1300 mg daily for bone development"
            ],
            "young_adult": [
                "vitamin e - 15 mg daily for antioxidant protection",
                "b-complex vitamins - energy metabolism and heart health"
            ],
            "middle_aged": [
                "fish oil - 1000-2000 mg daily for omega-3 support",
                "plant sterols - 2 grams daily for cholesterol management",
                "potassium - 3500-4700 mg daily for blood pressure"
            ],
            "senior": [
                "vitamin b12 - 2.4 mcg daily for nerve function",
                "fiber supplement - 25-35 grams daily for digestive health",
                "vitamin k2 - 100-200 mcg daily for arterial health"
            ]
        },
                 "exercise_plan": {
             "cardio": "30-45 minutes moderate cardio 5 days/week (walking, cycling, swimming) - improves heart function and circulation",
             "strength": "2-3 days/week resistance training focusing on major muscle groups - builds muscle mass and improves metabolism",
             "flexibility": "Daily stretching and yoga for stress reduction - lowers cortisol and blood pressure",
             "intensity": "Moderate intensity, avoid high-intensity intervals if high risk - safe cardiovascular training",
             "precautions": "Monitor heart rate, avoid exercise in extreme temperatures, stop if chest pain occurs"
         },
         "meal_pattern": {
             "all": "Mediterranean-style eating pattern with emphasis on plant-based foods",
             "adolescent": "3 balanced meals with heart-healthy snacks",
             "young_adult": "Regular meals focusing on anti-inflammatory foods",
             "middle_aged": "Portion-controlled Mediterranean diet",
             "senior": "4-5 smaller, nutrient-dense meals throughout day"
         }
    },
    
    "type 2 diabetes": {
        "general_advice": "Focus on blood sugar management through balanced nutrition, regular physical activity, and evidence-based dietary patterns like Mediterranean or DASH diet.",
        "foods_to_include": {
            "all": [
                "complex carbohydrates (quinoa, brown rice, oats) - slow glucose release",
                "fiber-rich foods (vegetables, legumes, whole grains) - blood sugar control",
                "lean proteins (chicken, fish, tofu) - stabilizes blood sugar",
                "healthy fats (avocado, nuts, olive oil) - slows carbohydrate absorption",
                "non-starchy vegetables (broccoli, spinach, cauliflower) - low glycemic impact",
                "berries (blueberries, strawberries, raspberries) - antioxidants and fiber",
                "cinnamon - may improve insulin sensitivity",
                "apple cider vinegar - may help with post-meal blood sugar",
                "chia seeds - high fiber and omega-3 content",
                "green tea - antioxidants and potential glucose benefits"
            ],
            "adolescent": [
                "growth-supporting proteins (lean meats, eggs, dairy) - development needs",
                "calcium-rich foods (milk, yogurt, cheese) - bone development",
                "iron sources (lean red meat, spinach, legumes) - growth requirements"
            ],
            "young_adult": [
                "nutrient-dense whole foods (vegetables, fruits, whole grains) - overall health",
                "varied protein sources (fish, poultry, legumes) - muscle maintenance"
            ],
            "middle_aged": [
                "low-glycemic foods (sweet potatoes, quinoa, legumes) - blood sugar control",
                "antioxidant-rich foods (berries, dark chocolate, nuts) - cellular protection"
            ],
            "senior": [
                "easily digestible proteins (fish, eggs, yogurt) - muscle preservation",
                "hydrating foods (soups, smoothies, fruits) - hydration support",
                "nutrient-dense options (nuts, seeds, avocados) - concentrated nutrition"
            ]
        },
        "foods_to_avoid": {
            "all": [
                "refined sugars (white sugar, corn syrup, honey) - rapid blood sugar spikes",
                "white bread and pasta - high glycemic index",
                "sugary beverages (soda, juice, energy drinks) - liquid sugar",
                "processed foods (packaged snacks, frozen meals) - hidden sugars",
                "high-glycemic fruits (watermelon, pineapple, dates) - blood sugar impact",
                "alcohol - can interfere with blood sugar regulation"
            ],
            "adolescent": [
                "candy and sweets - concentrated sugar",
                "soda and sugary drinks - liquid calories",
                "white pasta and bread - refined carbohydrates",
                "sweetened cereals - breakfast sugar bombs"
            ],
            "young_adult": [
                "alcohol - blood sugar interference",
                "fast food - high in refined carbs and fats",
                "desserts and pastries - concentrated sugar and fat"
            ],
            "middle_aged": [
                "refined grains (white rice, white bread) - blood sugar spikes",
                "sweetened beverages (coffee drinks, smoothies) - hidden sugars",
                "high-fat foods (fried foods, fatty meats) - insulin resistance"
            ],
            "senior": [
                "high-sugar foods (candy, desserts) - blood sugar management",
                "difficult-to-digest items (raw vegetables, tough meats) - digestive stress",
                "large portions - blood sugar spikes"
            ]
        },
        "supplements": {
            "all": [
                "chromium - 200-1000 mcg daily for glucose metabolism",
                "magnesium - 300-400 mg daily for insulin sensitivity",
                "vitamin d - 1000-2000 IU daily for glucose regulation",
                "alpha-lipoic acid - 300-600 mg daily for nerve health",
                "berberine - 500-1500 mg daily for blood sugar control",
                "cinnamon - 1-6 grams daily for insulin sensitivity"
            ],
            "adolescent": [
                "multivitamin - comprehensive nutrient support",
                "calcium - 1000-1300 mg daily for bone development"
            ],
            "young_adult": [
                "omega-3 - 1000-2000 mg daily for inflammation",
                "vitamin e - 15 mg daily for antioxidant protection"
            ],
            "middle_aged": [
                "fenugreek - 5-30 grams daily for blood sugar support",
                "biotin - 30-100 mcg daily for glucose metabolism",
                "coenzyme q10 - 100-300 mg daily for energy production"
            ],
            "senior": [
                "vitamin b12 - 2.4 mcg daily for nerve function",
                "fiber supplement - 25-35 grams daily for digestive health",
                "probiotics - gut microbiome support"
            ]
        },
                 "exercise_plan": {
             "cardio": "150 minutes/week moderate cardio (walking, swimming, cycling) - improves insulin sensitivity",
             "strength": "2-3 days/week resistance training to improve insulin sensitivity - builds muscle mass",
             "flexibility": "Daily stretching and balance exercises - improves circulation",
             "intensity": "Moderate intensity, monitor blood sugar before/after exercise - safe training",
             "precautions": "Check blood sugar before exercise, carry glucose tablets, avoid exercise if blood sugar >250 mg/dL"
         },
         "meal_pattern": {
             "all": "Consistent meal timing with balanced macronutrients",
             "adolescent": "3 structured meals with protein-rich snacks",
             "young_adult": "Regular meals with emphasis on protein and fiber",
             "middle_aged": "Smaller, frequent meals to maintain blood sugar",
             "senior": "4-5 smaller meals with consistent timing"
         }
    },
    
    "obesity": {
        "general_advice": "Focus on sustainable weight management through balanced nutrition, increased physical activity, and evidence-based behavioral strategies.",
        "foods_to_include": {
            "all": [
                "lean proteins (chicken breast, fish, tofu) - increases satiety",
                "fiber-rich vegetables (broccoli, spinach, kale) - low calorie, high volume",
                "whole grains (quinoa, oats, brown rice) - sustained energy",
                "healthy fats (avocado, nuts, olive oil) - satiety and nutrient absorption",
                "low-calorie fruits (berries, apples, pears) - natural sweetness",
                "legumes (lentils, chickpeas, black beans) - protein and fiber",
                "green tea - metabolism support and hydration",
                "apple cider vinegar - may support weight loss",
                "cayenne pepper - metabolism boost",
                "ginger - digestion and metabolism support"
            ],
            "adolescent": [
                "growth-supporting proteins (lean meats, eggs, dairy) - development needs",
                "calcium-rich foods (milk, yogurt, cheese) - bone development",
                "iron sources (lean red meat, spinach, legumes) - growth requirements"
            ],
            "young_adult": [
                "nutrient-dense whole foods (vegetables, fruits, whole grains) - overall health",
                "varied protein sources (fish, poultry, legumes) - muscle maintenance"
            ],
            "middle_aged": [
                "anti-inflammatory foods (berries, fatty fish, nuts) - metabolic health",
                "antioxidant-rich foods (dark chocolate, green tea, spices) - cellular protection"
            ],
            "senior": [
                "easily digestible proteins (fish, eggs, yogurt) - muscle preservation",
                "hydrating foods (soups, smoothies, fruits) - hydration support",
                "nutrient-dense options (nuts, seeds, avocados) - concentrated nutrition"
            ]
        },
        "foods_to_avoid": {
            "all": [
                "highly processed foods (chips, crackers, frozen meals) - high in calories and low in nutrients",
                "excessive sugar (candy, soda, desserts) - empty calories",
                "trans fats (margarine, fried foods, baked goods) - promotes fat storage",
                "refined carbohydrates (white bread, pasta, rice) - blood sugar spikes",
                "sugary beverages (soda, juice, energy drinks) - liquid calories",
                "excessive alcohol - high in calories and reduces inhibition"
            ],
            "adolescent": [
                "sugary beverages (soda, energy drinks) - liquid calories",
                "highly processed snacks (chips, cookies, candy) - empty calories",
                "fast food (burgers, fries, pizza) - high calorie density"
            ],
            "young_adult": [
                "excessive alcohol (more than 2 drinks/day) - calorie dense",
                "ultra-processed foods (frozen meals, instant foods) - poor nutrient density",
                "large portions (restaurant meals, buffets) - overeating risk"
            ],
            "middle_aged": [
                "excessive sodium (processed foods, canned goods) - water retention",
                "refined carbohydrates (white bread, pasta, rice) - blood sugar spikes",
                "high-calorie foods (nuts, oils, fatty meats) - portion control needed"
            ],
            "senior": [
                "high-sodium foods (canned soups, processed meats) - water retention",
                "difficult-to-chew items (tough meats, raw vegetables) - swallowing issues",
                "excessive portions (large meals) - digestive stress"
            ]
        },
        "supplements": {
            "all": [
                "multivitamin - comprehensive nutrient support",
                "vitamin d - 1000-2000 IU daily for metabolism",
                "omega-3 - 1000-2000 mg daily for inflammation reduction",
                "protein powder - 20-30 grams per serving for satiety",
                "green tea extract - 250-500 mg daily for metabolism",
                "fiber supplement - 25-35 grams daily for satiety"
            ],
            "adolescent": [
                "calcium - 1000-1300 mg daily for bone development",
                "iron - 8-15 mg daily for growth support"
            ],
            "young_adult": [
                "vitamin b12 - 2.4 mcg daily for energy metabolism",
                "magnesium - 300-400 mg daily for muscle function"
            ],
            "middle_aged": [
                "conjugated linoleic acid - 3-6 grams daily for fat metabolism",
                "garcinia cambogia - 500-1000 mg daily for appetite control",
                "chromium - 200-1000 mcg daily for glucose metabolism"
            ],
            "senior": [
                "vitamin b12 - 2.4 mcg daily for energy",
                "calcium - 1000-1200 mg daily for bone health",
                "fiber supplement - 25-35 grams daily for digestive health"
            ]
        },
                 "exercise_plan": {
             "cardio": "300 minutes/week moderate cardio for weight loss (walking, cycling, swimming) - creates calorie deficit",
             "strength": "3-4 days/week resistance training to build muscle mass - increases metabolism",
             "flexibility": "Daily stretching and mobility work - improves range of motion",
             "intensity": "Mix of moderate and high-intensity intervals - maximizes calorie burn",
             "precautions": "Start slowly, focus on consistency, avoid overtraining, listen to body signals"
         },
         "meal_pattern": {
             "all": "Portion-controlled meals with emphasis on protein and fiber",
             "adolescent": "3 structured meals with healthy snacks",
             "young_adult": "Regular meals focusing on satiety and nutrition",
             "middle_aged": "Smaller, frequent meals to maintain metabolism",
             "senior": "4-5 smaller, nutrient-dense meals throughout day"
         }
    },
    
    "alzheimer's disease": {
        "general_advice": "Focus on brain-healthy nutrition with emphasis on antioxidants, anti-inflammatory foods, and evidence-based dietary patterns like MIND diet.",
        "foods_to_include": {
            "all": [
                "fatty fish (salmon, mackerel, sardines) - omega-3 DHA for brain health",
                "berries (blueberries, strawberries, blackberries) - polyphenols and antioxidants",
                "leafy greens (spinach, kale, Swiss chard) - folate and antioxidants",
                "nuts and seeds (walnuts, almonds, flaxseeds) - vitamin E and omega-3",
                "olive oil (extra virgin) - monounsaturated fats and polyphenols",
                "whole grains (oats, quinoa, brown rice) - B vitamins and fiber",
                "turmeric - curcumin for anti-inflammatory effects",
                "dark chocolate (70%+ cocoa) - flavonoids and antioxidants",
                "green tea - catechins and L-theanine",
                "avocado - healthy fats and vitamin E",
                "eggs - choline for neurotransmitter production",
                "pumpkin seeds - zinc and magnesium"
            ],
            "adolescent": [
                "omega-3 rich foods (fatty fish, walnuts, chia seeds) - brain development",
                "antioxidant-rich fruits (berries, citrus, apples) - cellular protection",
                "brain-supporting proteins (eggs, fish, lean meats) - neurotransmitter support"
            ],
            "young_adult": [
                "nutrient-dense whole foods (vegetables, fruits, whole grains) - overall health",
                "varied protein sources (fish, poultry, legumes) - brain function"
            ],
            "middle_aged": [
                "anti-inflammatory foods (berries, fatty fish, nuts) - brain protection",
                "antioxidant-rich foods (dark chocolate, green tea, spices) - cellular defense"
            ],
            "senior": [
                "easily digestible proteins (fish, eggs, yogurt) - brain maintenance",
                "hydrating foods (soups, smoothies, fruits) - cognitive function",
                "nutrient-dense options (nuts, seeds, avocados) - concentrated nutrition"
            ]
        },
        "foods_to_avoid": {
            "all": [
                "trans fats (margarine, fried foods, baked goods) - promotes inflammation",
                "excessive sugar (candy, soda, desserts) - oxidative stress",
                "processed foods (packaged snacks, frozen meals) - poor nutrient density",
                "refined carbohydrates (white bread, pasta, rice) - blood sugar spikes",
                "alcohol - neurotoxic effects",
                "excessive salt - blood pressure impact"
            ],
            "adolescent": [
                "sugary beverages (soda, energy drinks) - blood sugar spikes",
                "highly processed snacks (chips, cookies, candy) - poor nutrition",
                "artificial sweeteners - potential neurotoxic effects"
            ],
            "young_adult": [
                "excessive alcohol (more than 2 drinks/day) - brain damage risk",
                "ultra-processed foods (frozen meals, instant foods) - poor nutrients",
                "high-sugar foods (desserts, candy, soda) - oxidative stress"
            ],
            "middle_aged": [
                "excessive sodium (processed foods, canned goods) - blood pressure",
                "refined carbohydrates (white bread, pasta, rice) - inflammation",
                "inflammatory foods (red meat, fried foods) - brain inflammation"
            ],
            "senior": [
                "high-sodium foods (canned soups, processed meats) - blood pressure",
                "difficult-to-chew items (tough meats, raw vegetables) - swallowing issues",
                "excessive portions (large meals) - digestive stress"
            ]
        },
        "supplements": {
            "all": [
                "omega-3 (DHA) - 1000-2000 mg daily for brain health",
                "vitamin d - 1000-2000 IU daily for cognitive function",
                "b-complex vitamins - neurotransmitter production",
                "acetyl-l-carnitine - 500-2000 mg daily for brain energy",
                "phosphatidylserine - 100-300 mg daily for memory",
                "ginkgo biloba - 120-240 mg daily for blood flow"
            ],
            "adolescent": [
                "multivitamin - comprehensive nutrient support",
                "calcium - 1000-1300 mg daily for bone development"
            ],
            "young_adult": [
                "vitamin e - 15 mg daily for antioxidant protection",
                "magnesium - 300-400 mg daily for brain function"
            ],
            "middle_aged": [
                "curcumin - 500-1000 mg daily for anti-inflammatory effects",
                "resveratrol - 100-500 mg daily for antioxidant protection",
                "coenzyme q10 - 100-300 mg daily for energy production"
            ],
            "senior": [
                "vitamin b12 - 2.4 mcg daily for nerve function",
                "vitamin e - 15 mg daily for antioxidant protection",
                "coenzyme q10 - 100-300 mg daily for cellular energy"
            ]
        },
                 "exercise_plan": {
             "cardio": "150 minutes/week moderate cardio to improve blood flow to brain - enhances cognitive function",
             "strength": "2-3 days/week resistance training for cognitive benefits - builds brain connections",
             "flexibility": "Daily stretching and balance exercises - improves coordination",
             "intensity": "Moderate intensity with focus on consistency - sustainable brain health",
             "precautions": "Include cognitive challenges, social interaction during exercise, avoid overexertion"
         },
         "meal_pattern": {
             "all": "MIND diet pattern combining Mediterranean and DASH diets",
             "adolescent": "3 balanced meals with brain-healthy snacks",
             "young_adult": "Regular meals focusing on cognitive support",
             "middle_aged": "Anti-inflammatory meal pattern",
             "senior": "4-5 smaller, nutrient-dense meals throughout day"
         }
    },
    
    "breast cancer": {
        "general_advice": "Focus on anti-inflammatory nutrition and maintaining healthy body weight through evidence-based dietary patterns.",
        "foods_to_include": {
            "all": [
                "cruciferous vegetables (broccoli, cauliflower, Brussels sprouts) - sulforaphane",
                "berries (blueberries, strawberries, raspberries) - antioxidants",
                "fatty fish (salmon, mackerel, sardines) - omega-3 anti-inflammatory",
                "whole grains (oats, quinoa, brown rice) - fiber and nutrients",
                "legumes (lentils, chickpeas, black beans) - plant protein and fiber",
                "green tea - catechins and antioxidants",
                "turmeric - curcumin anti-inflammatory",
                "garlic - allicin and sulfur compounds",
                "mushrooms (shiitake, maitake) - beta-glucans",
                "flaxseeds - lignans and omega-3",
                "pomegranate - ellagic acid and antioxidants",
                "walnuts - omega-3 and antioxidants"
            ],
            "adolescent": [
                "growth-supporting proteins (lean meats, eggs, dairy) - development needs",
                "calcium-rich foods (milk, yogurt, cheese) - bone development",
                "antioxidant-rich fruits (berries, citrus, apples) - cellular protection"
            ],
            "young_adult": [
                "nutrient-dense whole foods (vegetables, fruits, whole grains) - overall health",
                "varied protein sources (fish, poultry, legumes) - muscle maintenance"
            ],
            "middle_aged": [
                "anti-inflammatory foods (berries, fatty fish, nuts) - cellular protection",
                "antioxidant-rich foods (dark chocolate, green tea, spices) - oxidative defense"
            ],
            "senior": [
                "easily digestible proteins (fish, eggs, yogurt) - muscle preservation",
                "hydrating foods (soups, smoothies, fruits) - hydration support",
                "nutrient-dense options (nuts, seeds, avocados) - concentrated nutrition"
            ]
        },
        "foods_to_avoid": {
            "all": [
                "processed meats (bacon, sausage, deli meats) - nitrates and preservatives",
                "excessive alcohol (more than 1 drink/day) - hormone disruption",
                "refined sugars (white sugar, corn syrup) - inflammation",
                "trans fats (margarine, fried foods) - cellular damage",
                "charred foods (grilled meats) - carcinogenic compounds",
                "excessive red meat - saturated fat and iron"
            ],
            "adolescent": [
                "sugary beverages (soda, energy drinks) - inflammation",
                "highly processed snacks (chips, cookies, candy) - poor nutrition",
                "artificial sweeteners - potential health risks"
            ],
            "young_adult": [
                "excessive alcohol (more than 2 drinks/day) - hormone disruption",
                "ultra-processed foods (frozen meals, instant foods) - poor nutrients",
                "high-sugar foods (desserts, candy, soda) - inflammation"
            ],
            "middle_aged": [
                "excessive sodium (processed foods, canned goods) - water retention",
                "refined carbohydrates (white bread, pasta, rice) - blood sugar spikes",
                "inflammatory foods (red meat, fried foods) - cellular stress"
            ],
            "senior": [
                "high-sodium foods (canned soups, processed meats) - blood pressure",
                "difficult-to-chew items (tough meats, raw vegetables) - swallowing issues",
                "excessive portions (large meals) - digestive stress"
            ]
        },
        "supplements": {
            "all": [
                "vitamin d - 1000-2000 IU daily for immune function",
                "omega-3 - 1000-2000 mg daily for anti-inflammatory effects",
                "antioxidants (vitamin e, selenium) - cellular protection",
                "curcumin - 500-1000 mg daily for anti-inflammatory effects",
                "green tea extract - 250-500 mg daily for antioxidants",
                "indole-3-carbinol - 200-400 mg daily for hormone balance"
            ],
            "adolescent": [
                "multivitamin - comprehensive nutrient support",
                "calcium - 1000-1300 mg daily for bone development"
            ],
            "young_adult": [
                "vitamin e - 15 mg daily for antioxidant protection",
                "magnesium - 300-400 mg daily for cellular function"
            ],
            "middle_aged": [
                "resveratrol - 100-500 mg daily for antioxidant protection",
                "coenzyme q10 - 100-300 mg daily for cellular energy",
                "vitamin c - 500-1000 mg daily for immune support"
            ],
            "senior": [
                "vitamin b12 - 2.4 mcg daily for nerve function",
                "vitamin e - 15 mg daily for antioxidant protection",
                "selenium - 55 mcg daily for immune function"
            ]
        },
                 "exercise_plan": {
             "cardio": "150 minutes/week moderate cardio to maintain healthy weight - reduces cancer risk",
             "strength": "2-3 days/week resistance training for bone health - prevents osteoporosis",
             "flexibility": "Daily stretching and yoga for stress reduction - lowers cortisol",
             "intensity": "Moderate intensity with focus on consistency - sustainable health",
             "precautions": "Avoid excessive exercise, focus on stress reduction, listen to body signals"
         },
         "meal_pattern": {
             "all": "Plant-forward diet with emphasis on anti-inflammatory foods",
             "adolescent": "3 balanced meals with healthy snacks",
             "young_adult": "Regular meals focusing on cancer prevention",
             "middle_aged": "Anti-inflammatory meal pattern",
             "senior": "4-5 smaller, nutrient-dense meals throughout day"
         }
    }
}

# Age-specific recommendations
AGE_RECOMMENDATIONS = {
    "adolescent": {
        "calories": "2000-2800 calories daily depending on activity level",
        "protein": "0.8-1.0 grams per kg body weight",
        "calcium": "1000-1300 mg daily",
        "iron": "8-15 mg daily",
        "vitamin_d": "600-800 IU daily"
    },
    "young_adult": {
        "calories": "1800-2400 calories daily depending on activity level",
        "protein": "0.8-1.2 grams per kg body weight",
        "calcium": "1000 mg daily",
        "iron": "8-18 mg daily",
        "vitamin_d": "600-800 IU daily"
    },
    "middle_aged": {
        "calories": "1600-2200 calories daily depending on activity level",
        "protein": "1.0-1.2 grams per kg body weight",
        "calcium": "1000 mg daily",
        "iron": "8 mg daily",
        "vitamin_d": "800-1000 IU daily"
    },
    "senior": {
        "calories": "1400-2000 calories daily depending on activity level",
        "protein": "1.0-1.3 grams per kg body weight",
        "calcium": "1000-1200 mg daily",
        "iron": "8 mg daily",
        "vitamin_d": "800-1000 IU daily"
    }
}

# Exercise intensity guidelines
EXERCISE_GUIDELINES = {
    "low_intensity": {
        "description": "Light walking, gentle stretching, tai chi",
        "heart_rate": "50-60% of max heart rate",
        "duration": "30-60 minutes",
        "frequency": "Daily"
    },
    "moderate_intensity": {
        "description": "Brisk walking, cycling, swimming",
        "heart_rate": "60-70% of max heart rate",
        "duration": "30-45 minutes",
        "frequency": "5-6 days per week"
    },
    "high_intensity": {
        "description": "Running, high-intensity interval training",
        "heart_rate": "70-85% of max heart rate",
        "duration": "20-30 minutes",
        "frequency": "3-4 days per week"
    }
}

def get_nutrition_plan(disease, age_group):
    """Get comprehensive nutrition plan for specific disease and age group"""
    if disease.lower() in NUTRITION_DATABASE:
        return NUTRITION_DATABASE[disease.lower()]
    else:
        # Return general healthy eating plan
        return {
            "general_advice": "Focus on a balanced diet with diverse nutrients to support overall health.",
            "foods_to_include": {
                "all": ["variety of fruits and vegetables", "whole grains", "lean proteins", "healthy fats"],
                "adolescent": ["growth-supporting foods", "calcium-rich foods", "iron sources"],
                "young_adult": ["nutrient-dense whole foods", "varied protein sources"],
                "middle_aged": ["anti-inflammatory foods", "antioxidant-rich foods"],
                "senior": ["easily digestible proteins", "hydrating foods", "nutrient-dense options"]
            },
            "foods_to_avoid": {
                "all": ["highly processed foods", "excessive sugar", "trans fats"],
                "adolescent": ["sugary beverages", "highly processed snacks"],
                "young_adult": ["excessive alcohol", "ultra-processed foods"],
                "middle_aged": ["excessive sodium", "refined carbohydrates"],
                "senior": ["high-sodium foods", "difficult-to-chew items"]
            },
            "supplements": {
                "all": ["multivitamin"],
                "adolescent": ["vitamin d", "calcium"],
                "young_adult": ["vitamin d"],
                "middle_aged": ["vitamin d", "omega-3"],
                "senior": ["vitamin b12", "vitamin d", "calcium"]
            },
            "exercise_plan": {
                "cardio": "150 minutes/week moderate cardio for general health",
                "strength": "2-3 days/week resistance training",
                "flexibility": "Daily stretching and mobility work",
                "intensity": "Moderate intensity with focus on consistency",
                "precautions": "Start slowly, focus on consistency"
            },
            "meal_pattern": {
                "all": "Balanced meals with variety of nutrients and healthy fats",
                "adolescent": "3 balanced meals with variety of nutrients",
                "young_adult": "Regular meals with balanced carbohydrates and proteins",
                "middle_aged": "Portion-controlled meals with balanced carbohydrates and proteins",
                "senior": "4-5 smaller, nutrient-dense meals throughout day"
            }
        }


-- DATABASE 1 USERS ------

DROP TABLE IF EXISTS users;
CREATE TABLE users 
(
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);


--DATABASE 2 ACTIVITIES -------

DROP TABLE IF EXISTS activities;

CREATE TABLE activities 
(
    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    county TEXT NOT NULL,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    pricenote TEXT NOT NULL,
    description TEXT NOT NULL,
    image TEXT NOT NULL

);

INSERT INTO activities(county, category, name, price, pricenote, description, image)
VALUES
    
    ("Belfast", "Nature", "Giant's Causeway", 0, "FREE", "The Giant's Causeway is an area of about 40,000 interlocking basalt columns, the result of an ancient volcanic fissure eruption.", "giants.jpg"),
    ("Clare", "Nature", "Cliffs of Moher", 0,  "FREE", "Visit the awe-inspiring Cliffs of Moher for the ultimate experience with free admission. Located on County Clare’s west coast, the Cliffs stretch for 8 kms/5 miles and 214 metres/700 feet above the Atlantic Ocean. ", "cliffs.jpg"),
    ("Coastal region", "Nature", "The Wild Atlantic Way", 0,  "FREE", "The Wild Atlantic Way, 1600 miles (2600 km) in length, is one of the longest defined coastal routes in the world. It winds its way all along the Irish west coast from the Inishowen Peninsula in the north down to the picturesque town of Kinsale, County Cork, in the south.", "wild.jpg"),
    ("Clare", "Nature", "The Burren",0,  "FREE", "For such a rocky place, the Burren has a poetic beauty that has captivated the hearts and minds of poets, painters, artists and writers. You'll feel it as you walk along butter-colored Fanore Beach, backed by a bare limestone hill and lapped by the Atlantic Ocean.", "burren.jpg"),

    ("Cork", "Museums", "Titanic Experience Cobh", 10.5, "10.50", "Titanic Experience Cobh is a unique visitor experience located in the historic White Star Line Building , the very place from where Titanic’s last passengers departed. Take a guided tour and retrace the footsteps of our Queenstown passengers. Featuring real passenger stories and eyewitness accounts of the tragedy.", "cobh.jpg"),
    ("Waterford", "Museums", "Waterford Treasures Medieval Museum", 10,  "10.00", "Welcome to Medieval Waterford Ireland’s only purpose-built medieval museum and the only building on the island to incorporate two medieval chambers, the 13th-century Choristers’ Hall and the 15th-century Mayor’s Wine Vault.", "waterford.jpg"),
    ("Dublin", "Museums", "National Wax Museum",18,  "18.00", "The National Wax Museum Plus is an interactive tourist attraction based on 22-25 Westmoreland Street. It's fun for all the family!", "wax.jpg"),
    ("Dublin", "Museums", "Little Museum of Dublin", 15, "15.00", "This award-winning museum tells the story of Dublin. Housed in a beautiful Georgian building, our collection was created by public donation. Entry to the museum is by guided tour only, and most tours sell out. To avoid disappointment book your tickets now.", "little.jpg"),

    ("Cork", "Castles", "Blarney Castle",0,  "FREE", "Built nearly six hundred years ago by one of Ireland’s greatest chieftans, Cormac MacCarthy, and has been attracting attention ever since. Over the last few hundred years, millions have flocked to Blarney making it a world landmark and one of Ireland’s greatest treasures.", "blarney.jpg"),
    ("Dublin", "Castles", "Dublin Castle",0,  "FREE", "Constructed in the early thirteenth century on the site of a Viking settlement, Dublin Castle served for centuries as the headquarters of English, and later British, administration in Ireland. In 1922, following Ireland’s independence, Dublin Castle was handed over to the new Irish government. It is now a major government complex and a key tourist attraction. We hope you enjoy your visit.", "dubcastle.jpg"),
    ("Kerry", "Castles", "Ross Castle",5,  "5.00", "A vision on the shores of Lough Leane, the 15th-century Ross Castle was built as a medieval fortress for an Irish chieftain named O’Donoghue, and was said to be one of the last strongholds to fall to the brutal English Cromwellian forces in the mid-16th century. The ruin has been restored, and features lovely 16th- and 17th-century furniture.", "ross.jpg"),
    ("Kilkenny", "Castles", "Kilkenny Castle",0,  "FREE", " Kilkenny Castle is open to visitors all year round and is largely a Victorian remodelling of the thirteenth century defensive Castle. Each year, hundreds of thousands of visitors come to see this grand country house and walk through its fifty acres of rolling parkland with mature trees and an abundance of wildlife.", "kilkenney.jpg"),

    ("Dublin", "Entertainment", "Dublin Zoo", 17.75,  "17.75", "A family favorite, the 69-acre (28-hectare) Dublin Zoo has been around since 1831. Over 400 animals from about 100 different species can be seen across its various sections. In the African Savanna, rhinos, zebras, giraffes, and ostriches roam, while the Asian Forests exhibit is home to lions, snow leopards, and crested black macaques.", "zoo.jpg"),
    ("Waterford", "Entertainment", "Nonstop Karting", 50,  "50.00", "One of Ireland’s most loved karting tracks and is sure to be a day full of thrills for anyone who visits. It’s challenging, it’s exhilarating, and it’s FUN. And it does all this while still maintaining an exceptionally high standard of safety. ", "kart.jpg"),
    ("Wicklow", "Entertainment", "Combat Laser Tag", 22,  "22.00", "Whether you are aged 8 or 98 the exhilarating experience that is Laser Tag has finally come to Jungle Den offering a rollercoaster ride of heart racing laser tag excitement suitable for all ages.Laser Tag is a live lasertag gun combat pursuit set in a thrilling battle zone. The game in many ways mirrors the popular hobby of paint balling. However, instead of getting hit by pellets, you fire lasers at your opponents. ", "laser.jpg"),
    ("Cork", "Entertainment", "We Escape Cork", 15,  "15.00", "Escape room games are a trending type of entertainment in Ireland. For an hour, you'll be locked in a room left to find hidden clues, keys or puzzles, and solve them to escape. Whether you’ll step out as a winner depends on your wit, inventiveness and teamwork. Here you can find information about the best escape rooms provided by different companies. Are you up to the challenge?", "escape.jpg")

;



--DATABASE 4 DATES ----

DROP TABLE IF EXISTS dates;
CREATE TABLE dates 
(
    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL
);

INSERT INTO dates(date)
VALUES
    ( "2023-04-27"),
    ( "2023-04-23"),
    ( "2023-04-22"),
    ( "2023-04-24"),
    ( "2023-03-31"),
    ( "2023-03-30"),
    ( "2023-03-31"),
    ( "2023-03-30"),
    ( "2023-04-01"),
    ( "2023-04-01"),
    ( "2023-04-03"),
    ( "2023-04-03"),
    ( "2023-04-27"),
    ( "2023-04-27"),
    ( "2023-04-01"),
    ( "2023-04-05")
    
;


--reviews table

DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews 
(
    user_id INTEGER NOT NULL,
    activity_name TEXT NOT NULL,
    stars TEXT NOT NULL,
    star_num INTEGER NOT NULL,
    review TEXT NOT NULL
);

DELETE 
FROM reviews
WHERE user_id="chigz";

----DATABASE ADMINS

DROP TABLE IF EXISTS admins;
CREATE TABLE admins
(
    admin_id TEXT PRIMARY KEY
);

INSERT INTO admins
VALUES
    ("derek"),
    ("cm90");
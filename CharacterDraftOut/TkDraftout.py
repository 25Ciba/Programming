import random
import re

#*============*

AOT = [

    'Eren Yeager',

    'Mikasa Ackerman',

    'Armin Arlert',

    'Levi Ackerman',

    'Erwin Smith',

    'Hange Zoë',

    'Sasha Braus',

    'Jean Kirstein',

    'Connie Springer',

    'Historia Reiss',

    'Ymir',

    'Reiner Braun',

    'Bertolt Hoover',

    'Annie Leonhart',

    'Zeke Yeager',

    'Grisha Jaeger',

    'Carla Jaeger',

    'Kenny Akerman',

    'Hannes',

    'Dot Pixis',

    'Keith Shadis',

    'Marco Bott',

    'Floch Forster',

    'Pieck Finger',

    'Porco Galliard',

    'Colt Grice',

    'Gabi Braun',

    'Falco Grice',

    'Theo Magath',

    'Tom Ksaver',

    'Lara Tybur',

    'Ymir Fritz',

    'Flegel Reeves',

    'Kiyomi Azumabito',

    'Niccolo',

    'Yelena',

    'Onyankopon',

]

#*============*

JJK = [

    'Kento Nanami',

    'Mei Mei',

    'Ui Ui',

    'Toji Fushiguro',

    'Yuki Tsukumo',

    'Ryu Ishigori',

    'Hajime Kashimo',

    'Hiromi Higuruma',

    'Takuma Ino',

    'Naobito Zenin',

    'Naoya Zenin',

    'Ogi Zenin',

    'Jinichi Zenin',

    'Ranta Zenin',

    'Master Tengen',

    'Ryomen Sukuna',

    'Kenjaku',

    'Suguru Geto',

    'Uraume',

    'Haruta Shigemo',

    'Jiro Awasaka',

    'Juzo Kumiya',

    'Ogami',

    'Shiu Kong',

    'Larue',

    'Mimiko Hasaba',

    'Nanako Hasaba',

    'Junpei Yoshino',

    'Mahito',

    'Jogo',

    'Hanami',

    'Dagon',

    'Choso',

    'Eso',

    'Kechizu',

    'Kurourushi',

    'Rika Orimoto',

]

#*============*

MHA = [

    'Izuku Midoriya (Deku)',

    'Katsuki Bakugo (Great Explosion Murder God Dynamight)',

    'Ochaco Uraraka (Uravity)',

    'Shoto Todoroki (Shoto)',

    'Tenya Ida (Ingenium)',

    'All Might (Toshinori Yagi)',

    'Tomura Shigaraki (Tenko Shimura)',

    'All For One',

    'Eijiro Kirishima (Red Riot)',

    'Tsuyu Asui (Froppy)',

    'Momo Yaoyorozu (Creati)',

    'Fumikage Tokoyami (Tsukuyomi)',

    'Kyoka Jiro (Earphone Jack)',

    'Mina Ashido (Pinky)',

    'Denki Kaminari (Chargebolt)',

    'Mezo Shoji (Tentacole)',

    'Hanto Sero (Cellophane)',

    'Mashirao Ojiro (Tailman)',

    'Minoru Mineta (Grape Juice)',

    'Toru Hagakure (Invisible Girl)',

    'Koji Koda (Anima)',

    'Rikido Sato (Sugarman)',

    'Yuga Aoyama (Cant Stop Twinkling)',

    'Mirio Togata (Lemillion - The Big 3)',

    'Mei Hatsume (Support Course)',

    'Itsuka Kendo (Battle Fist)',

    'Neito Monoma (Phantom Thief)',

    'Endeavor (Enji Todoroki)',

    'Hawks (Keigo Takami)',

    'Eraser Head (Shota Aizawa)',

    'Best Jeanist (Tsunagu Hakamada)',

    'Gran Torino (Sorahiko Torino)',

    'Mirko (Rumi Usagiyama)',

    'Present Mic (Hizashi Yamada)',

    'Midnight (Nemuri Kayama)',

    'Nezu (Principal Nezu)',

    'Recovery Girl (Chiyo Shuzenji)',

    'Kamui Woods (Shinji Nishiya)',

    'Mt. Lady (Yu Takeyama)',

    'Fat Gum (Taishiro Toyomitsu)',

    'Sir Nighteye (Mirai Sasaki)',

    'Gang Orca (Kugo Sakamata)',

    'Dabi (Toya Todoroki)',

    'Himiko Toga',

    'Twice (Jin Bubaigawara)',

    'Kurogiri (Oboro Shirakumo)',

    'Overhaul (Kai Chisaki)',

    'Stain (Chizome Akaguro)',

    'Lady Nagant (Kaina Tsutsumi)',

    'Gentle Criminal (Danjuro Tobita)',

    'Muscular (Goto Imasuji)',

    'Eri',

]

#*============*

OPM = [

    'Saitama',

    'Genos',

    'Tatsumaki',

    'Fubuki',

    'Bang',

    'Garou',

    'King',

    "Speed-o'-Sound Sonic",

    'Atomic Samurai',

    'Metal Bat',

    'Child Emperor',

    'Zombieman',

    'Flashy Flash',

    'Mumen Rider',

    'Blast',

    'Bofoi',

    'Metal Knight',

    'Drive Knight',

    'Pig God',

    'Watchdog Man',

    'Superalloy Darkshine',

    'Tanktop Master',

    'Puri-Puri Prisoner',

    'Sweet Mask',

    'Amai Mask',

    'Boros',

    'Orochi',

    'Psykos',

    'Monster God',

    'Empty Void',

    'Suiryu',

    'Charanko',

    'Bomb',

    'Dr. Kuseno',

    'Dr. Genus',

    'Armored Gorilla',

    'Carnage Kabuto',

    'Vaccine Man',

    'Deep Sea King',

    'Melzargard',

    'Geryuganshoop',

    'Groribas',

    'Crablante',

    'Stinger',

    'Lightning Max',

    'Sneck',

    'Iaian',

    'Spring Mustachio',

    'Golden Ball',

    'Death Gatling',

    'Smile Man',

    'Blue Fire',

    'Heavy Tank Fundoshi',

    'Tanktop Tiger',

    'Tanktop Black Hole',

    'Gouketsu',

    'Elder Centipede',

    'Black Sperm',

    'Homeless Emperor',

    'Fuhrer Ugly',

    'Gums',

    'Nyan',

    'Phoenix Man',

    'Overgrown Rover',

    'Evil Natural Water',

    'G4',

    'G5',

    'Awakened Cockroach',

    'Bakuzan',

    'Choze',

    'Marshall Gorilla',

    'Rhino Wrestler',

    'Royal Ripper',

    'Bug God',

    'Pure Blood',

    'Freezer Man',

    'Slacker Sid',

    'Subterranean King',

    'Sky King',

    'Ancient King',

    'Deep Sea King',

    'Pluton',

    'Marugori',

    'Beefcake',

    'Fukegao',

    'Hammerhead',

    'Sonic',

    'Tareo',

    'Zenko',

]

#*============*

SL = [

    'Sung Jin-Woo (The Shadow Monarch)',

    "Sung Il-Hwan (Jin-Woo's Father / Vessel of the Rulers)",

    'Cha Hae-In (The Radiant Sword / S-Rank Hunter)',

    "Yoo Jin-Ho (Jin-Woo's Loyal Vice-Guild Master)",

    'Go Gun-Hee (The Association President / Sky Above the Sky)',

    'Thomas Andre (The Goliath / National Level Hunter)',

    'Liu Zhigang (The Hero of China / National Level Hunter)',

    'Christopher Reed (National Level Hunter / Vessel of the Rulers)',

    'Siddharth Bachchan (National Level Hunter)',

    'Jonas (National Level Hunter of Brazil)',

    'Choi Jong-In (The Ultimate Soldier / Master of Hunters Guild)',

    'Baek Yoon-Ho (The White Tiger / Guild Master)',

    'Min Byung-Gu (The Retired S-Rank Healer)',

    'Lim Tae-Gyu (Master of Fiend Guild)',

    'Ma Dong-Wook (Master of Fame Guild)',

    'Yoo Myung-Han (Chairman of Yoojin Construction)',

    "Park Heeo-Jin (B-Rank Mage / Jin-Woo's Early Party Member)",

    "Lee Ju-Hee (B-Rank Healer / Jin-Woo's Friend from the Double Dungeon)",

    'Song Chi-Yeul (C-Rank Mage / The Veteran Sword Elder)',

    'Kim Chul (Iron / High Orc Shadow / A-Rank Tanker)',

    'Hwang Dong-Su (Greed / S-Rank Traitor / Scavenger Guild)',

    "Hwang Dong-Suk (C-Rank Villain / Dong-Su's Brother)",

    'Woo Jin-Chul (The Surveillance Chief / Later Association President)',

    'Han Jae-Gu (A-Rank Hunter of White Tiger Guild)',

    'Kim Gu-Bhim (A-Rank Hunter of White Tiger Guild)',

    'Park Jong-Soo (Master of Knights Guild)',

    'Jeong Yun-Ki (Vice-Master of Knights Guild)',

    "Goto Ryuji (Japan's Strongest S-Rank Hunter)",

    'Reiji Sugimoto (Japanese S-Rank Hunter)',

    'Akari Shimizu (Japanese S-Rank Healer)',

    'Kenzo Tanaka (Japanese S-Rank Brawler)',

    'Kanae Tawata (Japanese S-Rank Assassin)',

    'Minoru Hoshino (Japanese S-Rank Hunter)',

    'Kei (Japanese S-Rank Ice Mage)',

    'Mari Ishida (Japanese S-Rank Hunter)',

    'Kumamoto (Japanese S-Rank Berserker)',

    'Yuri Orloff (The Russian S-Rank Barrier King)',

    "Lennart Niermann (Germany's Top S-Rank Hunter)",

    "Laura (Thomas Andre's Personal Manager)",

    'Selner (The Prophet / Madam Selner)',

    'David Brennon (Director of the Federal Bureau of Hunters)',

    'Gina (American S-Rank Hunter)',

    'Norris (American S-Rank Hunter)',

    'Brent (American S-Rank Hunter)',

    "Jong-Soo's Secretary (Knights Guild Staff)",

    "Sung Jin-Ah (Jin-Woo's Younger Sister)",

    "Park Kyung-Hye (Jin-Woo's Mother)",

    "Yoo Jin-Hee (Jin-Ho's Older Sister)",

    "Han Song-Yi (E-Rank Hunter / Jin-Ah's Friend)",

    "The Architect (The Creator of the System / Ashborn's Servant)",

    'Ashborn (The Original Shadow Monarch)',

    'Antares (The Monarch of Destruction / King of Dragons)',

    'Rakan (The Monarch of Fangs / King of Beasts)',

    'Baruka (The Monarch of White Flames / King of Snow Folk)',

    'Querehsha (The Monarch of Plagues / Queen of Insects)',

    'Yogumunt (The Monarch of Transmutation / King of Demonic Spectres)',

    'Tarnak (The Monarch of Iron Body / King of Monstrous Humanoids)',

    'Sillad (The Monarch of Frost / King of Snow Folk)',

    'Legia (The Monarch of the Beginning / King of Giants)',

    'Absolute Being (The Creator Creator of Monarchs and Rulers)',

    "Igris (The Blood Red Commander / Jin-Woo's Shadow)",

    "Beru (The Shadow Ant King / Jin-Woo's Shadow)",

    "Tusk (The High Orc Shaman Shadow / Jin-Woo's Shadow)",

    "Tank (The Ice Bear Shadow / Jin-Woo's Shadow)",

    "Kaisel (The Shadow Wyvern / Jin-Woo's Mount)",

    "Jima (The Naga Shadow / Jin-Woo's Shadow)",

    "Bellion (The Grand Marshal / Ashborn's Original Shadow)",

    "Kamish (The Shadow Dragon / Humanity's Greatest Calamity)",

]

#*============*

DL = [

    'Tanjirō Kamado',

    'Nezuko Kamado',

    'Zenitsu Agatsuma',

    'Inosuke Hashibira',

    'Kanao Tsuyuri',

    'Genya Shinazugawa',

    'Giyū Tomioka (Water Hashira)',

    'Shinobu Kochō (Insect Hashira)',

    'Kyōjurō Rengoku (Flame Hashira)',

    'Tengen Uzui (Sound Hashira)',

    'Mitsuri Kanroji (Love Hashira)',

    'Muichirō Tokitō (Mist Hashira)',

    'Gyōmei Himejima (Stone Hashira)',

    'Obanai Iguro (Serpent Hashira)',

    'Sanemi Shinazugawa (Wind Hashira)',

    'Muzan Kibutsuji (Demon King)',

    'Kokushibō (Upper Moon One)',

    'Dōma (Upper Moon Two)',

    'Akaza (Upper Moon Three)',

    'Hantengu (Upper Moon Four)',

    'Gyokko (Upper Moon Five)',

    'Gyūtarō (Upper Moon Six)',

    'Daki (Upper Moon Six)',

    'Kaigaku (Upper Moon Six)',

    'Nakime (Upper Moon Four)',

    'Enmu (Lower Moon One)',

    'Rui (Lower Moon Five)',

    'Kyōgai (Former Lower Moon Six)',

    'Sakonji Urokodaki (Former Water Hashira)',

    'Jigorō Kuwajima (Former Roaring Hashira)',

    'Shinjurō Rengoku (Former Flame Hashira)',

    'Kanae Kochō (Former Flower Hashira)',

    'Yoriichi Tsugikuni (Creator of Sun Breathing)',

    'Tamayo (Demon Doctor)',

    "Yushirō (Tamayo's Assistant)",

    'Murata (Demon Slayer Corps Member)',

    'Aoi Kanzaki (Butterfly Mansion Helper)',

    'Sumi Nakahara (Butterfly Mansion Helper)',

    'Kiyo Terauchi (Butterfly Mansion Helper)',

    'Naho Takada (Butterfly Mansion Helper)',

    'Sabo (Demon Slayer Cadet)',

    'Makomo (Demon Slayer Cadet)',

    'Hotaru Haganezuka (Swordsmith)',

    'Kozo Kanamori (Swordsmith)',

    'Kotetsu (Swordsmith Village Resident)',

    'Tecchin Tecchikawahara (Swordsmith Village Chief)',

    "Hinatsuru (Tengen's Wife)",

    "Makuo (Tengen's Wife)",

    "Suma (Tengen's Wife)",

    'Kagaya Ubuyashiki (Master of the Mansion)',

    "Amane Ubuyashiki (Kagaya's Wife)",

    "Kiriya Ubuyashiki (Kagaya's Son)",

    "Kanata Ubuyashiki (Kagaya's Daughter)",

    "Kuina Ubuyashiki (Kagaya's Daughter)",

    "Nichika Ubuyashiki (Kagaya's Daughter)",

    "Hinaki Ubuyashiki (Kagaya's Daughter)",

    'Susamaru (Temari Demon)',

    'Yahaba (Arrow Demon)',

    'Spider Demon Mother (Spider Family)',

    'Spider Demon Father (Spider Family)',

    'Spider Demon Brother (Spider Family)',

    'Spider Demon Sister (Spider Family)',

    'Hand Demon (Final Selection Demon)',

    "Kie Kamado (Tanjirō's Mother)",

    "Takeo Kamado (Tanjirō's Brother)",

    "Hanako Kamado (Tanjirō's Sister)",

    "Shigeru Kamado (Tanjirō's Brother)",

    "Rokuta Kamado (Tanjirō's Brother)",

    "Tanjūrō Kamado (Tanjirō's Father)",

    "Senjūrō Rengoku (Kyōjurō's Brother)",

    "Ruka Rengoku (Kyōjurō's Mother)",

    "Kotoha Hashibira (Inosuke's Mother)",

    "Yuichirō Tokitō (Muichirō's Twin Brother)",

    "Tsutako Tomioka (Giyū's Sister)",

]

#*============*

BL = [

    'Yoichi Isagi',

    'Meguru Bachira',

    'Rensuke Kunigami',

    'Hyoma Chigiri',

    'Rin Itoshi',

    'Sae Itoshi',

    'Seishiro Nagi',

    'Reo Mikage',

    'Zantetsu Tsurugi',

    'Shouei Barou',

    'Gin Gagamaru',

    'Jingo Raichi',

    'Gurimu Igarashi',

    'Asahi Naruhaya',

    'Wataru Kuon',

    'Okuhito Iemon',

    'Yudai Imamura',

    'Ryosuke Kira',

    'Jin Kiyora',

    'Ikki Niko',

    'Junichi Wanima',

    'Keisuke Wanima',

    'Ryusei Shidou',

    'Tabito Karasu',

    'Eita Otoya',

    'Kenyu Yukimiya',

    'Yo Hiyori',

    'Nijiro Nanase',

    'Kurona Ranze',

    'Aoshi Tokimitsu',

    'Jubei Aryu',

    'Anri Teieri',

    'Jinpachi Ego',

    'Yasuhito Fukaku',

    'Oliver Aiku',

    'Shuto Sendo',

    'Kazuma Niou',

    'Teppei Neru',

    'Kento Cho',

    'Teru Kitsunezato',

    'Itsuki Wakatsuki',

    'Haru Hayate',

    'Taiga Tsunzaki',

    'Miroku Darai',

    'Shingen Tanaka',

    'Noel Noa',

    'Chris Prince',

    'Lavinho',

    'Marc Snuffy',

    'Julian Loki',

    'Michael Kaiser',

    'Alexis Ness',

    'Benedict Grim',

    'Erik Gesner',

    'Mensah',

    'Birkenstock',

    'Agi',

    'Don Lorenzo',

    'Drago',

    'Charles Chevalier',

    'Leonardo Luna',

    'Pablo Cavasoz',

    'Adam Blake',

    'Dada Silva',

]

#*============*

ANIME_LISTS = {

    "AOT": AOT,

    "JJK": JJK,

    "MHA": MHA,

    "OPM": OPM,

    "SL": SL,

    "DL": DL,

    "BL": BL,

}

#*============*

def register_anime(short_name, characters):

    """Register an anime character list so it is included in every new shuffled pool.

    Example:

        register_anime("OP", OP)

    """

    key = short_name.strip().upper()

    if not key:

        raise ValueError("Anime name cannot be empty.")

    if key in ANIME_LISTS:

        raise ValueError(f"Anime list '{key}' is already registered.")

    if isinstance(characters, str):

        raise TypeError("characters must be a list of character names, not one string.")

    cleaned = [name.strip() for name in characters if isinstance(name, str) and name.strip()]

    if not cleaned:

        raise ValueError("Add at least one character name to the list.")

    ANIME_LISTS[key] = cleaned

#


# Expanded rosters: identifying descriptions may contain source-material spoilers.
# Pokemon names and types: https://github.com/PokeAPI/pokeapi/tree/master/data/v2/csv
ANIME_LISTS.update({'DN': ['Light Yagami: Kira / Death Note strategist',
        'L Lawliet: Detective pursuing Kira',
        'Ryuk: Shinigami who drops the notebook',
        'Misa Amane: Second Kira / Shinigami Eyes',
        "Rem: Misa's protective Shinigami",
        "Near: SPK leader / L's successor",
        "Mello: L's rival successor",
        "Teru Mikami: Prosecutor / Kira's chosen follower",
        "Kiyomi Takada: News presenter / Kira's spokesperson",
        "Soichiro Yagami: Task force chief / Light's father",
        'Touta Matsuda: Japanese task force investigator',
        'Shuichi Aizawa: Japanese task force investigator',
        'Kanzo Mogi: Japanese task force investigator',
        'Hideki Ide: Japanese task force investigator',
        'Hirokazu Ukita: Early task force investigator',
        "Watari: L's handler / Wammy's House founder",
        'Naomi Misora: Former FBI agent / investigator',
        'Raye Penber: FBI agent investigating Light',
        'Kyosuke Higuchi: Yotsuba Kira',
        'Reiji Namikawa: Yotsuba executive',
        'Hitoshi Demegawa: Sakura TV director',
        "Matt: Mello's ally / surveillance specialist",
        'Stephen Gevanni: SPK agent / notebook investigator',
        'Halle Lidner: SPK agent / bodyguard',
        'Anthony Rester: SPK agent',
        'Sidoh: Shinigami seeking his notebook',
        'Gelus: Shinigami who saved Misa',
        "Sayu Yagami: Light's sister / kidnapping victim",
        "Sachiko Yagami: Light's mother"],
 'SG': ['Rintaro Okabe: Hououin Kyouma / Reading Steiner',
        'Kurisu Makise: Neuroscientist / time machine researcher',
        "Mayuri Shiina: Lab member / Okabe's childhood friend",
        'Itaru Hashida: Daru / expert hacker',
        'Suzuha Amane: Time traveller / part-time warrior',
        'Faris NyanNyan: Rumiho Akiha / maid cafe owner',
        'Luka Urushibara: Shrine attendant / lab member',
        'Moeka Kiryu: Rounder / text-message specialist',
        'Yugo Tennouji: Mr. Braun / CRT shop owner',
        "Nae Tennouji: Mr. Braun's daughter",
        "Shouichi Makise: Dr. Nakabachi / Kurisu's father",
        'Maho Hiyajo: Neuroscientist / Amadeus researcher',
        'Alexis Leskinen: Professor / time travel researcher',
        'Judy Reyes: Neuroscientist / research rival',
        "Kagari Shiina: Mayuri's adopted daughter / time traveller",
        "Yuki Amane: Cosplayer / Suzuha's mother"],
 'NAR': ['Naruto Uzumaki: Nine-Tails jinchuriki / Seventh Hokage',
         'Sasuke Uchiha: Sharingan and Rinnegan / Team 7',
         'Sakura Haruno: Medical ninja / superhuman strength',
         'Kakashi Hatake: Copy Ninja / Sixth Hokage',
         'Sai: Ink beast techniques / Root operative',
         'Yamato: Wood Release / Team 7 captain',
         'Hinata Hyuga: Byakugan / Gentle Fist',
         'Neji Hyuga: Hyuga prodigy / Byakugan',
         'Rock Lee: Taijutsu specialist / Eight Gates',
         'Might Guy: Taijutsu master / Eight Gates',
         'Tenten: Ninja weapon specialist',
         'Shikamaru Nara: Shadow techniques / tactical genius',
         'Ino Yamanaka: Mind Transfer / sensory ninja',
         'Choji Akimichi: Expansion techniques / butterfly mode',
         'Asuma Sarutobi: Chakra blades / Team 10 leader',
         "Kiba Inuzuka: Beast mimicry / Akamaru's partner",
         "Akamaru: Ninja hound / Kiba's partner",
         'Shino Aburame: Chakra-eating insects',
         'Kurenai Yuhi: Genjutsu specialist',
         "Konohamaru Sarutobi: Rasengan / Hiruzen's grandson",
         "Iruka Umino: Academy teacher / Naruto's mentor",
         'Jiraiya: Toad Sage / Legendary Sannin',
         'Tsunade: Medical master / Fifth Hokage',
         'Orochimaru: Snake techniques / Legendary Sannin',
         'Kabuto Yakushi: Medical ninja / Sage Mode',
         "Shizune: Medical ninja / Tsunade's assistant",
         'Hashirama Senju: Wood Release / First Hokage',
         'Tobirama Senju: Flying Raijin / Second Hokage',
         'Hiruzen Sarutobi: Professor / Third Hokage',
         'Minato Namikaze: Yellow Flash / Fourth Hokage',
         'Kushina Uzumaki: Chakra chains / Nine-Tails host',
         'Danzo Shimura: Root leader / stolen Sharingan',
         'Itachi Uchiha: Akatsuki / Mangekyo Sharingan',
         'Shisui Uchiha: Kotoamatsukami / Body Flicker',
         'Madara Uchiha: Uchiha legend / Rinnegan',
         'Obito Uchiha: Kamui / masked Akatsuki leader',
         'Nagato: Rinnegan / Six Paths of Pain',
         'Yahiko: Original Akatsuki founder',
         'Konan: Paper techniques / Akatsuki',
         'Kisame Hoshigaki: Samehada / chakra absorption',
         'Deidara: Explosive clay / Akatsuki',
         'Sasori: Human puppets / Akatsuki',
         'Hidan: Jashin ritual / immortality',
         'Kakuzu: Five hearts / thread techniques',
         "Black Zetsu: Kaguya's will / manipulator",
         'White Zetsu: Infiltration / plant-like clone',
         'Gaara: Sand manipulation / Fifth Kazekage',
         'Temari: Wind fan / Sand siblings',
         'Kankuro: Puppet master / Sand siblings',
         'Chiyo: Puppet master / medical expert',
         'Rasa: Gold Dust / Fourth Kazekage',
         'Killer B: Eight-Tails jinchuriki / swordsman',
         'A: Lightning Armour / Fourth Raikage',
         'Darui: Storm Release / Cloud ninja',
         'C: Cloud sensor / medical ninja',
         'Mei Terumi: Lava and Boil Release / Fifth Mizukage',
         'Ao: Byakugan / Mist sensor',
         'Chojuro: Hiramekarei swordsman',
         'Onoki: Particle Style / Third Tsuchikage',
         'Kurotsuchi: Lava Release / Stone ninja',
         'Akatsuchi: Stone ninja / golem techniques',
         'Mu: Particle Style / Second Tsuchikage',
         'Gengetsu Hozuki: Clam illusions / Second Mizukage',
         'Third Raikage: Lightning spear / exceptional endurance',
         "Zabuza Momochi: Demon of the Mist / executioner's blade",
         'Haku: Ice Release / crystal ice mirrors',
         'Suigetsu Hozuki: Hydrification / Team Taka',
         'Karin Uzumaki: Sensory ninja / healing bite',
         'Jugo: Natural energy transformation / Team Taka',
         'Kimimaro: Bone manipulation / Kaguya clan',
         'Tayuya: Flute genjutsu / Sound Four',
         'Kidomaru: Spider techniques / Sound Four',
         'Sakon and Ukon: Body merging / Sound Four',
         'Jirobo: Earth Release / Sound Four',
         'Dosu Kinuta: Sound gauntlet / Sound genin',
         'Zaku Abumi: Air pressure attacks / Sound genin',
         'Kin Tsuchi: Bell genjutsu / Sound genin',
         'Hanzo: Salamander summoner / Rain leader',
         'Mifune: Land of Iron samurai commander',
         "Dan Kato: Spirit Transformation / Tsunade's partner",
         "Nawaki: Tsunade's younger brother",
         "Sakumo Hatake: White Fang / Kakashi's father",
         'Fugaku Uchiha: Uchiha clan head',
         "Mikoto Uchiha: Sasuke and Itachi's mother",
         "Izuna Uchiha: Madara's brother / Mangekyo Sharingan",
         'Shikaku Nara: Allied forces strategist',
         'Inoichi Yamanaka: Intelligence division leader',
         'Choza Akimichi: Akimichi clan head',
         'Hiashi Hyuga: Hyuga clan head',
         "Hizashi Hyuga: Neji's father",
         "Anko Mitarashi: Snake techniques / Orochimaru's student",
         'Ibiki Morino: Interrogation specialist',
         'Hayate Gekko: Leaf swordsman / exam proctor',
         'Genma Shiranui: Leaf special jonin',
         'Yugao Uzuki: ANBU swordswoman',
         'Yugito Nii: Two-Tails jinchuriki',
         'Yagura Karatachi: Three-Tails jinchuriki / Fourth Mizukage',
         'Roshi: Four-Tails jinchuriki / Lava Release',
         'Han: Five-Tails jinchuriki / steam armour',
         'Utakata: Six-Tails jinchuriki / bubble techniques',
         'Fu: Seven-Tails jinchuriki',
         'Shukaku: One-Tail / sand and sealing',
         'Matatabi: Two-Tails / blue flames',
         'Isobu: Three-Tails / armoured turtle',
         'Son Goku: Four-Tails / lava',
         'Kokuo: Five-Tails / steam',
         'Saiken: Six-Tails / corrosive slug',
         'Chomei: Seven-Tails / flying beetle',
         'Gyuki: Eight-Tails / octopus ox',
         'Kurama: Nine-Tails / immense chakra',
         'Hagoromo Otsutsuki: Sage of Six Paths',
         "Hamura Otsutsuki: Hagoromo's brother / moon ancestor",
         'Kaguya Otsutsuki: Chakra progenitor / dimensional powers',
         "Indra Otsutsuki: Hagoromo's elder son",
         "Asura Otsutsuki: Hagoromo's younger son",
         'Fukasaku: Elder toad / Sage Mode teacher',
         'Shima: Elder toad / sound genjutsu',
         'Gamabunta: Giant toad chief',
         'Katsuyu: Healing slug summon',
         'Manda: Giant snake summon'],
 'TG': ['Ken Kaneki: One-Eyed Ghoul / Haise Sasaki',
        'Touka Kirishima: Rabbit / Anteiku waitress',
        "Rize Kamishiro: Binge Eater / Kaneki's donor",
        "Hideyoshi Nagachika: Hide / Kaneki's perceptive friend",
        'Yoshimura: Anteiku manager / non-killing Owl',
        'Eto Yoshimura: One-Eyed Owl / author Sen Takatsuki',
        'Shu Tsukiyama: Gourmet / ghoul aristocrat',
        'Nishiki Nishio: Serpent / university ghoul',
        'Hinami Fueguchi: Dual kagune / young Anteiku ally',
        'Ayato Kirishima: Black Rabbit / Aogiri executive',
        'Renji Yomo: Raven / Anteiku protector',
        'Uta: Mask maker / Clowns member',
        'Itori: Information broker / Clowns member',
        'Roma Hoito: Clowns founder / Dodgy Mother',
        'Nico: Clowns member / regenerative ghoul',
        'Donato Porpora: Priest / Clowns member',
        'Yakumo Oomori: Jason / Yamori',
        'Naki: White Suits leader',
        'Tatara: Aogiri leader / flame kakuja',
        'Noro: Aogiri ghoul / extreme regeneration',
        'Seidou Takizawa: Investigator turned artificial Owl',
        'Koutarou Amon: Investigator / artificial half-ghoul',
        "Akira Mado: Quinque specialist / Kureo's daughter",
        'Kureo Mado: Ghoul investigator / quinque collector',
        'Kishou Arima: CCG Reaper / elite investigator',
        'Juuzou Suzuya: Knife specialist / special class investigator',
        "Yukinori Shinohara: Juuzou's mentor / Arata armour",
        'Iwao Kuroiwa: Special class investigator',
        'Kousuke Houji: Special class investigator',
        "Take Hirako: Arima's former subordinate",
        'Itsuki Marude: CCG commander / strategist',
        'Kuki Urie: Quinx squad leader',
        'Ginshi Shirazu: Quinx / ukaku user',
        'Tooru Mutsuki: Quinx / investigator',
        'Saiko Yonebayashi: Quinx / powerful kagune',
        'Hairu Ihei: Half-human investigator',
        'Shio Ihei: Zero Squad / Garden child',
        'Rikai Souzu: Zero Squad / Garden child',
        'Yusa Arima: Zero Squad / Garden child',
        'Nimura Furuta: Souta / CCG manipulator',
        'Matasaka Kamishiro: Matasaka Kamishiro / martial artist',
        'Karren von Rosewald: Kanae / Tsukiyama family servant',
        'Matsumae: Tsukiyama family guard',
        "Mirumo Tsukiyama: Shu's father / ghoul patriarch",
        "Kimi Nishino: Researcher / Nishiki's partner",
        'Akihiro Kanou: Surgeon / artificial ghoul experiments',
        'Kurona Yasuhisa: Artificial one-eyed ghoul',
        "Nashiro Yasuhisa: Kurona's twin / artificial ghoul",
        'Kaya Irimi: Black Dog / Anteiku fighter',
        'Enji Koma: Devil Ape / Anteiku fighter',
        "Ryouko Fueguchi: Hinami's mother",
        "Arata Kirishima: Corpse Collector / Touka's father",
        "Ichika Kaneki: Kaneki and Touka's daughter"],
 'HXH': ['Gon Freecss: Enhancement Nen / fishing rod hunter',
         'Killua Zoldyck: Assassin / Godspeed lightning',
         'Kurapika: Scarlet Eyes / Chain Jail',
         'Leorio Paradinight: Aspiring doctor / emission punch',
         'Hisoka Morow: Bungee Gum / magician',
         'Illumi Zoldyck: Needle manipulation / assassin',
         "Ging Freecss: Ruins Hunter / Gon's father",
         'Isaac Netero: Hunter chairman / Hundred-Type Guanyin',
         'Beyond Netero: Dark Continent expedition leader',
         'Silva Zoldyck: Zoldyck patriarch / assassin',
         'Zeno Zoldyck: Dragon Head / master assassin',
         "Alluka Zoldyck: Nanika's host / Killua's sister",
         'Nanika: Wish-granting entity',
         'Kalluto Zoldyck: Paper manipulation / Phantom Troupe',
         'Milluki Zoldyck: Inventor / Zoldyck sibling',
         'Kikyo Zoldyck: Zoldyck matriarch',
         'Maha Zoldyck: Elder Zoldyck assassin',
         'Gotoh: Coin bullets / Zoldyck butler',
         'Canary: Apprentice Zoldyck butler',
         "Tsubone: Rider's High / veteran butler",
         "Amane: Zoldyck butler / Tsubone's granddaughter",
         'Chrollo Lucilfer: Skill Hunter / Phantom Troupe leader',
         'Machi Komacine: Nen threads / Phantom Troupe',
         'Nobunaga Hazama: Swordsman / Phantom Troupe',
         'Feitan Portor: Pain Packer / Phantom Troupe',
         'Phinks Magcub: Ripper Cyclotron / Phantom Troupe',
         'Franklin Bordeau: Double Machine Gun / Phantom Troupe',
         'Shizuku Murasaki: Blinky vacuum / Phantom Troupe',
         'Shalnark: Black Voice / Phantom Troupe',
         'Pakunoda: Memory bullets / Phantom Troupe',
         'Uvogin: Big Bang Impact / Phantom Troupe',
         'Bonolenov Ndongo: Battle Cantabile / Phantom Troupe',
         'Kortopi: Gallery Fake / Phantom Troupe',
         'Biscuit Krueger: Nen master / muscular true form',
         'Wing: Shingen-ryu teacher',
         "Zushi: Wing's young Nen student",
         "Kite: Crazy Slots / Ging's student",
         'Razor: Greed Island game master / emitter',
         'Palm Siberia: Crystal divination / Black Widow',
         'Knuckle Bine: Hakoware / Beast Hunter',
         'Shoot McMahon: Hotel Rafflesia / Beast Hunter',
         'Morel Mackernasey: Deep Purple smoke / Sea Hunter',
         'Knov: Hide and Seek / portal rooms',
         'Meruem: Chimera Ant King',
         'Neferpitou: Royal Guard / Doctor Blythe',
         'Shaiapouf: Royal Guard / butterfly scales',
         'Menthuthuyoupi: Royal Guard / shapeshifting rage',
         "Chimera Ant Queen: Mother of Meruem's colony",
         'Colt: Chimera Ant squadron leader',
         'Ikalgo: Octopus ant / corpse puppetry',
         'Meleoron: Perfect Plan / invisibility',
         'Zazan: Scorpion ant queen',
         'Leol: Rental Pod / lion ant',
         'Cheetu: Super-speed cheetah ant',
         'Welfin: Missileman / wolf ant',
         'Bloster: Lobster ant / aura bullets',
         'Rammot: Rabbit ant / enhancer',
         'Flutter: Dragonfly ant / reconnaissance',
         'Komugi: Gungi prodigy',
         'Neon Nostrade: Lovely Ghostwriter / fortune teller',
         'Light Nostrade: Mafia family boss',
         'Melody: Music Hunter / exceptional hearing',
         'Basho: Haiku Nen / bodyguard',
         'Baise: Instant Lover / bodyguard',
         'Squala: Dog manipulation / bodyguard',
         'Dalzollene: Nostrade bodyguard captain',
         'Genthru: Bomber / Countdown',
         'Sub: Bomber accomplice',
         'Bara: Bomber accomplice',
         'Tsezguerra: Single-Star Jackpot Hunter',
         'Goreinu: Gorilla Nen beasts',
         'Hanzo: Ninja / Hunter examinee',
         'Pokkle: Rainbow arrows / Hunter',
         'Ponzu: Bee handler / examinee',
         'Tonpa: Rookie Crusher',
         'Satotz: Hunter exam proctor',
         'Menchi: Gourmet Hunter',
         'Buhara: Gourmet Hunter',
         'Lippo: Blacklist Hunter / Trick Tower examiner',
         'Beans: Hunter Association secretary',
         'Pariston Hill: Former vice-chairman / political schemer',
         'Cheadle Yorkshire: Disease Hunter / Zodiac Dog',
         'Mizaistom Nana: Crime Hunter / Zodiac Ox',
         'Botobai Gigante: Terrorist Hunter / Zodiac Dragon',
         'Kanzai: Treasure Hunter / Zodiac Tiger',
         'Gel: Poison Hunter / Zodiac Snake',
         'Piyon: Paleograph Hunter / Zodiac Rabbit',
         'Saccho Kobayakawa: Double-Star Hunter / Zodiac Horse',
         'Ginta: Poacher Hunter / Zodiac Sheep',
         'Saiyu: Bounty Hunter / Zodiac Monkey',
         'Cluck: Botanical Hunter / Zodiac Chicken',
         'Tserriednich Hui Guo Rou: Fourth Kakin prince / specialist Nen',
         'Benjamin Hui Guo Rou: First Kakin prince / Benjamin Baton',
         "Camilla Hui Guo Rou: Second Kakin prince / Cat's Name",
         'Halkenburg Hui Guo Rou: Ninth Kakin prince / collective aura',
         "Woble Hui Guo Rou: Fourteenth Kakin prince / Kurapika's ward",
         "Oito Hui Guo Rou: Kakin queen / Woble's mother"],
 'SAO': ['Kirito: Kazuto Kirigaya / Black Swordsman',
         'Asuna: Asuna Yuuki / Flash swordswoman',
         'Leafa: Suguha Kirigaya / Sylph swordswoman',
         'Sinon: Shino Asada / sniper',
         "Yui: Mental health AI / Kirito's adopted daughter",
         'Klein: Ryotaro Tsuboi / samurai guild leader',
         'Agil: Andrew Gilbert Mills / axe fighter and merchant',
         'Lisbeth: Rika Shinozaki / blacksmith',
         'Silica: Keiko Ayano / beast tamer',
         "Pina: Silica's feathered dragon",
         'Akihiko Kayaba: Heathcliff / SAO creator',
         'Nobuyuki Sugou: Oberon / Fairy King',
         'Yuuki Konno: Absolute Sword / Sleeping Knights',
         "Aiko Yuuki: Yuuki's sister / Sleeping Knights founder",
         'Siune: Sleeping Knights healer',
         'Jun: Sleeping Knights swordsman',
         'Tecchi: Sleeping Knights tank',
         'Talken: Sleeping Knights lancer',
         'Nori: Sleeping Knights fighter',
         "Eugeo: Blue Rose Sword / Kirito's partner",
         'Alice Zuberg: Integrity Knight / Fragrant Olive Sword',
         'Quinella: Administrator / Axiom Church ruler',
         'Cardinal: Underworld system administrator',
         'Bercouli Synthesis One: Integrity Knight commander',
         'Fanatio Synthesis Two: Heaven-Piercing Sword',
         'Deusolbert Synthesis Seven: Conflagrant Flame Bow',
         'Eldrie Synthesis Thirty-One: Frost Scale Whip',
         'Sheyta Synthesis Twelve: Black Lily Sword',
         'Renly Synthesis Twenty-Seven: Double-Winged Blades',
         'Fizel Synthesis Twenty-Nine: Young Integrity Knight',
         'Linel Synthesis Twenty-Eight: Young Integrity Knight',
         "Selka Zuberg: Alice's sister / apprentice nun",
         'Sortiliena Serlut: Academy elite swordswoman',
         "Ronye Arabel: Kirito's page",
         "Tiese Shtolienen: Eugeo's page",
         'Gabriel Miller: Subtilizer / Emperor Vecta',
         'Vassago Casals: PoH / Laughing Coffin leader',
         'Shouichi Shinkawa: Red-Eyed XaXa / Death Gun',
         'Atsushi Kanamoto: Johnny Black / Laughing Coffin',
         'Kyouji Shinkawa: Spiegel / Death Gun accomplice',
         'Kikuoka Seijirou: Rath official / project leader',
         "Rinko Koujiro: Scientist / Kayaba's former colleague",
         'Takeru Higa: Rath engineer / fluctlight researcher',
         'Iskahn: Pugilist leader / Dark Territory',
         'Lipia Zancale: Dark knight',
         'Shasta: Dark Knights commander',
         'Dee Eye Ell: Dark mage leader',
         'Lilpilin: Orc chief',
         'Eiji: Ordinal Scale swordsman',
         'Yuna: Yuuna Shigemura / idol singer',
         "Tetsuhiro Shigemura: Professor / Yuna's father",
         "Mito: Misumi Tozawa / Asuna's friend",
         'Argo: Information broker / the Rat',
         'Sachi: Moonlit Black Cats member',
         'Diavel: Early raid leader',
         'Kibaou: Aincrad Liberation Force leader'],
 'NGNL': ["Sora: Blank's strategist / Elkia king",
          "Shiro: Blank's calculation prodigy / Elkia queen",
          "Stephanie Dola: Former king's granddaughter",
          'Jibril: Flugel / knowledge collector',
          'Tet: One True God / god of games',
          'Chlammy Zell: Imanity gambler',
          "Fiel Nirvalen: Elf magician / Chlammy's ally",
          'Izuna Hatsuse: Werebeast prodigy / Blood Destruction',
          "Ino Hatsuse: Werebeast diplomat / Izuna's grandfather",
          'Miko: Eastern Union shrine maiden',
          'Riku Dola: Imanity leader during the Great War',
          "Schwi Dola: Ex-Machina / Riku's partner",
          "Couronne Dola: Riku's adoptive sister / Elkia founder",
          "Azril: Flugel leader / Jibril's sister",
          'Artosh: Old Deus / god of war',
          'Einzig: Ex-Machina cluster representative',
          'Emir-Eins: Ex-Machina leader',
          'Plum Stoker: Dhampir magician',
          'Laila Lorelei: Siren queen',
          'Holou: Old Deus / wisdom'],
 'CG': ['Lelouch Lamperouge: Zero / Geass of absolute obedience',
        'Suzaku Kururugi: Lancelot pilot / Knight of Zero',
        'C.C.: Immortal Code bearer / Geass contractor',
        'Kallen Kozuki: Guren pilot / Black Knights ace',
        "Nunnally Lamperouge: Lelouch's sister / Britannian princess",
        'Schneizel el Britannia: Britannian prince / master strategist',
        'Charles zi Britannia: Emperor / memory-altering Geass',
        'Marianne vi Britannia: Knightmare ace / consciousness-transfer Geass',
        'Cornelia li Britannia: Britannian princess / military commander',
        'Euphemia li Britannia: Britannian princess / Special Zone advocate',
        'Clovis la Britannia: Area 11 governor / prince',
        'Rolo Lamperouge: Perception-freezing Geass / Vincent pilot',
        'V.V.: Immortal Code bearer / Geass Order leader',
        'Mao: Mind-reading Geass user',
        'Jeremiah Gottwald: Cyborg / Geass Canceller',
        'Villetta Nu: Britannian officer / Knightmare pilot',
        'Lloyd Asplund: Lancelot engineer',
        'Cecile Croomy: Scientist / Lancelot support',
        'Rakshata Chawla: Guren engineer / Black Knights scientist',
        'Diethard Ried: Media strategist / Black Knights',
        'Kaname Ohgi: Black Knights deputy commander',
        'Kyoshiro Tohdoh: Miracle of Itsukushima / samurai commander',
        'Nagisa Chiba: Four Holy Swords / pilot',
        'Shogo Asahina: Four Holy Swords / pilot',
        'Ryoga Senba: Four Holy Swords / pilot',
        'Kosetsu Urabe: Four Holy Swords / pilot',
        'Shinichiro Tamaki: Black Knights member',
        'Kaguya Sumeragi: Kyoto representative / political leader',
        'Li Xingke: Chinese Federation strategist / Shen Hu pilot',
        'Tianzi: Chinese empress',
        'Hong Gu: Chinese Federation military officer',
        'Gino Weinberg: Knight of Three / Tristan pilot',
        'Anya Alstreim: Knight of Six / Mordred pilot',
        'Bismarck Waldstein: Knight of One / foresight Geass',
        'Luciano Bradley: Knight of Ten / Percival pilot',
        'Dorothea Ernst: Knight of Four',
        'Monica Kruszewski: Knight of Twelve',
        "Shirley Fenette: Ashford student / Lelouch's friend",
        'Milly Ashford: Student council president',
        'Rivalz Cardemonde: Student council member',
        'Nina Einstein: FLEIJA researcher',
        "Sayoko Shinozaki: Ninja maid / Lelouch's ally",
        'Andreas Darlton: Britannian general',
        "Gilbert G.P. Guilford: Cornelia's knight",
        'Bartley Asprius: Britannian general / Code R researcher',
        'Akito Hyuga: W-0 pilot / Geass-affected warrior',
        'Leila Malcal: W-0 commander',
        "Shin Hyuga Shaing: Geass user / Akito's brother",
        'Ashley Ashra: Knightmare pilot / Ashura Squad',
        'Sham na Bith: Zilkhstan ruler / time-loop Geass',
        'Shalio: Zilkhstan warrior king'],
 'TEN': ['Rimuru Tempest: Reincarnated slime / Tempest ruler',
         "Ciel: Manas / Rimuru's evolved analytical partner",
         'Veldora Tempest: Storm Dragon',
         'Benimaru: Oni general / flame swordsman',
         'Shuna: Oni princess / magic and weaving',
         'Shion: Oni secretary / giant sword',
         'Souei: Oni spy / shadow techniques',
         'Hakurou: Ogre sword instructor',
         'Kurobe: Ogre blacksmith',
         "Ranga: Tempest wolf / Rimuru's companion",
         'Gobta: Goblin rider / unexpected prodigy',
         'Rigurd: Goblin administrator / Tempest official',
         'Rigur: Goblin patrol captain',
         "Gobzo: Goblin / Shion's subordinate",
         'Geld: Orc lord / Tempest construction chief',
         'Gabiru: Dragonewt / spear fighter',
         "Souka: Dragonewt / Souei's subordinate",
         'Abiru: Lizardman chieftain',
         'Treyni: Dryad / forest guardian',
         "Trya: Dryad / Treyni's sister",
         'Ramiris: Labyrinth fairy / demon lord',
         "Beretta: Demon-possessed automaton / Ramiris's guard",
         "Diablo: Primordial Black / Rimuru's butler",
         'Testarossa: Primordial White / diplomat',
         'Ultima: Primordial Violet / demon subordinate',
         'Carrera: Primordial Yellow / destructive magic',
         'Guy Crimson: Primordial Red / demon lord',
         "Rain: Primordial Blue / Guy's maid",
         "Misery: Primordial Green / Guy's maid",
         'Milim Nava: Dragonoid / demon lord',
         'Luminous Valentine: Vampire ruler / demon lord',
         'Leon Cromwell: Platinum Saber / demon lord',
         'Dino: Sleeping Ruler / fallen angel',
         'Dagruel: Giant king / demon lord',
         'Clayman: Marionette Master / demon lord',
         'Carrion: Beast Master / Eurazania ruler',
         'Frey: Sky Queen / harpy ruler',
         'Albis: Golden Serpent / Beastketeer',
         'Suphia: White Tiger Claw / Beastketeer',
         'Phobio: Black Leopard Fang / Beastketeer',
         "Shizu Izawa: Summoned hero / Ifrit's host",
         'Ifrit: Greater fire spirit',
         'Hinata Sakaguchi: Holy knight commander',
         'Chloe Aubert: Hero / time-related powers',
         "Chronoa: Chloe's alternate personality / hero",
         'Kenya Misaki: Summoned child / swordsman',
         'Ryota Sekiguchi: Summoned child',
         'Gale Gibson: Summoned child / earth spirit',
         'Alice Rondo: Summoned child / puppet control',
         'Yuuki Kagurazaka: Summoned guildmaster / schemer',
         'Kagali: Former demon lord Kazalim / guild official',
         'Laplace: Moderate Harlequin Alliance / jester',
         'Tear: Moderate Harlequin Alliance / jester',
         'Footman: Moderate Harlequin Alliance / jester',
         'Gazel Dwargo: Dwarven king / master swordsman',
         'Kaijin: Dwarven master craftsman',
         'Vesta: Dwarven researcher',
         'Mjollmile: Merchant / Tempest finance official',
         'Youm: Champion / mercenary leader',
         "Mjurran: Majin mage / Youm's partner",
         "Grucius: Lycanthrope / Youm's ally",
         'Razen: Razen / Falmuth court magician',
         'Edmaris: King of Falmuth',
         'Fuze: Blumund guildmaster',
         'Eren: Elen / elven adventurer',
         "Kaval: Adventurer / Eren's companion",
         "Gido: Scout / Eren's companion",
         'Elmesia El-Ru Sarion: Sorcerous Dynasty empress',
         "Elalude: Elven noble / Eren's father",
         'Velzard: White Ice Dragon',
         'Velgrynd: Scorch Dragon',
         'Veldanava: Star-King Dragon / creator',
         'Rudra Nam Ul Nasca: Eastern Emperor / hero',
         'Masayuki: Chosen Hero / luck-based abilities',
         'Michael: Manas / Justice King',
         'Feldway: Primordial angel / phantom leader',
         'Zegion: Insect warrior / labyrinth guardian',
         'Apito: Insect queen / labyrinth guardian',
         'Kumara: Nine-headed beast / labyrinth guardian',
         'Adalman: Undead priest / labyrinth guardian',
         "Albert: Undead swordsman / Adalman's ally",
         "Wenti: Death dragon / Adalman's ally"],
 'BC': ['Asta: Anti-magic swordsman / Black Bulls',
        'Yuno Grinberryall: Wind and star magic / Golden Dawn',
        'Noelle Silva: Water magic / Black Bulls',
        'Yami Sukehiro: Dark magic / Black Bulls captain',
        'Nacht Faust: Shadow magic / devil host',
        'Magna Swing: Fire magic / Soul Chain Deathmatch',
        'Luck Voltia: Lightning magic / battle enthusiast',
        'Finral Roulacase: Spatial magic / transport',
        'Vanessa Enoteca: Thread magic / fate manipulation',
        "Gauche Adlai: Mirror magic / Marie's brother",
        'Grey: Transformation and transmutation magic',
        'Charmy Pappitson: Cotton and food magic',
        'Gordon Agrippa: Poison and curse research',
        'Henry Legolant: Recombination magic / moving base',
        'Zora Ideale: Trap magic / counterattacks',
        'Secre Swallowtail: Nero / sealing magic',
        "Liebe: Anti-magic devil / Asta's partner",
        'Julius Novachrono: Time magic / Wizard King',
        'Lucius Zogratis: Soul magic / Zogratis sibling',
        'William Vangeance: World Tree magic / Golden Dawn captain',
        'Mimosa Vermillion: Plant magic / healing',
        'Klaus Lunettes: Steel magic / Golden Dawn',
        'Langris Vaude: Offensive spatial magic',
        'Letoile Becquerel: Compass magic',
        'David Swallow: Dice magic',
        'Alecdora Sandler: Sand magic',
        'Hamon Caseus: Glass magic',
        'Shiren Tium: Stone magic',
        'Fuegoleon Vermillion: Fire magic / Crimson Lion captain',
        'Mereoleona Vermillion: Fire magic / Hellfire Incarnate',
        'Leopold Vermillion: Fire magic / royal knight',
        'Nozel Silva: Mercury magic / Silver Eagle captain',
        'Nebra Silva: Mist magic / Silva royal',
        'Solid Silva: Water magic / Silva royal',
        "Acier Silva: Steel magic / Noelle's mother",
        'Charlotte Roselei: Briar magic / Blue Rose captain',
        'Sol Marron: Earth magic / Blue Rose',
        'Jack the Ripper: Severing magic / Green Mantis captain',
        'Sekke Bronzazza: Bronze magic / Green Mantis',
        'Rill Boismortier: Painting magic / Aqua Deer captain',
        'Dorothy Unsworth: Dream magic / Coral Peacock captain',
        'Kirsch Vermillion: Cherry blossom magic',
        'Kaiser Granvorka: Vortex magic / Purple Orca captain',
        'Gueldre Poizot: Permeation magic / former captain',
        "Marx Francois: Memory magic / Julius's aide",
        'Owen: Water recovery magic / doctor',
        'Lumiere Silvamillion Clover: Light magic / First Wizard King',
        'Licht: Sword magic / elf leader',
        'Patry: Light magic / Eye of the Midnight Sun',
        'Rhya: Copy magic / Third Eye',
        'Vetto: Beast magic / Third Eye',
        'Fana: Fire magic / Third Eye',
        'Sally: Gel magic / researcher',
        'Rades Spirito: Corpse magic',
        'Valtos: Spatial magic / Midnight Sun',
        'Ralph Niaflem: Fire magic / Spade loyalist',
        'Lolopechka: Water magic / Heart Queen',
        'Undine: Water spirit',
        'Sylph: Bell / wind spirit',
        'Salamander: Fire spirit',
        'Gadjah: Lightning magic / Spirit Guardian',
        'Floga: Fire Spirit Guardian',
        'Potrof: Plant Spirit Guardian',
        'Sarado: Earth Spirit Guardian',
        'Smurik: Wind Spirit Guardian',
        'Mars: Mineral and fire magic / Diamond warrior',
        'Ladros: Magic absorption / Diamond warrior',
        'Lotus Whomalt: Smoke magic / Diamond commander',
        'Morris Libardirt: Modification magic / scientist',
        'Dante Zogratis: Body and gravity magic / Dark Triad',
        'Vanica Zogratis: Blood and curse magic / Dark Triad',
        'Zenon Zogratis: Bone and spatial magic / Dark Triad',
        'Lucifero: Gravity devil',
        'Megicula: Curse devil',
        'Beelzebub: Spatial devil',
        'Zagred: Word Soul magic / devil',
        'Lilith: Demon ice magic',
        'Naamah: Demon fire magic',
        'Lucifugus: Supreme devil',
        'Adrammelech: Supreme devil / underworld',
        'Sister Lily: Water magic / Hage church',
        'Father Orsi: Hage church priest',
        "Rebecca Scarlet: Townswoman / Asta's friend",
        "Marie Adlai: Gauche's sister",
        "Witch Queen: Blood magic / Witches' Forest ruler",
        "Richita: Mana-draining mother / Liebe's guardian",
        'Ichika Yami: Dark magic / Ryuzen Seven',
        'Ryuya Ryudo: Hino shogun / Tengentsu eye',
        'Yosuga Mushogatake: Iron magic / Ryuzen Seven',
        'Fumito Mikuriya: Food magic / Ryuzen Seven',
        'Daizaemon Ooka: Earth magic / Ryuzen Seven',
        'Jozo Hanegatsuji: Wind magic / Ryuzen Seven',
        'Komari Imari: Lightning magic / Ryuzen Seven',
        'Ginnojomorifuyu Kezokaku: Snow magic / Ryuzen Seven'],
 'BLE': ['Ichigo Kurosaki: Substitute Soul Reaper / Zangetsu',
         'Rukia Kuchiki: Sode no Shirayuki / Soul Reaper',
         'Orihime Inoue: Shun Shun Rikka / event rejection',
         'Uryu Ishida: Quincy archer / Antithesis',
         'Yasutora Sado: Chad / armoured fullbring arms',
         'Kisuke Urahara: Benihime / inventor and former captain',
         'Yoruichi Shihoin: Flash Goddess / Shunko',
         "Isshin Kurosaki: Engetsu / Ichigo's father",
         "Masaki Kurosaki: Quincy / Ichigo's mother",
         "Ryuken Ishida: Quincy doctor / Uryu's father",
         "Karin Kurosaki: Ichigo's spiritually aware sister",
         "Yuzu Kurosaki: Ichigo's younger sister",
         'Kon: Modified soul / stuffed lion',
         'Tessai Tsukabishi: Former Kido Corps chief',
         'Jinta Hanakari: Urahara shop assistant',
         'Ururu Tsumugiya: Urahara shop assistant / enhanced strength',
         'Genryusai Yamamoto: Ryujin Jakka / Head Captain',
         'Chojiro Sasakibe: Gonryomaru / First Division lieutenant',
         'Soi Fon: Suzumebachi / stealth captain',
         'Marechiyo Omaeda: Gegetsuburi / Second Division lieutenant',
         'Gin Ichimaru: Shinso / former Third Division captain',
         'Izuru Kira: Wabisuke / Third Division lieutenant',
         'Retsu Unohana: Minazuki / first Kenpachi',
         'Isane Kotetsu: Itegumo / healer',
         'Sosuke Aizen: Kyoka Suigetsu / complete hypnosis',
         'Momo Hinamori: Tobiume / Fifth Division lieutenant',
         'Byakuya Kuchiki: Senbonzakura / Sixth Division captain',
         'Renji Abarai: Zabimaru / Sixth Division lieutenant',
         'Sajin Komamura: Tenken / wolf captain',
         'Tetsuzaemon Iba: Seventh Division officer',
         'Shunsui Kyoraku: Katen Kyokotsu / captain commander',
         'Nanao Ise: Kido expert / divine sword',
         'Kaname Tosen: Suzumushi / former Ninth Division captain',
         'Shuhei Hisagi: Kazeshini / Ninth Division lieutenant',
         'Toshiro Hitsugaya: Hyorinmaru / ice prodigy',
         'Rangiku Matsumoto: Haineko / ash blades',
         'Kenpachi Zaraki: Nozarashi / Eleventh Division captain',
         'Yachiru Kusajishi: Sanpo Kenju / pink-haired lieutenant',
         'Ikkaku Madarame: Hozukimaru / Eleventh Division',
         "Yumichika Ayasegawa: Ruri'iro Kujaku / Eleventh Division",
         'Mayuri Kurotsuchi: Ashisogi Jizo / scientist captain',
         "Nemu Kurotsuchi: Artificial soul / Mayuri's lieutenant",
         'Akon: Research institute scientist',
         'Jushiro Ukitake: Sogyo no Kotowari / Thirteenth Division',
         'Kaien Shiba: Nejibana / former lieutenant',
         'Kukaku Shiba: Fireworks expert / Shiba clan',
         'Ganju Shiba: Sand transformation / Shiba clan',
         'Shinji Hirako: Sakanade / Visored leader',
         'Hiyori Sarugaki: Kubikiri Orochi / Visored',
         'Kensei Muguruma: Tachikaze / Visored captain',
         'Mashiro Kuna: Visored / kick specialist',
         'Rose Otoribashi: Kinshara / music-based Bankai',
         'Love Aikawa: Tengumaru / Visored',
         'Lisa Yadomaru: Haguro Tonbo / Visored',
         'Hachigen Ushoda: Barrier expert / Visored',
         'Ichibe Hyosube: Ichimonji / naming powers / Squad Zero',
         'Oetsu Nimaiya: Zanpakuto creator / Squad Zero',
         'Senjumaru Shutara: Weaving powers / Squad Zero',
         'Tenjiro Kirinji: Healing hot springs / Squad Zero',
         'Kirio Hikifune: Artificial souls / Squad Zero',
         'Yhwach: Quincy progenitor / Almighty',
         'Jugram Haschwalth: Balance / Sternritter commander',
         'Lille Barro: X-Axis / Schutzstaffel',
         'Gerard Valkyrie: Miracle / Schutzstaffel',
         "Pernida Parnkgjas: Compulsory / Soul King's left arm",
         'Askin Nakk Le Vaar: Deathdealing / Schutzstaffel',
         'Gremmy Thoumeaux: Visionary / imagination',
         'Bazz-B: Heat / flame manipulation',
         'Bambietta Basterbine: Explode / reishi bombs',
         'Candice Catnipp: Thunderbolt / lightning',
         'Meninas McAllon: Power / strength',
         'Giselle Gewelle: Zombie / blood puppetry',
         'Liltotto Lamperd: Glutton / consumption',
         'Quilge Opie: Jail / Hueco Mundo commander',
         'As Nodt: Fear / terror induction',
         'Mask De Masculine: Superstar / wrestler',
         "James: Mask's supporting partner",
         'Royd Lloyd: Yourself / appearance and memory imitation',
         'Loyd Lloyd: Yourself / appearance and power imitation',
         'Robert Accutrone: Sternritter gunslinger',
         'Nanana Najahkoop: Underbelly / reishi analysis',
         'Pepe Waccabrada: Love / mind control',
         'BG9: Mechanical Quincy',
         'Cang Du: Iron / hardened body',
         'Driscoll Berci: Overkill / power from kills',
         'Nianzol Weizol: Wind / attack deflection',
         'Shaz Domino: Regenerative Quincy combatant',
         'Coyote Starrk: Primera Espada / Los Lobos',
         "Lilynette Gingerbuck: Starrk's partner / split soul",
         'Baraggan Louisenbairn: Segunda Espada / aging aura',
         'Tier Harribel: Tercera Espada / water manipulation',
         'Ulquiorra Cifer: Cuarta Espada / Murcielago',
         'Nnoitra Gilga: Quinta Espada / Santa Teresa',
         'Grimmjow Jaegerjaquez: Sexta Espada / Pantera',
         'Zommari Rureaux: Septima Espada / Amor',
         'Szayelaporro Granz: Octava Espada / scientist',
         'Aaroniero Arruruerie: Novena Espada / hollow absorption',
         'Yammy Llargo: Rage-powered Espada / Ira',
         'Nelliel Tu Odelschwanck: Former Tercera Espada / Gamuza',
         'Luppi Antenor: Former Sexta Espada / Trepadora',
         'Tesla Lindocruz: Verruga / boar release',
         'Dordonii Alessandro Del Socaccio: Privaron Espada / wind',
         'Cirucci Sanderwicci: Privaron Espada / wings and tail',
         'Gantenbainne Mosqueda: Privaron Espada / Dragra',
         'Wonderweiss Margela: Extinguir / flame sealing',
         'Rudbornn Chelute: Exequias commander / Calavera',
         "Pesche Guatiche: Nel's companion / Infinite Slick",
         "Dondochakka Birstanne: Nel's companion",
         'Loly Aivirrne: Escolopendra / poisonous release',
         'Menoly Mallia: Arrancar / palace attendant',
         "Emilou Apacci: Harribel's Fraccion / deer release",
         "Franceska Mila Rose: Harribel's Fraccion / lion release",
         "Cyan Sung-Sun: Harribel's Fraccion / snake release",
         'Ayon: Chimera hollow / Tres Bestias summon',
         "Shawlong Koufang: Grimmjow's Fraccion / Tijereta",
         "Edrad Liones: Grimmjow's Fraccion / Volcanica",
         "Yylfordt Granz: Grimmjow's Fraccion / Del Toro",
         "Di Roy Rinker: Grimmjow's Fraccion",
         "Nakeem Grindina: Grimmjow's Fraccion",
         'Shukuro Tsukishima: Book of the End / past insertion',
         'Kugo Ginjo: Cross of Scaffold / former substitute',
         'Riruka Dokugamine: Dollhouse / fullbringer',
         'Yukio Hans Vorarlberna: Invaders Must Die / game worlds',
         'Jackie Tristan: Dirty Boots / fullbringer',
         'Giriko Kutsuzawa: Time Tells No Lies / fullbringer',
         'Moe Shishigawara: Jackpot Knuckle / probability',
         'Soul King: Linchpin of the worlds',
         "Mimihagi: Soul King's right arm / stagnation"],
 'SDS': ["Meliodas: Dragon's Sin of Wrath / demon prince",
         'Elizabeth Liones: Goddess princess / healing',
         "Ban: Fox's Sin of Greed / Snatch",
         "Diane: Serpent's Sin of Envy / giant",
         "King: Grizzly's Sin of Sloth / Fairy King Harlequin",
         "Gowther: Goat's Sin of Lust / doll magician",
         "Merlin: Boar's Sin of Gluttony / Infinity",
         "Escanor: Lion's Sin of Pride / Sunshine",
         'Hawk: Talking pig / scrap disposal captain',
         'Hawk Mama: Giant green pig / seal containing Chaos',
         'Elaine: Fountain guardian / wind fairy',
         'Jericho: Ice magic / Holy Knight',
         'Gilthunder: Lightning magic / Holy Knight',
         'Howzer: Tempest magic / Holy Knight',
         'Griamore: Wall magic / Holy Knight',
         'Hendrickson: Acid magic / former Great Holy Knight',
         'Dreyfus: Break magic / Great Holy Knight',
         'Zaratras: Purge / former Great Holy Knight',
         'Gustaf: Ice Fang / Holy Knight',
         'Helbram: Fairy / Link magic',
         'Slader: Overpower / Roars of Dawn leader',
         'Guila: Explosion magic / Holy Knight',
         'Deathpierce: Melody magic / Pleiades',
         'Denzel Liones: Judgement / Pleiades captain',
         'Dogedo: Boost magic / Pleiades',
         'Deldry: Love Drive / Pleiades',
         'Arden: Vain / Pleiades archer',
         'Waillo: Vroom magic / Pleiades',
         'Arthur Pendragon: King of Camelot / Chaos',
         "Cusack: Chandler's counterpart / demon swordsman",
         "Chandler: Meliodas's teacher / demon magician",
         'Zeldris: Piety / demon prince',
         'Estarossa: Love / Commandment warrior',
         "Mael: Archangel / Sunshine's original bearer",
         'Galand: Truth / Ten Commandments',
         'Melascula: Faith / soul manipulation',
         'Derieri: Purity / Combo Star',
         'Monspeet: Reticence / Trick Star',
         'Gloxinia: Repose / first Fairy King',
         'Drole: Patience / giant king',
         'Grayroad: Pacifism / demon curse',
         'Fraudrin: Selflessness proxy / Full Size',
         'Gowther the Demon: Original Selflessness / doll creator',
         'Demon King: Ruler of the Demon Clan',
         'Supreme Deity: Ruler of the Goddess Clan',
         'Ludociel: Flash / Four Archangels',
         'Sariel: Tornado / Four Archangels',
         'Tarmiel: Ocean / Four Archangels',
         'Nerobasta: Divine Lance / goddess',
         'Jenna: Druid priestess',
         'Zaneri: Druid priestess',
         "Matrona: Giant warrior / Diane's mentor",
         "Dolores: Young giant / Diane's friend",
         "Oslo: Black hound / King's companion",
         "Zhivago: Werefox / Ban's adoptive father",
         'Rou: Human warrior / ancient Holy War',
         "Gerheade: Fairy / Gloxinia's sister",
         "Gelda: Vampire / Zeldris's partner",
         "Cath Palug: Chaos beast / Arthur's companion",
         'Bartra Liones: Vision / king of Liones',
         "Margaret Liones: Princess / Ludociel's vessel",
         'Veronica Liones: Warrior princess',
         "Nadja Liones: Princess / doll Gowther's companion"],
 'DBZ': ['Son Goku: Saiyan / Kamehameha / Super Saiyan',
         'Vegeta: Saiyan prince / Final Flash',
         "Son Gohan: Goku's son / hidden potential",
         'Piccolo: Namekian warrior / Special Beam Cannon',
         'Krillin: Human martial artist / Destructo Disc',
         'Tien Shinhan: Three-eyed martial artist / Tri-Beam',
         'Yamcha: Wolf Fang Fist / martial artist',
         'Chiaotzu: Psychic martial artist',
         'Master Roshi: Turtle Hermit / Kamehameha teacher',
         'Bulma: Capsule Corp inventor / genius',
         "Chi-Chi: Martial artist / Goku's wife",
         "Son Goten: Goku's younger son / Super Saiyan",
         "Trunks: Vegeta's son / young Super Saiyan",
         'Future Trunks: Time-travelling swordsman',
         "Gotenks: Goten and Trunks's fusion",
         "Vegito: Goku and Vegeta's Potara fusion",
         "Gogeta: Goku and Vegeta's Fusion Dance warrior",
         "Videl: Martial artist / Mr. Satan's daughter",
         'Mr. Satan: World champion / Hercule',
         'Android 16: Red Ribbon android / nature lover',
         'Android 17: Lapis / infinite-energy android',
         'Android 18: Lazuli / infinite-energy android',
         'Android 19: Energy-absorbing android',
         'Dr. Gero: Android 20 / Red Ribbon scientist',
         'Cell: Bio-android / genetic warrior',
         "Cell Junior: Cell's offspring / miniature fighter",
         'Frieza: Galactic emperor / transforming tyrant',
         "King Cold: Frieza's father",
         "Cooler: Frieza's brother / movie antagonist",
         "Raditz: Goku's Saiyan brother",
         "Nappa: Saiyan elite / Vegeta's partner",
         'Saibaman: Cultivated alien fighter',
         "Zarbon: Frieza's officer / monster transformation",
         "Dodoria: Frieza's brutal officer",
         'Cui: Frieza Force elite',
         'Captain Ginyu: Body Change / Ginyu Force leader',
         'Jeice: Crusher Ball / Ginyu Force',
         'Burter: Super-speed / Ginyu Force',
         'Recoome: Brute force / Ginyu Force',
         'Guldo: Time freeze / Ginyu Force',
         'Appule: Frieza Force soldier',
         'Majin Buu: Fat Buu / magical regeneration',
         "Evil Buu: Buu's expelled evil",
         'Super Buu: Absorption / destructive Majin',
         'Kid Buu: Original chaotic Majin',
         "Uub: Kid Buu's human reincarnation",
         'Babidi: Sorcerer / Majin control',
         "Bibidi: Ancient sorcerer / Buu's former master",
         'Dabura: Demon Realm king / petrifying spit',
         "Pui Pui: Babidi's gravity-trained fighter",
         'Yakon: Light-eating monster',
         'Spopovich: Majin-enhanced tournament fighter',
         "Yamu: Babidi's energy collector",
         'Supreme Kai Shin: Eastern Supreme Kai',
         "Kibito: Supreme Kai's attendant",
         'Elder Kai: Ancient Supreme Kai / potential unlock',
         "Kibito Kai: Shin and Kibito's Potara fusion",
         'Grand Supreme Kai: Ancient leader of the Kais',
         'King Kai: North Kai / Kaio-ken teacher',
         'Grand Kai: Overseer of the four Kais',
         'West Kai: Western quadrant deity',
         'East Kai: Eastern quadrant deity',
         'South Kai: Southern quadrant deity',
         'Pikkon: Other World martial artist',
         'King Yemma: Other World judge',
         "Kami: Earth's guardian / Namekian",
         "Dende: Namekian healer / Earth's guardian",
         "Nail: Namekian warrior / Guru's protector",
         'Grand Elder Guru: Namekian elder / potential unlock',
         'Moori: Namekian elder',
         "Mr. Popo: Guardian's attendant",
         'Korin: Martial arts master / senzu keeper',
         "Yajirobe: Swordsman / Korin's companion",
         "Shenron: Earth's wish-granting dragon",
         "Porunga: Namek's wish-granting dragon",
         'Oolong: Shapeshifting pig',
         "Puar: Shapeshifting cat / Yamcha's companion",
         "Ox-King: Chi-Chi's father / Roshi's student",
         'Dr. Brief: Capsule Corp founder / inventor',
         'Fortuneteller Baba: Psychic / spirit medium',
         'Launch: Split-personality gunfighter',
         'Broly: Legendary Super Saiyan / Z movie version',
         "Paragus: Broly's father / Saiyan survivor",
         "Bardock: Goku's father / Saiyan warrior",
         "King Vegeta: Saiyan king / Vegeta's father",
         'Turles: Saiyan / Tree of Might',
         'Lord Slug: Super Namekian / movie villain',
         'Garlic Jr.: Immortal demon / Dead Zone',
         'Dr. Wheelo: Scientist / giant robotic body',
         "Dr. Kochin: Dr. Wheelo's assistant",
         'Android 13: Red Ribbon movie android',
         'Android 14: Red Ribbon movie android',
         'Android 15: Red Ribbon movie android',
         'Bojack: Galactic warrior / movie villain',
         "Zangya: Bojack's warrior",
         "Bido: Bojack's warrior",
         "Bujin: Bojack's psychic warrior",
         "Kogu: Bojack's swordsman",
         'Janemba: Reality-warping demon / Fusion Reborn',
         'Hirudegarn: Phantom demon / Wrath of the Dragon',
         'Tapion: Hero / enchanted ocarina',
         "Minotia: Tapion's younger brother"],
 'VS': ["Thorfinn: Icelandic warrior / Thors's son",
        'Thors: Troll of Jom / former Jomsviking',
        'Askeladd: Mercenary captain / cunning swordsman',
        'Thorkell: Giant warrior / battle fanatic',
        'Canute: Danish prince / king',
        "Leif Erikson: Explorer / Thorfinn's family friend",
        "Einar: English farmer / Thorfinn's companion",
        "Arnheid: Ketil's enslaved servant",
        "Gardar: Arnheid's husband / escaped slave",
        'Ketil: Farm owner / wealthy landholder',
        "Thorgil: Ketil's warrior son",
        "Olmar: Ketil's younger son",
        "Sverkel: Ketil's father / farmer",
        'Snake: Farm guard leader / skilled swordsman',
        'Fox: Farm guard / mercenary',
        'Badger: Farm guard',
        'Pater: Ketil farm retainer',
        "Bjorn: Askeladd's second-in-command / berserker",
        'Floki: Jomsviking commander / schemer',
        "Ragnar: Canute's guardian",
        'Willibald: Priest / philosopher of love',
        'Sweyn Forkbeard: King of Denmark and England',
        "Harald: Canute's elder brother / Danish king",
        "Wulf: Canute's guard / combat instructor",
        "Gunnar: Canute's adviser",
        "Helga: Thorfinn's mother",
        "Ylva: Thorfinn's elder sister",
        'Halfdan: Wealthy Icelandic landowner',
        "Sigurd: Halfdan's son",
        'Gudrid: Aspiring explorer / sailor',
        'Hild: Hunter / crossbow inventor',
        'Garm: Spear prodigy / battle seeker',
        'Vagn: Jomsviking faction leader',
        "Baldr: Floki's grandson",
        "Bug-Eyes: Thorfinn / Leif's adopted son",
        "Cordelia: Gentle giant / Thorkell's child",
        'Karli: Orphan travelling with Thorfinn',
        'Ivar: Vinland settler / militant swordsman',
        "Styrk: Ivar's brother / strategist",
        'Hreidar: Vinland settler',
        'Eyvind: Vinland settler / inventor'],
 'FF': ["Shinra Kusakabe: Devil's Footprints / Company 8",
        'Arthur Boyle: Plasma sword / Knight King',
        'Maki Oze: Flame control / former soldier',
        'Akitaru Obi: Company 8 captain / physical strength',
        'Takehisa Hinawa: Bullet velocity control / lieutenant',
        'Iris: Sister / Company 8 prayer support',
        'Tamaki Kotatsu: Nekomata flames / Company 8',
        'Vulcan Joseph: Mechanic / Company 8 engineer',
        'Viktor Licht: Scientist / combustion researcher',
        'Lisa Isaribi: Feeler / tentacle flames',
        "Yu: Vulcan's apprentice",
        'Joker: Ignition ability / intelligence broker',
        'Benimaru Shinmon: Compound pyrokinetic / Asakusa captain',
        'Konro Sagamiya: Company 7 lieutenant',
        'Hikage: Company 7 child / fox flames',
        'Hinata: Company 7 child / fox flames',
        'Leonard Burns: Voltage Nova / Company 1 captain',
        'Karim Flam: Thermoacoustic refrigeration / Company 1',
        'Foien Li: Company 1 lieutenant',
        'Onyango: Company 1 veteran',
        'Takeru Noto: Juggernaut / explosive flames',
        'Gustav Honda: Company 2 captain / head reinforcement',
        'Hajiki: Company 2 / thermal vision',
        'Giovanni: Company 3 captain / mechanical body',
        'Soichiro Hague: Company 4 captain',
        'Pan Ko Paat: Company 4 lieutenant / whistle encouragement',
        'Ogun Montgomery: Flamy Ink / Company 4',
        'Hibana: Company 5 captain / heat syncope',
        'Toru Kishiri: Bubblegum explosives / Company 5',
        'Kayoko Huang: Company 6 captain / flame healing',
        "Sho Kusakabe: Severed Universe / Shinra's brother",
        'Haumea: Adolla Burst / electrical manipulation',
        'Arrow: White-Clad archer',
        "Charon: Kinetic absorption / Haumea's guardian",
        'Inca Kasugatani: Fire-path prediction / Adolla Burst',
        'Nataku Son: Radiation flames / Adolla Burst',
        'Sumire: Tremor-based ignition / Adolla Burst',
        'Amaterasu: First Pillar / power plant core',
        'Assault: White-Clad assassin',
        'Yona: Shapeshifter / White-Clad',
        'Mirage: Heat mirages / White-Clad',
        'Flail: Flame mace / White-Clad',
        'Orochi: Medusa Whip / White-Clad',
        'Ritsu: Necro Pyro / White-Clad',
        'Yom: White-Clad / flame cloaking',
        'Rekka Hoshimiya: Company 1 traitor / explosive fists',
        'Evangelist: Adolla entity / White-Clad deity',
        'Woman in Black: Adolla-linked survivor / Tabernacle',
        'Dragon: White-Clad powerhouse / draconic body',
        'Gold: Gold manipulation / White-Clad',
        'Stream: Airflow manipulation / White-Clad',
        'Fracture: White-Clad fighter',
        'Raffles III: Holy Sol Temple emperor',
        'Scop: Talking mole / Chinese Peninsula',
        'Yata: Talking crow / Chinese Peninsula'],
 'COTE': ['Kiyotaka Ayanokoji: White Room prodigy / strategist',
          'Suzune Horikita: Class D leader / analytical student',
          'Kikyo Kushida: Social manipulator / hidden hostility',
          "Kei Karuizawa: Class social leader / Ayanokoji's ally",
          'Kakeru Ryuen: Ruthless class leader / strategist',
          'Arisu Sakayanagi: Class A leader / chess prodigy',
          'Honami Ichinose: Popular class leader / social intelligence',
          'Kohei Katsuragi: Class A strategist',
          'Rokusuke Koenji: Eccentric prodigy / exceptional athleticism',
          'Ken Sudo: Basketball player / physical specialist',
          'Yosuke Hirata: Class mediator / popular student',
          'Airi Sakura: Shy student / gravure model',
          'Haruka Hasebe: Ayanokoji Group member',
          'Akito Miyake: Archery club / Ayanokoji Group',
          'Teruhiko Yukimura: Academically gifted / Ayanokoji Group',
          'Kanji Ike: Social student / outdoor skills',
          'Haruki Yamauchi: Class D student / schemer',
          "Maya Sato: Kei's friend / Class D",
          'Chiaki Matsushita: Quietly capable Class D student',
          'Mei-Yu Wang: Mii-chan / academically capable student',
          'Satsuki Shinohara: Class D student',
          'Hideo Sotomura: Professor / anime enthusiast',
          'Kayano Onodera: Athletic Class D student',
          "Mio Ibuki: Martial artist / Ryuen's class",
          "Daichi Ishizaki: Ryuen's loyal classmate",
          "Albert Yamada: Ryuen's physically powerful ally",
          'Hiyori Shiina: Book lover / perceptive student',
          "Satoru Kaneda: Ryuen's strategist",
          "Masumi Kamuro: Sakayanagi's associate",
          'Hayato Kito: Class A enforcer',
          'Yahiko Totsuka: Katsuragi faction student',
          "Ryuji Kanzaki: Ichinose's analytical classmate",
          "Chihiro Shiranami: Ichinose's classmate",
          "Yuki Himeno: Reserved student / Ichinose's class",
          "Mako Amikura: Ichinose's friend",
          "Manabu Horikita: Student council president / Suzune's brother",
          'Miyabi Nagumo: Student council president / meritocracy advocate',
          'Akane Tachibana: Student council secretary',
          'Ikuto Kiriyama: Student council vice-president',
          'Fuka Kiryuin: Exceptional senior / independent prodigy',
          'Sae Chabashira: Class D homeroom teacher',
          'Chie Hoshinomiya: Class B homeroom teacher',
          'Tomonari Mashima: Class A homeroom teacher',
          'Kazuma Sakagami: Class C homeroom teacher',
          "Atsuomi Ayanokoji: White Room founder / Kiyotaka's father",
          "Chairman Sakayanagi: School chairman / Arisu's father",
          'Tsukishiro: Acting director / White Room associate',
          'Ichika Amasawa: White Room student / first-year infiltrator',
          'Takuya Yagami: White Room student / first-year strategist',
          'Tsubasa Nanase: First-year student / martial skills',
          'Kazuomi Hosen: Violent first-year leader',
          'Riku Utomiya: First-year physical specialist',
          'Sakurako Tsubaki: First-year strategist'],
 'HQ': ['Shoyo Hinata: Karasuno middle blocker / quick attacker',
        'Tobio Kageyama: Karasuno setter / King of the Court',
        'Daichi Sawamura: Karasuno captain / defensive wing spiker',
        'Koshi Sugawara: Karasuno setter / vice-captain',
        'Asahi Azumane: Karasuno ace',
        'Yu Nishinoya: Karasuno libero / Guardian Deity',
        'Ryunosuke Tanaka: Karasuno wing spiker',
        'Kei Tsukishima: Karasuno middle blocker / read blocking',
        'Tadashi Yamaguchi: Karasuno pinch server',
        'Chikara Ennoshita: Karasuno wing spiker / future captain',
        'Hisashi Kinoshita: Karasuno pinch server',
        'Kazuhito Narita: Karasuno middle blocker',
        'Kiyoko Shimizu: Karasuno manager',
        'Hitoka Yachi: Karasuno manager / designer',
        'Keishin Ukai: Karasuno coach',
        'Ittetsu Takeda: Karasuno faculty adviser',
        'Ikkei Ukai: Former Karasuno coach',
        'Tenma Udai: Little Giant / former Karasuno ace',
        'Toru Oikawa: Aoba Johsai setter / elite server',
        'Hajime Iwaizumi: Aoba Johsai ace / vice-captain',
        'Issei Matsukawa: Aoba Johsai middle blocker',
        'Takahiro Hanamaki: Aoba Johsai wing spiker',
        'Shinji Watari: Aoba Johsai libero',
        'Shigeru Yahaba: Aoba Johsai setter',
        'Yutaro Kindaichi: Aoba Johsai middle blocker',
        'Akira Kunimi: Aoba Johsai wing spiker',
        'Kentaro Kyotani: Mad Dog / Aoba Johsai attacker',
        'Tetsuro Kuroo: Nekoma captain / read blocker',
        'Kenma Kozume: Nekoma setter / analytical strategist',
        'Morisuke Yaku: Nekoma libero',
        'Nobuyuki Kai: Nekoma vice-captain',
        'Taketora Yamamoto: Nekoma ace',
        'Shohei Fukunaga: Nekoma wing spiker',
        'Lev Haiba: Nekoma middle blocker / tall rookie',
        'So Inuoka: Nekoma middle blocker / opposite',
        'Yuki Shibayama: Nekoma libero',
        'Yasufumi Nekomata: Nekoma coach',
        'Kotaro Bokuto: Fukurodani ace / top wing spiker',
        'Keiji Akaashi: Fukurodani setter',
        'Akinori Konoha: Fukurodani all-rounder',
        'Yamato Sarukui: Fukurodani wing spiker',
        'Tatsuki Washio: Fukurodani middle blocker',
        'Haruki Komi: Fukurodani libero',
        'Wakatoshi Ushijima: Shiratorizawa ace / left-handed cannon',
        'Satori Tendo: Shiratorizawa middle blocker / Guess Monster',
        'Tsutomu Goshiki: Shiratorizawa wing spiker',
        'Kenjiro Shirabu: Shiratorizawa setter',
        'Eita Semi: Shiratorizawa setter / pinch server',
        'Reon Ohira: Shiratorizawa vice-captain',
        'Hayato Yamagata: Shiratorizawa libero',
        'Tanji Washijo: Shiratorizawa coach',
        'Takanobu Aone: Date Tech middle blocker / Iron Wall',
        'Kenji Futakuchi: Date Tech captain / wing spiker',
        'Kanji Koganegawa: Date Tech setter',
        'Yasushi Kamasaki: Date Tech middle blocker',
        'Kaname Moniwa: Date Tech former captain / setter',
        'Atsumu Miya: Inarizaki setter / dual-style server',
        'Osamu Miya: Inarizaki opposite / twin quick attacks',
        'Shinsuke Kita: Inarizaki captain / reliable all-rounder',
        'Rintaro Suna: Inarizaki middle blocker',
        'Aran Ojiro: Inarizaki ace',
        'Hitoshi Ginjima: Inarizaki wing spiker',
        'Ren Omimi: Inarizaki middle blocker',
        'Michinari Akagi: Inarizaki libero',
        'Sachiro Hirugami: Kamomedai middle blocker / blocking specialist',
        'Korai Hoshiumi: Kamomedai ace / Little Giant',
        'Gao Hakuba: Kamomedai towering opposite',
        'Aikichi Suwa: Kamomedai setter / captain',
        'Kiyoomi Sakusa: Itachiyama ace / flexible wrists',
        'Motoya Komori: Itachiyama libero',
        'Suguru Daisho: Nohebi captain / tactical provocateur',
        'Yuji Terushima: Johzenji captain / improvisational attacker',
        'Takeru Nakashima: Wakutani Minami ace',
        'Wakatsu Kiryu: Mujinazaka ace / top wing spiker',
        'Eikichi Chigaya: Shinzen middle blocker'],
 'KNB': ['Tetsuya Kuroko: Seirin / misdirection / Phantom Sixth Man',
         'Taiga Kagami: Seirin ace / jumping power / Zone',
         'Junpei Hyuga: Seirin captain / clutch three-pointers',
         'Shun Izuki: Seirin point guard / Eagle Eye',
         'Teppei Kiyoshi: Iron Heart / Uncrowned King',
         'Rinnosuke Mitobe: Seirin centre / hook shots',
         'Shinji Koganei: Seirin all-rounder / animal instincts',
         'Koki Furihata: Seirin reserve point guard',
         'Hiroshi Fukuda: Seirin reserve centre',
         'Koichi Kawahara: Seirin reserve forward',
         'Riko Aida: Seirin coach / body analysis',
         "Kagetora Aida: Riko's father / former national player",
         'Ryota Kise: Kaijo ace / Perfect Copy',
         'Yukio Kasamatsu: Kaijo captain / point guard',
         'Yoshitaka Moriyama: Kaijo shooting guard',
         'Mitsuhiro Hayakawa: Kaijo rebound specialist',
         'Koji Kobori: Kaijo centre',
         'Shintaro Midorima: Shutoku ace / full-court three-pointers',
         'Kazunari Takao: Shutoku point guard / Hawk Eye',
         'Taisuke Otsubo: Shutoku captain / centre',
         'Kiyoshi Miyaji: Shutoku small forward',
         'Shinsuke Kimura: Shutoku power forward',
         'Daiki Aomine: Too ace / formless shots / Zone',
         'Satsuki Momoi: Too manager / analytical scouting',
         'Shoichi Imayoshi: Too captain / point guard',
         'Ryo Sakurai: Too shooting guard / quick release',
         'Kosuke Wakamatsu: Too centre',
         'Yoshinori Susa: Too power forward',
         'Atsushi Murasakibara: Yosen centre / dominant reach',
         'Tatsuya Himuro: Yosen shooting guard / Mirage Shot',
         'Kenichi Okamura: Yosen captain / centre',
         'Kensuke Fukui: Yosen point guard',
         'Wei Liu: Yosen small forward',
         'Seijuro Akashi: Rakuzan captain / Emperor Eye',
         'Reo Mibuchi: Uncrowned King / three shot forms',
         'Kotaro Hayama: Uncrowned King / Lightning Dribble',
         'Eikichi Nebuya: Uncrowned King / muscular centre',
         'Chihiro Mayuzumi: Rakuzan / new phantom sixth man',
         'Shogo Haizaki: Fukuda Sogo / Pillage',
         'Makoto Hanamiya: Kirisaki Daiichi / Spiderweb strategist',
         'Kentaro Seto: Kirisaki Daiichi / high-IQ centre',
         'Tomoki Tsugawa: Seiho / defensive specialist',
         'Masaaki Nakatani: Shutoku coach',
         'Naoto Sanada: Too coach',
         'Masako Araki: Yosen coach',
         'Eiji Shirogane: Rakuzan coach',
         'Shuzo Nijimura: Former Teiko captain',
         "Shigehiro Ogiwara: Kuroko's childhood basketball friend",
         'Nash Gold Jr.: Jabberwock / Belial Eye',
         'Jason Silver: Jabberwock / exceptional physicality',
         'Nick: Jabberwock shooting guard',
         'Allen: Jabberwock small forward',
         'Zack: Jabberwock power forward',
         "Alexandra Garcia: Former professional / Kagami's mentor"],
 'EIS': ['Cid Kagenou: Shadow / I Am Atomic',
         'Alpha: First Shadow / Shadow Garden leader',
         'Beta: Second Shadow / author Natsume Kafka',
         'Gamma: Third Shadow / Mitsugoshi business genius',
         'Delta: Fourth Shadow / beastkin berserker',
         'Epsilon: Fifth Shadow / precise slime control',
         'Zeta: Sixth Shadow / beastkin spy',
         'Eta: Seventh Shadow / genius researcher',
         'Nu: Shadow Garden operative / infiltration',
         'Lambda: Shadow Garden combat instructor',
         'Victoria: Number 559 / devoted operative',
         'Kai: Shadow Garden operative / Number 22',
         'Omega: Shadow Garden operative / Number 24',
         "Claire Kagenou: Cid's sister / Dark Knight",
         'Alexia Midgar: Midgar princess / swordswoman',
         'Iris Midgar: Midgar princess / Crimson Knights',
         'Rose Oriana: Oriana princess / Number 666',
         'Sherry Barnett: Ancient artifact researcher',
         'Aurora: Witch of Calamity / Diablos connection',
         'Elizabeth: Blood Queen / progenitor vampire',
         "Mary: Ancient vampire / Elizabeth's servant",
         'Yukime: Spirit Fox / Lawless City ruler',
         'Juggernaut: Black Tower ruler / brute strength',
         "Crimson: Vampire / Elizabeth's subordinate",
         'Beatrix: War Goddess / elf swordswoman',
         'Annerose Nichtsehen: Travelling swordswoman',
         'Goldoh Kinmeki: Mercenary / Golden Gilded',
         'Quinton: Mercenary / tournament fighter',
         "Skel Etal: Cid's academy friend",
         "Po Tato: Cid's academy friend",
         "Akane Nishino: Cid's former-world classmate",
         "Akira Nishino: Akane's brother / researcher",
         'Mordred: Knights of Rounds / Ragnarok wielder',
         'Nelson: Knights of Rounds / sanctuary researcher',
         'Lutheran Barnett: Academy vice-principal / cult researcher',
         'Zenon Griffey: Sword instructor / Cult of Diablos',
         "Olba: Cult knight / Milia's father",
         'Milia: Possessed girl / cult experiment survivor',
         'Rex: Cult operative / academy attacker',
         'Doem Ketsuhat: Oriana noble / cult manipulator',
         'Gettan: Great Wolf / cult-aligned swordsman',
         'Petos: Knights of Rounds / cult researcher',
         'Fenrir: Knights of Rounds / ancient swordsman',
         'Loki: Knights of Rounds / cult strategist',
         'Christina Hope: Midgar noble / academy student',
         'Kanade: Academy student / survivalist',
         "Nina: Claire's friend / covert operative",
         'Isaac: Academy student / cult connection'],
 'JOJO': ['Jonathan Joestar: Hamon / original JoJo',
          'Will Anthonio Zeppeli: Hamon master / Ripple teacher',
          'Dire: Hamon / Thunder Cross Split Attack',
          'Straizo: Hamon master / later vampire',
          'Tonpetty: Hamon grandmaster / prophetic insight',
          'Dio Brando: Vampire / later DIO / The World',
          'Joseph Joestar: Hamon / Hermit Purple / trickster',
          'Caesar Anthonio Zeppeli: Hamon / bubble cutters',
          "Lisa Lisa: Hamon master / Joseph's mother",
          'Rudol von Stroheim: Cyborg / German technology',
          'Kars: Pillar Man / Ultimate Life Form',
          'Esidisi: Pillar Man / boiling blood',
          'Wamuu: Pillar Man / divine sandstorm',
          'Santana: Pillar Man / body manipulation',
          'Loggins: Hamon instructor',
          'Messina: Hamon instructor',
          'Jotaro Kujo: Star Platinum / time stop',
          'Noriaki Kakyoin: Hierophant Green / Emerald Splash',
          "Muhammad Avdol: Magician's Red / fire",
          'Jean Pierre Polnareff: Silver Chariot / sword Stand',
          'Iggy: The Fool / sand Stand',
          'Holy Kujo: Unnamed plant-like Stand',
          'Gray Fly: Tower of Gray / beetle Stand',
          'Impostor Captain Tennille: Dark Blue Moon / aquatic Stand',
          "Forever: Strength / orangutan's ship Stand",
          'Devo the Cursed: Ebony Devil / possessed doll',
          'Rubber Soul: Yellow Temperance / flesh disguise',
          'Hol Horse: Emperor / homing revolver',
          'J. Geil: Hanged Man / mirror reflections',
          'Nena: Empress / parasitic growth',
          'ZZ: Wheel of Fortune / car Stand',
          'Enya the Hag: Justice / fog puppetry',
          'Steely Dan: Lovers / microscopic Stand',
          'Arabia Fats: Sun / artificial sunlight',
          'Mannish Boy: Death Thirteen / dream world',
          'Cameo: Judgement / clay wishes',
          'Midler: High Priestess / mineral transformation',
          "N'Doul: Geb / remote water Stand",
          'Oingo: Khnum / face transformation',
          'Boingo: Tohth / predictive comic',
          'Anubis: Possessing sword / sentient Stand',
          "Chaka: Anubis's sword-possessed wielder",
          "Khan: Anubis's sword-possessed barber",
          'Mariah: Bastet / magnetism',
          'Alessi: Sethan / age regression',
          "Daniel J. D'Arby: Osiris / soul gambling",
          "Telence T. D'Arby: Atum / soul-reading gamer",
          'Pet Shop: Horus / ice falcon',
          'Kenny G.: Tenore Sax / illusions',
          'Vanilla Ice: Cream / void sphere',
          'Josuke Higashikata (Part 4): Crazy Diamond / restoration',
          'Koichi Hirose: Echoes / sound and weight',
          'Okuyasu Nijimura: The Hand / space erasure',
          'Keicho Nijimura: Bad Company / miniature army',
          "Rohan Kishibe: Heaven's Door / memory reading and commands",
          'Yukako Yamagishi: Love Deluxe / hair control',
          'Yoshikage Kira (Part 4): Killer Queen / bombs and Bites the Dust',
          'Yoshihiro Kira: Atom Heart Father / photograph ghost',
          'Akira Otoishi: Red Hot Chili Pepper / electricity',
          'Shigekiyo Yangu: Harvest / collecting swarm',
          'Toshikazu Hazamada: Surface / copying mannequin',
          'Tamami Kobayashi: The Lock / guilt manipulation',
          'Anjuro Katagiri: Aqua Necklace / water murderer',
          'Tonio Trussardi: Pearl Jam / healing cuisine',
          'Aya Tsuji: Cinderella / face and fortune alteration',
          'Shizuka Joestar: Achtung Baby / invisibility',
          'Ken Oyanagi: Boy II Man / rock-paper-scissors theft',
          'Yuya Fungami: Highway Star / scent tracking and draining',
          'Toyohiro Kanedaichi: Super Fly / tower prison',
          'Terunosuke Miyamoto: Enigma / paper imprisonment',
          'Masazo Kinoto: Cheap Trick / parasitic back Stand',
          'Mikitaka Hazekura: Earth Wind and Fire / shapeshifting',
          'Bug-Eaten: Ratt / flesh-melting darts',
          'Not Bug-Eaten: Ratt / flesh-melting darts',
          'Giorno Giovanna: Gold Experience / life creation and Requiem',
          'Bruno Bucciarati: Sticky Fingers / zippers',
          'Leone Abbacchio: Moody Blues / event replay',
          'Guido Mista: Sex Pistols / bullet guidance',
          'Narancia Ghirga: Aerosmith / miniature fighter plane',
          'Pannacotta Fugo: Purple Haze / lethal virus',
          'Trish Una: Spice Girl / softening',
          'Diavolo: King Crimson / time erasure',
          "Vinegar Doppio: Epitaph access / Diavolo's alternate personality",
          'Risotto Nero: Metallica / iron manipulation',
          'Prosciutto: The Grateful Dead / aging',
          'Pesci: Beach Boy / fishing hook Stand',
          'Ghiaccio: White Album / extreme cold',
          'Melone: Baby Face / computer-generated homunculus',
          'Illuso: Man in the Mirror / mirror world',
          'Formaggio: Little Feet / shrinking',
          'Polpo: Black Sabbath / shadow assassin',
          'Mario Zucchero: Soft Machine / deflation',
          'Sale: Kraft Work / kinetic fixing',
          'Squalo: Clash / water-jumping shark',
          'Tiziano: Talking Head / forced lies',
          'Carne: Notorious B.I.G / posthumous pursuit',
          'Cioccolata: Green Day / lethal mould',
          'Secco: Oasis / ground liquefaction',
          'Jolyne Cujoh: Stone Free / thread body',
          'Ermes Costello: Kiss / duplicating stickers',
          'Foo Fighters: Plankton colony / Stand intelligence',
          'Weather Report: Weather control / Heavy Weather',
          'Narciso Anasui: Diver Down / internal reconstruction',
          'Emporio Alnino: Burning Down the House / ghost room',
          'Enrico Pucci: Whitesnake / C-Moon / Made in Heaven',
          'Johngalli A.: Manhattan Transfer / sniper Stand',
          'Thunder McQueen: Highway to Hell / linked damage',
          'Miraschon: Marilyn Manson / debt collector',
          "Lang Rangler: Jumpin' Jack Flash / zero gravity",
          'Sports Maxx: Limp Bizkit / invisible undead',
          'Viviano Westwood: Planet Waves / meteors',
          "Kenzou: Dragon's Dream / feng shui",
          'D an G: Yo-Yo Ma / automatic assassin',
          'Guccio: Survivor / aggression induction',
          'Miuccia Miuller: Jail House Lock / memory limit',
          'Ungalo: Bohemian Rhapsody / fictional beings',
          'Rikiel: Sky High / rod manipulation',
          'Donatello Versus: Under World / earth memories',
          'Green Baby: Green Green Grass of Home / shrinking approach',
          'Johnny Joestar: Tusk / Spin-powered nail bullets',
          'Gyro Zeppeli: Steel Ball Spin / Ball Breaker',
          'Funny Valentine: D4C / dimensional travel / Love Train',
          'Diego Brando: Scary Monsters / dinosaur transformation',
          'Alternate Diego Brando: The World / time stop',
          'Lucy Steel: Ticket to Ride / protective misfortune',
          'Hot Pants: Cream Starter / flesh spray',
          'Mountain Tim: Oh! Lonesome Me / rope travel',
          'Ringo Roadagain: Mandom / six-second rewind',
          'Wekapipo: Wrecking Ball / Zeppeli steel-ball technique',
          'Sandman: In a Silent Way / sound constructs',
          'Pocoloco: Hey Ya! / encouraging Stand',
          'Blackmore: Catch the Rainbow / rain control',
          'Dr. Ferdinand: Scary Monsters / dinosaur infection',
          'Oyecomova: Boku no Rhythm wo Kiitekure / contact bombs',
          'Pork Pie Hat Kid: Wired / fishing hooks',
          'Benjamin Boom Boom: Tomb of the Boom / magnetic iron',
          'Andre Boom Boom: Tomb of the Boom / magnetic iron',
          'L.A. Boom Boom: Tomb of the Boom / magnetic iron',
          'Eleven Men: Tattoo You! / body-hopping group',
          'Axl RO: Civil War / discarded guilt',
          'Magenta Magenta: 20th Century BOY / defensive invulnerability',
          'Mike O.: Tubular Bells / metal balloon animals',
          'Sugar Mountain: Giant tree / trial Stand',
          "Jesus: Saint's Corpse / miraculous guidance",
          'Josuke Higashikata (Part 8): Soft and Wet / bubbles / Go Beyond',
          'Yasuho Hirose: Paisley Park / information navigation',
          'Rai Mamezuku: Doggy Style / unravelling body',
          'Norisuke Higashikata IV: King Nothing / scent puzzle',
          'Jobin Higashikata: Speed King / heat storage',
          'Tsurugi Higashikata: Paper Moon King / perception confusion',
          'Daiya Higashikata: California King Bed / memory theft',
          'Hato Higashikata: Walking Heart / extending heels',
          'Joshu Higashikata: Nut King Call / nuts and bolts',
          'Kaato Higashikata: Space Trucking / card storage',
          'Mitsuba Higashikata: Awaking III Leaves / vector arrows',
          'Yoshikage Kira (Part 8): Killer Queen / explosive bubbles',
          'Josefumi Kujo: Soft and Wet / plundering bubbles',
          'Kei Nijimura: Born This Way / freezing motorcycle',
          'Tooru: Wonder of U / calamity',
          'Ojiro Sasame: Fun Fun Fun / limb control',
          'Aisho Dainenjiyama: Doobie Wah! / breath-tracking vortex',
          'Tamaki Damo: Vitamin C / softening',
          'Yotsuyu Yagiyama: I Am a Rock / attraction',
          'A. Phex Elder Brother: Schott Key No. 1 / transfer between hands',
          'A. Phex Younger Brother: Schott Key No. 2 / toxic gas football',
          'Urban Guerrilla: Brain Storm / corrosive organisms',
          'Doremifasolati Do: Rock organism / subterranean transport',
          'Poor Tom: Ozon Baby / pressure manipulation',
          'Dolomite: Blue Hawaii / pursuit possession',
          'Wu Tomoki: Doctor Wu / particle disassembly',
          'Jodio Joestar: November Rain / heavy rain',
          'Dragona Joestar: Smooth Operators / surface displacement',
          'Paco Laburantes: The Hustle / muscle control',
          'Usagi Alohaoe: The Matte Kudasai / object replication',
          'Charming Man: Bigmouth Strikes Again / disguise particles',
          'Lulu: Bags Groove / disease-like attack',
          'Bobby Jean: Glory Days / slow bullets'],
 'PKMN': ['Bulbasaur: Grass/Poison / National Dex #0001',
          'Ivysaur: Grass/Poison / National Dex #0002',
          'Venusaur: Grass/Poison / National Dex #0003',
          'Charmander: Fire / National Dex #0004',
          'Charmeleon: Fire / National Dex #0005',
          'Charizard: Fire/Flying / National Dex #0006',
          'Squirtle: Water / National Dex #0007',
          'Wartortle: Water / National Dex #0008',
          'Blastoise: Water / National Dex #0009',
          'Caterpie: Bug / National Dex #0010',
          'Metapod: Bug / National Dex #0011',
          'Butterfree: Bug/Flying / National Dex #0012',
          'Weedle: Bug/Poison / National Dex #0013',
          'Kakuna: Bug/Poison / National Dex #0014',
          'Beedrill: Bug/Poison / National Dex #0015',
          'Pidgey: Normal/Flying / National Dex #0016',
          'Pidgeotto: Normal/Flying / National Dex #0017',
          'Pidgeot: Normal/Flying / National Dex #0018',
          'Rattata: Normal / National Dex #0019',
          'Raticate: Normal / National Dex #0020',
          'Spearow: Normal/Flying / National Dex #0021',
          'Fearow: Normal/Flying / National Dex #0022',
          'Ekans: Poison / National Dex #0023',
          'Arbok: Poison / National Dex #0024',
          'Pikachu: Electric / National Dex #0025',
          'Raichu: Electric / National Dex #0026',
          'Sandshrew: Ground / National Dex #0027',
          'Sandslash: Ground / National Dex #0028',
          'Nidoran♀: Poison / National Dex #0029',
          'Nidorina: Poison / National Dex #0030',
          'Nidoqueen: Poison/Ground / National Dex #0031',
          'Nidoran♂: Poison / National Dex #0032',
          'Nidorino: Poison / National Dex #0033',
          'Nidoking: Poison/Ground / National Dex #0034',
          'Clefairy: Fairy / National Dex #0035',
          'Clefable: Fairy / National Dex #0036',
          'Vulpix: Fire / National Dex #0037',
          'Ninetales: Fire / National Dex #0038',
          'Jigglypuff: Normal/Fairy / National Dex #0039',
          'Wigglytuff: Normal/Fairy / National Dex #0040',
          'Zubat: Poison/Flying / National Dex #0041',
          'Golbat: Poison/Flying / National Dex #0042',
          'Oddish: Grass/Poison / National Dex #0043',
          'Gloom: Grass/Poison / National Dex #0044',
          'Vileplume: Grass/Poison / National Dex #0045',
          'Paras: Bug/Grass / National Dex #0046',
          'Parasect: Bug/Grass / National Dex #0047',
          'Venonat: Bug/Poison / National Dex #0048',
          'Venomoth: Bug/Poison / National Dex #0049',
          'Diglett: Ground / National Dex #0050',
          'Dugtrio: Ground / National Dex #0051',
          'Meowth: Normal / National Dex #0052',
          'Persian: Normal / National Dex #0053',
          'Psyduck: Water / National Dex #0054',
          'Golduck: Water / National Dex #0055',
          'Mankey: Fighting / National Dex #0056',
          'Primeape: Fighting / National Dex #0057',
          'Growlithe: Fire / National Dex #0058',
          'Arcanine: Fire / National Dex #0059',
          'Poliwag: Water / National Dex #0060',
          'Poliwhirl: Water / National Dex #0061',
          'Poliwrath: Water/Fighting / National Dex #0062',
          'Abra: Psychic / National Dex #0063',
          'Kadabra: Psychic / National Dex #0064',
          'Alakazam: Psychic / National Dex #0065',
          'Machop: Fighting / National Dex #0066',
          'Machoke: Fighting / National Dex #0067',
          'Machamp: Fighting / National Dex #0068',
          'Bellsprout: Grass/Poison / National Dex #0069',
          'Weepinbell: Grass/Poison / National Dex #0070',
          'Victreebel: Grass/Poison / National Dex #0071',
          'Tentacool: Water/Poison / National Dex #0072',
          'Tentacruel: Water/Poison / National Dex #0073',
          'Geodude: Rock/Ground / National Dex #0074',
          'Graveler: Rock/Ground / National Dex #0075',
          'Golem: Rock/Ground / National Dex #0076',
          'Ponyta: Fire / National Dex #0077',
          'Rapidash: Fire / National Dex #0078',
          'Slowpoke: Water/Psychic / National Dex #0079',
          'Slowbro: Water/Psychic / National Dex #0080',
          'Magnemite: Electric/Steel / National Dex #0081',
          'Magneton: Electric/Steel / National Dex #0082',
          'Farfetch’d: Normal/Flying / National Dex #0083',
          'Doduo: Normal/Flying / National Dex #0084',
          'Dodrio: Normal/Flying / National Dex #0085',
          'Seel: Water / National Dex #0086',
          'Dewgong: Water/Ice / National Dex #0087',
          'Grimer: Poison / National Dex #0088',
          'Muk: Poison / National Dex #0089',
          'Shellder: Water / National Dex #0090',
          'Cloyster: Water/Ice / National Dex #0091',
          'Gastly: Ghost/Poison / National Dex #0092',
          'Haunter: Ghost/Poison / National Dex #0093',
          'Gengar: Ghost/Poison / National Dex #0094',
          'Onix: Rock/Ground / National Dex #0095',
          'Drowzee: Psychic / National Dex #0096',
          'Hypno: Psychic / National Dex #0097',
          'Krabby: Water / National Dex #0098',
          'Kingler: Water / National Dex #0099',
          'Voltorb: Electric / National Dex #0100',
          'Electrode: Electric / National Dex #0101',
          'Exeggcute: Grass/Psychic / National Dex #0102',
          'Exeggutor: Grass/Psychic / National Dex #0103',
          'Cubone: Ground / National Dex #0104',
          'Marowak: Ground / National Dex #0105',
          'Hitmonlee: Fighting / National Dex #0106',
          'Hitmonchan: Fighting / National Dex #0107',
          'Lickitung: Normal / National Dex #0108',
          'Koffing: Poison / National Dex #0109',
          'Weezing: Poison / National Dex #0110',
          'Rhyhorn: Ground/Rock / National Dex #0111',
          'Rhydon: Ground/Rock / National Dex #0112',
          'Chansey: Normal / National Dex #0113',
          'Tangela: Grass / National Dex #0114',
          'Kangaskhan: Normal / National Dex #0115',
          'Horsea: Water / National Dex #0116',
          'Seadra: Water / National Dex #0117',
          'Goldeen: Water / National Dex #0118',
          'Seaking: Water / National Dex #0119',
          'Staryu: Water / National Dex #0120',
          'Starmie: Water/Psychic / National Dex #0121',
          'Mr. Mime: Psychic/Fairy / National Dex #0122',
          'Scyther: Bug/Flying / National Dex #0123',
          'Jynx: Ice/Psychic / National Dex #0124',
          'Electabuzz: Electric / National Dex #0125',
          'Magmar: Fire / National Dex #0126',
          'Pinsir: Bug / National Dex #0127',
          'Tauros: Normal / National Dex #0128',
          'Magikarp: Water / National Dex #0129',
          'Gyarados: Water/Flying / National Dex #0130',
          'Lapras: Water/Ice / National Dex #0131',
          'Ditto: Normal / National Dex #0132',
          'Eevee: Normal / National Dex #0133',
          'Vaporeon: Water / National Dex #0134',
          'Jolteon: Electric / National Dex #0135',
          'Flareon: Fire / National Dex #0136',
          'Porygon: Normal / National Dex #0137',
          'Omanyte: Rock/Water / National Dex #0138',
          'Omastar: Rock/Water / National Dex #0139',
          'Kabuto: Rock/Water / National Dex #0140',
          'Kabutops: Rock/Water / National Dex #0141',
          'Aerodactyl: Rock/Flying / National Dex #0142',
          'Snorlax: Normal / National Dex #0143',
          'Articuno: Ice/Flying / National Dex #0144',
          'Zapdos: Electric/Flying / National Dex #0145',
          'Moltres: Fire/Flying / National Dex #0146',
          'Dratini: Dragon / National Dex #0147',
          'Dragonair: Dragon / National Dex #0148',
          'Dragonite: Dragon/Flying / National Dex #0149',
          'Mewtwo: Psychic / National Dex #0150',
          'Mew: Psychic / National Dex #0151',
          'Chikorita: Grass / National Dex #0152',
          'Bayleef: Grass / National Dex #0153',
          'Meganium: Grass / National Dex #0154',
          'Cyndaquil: Fire / National Dex #0155',
          'Quilava: Fire / National Dex #0156',
          'Typhlosion: Fire / National Dex #0157',
          'Totodile: Water / National Dex #0158',
          'Croconaw: Water / National Dex #0159',
          'Feraligatr: Water / National Dex #0160',
          'Sentret: Normal / National Dex #0161',
          'Furret: Normal / National Dex #0162',
          'Hoothoot: Normal/Flying / National Dex #0163',
          'Noctowl: Normal/Flying / National Dex #0164',
          'Ledyba: Bug/Flying / National Dex #0165',
          'Ledian: Bug/Flying / National Dex #0166',
          'Spinarak: Bug/Poison / National Dex #0167',
          'Ariados: Bug/Poison / National Dex #0168',
          'Crobat: Poison/Flying / National Dex #0169',
          'Chinchou: Water/Electric / National Dex #0170',
          'Lanturn: Water/Electric / National Dex #0171',
          'Pichu: Electric / National Dex #0172',
          'Cleffa: Fairy / National Dex #0173',
          'Igglybuff: Normal/Fairy / National Dex #0174',
          'Togepi: Fairy / National Dex #0175',
          'Togetic: Fairy/Flying / National Dex #0176',
          'Natu: Psychic/Flying / National Dex #0177',
          'Xatu: Psychic/Flying / National Dex #0178',
          'Mareep: Electric / National Dex #0179',
          'Flaaffy: Electric / National Dex #0180',
          'Ampharos: Electric / National Dex #0181',
          'Bellossom: Grass / National Dex #0182',
          'Marill: Water/Fairy / National Dex #0183',
          'Azumarill: Water/Fairy / National Dex #0184',
          'Sudowoodo: Rock / National Dex #0185',
          'Politoed: Water / National Dex #0186',
          'Hoppip: Grass/Flying / National Dex #0187',
          'Skiploom: Grass/Flying / National Dex #0188',
          'Jumpluff: Grass/Flying / National Dex #0189',
          'Aipom: Normal / National Dex #0190',
          'Sunkern: Grass / National Dex #0191',
          'Sunflora: Grass / National Dex #0192',
          'Yanma: Bug/Flying / National Dex #0193',
          'Wooper: Water/Ground / National Dex #0194',
          'Quagsire: Water/Ground / National Dex #0195',
          'Espeon: Psychic / National Dex #0196',
          'Umbreon: Dark / National Dex #0197',
          'Murkrow: Dark/Flying / National Dex #0198',
          'Slowking: Water/Psychic / National Dex #0199',
          'Misdreavus: Ghost / National Dex #0200',
          'Unown: Psychic / National Dex #0201',
          'Wobbuffet: Psychic / National Dex #0202',
          'Girafarig: Normal/Psychic / National Dex #0203',
          'Pineco: Bug / National Dex #0204',
          'Forretress: Bug/Steel / National Dex #0205',
          'Dunsparce: Normal / National Dex #0206',
          'Gligar: Ground/Flying / National Dex #0207',
          'Steelix: Steel/Ground / National Dex #0208',
          'Snubbull: Fairy / National Dex #0209',
          'Granbull: Fairy / National Dex #0210',
          'Qwilfish: Water/Poison / National Dex #0211',
          'Scizor: Bug/Steel / National Dex #0212',
          'Shuckle: Bug/Rock / National Dex #0213',
          'Heracross: Bug/Fighting / National Dex #0214',
          'Sneasel: Dark/Ice / National Dex #0215',
          'Teddiursa: Normal / National Dex #0216',
          'Ursaring: Normal / National Dex #0217',
          'Slugma: Fire / National Dex #0218',
          'Magcargo: Fire/Rock / National Dex #0219',
          'Swinub: Ice/Ground / National Dex #0220',
          'Piloswine: Ice/Ground / National Dex #0221',
          'Corsola: Water/Rock / National Dex #0222',
          'Remoraid: Water / National Dex #0223',
          'Octillery: Water / National Dex #0224',
          'Delibird: Ice/Flying / National Dex #0225',
          'Mantine: Water/Flying / National Dex #0226',
          'Skarmory: Steel/Flying / National Dex #0227',
          'Houndour: Dark/Fire / National Dex #0228',
          'Houndoom: Dark/Fire / National Dex #0229',
          'Kingdra: Water/Dragon / National Dex #0230',
          'Phanpy: Ground / National Dex #0231',
          'Donphan: Ground / National Dex #0232',
          'Porygon2: Normal / National Dex #0233',
          'Stantler: Normal / National Dex #0234',
          'Smeargle: Normal / National Dex #0235',
          'Tyrogue: Fighting / National Dex #0236',
          'Hitmontop: Fighting / National Dex #0237',
          'Smoochum: Ice/Psychic / National Dex #0238',
          'Elekid: Electric / National Dex #0239',
          'Magby: Fire / National Dex #0240',
          'Miltank: Normal / National Dex #0241',
          'Blissey: Normal / National Dex #0242',
          'Raikou: Electric / National Dex #0243',
          'Entei: Fire / National Dex #0244',
          'Suicune: Water / National Dex #0245',
          'Larvitar: Rock/Ground / National Dex #0246',
          'Pupitar: Rock/Ground / National Dex #0247',
          'Tyranitar: Rock/Dark / National Dex #0248',
          'Lugia: Psychic/Flying / National Dex #0249',
          'Ho-Oh: Fire/Flying / National Dex #0250',
          'Celebi: Psychic/Grass / National Dex #0251',
          'Treecko: Grass / National Dex #0252',
          'Grovyle: Grass / National Dex #0253',
          'Sceptile: Grass / National Dex #0254',
          'Torchic: Fire / National Dex #0255',
          'Combusken: Fire/Fighting / National Dex #0256',
          'Blaziken: Fire/Fighting / National Dex #0257',
          'Mudkip: Water / National Dex #0258',
          'Marshtomp: Water/Ground / National Dex #0259',
          'Swampert: Water/Ground / National Dex #0260',
          'Poochyena: Dark / National Dex #0261',
          'Mightyena: Dark / National Dex #0262',
          'Zigzagoon: Normal / National Dex #0263',
          'Linoone: Normal / National Dex #0264',
          'Wurmple: Bug / National Dex #0265',
          'Silcoon: Bug / National Dex #0266',
          'Beautifly: Bug/Flying / National Dex #0267',
          'Cascoon: Bug / National Dex #0268',
          'Dustox: Bug/Poison / National Dex #0269',
          'Lotad: Water/Grass / National Dex #0270',
          'Lombre: Water/Grass / National Dex #0271',
          'Ludicolo: Water/Grass / National Dex #0272',
          'Seedot: Grass / National Dex #0273',
          'Nuzleaf: Grass/Dark / National Dex #0274',
          'Shiftry: Grass/Dark / National Dex #0275',
          'Taillow: Normal/Flying / National Dex #0276',
          'Swellow: Normal/Flying / National Dex #0277',
          'Wingull: Water/Flying / National Dex #0278',
          'Pelipper: Water/Flying / National Dex #0279',
          'Ralts: Psychic/Fairy / National Dex #0280',
          'Kirlia: Psychic/Fairy / National Dex #0281',
          'Gardevoir: Psychic/Fairy / National Dex #0282',
          'Surskit: Bug/Water / National Dex #0283',
          'Masquerain: Bug/Flying / National Dex #0284',
          'Shroomish: Grass / National Dex #0285',
          'Breloom: Grass/Fighting / National Dex #0286',
          'Slakoth: Normal / National Dex #0287',
          'Vigoroth: Normal / National Dex #0288',
          'Slaking: Normal / National Dex #0289',
          'Nincada: Bug/Ground / National Dex #0290',
          'Ninjask: Bug/Flying / National Dex #0291',
          'Shedinja: Bug/Ghost / National Dex #0292',
          'Whismur: Normal / National Dex #0293',
          'Loudred: Normal / National Dex #0294',
          'Exploud: Normal / National Dex #0295',
          'Makuhita: Fighting / National Dex #0296',
          'Hariyama: Fighting / National Dex #0297',
          'Azurill: Normal/Fairy / National Dex #0298',
          'Nosepass: Rock / National Dex #0299',
          'Skitty: Normal / National Dex #0300',
          'Delcatty: Normal / National Dex #0301',
          'Sableye: Dark/Ghost / National Dex #0302',
          'Mawile: Steel/Fairy / National Dex #0303',
          'Aron: Steel/Rock / National Dex #0304',
          'Lairon: Steel/Rock / National Dex #0305',
          'Aggron: Steel/Rock / National Dex #0306',
          'Meditite: Fighting/Psychic / National Dex #0307',
          'Medicham: Fighting/Psychic / National Dex #0308',
          'Electrike: Electric / National Dex #0309',
          'Manectric: Electric / National Dex #0310',
          'Plusle: Electric / National Dex #0311',
          'Minun: Electric / National Dex #0312',
          'Volbeat: Bug / National Dex #0313',
          'Illumise: Bug / National Dex #0314',
          'Roselia: Grass/Poison / National Dex #0315',
          'Gulpin: Poison / National Dex #0316',
          'Swalot: Poison / National Dex #0317',
          'Carvanha: Water/Dark / National Dex #0318',
          'Sharpedo: Water/Dark / National Dex #0319',
          'Wailmer: Water / National Dex #0320',
          'Wailord: Water / National Dex #0321',
          'Numel: Fire/Ground / National Dex #0322',
          'Camerupt: Fire/Ground / National Dex #0323',
          'Torkoal: Fire / National Dex #0324',
          'Spoink: Psychic / National Dex #0325',
          'Grumpig: Psychic / National Dex #0326',
          'Spinda: Normal / National Dex #0327',
          'Trapinch: Ground / National Dex #0328',
          'Vibrava: Ground/Dragon / National Dex #0329',
          'Flygon: Ground/Dragon / National Dex #0330',
          'Cacnea: Grass / National Dex #0331',
          'Cacturne: Grass/Dark / National Dex #0332',
          'Swablu: Normal/Flying / National Dex #0333',
          'Altaria: Dragon/Flying / National Dex #0334',
          'Zangoose: Normal / National Dex #0335',
          'Seviper: Poison / National Dex #0336',
          'Lunatone: Rock/Psychic / National Dex #0337',
          'Solrock: Rock/Psychic / National Dex #0338',
          'Barboach: Water/Ground / National Dex #0339',
          'Whiscash: Water/Ground / National Dex #0340',
          'Corphish: Water / National Dex #0341',
          'Crawdaunt: Water/Dark / National Dex #0342',
          'Baltoy: Ground/Psychic / National Dex #0343',
          'Claydol: Ground/Psychic / National Dex #0344',
          'Lileep: Rock/Grass / National Dex #0345',
          'Cradily: Rock/Grass / National Dex #0346',
          'Anorith: Rock/Bug / National Dex #0347',
          'Armaldo: Rock/Bug / National Dex #0348',
          'Feebas: Water / National Dex #0349',
          'Milotic: Water / National Dex #0350',
          'Castform: Normal / National Dex #0351',
          'Kecleon: Normal / National Dex #0352',
          'Shuppet: Ghost / National Dex #0353',
          'Banette: Ghost / National Dex #0354',
          'Duskull: Ghost / National Dex #0355',
          'Dusclops: Ghost / National Dex #0356',
          'Tropius: Grass/Flying / National Dex #0357',
          'Chimecho: Psychic / National Dex #0358',
          'Absol: Dark / National Dex #0359',
          'Wynaut: Psychic / National Dex #0360',
          'Snorunt: Ice / National Dex #0361',
          'Glalie: Ice / National Dex #0362',
          'Spheal: Ice/Water / National Dex #0363',
          'Sealeo: Ice/Water / National Dex #0364',
          'Walrein: Ice/Water / National Dex #0365',
          'Clamperl: Water / National Dex #0366',
          'Huntail: Water / National Dex #0367',
          'Gorebyss: Water / National Dex #0368',
          'Relicanth: Water/Rock / National Dex #0369',
          'Luvdisc: Water / National Dex #0370',
          'Bagon: Dragon / National Dex #0371',
          'Shelgon: Dragon / National Dex #0372',
          'Salamence: Dragon/Flying / National Dex #0373',
          'Beldum: Steel/Psychic / National Dex #0374',
          'Metang: Steel/Psychic / National Dex #0375',
          'Metagross: Steel/Psychic / National Dex #0376',
          'Regirock: Rock / National Dex #0377',
          'Regice: Ice / National Dex #0378',
          'Registeel: Steel / National Dex #0379',
          'Latias: Dragon/Psychic / National Dex #0380',
          'Latios: Dragon/Psychic / National Dex #0381',
          'Kyogre: Water / National Dex #0382',
          'Groudon: Ground / National Dex #0383',
          'Rayquaza: Dragon/Flying / National Dex #0384',
          'Jirachi: Steel/Psychic / National Dex #0385',
          'Deoxys: Psychic / National Dex #0386',
          'Turtwig: Grass / National Dex #0387',
          'Grotle: Grass / National Dex #0388',
          'Torterra: Grass/Ground / National Dex #0389',
          'Chimchar: Fire / National Dex #0390',
          'Monferno: Fire/Fighting / National Dex #0391',
          'Infernape: Fire/Fighting / National Dex #0392',
          'Piplup: Water / National Dex #0393',
          'Prinplup: Water / National Dex #0394',
          'Empoleon: Water/Steel / National Dex #0395',
          'Starly: Normal/Flying / National Dex #0396',
          'Staravia: Normal/Flying / National Dex #0397',
          'Staraptor: Normal/Flying / National Dex #0398',
          'Bidoof: Normal / National Dex #0399',
          'Bibarel: Normal/Water / National Dex #0400',
          'Kricketot: Bug / National Dex #0401',
          'Kricketune: Bug / National Dex #0402',
          'Shinx: Electric / National Dex #0403',
          'Luxio: Electric / National Dex #0404',
          'Luxray: Electric / National Dex #0405',
          'Budew: Grass/Poison / National Dex #0406',
          'Roserade: Grass/Poison / National Dex #0407',
          'Cranidos: Rock / National Dex #0408',
          'Rampardos: Rock / National Dex #0409',
          'Shieldon: Rock/Steel / National Dex #0410',
          'Bastiodon: Rock/Steel / National Dex #0411',
          'Burmy: Bug / National Dex #0412',
          'Wormadam: Bug/Grass / National Dex #0413',
          'Mothim: Bug/Flying / National Dex #0414',
          'Combee: Bug/Flying / National Dex #0415',
          'Vespiquen: Bug/Flying / National Dex #0416',
          'Pachirisu: Electric / National Dex #0417',
          'Buizel: Water / National Dex #0418',
          'Floatzel: Water / National Dex #0419',
          'Cherubi: Grass / National Dex #0420',
          'Cherrim: Grass / National Dex #0421',
          'Shellos: Water / National Dex #0422',
          'Gastrodon: Water/Ground / National Dex #0423',
          'Ambipom: Normal / National Dex #0424',
          'Drifloon: Ghost/Flying / National Dex #0425',
          'Drifblim: Ghost/Flying / National Dex #0426',
          'Buneary: Normal / National Dex #0427',
          'Lopunny: Normal / National Dex #0428',
          'Mismagius: Ghost / National Dex #0429',
          'Honchkrow: Dark/Flying / National Dex #0430',
          'Glameow: Normal / National Dex #0431',
          'Purugly: Normal / National Dex #0432',
          'Chingling: Psychic / National Dex #0433',
          'Stunky: Poison/Dark / National Dex #0434',
          'Skuntank: Poison/Dark / National Dex #0435',
          'Bronzor: Steel/Psychic / National Dex #0436',
          'Bronzong: Steel/Psychic / National Dex #0437',
          'Bonsly: Rock / National Dex #0438',
          'Mime Jr.: Psychic/Fairy / National Dex #0439',
          'Happiny: Normal / National Dex #0440',
          'Chatot: Normal/Flying / National Dex #0441',
          'Spiritomb: Ghost/Dark / National Dex #0442',
          'Gible: Dragon/Ground / National Dex #0443',
          'Gabite: Dragon/Ground / National Dex #0444',
          'Garchomp: Dragon/Ground / National Dex #0445',
          'Munchlax: Normal / National Dex #0446',
          'Riolu: Fighting / National Dex #0447',
          'Lucario: Fighting/Steel / National Dex #0448',
          'Hippopotas: Ground / National Dex #0449',
          'Hippowdon: Ground / National Dex #0450',
          'Skorupi: Poison/Bug / National Dex #0451',
          'Drapion: Poison/Dark / National Dex #0452',
          'Croagunk: Poison/Fighting / National Dex #0453',
          'Toxicroak: Poison/Fighting / National Dex #0454',
          'Carnivine: Grass / National Dex #0455',
          'Finneon: Water / National Dex #0456',
          'Lumineon: Water / National Dex #0457',
          'Mantyke: Water/Flying / National Dex #0458',
          'Snover: Grass/Ice / National Dex #0459',
          'Abomasnow: Grass/Ice / National Dex #0460',
          'Weavile: Dark/Ice / National Dex #0461',
          'Magnezone: Electric/Steel / National Dex #0462',
          'Lickilicky: Normal / National Dex #0463',
          'Rhyperior: Ground/Rock / National Dex #0464',
          'Tangrowth: Grass / National Dex #0465',
          'Electivire: Electric / National Dex #0466',
          'Magmortar: Fire / National Dex #0467',
          'Togekiss: Fairy/Flying / National Dex #0468',
          'Yanmega: Bug/Flying / National Dex #0469',
          'Leafeon: Grass / National Dex #0470',
          'Glaceon: Ice / National Dex #0471',
          'Gliscor: Ground/Flying / National Dex #0472',
          'Mamoswine: Ice/Ground / National Dex #0473',
          'Porygon-Z: Normal / National Dex #0474',
          'Gallade: Psychic/Fighting / National Dex #0475',
          'Probopass: Rock/Steel / National Dex #0476',
          'Dusknoir: Ghost / National Dex #0477',
          'Froslass: Ice/Ghost / National Dex #0478',
          'Rotom: Electric/Ghost / National Dex #0479',
          'Uxie: Psychic / National Dex #0480',
          'Mesprit: Psychic / National Dex #0481',
          'Azelf: Psychic / National Dex #0482',
          'Dialga: Steel/Dragon / National Dex #0483',
          'Palkia: Water/Dragon / National Dex #0484',
          'Heatran: Fire/Steel / National Dex #0485',
          'Regigigas: Normal / National Dex #0486',
          'Giratina: Ghost/Dragon / National Dex #0487',
          'Cresselia: Psychic / National Dex #0488',
          'Phione: Water / National Dex #0489',
          'Manaphy: Water / National Dex #0490',
          'Darkrai: Dark / National Dex #0491',
          'Shaymin: Grass / National Dex #0492',
          'Arceus: Normal / National Dex #0493',
          'Victini: Psychic/Fire / National Dex #0494',
          'Snivy: Grass / National Dex #0495',
          'Servine: Grass / National Dex #0496',
          'Serperior: Grass / National Dex #0497',
          'Tepig: Fire / National Dex #0498',
          'Pignite: Fire/Fighting / National Dex #0499',
          'Emboar: Fire/Fighting / National Dex #0500',
          'Oshawott: Water / National Dex #0501',
          'Dewott: Water / National Dex #0502',
          'Samurott: Water / National Dex #0503',
          'Patrat: Normal / National Dex #0504',
          'Watchog: Normal / National Dex #0505',
          'Lillipup: Normal / National Dex #0506',
          'Herdier: Normal / National Dex #0507',
          'Stoutland: Normal / National Dex #0508',
          'Purrloin: Dark / National Dex #0509',
          'Liepard: Dark / National Dex #0510',
          'Pansage: Grass / National Dex #0511',
          'Simisage: Grass / National Dex #0512',
          'Pansear: Fire / National Dex #0513',
          'Simisear: Fire / National Dex #0514',
          'Panpour: Water / National Dex #0515',
          'Simipour: Water / National Dex #0516',
          'Munna: Psychic / National Dex #0517',
          'Musharna: Psychic / National Dex #0518',
          'Pidove: Normal/Flying / National Dex #0519',
          'Tranquill: Normal/Flying / National Dex #0520',
          'Unfezant: Normal/Flying / National Dex #0521',
          'Blitzle: Electric / National Dex #0522',
          'Zebstrika: Electric / National Dex #0523',
          'Roggenrola: Rock / National Dex #0524',
          'Boldore: Rock / National Dex #0525',
          'Gigalith: Rock / National Dex #0526',
          'Woobat: Psychic/Flying / National Dex #0527',
          'Swoobat: Psychic/Flying / National Dex #0528',
          'Drilbur: Ground / National Dex #0529',
          'Excadrill: Ground/Steel / National Dex #0530',
          'Audino: Normal / National Dex #0531',
          'Timburr: Fighting / National Dex #0532',
          'Gurdurr: Fighting / National Dex #0533',
          'Conkeldurr: Fighting / National Dex #0534',
          'Tympole: Water / National Dex #0535',
          'Palpitoad: Water/Ground / National Dex #0536',
          'Seismitoad: Water/Ground / National Dex #0537',
          'Throh: Fighting / National Dex #0538',
          'Sawk: Fighting / National Dex #0539',
          'Sewaddle: Bug/Grass / National Dex #0540',
          'Swadloon: Bug/Grass / National Dex #0541',
          'Leavanny: Bug/Grass / National Dex #0542',
          'Venipede: Bug/Poison / National Dex #0543',
          'Whirlipede: Bug/Poison / National Dex #0544',
          'Scolipede: Bug/Poison / National Dex #0545',
          'Cottonee: Grass/Fairy / National Dex #0546',
          'Whimsicott: Grass/Fairy / National Dex #0547',
          'Petilil: Grass / National Dex #0548',
          'Lilligant: Grass / National Dex #0549',
          'Basculin: Water / National Dex #0550',
          'Sandile: Ground/Dark / National Dex #0551',
          'Krokorok: Ground/Dark / National Dex #0552',
          'Krookodile: Ground/Dark / National Dex #0553',
          'Darumaka: Fire / National Dex #0554',
          'Darmanitan: Fire / National Dex #0555',
          'Maractus: Grass / National Dex #0556',
          'Dwebble: Bug/Rock / National Dex #0557',
          'Crustle: Bug/Rock / National Dex #0558',
          'Scraggy: Dark/Fighting / National Dex #0559',
          'Scrafty: Dark/Fighting / National Dex #0560',
          'Sigilyph: Psychic/Flying / National Dex #0561',
          'Yamask: Ghost / National Dex #0562',
          'Cofagrigus: Ghost / National Dex #0563',
          'Tirtouga: Water/Rock / National Dex #0564',
          'Carracosta: Water/Rock / National Dex #0565',
          'Archen: Rock/Flying / National Dex #0566',
          'Archeops: Rock/Flying / National Dex #0567',
          'Trubbish: Poison / National Dex #0568',
          'Garbodor: Poison / National Dex #0569',
          'Zorua: Dark / National Dex #0570',
          'Zoroark: Dark / National Dex #0571',
          'Minccino: Normal / National Dex #0572',
          'Cinccino: Normal / National Dex #0573',
          'Gothita: Psychic / National Dex #0574',
          'Gothorita: Psychic / National Dex #0575',
          'Gothitelle: Psychic / National Dex #0576',
          'Solosis: Psychic / National Dex #0577',
          'Duosion: Psychic / National Dex #0578',
          'Reuniclus: Psychic / National Dex #0579',
          'Ducklett: Water/Flying / National Dex #0580',
          'Swanna: Water/Flying / National Dex #0581',
          'Vanillite: Ice / National Dex #0582',
          'Vanillish: Ice / National Dex #0583',
          'Vanilluxe: Ice / National Dex #0584',
          'Deerling: Normal/Grass / National Dex #0585',
          'Sawsbuck: Normal/Grass / National Dex #0586',
          'Emolga: Electric/Flying / National Dex #0587',
          'Karrablast: Bug / National Dex #0588',
          'Escavalier: Bug/Steel / National Dex #0589',
          'Foongus: Grass/Poison / National Dex #0590',
          'Amoonguss: Grass/Poison / National Dex #0591',
          'Frillish: Water/Ghost / National Dex #0592',
          'Jellicent: Water/Ghost / National Dex #0593',
          'Alomomola: Water / National Dex #0594',
          'Joltik: Bug/Electric / National Dex #0595',
          'Galvantula: Bug/Electric / National Dex #0596',
          'Ferroseed: Grass/Steel / National Dex #0597',
          'Ferrothorn: Grass/Steel / National Dex #0598',
          'Klink: Steel / National Dex #0599',
          'Klang: Steel / National Dex #0600',
          'Klinklang: Steel / National Dex #0601',
          'Tynamo: Electric / National Dex #0602',
          'Eelektrik: Electric / National Dex #0603',
          'Eelektross: Electric / National Dex #0604',
          'Elgyem: Psychic / National Dex #0605',
          'Beheeyem: Psychic / National Dex #0606',
          'Litwick: Ghost/Fire / National Dex #0607',
          'Lampent: Ghost/Fire / National Dex #0608',
          'Chandelure: Ghost/Fire / National Dex #0609',
          'Axew: Dragon / National Dex #0610',
          'Fraxure: Dragon / National Dex #0611',
          'Haxorus: Dragon / National Dex #0612',
          'Cubchoo: Ice / National Dex #0613',
          'Beartic: Ice / National Dex #0614',
          'Cryogonal: Ice / National Dex #0615',
          'Shelmet: Bug / National Dex #0616',
          'Accelgor: Bug / National Dex #0617',
          'Stunfisk: Ground/Electric / National Dex #0618',
          'Mienfoo: Fighting / National Dex #0619',
          'Mienshao: Fighting / National Dex #0620',
          'Druddigon: Dragon / National Dex #0621',
          'Golett: Ground/Ghost / National Dex #0622',
          'Golurk: Ground/Ghost / National Dex #0623',
          'Pawniard: Dark/Steel / National Dex #0624',
          'Bisharp: Dark/Steel / National Dex #0625',
          'Bouffalant: Normal / National Dex #0626',
          'Rufflet: Normal/Flying / National Dex #0627',
          'Braviary: Normal/Flying / National Dex #0628',
          'Vullaby: Dark/Flying / National Dex #0629',
          'Mandibuzz: Dark/Flying / National Dex #0630',
          'Heatmor: Fire / National Dex #0631',
          'Durant: Bug/Steel / National Dex #0632',
          'Deino: Dark/Dragon / National Dex #0633',
          'Zweilous: Dark/Dragon / National Dex #0634',
          'Hydreigon: Dark/Dragon / National Dex #0635',
          'Larvesta: Bug/Fire / National Dex #0636',
          'Volcarona: Bug/Fire / National Dex #0637',
          'Cobalion: Steel/Fighting / National Dex #0638',
          'Terrakion: Rock/Fighting / National Dex #0639',
          'Virizion: Grass/Fighting / National Dex #0640',
          'Tornadus: Flying / National Dex #0641',
          'Thundurus: Electric/Flying / National Dex #0642',
          'Reshiram: Dragon/Fire / National Dex #0643',
          'Zekrom: Dragon/Electric / National Dex #0644',
          'Landorus: Ground/Flying / National Dex #0645',
          'Kyurem: Dragon/Ice / National Dex #0646',
          'Keldeo: Water/Fighting / National Dex #0647',
          'Meloetta: Normal/Psychic / National Dex #0648',
          'Genesect: Bug/Steel / National Dex #0649',
          'Chespin: Grass / National Dex #0650',
          'Quilladin: Grass / National Dex #0651',
          'Chesnaught: Grass/Fighting / National Dex #0652',
          'Fennekin: Fire / National Dex #0653',
          'Braixen: Fire / National Dex #0654',
          'Delphox: Fire/Psychic / National Dex #0655',
          'Froakie: Water / National Dex #0656',
          'Frogadier: Water / National Dex #0657',
          'Greninja: Water/Dark / National Dex #0658',
          'Bunnelby: Normal / National Dex #0659',
          'Diggersby: Normal/Ground / National Dex #0660',
          'Fletchling: Normal/Flying / National Dex #0661',
          'Fletchinder: Fire/Flying / National Dex #0662',
          'Talonflame: Fire/Flying / National Dex #0663',
          'Scatterbug: Bug / National Dex #0664',
          'Spewpa: Bug / National Dex #0665',
          'Vivillon: Bug/Flying / National Dex #0666',
          'Litleo: Fire/Normal / National Dex #0667',
          'Pyroar: Fire/Normal / National Dex #0668',
          'Flabébé: Fairy / National Dex #0669',
          'Floette: Fairy / National Dex #0670',
          'Florges: Fairy / National Dex #0671',
          'Skiddo: Grass / National Dex #0672',
          'Gogoat: Grass / National Dex #0673',
          'Pancham: Fighting / National Dex #0674',
          'Pangoro: Fighting/Dark / National Dex #0675',
          'Furfrou: Normal / National Dex #0676',
          'Espurr: Psychic / National Dex #0677',
          'Meowstic: Psychic / National Dex #0678',
          'Honedge: Steel/Ghost / National Dex #0679',
          'Doublade: Steel/Ghost / National Dex #0680',
          'Aegislash: Steel/Ghost / National Dex #0681',
          'Spritzee: Fairy / National Dex #0682',
          'Aromatisse: Fairy / National Dex #0683',
          'Swirlix: Fairy / National Dex #0684',
          'Slurpuff: Fairy / National Dex #0685',
          'Inkay: Dark/Psychic / National Dex #0686',
          'Malamar: Dark/Psychic / National Dex #0687',
          'Binacle: Rock/Water / National Dex #0688',
          'Barbaracle: Rock/Water / National Dex #0689',
          'Skrelp: Poison/Water / National Dex #0690',
          'Dragalge: Poison/Dragon / National Dex #0691',
          'Clauncher: Water / National Dex #0692',
          'Clawitzer: Water / National Dex #0693',
          'Helioptile: Electric/Normal / National Dex #0694',
          'Heliolisk: Electric/Normal / National Dex #0695',
          'Tyrunt: Rock/Dragon / National Dex #0696',
          'Tyrantrum: Rock/Dragon / National Dex #0697',
          'Amaura: Rock/Ice / National Dex #0698',
          'Aurorus: Rock/Ice / National Dex #0699',
          'Sylveon: Fairy / National Dex #0700',
          'Hawlucha: Fighting/Flying / National Dex #0701',
          'Dedenne: Electric/Fairy / National Dex #0702',
          'Carbink: Rock/Fairy / National Dex #0703',
          'Goomy: Dragon / National Dex #0704',
          'Sliggoo: Dragon / National Dex #0705',
          'Goodra: Dragon / National Dex #0706',
          'Klefki: Steel/Fairy / National Dex #0707',
          'Phantump: Ghost/Grass / National Dex #0708',
          'Trevenant: Ghost/Grass / National Dex #0709',
          'Pumpkaboo: Ghost/Grass / National Dex #0710',
          'Gourgeist: Ghost/Grass / National Dex #0711',
          'Bergmite: Ice / National Dex #0712',
          'Avalugg: Ice / National Dex #0713',
          'Noibat: Flying/Dragon / National Dex #0714',
          'Noivern: Flying/Dragon / National Dex #0715',
          'Xerneas: Fairy / National Dex #0716',
          'Yveltal: Dark/Flying / National Dex #0717',
          'Zygarde: Dragon/Ground / National Dex #0718',
          'Diancie: Rock/Fairy / National Dex #0719',
          'Hoopa: Psychic/Ghost / National Dex #0720',
          'Volcanion: Fire/Water / National Dex #0721',
          'Rowlet: Grass/Flying / National Dex #0722',
          'Dartrix: Grass/Flying / National Dex #0723',
          'Decidueye: Grass/Ghost / National Dex #0724',
          'Litten: Fire / National Dex #0725',
          'Torracat: Fire / National Dex #0726',
          'Incineroar: Fire/Dark / National Dex #0727',
          'Popplio: Water / National Dex #0728',
          'Brionne: Water / National Dex #0729',
          'Primarina: Water/Fairy / National Dex #0730',
          'Pikipek: Normal/Flying / National Dex #0731',
          'Trumbeak: Normal/Flying / National Dex #0732',
          'Toucannon: Normal/Flying / National Dex #0733',
          'Yungoos: Normal / National Dex #0734',
          'Gumshoos: Normal / National Dex #0735',
          'Grubbin: Bug / National Dex #0736',
          'Charjabug: Bug/Electric / National Dex #0737',
          'Vikavolt: Bug/Electric / National Dex #0738',
          'Crabrawler: Fighting / National Dex #0739',
          'Crabominable: Fighting/Ice / National Dex #0740',
          'Oricorio: Fire/Flying / National Dex #0741',
          'Cutiefly: Bug/Fairy / National Dex #0742',
          'Ribombee: Bug/Fairy / National Dex #0743',
          'Rockruff: Rock / National Dex #0744',
          'Lycanroc: Rock / National Dex #0745',
          'Wishiwashi: Water / National Dex #0746',
          'Mareanie: Poison/Water / National Dex #0747',
          'Toxapex: Poison/Water / National Dex #0748',
          'Mudbray: Ground / National Dex #0749',
          'Mudsdale: Ground / National Dex #0750',
          'Dewpider: Water/Bug / National Dex #0751',
          'Araquanid: Water/Bug / National Dex #0752',
          'Fomantis: Grass / National Dex #0753',
          'Lurantis: Grass / National Dex #0754',
          'Morelull: Grass/Fairy / National Dex #0755',
          'Shiinotic: Grass/Fairy / National Dex #0756',
          'Salandit: Poison/Fire / National Dex #0757',
          'Salazzle: Poison/Fire / National Dex #0758',
          'Stufful: Normal/Fighting / National Dex #0759',
          'Bewear: Normal/Fighting / National Dex #0760',
          'Bounsweet: Grass / National Dex #0761',
          'Steenee: Grass / National Dex #0762',
          'Tsareena: Grass / National Dex #0763',
          'Comfey: Fairy / National Dex #0764',
          'Oranguru: Normal/Psychic / National Dex #0765',
          'Passimian: Fighting / National Dex #0766',
          'Wimpod: Bug/Water / National Dex #0767',
          'Golisopod: Bug/Water / National Dex #0768',
          'Sandygast: Ghost/Ground / National Dex #0769',
          'Palossand: Ghost/Ground / National Dex #0770',
          'Pyukumuku: Water / National Dex #0771',
          'Type: Null: Normal / National Dex #0772',
          'Silvally: Normal / National Dex #0773',
          'Minior: Rock/Flying / National Dex #0774',
          'Komala: Normal / National Dex #0775',
          'Turtonator: Fire/Dragon / National Dex #0776',
          'Togedemaru: Electric/Steel / National Dex #0777',
          'Mimikyu: Ghost/Fairy / National Dex #0778',
          'Bruxish: Water/Psychic / National Dex #0779',
          'Drampa: Normal/Dragon / National Dex #0780',
          'Dhelmise: Ghost/Grass / National Dex #0781',
          'Jangmo-o: Dragon / National Dex #0782',
          'Hakamo-o: Dragon/Fighting / National Dex #0783',
          'Kommo-o: Dragon/Fighting / National Dex #0784',
          'Tapu Koko: Electric/Fairy / National Dex #0785',
          'Tapu Lele: Psychic/Fairy / National Dex #0786',
          'Tapu Bulu: Grass/Fairy / National Dex #0787',
          'Tapu Fini: Water/Fairy / National Dex #0788',
          'Cosmog: Psychic / National Dex #0789',
          'Cosmoem: Psychic / National Dex #0790',
          'Solgaleo: Psychic/Steel / National Dex #0791',
          'Lunala: Psychic/Ghost / National Dex #0792',
          'Nihilego: Rock/Poison / National Dex #0793',
          'Buzzwole: Bug/Fighting / National Dex #0794',
          'Pheromosa: Bug/Fighting / National Dex #0795',
          'Xurkitree: Electric / National Dex #0796',
          'Celesteela: Steel/Flying / National Dex #0797',
          'Kartana: Grass/Steel / National Dex #0798',
          'Guzzlord: Dark/Dragon / National Dex #0799',
          'Necrozma: Psychic / National Dex #0800',
          'Magearna: Steel/Fairy / National Dex #0801',
          'Marshadow: Fighting/Ghost / National Dex #0802',
          'Poipole: Poison / National Dex #0803',
          'Naganadel: Poison/Dragon / National Dex #0804',
          'Stakataka: Rock/Steel / National Dex #0805',
          'Blacephalon: Fire/Ghost / National Dex #0806',
          'Zeraora: Electric / National Dex #0807',
          'Meltan: Steel / National Dex #0808',
          'Melmetal: Steel / National Dex #0809',
          'Grookey: Grass / National Dex #0810',
          'Thwackey: Grass / National Dex #0811',
          'Rillaboom: Grass / National Dex #0812',
          'Scorbunny: Fire / National Dex #0813',
          'Raboot: Fire / National Dex #0814',
          'Cinderace: Fire / National Dex #0815',
          'Sobble: Water / National Dex #0816',
          'Drizzile: Water / National Dex #0817',
          'Inteleon: Water / National Dex #0818',
          'Skwovet: Normal / National Dex #0819',
          'Greedent: Normal / National Dex #0820',
          'Rookidee: Flying / National Dex #0821',
          'Corvisquire: Flying / National Dex #0822',
          'Corviknight: Flying/Steel / National Dex #0823',
          'Blipbug: Bug / National Dex #0824',
          'Dottler: Bug/Psychic / National Dex #0825',
          'Orbeetle: Bug/Psychic / National Dex #0826',
          'Nickit: Dark / National Dex #0827',
          'Thievul: Dark / National Dex #0828',
          'Gossifleur: Grass / National Dex #0829',
          'Eldegoss: Grass / National Dex #0830',
          'Wooloo: Normal / National Dex #0831',
          'Dubwool: Normal / National Dex #0832',
          'Chewtle: Water / National Dex #0833',
          'Drednaw: Water/Rock / National Dex #0834',
          'Yamper: Electric / National Dex #0835',
          'Boltund: Electric / National Dex #0836',
          'Rolycoly: Rock / National Dex #0837',
          'Carkol: Rock/Fire / National Dex #0838',
          'Coalossal: Rock/Fire / National Dex #0839',
          'Applin: Grass/Dragon / National Dex #0840',
          'Flapple: Grass/Dragon / National Dex #0841',
          'Appletun: Grass/Dragon / National Dex #0842',
          'Silicobra: Ground / National Dex #0843',
          'Sandaconda: Ground / National Dex #0844',
          'Cramorant: Flying/Water / National Dex #0845',
          'Arrokuda: Water / National Dex #0846',
          'Barraskewda: Water / National Dex #0847',
          'Toxel: Electric/Poison / National Dex #0848',
          'Toxtricity: Electric/Poison / National Dex #0849',
          'Sizzlipede: Fire/Bug / National Dex #0850',
          'Centiskorch: Fire/Bug / National Dex #0851',
          'Clobbopus: Fighting / National Dex #0852',
          'Grapploct: Fighting / National Dex #0853',
          'Sinistea: Ghost / National Dex #0854',
          'Polteageist: Ghost / National Dex #0855',
          'Hatenna: Psychic / National Dex #0856',
          'Hattrem: Psychic / National Dex #0857',
          'Hatterene: Psychic/Fairy / National Dex #0858',
          'Impidimp: Dark/Fairy / National Dex #0859',
          'Morgrem: Dark/Fairy / National Dex #0860',
          'Grimmsnarl: Dark/Fairy / National Dex #0861',
          'Obstagoon: Dark/Normal / National Dex #0862',
          'Perrserker: Steel / National Dex #0863',
          'Cursola: Ghost / National Dex #0864',
          'Sirfetch’d: Fighting / National Dex #0865',
          'Mr. Rime: Ice/Psychic / National Dex #0866',
          'Runerigus: Ground/Ghost / National Dex #0867',
          'Milcery: Fairy / National Dex #0868',
          'Alcremie: Fairy / National Dex #0869',
          'Falinks: Fighting / National Dex #0870',
          'Pincurchin: Electric / National Dex #0871',
          'Snom: Ice/Bug / National Dex #0872',
          'Frosmoth: Ice/Bug / National Dex #0873',
          'Stonjourner: Rock / National Dex #0874',
          'Eiscue: Ice / National Dex #0875',
          'Indeedee: Psychic/Normal / National Dex #0876',
          'Morpeko: Electric/Dark / National Dex #0877',
          'Cufant: Steel / National Dex #0878',
          'Copperajah: Steel / National Dex #0879',
          'Dracozolt: Electric/Dragon / National Dex #0880',
          'Arctozolt: Electric/Ice / National Dex #0881',
          'Dracovish: Water/Dragon / National Dex #0882',
          'Arctovish: Water/Ice / National Dex #0883',
          'Duraludon: Steel/Dragon / National Dex #0884',
          'Dreepy: Dragon/Ghost / National Dex #0885',
          'Drakloak: Dragon/Ghost / National Dex #0886',
          'Dragapult: Dragon/Ghost / National Dex #0887',
          'Zacian: Fairy / National Dex #0888',
          'Zamazenta: Fighting / National Dex #0889',
          'Eternatus: Poison/Dragon / National Dex #0890',
          'Kubfu: Fighting / National Dex #0891',
          'Urshifu: Fighting/Dark / National Dex #0892',
          'Zarude: Dark/Grass / National Dex #0893',
          'Regieleki: Electric / National Dex #0894',
          'Regidrago: Dragon / National Dex #0895',
          'Glastrier: Ice / National Dex #0896',
          'Spectrier: Ghost / National Dex #0897',
          'Calyrex: Psychic/Grass / National Dex #0898',
          'Wyrdeer: Normal/Psychic / National Dex #0899',
          'Kleavor: Bug/Rock / National Dex #0900',
          'Ursaluna: Ground/Normal / National Dex #0901',
          'Basculegion: Water/Ghost / National Dex #0902',
          'Sneasler: Fighting/Poison / National Dex #0903',
          'Overqwil: Dark/Poison / National Dex #0904',
          'Enamorus: Fairy/Flying / National Dex #0905',
          'Sprigatito: Grass / National Dex #0906',
          'Floragato: Grass / National Dex #0907',
          'Meowscarada: Grass/Dark / National Dex #0908',
          'Fuecoco: Fire / National Dex #0909',
          'Crocalor: Fire / National Dex #0910',
          'Skeledirge: Fire/Ghost / National Dex #0911',
          'Quaxly: Water / National Dex #0912',
          'Quaxwell: Water / National Dex #0913',
          'Quaquaval: Water/Fighting / National Dex #0914',
          'Lechonk: Normal / National Dex #0915',
          'Oinkologne: Normal / National Dex #0916',
          'Tarountula: Bug / National Dex #0917',
          'Spidops: Bug / National Dex #0918',
          'Nymble: Bug / National Dex #0919',
          'Lokix: Bug/Dark / National Dex #0920',
          'Pawmi: Electric / National Dex #0921',
          'Pawmo: Electric/Fighting / National Dex #0922',
          'Pawmot: Electric/Fighting / National Dex #0923',
          'Tandemaus: Normal / National Dex #0924',
          'Maushold: Normal / National Dex #0925',
          'Fidough: Fairy / National Dex #0926',
          'Dachsbun: Fairy / National Dex #0927',
          'Smoliv: Grass/Normal / National Dex #0928',
          'Dolliv: Grass/Normal / National Dex #0929',
          'Arboliva: Grass/Normal / National Dex #0930',
          'Squawkabilly: Normal/Flying / National Dex #0931',
          'Nacli: Rock / National Dex #0932',
          'Naclstack: Rock / National Dex #0933',
          'Garganacl: Rock / National Dex #0934',
          'Charcadet: Fire / National Dex #0935',
          'Armarouge: Fire/Psychic / National Dex #0936',
          'Ceruledge: Fire/Ghost / National Dex #0937',
          'Tadbulb: Electric / National Dex #0938',
          'Bellibolt: Electric / National Dex #0939',
          'Wattrel: Electric/Flying / National Dex #0940',
          'Kilowattrel: Electric/Flying / National Dex #0941',
          'Maschiff: Dark / National Dex #0942',
          'Mabosstiff: Dark / National Dex #0943',
          'Shroodle: Poison/Normal / National Dex #0944',
          'Grafaiai: Poison/Normal / National Dex #0945',
          'Bramblin: Grass/Ghost / National Dex #0946',
          'Brambleghast: Grass/Ghost / National Dex #0947',
          'Toedscool: Ground/Grass / National Dex #0948',
          'Toedscruel: Ground/Grass / National Dex #0949',
          'Klawf: Rock / National Dex #0950',
          'Capsakid: Grass / National Dex #0951',
          'Scovillain: Grass/Fire / National Dex #0952',
          'Rellor: Bug / National Dex #0953',
          'Rabsca: Bug/Psychic / National Dex #0954',
          'Flittle: Psychic / National Dex #0955',
          'Espathra: Psychic / National Dex #0956',
          'Tinkatink: Fairy/Steel / National Dex #0957',
          'Tinkatuff: Fairy/Steel / National Dex #0958',
          'Tinkaton: Fairy/Steel / National Dex #0959',
          'Wiglett: Water / National Dex #0960',
          'Wugtrio: Water / National Dex #0961',
          'Bombirdier: Flying/Dark / National Dex #0962',
          'Finizen: Water / National Dex #0963',
          'Palafin: Water / National Dex #0964',
          'Varoom: Steel/Poison / National Dex #0965',
          'Revavroom: Steel/Poison / National Dex #0966',
          'Cyclizar: Dragon/Normal / National Dex #0967',
          'Orthworm: Steel / National Dex #0968',
          'Glimmet: Rock/Poison / National Dex #0969',
          'Glimmora: Rock/Poison / National Dex #0970',
          'Greavard: Ghost / National Dex #0971',
          'Houndstone: Ghost / National Dex #0972',
          'Flamigo: Flying/Fighting / National Dex #0973',
          'Cetoddle: Ice / National Dex #0974',
          'Cetitan: Ice / National Dex #0975',
          'Veluza: Water/Psychic / National Dex #0976',
          'Dondozo: Water / National Dex #0977',
          'Tatsugiri: Dragon/Water / National Dex #0978',
          'Annihilape: Fighting/Ghost / National Dex #0979',
          'Clodsire: Poison/Ground / National Dex #0980',
          'Farigiraf: Normal/Psychic / National Dex #0981',
          'Dudunsparce: Normal / National Dex #0982',
          'Kingambit: Dark/Steel / National Dex #0983',
          'Great Tusk: Ground/Fighting / National Dex #0984',
          'Scream Tail: Fairy/Psychic / National Dex #0985',
          'Brute Bonnet: Grass/Dark / National Dex #0986',
          'Flutter Mane: Ghost/Fairy / National Dex #0987',
          'Slither Wing: Bug/Fighting / National Dex #0988',
          'Sandy Shocks: Electric/Ground / National Dex #0989',
          'Iron Treads: Ground/Steel / National Dex #0990',
          'Iron Bundle: Ice/Water / National Dex #0991',
          'Iron Hands: Fighting/Electric / National Dex #0992',
          'Iron Jugulis: Dark/Flying / National Dex #0993',
          'Iron Moth: Fire/Poison / National Dex #0994',
          'Iron Thorns: Rock/Electric / National Dex #0995',
          'Frigibax: Dragon/Ice / National Dex #0996',
          'Arctibax: Dragon/Ice / National Dex #0997',
          'Baxcalibur: Dragon/Ice / National Dex #0998',
          'Gimmighoul: Ghost / National Dex #0999',
          'Gholdengo: Steel/Ghost / National Dex #1000',
          'Wo-Chien: Dark/Grass / National Dex #1001',
          'Chien-Pao: Dark/Ice / National Dex #1002',
          'Ting-Lu: Dark/Ground / National Dex #1003',
          'Chi-Yu: Dark/Fire / National Dex #1004',
          'Roaring Moon: Dragon/Dark / National Dex #1005',
          'Iron Valiant: Fairy/Fighting / National Dex #1006',
          'Koraidon: Fighting/Dragon / National Dex #1007',
          'Miraidon: Electric/Dragon / National Dex #1008',
          'Walking Wake: Water/Dragon / National Dex #1009',
          'Iron Leaves: Grass/Psychic / National Dex #1010',
          'Dipplin: Grass/Dragon / National Dex #1011',
          'Poltchageist: Grass/Ghost / National Dex #1012',
          'Sinistcha: Grass/Ghost / National Dex #1013',
          'Okidogi: Poison/Fighting / National Dex #1014',
          'Munkidori: Poison/Psychic / National Dex #1015',
          'Fezandipiti: Poison/Fairy / National Dex #1016',
          'Ogerpon: Grass / National Dex #1017',
          'Archaludon: Steel/Dragon / National Dex #1018',
          'Hydrapple: Grass/Dragon / National Dex #1019',
          'Gouging Fire: Fire/Dragon / National Dex #1020',
          'Raging Bolt: Electric/Dragon / National Dex #1021',
          'Iron Boulder: Rock/Psychic / National Dex #1022',
          'Iron Crown: Steel/Psychic / National Dex #1023',
          'Terapagos: Normal / National Dex #1024',
          'Pecharunt: Poison/Ghost / National Dex #1025',
          "Ash Ketchum: Pikachu's trainer / World Champion",
          'Misty: Cerulean Gym Leader / Water specialist',
          'Brock: Pewter Gym Leader / Pokemon doctor',
          'Professor Oak: Kanto Pokemon researcher',
          "Gary Oak: Ash's rival / Pokemon researcher",
          "Jessie: Team Rocket / Wobbuffet's trainer",
          'James: Team Rocket / Pokemon collector',
          'Giovanni: Team Rocket boss / Ground specialist',
          "Delia Ketchum: Ash's mother",
          "Tracey Sketchit: Pokemon watcher / Oak's assistant",
          'May: Hoenn coordinator / contest performer',
          "Max: May's younger brother / knowledgeable companion",
          "Dawn: Sinnoh coordinator / Piplup's trainer",
          'Iris: Dragon specialist / Unova Champion',
          'Cilan: Pokemon Connoisseur / Gym Leader',
          "Serena: Kalos performer / Ash's companion",
          'Clemont: Lumiose Gym Leader / inventor',
          "Bonnie: Clemont's sister / Zygarde's friend",
          "Lillie: Alolan student / Snowy's trainer",
          'Kiawe: Alolan Fire specialist',
          'Mallow: Alolan cook / Grass specialist',
          'Lana: Alolan student / Water specialist',
          'Sophocles: Alolan inventor / Electric specialist',
          'Professor Kukui: Alola researcher / Masked Royal',
          "Gladion: Silvally's trainer / Lillie's brother",
          'Goh: Pokemon catcher / Project Mew',
          "Chloe: Eevee's trainer / Goh's friend",
          "Leon: Galar Champion / Charizard's trainer",
          "Cynthia: Sinnoh Champion / Garchomp's trainer",
          'Steven Stone: Hoenn Champion / Steel specialist',
          'Lance: Dragon master / Indigo Champion',
          'Diantha: Kalos Champion / actress',
          'Alain: Mega Charizard X trainer',
          'Paul: Sinnoh rival / rigorous trainer',
          'N: Pokemon communicator / Team Plasma',
          "Liko: Pokemon Horizons protagonist / Sprigatito's trainer",
          "Roy: Pokemon Horizons protagonist / Fuecoco's trainer",
          "Dot: Nidothing / Quaxly's trainer",
          'Friede: Rising Volt Tacklers captain / Pokemon professor',
          "Amethio: Explorers member / Ceruledge's trainer"]})

NOVEL_LISTS = {'ORV': ['Kim Dokja: Sole reader / Fourth Wall / strategic knowledge',
         'Yoo Joonghyuk: Regressor / Ways of Survival protagonist',
         'Han Sooyoung: Author / Avatar skill',
         'Yoo Sangah: Polyglot office worker / agile fighter',
         'Jung Heewon: Judge of Destruction / swordswoman',
         'Lee Hyunsung: Steel Sword / military veteran',
         'Lee Jihye: Naval Warfare specialist / swordswoman',
         'Lee Gilyoung: Insect control / young companion',
         'Shin Yoosung: Beast tamer / young companion',
         'Lee Seolhwa: Poison doctor / healer',
         'Gong Pildu: Armed Fortress / defence specialist',
         'Han Myungoh: Former department head / demon connection',
         "Lee Sookyung: Kim Dokja's mother / Wanderers leader",
         "Yoo Mia: Yoo Joonghyuk's younger sister",
         'Kim Namwoon: Delusional demon / violent incarnation',
         'Anna Croft: Prophet / Zarathustra leader',
         "Selena Kim: Anna Croft's ally / fighter",
         'Iris Vladimir: Zarathustra incarnation',
         'Jang Hayoung: Transcendent / unidentified wall',
         'Jang Sungchul: Revolutionary / Demon Realm',
         'Mark Javier: Gourmet Association incarnation',
         'Asuka Ren: Manga artist / Peace Land connection',
         'Yamamoto Hajime: Japanese incarnation / Peace Land',
         'Kyrgios Rodgraim: Electrification master / small person',
         'Breaking the Sky Sword Saint: Transcendent swordswoman',
         'Breaking the Sky Master: Martial arts master / canine form',
         'Nirvana Moebius: Reincarnator / Salvation Church leader',
         'Reinheit: Dark Castle ruler / Paradise master',
         'Eileen: Demon Realm doctor',
         'Syswitz: Demon duke / industrial complex ruler',
         'Asmodeus: Demon King of Lust',
         'Agares: Demon King / eastern hell ruler',
         'Uriel: Demon-like Judge of Fire / archangel',
         'Sun Wukong: Great Sage Equal of Heaven / constellation',
         'Abyssal Black Flame Dragon: Dragon constellation / dark flames',
         'Secretive Plotter: Mysterious outer-god constellation',
         'Mass Production Maker: Industrial constellation / item maker',
         'Oldest Dream: Dreaming entity / world-line observer',
         'Hades: Underworld king / constellation',
         'Persephone: Underworld queen / constellation',
         'Zeus: Olympus leader / lightning',
         'Poseidon: Olympus sea god',
         'Athena: Olympus goddess / strategy',
         'Dionysus: Olympus god / wine',
         'Hephaestus: Olympus god / smithing',
         'Hermes: Olympus messenger god',
         'Surya: Vedic sun constellation',
         'Indra: Vedic thunder constellation',
         'Michael: Archangel / Eden',
         "Metatron: Eden's scribe / constellation",
         'Gabriel: Archangel / Eden',
         "Cheok Jungyeong: Goryeo's First Sword",
         'Yi Sunsin: Maritime War God / naval constellation',
         "Bihyung: Dokkaebi / Kim Dokja's channel host",
         "Biyoo: Young dokkaebi / Kim Dokja's companion",
         'Dokgak: Dokkaebi / scenario administrator',
         'Paul: Dokkaebi / hostile scenario administrator',
         'Baram: Bureau dokkaebi',
         'Fourth Wall: Sentient wall / mental protection'],
 'TBATE': ['Arthur Leywin: Reincarnated King Grey / aether swordsman',
           'Tessia Eralith: Elven princess / plant mage',
           "Sylvie: Dragon companion / Sylvia's daughter",
           'Regis: Aetheric companion / destruction',
           "Sylvia: Dragon / Arthur's early protector",
           "Reynolds Leywin: Arthur's father / augmenter",
           "Alice Leywin: Arthur's mother / healer",
           'Eleanor Leywin: Ellie / mana archer',
           "Boo: Guardian bear / Ellie's bond",
           "Virion Eralith: Elven elder / Arthur's mentor",
           "Alduin Eralith: Elven king / Tessia's father",
           "Merial Eralith: Elven queen / Tessia's mother",
           'Rinia Darcassan: Diviner / elven elder',
           "Lania Darcassan: Diviner / Rinia's sister",
           'Vincent Helstea: Merchant / Leywin family friend',
           "Tabitha Helstea: Lilia's mother",
           "Lilia Helstea: Mage / Arthur's childhood friend",
           'Jasmine Flamesworth: Twin Horns adventurer / wind fighter',
           'Helen Shard: Twin Horns leader / archer',
           'Durden Walker: Twin Horns earth mage',
           'Adam Krensh: Twin Horns spear fighter',
           'Angela Rose: Twin Horns wind mage',
           "Elijah Knight: Xyrus student / Arthur's friend",
           "Nico Sever: Grey's former friend / Scythe",
           "Cecilia: Legacy / Grey and Nico's former friend",
           'Lucas Wykes: Xyrus mage / noble antagonist',
           'Bairon Wykes: Thunderlord / lightning Lance',
           'Varay Aurae: Zero / ice Lance',
           'Aya Grephin: Phantasm / illusion Lance',
           'Mica Earthborn: Ohmwrecker / gravity Lance',
           'Olfred Warend: Balrog / magma Lance',
           'Alea Triscan: Aureate / elven Lance',
           'Cynthia Goodsky: Xyrus director / wind mage',
           'Gideon: Dicathen inventor / engineer',
           "Emily Watsken: Gideon's apprentice / inventor",
           'Kathyln Glayder: Human princess / ice mage',
           'Curtis Glayder: Human prince / fire mage',
           "Grawder: Curtis's lion bond",
           'Doradrea Oreguard: Dwarven Xyrus student',
           'Theodore Maxwell: Xyrus student / wind mage',
           'Feyrith Ivsaar III: Elven Xyrus student / water mage',
           'Claire Bladeheart: Disciplinary Committee leader',
           'Professor Glory: Xyrus combat instructor',
           'Kordri: Asuran martial arts instructor / Thyestes',
           'Windsom: Indrath dragon / asuran envoy',
           "Myre: Asuran healer / Kezess's wife",
           'Kezess Indrath: Dragon lord / Epheotus ruler',
           'Wren Kain IV: Asuran artificer / titan',
           'Aldir: Asuran general / World Eater',
           'Taci: Young Thyestes asura',
           "Agrona Vritra: Vritra ruler / Alacrya's high sovereign",
           'Seris Vritra: Scythe / independent strategist',
           'Caera Denoir: Vritra-blooded swordswoman',
           "Alaric: Arthur's Alacryan mentor",
           'Lyra Dreide: Retainer / Alacryan administrator',
           "Cylrit: Seris's retainer / swordsman",
           'Uto: Retainer / black spike magic',
           'Jagrette: Retainer / poison mage',
           'Bilal: Retainer / Alacryan fighter',
           'Cadell: Scythe / soulfire',
           'Dragoth Vritra: Scythe / brute strength',
           'Melzri Vritra: Scythe / combat specialist',
           'Viessa Vritra: Scythe / illusion magic',
           'Mawar: Retainer / Alacryan fighter',
           'Seth Milview: Central Academy student',
           'Mayla: Central Academy student',
           'Enola: Central Academy student',
           'Wade: Central Academy student',
           'Taegen: Denoir guard / swordsman',
           'Arian: Denoir guard / mage',
           "Corbett Denoir: Caera's adoptive father",
           "Lenora Denoir: Caera's adoptive mother",
           "Sevren Denoir: Caera's adoptive brother",
           'Darrin Ordin: Dicathen veteran / adventurer',
           'Albold: Elven warrior / Dicathen',
           "Trodius Flamesworth: Noble commander / Jasmine's father",
           'Sebastian: Royal court mage / antagonist',
           'Rahdeas: Dwarven council member',
           'Dawsid Greysunders: Dwarven king',
           'Glaudera Greysunders: Dwarven queen',
           'Blaine Glayder: Human king / Sapin',
           'Priscilla Glayder: Human queen / Sapin',
           'Mordain Asclepius: Phoenix lord / Hearth leader',
           "Chul: Half-phoenix warrior / Arthur's ally",
           "Dawn: Phoenix / Chul's mother"],
 'SS': ['Sunny: Sunless / Lost from Light / shadow powers',
        'Nephis: Changing Star / soul flames and healing',
        'Cassie: Cassia / Song of the Fallen / oracle',
        'Effie: Athena / Raised by Wolves / superhuman physique',
        'Kai: Nightingale / flight and perception',
        'Jet: Soul Reaper / soul-damaging combat',
        'Mordret: Prince of Nothing / reflection powers',
        "Rain: Sunny's younger sister / hunter",
        "Saint: Sunny's stone knight shadow",
        "Nightmare: Sunny's shadow steed / dream powers",
        "Fiend: Sunny's metal-eating shadow",
        "Serpent: Sunny's Soul Serpent / weapon forms",
        'Mimic: Marvelous Mimic / living chest',
        "Aiko: Sunny's assistant / business manager",
        'Master Naeve: House of Night / aquatic fighter',
        'Bloodwave: House of Night Saint / sea transformation',
        'Teacher Julius: Academy historian / wilderness knowledge',
        'Professor Obel: Scientist / Nightmare research',
        'Morgan: Princess of War / Valor swordswoman',
        'Anvil of Valor: Sovereign / sword domain',
        'Ki Song: Sovereign / Queen of Worms',
        'Asterion: Dreamspawn / mysterious Sovereign',
        "Broken Sword: Nephis's father / Immortal Flame hero",
        "Smile of Heaven: Nephis's mother / Dreamspawn",
        "Immortal Flame: Nephis's grandfather / clan founder",
        'Seishan: Song daughter / Forgotten Shore leader',
        'Beastmaster: Song Saint / mental influence',
        'Revel: Lightslayer / Song Saint',
        'Moonveil: Song Saint / ability suppression',
        'Silent Stalker: Song Saint / hunter',
        'Dire Fang: Song Saint / beast transformation',
        'Summer Knight: Valor Saint / radiant warrior',
        'Whispering Blade: Madoc / Valor swordsman',
        'Sky Tide: Tyris / storm bird transformation',
        "Roan: Saint / Tyris's husband",
        'Luster: Antarctica irregular / essence support',
        'Belle: Antarctica irregular / swordsman',
        'Dorn: Antarctica irregular / heavy fighter',
        'Kim: Antarctica irregular / perception',
        'Samara: Antarctica irregular / marksman',
        'Quentin: Antarctica irregular / healer',
        'Winter: Antarctica Master / archer',
        'Dale: Antarctica Master / combatant',
        'Verne: Antarctica Master / officer',
        'Wake of Ruin: Saint / swarm transformation',
        'Jest: Valor Saint / veteran',
        'Gunlaug: Bright Lord / Forgotten Shore ruler',
        "Harus: Gunlaug's executioner / blind fighter",
        "Gemma: Gunlaug's lieutenant / armour user",
        'Caster: Legacy swordsman / acceleration',
        'Shakti: Fire Keeper / plant-growing artisan',
        'Eurys of the Nine: God-slaying warrior / chained skeleton',
        'Noctis: Chain Lord / sorcerer',
        'Solvane: Chain Lord / immortal warrior',
        'Hope: Demon of Desire / daemon',
        'Weaver: Demon of Fate / daemon',
        'Ariel: Demon of Dread / Tomb creator',
        'Nether: Demon of Destiny / Underworld',
        'Oblivion: Forgotten daemon',
        'Imagination: Daemon / Demon of Imagination',
        'War God: Deity / warfare',
        'Storm God: Deity / storms and darkness',
        'Sun God: Deity / light and fire',
        'Beast God: Deity / beasts and life',
        'Heart God: Deity / souls and emotions',
        'Shadow God: Deity / shadows and death',
        'Dream God: Forgotten God / dreams and the Void',
        'Vile Thieving Bird: Nightmare creature / fate thief',
        'Soul Devouring Tree: Forgotten Shore horror / mind influence',
        'Crimson Terror: Crimson Spire guardian',
        'Goliath: Antarctica titan / colossal creature',
        'Winter Beast: Antarctica titan / freezing storm',
        'Daeron: Serpent King / Great River sovereign',
        'Wind Flower: Twilight princess / time-loop guide',
        'Ananke: Great River priestess / Weaver devotee',
        'Undying Slaughter: Defiled Effie / Six Plagues',
        'Devouring Beast: Defiled Jet / Six Plagues',
        'Dread Lord: Defiled Kai / Six Plagues',
        'Soul Stealer: Defiled Mordret / Six Plagues',
        'Torment: Defiled Cassie / Six Plagues',
        'Mad Prince: Defiled Sunny / Six Plagues',
        'Stev: Bright Castle Memory Market keeper',
        "Beth: Professor Obel's assistant / Antarctica researcher",
        'Harper: Bright Castle informant',
        "Tessai: Gunlaug's Castle Guard leader",
        'Kido: Forgotten Shore artisan / plant cultivation',
        "Saint of Sorrow: Legacy Saint / Tamar's parent",
        "Tamar: Legacy student / Rain's ally"],
 'RI': ['Fang Yuan: Gu Yue Fang Yuan / Spring Autumn Cicada',
        "Fang Zheng: Fang Yuan's twin / righteous-path Gu Master",
        'Bai Ning Bing: Northern Dark Ice Soul physique / ice path',
        'Hei Lou Lan: Great Strength True Martial physique',
        'Tai Bai Yun Sheng: Time-path healer / landscape restoration',
        'Shang Xin Ci: Shang clan leader / merchant',
        'Shang Yan Fei: Shang clan patriarch / blood path',
        'Wei De Xin: Shang clan manager',
        'Shang Pu Lao: Shang clan young master',
        'Shang Chi Wen: Shang clan young master',
        'Shang Qiu Niu: Shang clan young master',
        'Shang Bi Xi: Shang clan young master',
        'Shang Ya Zi: Shang clan young master',
        'Shang Yi Fan: Shang clan young master',
        'Gu Yue Bo: Gu Yue clan leader',
        'Gu Yue Qing Shu: Gu Yue clan elite / wood charm',
        'Gu Yue Chi Lian: Gu Yue elder / Chi faction',
        'Gu Yue Mo Chen: Gu Yue elder / Mo faction',
        'Gu Yue Chi Cheng: Chi faction young Gu Master',
        'Gu Yue Mo Bei: Mo faction young Gu Master',
        'Gu Yue Yao Ji: Medicine hall elder',
        "Gu Yue Yao Le: Yao Ji's granddaughter",
        'Gu Yue Jiang Ya: Gu Master / merchant',
        "Gu Yue Jiang He: Gu Master / Jiang Ya's brother",
        "Gu Yue Dong Tu: Fang Yuan's uncle",
        "Shen Cui: Fang Yuan's household servant",
        'Jia Fu: Merchant caravan leader',
        "Jia Jin Sheng: Jia clan merchant / Jia Fu's brother",
        'Jia Gui: Jia clan merchant rival',
        'Tie Xue Leng: Divine Investigator',
        'Tie Ruo Nan: Investigator / Tie clan genius',
        'Tie Mu Bai: Tie clan expert / metal path',
        'Tie Bai Qi: Tie clan expert',
        'Tie Mian Shen: Tie clan Gu Immortal',
        'Tie Qu Zhong: Tie clan Gu Immortal',
        'Xiong Li: Xiong clan strength expert',
        'Xiong Jiang: Xiong clan fighter / zombie transformation',
        'Xiong Jiao Man: Xiong clan Gu Master / bear control',
        'Bai Hua: Bai clan young master',
        'Bai Sheng: Bai clan young master',
        'Bai clan leader: Bai clan matriarch',
        'Gu Yue First Generation: Blood ancestor / clan founder',
        "Lord Sky Crane: Immortal Crane Sect / Fang Zheng's mentor",
        'He Feng Yang: Immortal Crane Sect elder',
        'Feng Jiu Ge: Sound-path genius / nine songs',
        "Feng Jin Huang: Dream-path prodigy / Feng Jiu Ge's daughter",
        "Fairy Bai Qing: Feng Jin Huang's mother / Spirit Affinity House",
        "Fairy Li Shan: Hei Lou Lan's aunt / information-path oath",
        'Hei Cheng: Hei tribe immortal / dark path',
        'Hei Bao: Hei tribe immortal / wood path',
        'Hei Fan: Hei tribe time-path ancestor',
        "Su Xian Er: Hei Cheng's wife",
        'Dong Fang Chang Fan: Wisdom-path schemer / possession',
        'Dong Fang Yu Liang: Dong Fang tribe leader / wisdom path',
        "Dong Fang Qing Yu: Dong Fang Yu Liang's sister",
        'Ma Hong Yun: Luck-favoured Northern Plains youth',
        'Zhao Lian Yun: Otherworldly demon / love Gu',
        'Ma Ying Jie: Ma tribe leader / enslavement path',
        'Ma Zun: Horse King / enslavement path',
        'Chang Shan Yin: Wolf King / enslavement path',
        "Chang Ji You: Chang Shan Yin's son",
        'Pan Ping: Single Blade General',
        'Liu Wen Wu: Liu tribe leader / light path',
        'Mo Shi Kuang: Inkman / qi path',
        'Ouyang Bi Sang: Transformation-path fighter',
        'Nu Er Tu: Leopard King / enslavement path',
        'Wu Yong: Wu clan leader / wind path',
        'Wu Du Xiu: Wu clan matriarch / wind path',
        "Wu Yi Hai: Wu Yong's half-brother / transformation path",
        'Wu Shuai: Dragonman leader / enslavement path',
        "Wu Shuai Clone: Fang Yuan's dragonman clone",
        "Qi Sea Ancestor: Fang Yuan's qi-path clone",
        "Zhan Bu Du: Fang Yuan's transformation-path clone",
        "Meng Qiu Zhen: Fang Yuan's dream-path clone",
        "Li Xiao Bai: Fang Yuan's literature-path clone",
        'Fang Di Chang: Fang clan wisdom-path strategist',
        'Fang Gong: Fang clan strength-path leader',
        'Fang An Lei: Fang clan immortal / wood path',
        'Fang Leng: Fang clan Gu Immortal',
        'Fang Yun: Fang clan Gu Immortal',
        'Chu Du: Domination Immortal / strength path',
        "Lang Ya Land Spirit: Long Hair Ancestor's blessed-land spirit",
        'Long Hair Ancestor: Refinement-path supreme grandmaster',
        'Mo Tan Sang: Inkman City leader',
        'Shi Nu: Rockman Gu Immortal / Shadow Sect',
        'Ying Wu Xie: Pure Dream Reality Seeker / Shadow Sect',
        'Old Man Yan Shi: Shadow Sect wisdom-path planner',
        'Purple Mountain True Monarch: Wisdom-path expert / Shadow Sect',
        'Bo Qing: Pseudo-Immortal Venerable / sword path',
        "Mo Yao: Inkman refinement expert / Bo Qing's wife",
        'Xue Hu: Snowy Mountain leader / snow path',
        "Lady Wan Shou: Refinement expert / Xue Hu's wife",
        "Blazing Heaven Demoness: Hei Lou Lan's aunt / fire path",
        'Yin Liu Gong: Northern Plains zombie leader',
        'Fairy Zi Wei: Heavenly Court wisdom-path expert',
        'Duke Long: Heavenly Court / qi and transformation paths',
        'Qin Ding Ling: Heavenly Court leader / luck path',
        'Fan Xi Liu: Immortal Crane Sect elder',
        'Chen Yi: Heavenly Lotus Sect elder / wood path',
        'Li Huang: Heavenly Court fire-path expert',
        'Gu Liu Ru: Heavenly Court time-path expert',
        "Xing Ye Wang: Star Lord Wan Xiang's identity / star path",
        'Zhou Xiong Xin: Heavenly Court information-path expert',
        'Che Wei: Heavenly Court formation expert',
        'Cong Yan: Heavenly Court immortal',
        'Wan Zi Hong: Heavenly Court wood-path expert',
        "Fang Di Chang Clone: Fang Yuan's wisdom-path clone",
        'Shen Shang: Eastern Sea human-path expert',
        'Shen Cong Sheng: Shen clan leader / sound path',
        'Song Qi Yuan: Song clan leader / light path',
        'Song Yi Shi: Song clan water-path immortal',
        'Qing Yue An: Eastern Sea immortal / wood path',
        'Hua Cai Yun: Hua clan immortal / cloud path',
        'Hua Die: Eastern Sea Gu Immortal',
        'Miao Ming Shen: Eastern Sea space-path expert',
        "Gui Qi Ye: Miao Ming Shen's ally",
        "Feng Jiang: Miao Ming Shen's ally",
        'Tu Tou Tuo: Earth-path Gu Immortal',
        'Zeng Luo Zi: Information-path Gu Immortal',
        'Ren Xiu Ping: Enslavement-path Gu Immortal',
        "Ren Zu: Humanity's ancestor / legendary Gu user",
        "Verdant Great Sun: Ren Zu's first son",
        "Desolate Ancient Moon: Ren Zu's daughter",
        "Northern Dark Ice Soul: Ren Zu's child / physique namesake",
        "Great Strength True Martial: Ren Zu's child / physique namesake",
        "Carefree Wisdom Heart: Ren Zu's child / wisdom",
        "Boundless Forest Samsara: Ren Zu's child",
        "Blazing Glory Lightning Brilliance: Ren Zu's child",
        "Myriad Gold Wondrous Essence: Ren Zu's child",
        "Thick Earth Central Origin: Ren Zu's child",
        'Great Dream Immortal Venerable: Prophesied future venerable',
        'Primordial Origin Immortal Venerable: Qi-path founder / first venerable',
        'Star Constellation Immortal Venerable: Wisdom and star paths',
        'Limitless Demon Venerable: Rule-path founder',
        'Reckless Savage Demon Venerable: Strength and transformation paths',
        'Red Lotus Demon Venerable: Time path / damaged fate Gu',
        'Genesis Lotus Immortal Venerable: Wood and painting paths',
        'Thieving Heaven Demon Venerable: Theft and space paths',
        'Giant Sun Immortal Venerable: Luck-path founder',
        'Spectral Soul Demon Venerable: Soul-path founder / Shadow Sect',
        'Paradise Earth Immortal Venerable: Earth path / peaceful venerable']}

SERIES_TITLES = {'AOT': 'Attack on Titan', 'JJK': 'Jujutsu Kaisen', 'MHA': 'My Hero Academia', 'OPM': 'One Punch Man', 'SL': 'Solo Leveling', 'DL': 'Demon Slayer', 'BL': 'Blue Lock', 'DN': 'Death Note', 'SG': 'Steins;Gate', 'NAR': 'Naruto', 'TG': 'Tokyo Ghoul', 'HXH': 'Hunter x Hunter', 'SAO': 'Sword Art Online', 'NGNL': 'No Game No Life', 'CG': 'Code Geass', 'TEN': 'That Time I Got Reincarnated as a Slime', 'BC': 'Black Clover', 'BLE': 'Bleach', 'SDS': 'The Seven Deadly Sins', 'DBZ': 'Dragon Ball Z', 'VS': 'Vinland Saga', 'FF': 'Fire Force', 'COTE': 'Classroom of the Elite', 'HQ': 'Haikyuu!!', 'KNB': "Kuroko's Basketball", 'EIS': 'The Eminence in Shadow', 'JOJO': "JoJo's Bizarre Adventure", 'ORV': "Omniscient Reader's Viewpoint", 'TBATE': 'The Beginning After the End', 'SS': 'Shadow Slave', 'RI': 'Reverend Insanity', 'PKMN': 'Pokemon'}

GAME_MODES = {
    "anime": "Anime Only",
    "novel": "Light / Web Novels Only",
    "everything": "Everything",
}
POKEMON_DRAW_CHANCE = 0.01

def selected_rosters(mode="everything"):
    """Group adaptations by requested roster: the four web novels stay in Novel Only."""
    if mode not in GAME_MODES:
        raise ValueError(f"Unknown draft mode: {mode}")
    result = {}
    if mode in ("anime", "everything"):
        result.update(ANIME_LISTS)
    if mode in ("novel", "everything"):
        result.update(NOVEL_LISTS)
    return result

class CharacterPool(list):
    """A draw-without-replacement pool with a 1% Pokemon branch.

    The 1% chance applies while both Pokemon and other characters remain.
    Once either category runs out, draws use the remaining category.
    All species remain eligible; no Pokemon are discarded to achieve rarity.
    """
    def pop(self, index=None):
        if index is not None:
            return super().pop(index)
        rare = [i for i, item in enumerate(self) if item["anime"] == "PKMN"]
        common = [i for i, item in enumerate(self) if item["anime"] != "PKMN"]
        if not rare and not common:
            raise IndexError("pop from empty character pool")
        if rare and common:
            candidates = rare if random.random() < POKEMON_DRAW_CHANCE else common
        else:
            candidates = rare or common
        return super().pop(random.choice(candidates))

def make_character_pool(mode="everything"):
    """Build the selected pool, deduplicating exact identities within each series."""
    pool = CharacterPool()
    for series, characters in selected_rosters(mode).items():
        seen = set()
        for character_name in characters:
            identity = re.split(r"[:(]", character_name, maxsplit=1)[0].strip().casefold()
            if identity in seen:
                continue
            seen.add(identity)
            pool.append({"name": character_name, "anime": series,
                         "display": f"{character_name} [{series}]"})
    return pool

STAT_SLOTS = [

    "Speed",

    "Intelligence",

    "Strength",

    "Defence",

    "Endurance",

    "Ability",

    "Willpower",

]

#

STARTING_BALANCE = 20

#


import tkinter as tk



#

#**GUI THEME**

BG = "#0b1020"

PANEL = "#141c31"

PANEL_ALT = "#1a2540"

ACCENT = "#7c9cff"

ACCENT_HOVER = "#9db4ff"

TEXT = "#edf2ff"

MUTED = "#a4b0cc"

GREEN = "#75e0b2"

RED = "#ff8795"

GOLD = "#ffd479"

PLAYER_COLORS = ("#ff5c6c", "#5ca8ff")

#

class Player:

    def __init__(self, name, balance=STARTING_BALANCE):

        self.name = name

        self.balance = balance

        self.build = {}

        self.consecutive_passes = 0

        self.force_next_pick = False

    #

    def has_empty_slots(self):

        return len(self.build) < len(STAT_SLOTS)

    #

    def next_slot(self):

        for slot in STAT_SLOTS:

            if slot not in self.build:

                return slot

        return None

    #

    def add_character(self, slot, character, cost=0):

        if slot in self.build:

            raise ValueError(f"{self.name} already has a character for {slot}.")

        if cost > self.balance:

            raise ValueError("The player cannot afford that amount.")

        self.balance -= cost

        self.build[slot] = {"character": character, "cost": cost}

        self.consecutive_passes = 0

        self.force_next_pick = False

#


#

class AnimeDraftGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("Anime & Novel Draft")

        self.root.geometry("1180x790")

        self.root.minsize(980, 680)

        self.root.configure(bg=BG)

        self.players = []

        self.game_mode = "everything"

        self.character_pool = CharacterPool()

        self.current_player_index = 0

        self.current_character = None

        self.current_slot = None

        self.high_bid = 0

        self.high_bidder_index = None

        self.free_offer_passer = None

        self.game_finished = False

        self.show_setup()

    #

    def clear_window(self):

        for widget in self.root.winfo_children():

            widget.destroy()

    #

    def make_label(self, parent, text, size=11, color=TEXT, bold=False, **kwargs):

        return tk.Label(

            parent, text=text, bg=kwargs.pop("bg", parent.cget("bg")),

            fg=color, font=("Segoe UI", size, "bold" if bold else "normal"),

            **kwargs

        )

    #

    def make_button(self, parent, text, command, bg=ACCENT, fg="#081020", **kwargs):

        return tk.Button(

            parent, text=text, command=command, bg=bg, fg=fg,

            activebackground=ACCENT_HOVER, activeforeground="#081020",

            relief="flat", bd=0, cursor="hand2", padx=16, pady=10,

            font=("Segoe UI", 10, "bold"), **kwargs

        )

    #

    def show_setup(self):

        self.clear_window()

        outer = tk.Frame(self.root, bg=BG)

        outer.pack(fill="both", expand=True, padx=30, pady=25)

        self.make_label(outer, "ANIME & NOVEL DRAFT", 25, TEXT, True).pack(pady=(12, 8))

        self.make_label(

            outer, "Build your team. Manage your money. Decide who deserves each stat.",

            11, MUTED

        ).pack(pady=(0, 16))

        card = tk.Frame(outer, bg=PANEL, padx=26, pady=18)

        card.pack()

        self.make_label(card, "PLAYER NAMES", 12, ACCENT, True, bg=PANEL).pack(anchor="w", pady=(0, 18))

        self.make_label(card, "Player 1", 10, MUTED, True, bg=PANEL).pack(anchor="w")

        self.name1 = tk.Entry(card, width=34, font=("Segoe UI", 12), bg=PANEL_ALT, fg=TEXT,

                              insertbackground=TEXT, relief="flat", bd=0)

        self.name1.pack(ipady=7, pady=(4, 10))

        self.name1.insert(0, "Player 1")

        self.make_label(card, "Player 2", 10, MUTED, True, bg=PANEL).pack(anchor="w")

        self.name2 = tk.Entry(card, width=34, font=("Segoe UI", 12), bg=PANEL_ALT, fg=TEXT,

                              insertbackground=TEXT, relief="flat", bd=0)

        self.name2.pack(ipady=7, pady=(4, 14))

        self.name2.insert(0, "Player 2")

        self.make_label(card, "CHOOSE YOUR POOL", 10, ACCENT, True).pack(anchor="w", pady=(0, 5))
        self.mode_var = tk.StringVar(value=getattr(self, "game_mode", "everything"))
        mode_row = tk.Frame(card, bg=PANEL)
        mode_row.pack(fill="x")
        for mode, label in GAME_MODES.items():
            tk.Radiobutton(
                mode_row, text=label, variable=self.mode_var, value=mode,
                command=self.update_mode_preview, bg=PANEL, fg=TEXT,
                selectcolor=PANEL_ALT, activebackground=PANEL, activeforeground=TEXT,
                font=("Segoe UI", 10), cursor="hand2",
            ).pack(anchor="w")
        self.mode_preview = self.make_label(card, "", 9, MUTED, wraplength=410, justify="left")
        self.mode_preview.pack(fill="x", pady=(5, 12))
        self.update_mode_preview()

        self.make_button(card, "START DRAFT  →", self.start_game).pack(fill="x")

        self.make_label(

            outer,

            "Each player starts with £20 and fills Speed, Intelligence, Strength, Defence,\n"

            "Endurance, Ability and Willpower. Players alternate bids. Passing after a bid awards the character to the highest bidder at their bid price. With no bids, passing offers the other player the character for free.",

            10, MUTED, justify="center", wraplength=700

        ).pack(pady=12)

        self.name1.focus_set()

    def update_mode_preview(self):
        mode = self.mode_var.get()
        pool = make_character_pool(mode)
        count = len(selected_rosters(mode))
        note = " Pokemon: 1% of draws while both pools remain." if mode != "novel" else " Includes ORV, TBATE, Shadow Slave and Reverend Insanity."
        self.mode_preview.config(text=f"{count} series / {len(pool):,} entries.{note}\nDescriptions include source-material spoilers.")

    #

    def start_game(self):

        name1 = self.name1.get().strip() or "Player 1"

        name2 = self.name2.get().strip() or "Player 2"

        if name1.casefold() == name2.casefold():
            name2 += " (Player 2)"

        self.game_mode = self.mode_var.get()

        self.character_pool = make_character_pool(self.game_mode)

        self.players = [Player(name1), Player(name2)]

        self.current_player_index = 0

        self.current_character = None

        self.free_offer_passer = None

        self.game_finished = False

        self.show_game()

        self.prepare_turn()

    #

    def show_game(self):

        self.clear_window()

        header = tk.Frame(self.root, bg=BG)

        header.pack(fill="x", padx=22, pady=(18, 10))

        self.make_label(header, "ANIME & NOVEL DRAFT", 18, TEXT, True, bg=BG).pack(side="left")

        self.pool_label = self.make_label(header, "", 10, MUTED, True, bg=BG)

        self.pool_label.pack(side="right", pady=6)

        body = tk.Frame(self.root, bg=BG)

        body.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        body.grid_columnconfigure(0, weight=2, uniform="auction_columns")

        body.grid_columnconfigure(1, weight=5, uniform="auction_columns")

        body.grid_columnconfigure(2, weight=2, uniform="auction_columns")

        body.grid_rowconfigure(0, weight=1)

        self.player_panels = []

        for index, column in enumerate((0, 2)):

            player_panel = tk.Frame(body, bg=PANEL, padx=12, pady=14)

            player_panel.grid(row=0, column=column, sticky="nsew",

                              padx=(0, 8) if column == 0 else (8, 0))

            top = tk.Frame(player_panel, bg=PANEL)

            top.pack(fill="x")

            player_color = PLAYER_COLORS[index]

            name_label = self.make_label(top, "", 12, player_color, True, bg=PANEL)

            name_label.pack(anchor="w")

            money_label = self.make_label(player_panel, "", 11, player_color, True, bg=PANEL)

            money_label.pack(anchor="w", pady=(5, 0))

            progress_label = self.make_label(player_panel, "", 9, MUTED, bg=PANEL)

            progress_label.pack(anchor="w", pady=(3, 8))

            slot_labels = {}

            for slot in STAT_SLOTS:

                row = tk.Frame(player_panel, bg=PANEL_ALT, padx=7, pady=8)

                row.pack(fill="x", pady=3)

                self.make_label(row, slot, 8, MUTED, True, bg=PANEL_ALT).pack(anchor="w")

                value = self.make_label(row, "—", 9, TEXT, bg=PANEL_ALT,

                                        anchor="w", justify="left", wraplength=170)

                value.pack(fill="x", expand=True, pady=(3, 0))

                slot_labels[slot] = value

            self.player_panels.append({"frame": player_panel, "name": name_label,

                                       "color": player_color, "money": money_label,

                                       "progress": progress_label, "slots": slot_labels})

        center = tk.Frame(body, bg=PANEL, padx=20, pady=18)

        center.grid(row=0, column=1, sticky="nsew", padx=4)

        self.turn_label = self.make_label(center, "", 11, ACCENT, True, bg=PANEL)

        self.turn_label.pack(anchor="center")

        self.slot_label = self.make_label(center, "", 20, TEXT, True, bg=PANEL)

        self.slot_label.pack(anchor="center", pady=(8, 14))

        self.character_card = tk.Frame(center, bg=PANEL_ALT, padx=16, pady=18)

        self.character_card.pack(fill="both", expand=True)

        self.make_label(self.character_card, "CURRENT CHARACTER", 9, MUTED, True,

                        bg=PANEL_ALT).pack(pady=(8, 12))

        self.character_name_label = self.make_label(

            self.character_card, "Waiting for draft...", 23, TEXT, True,

            bg=PANEL_ALT, wraplength=440, justify="center"

        )

        self.character_name_label.pack(expand=True, fill="x", padx=10)

        self.anime_tag_label = self.make_label(self.character_card, "", 11, ACCENT,

                                               True, bg=PANEL_ALT, wraplength=440)

        self.anime_tag_label.pack(pady=(12, 8))

        self.status_label = self.make_label(center, "", 10, MUTED, bg=PANEL,

                                            wraplength=470, justify="center")

        self.status_label.pack(fill="x", pady=(12, 6))

        actions = tk.Frame(center, bg=PANEL)

        actions.pack(fill="x", pady=(6, 0))

        bid_area = tk.Frame(actions, bg=PANEL)

        bid_area.pack(side="left", fill="x", expand=True)

        self.make_label(bid_area, "YOUR BID (£)", 9, MUTED, True, bg=PANEL).pack(anchor="w")

        self.bid_entry = tk.Entry(

            bid_area, width=10, font=("Segoe UI", 13, "bold"), bg=PANEL_ALT, fg=TEXT,

            insertbackground=TEXT, relief="flat", justify="center"

        )

        self.bid_entry.pack(anchor="w", ipady=8, pady=(5, 0))

        self.bid_entry.insert(0, "1")

        self.bid_entry.bind("<Return>", lambda _event: self.buy_character())

        self.pass_button = self.make_button(actions, "PASS", self.pass_character,

                                            bg="#2a3652", fg=TEXT)

        self.pass_button.pack(side="right", padx=(6, 0), pady=(16, 0))

        self.buy_button = self.make_button(actions, "PLACE BID", self.buy_character, bg=GREEN)

        self.buy_button.pack(side="right", padx=(6, 0), pady=(16, 0))

        footer = tk.Frame(self.root, bg=BG)

        footer.pack(fill="x", padx=22, pady=(0, 14))

        self.log_label = self.make_label(footer, "", 9, MUTED, bg=BG, anchor="w", wraplength=1080, justify="left")

        self.log_label.pack(fill="x")

    #

    def update_builds(self):

        for index, player in enumerate(self.players):

            panel = self.player_panels[index]

            panel["name"].config(text=player.name, fg=panel["color"])

            panel["money"].config(text=f"£{player.balance}", fg=panel["color"])

            panel["progress"].config(text=f"{len(player.build)}/{len(STAT_SLOTS)} slots filled")

            for slot in STAT_SLOTS:

                entry = player.build.get(slot)

                if entry:

                    character = entry["character"]

                    text = f"{character['name']} [{character['anime']}]"

                    panel["slots"][slot].config(text=text, fg=panel["color"])

                else:

                    panel["slots"][slot].config(text="—", fg=MUTED)

        self.pool_label.config(text=f"{GAME_MODES[self.game_mode].upper()}  |  {len(self.character_pool)} LEFT")

    #

    def prepare_turn(self):

        """Reveal one character and begin an alternating two-player auction."""

        self.free_offer_passer = None

        if all(not player.has_empty_slots() for player in self.players):

            self.finish_game()

            return

        attempts = 0

        while not self.players[self.current_player_index].has_empty_slots() and attempts < 2:

            self.current_player_index = (self.current_player_index + 1) % 2

            attempts += 1

        if not self.character_pool:

            self.finish_game(pool_exhausted=True)

            return

        self.current_character = self.character_pool.pop()

        self.high_bid = 0

        self.high_bidder_index = None

        self.current_slot = self.players[self.current_player_index].next_slot()

        self.update_builds()

        self.show_current_auction()

    #

    def show_current_auction(self):

        player = self.players[self.current_player_index]

        self.current_slot = player.next_slot()

        player_color = PLAYER_COLORS[self.current_player_index]

        self.turn_label.config(

            text=f"{player.name.upper()}'S BID  •  £{player.balance} AVAILABLE",

            fg=player_color

        )

        self.slot_label.config(text=f"Choose for: {self.current_slot}")

        self.character_name_label.config(text=self.current_character["name"])

        self.anime_tag_label.config(text=SERIES_TITLES.get(self.current_character["anime"], self.current_character["anime"]))

        if self.high_bidder_index is None:

            bid_text = "No bids yet. Enter at least £1 to start the auction."

        else:

            leader = self.players[self.high_bidder_index]

            bid_text = f"Highest bid: £{self.high_bid} by {leader.name}. Enter a higher bid or pass to let them win at that price."

        minimum = self.high_bid + 1

        can_bid = player.has_empty_slots() and player.balance >= minimum

        if not player.has_empty_slots():

            bid_text = f"{player.name} has filled all stat slots and cannot bid. Pass to continue."

        elif not can_bid:

            if self.high_bidder_index is None:

                bid_text = f"{player.name} has £{player.balance}. Choose OFFER FREE to offer this character to the other player."

            else:

                bid_text = f"You have £{player.balance} and cannot beat £{self.high_bid}. Pass to close the auction."

        status_color = (PLAYER_COLORS[self.high_bidder_index] if self.high_bidder_index is not None

                        else PLAYER_COLORS[self.current_player_index])

        self.status_label.config(text=bid_text, fg=status_color)

        self.buy_button.config(text="PLACE BID", state="normal" if can_bid else "disabled")

        self.pass_button.config(text="PASS / SETTLE" if self.high_bidder_index is not None else "OFFER FREE", state="normal")

        self.bid_entry.config(state="normal")

        self.bid_entry.delete(0, "end")

        self.bid_entry.insert(0, str(minimum) if can_bid else "0")

        self.bid_entry.config(state="normal" if can_bid else "disabled")

        if can_bid:

            self.bid_entry.focus_set()

        self.update_builds()

    #

    def buy_character(self):

        """Place a bid, then give the other player the next bidding turn."""

        if self.game_finished or self.current_character is None:

            return

        if self.free_offer_passer is not None:
            self.resolve_free_offer(True)
            return

        player = self.players[self.current_player_index]
        if not player.has_empty_slots():
            return

        try:

            bid = int(self.bid_entry.get().strip())

        except ValueError:

            self.status_label.config(text="Enter a whole number for your bid.", fg=RED)

            return

        minimum = self.high_bid + 1

        if bid < minimum:

            self.status_label.config(text=f"Your bid must be at least £{minimum}.", fg=RED)

            return

        if bid > player.balance:

            self.status_label.config(text=f"You only have £{player.balance} available.", fg=RED)

            return

        self.high_bid = bid

        self.high_bidder_index = self.current_player_index

        self.log_label.config(

            text=f"{player.name} bids £{bid} for {self.current_character['name']} "

                 f"[{self.current_character['anime']}].",

            fg=PLAYER_COLORS[self.current_player_index]

        )

        self.current_player_index = (self.current_player_index + 1) % 2

        other = self.players[self.current_player_index]

        if not other.has_empty_slots():

            self.award_character(self.high_bidder_index, self.high_bid)

            return

        if other.balance <= self.high_bid:

            self.award_character(self.high_bidder_index, self.high_bid)

            return

        self.show_current_auction()

    #

    def pass_character(self):
        """Settle the bid or show a free offer inside the character card."""
        if self.game_finished or self.current_character is None:
            return
        if self.free_offer_passer is not None:
            self.resolve_free_offer(False)
            return
        if self.high_bidder_index is not None:
            self.award_character(self.high_bidder_index, self.high_bid)
            return

        passer_index = self.current_player_index
        other_index = 1 - passer_index
        other = self.players[other_index]
        if not other.has_empty_slots():
            self.log_label.config(text=f"{other.name} has no empty slots. Character skipped.")
            self.prepare_turn()
            return

        self.free_offer_passer = passer_index
        color = PLAYER_COLORS[other_index]
        self.turn_label.config(text=f"{other.name.upper()}'S FREE OFFER", fg=color)
        self.slot_label.config(text=f"Take for: {other.next_slot()}")
        self.status_label.config(
            text=f"{self.players[passer_index].name} passed without bidding. "
                 f"{other.name}, take this character for £0 or decline to skip it.", fg=GOLD)
        self.bid_entry.config(state="disabled")
        self.buy_button.config(text="TAKE FREE", state="normal")
        self.pass_button.config(text="DECLINE", state="normal")
        self.buy_button.focus_set()

    def resolve_free_offer(self, accept):
        """Resolve the on-screen offer once, preserving the original turn rules."""
        if self.game_finished or self.current_character is None or self.free_offer_passer is None:
            return
        passer_index = self.free_offer_passer
        other_index = 1 - passer_index
        self.free_offer_passer = None
        if accept:
            self.award_character(other_index, 0)
        else:
            self.log_label.config(
                text=f"{self.players[other_index].name} declined "
                     f"{self.current_character['name']}. Moving to the next character.", fg=MUTED)
            self.current_player_index = passer_index
            self.prepare_turn()

    def award_character(self, winner_index, cost):

        winner = self.players[winner_index]

        character = self.current_character

        slot = winner.next_slot()

        if slot is None:

            self.current_player_index = (winner_index + 1) % 2

            self.prepare_turn()

            return

        winner.add_character(slot, character, cost)

        self.log_label.config(

            text=f"{winner.name} drafted {character['name']} [{character['anime']}] "

                 f"for {slot} at £{cost}."

        )

        self.current_player_index = (winner_index + 1) % 2

        self.prepare_turn()

    #

    def finish_game(self, pool_exhausted=False):

        self.game_finished = True

        self.clear_window()

        outer = tk.Frame(self.root, bg=BG, padx=24, pady=22)

        outer.pack(fill="both", expand=True)

        title = "DRAFT COMPLETE" if not pool_exhausted else "CHARACTER POOL EMPTY"

        self.make_label(outer, title, 23, TEXT, True, bg=BG).pack(pady=(8, 4))

        subtitle = "Compare both builds and decide who wins." if not pool_exhausted else "The pool ran out before both builds were complete."

        self.make_label(outer, subtitle, 10, MUTED, bg=BG).pack(pady=(0, 18))

        columns = tk.Frame(outer, bg=BG)

        columns.pack(fill="both", expand=True)

        columns.grid_columnconfigure(0, weight=1, uniform="final")

        columns.grid_columnconfigure(1, weight=1, uniform="final")

        for i, player in enumerate(self.players):

            panel = tk.Frame(columns, bg=PANEL, padx=18, pady=18)

            panel.grid(row=0, column=i, sticky="nsew", padx=(0, 8) if i == 0 else (8, 0))

            self.make_label(panel, player.name, 16, ACCENT, True, bg=PANEL).pack(anchor="w")

            self.make_label(panel, f"Money remaining: £{player.balance}", 10, GREEN, True, bg=PANEL).pack(anchor="w", pady=(3, 12))

            for slot in STAT_SLOTS:

                entry = player.build.get(slot)

                if entry:

                    character = entry["character"]

                    text = f"{character['name']} [{character['anime']}]\nPaid: £{entry['cost']}"

                    color = TEXT

                else:

                    text = "Not filled"

                    color = MUTED

                row = tk.Frame(panel, bg=PANEL_ALT, padx=10, pady=8)

                row.pack(fill="x", pady=3)

                self.make_label(row, slot.upper(), 8, MUTED, True, bg=PANEL_ALT, width=14, anchor="w").pack(side="left")

                self.make_label(row, text, 9, color, bg=PANEL_ALT, justify="left", wraplength=300, anchor="w").pack(side="left", fill="x", expand=True)

        bottom = tk.Frame(outer, bg=BG)

        bottom.pack(fill="x", pady=(18, 0))

        self.make_button(bottom, "NEW GAME", self.show_setup).pack(side="left")

        self.make_button(bottom, "CLOSE", self.root.destroy, bg="#2a3652", fg=TEXT).pack(side="right")

#

def main():

    root = tk.Tk()

    AnimeDraftGUI(root)

    root.mainloop()

if __name__ == "__main__":

    main()

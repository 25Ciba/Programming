import random
import itertools
import threading
import time
import sys

class Player(): 

    def __init__(self, Playername, Balance):

        self.name = Playername
        self.bal = Balance

    def getBal(self):
        print(f"Account holder: {self.name}")
        print(f"Current balance: £{self.bal}")

    def pay(self, money):

        if money > self.bal:
            print("You cannot buy this character currently.")
        else:
            self.bal -= money 
            print(f"Withdrew £ money}. New balance: £{self.bal}")

def addPlayer():
    inputName = input("Enter account: ").strip()  
    newPlayer = Player(inputName, 20)
    Players.append(newplayer)
    print("Welcome to the game")

def pick():
    

def gameBegin():
    Turn = 1
    addPlayer()
    addPlayer()
    while True:
        print(f"Turn {Turn}. {Players[0]}'s First Pick.")
        print(
            f"""

            Character: {Speed1}
            Money: {Players[0].getBal}

            """
        )


Players = [

]

#=======================================================

AOT = [
    "Eren Yeager",
    "Mikasa Ackerman",
    "Armin Arlert",
    "Levi Ackerman",
    "Erwin Smith",
    "Hange Zoë",
    "Sasha Braus",
    "Jean Kirstein",
    "Connie Springer",
    "Historia Reiss",
    "Ymir",
    "Reiner Braun", 
    "Bertolt Hoover", 
    "Annie Leonhart", 
    "Zeke Yeager", 
    "Grisha Jaeger", 
    "Carla Jaeger", 
    "Kenny Ackerman", 
    "Hannes",
    "Dot Pixis", 
    "Keith Shadis", 
    "Marco Bott", 
    "Floch Forster", 
    "Pieck Finger", 
    "Porco Galliard", 
    "Colt Grice", 
    "Gabi Braun", 
    "Falco Grice", 
    "Theo Magath", 
    "Tom Ksaver",  
    "Lara Tybur", 
    "Ymir Fritz",  
    "Flegel Reeves", 
    "Kiyomi Azumabito", 
    "Niccolo", 
    "Yelena", 
    "Onyankopon"
]

####

JJK = [
    "Kento Nanami",
    "Mei Mei",
    "Ui Ui",
    "Toji Fushiguro",
    "Yuki Tsukumo",
    "Ryu Ishigori",
    "Hajime Kashimo",
    "Hiromi Higuruma",
    "Takuma Ino",
    "Naobito Zenin",
    "Naoya Zenin",
    "Ogi Zenin",
    "Jinichi Zenin",
    "Ranta Zenin",
    "Master Tengen",
    "Ryomen Sukuna",
    "Kenjaku",
    "Suguru Geto",
    "Uraume",
    "Haruta Shigemo",
    "Jiro Awasaka",
    "Juzo Kumiya",
    "Ogami",
    "Shiu Kong",
    "Larue",
    "Mimiko Hasaba",
    "Nanako Hasaba",
    "Junpei Yoshino",
    "Mahito",
    "Jogo",
    "Hanami",
    "Dagon",
    "Choso",
    "Eso",
    "Kechizu",
    "Kurourushi",
    "Rika Orimoto"
]

###

MHA = [
    "Izuku Midoriya (Deku)",
    "Katsuki Bakugo (Great Explosion Murder God Dynamight)",
    "Ochaco Uraraka (Uravity)",
    "Shoto Todoroki (Shoto)",
    "Tenya Ida (Ingenium)",
    "All Might (Toshinori Yagi)",
    "Tomura Shigaraki (Tenko Shimura)",
    "All For One",
    "Eijiro Kirishima (Red Riot)",
    "Tsuyu Asui (Froppy)",
    "Momo Yaoyorozu (Creati)",
    "Fumikage Tokoyami (Tsukuyomi)",
    "Kyoka Jiro (Earphone Jack)",
    "Mina Ashido (Pinky)",
    "Denki Kaminari (Chargebolt)",
    "Mezo Shoji (Tentacole)",
    "Hanto Sero (Cellophane)",
    "Mashirao Ojiro (Tailman)",
    "Minoru Mineta (Grape Juice)",
    "Toru Hagakure (Invisible Girl)",
    "Koji Koda (Anima)",
    "Rikido Sato (Sugarman)",
    "Yuga Aoyama (Cant Stop Twinkling)",
    "Mirio Togata (Lemillion - The Big 3)",
    "Mei Hatsume (Support Course)",
    "Itsuka Kendo (Battle Fist)",
    "Neito Monoma (Phantom Thief)",
    "Endeavor (Enji Todoroki)",
    "Hawks (Keigo Takami)",
    "Eraser Head (Shota Aizawa)",
    "Best Jeanist (Tsunagu Hakamada)",
    "Gran Torino (Sorahiko Torino)",
    "Mirko (Rumi Usagiyama)",
    "Present Mic (Hizashi Yamada)",
    "Midnight (Nemuri Kayama)",
    "Nezu (Principal Nezu)",
    "Recovery Girl (Chiyo Shuzenji)",
    "Kamui Woods (Shinji Nishiya)",
    "Mt. Lady (Yu Takeyama)",
    "Fat Gum (Taishiro Toyomitsu)",
    "Sir Nighteye (Mirai Sasaki)",
    "Gang Orca (Kugo Sakamata)",
    "Dabi (Toya Todoroki)",
    "Himiko Toga",
    "Twice (Jin Bubaigawara)",
    "Kurogiri (Oboro Shirakumo)",
    "Overhaul (Kai Chisaki)",
    "Stain (Chizome Akaguro)",
    "Lady Nagant (Kaina Tsutsumi)",
    "Gentle Criminal (Danjuro Tobita)",
    "Muscular (Goto Imasuji)",
    "Eri"
]

###

OPM = [
    "Saitama", 
    "Genos", 
    "Tatsumaki", 
    "Fubuki", 
    "Bang", 
    "Garou", 
    "King", 
    "Speed-o'-Sound Sonic", 
    "Atomic Samurai", 
    "Metal Bat", 
    "Child Emperor", 
    "Zombieman", 
    "Flashy Flash", 
    "Mumen Rider", 
    "Blast", 
    "Bofoi", 
    "Metal Knight", 
    "Drive Knight", 
    "Pig God", 
    "Watchdog Man", 
    "Superalloy Darkshine", 
    "Tanktop Master", 
    "Puri-Puri Prisoner", 
    "Sweet Mask", 
    "Amai Mask", 
    "Boros", 
    "Orochi", 
    "Psykos", 
    "Monster God", 
    "Empty Void", 
    "Suiryu", 
    "Charanko", 
    "Bomb", 
    "Dr. Kuseno", 
    "Dr. Genus", 
    "Armored Gorilla", 
    "Carnage Kabuto", 
    "Vaccine Man", 
    "Deep Sea King", 
    "Melzargard", 
    "Geryuganshoop", 
    "Groribas", 
    "Crablante", 
    "Stinger", 
    "Lightning Max", 
    "Sneck", 
    "Iaian", 
    "Spring Mustachio", 
    "Golden Ball", 
    "Death Gatling", 
    "Smile Man", 
    "Blue Fire", 
    "Heavy Tank Fundoshi", 
    "Tanktop Tiger", 
    "Tanktop Black Hole", 
    "Gouketsu", 
    "Elder Centipede", 
    "Black Sperm", 
    "Homeless Emperor", 
    "Fuhrer Ugly", 
    "Gums", 
    "Nyan", 
    "Phoenix Man", 
    "Overgrown Rover", 
    "Evil Natural Water", 
    "G4", 
    "G5", 
    "Awakened Cockroach", 
    "Bakuzan", 
    "Choze", 
    "Marshall Gorilla", 
    "Rhino Wrestler", 
    "Royal Ripper", 
    "Bug God", 
    "Pure Blood", 
    "Freezer Man", 
    "Slacker Sid", 
    "Subterranean King", 
    "Sky King", 
    "Ancient King", 
    "Deep Sea King", 
    "Pluton", 
    "Marugori", 
    "Beefcake", 
    "Fukegao", 
    "Hammerhead", 
    "Sonic", 
    "Tareo", 
    "Zenko"
]

###

SL = [
    "Sung Jin-Woo (The Shadow Monarch)",
    "Sung Il-Hwan (Jin-Woo's Father / Vessel of the Rulers)",
    "Cha Hae-In (The Radiant Sword / S-Rank Hunter)",
    "Yoo Jin-Ho (Jin-Woo's Loyal Vice-Guild Master)",
    "Go Gun-Hee (The Association President / Sky Above the Sky)",
    "Thomas Andre (The Goliath / National Level Hunter)",
    "Liu Zhigang (The Hero of China / National Level Hunter)",
    "Christopher Reed (National Level Hunter / Vessel of the Rulers)",
    "Siddharth Bachchan (National Level Hunter)",
    "Jonas (National Level Hunter of Brazil)",
    "Choi Jong-In (The Ultimate Soldier / Master of Hunters Guild)",
    "Baek Yoon-Ho (The White Tiger / Guild Master)",
    "Min Byung-Gu (The Retired S-Rank Healer)",
    "Lim Tae-Gyu (Master of Fiend Guild)",
    "Ma Dong-Wook (Master of Fame Guild)",
    "Yoo Myung-Han (Chairman of Yoojin Construction)",
    "Park Heeo-Jin (B-Rank Mage / Jin-Woo's Early Party Member)",
    "Lee Ju-Hee (B-Rank Healer / Jin-Woo's Friend from the Double Dungeon)",
    "Song Chi-Yeul (C-Rank Mage / The Veteran Sword Elder)",
    "Kim Chul (Iron / High Orc Shadow / A-Rank Tanker)",
    "Hwang Dong-Su (Greed / S-Rank Traitor / Scavenger Guild)",
    "Hwang Dong-Suk (C-Rank Villain / Dong-Su's Brother)",
    "Woo Jin-Chul (The Surveillance Chief / Later Association President)",
    "Han Jae-Gu (A-Rank Hunter of White Tiger Guild)",
    "Kim Gu-Bhim (A-Rank Hunter of White Tiger Guild)",
    "Park Jong-Soo (Master of Knights Guild)",
    "Jeong Yun-Ki (Vice-Master of Knights Guild)",
    "Goto Ryuji (Japan's Strongest S-Rank Hunter)",
    "Reiji Sugimoto (Japanese S-Rank Hunter)",
    "Akari Shimizu (Japanese S-Rank Healer)",
    "Kenzo Tanaka (Japanese S-Rank Brawler)",
    "Kanae Tawata (Japanese S-Rank Assassin)",
    "Minoru Hoshino (Japanese S-Rank Hunter)",
    "Kei (Japanese S-Rank Ice Mage)",
    "Mari Ishida (Japanese S-Rank Hunter)",
    "Kumamoto (Japanese S-Rank Berserker)",
    "Yuri Orloff (The Russian S-Rank Barrier King)",
    "Lennart Niermann (Germany's Top S-Rank Hunter)",
    "Laura (Thomas Andre's Personal Manager)",
    "Selner (The Prophet / Madam Selner)",
    "David Brennon (Director of the Federal Bureau of Hunters)",
    "Gina (American S-Rank Hunter)",
    "Norris (American S-Rank Hunter)",
    "Brent (American S-Rank Hunter)",
    "Jong-Soo's Secretary (Knights Guild Staff)",
    "Sung Jin-Ah (Jin-Woo's Younger Sister)",
    "Park Kyung-Hye (Jin-Woo's Mother)",
    "Yoo Jin-Hee (Jin-Ho's Older Sister)",
    "Han Song-Yi (E-Rank Hunter / Jin-Ah's Friend)",
    "The Architect (The Creator of the System / Ashborn's Servant)",
    "Ashborn (The Original Shadow Monarch)",
    "Antares (The Monarch of Destruction / King of Dragons)",
    "Rakan (The Monarch of Fangs / King of Beasts)",
    "Baruka (The Monarch of White Flames / King of Snow Folk)",
    "Querehsha (The Monarch of Plagues / Queen of Insects)",
    "Yogumunt (The Monarch of Transmutation / King of Demonic Spectres)",
    "Tarnak (The Monarch of Iron Body / King of Monstrous Humanoids)",
    "Sillad (The Monarch of Frost / King of Snow Folk)",
    "Legia (The Monarch of the Beginning / King of Giants)",
    "Absolute Being (The Creator Creator of Monarchs and Rulers)",
    "Igris (The Blood Red Commander / Jin-Woo's Shadow)",
    "Beru (The Shadow Ant King / Jin-Woo's Shadow)",
    "Tusk (The High Orc Shaman Shadow / Jin-Woo's Shadow)",
    "Tank (The Ice Bear Shadow / Jin-Woo's Shadow)",
    "Kaisel (The Shadow Wyvern / Jin-Woo's Mount)",
    "Jima (The Naga Shadow / Jin-Woo's Shadow)",
    "Bellion (The Grand Marshal / Ashborn's Original Shadow)",
    "Kamish (The Shadow Dragon / Humanity's Greatest Calamity)"
]

###

DL = [
    "Tanjirō Kamado", 
    "Nezuko Kamado", 
    "Zenitsu Agatsuma", 
    "Inosuke Hashibira", 
    "Kanao Tsuyuri", 
    "Genya Shinazugawa", 
    "Giyū Tomioka (Water Hashira)", 
    "Shinobu Kochō (Insect Hashira)", 
    "Kyōjurō Rengoku (Flame Hashira)", 
    "Tengen Uzui (Sound Hashira)", 
    "Mitsuri Kanroji (Love Hashira)", 
    "Muichirō Tokitō (Mist Hashira)", 
    "Gyōmei Himejima (Stone Hashira)", 
    "Obanai Iguro (Serpent Hashira)", 
    "Sanemi Shinazugawa (Wind Hashira)", 
    "Muzan Kibutsuji (Demon King)", 
    "Kokushibō (Upper Moon One)", 
    "Dōma (Upper Moon Two)", 
    "Akaza (Upper Moon Three)", 
    "Hantengu (Upper Moon Four)", 
    "Gyokko (Upper Moon Five)", 
    "Gyūtarō (Upper Moon Six)", 
    "Daki (Upper Moon Six)", 
    "Kaigaku (Upper Moon Six)", 
    "Nakime (Upper Moon Four)", 
    "Enmu (Lower Moon One)", 
    "Rui (Lower Moon Five)", 
    "Kyōgai (Former Lower Moon Six)", 
    "Sakonji Urokodaki (Former Water Hashira)", 
    "Jigorō Kuwajima (Former Roaring Hashira)", 
    "Shinjurō Rengoku (Former Flame Hashira)", 
    "Kanae Kochō (Former Flower Hashira)", 
    "Yoriichi Tsugikuni (Creator of Sun Breathing)", 
    "Tamayo (Demon Doctor)", "Yushirō (Tamayo's Assistant)", 
    "Murata (Demon Slayer Corps Member)", 
    "Aoi Kanzaki (Butterfly Mansion Helper)", 
    "Sumi Nakahara (Butterfly Mansion Helper)", 
    "Kiyo Terauchi (Butterfly Mansion Helper)", 
    "Naho Takada (Butterfly Mansion Helper)", 
    "Sabo (Demon Slayer Cadet)", 
    "Makomo (Demon Slayer Cadet)", 
    "Hotaru Haganezuka (Swordsmith)", 
    "Kozo Kanamori (Swordsmith)", 
    "Kotetsu (Swordsmith Village Resident)", 
    "Tecchin Tecchikawahara (Swordsmith Village Chief)", 
    "Hinatsuru (Tengen's Wife)", 
    "Makuo (Tengen's Wife)", 
    "Suma (Tengen's Wife)", 
    "Kagaya Ubuyashiki (Master of the Mansion)", 
    "Amane Ubuyashiki (Kagaya's Wife)", 
    "Kiriya Ubuyashiki (Kagaya's Son)", 
    "Kanata Ubuyashiki (Kagaya's Daughter)", 
    "Kuina Ubuyashiki (Kagaya's Daughter)", 
    "Nichika Ubuyashiki (Kagaya's Daughter)", 
    "Hinaki Ubuyashiki (Kagaya's Daughter)", 
    "Susamaru (Temari Demon)", 
    "Yahaba (Arrow Demon)", 
    "Spider Demon Mother (Spider Family)", 
    "Spider Demon Father (Spider Family)", 
    "Spider Demon Brother (Spider Family)", 
    "Spider Demon Sister (Spider Family)", 
    "Hand Demon (Final Selection Demon)", 
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
    "Tsutako Tomioka (Giyū's Sister)"
]

###

BL = [
    "Yoichi Isagi"
    "Meguru Bachira"
    "Rensuke Kunigami"
    "Hyoma Chigiri"
    "Rin Itoshi"
    "Sae Itoshi"
    "Seishiro Nagi"
    "Reo Mikage"
    "Zantetsu Tsurugi"
    "Shouei Barou"
    "Gin Gagamaru"
    "Jingo Raichi"
    "Gurimu Igarashi"
    "Asahi Naruhaya"
    "Wataru Kuon"
    "Okuhito Iemon"
    "Yudai Imamura"
    "Ryosuke Kira"
    "Jin Kiyora"
    "Ikki Niko"
    "Junichi Wanima"
    "Keisuke Wanima"
    "Ryusei Shidou"
    "Tabito Karasu"
    "Eita Otoya"
    "Kenyu Yukimiya"
    "Yo Hiyori"
    "Nijiro Nanase"
    "Kurona Ranze"
    "Aoshi Tokimitsu"
    "Jubei Aryu"
    "Anri Teieri"
    "Jinpachi Ego"
    "Yasuhito Fukaku"
    "Oliver Aiku"
    "Shuto Sendo"
    "Kazuma Niou"
    "Teppei Neru"
    "Kento Cho"
    "Teru Kitsunezato"
    "Itsuki Wakatsuki"
    "Haru Hayate"
    "Taiga Tsunzaki"
    "Miroku Darai"
    "Shingen Tanaka"
    "Noel Noa"
    "Chris Prince"
    "Lavinho"
    "Marc Snuffy"
    "Julian Loki"
    "Michael Kaiser"
    "Alexis Ness"
    "Benedict Grim"
    "Erik Gesner"
    "Mensah"
    "Birkenstock"
    "Agi"
    "Don Lorenzo"
    "Drago"
    "Charles Chevalier"
    "Leonardo Luna"
    "Pablo Cavasoz"
    "Adam Blake"
    "Dada Silva"
]

#=================================================================

a = random.choice(AOT)
b = random.choice(JJK)
c = random.choice(MHA)
d = random.choice(OPM)
e = random.choice(SL)
f = random.choice(DL)
g = random.choice(BL)
h = random.choice(AOT)
i = random.choice(JJK)
j = random.choice(MHA)
k = random.choice(OPM)
l = random.choice(SL)
m = random.choice(DL)
n = random.choice(BL)

#

All = [a, b, c, d, e, f, g, h, i, j, k, l, m, n]
pot = random.shuffle()

#

Speed1 = pot[0]
speed2 = pot[1]
Intelligence1 = pot[2]
Intelligence2 = pot[3]
Strength1 = pot[4]
Strength2 = pot[5]
Defence1 = pot[6]
Defence2 = pot[7]
Endurance1 = pot[8]
Endurance2 = pot[9]
Ability1 = pot[10]
Ability2 = pot[11]
Willpower1 = pot[12]
Willpower2 = pot[13]




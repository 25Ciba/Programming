Ruins = [
    "Blue-gray_ruins1.png",
    "Sand_ruins1.png"
    "Snow_ruins4.png"
]

class Ruins():
    
    def __init__():
        
        def Generate_Ruins(self):

            roll = random.randint(1, 100)

            ##

            # 70% Common
            if roll <= 70:
                enemy_type = "Common"

            ##

            # 20% Strong
            elif roll <= 90:
                enemy_type = "Strong"

            ##

            # 8% Elite
            elif roll <= 98:
                enemy_type = "Elite"

            ##

            # 2% Boss
            else:
                enemy_type = "Boss"

            ##

            ruin = Enemy(self.screen, enemy_type, self.player)
            self.enemies.append(enemy)

        #

        def render(self):
            for enemy in self.enemies:
                enemy.render()

# CLASS Item

#     ATTRIBUTES
#         name
#         description
#         itemType
#         damage
#         defence
#         value
#         buyPrice
#         sellPrice


#     FUNCTION initialise(name, description, itemType, damage, defence, value)

#         SET name to name
#         SET description to description
#         SET itemType to itemType
#         SET damage to damage
#         SET defence to defence
#         SET value to value

#         SET buyPrice to value
#         SET sellPrice to value * 0.5

#     END FUNCTION

# END CLASS



# CLASS Inventory

#     ATTRIBUTES
#         items
#         mainHand
#         offHand
#         helmet
#         chestplate
#         leggings
#         boots
#         charm


#     FUNCTION initialise()

#         SET items to empty list

#         SET mainHand to empty
#         SET offHand to empty
#         SET helmet to empty
#         SET chestplate to empty
#         SET leggings to empty
#         SET boots to empty
#         SET charm to empty

#     END FUNCTION


#     FUNCTION addItem(item)

#         ADD item to items

#     END FUNCTION


#     FUNCTION removeItem(item)

#         IF item is in items THEN
#             REMOVE item from items
#         END IF

#     END FUNCTION


#     FUNCTION equipItem(item)

#         IF item.itemType = "Helmet" THEN
#             SET helmet to item

#         ELSE IF item.itemType = "Chestplate" THEN
#             SET chestplate to item

#         ELSE IF item.itemType = "Leggings" THEN
#             SET leggings to item

#         ELSE IF item.itemType = "Boots" THEN
#             SET boots to item

#         ELSE IF item.itemType = "MainHand" THEN
#             SET mainHand to item

#         ELSE IF item.itemType = "OffHand" THEN
#             SET offHand to item

#         ELSE IF item.itemType = "Charm" THEN
#             SET charm to item

#         ELSE
#             DISPLAY "Item cant be equiped"
#         END IF

#     END FUNCTION


#     FUNCTION removeEquippedItem(slot)

#         IF slot = "Helmet" THEN
#             SET helmet to empty

#         ELSE IF slot = "Chestplate" THEN
#             SET chestplate to empty

#         ELSE IF slot = "Leggings" THEN
#             SET leggings to empty

#         ELSE IF slot = "Boots" THEN
#             SET boots to empty

#         ELSE IF slot = "MainHand" THEN
#             SET mainHand to empty

#         ELSE IF slot = "OffHand" THEN
#             SET offHand to empty

#         ELSE IF slot = "Charm" THEN
#             SET charm to empty
#         END IF

#     END FUNCTION


#     FUNCTION getItem(slot)

#         IF slot = "Helmet" THEN
#             RETURN helmet

#         ELSE IF slot = "Chestplate" THEN
#             RETURN chestplate

#         ELSE IF slot = "Leggings" THEN
#             RETURN leggings

#         ELSE IF slot = "Boots" THEN
#             RETURN boots

#         ELSE IF slot = "MainHand" THEN
#             RETURN mainHand

#         ELSE IF slot = "OffHand" THEN
#             RETURN offHand

#         ELSE IF slot = "Charm" THEN
#             RETURN charm
#         END IF

#     END FUNCTION


#     FUNCTION displayInventory()

#         DISPLAY items
#         DISPLAY "Main Hand:", mainHand
#         DISPLAY "Off Hand:", offHand
#         DISPLAY "Helmet:", helmet
#         DISPLAY "Chestplate:", chestplate
#         DISPLAY "Leggings:", leggings
#         DISPLAY "Boots:", boots
#         DISPLAY "Charm:", charm

#     END FUNCTION

# END CLASS



# CLASS Store

#     ATTRIBUTES
#         storeName
#         storeInventory
#         playerInventory
#         playerMoney


#     FUNCTION initialise(storeName, playerInventory)

#         SET storeName to storeName
#         SET storeInventory to empty list
#         SET playerInventory to playerInventory
#         SET playerMoney to 0

#     END FUNCTION


#     FUNCTION addItemToStore(item, price)

#         SET item.buyPrice to price
#         ADD item to storeInventory

#     END FUNCTION


#     FUNCTION buyFromStore(item)

#         IF item is in storeInventory THEN

#             IF playerMoney >= item.buyPrice THEN

#                 REMOVE item.buyPrice from playerMoney
#                 REMOVE item from storeInventory
#                 CALL playerInventory.addItem(item)

#                 DISPLAY "Item purchased"

#             ELSE
#                 DISPLAY "Not enough money"
#             END IF

#         ELSE
#             DISPLAY "Item is not avalible"
#         END IF

#     END FUNCTION


#     FUNCTION sellToStore(item)

#         IF item is in playerInventory.items THEN

#             CALL playerInventory.removeItem(item)

#             ADD item.sellPrice to playerMoney
#             ADD item to storeInventory

#             DISPLAY "Item sold"

#         ELSE
#             DISPLAY "You do not have this item"
#         END IF

#     END FUNCTION


#     FUNCTION displayStore()

#         DISPLAY storeName
#         DISPLAY playerMoney

#         DISPLAY "Items for sale:"

#         FOR each item in storeInventory
#             DISPLAY item.name
#             DISPLAY item.buyPrice
#         END FOR

#         DISPLAY "Your items:"

#         FOR each item in playerInventory.items
#             DISPLAY item.name
#             DISPLAY item.sellPrice
#         END FOR

#     END FUNCTION


#     FUNCTION update()

#         CALL displayStore()

#         IF player selects an item from store THEN
#             CALL buyFromStore(selected item)

#         ELSE IF player selects an item from player inventory THEN
#             CALL sellToStore(selected item)

#         END IF

#     END FUNCTION

# END CLASS



# CLASS MapSystem

#     ATTRIBUTES
#         mapImage
#         mapPosition
#         mapSize
#         normalSize
#         enlargedSize
#         isEnlarged


#     FUNCTION initialise()

#         SET mapImage to map image
#         SET mapPosition to top right of screen

#         SET normalSize to small map dimensions
#         SET enlargedSize to large map dimensions

#         SET mapSize to normalSize
#         SET isEnlarged to FALSE

#     END FUNCTION


#     FUNCTION displayMap()

#         DISPLAY mapImage at mapPosition
#         SET mapImage size to mapSize

#     END FUNCTION


#     FUNCTION enlargeMap()

#         IF isEnlarged = FALSE THEN
#             SET mapSize to enlargedSize
#             SET isEnlarged to TRUE
#         END IF

#     END FUNCTION


#     FUNCTION minimiseMap()

#         IF isEnlarged = TRUE THEN
#             SET mapSize to normalSize
#             SET isEnlarged to FALSE
#         END IF

#     END FUNCTION


#     FUNCTION handleClick(mousePosition)

#         IF mousePosition is inside map THEN

#             IF isEnlarged = FALSE THEN
#                 CALL enlargeMap()

#             ELSE
#                 CALL minimiseMap()

#             END IF

#         END IF

#     END FUNCTION


#     FUNCTION update(mousePosition)

#         CALL handleClick(mousePosition)
#         CALL displayMap()

#     END FUNCTION

# END CLASS



# CLASS InteractionSystem

#     ATTRIBUTES
#         interactionKey
#         nearbyObject


#     FUNCTION initialise()

#         SET interactionKey to "INTERACT"
#         SET nearbyObject to empty

#     END FUNCTION


#     FUNCTION findNearbyObject(player)

#         SEARCH for interactable objects near player

#         IF an interactable object is found THEN
#             SET nearbyObject to closest interactable object
#         ELSE
#             SET nearbyObject to empty
#         END IF

#     END FUNCTION


#     FUNCTION displayInteractionPrompt()

#         IF nearbyObject is not empty THEN
#             DISPLAY "Press [INTERACT] to interact"
#         END IF

#     END FUNCTION


#     FUNCTION interact()

#         IF nearbyObject is not empty THEN
#             CALL nearbyObject.interact()
#         END IF

#     END FUNCTION


#     FUNCTION update(player, input)

#         CALL findNearbyObject(player)
#         CALL displayInteractionPrompt()

#         IF input = interactionKey THEN
#             CALL interact()
#         END IF

#     END FUNCTION

# END CLASS



# CLASS Door

#     ATTRIBUTES
#         isOpen


#     FUNCTION initialise()

#         SET isOpen to FALSE

#     END FUNCTION


#     FUNCTION interact()

#         IF isOpen = FALSE THEN

#             SET isOpen to TRUE
#             OPEN door

#         ELSE

#             SET isOpen to FALSE
#             CLOSE door

#         END IF

#     END FUNCTION

# END CLASS



# CLASS Chest

#     ATTRIBUTES
#         inventory
#         isOpen


#     FUNCTION initialise()

#         SET inventory to empty list
#         SET isOpen to FALSE

#     END FUNCTION


#     FUNCTION interact()

#         IF isOpen = FALSE THEN

#             SET isOpen to TRUE
#             DISPLAY chest inventory

#         ELSE

#             CLOSE chest
#             SET isOpen to FALSE

#         END IF

#     END FUNCTION

# END CLASS



# CLASS NPC

#     ATTRIBUTES
#         name
#         dialogue


#     FUNCTION initialise(name, dialogue)

#         SET name to name
#         SET dialogue to dialogue

#     END FUNCTION


#     FUNCTION interact()

#         DISPLAY dialogue

#     END FUNCTION

# END CLASS



# CLASS Shop

#     ATTRIBUTES
#         store


#     FUNCTION initialise(store)

#         SET store to store

#     END FUNCTION


#     FUNCTION interact()

#         CALL store.update()

#     END FUNCTION

# END CLASS



# CLASS Player

#     ATTRIBUTES
#         inventory
#         money
#         position


#     FUNCTION initialise()

#         CREATE new Inventory
#         SET inventory to new Inventory

#         SET money to 0
#         SET position to starting position

#     END FUNCTION


#     FUNCTION pickUpItem(item)

#         CALL inventory.addItem(item)

#     END FUNCTION


#     FUNCTION equip(item)

#         IF item is in inventory.items THEN
#             CALL inventory.equipItem(item)
#         END IF

#     END FUNCTION

# END CLASS



# CLASS Game

#     ATTRIBUTES
#         player
#         map
#         interactionSystem
#         store
#         gameObjects


#     FUNCTION initialise()

#         CREATE Player
#         SET player to new Player

#         CREATE MapSystem
#         SET map to new MapSystem

#         CREATE InteractionSystem
#         SET interactionSystem to new InteractionSystem

#         CREATE Store
#         SET store to new Store using player.inventory

#         SET gameObjects to empty list

#     END FUNCTION


#     FUNCTION addGameObject(object)

#         ADD object to gameObjects

#     END FUNCTION


#     FUNCTION update(input, mousePosition)

#         CALL interactionSystem.update(player, input)
#         CALL map.update(mousePosition)

#         UPDATE player

#     END FUNCTION


#     FUNCTION run()

#         WHILE game is running

#             GET player input
#             GET mouse position

#             CALL update(input, mousePosition)

#             DISPLAY game

#         END WHILE

#     END FUNCTION

# END CLASS


# -------------

# CLASS General Settings

#     ATTRIBUTES
#         musicVolume
#         sfxVolume
#         ambientVolume

#         controls


#     FUNCTION initialise()

#         SET musicVolume to 100
#         SET sfxVolume to 100
#         SET ambientVolume to 100

#         SET controls to default controls

#     END FUNCTION


#     FUNCTION setMusicVolume(volume)

#         IF volume >= 0 AND volume <= 100 THEN
#             SET musicVolume to volume
#         END IF

#     END FUNCTION


#     FUNCTION setSFXVolume(volume)

#         IF volume >= 0 AND volume <= 100 THEN
#             SET sfxVolume to volume
#         END IF

#     END FUNCTION


#     FUNCTION setAmbientVolume(volume)

#         IF volume >= 0 AND volume <= 100 THEN
#             SET ambientVolume to volume
#         END IF

#     END FUNCTION


#     FUNCTION changeControl(action, key)

#         SET controls[action] to key

#     END FUNCTION


#     FUNCTION resetControls()

#         SET controls to default controls

#     END FUNCTION


#     FUNCTION displaySettings()

#         DISPLAY "SETTINGS"

#         DISPLAY "Music Volume"
#         DISPLAY music volume slider

#         DISPLAY "SFX Volume"
#         DISPLAY SFX volume slider

#         DISPLAY "Ambient Volume"
#         DISPLAY ambient volume slider

#         DISPLAY "CONTROLS"

#         FOR each control in controls
#             DISPLAY control action and assigned key
#         END FOR

#     END FUNCTION


#     FUNCTION update(input)

#         IF player moves music volume slider THEN
#             CALL setMusicVolume(selected volume)
#         END IF

#         IF player moves SFX volume slider THEN
#             CALL setSFXVolume(selected volume)
#         END IF

#         IF player moves ambient volume slider THEN
#             CALL setAmbientVolume(selected volume)
#         END IF

#         IF player selects a control THEN
#             CALL changeControl(selected action, selected key)
#         END IF

#     END FUNCTION

# END CLASS

# -----------------------

# CLASS MainMenu

#     ATTRIBUTES
#         player
#         settings
#         game


#     FUNCTION initialise()

#         CREATE player
#         CREATE settings
#         CREATE game

#     END FUNCTION


#     FUNCTION display()

#         DISPLAY "MAIN MENU"

#         DISPLAY "NEW GAME"
#         DISPLAY "LOAD GAME"
#         DISPLAY "GENERAL SETTINGS"
#         DISPLAY "QUIT"

#     END FUNCTION


#     FUNCTION update()

#         CALL display()

#         IF New_Game is selected THEN
#             CALL startNewGame()

#         ELSE IF Load_Game is selected THEN
#             CALL loadGame()

#         ELSE IF General_Settings is selected THEN
#             OPEN General Settings

#         ELSE IF Quit is selected THEN
#             CALL quitGame()

#         END IF

#     END FUNCTION


#     FUNCTION startNewGame()

#         CREATE NewGame
#         CALL NewGame.start()

#     END FUNCTION


#     FUNCTION loadGame()

#         LOAD latest saved game

#         IF save file exists THEN
#             LOAD player data
#             LOAD game progress
#             START gameplay

#         ELSE
#             DISPLAY "No save game found"
#         END IF

#     END FUNCTION


#     FUNCTION quitGame()

#         SET gameRunning to FALSE

#     END FUNCTION

# END CLASS



# CLASS NewGame

#     ATTRIBUTES
#         player


#     FUNCTION initialise(player)

#         SET player to player

#     END FUNCTION


#     FUNCTION start()

#         CALL clanSelection()

#         CALL characterSelection()

#         CALL fragmentSelection()

#         CALL chooseStart()

#     END FUNCTION


#     FUNCTION clanSelection()

#         DISPLAY "CLAN SELECTION"

#         DISPLAY Mage
#         DISPLAY Tank
#         DISPLAY Fighter
#         DISPLAY Assassin
#         DISPLAY Summoner
#         DISPLAY Marksman


#         IF Mage is selected THEN
#             SET player.clan to Mage

#         ELSE IF Tank is selected THEN
#             SET player.clan to Tank

#         ELSE IF Fighter is selected THEN
#             SET player.clan to Fighter

#         ELSE IF Assassin is selected THEN
#             SET player.clan to Assassin

#         ELSE IF Summoner is selected THEN
#             SET player.clan to Summoner

#         ELSE IF Marksman is selected THEN
#             SET player.clan to Marksman

#         END IF

#     END FUNCTION


#     FUNCTION characterSelection()

#         DISPLAY "CHARACTER SELECTION"

#         DISPLAY male character
#         DISPLAY female character

#         IF male character is selected THEN

#             SET player.character to Male
#             SET player.characterColour to player.clan colour

#         ELSE IF female character is selected THEN

#             SET player.character to Female
#             SET player.characterColour to player.clan colour

#         END IF

#     END FUNCTION


#     FUNCTION fragmentSelection()

#         DISPLAY "FRAGMENT SELECTION"

#         DISPLAY Piano
#         DISPLAY Guitar
#         DISPLAY Flute
#         DISPLAY Harp
#         DISPLAY Cello
#         DISPLAY Violin


#         IF Piano is selected THEN
#             SET player.fragment to Piano

#         ELSE IF Guitar is selected THEN
#             SET player.fragment to Guitar

#         ELSE IF Flute is selected THEN
#             SET player.fragment to Flute

#         ELSE IF Harp is selected THEN
#             SET player.fragment to Harp

#         ELSE IF Cello is selected THEN
#             SET player.fragment to Cello

#         ELSE IF Violin is selected THEN
#             SET player.fragment to Violin

#         END IF

#     END FUNCTION


#     FUNCTION chooseStart()

#         DISPLAY "TUTORIAL"
#         DISPLAY "START GAME"

#         IF Tutorial is selected THEN

#             CALL Tutorial.start()

#             CALL Gameplay.start(player)

#         ELSE IF Start_Game is selected THEN

#             CALL Gameplay.start(player)

#         END IF

#     END FUNCTION

# END CLASS



# CLASS Gameplay

#     ATTRIBUTES
#         player
#         inventory
#         map
#         interactionSystem
#         gameObjects
#         store
#         gameRunning
#         score
#         coins
#         timeSurvived
#         areasCleared


#     FUNCTION initialise(player)

#         SET player to player
#         SET inventory to player.inventory

#         CREATE MapSystem
#         SET map to MapSystem

#         CREATE InteractionSystem
#         SET interactionSystem to InteractionSystem

#         CREATE Store using player.inventory
#         SET store to Store

#         SET score to 0
#         SET coins to 0
#         SET timeSurvived to 0
#         SET areasCleared to 0

#         SET gameRunning to TRUE

#     END FUNCTION


#     FUNCTION start(player)

#         CALL initialise(player)

#         WHILE gameRunning = TRUE

#             CALL update()
#             CALL display()

#         END WHILE

#         CALL endGame()

#     END FUNCTION


#     FUNCTION update()

#         GET player input
#         GET mouse position

#         CALL interactionSystem.update(player, input)

#         CALL map.update(mouse position)

#         UPDATE player

#         UPDATE enemies

#         UPDATE areas

#         UPDATE music

#         UPDATE ambient sounds

#         IF Settings button is selected THEN
#             OPEN General Settings
#         END IF

#         IF Save_Game is selected THEN
#             CALL saveGame()
#             SET gameRunning to FALSE
#         END IF

#         IF Exit_Game is selected THEN
#             SET gameRunning to FALSE
#         END IF

#     END FUNCTION


#     FUNCTION display()

#         DISPLAY player
#         DISPLAY enemies
#         DISPLAY environment

#         DISPLAY map

#         DISPLAY health
#         DISPLAY score
#         DISPLAY coins

#     END FUNCTION


#     FUNCTION saveGame()

#         SAVE player data
#         SAVE inventory
#         SAVE player position
#         SAVE score
#         SAVE coins
#         SAVE areasCleared
#         SAVE timeSurvived

#         DISPLAY "Game Saved"

#     END FUNCTION


#     FUNCTION endGame()

#         CALL ResultsScreen.display(
#             score,
#             coins,
#             timeSurvived,
#             areasCleared
#         )

#         RETURN TO MainMenu

#     END FUNCTION

# END CLASS



# CLASS Tutorial

#     FUNCTION start()

#         DISPLAY tutorial introduction

#         DISPLAY movement instructions
#         DISPLAY combat instructions
#         DISPLAY interaction instructions
#         DISPLAY inventory instructions
#         DISPLAY map instructions
#         DISPLAY music fragment instructions

#         WAIT until tutorial is completed

#     END FUNCTION

# END CLASS



# CLASS ResultsScreen

#     FUNCTION display(score, coins, timeSurvived, areasCleared)

#         DISPLAY "GAME COMPLETE"

#         DISPLAY "Score: " + score
#         DISPLAY "Coins: " + coins
#         DISPLAY "Time Survived: " + timeSurvived
#         DISPLAY "Areas Cleared: " + areasCleared

#         WAIT for player

#     END FUNCTION

# END CLASS



# CLASS SaveSystem

#     FUNCTION saveGame(player, score, coins, timeSurvived, areasCleared)

#         SAVE player information
#         SAVE player inventory
#         SAVE player equipment
#         SAVE player position

#         SAVE score
#         SAVE coins
#         SAVE timeSurvived
#         SAVE areasCleared

#         WRITE all information to save file

#     END FUNCTION


#     FUNCTION loadGame()

#         READ save file

#         IF save file exists THEN

#             LOAD player information
#             LOAD inventory
#             LOAD equipment
#             LOAD player position

#             LOAD score
#             LOAD coins
#             LOAD timeSurvived
#             LOAD areasCleared

#             RETURN loaded game

#         ELSE

#             RETURN no save found

#         END IF

#     END FUNCTION

# END CLASS



# CLASS Game

#     ATTRIBUTES
#         mainMenu
#         gameRunning


#     FUNCTION initialise()

#         CREATE MainMenu
#         SET mainMenu to MainMenu

#         SET gameRunning to TRUE

#     END FUNCTION


#     FUNCTION run()

#         WHILE gameRunning = TRUE

#             CALL mainMenu.update()

#         END WHILE

#     END FUNCTION

# END CLASS
CLASS Item

    ATTRIBUTES
        name
        description
        itemType
        damage
        defence
        value
        buyPrice
        sellPrice

    FUNCTION initialise(name, description, itemType, damage, defence, value)

        SET name to name
        SET description to description
        SET itemType to itemType
        SET damage to damage
        SET defence to defence
        SET value to value
        SET buyPrice to value
        SET sellPrice to value * 0.5

    END FUNCTION

END CLASS



CLASS Inventory

    ATTRIBUTES
        items
        mainHand
        offHand
        helmet
        chestplate
        leggings
        boots
        charm

    FUNCTION initialise()

        SET items to empty list
        SET mainHand to empty
        SET offHand to empty
        SET helmet to empty
        SET chestplate to empty
        SET leggings to empty
        SET boots to empty
        SET charm to empty

    END FUNCTION

    FUNCTION addItem(item)

        ADD item to items

    END FUNCTION

    FUNCTION removeItem(item)

        IF item is in items THEN
            REMOVE item from items
        END IF

    END FUNCTION

    FUNCTION equipItem(item)

        IF item.itemType = "Helmet" THEN
            SET helmet to item
        ELSE IF item.itemType = "Chestplate" THEN
            SET chestplate to item
        ELSE IF item.itemType = "Leggings" THEN
            SET leggings to item
        ELSE IF item.itemType = "Boots" THEN
            SET boots to item
        ELSE IF item.itemType = "MainHand" THEN
            SET mainHand to item
        ELSE IF item.itemType = "OffHand" THEN
            SET offHand to item
        ELSE IF item.itemType = "Charm" THEN
            SET charm to item
        ELSE
            DISPLAY "Item cant be equiped"
        END IF

    END FUNCTION

    FUNCTION removeEquippedItem(slot)

        IF slot = "Helmet" THEN
            SET helmet to empty
        ELSE IF slot = "Chestplate" THEN
            SET chestplate to empty
        ELSE IF slot = "Leggings" THEN
            SET leggings to empty
        ELSE IF slot = "Boots" THEN
            SET boots to empty
        ELSE IF slot = "MainHand" THEN
            SET mainHand to empty
        ELSE IF slot = "OffHand" THEN
            SET offHand to empty
        ELSE IF slot = "Charm" THEN
            SET charm to empty
        END IF

    END FUNCTION

    FUNCTION getItem(slot)

        IF slot = "Helmet" THEN
            RETURN helmet
        ELSE IF slot = "Chestplate" THEN
            RETURN chestplate
        ELSE IF slot = "Leggings" THEN
            RETURN leggings
        ELSE IF slot = "Boots" THEN
            RETURN boots
        ELSE IF slot = "MainHand" THEN
            RETURN mainHand
        ELSE IF slot = "OffHand" THEN
            RETURN offHand
        ELSE IF slot = "Charm" THEN
            RETURN charm
        END IF

    END FUNCTION

    FUNCTION displayInventory()

        DISPLAY items
        DISPLAY "Main Hand:", mainHand
        DISPLAY "Off Hand:", offHand
        DISPLAY "Helmet:", helmet
        DISPLAY "Chestplate:", chestplate
        DISPLAY "Leggings:", leggings
        DISPLAY "Boots:", boots
        DISPLAY "Charm:", charm

    END FUNCTION

END CLASS



CLASS Store

    ATTRIBUTES
        storeName
        storeInventory
        playerInventory
        playerMoney


    FUNCTION initialise(storeName, playerInventory)

        SET storeName to storeName
        SET storeInventory to empty list
        SET playerInventory to playerInventory
        SET playerMoney to 0

    END FUNCTION


    FUNCTION addItemToStore(item, price)

        SET item.buyPrice to price
        ADD item to storeInventory

    END FUNCTION


    FUNCTION buyFromStore(item)

        IF item is in storeInventory THEN

            IF playerMoney >= item.buyPrice THEN

                REMOVE item.buyPrice from playerMoney
                REMOVE item from storeInventory
                CALL playerInventory.addItem(item)

                DISPLAY "Item purchased"

            ELSE
                DISPLAY "Not enough money"
            END IF

        ELSE
            DISPLAY "Item is not avalible"
        END IF

    END FUNCTION


    FUNCTION sellToStore(item)

        IF item is in playerInventory.items THEN

            CALL playerInventory.removeItem(item)

            ADD item.sellPrice to playerMoney
            ADD item to storeInventory

            DISPLAY "Item sold"

        ELSE
            DISPLAY "You do not have this item"
        END IF

    END FUNCTION


    FUNCTION displayStore()

        DISPLAY storeName
        DISPLAY playerMoney

        DISPLAY "Items for sale:"

        FOR each item in storeInventory
            DISPLAY item.name
            DISPLAY item.buyPrice
        END FOR

        DISPLAY "Your items:"

        FOR each item in playerInventory.items
            DISPLAY item.name
            DISPLAY item.sellPrice
        END FOR

    END FUNCTION


    FUNCTION update()

        CALL displayStore()

        IF player selects an item from store THEN
            CALL buyFromStore(selected item)

        ELSE IF player selects an item from player inventory THEN
            CALL sellToStore(selected item)

        END IF

    END FUNCTION

END CLASS

rere

CLASS MapSystem

    ATTRIBUTES
        mapImage
        mapPosition
        mapSize
        normalSize
        enlargedSize
        isEnlarged


    FUNCTION initialise()

        SET mapImage to map image
        SET mapPosition to top right of screen

        SET normalSize to small map dimensions
        SET enlargedSize to large map dimensions

        SET mapSize to normalSize
        SET isEnlarged to FALSE

    END FUNCTION


    FUNCTION displayMap()

        DISPLAY mapImage at mapPosition
        SET mapImage size to mapSize

    END FUNCTION


    FUNCTION enlargeMap()

        IF isEnlarged = FALSE THEN
            SET mapSize to enlargedSize
            SET isEnlarged to TRUE
        END IF

    END FUNCTION


    FUNCTION minimiseMap()

        IF isEnlarged = TRUE THEN
            SET mapSize to normalSize
            SET isEnlarged to FALSE
        END IF

    END FUNCTION


    FUNCTION handleClick(mousePosition)

        IF mousePosition is inside map THEN

            IF isEnlarged = FALSE THEN
                CALL enlargeMap()

            ELSE
                CALL minimiseMap()

            END IF

        END IF

    END FUNCTION


    FUNCTION update(mousePosition)

        CALL handleClick(mousePosition)
        CALL displayMap()

    END FUNCTION

END CLASS




CLASS Shop

    ATTRIBUTES
        store


    FUNCTION initialise(store)

        SET store to store

    END FUNCTION


    FUNCTION interact()

        CALL store.update()

    END FUNCTION

END CLASS


CLASS Game

    ATTRIBUTES
        player
        map
        interactionSystem
        store
        gameObjects


    FUNCTION initialise()

        CREATE Player
        SET player to new Player

        CREATE MapSystem
        SET map to new MapSystem

        CREATE InteractionSystem
        SET interactionSystem to new InteractionSystem

        CREATE Store
        SET store to new Store using player.inventory

        SET gameObjects to empty list

    END FUNCTION


    FUNCTION addGameObject(object)

        ADD object to gameObjects

    END FUNCTION


    FUNCTION update(input, mousePosition)

        CALL interactionSystem.update(player, input)
        CALL map.update(mousePosition)

        UPDATE player

    END FUNCTION


    FUNCTION run()

        WHILE game is running

            GET player input
            GET mouse position

            CALL update(input, mousePosition)

            DISPLAY game

        END WHILE

    END FUNCTION

END CLASS


CLASS ResultsScreen

    FUNCTION display(score, coins, timeSurvived, areasCleared)

        DISPLAY "GAME COMPLETE"

        DISPLAY "Score: " + score
        DISPLAY "Coins: " + coins
        DISPLAY "Time Survived: " + timeSurvived
        DISPLAY "Areas Cleared: " + areasCleared

        WAIT for player

    END FUNCTION

END CLASS



CLASS SaveSystem

    FUNCTION saveGame(player, score, coins, timeSurvived, areasCleared)

        SAVE player information
        SAVE player inventory
        SAVE player equipment
        SAVE player position

        SAVE score
        SAVE coins
        SAVE timeSurvived
        SAVE areasCleared

        WRITE all information to save file

    END FUNCTION


    FUNCTION loadGame()

        READ save file

        IF save file exists THEN

            LOAD player information
            LOAD inventory
            LOAD equipment
            LOAD player position

            LOAD score
            LOAD coins
            LOAD timeSurvived
            LOAD areasCleared

            RETURN loaded game

        ELSE

            RETURN no save found

        END IF

    END FUNCTION

END CLASS



CLASS Game

    ATTRIBUTES
        mainMenu
        gameRunning


    FUNCTION initialise()

        CREATE MainMenu
        SET mainMenu to MainMenu

        SET gameRunning to TRUE

    END FUNCTION


    FUNCTION run()

        WHILE gameRunning = TRUE

            CALL mainMenu.update()

        END WHILE

    END FUNCTION

END CLASS
STEP-1

use gameDB

db.createCollection("players")
db.createCollection("items")
db.createCollection("purchases")
db.createCollection("membership")


STEP-2

db.players.insertMany([
    {
      "PlayerID": 1,
      "Username": "Goku",
      "Email": "goku@dbz.com",
      "Level": 99,
      "Coins": 1000,
      "MembershipType": "VIP",
      "MembershipExpiry": "2026-03-29",
      "MatchesPlayed": 200,
      "Wins": 150,
      "XP": 12000
    },
    {
      "PlayerID": 2,
      "Username": "Vegeta",
      "Email": "vegeta@dbz.com",
      "Level": 95,
      "Coins": 850,
      "MembershipType": "Free",
      "MembershipExpiry": "2025-03-29",
      "MatchesPlayed": 150,
      "Wins": 120,
      "XP": 11000
    },
    {
      "PlayerID": 3,
      "Username": "Gohan",
      "Email": "gohan@dbz.com",
      "Level": 85,
      "Coins": 700,
      "MembershipType": "Free",
      "MembershipExpiry": "2025-03-29",
      "MatchesPlayed": 180,
      "Wins": 130,
      "XP": 10000
    },
    {
      "PlayerID": 4,
      "Username": "Piccolo",
      "Email": "piccolo@dbz.com",
      "Level": 90,
      "Coins": 900,
      "MembershipType": "VIP",
      "MembershipExpiry": "2026-03-29",
      "MatchesPlayed": 190,
      "Wins": 140,
      "XP": 10500
    },
    {
      "PlayerID": 5,
      "Username": "Trunks",
      "Email": "trunks@dbz.com",
      "Level": 80,
      "Coins": 600,
      "MembershipType": "Free",
      "MembershipExpiry": "2025-03-29",
      "MatchesPlayed": 120,
      "Wins": 100,
      "XP": 9500
    },
    {
      "PlayerID": 6,
      "Username": "Frieza",
      "Email": "frieza@dbz.com",
      "Level": 100,
      "Coins": 1200,
      "MembershipType": "VIP",
      "MembershipExpiry": "2026-03-29",
      "MatchesPlayed": 220,
      "Wins": 180,
      "XP": 13000
    },
    {
      "PlayerID": 7,
      "Username": "Cell",
      "Email": "cell@dbz.com",
      "Level": 98,
      "Coins": 1100,
      "MembershipType": "VIP",
      "MembershipExpiry": "2026-03-29",
      "MatchesPlayed": 210,
      "Wins": 170,
      "XP": 12500
    },
    {
      "PlayerID": 8,
      "Username": "Majin Buu",
      "Email": "buu@dbz.com",
      "Level": 75,
      "Coins": 500,
      "MembershipType": "Free",
      "MembershipExpiry": "2025-03-29",
      "MatchesPlayed": 100,
      "Wins": 90,
      "XP": 8000
    },
    {
      "PlayerID": 9,
      "Username": "Krillin",
      "Email": "krillin@dbz.com",
      "Level": 70,
      "Coins": 450,
      "MembershipType": "Free",
      "MembershipExpiry": "2025-03-29",
      "MatchesPlayed": 90,
      "Wins": 80,
      "XP": 7000
    },
    {
      "PlayerID": 10,
      "Username": "Yamcha",
      "Email": "yamcha@dbz.com",
      "Level": 65,
      "Coins": 400,
      "MembershipType": "Free",
      "MembershipExpiry": "2025-03-29",
      "MatchesPlayed": 70,
      "Wins": 60,
      "XP": 6500
    }
  ]
  )

  db.items.insertMany([
    {
      "ItemID": 1,
      "ItemName": "Saiyan Armor",
      "Price": 500
    },
    {
      "ItemID": 2,
      "ItemName": "Z-Sword",
      "Price": 1000
    },
    {
      "ItemID": 3,
      "ItemName": "Dragon Radar",
      "Price": 300
    },
    {
      "ItemID": 4,
      "ItemName": "Power Boost",
      "Price": 700
    },
    {
      "ItemID": 5,
      "ItemName": "Instant Transmission",
      "Price": 1200
    },
    {
      "ItemID": 6,
      "ItemName": "Sensu Beans",
      "Price": 200
    },
    {
      "ItemID": 7,
      "ItemName": "Kaioken Power-Up",
      "Price": 1500
    },
    {
      "ItemID": 8,
      "ItemName": "Majin Mark",
      "Price": 800
    },
    {
      "ItemID": 9,
      "ItemName": "Energy Shield",
      "Price": 600
    },
    {
      "ItemID": 10,
      "ItemName": "Super Saiyan Aura",
      "Price": 1000
    }
  ]
  )

  db.purchases.insertMany([
    {
      "PlayerID": 1,
      "ItemsPurchased": ["Saiyan Armor", "Z-Sword"],
      "PurchaseDate": "2024-04-01",
      "TotalPrice": 1500
    },
    {
      "PlayerID": 2,
      "ItemsPurchased": ["Saiyan Armor"],
      "PurchaseDate": "2024-04-02",
      "TotalPrice": 500
    },
    {
      "PlayerID": 3,
      "ItemsPurchased": ["Z-Sword", "Dragon Radar"],
      "PurchaseDate": "2024-04-03",
      "TotalPrice": 1300
    },
    {
      "PlayerID": 4,
      "ItemsPurchased": ["Dragon Radar"],
      "PurchaseDate": "2024-04-04",
      "TotalPrice": 300
    }
  ]
  )

  db.membership.insertMany([
    {
      "PlayerID": 1,
      "MembershipType": "VIP",
      "MembershipExpiry": "2026-03-29"
    },
    {
      "PlayerID": 2,
      "MembershipType": "Free",
      "MembershipExpiry": "2025-03-29"
    },
    {
      "PlayerID": 3,
      "MembershipType": "Free",
      "MembershipExpiry": "2025-03-29"
    },
    {
      "PlayerID": 4,
      "MembershipType": "VIP",
      "MembershipExpiry": "2026-03-29"
    }
  ]
  )
  STEP-3  

//1. Find the player with the highest level

db.players.find().sort({level:-1}).limit(1)

//2. Retrieve players who have more than 1000 coins

db.players.find({Coins: {$gt : 1000}})

//3. Find all VIP members

db.players.find({MembershipType : 'VIP'})

//4. Create index on player

db.players.createIndex({title: 1})


//5.Retrieve all players sorted by level in descending order

db.players.find().sort({level:-1})

STEP - 4

//Update a player’s level and coins

db.players.updateOne({playerID : 1},{$set : {level: 110, Coins: 4000}} )

//Delete a player account

db.players.deleteOne({playerID: 10})

STEP - 5

// Create an index on usernames for faster lookups

db.items.createIndex({username: 1})


STEP - 6

// We chose to embed frequently accessed and closely related data,
// such as a player's list of friends, directly within the player document.
// This approach allows for quick access and reduces the need for joins. 
// In contrast, we referenced larger and more independent data, like in-game purchases,
// by storing it in a separate collection (items).
// This method improves scalability, simplifies updates, and enables better data reuse. 
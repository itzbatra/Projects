CREATE TABLE "Attribution" (
	"AttributionID"	INTEGER,
	"Level"	INTEGER NOT NULL,
	"Coins"	INTEGER NOT NULL,
	"MatchesPlayed"	INTEGER NOT NULL,
	"Wins"	INTEGER NOT NULL,
	"XP"	INTEGER NOT NULL,
	PRIMARY KEY("AttributionID")
);

CREATE TABLE "Membership" (
	"MembershipID"	INTEGER,
	"MembershipType"	TEXT NOT NULL,
	"MembershipExpiry"	TEXT NOT NULL,
	PRIMARY KEY("MembershipID")
);

CREATE TABLE "Players" (
	"PlayerID"	INTEGER,
	"Username"	TEXT NOT NULL,
	"Email"	TEXT NOT NULL,
	"AttributionID"	INTEGER,
	PRIMARY KEY("PlayerID"),
	FOREIGN KEY("AttributionID") REFERENCES "Attribution"("AttributionID")
);

CREATE TABLE "PurchasedItem" (
	"ItemID"	INTEGER,
	"ItemName"	TEXT NOT NULL,
	"ItemPrice"	INTEGER NOT NULL,
	PRIMARY KEY("ItemID")
);

CREATE TABLE "Transactions" (
	"transaction_ID"	INTEGER,
	"PlayerID"	INTEGER,
	"ItemID"	INTEGER,
	PRIMARY KEY("transaction_ID"),
	FOREIGN KEY("ItemID") REFERENCES "PurchasedItem"("ItemID"),
	FOREIGN KEY("PlayerID") REFERENCES "Players"("PlayerID")
);

INSERT INTO "Attribution" (AttributionID, Level, Coins, MatchesPlayed, wins, XP)
SELECT * FROM "attribution_tab";

INSERT INTO "Membership" (MembershipID, MembershipType, MembershipExpiry)
SELECT * FROM "members_tab";

INSERT INTO "PurchasedItem" (ItemID, ItemName, ItemPrice)
SELECT * FROM "purchasedItem_tab";

INSERT INTO "Players" (PlayerID, Username, Email, AttributionID)
SELECT * FROM "players_tab";

INSERT INTO "Transactions" ("transaction_ID", "PlayerID", "ItemID")
SELECT * FROM "TransactionID_tab";

STEP - 4 TRIGGER AND VIEWS 


CREATE TRIGGER "assign_free_membership"
AFTER INSERT ON "Players"
FOR EACH ROW
BEGIN
    INSERT INTO "Membership" ("MembershipType", "MembershipExpiry")
    VALUES ('Free', '2025-03-29');
END;

CREATE VIEW "VIP_Members" AS
SELECT "Players"."PlayerID", "Players"."Username",  "Players"."Email", 
    "Membership"."MembershipType", "Membership"."MembershipExpiry"
FROM "Players" JOIN 
    "Membership" ON "Players"."PlayerID" = "Membership"."MembershipID"
WHERE 
    "Membership"."MembershipType" = 'VIP';

STEP-5

CREATE INDEX "Players_Username" ON "Players"(Username);

STEP-6
BEGIN TRANSACTION;

UPDATE "Attribution"
SET "Coins" = "Coins" - 500
WHERE "AttributionID" = (SELECT "AttributionID" FROM "Players" WHERE "PlayerID" = 2)
AND "Coins" >= 500;

    ROLLBACK;


STEP- 7

---The player with highest level
SELECT "PlayerID", "Username", "Level" FROM "Players" 
JOIN "Attribution" ON "Players"."AttributionID" = "Attribution"."AttributionID"
ORDER BY Level DESC LIMIT 1;

---Retrieve players who have played more than 50 matches

SELECT "PlayerID", "Username"
FROM "Players" JOIN "Attribution" ON "Players"."AttributionID" = "Attribution"."AttributionID"
WHERE "MatchesPlayed" > 50;

--Show all stats of users ranked top 10 in one of the stat
SELECT "PlayerID", "Username", "Level", "Coins", "MatchesPlayed", "Wins", "XP"
FROM "Players" JOIN "Attribution" ON "Players"."AttributionID" = "Attribution"."AttributionID"
ORDER BY "XP" DESC LIMIT 10;

--Calculate total coins owned by all players

SELECT SUM("Coins") AS "Total_Coins"
FROM "Attribution";

---Find all VIP members
---Since I have created an index AS VIP_Members so 5th query can be done in two ways 

SELECT "PlayerID", "Username", "MembershipType", "MembershipExpiry"
FROM "Players" JOIN "Membership" ON "PlayerID" = "MembershipID"
WHERE "MembershipType" = 'VIP';

OR

SELECT * FROM "VIP_Members";



db = db.getSiblingDB("app")
db.createCollection("words")

db.createUser(
    {
        user: "words-reader",
        pwd: "dev",
        roles: [
            {
                role: "read",
                db: "app"
            }
        ]
    }
);

db.createUser(
    {
        user: "words-writer",
        pwd: "dev",
        roles: [
            {
                role: "readWrite",
                db: "app"
            }
        ]
    }
);

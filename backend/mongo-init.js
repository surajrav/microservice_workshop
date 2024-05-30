db.createUser({
    user: "dev_user",
    pwd: "dev_pass",
    roles: [{ role: "readWrite", db: "ion"  }]
});
db.createCollection('users', { capped: false });

db = db.getSiblingDB('todo');
db.createUser({
    user: "dev_user",
    pwd: "dev_pass",
    roles: [{ role: "readWrite", db: "ion"  }]
});
db.createCollection('todos', { capped: false });
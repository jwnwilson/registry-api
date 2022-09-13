db.createUser({
  user: 'admin',
  pwd: 'password',
  roles: [
      {
          role: 'readWrite',
          db: 'registry',
      },
  ],
});

db = new Mongo().getDB("registry");

var collections = ['users', 'entityType', 'entity'];

for (var i=0; i< collections.length; i++) {
  var table = collections[i];
  db.createCollection(table, { capped: false });
  db[table].createIndex( { "owner": 1, "uuid": 1 }, { unique: true } );
  db[table].createIndex( { "owner": 1, "name": 1 }, { unique: true } );
}

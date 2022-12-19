function createCollections(db) {
  var collections = ['entityType', 'entity'];

  for (var i=0; i< collections.length; i++) {
    var table = collections[i];
    db.createCollection(table, { capped: false });
    db[table].createIndex( { "uuid": 1 }, { unique: true } );
    if (table === 'entity') {
      db[table].createIndex( { "name": 1, "entityType": 1 }, { unique: true } );
    } else {
      db[table].createIndex( { "name": 1 }, { unique: true } );
    }
  }
}

// Local DB setup
db.createUser({
  user: 'admin',
  pwd: 'password',
  roles: [
      {
          role: 'readWrite',
          db: 'registry',
      }
  ],
});

db = new Mongo().getDB("registry");

createCollections(db);

// Add entity types
db.entityType.insert({
  "name": "Product",
  "description": "A product that the organisation supports",
  "uuid": "c1607de2-6257-463a-bf69-2709ec7450e4",
  "fields": {
    "product_number": {
      "name": "product_number",
      "uuid": "18560f88-3e4c-4e7b-a5d0-6360774f3d59",
      "data_type": "string",
      "input_type": "text",
      "default": "",
      "description": "",
      "choices": [],
      "required": false
    }
  },
  "links": {}
});
db.entityType.insert({
  "name": "Supplier",
  "description": "A supplier that the organisation supports",
  "uuid": "b8f63b68-585d-49e3-82b5-45f2a7e33fba",
  "fields": {
    "supplier_number": {
      "name": "supplier_number",
      "uuid": "6f19b3d7-4175-44a4-8c22-6a3619daa5b0",
      "data_type": "number",
      "input_type": "text",
      "default": "",
      "description": "",
      "choices": [],
      "required": false
    }
  },
  "links": {}
});
db.entityType.insert({
  "name": "User",
  "description": "A user",
  "uuid": "f04afe93-759d-4139-bead-3adc7c77ee04",
  "fields": {
    "name": {
      "name": "name",
      "uuid": "3977bed3-6fc6-4a59-aadd-bc50d5601fdf",
      "data_type": "string",
      "input_type": "text",
      "default": "",
      "description": "",
      "choices": [],
      "required": false
    }, "email": {
      "name": "email",
      "uuid": "2f030b0e-f7d7-44f0-aeac-13a0817ecf6a",
      "data_type": "string",
      "input_type": "text",
      "default": "",
      "description": "",
      "choices": [],
      "required": false
    }
  },
  "links": {}
});

// Add entities
db.entity.insert({
  "name": "Product 1",
  "description": "Test product 1",
  "entity_type": "Product",
  "uuid": "4d4d036f-0c62-4b43-b01f-48a5304f0195",
  "fields": {
    "product_number": "abc"
  },
  "links": {}
});
db.entity.insert({
  "name": "Supplier 1",
  "description": "Test supplier 1",
  "entity_type": "Supplier",
  "uuid": "7e717bdb-edc1-4f0a-b211-7aeccc793647",
  "fields": {
    "supplier_number": 1234
  },
  "links": {}
});
db.entity.insert({
  "name": "Text User 1",
  "description": "Test supplier 1",
  "entity_type": "User",
  "uuid": "71e03252-58bc-461e-b0d6-610c1b538a38",
  "fields": {
    "name": "testy mcgee",
    "email": "test.com"
  },
  "links": {}
});

// Test DB setup
db = db.getSiblingDB("test_db");
db.createUser({
  user: 'admin',
  pwd: 'password',
  roles: [
      {
          role: 'readWrite',
          db: 'test_db',
      }
  ],
});

createCollections(db);

const { MongoClient } = require('mongodb');
const config = require('./config.json'); 

collection = undefined;

async function initMongo()
{
    try
    {
        const mongoClient = new MongoClient(config.connStr);
        var conn = await mongoClient.connect();
        var database = mongoClient.db("depression");
        collection = database.collection(config.accessorsDTb);
        
        // const query = { text: "Этот год был очень трудным...." };
        // const res = await collection.findOne(query);
        // console.log(res);                
    }
    catch(e){ console.log(e) }
}

async function getRandom()
{            
    var cursor = await collection.aggregate([{ $sample: { size: 10 } }]);
    
    var res = undefined;
    await cursor.forEach(
        doc => 
        {            
            if(res == undefined || res.result.length > doc.result.length)
                res = doc
        }
    );    
    //console.log( await collection.findOne({_id:res._id}));

    return {text: res.text, id:res._id, age:res.age, result: res.result};
}

async function updateEntry(txt, status)
{        
    var filter = {_id: txt};    
    const res = await collection.findOne(filter);        
    res.result.push(status);
    
    const options = { upsert: true };    
    const updateDoc = {
      $set: res
    };
    
    const result = await collection.updateOne(filter, updateDoc, options);    
    
    console.log(
      `${result.matchedCount} document(s) matched the filter, updated ${result.modifiedCount} document(s)`,
    );  
}

module.exports = {
    init: initMongo,
    get: getRandom,
    update: updateEntry
}
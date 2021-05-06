const mysql = require('mysql');

var conn = mysql.createConnection({
    host: "remotemysql.com",
    username: "LMhwjDOQr9",
    password: "iIykidkeEl",
    database: "LMhwjDOQr9"
});

conn.connect((err) => {
    if(error){
        console.log("Something went wrong with connection!");
        throw err;
    }else{
        console.log("Successfully connection!");
    }
});
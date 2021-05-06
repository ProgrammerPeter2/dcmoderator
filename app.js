const express = require("express");
const app = express();
const path = require("path");
const mysql = require("mysql")
const router = express.Router();

app.set("view engine", "pug");
app.set("views", path.join(__dirname, "views"));

router.get("/", (req, res) => {
  res.render("index");
});

router.get('/login', (req, res) => {
    //get loggig datas
    let dataurl = req.url.split('/login?')[1];
    let datas = dataurl.split('&');
    let uname = datas[0].split('=')[1];
    let password = datas[1].split('=')[1];
    //mysql connection
    var conn = mysql.createConnection({
        host: "remotemysql.com",
        username: "LMhwjDOQr9",
        password: "iIykidkeEl",
        database: "LMhwjDOQr9"
    });
    
    conn.connect((error) => {
        if(error){
            console.log("Something went wrong with connection!");
            throw error;
        }else{
            console.log("Successfully connection!");
        }
    });
    //mysql query
    let sql = `select * from users where username=${uname} and password=${password}`
    conn.query(sql, (error, result) => {
        if(error){
            throw error;
        }
        console.log(result)
    });
    //console.log(result);
    console.log(`Logged user as ${uname}`);
    res.redirect("/home?user="+uname);
});

router.get('/home', (req, res) => {
    let dataurl = req.url.split('/home?')[1];
    let username = dataurl.split('=')[1]
    let msg = "Hello " + username;
    res.render("home", {message: msg})
})
app.use("/", router);
const port = process.env.port || 5000
app.listen(port);

console.log(`Running at Port ${port}`);
const express = require('express');
var path = require('path');

const app = express();

app.use(express.static(path.join(__dirname, 'dist/startup-generator-client')));

app.get('*', function(req, res) {
    res.sendFile(path.join(__dirname, 'dist/startup-generator-client/index.html'));
});

app.listen(8081, () => {
    console.log('Server started on port 8081');
});

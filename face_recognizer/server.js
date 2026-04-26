const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = 5000;

app.use(cors());
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

let attendanceLogs = [];

// Python calls this to log a face
app.post('/api/attendance', (req, res) => {
    const { name, timestamp } = req.body;
    
    // Toggle Logic: Find last status for this person
    const userEntries = attendanceLogs.filter(log => log.name === name);
    const lastStatus = userEntries.length > 0 ? userEntries[0].status : "OUT";
    const newStatus = lastStatus === "IN" ? "OUT" : "IN";

    const entry = { name, timestamp, status: newStatus };
    attendanceLogs.unshift(entry); 
    
    console.log(`[EVENT] ${name} marked ${newStatus} at ${timestamp}`);
    res.status(200).json({ status: newStatus });
});

// Browser calls this to get logs
app.get('/api/logs', (req, res) => {
    res.json(attendanceLogs);
});

app.listen(PORT, () => {
    console.log(`🚀 Dashboard server running at http://localhost:${PORT}`);
});
// server.js
const express = require('express');
const multer = require('multer');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process'); // Import child_process module

const app = express();
const PORT = process.env.PORT || 3000;

// Configure storage using multer
const storage = multer.diskStorage({
    destination: (req, file, cb) => cb(null, 'uploads/'), // Specify the uploads directory
    filename: (req, file, cb) => cb(null, `${Date.now()}-${file.originalname}`) // Create a unique filename
});

// File filter to accept only PDF and Word files
const fileFilter = (req, file, cb) => {
    const fileTypes = /pdf|doc|docx/; // Allowed file types
    const isValid = fileTypes.test(path.extname(file.originalname).toLowerCase()) && fileTypes.test(file.mimetype);
    cb(null, isValid);
};

const upload = multer({ storage, fileFilter });

// Serve static files from the frontend directory
app.use(express.static(path.join(__dirname, 'frontend')));

// Middleware to delete previous files before uploading new one
const clearUploadsFolder = (req, res, next) => {
    fs.readdir('uploads', (err, files) => {
        if (err) return res.status(500).send('Internal Server Error');
        const deletePromises = files.map(file => 
            fs.promises.unlink(path.join('uploads', file)).catch(e => console.error('Error deleting file:', e))
        );
        Promise.all(deletePromises).then(() => next()).catch(() => res.status(500).send('Internal Server Error during cleanup'));
    });
};

// Handle file upload
app.post('/upload', clearUploadsFolder, upload.single('file'), (req, res) => {
    if (!req.file) return res.status(400).send('No file uploaded or file not supported.');
    console.log('File uploaded successfully:', req.file); // Log file info
    const clean_process = spawn('python', ['clean_neo.py'])
    console.log("Cleared the Neo4J");
    console.log("Initiating.......");
    
    const pythonProcess = spawn('python', ['init.py']); // Use 'python' or 'python3' as needed
    

    pythonProcess.stdout.on('data', (data) => {
        console.log(`Python output: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python script finished with code ${code}`);
    });

    res.json({ success: true }); // Send a JSON response to indicate success
});

// Start the server
app.listen(PORT, () => console.log(`Server is running on http://localhost:${PORT}`));
